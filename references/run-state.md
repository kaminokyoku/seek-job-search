# Run State and Handoff

Read when starting or resuming a run, reconciling outcomes, or updating the pending queue. Private structured records are the ledger; browser tabs and generated Markdown lists are not.

## One Active Owner

Use the workspace's existing exclusive run guard for application mutations. If none exists, atomically create `private/.seek-run.lock` as a lock directory and record an owner/run identifier, original run date, acquisition time and checkpoint reference inside it. If creation reports an existing directory, inspect ownership rather than overwriting it. A saved `active` boolean, old timestamp or a one-off command's exited PID alone does not prove the workflow is inactive. Check owner/checkpoint evidence before taking over; do not clear a live guard or run a competing flow. If ownership cannot be established, stop application mutations and report the conflict. Remove only the guard owned by this run when releasing it.

Checkpoint the canonical job ID, original run, reservation, document manifest, current stage, scoped approval references and unresolved questions before handoff. Release active ownership when waiting for a person, while retaining the checkpoint; do not hold an application lock indefinitely for an unanswered question. Interrupted `submitting` or uncertain outcomes still require reconciliation, not a fresh attempt.

## Resume Without Resetting

- Read the latest record before each external mutation and merge only the intended fields. Do not rebuild a whole batch from an old template that resets submitted states, reservations or approvals.
- Preserve exact employer/job-specific approvals with their user-message provenance, data scope and conditions. Resume them only within that scope and current tool rules; saved preferences alone are not final authorisation.
- Keep document readiness, disclosure approval, salary approval, screening completeness and submission status separate. A ready PDF is not approval, and an approved application may still have a blocked document or unanswered question.
- A blocker on one job need not stop an independently approved, non-reserved job once shortlist selection is complete. Do not transfer the blocked job's salary choice, consent or answers to it.
- Reuse the existing attachment when visibly verified as the intended version. A closed tab or timed-out chooser is not a reason to reupload, delete another CV or retry Submit blindly.
- Verify the vacancy and recipient are still the same before final submission. If the advertisement or required documents materially changed, reassess the evidence, pack and approval scope rather than relying on an old ready flag.
- A changed private input returns affected pending packs to the companion skill's source-change review. Never refresh hashes automatically or alter already-submitted files to match new facts.

## Screening Scope

Store the actual question and options where wording changes meaning. Match each answer by job/domain, duration, units and qualification, not just a similar label. Equivalent duties need a confirmed duration and basis; they do not rename a formal role or establish industry-specific experience. A reply answering several questions ambiguously leaves the unresolved parts unknown. Do not convert an answer to one question into a blanket negative or a new career claim.

## Reconcile After Material Changes

After an answer, approval, document revision or observed outcome, update the original job record, permanent history and pending queue consistently, then reconcile both dated lists. Preserve unrelated fields and history. Confirmed submissions leave the actionable pending/manual list; reserved/manual/external jobs remain with editable documents and current blockers. Do not select a replacement reserved role just because another job was submitted or resumed on a later date.

Before reporting, verify counts against records and distinguish observed confirmations from prepared, uncertain and user-reported submissions. Link only existing documents, showing QA-blocked packs honestly. Persist the submission state before refreshing summaries so a failed summary update cannot cause a duplicate application.
