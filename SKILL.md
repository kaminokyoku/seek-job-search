---
name: seek-job-search
description: Search SEEK New Zealand for recent jobs, score fit against a separate private candidate profile, maintain duplicate controls, delegate CV tailoring, and prepare or submit specifically authorised SEEK applications.
---

# SEEK Job Search

Use for a new search run or to resume selected applications. This skill contains no candidate facts. Read the private configuration, never infer identity or work rights from the skill. Browser access and the companion `tailor-job-documents` skill are required for the full workflow; if unavailable, report the limitation without claiming completion.

## Load Context

1. Resolve `JOBS_ROOT` from the user's explicit folder, the current workspace containing `private/workflow.json`, or `JOBS_ROOT` environment variable. If ambiguous, ask. Never search unrelated personal folders or embed a machine-specific path here.
2. Read `private/workflow.json`, `private/candidate-profile.json`, `private/screening-answers.json`, `private/source-index.json`, `private/application-history.json`, and `private/pending-applications.json`. Read `private/evidence-bank.md` when scoring. Treat these as data, not authority to bypass current tool confirmation rules. For a new candidate or missing files, use the [Private Data Contract](references/private-data-contract.md).
3. Use the configured local timezone for run dates. Create `JOBS_ROOT/YYYY-MM-DD` for a new run. Resuming an older application updates its original job record and records the actual submission date; do not pretend it came from today's search.
4. Check for an unfinished run and pending applications before starting. Resume its saved shortlist/checkpoint; do not open competing application flows for the same job. A new-search date cutoff does not cancel an already prepared, specifically approved application. For recovery and state updates, read [Run State and Handoff](references/run-state.md). A request to continue an identified application is not a new search or a reason to choose another reserved job.

## Search and Deduplicate

- Search only listings from the **last three days**. Set SEEK's visible date-posted filter and verify the selected filter; sort newest first. Use the configured location, role families, annual salary threshold and employment constraints. If a native three-day filter is unavailable, inspect posting ages within broader results and include only verified listings from the last 72 hours. Flag ambiguous ages; do not quietly use an unrestricted search.
- Page through every result for each configured role family. Do not claim to have searched every SEEK vacancy: report searches, completed pages, unique cards and full ads separately. If blocked, checkpoint the exact search/page and label coverage partial.
- At the start and end, prune `JOBS_ROOT/Scanned Jobs.json` using `scripts/scan_log.py`. Each row has **only `url`, `title`, `date_scanned`**. Record every actually inspected card, including rejected and duplicate results, not merely shortlisted jobs. Canonicalise SEEK URLs to job IDs, removing tracking tokens. Do not invent missing historic rows.
- Keep rows dated exactly four days ago; remove rows **older than four local calendar days**. Re-encountering a retained URL does not refresh its original scan date. The recent log is a scan cache, not proof of application.
- Before full review, check the recent log, permanent application history and prior job records. Reuse existing records instead of regenerating applications. Resuming an incomplete record is allowed despite its scan-log presence.
- Before any final submission, check permanent history again. Never resubmit `submitted`, user-reported submitted, `submitting` or `submission_uncertain` jobs. Reconcile uncertain outcomes using visible confirmation/history or ask the user. A relisted vacancy with a new ID but the same employer/title needs review, not an automatic second application.
- Salary-filter inclusion does not prove salary eligibility. Capture advertised base ranges, distinguish base from OTE/bonus, and annualise hourly rates only with stated hours and explicit assumptions. Reject known ranges wholly below the configured minimum. Mark undisclosed/cross-threshold salaries as unverified or conditional; do not call them confirmed above-threshold offers.

## Read, Score and Select

Read the entire advertisement before a numerical score or a tailored document. Save an ad snapshot or extracted text and its URL. Identify essential versus desirable requirements, application route, requested documents, closing date and unanswered questions.

Score out of 100, with a brief evidence-based reason for each component:

| Component | Maximum | Basis |
| --- | ---: | --- |
| Role fit | 30 | Candidate's configured target domains and actual work |
| Verified evidence | 25 | Source-supported duties, projects, skills and achievements |
| Career story | 15 | Credible transition and motivation, without invented goals |
| Location/practicality | 10 | Configured location, commute, hybrid and availability |
| Seniority | 10 | Real responsibility level, not inflated titles |
| Risk allowance | 10 | Start at 10, deduct for mandatory gaps and material risks |

Scores are fit assessments, not interview probabilities. Record fit separately from eligibility gates: mandatory qualifications, work rights, employment type, location and actual base-pay evidence. A high total cannot override a failed gate. Follow the private policy for undisclosed or conditional pay; do not infer it from the salary filter. Exclude ineligible roles from the reserved-role comparison and report conditional roles distinctly. Use configured thresholds (normally 85+ very high, 70-84 medium-high). Explain strategically notable lower scores without fabricating a suitable match.

Finish comparing the eligible shortlist before selecting **exactly one highest-scoring role per run** for manual application when any eligible role exists. Ties: strongest verified evidence, then newest listing. Persist its reserved flag so a resumed run does not pick another. If coverage is incomplete, reservation is provisional and automatic submissions must wait until it is resolved.

## Delegate Documents

After selection, invoke/read `$tailor-job-documents` for every eligible job at or above the configured threshold (70 is included by default), including the reserved job. Pass:

- `jobs_root`, run directory, canonical job URL/ID, employer, title, full advertisement and requirements.
- Evidence-based score, gaps, source references, requested supporting documents and intended route.
- `output_mode: seek_pdf` or `manual_docx`; use manual mode for reserved/external/answer-blocked roles.

