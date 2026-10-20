# Private Data Contract

All populated data belongs under a user-selected Jobs root, never in a skill bundle. JSON uses UTF-8, `schema_version: 1`, and an ISO `updated_on` date. Paths inside private files are relative to the Jobs root unless explicitly supplied otherwise. Never follow an unexpected path or upload an entire data file to an employer.

Required files:

| File | Content |
| --- | --- |
| `private/workflow.json` | `timezone`, search `location`, `posted_within_days: 3`, salary currency/minimum, `role_families`, scoring thresholds/weights, document/approval preferences, scan retention |
| `private/candidate-profile.json` | `identity`, dated `employment`, `education`, `certifications`, `languages`, corrections and explicit unknowns; every substantive entry has provenance |
| `private/source-index.json` | `sources` with IDs, relative paths, purpose and cautions; identify baseline and benchmark documents |
| `private/evidence-bank.md` | Verified duties, achievements, projects, boundaries and source/page references |
| `private/screening-answers.json` | `confirmed`, `unknown`, `answer_history`; confirmed entries contain `id`, `answer`, `scope`, `source`, `recorded_on` |
| `private/application-history.json` | Permanent `jobs` array: job ID, canonical URL, title/employer, state, relevant dates, approval/source and visible confirmation evidence |
| `private/pending-applications.json` | Incomplete jobs, exact unanswered questions, known document paths, scoped approval, reserved role and recovery notes |

Missing private files are not permission to reuse another candidate. Ask for the missing profile/source folder or create empty schemas and gather facts; do not invent identity, screening answers or experience. Empty/unconfirmed values remain `null` or explicitly unknown, not `false` or zero.

Application states include `prepared`, `awaiting_answers`, `awaiting_approval`, `reserved_manual`, `manual_external`, `submitting`, `submission_uncertain`, `submitted`, `submitted_user_reported`, `withdrawn` and `declined`. Never downgrade a confirmed submission on a rerun. Record `submitting` before clicking Submit; only an observed confirmation permits `submitted`. `submission_uncertain` and `submitting` require reconciliation, not retries. Store the employer/job and data scope for approvals; do not treat an approval record as standing consent for other recipients.

Keep document readiness, disclosure approval, salary approval, screening completeness and submission status independently identifiable within the existing records. Approval references need traceable user-message provenance, exact recipient/job, disclosed document/data scope and any conditions. Job-specific salary options and equivalent-duty durations stay scoped; do not overwrite standing preferences with an exception. Preserve the actual question/options when necessary to distinguish specialist, industry or formal-title experience. An ambiguous multi-question reply does not establish every answer.

Pending records retain their original run, reserved flag, current stage, manifest path and recovery notes across dates. Store active run ownership separately from an application state; a pending record is not itself a live lock. Update records incrementally, preserving other jobs and terminal states. The dated lists are derived views, not a second source of approval or submission truth; see [Run State and Handoff](run-state.md).

When starting for a new candidate, populate these files only from their supplied facts and source documents. Apply restrictive local permissions where available, explain that this is not encryption, and keep files out of any shared/versioned bundle. Never store credentials, OTPs, authentication cookies or identity-document numbers.

The root `Scanned Jobs.json` is a JSON array of exactly `url`, `title`, `date_scanned`. It is independent of the application-history schema and must never be used as proof of submission.
