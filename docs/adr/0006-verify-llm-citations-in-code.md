# 0006 — Trust LLM output only through citations verified in code

**Status:** Accepted · **Date:** 2026-10-24

## Context

Two features use a language model. Document extraction fills a passport's static fields
— manufacturer, chemistry, rated capacity, engine model, thrust rating — from datasheets
and Type Certificate Data Sheets. Regulation Q&A answers questions about the Battery
Regulation and EASA's continuing-airworthiness rules.

A language model produces plausible values whether or not the source supports them. On a
passport, a wrong value that looks sourced is worse than a missing one: the conformance
check would count it as present.

## Decision

**Extraction returns evidence, not just values.** For each field the model returns the
value, the page, and a verbatim quote. Code then checks that the quote appears on that
page and that the value agrees with it, with numbers and units parsed and compared. A
field that fails is dropped, never guessed or repaired. Every surviving field is stored
as a `FieldProvenance` with the source document's SHA-256.

**Regulation answers are extractive by default:** the retrieved paragraphs themselves,
each with its citation, such as `Art. 77(2)` or `M.A.305(d)`. A generated answer is
opt-in, may cite only paragraphs retrieved for that question, and refuses when the answer
is not in them. Both rules are enforced in code, not in the prompt.

**The model behind extraction is configuration.** A fine-tuned open model and the Claude
API sit behind one `Extractor` interface; whichever runs, its output passes the same
verification.

**Demo passports need no live model call.** Their extraction runs offline at seed time
and is stored with provenance.

The rejected alternative was asking the model for a confidence score per field. Models are
poorly calibrated about their own errors, and a score cannot be checked against the
document; a quote can.

## Consequences

Verification costs recall: a correct value with a misquoted source is dropped. That loss is
measured — the share of fields rejected is reported beside precision and recall — and a
regex baseline on the same pages shows whether the model earns its place.

Datasheets are copyrighted. The service stores extracted fields and their short quotes,
never the PDFs or their full text.
