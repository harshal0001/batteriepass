---
description: Review a component or the whole system for robustness, scalability and optimisation
---

Scale and robustness review of: $ARGUMENTS (if empty, the whole system)

1. Read `CLAUDE.md` §0 for the stated target scale and §3 for the principles.
2. Walk the code and check each principle. Produce a table:

   | Principle | Status (✅ / ⚠️ / ❌) | Evidence (file:line) | Fix |
   |---|---|---|---|

   Cover: boundary validation, typed errors, timeouts, retries only on idempotent ops, idempotent writes, structured logging + request id, health checks, config via env, graceful shutdown, stateless handlers, pagination, indexes per query, background work for slow ops, cache invalidation strategy, N+1 queries.
3. Answer explicitly: **what breaks first at 10×, and at 100×** the stated scale, and what the change would be. Draw a `flowchart` of the bottleneck path.
4. Rank the top 3 fixes by impact ÷ effort. For each, say whether it is worth doing *now* given the stated scale or should become a `deferred`-tagged ADR.
5. Do not change code. Present findings and wait for my decision.
