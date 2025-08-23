.PHONY: help up down build logs clean migrate seed test fmt lint web:test api:test

help: ## Show this help message
	@echo "Streamlink MVP - Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Start all services with docker compose
	docker compose up -d

down: ## Stop and remove all services
	docker compose down

build: ## Build all service images
	docker compose build

logs: ## Show logs from all services
	docker compose logs -f

clean: ## Remove all containers, volumes, and images
	docker compose down -v --rmi all

migrate: ## Run database migrations
	docker compose exec api alembic upgrade head

seed: ## Seed the database with sample data
	docker compose exec api python -m app.scripts.seed

test: ## Run all tests
	@echo "Running web tests..."
	@make web:test
	@echo "Running API tests..."
	@make api:test

web:test: ## Run frontend tests
	cd frontend && npm test

api:test: ## Run backend tests
	cd backend && python -m pytest

fmt: ## Format all code
	@echo "Formatting frontend..."
	cd frontend && npm run format
	@echo "Formatting backend..."
	cd backend && ruff format .

lint: ## Lint all code
	@echo "Linting frontend..."
	cd frontend && npm run lint
	@echo "Linting backend..."
	cd backend && ruff check .

install: ## Install dependencies for all services
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt

dev: ## Start development environment
	@echo "Starting development environment..."
	@make up
	@echo "Development environment started!"
	@echo "Frontend: http://localhost:3000"
	@echo "API: http://localhost:8000"
	@echo "PostgreSQL: localhost:5432"
	@echo "Redis: localhost:6379"
	@echo "Neo4j: http://localhost:7474"
