# PEKG MVP Architecture

This document describes the high‑level architecture of the Personal Entertainment Knowledge Graph (PEKG) MVP.  The design focuses on free or self‑hosted services and supports ingestion from Netflix CSV exports and the YouTube Data API.

```mermaid
flowchart TB
  subgraph Client [Frontend (Later)]
    U[User]
    UI[Web UI]
    U --> UI
  end

  subgraph API [Backend API (Later)]
    REST[REST / GraphQL]
    Worker[Background Worker]
  end

  subgraph STG [Staging Storage]
    UP[Uploads folder / local disk]
  end

  subgraph DBSQL [Postgres + pgvector]
    TBL_RAW[(raw_ingest_* tables)]
    TBL_META[(content + embeddings)]
    AUTH[(users / sessions / settings)]
  end

  subgraph GRAPH [Neo4j Community]
    GUser[(User nodes)]
    GItem[(Show/Movie/Video nodes)]
    GEdges{{WATCHED / LIKES / SIMILAR edges}}
  end

  subgraph CACHE [Redis]
    Q[Task queue]
    C[Cache]
    RLocks[Rate‑limit / locks]
  end

  subgraph LLM [Optional: Ollama]
    EMB[Embeddings API (nomic‑embed‑text)]
    CHAT[Chat LLM (llama3 / qwen)]
  end

  %% Flows
  UI -- upload Netflix CSV / YouTube Takeout --> REST
  REST -->|store file| UP
  REST -->|enqueue parse job| Q
  Worker -->|read file| UP
  Worker -->|parse rows| TBL_RAW
  Worker -->|upsert items| TBL_META
  Worker -->|create graph nodes/edges| GItem
  Worker -->|create user relations| GUser
  Worker -->|compute embeddings (optional)| EMB
  EMB -->|vectors| TBL_META
  REST -->|read models| TBL_META
  REST -->|graph queries| GRAPH
  REST -->|cache hot queries| C
  REST --> UI
```

## Component interactions

### Frontend

- Uploads Netflix CSV and initiates YouTube OAuth flows via the API.  
- Polls for ingestion status from the backend via Redis.  
- Displays recommendations and the user’s knowledge graph.

### Backend API

- Exposes endpoints to upload files, handle OAuth callbacks, read ingestion status, and return recommendations.  
- Stores uploaded files in a staging directory and enqueues background tasks in Redis.  
- Reads/writes data to PostgreSQL and Neo4j and optionally computes embeddings via a local LLM.  
- Uses Redis to cache frequently accessed responses and to implement rate limiting.

### Background worker

- Consumes ingestion tasks from Redis.  
- Parses Netflix CSVs and YouTube history, enriches titles via TMDB, and writes to the database and graph.  
- Optionally computes embeddings and similarity edges.  
- Creates and updates relations in Neo4j based on viewing history.

### Databases

| Component   | Role                                                       |
|-------------|------------------------------------------------------------|
| **Postgres**| Stores user accounts, raw ingestion tables, normalized content, and embedding vectors via pgvector. |
| **Neo4j**   | Maintains the graph of users, titles, genres, persons, and relations like WATCHED, LIKES, SIMILAR. |
| **Redis**   | Provides a task queue for background workers, a cache for API responses, and simple locks. |

### Optional LLM

Ollama can provide local embedding computation (e.g. with ``nomic‑embed‑text``) and natural language explanations via a small chat model.  These services are optional and can be toggled via environment variables.
