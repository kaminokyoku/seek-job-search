"""Maintain the three-field recent scan cache. Never submits applications."""

import argparse
from contextlib import contextmanager
from datetime import date, timedelta
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from urllib.parse import urlsplit


FIELDS = {"url", "title", "date_scanned"}


def canonical_url(value):
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in {
        "nz.seek.com", "seek.co.nz", "www.seek.co.nz"
    } or parsed.username is not None or parsed.password is not None or parsed.port is not None:
        raise ValueError("Expected a public SEEK New Zealand job URL")
    match = re.fullmatch(r"/job/(\d+)/?", parsed.path)
    if not match:
        raise ValueError("Expected /job/<numeric-id>, not an application or search URL")
    return f"https://nz.seek.com/job/{match.group(1)}"


def validate(rows, today):
    if not isinstance(rows, list):
        raise ValueError("Scan log must be a JSON array")
    clean = []
    for row in rows:
        if not isinstance(row, dict) or set(row) != FIELDS:
            raise ValueError("Each row must contain only url, title and date_scanned")
        if not all(isinstance(row[k], str) for k in FIELDS):
            raise ValueError("All three scan fields must be strings")
        when = date.fromisoformat(row["date_scanned"])
        if when.isoformat() != row["date_scanned"] or when > today:
            raise ValueError("Invalid or future scan date")
        title = row["title"].strip()
        if not title:
            raise ValueError("A visible job title is required")
        clean.append({"url": canonical_url(row["url"]), "title": title,
                      "date_scanned": when.isoformat()})
    return clean


def merge_rows(existing, incoming, today):
    cutoff = today - timedelta(days=4)
    rows = validate(existing, today) + validate(incoming, today)
    kept = {}
    for row in rows:
        if date.fromisoformat(row["date_scanned"]) < cutoff:
            continue
        old = kept.get(row["url"])
        # Keep the first retained observation; repeat sightings must not extend TTL.
        if old is None or row["date_scanned"] < old["date_scanned"]:
            kept[row["url"]] = row
    return sorted(kept.values(), key=lambda r: (r["date_scanned"], r["url"]))


@contextmanager
def locked(root):
    import fcntl
    lock_path = root / ".scan-log.lock"
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ValueError("Scan lock must be a regular, unlinked file")
        os.fchmod(fd, 0o600)
        fcntl.flock(fd, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


def atomic_write(path, rows):
    fd, tmp = tempfile.mkstemp(prefix=".scans-", suffix=".json", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(rows, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prune", "merge", "contains"])
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--today", required=True, type=date.fromisoformat)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--url")
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error("Root must be an existing, explicitly selected Jobs directory")
    if args.action == "merge" and not args.input:
        parser.error("merge requires --input")
    if args.action == "contains" and not args.url:
        parser.error("contains requires --url")
    try:
        incoming = json.loads(args.input.read_text(encoding="utf-8")) if args.action == "merge" else []
        target = canonical_url(args.url) if args.action == "contains" else None
        path = args.root / "Scanned Jobs.json"
        if path.is_symlink():
            raise ValueError("Refusing to replace a symlinked scan log")
        with locked(args.root):
            existing = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
            rows = merge_rows(existing, incoming, args.today)
            if args.action == "contains":
                result = {"seen": any(r["url"] == target for r in rows),
                          "application_status": "not_checked"}
            else:
                atomic_write(path, rows)
                result = {"rows": len(rows), "path": str(path)}
        print(json.dumps(result))
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Scan log unchanged: {exc}\n")


if __name__ == "__main__":
    main()
