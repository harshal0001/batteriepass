# Mermaid cheat sheet

All diagrams in this repo are Mermaid inside fenced code blocks. They render on
GitHub, GitLab, VS Code (Markdown Preview Mermaid extension), Obsidian, and
https://mermaid.live. Pick by the question you're answering.

## Sequence diagram — "who calls whom, in what order?"

Use for request flows, auth handshakes, retries, anything with time.

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant API
    participant S as Service
    participant DB
    participant Ext as External API

    U->>API: POST /orders
    API->>S: createOrder(cmd)
    S->>DB: INSERT order (status=pending)
    S->>Ext: charge(card)
    alt success
        Ext-->>S: 200
        S->>DB: UPDATE status=paid
        S-->>API: OrderCreated
        API-->>U: 201
    else timeout
        Ext--xS: timeout
        S->>DB: UPDATE status=payment_failed
        API-->>U: 502
    end
```

Tips: `->>` solid call, `-->>` dashed reply, `--x` failed, `alt/else`, `loop`,
`par` for concurrency, `Note over A,B: text`.

## Flowchart — "what are the branches?" / "what are the boxes?"

```mermaid
flowchart TD
    A[Receive webhook] --> B{Signature valid?}
    B -- no --> R[400 reject]
    B -- yes --> C{Seen event id before?}
    C -- yes --> D[200, ignore duplicate]
    C -- no --> E[Store event]
    E --> F[Enqueue processing]
    F --> G[200 ack]
```

Shapes: `[rect]` `(rounded)` `([stadium])` `[(database)]` `{diamond}`
`{{hexagon}}` `[[subroutine]]`. Direction: `TD` top-down, `LR` left-right.
Group with `subgraph Name ... end`.

## Architecture / C4-style container diagram

```mermaid
flowchart LR
    subgraph Client
        Web[Web app]
        Mobile[Mobile app]
    end
    subgraph Backend
        GW[API gateway]
        Svc[Core service]
        Wk[Worker]
    end
    subgraph Data
        PG[(Postgres)]
        RD[(Redis)]
        MQ[[Queue]]
    end
    Web --> GW
    Mobile --> GW
    GW --> Svc
    Svc --> PG
    Svc --> RD
    Svc --> MQ
    MQ --> Wk
    Wk --> PG
    Wk --> Ext[Email provider]
```

Mermaid also has a native `C4Context` / `C4Container` syntax; flowcharts are
more widely rendered, so prefer them.

## ER diagram — "what are the entities and relations?"

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_LINE : contains
    PRODUCT ||--o{ ORDER_LINE : "appears in"
    USER {
        uuid id PK
        text email UK
    }
    ORDER {
        uuid id PK
        uuid user_id FK
        text status
    }
```

Cardinality: `||` exactly one, `o|` zero or one, `}|` one or more, `}o` zero
or more.

## State diagram — "what states can this be in?"

```mermaid
stateDiagram-v2
    [*] --> Pending
    Pending --> Paid : payment ok
    Pending --> Failed : payment error
    Failed --> Pending : retry
    Paid --> Shipped : dispatch
    Shipped --> Delivered
    Paid --> Refunded : refund
    Delivered --> [*]
    Refunded --> [*]
```

## Class diagram — "what types exist and how do they relate?"

```mermaid
classDiagram
    class OrderService {
        +create(cmd) Order
        +pay(id) void
    }
    class OrderRepository {
        <<interface>>
        +save(order)
        +byId(id) Order
    }
    class PostgresOrderRepository
    OrderService --> OrderRepository : depends on
    PostgresOrderRepository ..|> OrderRepository : implements
```

## Gantt / timeline (rarely) — rollout plans

```mermaid
gantt
    title Rollout
    dateFormat YYYY-MM-DD
    section Deploy
    Migration      :a1, 2026-11-01, 1d
    API            :a2, after a1, 1d
    Worker         :a3, after a2, 1d
```

## Rules of thumb

- One diagram answers one question. Split rather than cram.
- ≤ 10 nodes per diagram; more than that, zoom out or split.
- Name participants by role (`Worker`), not implementation (`node-cron-v3`).
- Put the diagram next to the prose that explains it, not in an appendix.
- Update the diagram in the same commit as the code change it describes.
