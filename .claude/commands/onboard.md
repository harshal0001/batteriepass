---
description: Walk me through the whole codebase as if I were a new engineer joining today
---

Give me an onboarding tour of this repository.

1. Start from `docs/ARCHITECTURE.md`. If it is out of date versus the code, fix it first and tell me what was stale.
2. Produce the tour in this order:
   - **What the system does** (3 sentences) and the stated scale.
   - **System diagram** (Mermaid `flowchart`) with each box linked to its directory.
   - **The one request to understand**: pick the most representative user flow and draw its `sequenceDiagram` end to end, citing files.
   - **Layer by layer**: for domain → application → infrastructure → interfaces, list the 2–3 most important files and one sentence each on why they exist.
   - **Data model**: `erDiagram` of the core entities.
   - **Decisions that shaped it**: the 3–5 most impactful ADRs, one line each.
   - **Where it is weakest**: the top 3 robustness/scalability concerns with file references.
   - **Vocabulary**: terms from `docs/glossary.md` I must know, one line each.
3. End with 5 comprehension questions and offer to answer any of them.
