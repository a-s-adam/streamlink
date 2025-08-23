-- Enable pgvector extension for storing embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the streamlink database if it doesn't exist
-- (This will be handled by the POSTGRES_DB environment variable, but keeping for reference)
-- CREATE DATABASE IF NOT EXISTS streamlink;
