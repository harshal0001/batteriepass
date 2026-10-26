# Design docs

One file per feature or significant change, written **before** implementation and
approved by the owner. Template: `_template.md`. Create one with:

```bash
uv run python scripts/new_design.py "passport creation"
```

Every design doc has at least one Mermaid diagram, a test plan written before the code,
and a scale review ("what breaks at 10× / 100×?"). Decisions between alternatives that
come out of a design doc become ADRs in `docs/adr/`.

| Feature | Status | Doc |
|---|---|---|
| _none yet — candidates: passport creation flow, DynamoDB single-table layout, health service, document extraction, regulation Q&A_ | | |
