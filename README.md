# RAG FastAPI

An API built with **FastAPI**, **PostgreSQL + pgvector**, and **Ollama** that allows you to:  
- Upload PDF documents related to diseases.  
- Extract text, split it into chunks, and generate embeddings.  
- Ask natural language questions about the documents using an LLM.  

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Dikar265/rag_fast_api.git
cd rag_fast_api

# 2. Create .env file
echo "URL_DATABASE=postgresql+psycopg2:dsadsa//postgres:postgres@db:5432/ragdb
OLLAMA_HOST=http://ollama:11434" > .env

# 3. Run with Docker
docker compose up -d

### ⏳ Wait for Mistral to download

After running `docker compose up -d`, Ollama will start downloading the **Mistral** model.
This may take several minutes.

Check progress with:

```bash
docker compose logs -f ollama
