# rag_fast_api

A containerized Retrieval‑Augmented Generation (RAG) API using FastAPI, Ollama, and PostgreSQL with pgvector. This project allows users to upload documents and query them using an LLM with context-aware responses powered by embeddings.

## Features

- FastAPI backend with REST API
- RAG pipeline using Ollama with GPU support (via NVIDIA Docker runtime)
- PostgreSQL + pgvector for semantic storage and querying
- Docker Compose setup including:
  - API service
  - Ollama with optional GPU
  - PostgreSQL database
  - pgAdmin for DB inspection
- Upload and query `.txt` documents easily via the Swagger UI

## Architecture

```
                      +-------------+
                      |   Client    |
                      +------+------+
                             |
                             v
                    +--------+--------+
                    |    FastAPI      |
                    |   (web service) |
                    +--------+--------+
                             |
           +----------------+----------------+
           |                                 |
           v                                 v
   +---------------+               +-----------------+
   |   PostgreSQL  |               |     Ollama      |
   |  + pgvector   |               | (LLM Inference) |
   +---------------+               +-----------------+
```

## Getting Started

### Prerequisites

- Docker & Docker Compose
- NVIDIA GPU with drivers (optional, for accelerated inference)

### Clone the Repository

```
git clone https://github.com/Dikar265/rag_fast_api.git
cd rag_fast_api
```

### Run with Docker

```
docker compose up --build
```

This will start the following containers:

- `fastapi_rag`: FastAPI application
- `ollama_rag`: Ollama service with GPU support
- `postgres_rag`: PostgreSQL with pgvector enabled
- `pgadmin_rag`: Access pgAdmin at [http://localhost:5050](http://localhost:5050)

> Default pgAdmin credentials:
> - **Email**: `admin@admin.com`
> - **Password**: `admin`

### Environment Variables

The `web` service reads the PostgreSQL URL from the following variable:

```
URL_DATABASE=postgresql+psycopg2://postgres:postgres@db:5432/ragdb
```

Modify `.env` as needed.

## API Documentation

Once running, visit:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc UI: [http://localhost:8000/redoc](http://localhost:8000/redoc)

You can:

- Upload `.txt` documents
- Query uploaded documents using `/query`

## Database Initialization

If needed, place SQL files inside the `./init_db` directory. These will run automatically when the `db` service starts for the first time.

Example: creating tables and enabling the `vector` extension.

## Project Structure

```
.
├── main.py
├── auth.py
├── database.py
├── models.py
├── schemas.py
├── utils/
│   └── ...
├── Dockerfile
├── Dockerfile.ollama
├── docker-compose.yml
├── requirements.txt
├── init_db/
│   └── init.sql
├── .env
```

## Using GPU (optional but recommended)

If you have an NVIDIA GPU (e.g., RTX 4070), you can enable GPU acceleration so the model runs much faster.

### Step 1: Install NVIDIA Container Toolkit in WSL2

```
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### Step 2: Verify that Docker detects your GPU

```
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi
```

If successful, you should see a table with your GPU information (name, memory, usage, temperature, etc.).

Also, make sure your `docker-compose.yml` includes the following under `ollama`:

```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
```

> Note: You'll also need to have `nvidia-container-toolkit` properly configured in your Docker runtime.

## License

This project is released under the MIT License. Feel free to modify and use it as you like.
