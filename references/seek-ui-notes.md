# SEEK UI Notes

These are observed failure modes, not fixed selectors or permission to bypass safeguards. Inspect current UI each time.

- Apply links can change SEEK's visited/application activity even before submission. Establish the required job-specific approval before opening where this side effect matters.
- The application flow commonly contains documents, employer questions, profile and review. Progress-bar items may not navigate; use the actual Back/Continue controls and verify the next state.
- Selected attachment and saved default are different states. Record both before changing documents. A new upload can become default automatically: restore the recorded default, then reselect the job's tailored PDF without making it default, and verify both states. A different tab may have a stale CV list. Refresh only intentionally: it may lose screening answers or select an old CV again.
- A saved-resume limit dialog may appear instead of a file picker. Resolve the exact authorised deletion first, then upload via the supported file-chooser tool. Never assume a timed-out picker uploaded a file.
- Some source-based profile updates/rendering are asynchronous. Wait for the relevant visible state or use another pending task, rather than blindly repeating a mutation.
- After upload, observe the correct filename and usable navigation before continuing; a chooser closing is not proof the upload completed. On navigation failure, recover from the observed page and saved checkpoint using the supported browser, not invented routes, hidden APIs or another submission click.
- CV parsing may suggest duplicate roles/qualifications with slightly different names. Excluding a proposed duplicate is different from deleting an existing profile entry.
- Review includes the SEEK profile, not only attached files. Check titles/dates against private facts; never silently broaden profile visibility or begin identity verification.
- An Apply button or a SEEK-branded entry page does not establish an entirely SEEK-hosted route. Inspect the actual flow and stop at an external portal; record it as manual without submitting there.
- A success URL and explicit 'application sent' message establish submission. Read the narrow confirmation text/recipient and a sanitised URL, not the entire success-page body or accessibility tree: optional identity-verification links can contain authentication tokens. Do not store or echo those links. Do not click again, request 'strong interest', or start optional identity verification as part of applying.
- Preserve pending tabs for handoff when supported. Save enough local state to recover if tabs close; browser persistence is not the application ledger.
