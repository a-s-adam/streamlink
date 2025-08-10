# Personal Entertainment Knowledge Graph

This repository contains the code for the **Personal Entertainment Knowledge Graph (PEKG)** MVP.  
The goal of this project is to provide users with a unified view of their streaming habits by ingesting data from **Netflix** and **YouTube**, enriching it with metadata from TMDB and other sources, and building a knowledge graph and vector store for personalized recommendations.

## Features

The MVP supports the following high‑level features:

1. **Google sign‑in** using NextAuth on the frontend.  
2. **CSV upload** of Netflix viewing history.  
3. **YouTube ingestion** using OAuth and the YouTube Data API v3.  
4. **Metadata enrichment** via the TMDB API.  
5. **Knowledge graph** built in Neo4j Community Edition.  
6. **Vector store** built in PostgreSQL using the [`pgvector`](https://github.com/pgvector/pgvector) extension.  
7. **Hybrid recommendations** that combine graph algorithms and embedding similarity.  
8. **Optional local LLM** (via Ollama) to generate natural language explanations for recommendations.

## Repository structure

```
streamlink/
│  .gitignore             # Ignore rules for Python/Node/other toolchain artifacts
│  .env.example           # Template for all environment variables
│  docker-compose.yml     # Compose file to run local services
│  README.md              # Project overview and setup instructions
│
├‑backend/
│  ├‑app/
│  │  ├‑__init__.py
│  │  ├‑main.py         # FastAPI application entrypoint
│  │  ├‑config.py       # Pydantic settings model
│  │  ├‑api/
│  │  │  ├‑__init__.py
│  │  │  └‑routes.py    # Placeholder API routes (CSV upload, health)
│  │  ├‑models/
│  │  │  ├‑__init__.py
│  │  │  └‑user.py      # SQLAlchemy model definitions
│  │  ├‑services/
│  │  │  ├‑__init__.py
│  │  │  ├‑ingestion.py # Stubs for Netflix/YouTube ingestion
│  │  │  └‑tmdb.py      # Stub for TMDB metadata resolver
│  │  └‑db/
│  │     ├‑__init__.py
│  │     └‑database.py  # SQLAlchemy engine and session
│  └‑Dockerfile         # Build backend container image
│
└‑frontend/              # Placeholder for Next.js frontend
   └‑README.md          # Brief explanation of the frontend scaffold
```

## Getting started

1. **Clone the repository** (if you haven't already):

   ```sh
   git clone https://github.com/a-s-adam/streamlink.git
   cd streamlink
   ```

2. **Configure environment variables** by copying `.env.example` to `.env` and filling in the necessary secrets (API keys, database credentials, OAuth client secrets, etc.).

3. **Launch the infrastructure** via Docker Compose:

   ```sh
   docker compose up -d
   ```

   This will start PostgreSQL (with pgvector), Neo4j, Redis, and, if enabled, Ollama.  
   You can run the backend locally on your host machine or build it as a Docker container using the provided `backend/Dockerfile`.

4. **Run the backend** (locally):

   ```sh
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Run the frontend** (once scaffolded):

   ```sh
   cd frontend
   npm install
   npm run dev
   ```

## Next steps

This initial commit lays down the groundwork for the PEKG MVP.  
In subsequent iterations we will:

1. Build out the authentication flow with NextAuth and Google OAuth.
2. Implement ingestion pipelines for Netflix CSVs and YouTube history.
3. Add TMDB metadata lookup and normalize titles.
4. Design the Neo4j graph schema and populate it along with the pgvector store.
5. Develop recommendation algorithms (graph and embedding based) and expose them via the API.
6. Flesh out the Next.js UI for uploading files, connecting accounts, viewing the graph, and receiving recommendations.

Contributions and feedback are welcome!  
Feel free to open issues or pull requests as we iterate on the MVP.
