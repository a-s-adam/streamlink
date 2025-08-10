"""Ingestion services for Netflix and YouTube.

This module contains stub functions for parsing and ingesting viewing history
from Netflix CSV exports and the YouTube Data API.  Actual implementations
should be added in later iterations.
"""
from __future__ import annotations

import csv
from io import StringIO
from typing import Iterable, List, Tuple

from sqlalchemy.orm import Session

from ..models.user import User


def parse_netflix_csv(file_contents: str) -> List[Tuple[str, str]]:
    """Parse a Netflix viewing activity CSV and return a list of (title, date) tuples.

    The Netflix CSV format typically contains columns like ``Title`` and ``Date``.
    This stub simply reads the CSV and extracts those columns.  In a real
    implementation you should handle different locales and unexpected headers.
    """
    reader = csv.DictReader(StringIO(file_contents))
    records: List[Tuple[str, str]] = []
    for row in reader:
        title = row.get("Title") or row.get("title")
        date = row.get("Date") or row.get("date")
        if title and date:
            records.append((title.strip(), date.strip()))
    return records


def ingest_netflix_history(
    db: Session, *, user: User, records: Iterable[Tuple[str, str]]
) -> None:
    """Ingest parsed Netflix records into the database and knowledge graph.

    This function is a placeholder.  It should:
      * Normalize titles and look up TMDB IDs
      * Insert raw viewing events
      * Upsert canonical ``Title`` nodes and relationships in Neo4j
      * Compute and store embeddings in pgvector
    """
    # TODO: Implement ingestion logic
    for title, date in records:
        # Placeholder: print each record. Replace with real ingestion steps.
        print(f"Would ingest {title} watched on {date} for user {user.email}")


def ingest_youtube_history(db: Session, *, user: User, oauth_token: str) -> None:
    """Ingest liked videos and playlists from YouTube for a given user.

    A real implementation should use the YouTube Data API v3 to fetch the
    authenticated user's liked videos and playlists, map them to TMDB entries
    where possible, and then insert them into the knowledge graph and vector
    store.
    """
    # TODO: Call YouTube Data API and ingest results
    print(f"Would ingest YouTube history for user {user.email}")
