---
description: Close the session - write the learning-log entry and check docs are current
---

Close out this working session.

1. Review what changed in this session (`git diff` / `git log` since the session started, or the conversation if no git).
2. Verify the docs contract from `CLAUDE.md` was honoured:
   - Every multi-module feature has a design doc in `docs/design/`
   - Every choice between alternatives has an ADR
   - `docs/ARCHITECTURE.md` reflects any new component or dependency
   - New terms are in `docs/glossary.md`
   If anything is missing, create it now before continuing.
3. Prepend a new entry to `docs/LEARNINGS.md` using the template at the top of that file. Be specific in **Patterns / concepts used** and honest in **Open questions** (list anything you decided that I never reviewed).
4. Run the scale review question for the biggest thing built today: "What breaks at 10× / 100×?" and put the answer in the entry.
5. Reply with the new entry and a 3-line summary of docs touched.
