---
description: Explain a part of this codebase to me as if onboarding a new engineer, with diagrams
---

Explain: $ARGUMENTS

Rules for the explanation:
1. Answer **from the actual code in this repo**, citing file paths and line ranges. Do not describe how it "would usually" work.
2. Structure:
   - **One-paragraph summary** of what it does and why it exists.
   - **Where it sits**: a small Mermaid `flowchart` showing this piece and its immediate neighbours in the architecture.
   - **How it works**: a `sequenceDiagram` (for a flow) or `stateDiagram-v2` (for lifecycle) of the main path.
   - **Key design choices** and the ADR / design doc that made them (link them). If no ADR exists for an obvious decision, say so.
   - **What could go wrong**: failure modes, and how the code handles (or fails to handle) them.
   - **What would break at 10× / 100× load**.
   - **Concepts to know**: each new term in one line, with a glossary link; add missing ones to `docs/glossary.md`.
3. End with 3 questions I could answer to check I understood it.
4. Keep it under ~600 words plus diagrams. Offer to go deeper on any section.
