# Streamlink MVP

A modern, responsive web application that ingests Netflix CSV and YouTube history (OAuth), enriches with TMDB, stores items + events, computes embeddings, and serves basic recommendations with auth + settings.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### 1. Clone and Setup
```bash
git clone https://github.com/a-s-adam/streamlink.git
cd streamlink
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and fill in your values
# For testing, you can leave most values as defaults
```

### 3. Start the Application
```bash
# Start all services
make up

# Or manually:
docker compose up -d
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **Neo4j**: http://localhost:7474 (optional)

### 5. Seed the Database (Optional)
```bash
# Seed with sample data
make seed

# Or manually:
docker compose exec api python -m app.scripts.seed
```

## 🏗️ Architecture

### Backend (FastAPI)
- **FastAPI** with Python 3.11+
- **SQLAlchemy 2.x** with **Alembic** migrations
- **PostgreSQL** + **pgvector** for embeddings
- **Celery** + **Redis** for background tasks
- **Neo4j** for graph relationships (optional)

### Frontend (Next.js 14)
- **Next.js 14** with App Router
- **TypeScript** + **TailwindCSS**
- **shadcn/ui** components
- **NextAuth** for authentication

### Key Features
- Netflix CSV ingestion with TMDB enrichment
- YouTube OAuth integration
- AI-powered recommendations using embeddings
- Background job processing
- Mock mode for testing without API keys

## 🔧 Configuration

### Environment Variables

#### Common
```bash
NODE_ENV=development
APP_ENV=development
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/streamlink
REDIS_URL=redis://redis:6379/0
```

#### Authentication
```bash
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

#### APIs
```bash
TMDB_API_KEY=your-tmdb-api-key
YOUTUBE_API_KEY=your-youtube-api-key
YOUTUBE_OAUTH_CLIENT_ID=your-youtube-oauth-client-id
YOUTUBE_OAUTH_CLIENT_SECRET=your-youtube-oauth-client-secret
```

#### Embeddings
```bash
EMBEDDINGS_PROVIDER=openai  # or ollama
OPENAI_API_KEY=your-openai-api-key
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

#### Mock Mode
```bash
MOCK_MODE=true  # Enable for testing without real API keys
```

## 📁 Project Structure

```
streamlink/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routers
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   ├── tasks/          # Celery tasks
│   │   └── scripts/        # Database scripts
│   ├── alembic/            # Database migrations
│   └── requirements.txt
├── frontend/                # Next.js frontend
│   ├── src/
│   │   ├── app/            # Next.js app router
│   │   ├── components/     # React components
│   │   └── lib/            # Utilities
│   └── package.json
├── infra/                   # Infrastructure
│   └── init/               # Database initialization
├── samples/                 # Sample data files
├── docker-compose.yml       # Service orchestration
├── Makefile                 # Development commands
└── .env.example            # Environment template
```

## 🛠️ Development

### Available Commands
```bash
make help          # Show all available commands
make up            # Start all services
make down          # Stop all services
make build         # Build all service images
make logs          # Show service logs
make migrate       # Run database migrations
make seed          # Seed database with sample data
make test          # Run all tests
make fmt           # Format code
make lint          # Lint code
```

### Backend Development
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest

# Format code
ruff format .
ruff check .
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Lint and format
npm run lint
npm run format
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
# Start services
make up

# Run tests
make test

# Check service health
curl http://localhost:8000/health
curl http://localhost:3000
```

## 🚀 Deployment

### Production Considerations
1. Set `NODE_ENV=production` and `APP_ENV=production`
2. Use strong secrets for `NEXTAUTH_SECRET` and `ENCRYPTION_KEY`
3. Configure proper CORS origins
4. Set up SSL/TLS certificates
5. Configure database backups
6. Set up monitoring and logging

### Docker Production
```bash
# Build production images
docker compose -f docker-compose.prod.yml build

# Start production services
docker compose -f docker-compose.prod.yml up -d
```

## 🔍 API Endpoints

### Core Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

### Authentication
- `POST /api/auth/users` - Create user
- `GET /api/auth/users` - List users
- `GET /api/auth/users/{id}` - Get user

### Data Ingestion
- `POST /api/ingest/netflix` - Upload Netflix CSV
- `POST /api/ingest/youtube/start` - Start YouTube OAuth
- `POST /api/ingest/youtube/callback` - Handle OAuth callback
- `GET /api/ingest/status/{task_id}` - Check ingestion status

### Items & Recommendations
- `GET /api/items` - List media items
- `GET /api/recommendations` - Get user recommendations
- `POST /api/recommendations/refresh` - Refresh recommendations

### Background Jobs
- `GET /api/jobs/{task_id}` - Get job status
- `GET /api/jobs` - List active jobs
- `DELETE /api/jobs/{task_id}` - Cancel job

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run linting and formatting
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

- **Issues**: Create a GitHub issue
- **Documentation**: Check the `/docs` endpoint when running
- **Community**: Join our discussions

## 🔮 Roadmap

### ✅ Completed Features
- [x] User authentication with NextAuth
- [x] Advanced analytics dashboard
- [x] Export and backup functionality

### 🚧 In Progress
- [x] Basic recommendation algorithms (content-based with embeddings)
- [ ] Advanced recommendation algorithms (collaborative filtering, deep learning)

### 🔮 Future Features
- [ ] Social features and sharing
- [ ] Mobile app
- [ ] More streaming platform integrations (Hulu, Disney+, etc.)
- [ ] Real-time notifications and webhooks
- [ ] Advanced user preferences and learning
- [ ] Content discovery and trending
- [ ] Integration with external recommendation services
