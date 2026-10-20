import json
from datetime import date
from pathlib import Path
import subprocess
import sys
import stat
import tempfile
import unittest

from scan_log import canonical_url, merge_rows


class ScanLogTests(unittest.TestCase):
    today = date(2030, 5, 10)

    def row(self, job="12345678", when="2030-05-10", title="Example role"):
        return {"url": f"https://nz.seek.com/job/{job}", "title": title, "date_scanned": when}

    def test_tracking_parameters_and_aliases(self):
        self.assertEqual(canonical_url("https://www.seek.co.nz/job/12345678?token=discard#x"),
                         "https://nz.seek.com/job/12345678")

    def test_retention_boundary(self):
        rows = [self.row("1", "2030-05-05"), self.row("2", "2030-05-06")]
        self.assertEqual(merge_rows(rows, [], self.today), [rows[1]])

    def test_repeat_does_not_refresh_date(self):
        old = self.row(when="2030-05-07")
        new = self.row(title="New title")
        self.assertEqual(merge_rows([old], [new], self.today), [old])

    def test_expired_url_can_be_scanned_again(self):
        new = self.row()
        self.assertEqual(merge_rows([self.row(when="2030-05-01")], [new], self.today), [new])

    def test_only_three_fields(self):
        bad = {**self.row(), "email": "synthetic@example.invalid"}
        with self.assertRaises(ValueError):
            merge_rows([], [bad], self.today)

    def test_future_date_rejected(self):
        with self.assertRaises(ValueError):
            merge_rows([], [self.row(when="2030-05-11")], self.today)

    def test_other_domain_rejected(self):
        with self.assertRaises(ValueError):
            canonical_url("https://example.invalid/job/12345678")

    def test_application_url_rejected(self):
        with self.assertRaises(ValueError):
            canonical_url("https://nz.seek.com/job/12345678/apply")

    def test_zero_port_rejected(self):
        with self.assertRaises(ValueError):
            canonical_url("https://nz.seek.com:0/job/12345678")

    def test_empty_username_rejected(self):
        with self.assertRaises(ValueError):
            canonical_url("https://@nz.seek.com/job/12345678")

    def test_lock_symlink_cannot_change_other_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            other = root / 'unrelated.txt'
            other.write_text('preserve me')
            other.chmod(0o644)
            (root / '.scan-log.lock').symlink_to(other)
            proc = subprocess.run([sys.executable, str(Path(__file__).with_name('scan_log.py')),
                                   'prune', '--root', tmp, '--today', '2030-05-10'],
                                  capture_output=True)
            self.assertEqual(proc.returncode, 2)
            self.assertEqual(stat.S_IMODE(other.stat().st_mode), 0o644)
            self.assertEqual(other.read_text(), 'preserve me')
            self.assertFalse((root / 'Scanned Jobs.json').exists())

    def test_bad_input_does_not_erase_existing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            log = root / "Scanned Jobs.json"
            original = json.dumps([self.row()])
            log.write_text(original)
            bad = root / "bad.json"
            bad.write_text('{"wrong":"shape"}')
            proc = subprocess.run([sys.executable, str(Path(__file__).with_name("scan_log.py")),
                                   "merge", "--root", tmp, "--today", "2030-05-10",
                                   "--input", str(bad)], capture_output=True)
            self.assertEqual(proc.returncode, 2)
            self.assertEqual(log.read_text(), original)

    def test_pruning_does_not_touch_application_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "private").mkdir()
            history = root / "private" / "application-history.json"
            history.write_text('[{"status":"submitted"}]')
            subprocess.run([sys.executable, str(Path(__file__).with_name("scan_log.py")),
                            "prune", "--root", tmp, "--today", "2030-05-10"],
                           check=True, capture_output=True)
            self.assertEqual(history.read_text(), '[{"status":"submitted"}]')


if __name__ == "__main__":
    unittest.main()