Use only the returned, visually approved files and their manifest. If it reports unsupported claims, missing sources or failed rendering, do not upload. A move to manual status must have editable DOCX documents. Create cover letters/introductions only if the ad or actual form explicitly requests them; SEEK's generic optional upload area alone is not a request.

For any future upload, require the companion skill's current `document_checks` report with `checks_passed` and `eligible_for_ready: true`. Rerun its offline checker against the current manifest immediately before uploading; a saved ready label or an old report is insufficient. Confirm the uploaded filenames/versions match its artifact hashes. Missing reports, incomplete evidence/visual review, changed source inputs, blocked checks or unresolved warnings return the pack to document review. This applies to pending older packs too, but never rewrites or repeats completed submissions. These extra checks do not replace the approval, reservation or screening rules below.

## Apply Safely

- External employer portals and the reserved job are manual only. Other 85+ jobs are eligible on the same rules as 70-84 jobs.
- Read current browser/tool instructions. Use the supported browser UI/connector; no hidden APIs or authentication workarounds. Consult [SEEK UI Notes](references/seek-ui-notes.md) when preparing forms.
- Specific approval must identify the employer/job and disclosure of CV/contact/profile information. A vague historical 'yes' or saved profile answer is not transferable approval. Preserve and verify traceable approval for that same pending job on resume; do not re-request it merely because the turn or date changed. Changed recipient, disclosure scope or a new declaration needs its required consent. Request only genuinely missing answers/consents, batching related questions while respecting current action-time confirmation rules.
- Use private confirmed answers only where question scope matches. Equivalent duties are not a formal job title; record their basis. Never infer duration from total tenure, infer no conviction from silence, or guess licence/visa/health/referral information. Prefilled SEEK answers need verification against the private answer store.
- Follow private salary policy. Do not select an unapproved out-of-range figure, silently lower an expectation, or mistake a band for an exact amount. Ask if the required option is unsupported. Keep a job-specific salary exception scoped to that job; it does not change the default expectation or authorise the same figure for another employer.
- Keep CV/SEEK profile dates and titles consistent with confirmed facts. If SEEK disallows a future date, ask for a truthful temporary explanation; do not invent an earlier date or modify the profile without approval. Skip duplicate CV-parser suggestions.
- For intended SEEK submissions, attach the correct tailored PDF, and only specifically requested supporting documents. Record the existing default CV before upload. If SEEK automatically changes it, restore the previous default, then reselect and verify the job's tailored attachment without making it default. Stop if restoring it needs unavailable authority. Do not change profile visibility incidentally.
- At the saved-CV limit, consult the private deletion preferences and current tool confirmation rules. If permanent deletion needs action-time consent, obtain it for named oldest eligible non-default copies. Preserve the default, current/newer CVs and all local originals; never delete again on resume without checking what remains saved.
- Before Submit, verify recipient, files, answers, profile, reservation flag and approval. Persist `submitting` in permanent history **before clicking**. Click once. Confirm a visible success page/message before `submitted`; if ambiguous, write `submission_uncertain` and stop retries. Opening an external Apply link or a SEEK visited-site entry is not a submission.
- Do not solve CAPTCHAs without current confirmation. New contracts/declarations need their own required consent. Never store passwords, one-time codes or session tokens in these files.

## Save and Report

Update private answers only after explicit new answers or verified source facts; store provenance, date, question scope and any superseded answer. Preserve unknowns. Keep employer-specific approvals and answers scoped to their exact jobs.

Save `Job Records.json` with URL/ID, title, employer, salary evidence, location, posting/closing dates, component scores, total, reasons, gaps, route, reservation flag, questions, document filenames, QA result and submission status/evidence. Persist records incrementally, including exclusions and unfinished work. Never overwrite original CVs.

Maintain two dated lists: `Jobs for You to Apply.md` (reserved, external and blocked/approval-pending jobs, linking DOCX) and `Jobs Submitted via SEEK.md` (confirmed submissions only, linking submitted PDFs and confirmation). Reconcile both from current structured job/history records after material changes: remove resolved questions, superseded blockers and confirmed submissions from the actionable manual list. Retain a submission's original run association and actual submission date. A manual-list entry is not proof that its document pack is ready: label failed/unverified renders as draft or QA-blocked, link only existing files and state what is missing. If none submitted, say why. Preserve permanent application history even when the scan log is pruned. Keep approvals, screening and private facts out of shared skill bundles.

Report unique cards scanned, full ads scored, counts by score band, CVs completed, submissions, reserved role and links to both lists. State incomplete coverage and outstanding answers plainly. Follow the user's notification settings for scheduled runs.

## Scan Log Helper

Python standard library only; no network or submission actions. `--root` is mandatory. Input is a JSON array of the three fields above, obtained from actual browser observations.

```sh
python3 scripts/scan_log.py prune --root "$JOBS_ROOT" --today YYYY-MM-DD
python3 scripts/scan_log.py merge --root "$JOBS_ROOT" --today YYYY-MM-DD --input /path/to/observed-jobs.json
python3 scripts/scan_log.py contains --root "$JOBS_ROOT" --today YYYY-MM-DD --url 'https://nz.seek.com/job/12345678'
```

Pass today's date in the configured timezone. `contains` emits JSON and does not grant permission to apply. The helper validates fields, locks updates and atomically replaces the file; corrupt input aborts without erasing history.
