# Document Ingestion Service

A production-grade document processing pipeline that accepts PDF uploads, extracts and chunks text intelligently, persists structured data to PostgreSQL, and exposes the processed output via a REST API.

---

## What It Does

Upload a PDF. Get back structured, searchable text chunks — each stored in a database, linked to its source document, and returned via API.

```
Upload PDF  →  Extract Text  →  Chunk  →  Store  →  Return via API
```

This kind of pipeline is the foundation of any system that needs to reason over documents — search engines, Q&A systems, knowledge bases, and document intelligence tools.

---

## Architecture

```
Frontend (React)  →  Gateway (Node/Express)  →  AI Service (FastAPI)  →  PostgreSQL
     :5173               :3000                        :8000
```

The system follows an **API Gateway pattern** — the frontend communicates exclusively with the gateway, which proxies requests to the AI service. This decouples the client from internal service topology and keeps the architecture extensible.

---

## Services

### Gateway — `Node.js + Express`

- Accepts multipart file uploads from the frontend via `multer`
- Forwards files to the AI service using `axios` + `form-data`
- Returns the processed response back to the client

### AI Service — `FastAPI + Python`

- Receives uploaded PDF via `UploadFile`
- Persists file to local `uploads/` directory
- Inserts a document record into PostgreSQL via SQLAlchemy
- Extracts raw text page-by-page using **PyMuPDF (`fitz`)**
- Splits text into overlapping chunks using **LangChain `RecursiveCharacterTextSplitter`**
- Persists each chunk to the database linked by `document_id`
- Returns `document_id` and chunk array as JSON

### Frontend — `React + Vite`

- Minimal file upload interface
- Renders returned chunks on successful upload

---

## Database Schema

### `documents`

| Column        | Type      | Description                        |
| ------------- | --------- | ---------------------------------- |
| `id`          | UUID (PK) | Auto-generated document identifier |
| `filename`    | String    | Original filename of uploaded PDF  |
| `uploaded_at` | Timestamp | Time of ingestion                  |

### `chunks`

| Column        | Type         | Description                       |
| ------------- | ------------ | --------------------------------- |
| `id`          | Integer (PK) | Auto-incremented chunk identifier |
| `document_id` | UUID (FK)    | Reference to parent document      |
| `text`        | Text         | Chunk content                     |
| `chunk_index` | Integer      | Position of chunk within document |

---

## Tech Stack

| Layer          | Technology                                 |
| -------------- | ------------------------------------------ |
| Frontend       | React, Vite, Axios                         |
| Gateway        | Node.js, Express, Multer                   |
| AI Service     | Python, FastAPI, Uvicorn                   |
| PDF Parsing    | PyMuPDF (fitz)                             |
| Text Splitting | LangChain `RecursiveCharacterTextSplitter` |
| ORM            | SQLAlchemy                                 |
| Database       | PostgreSQL 14                              |
| Config         | python-dotenv                              |

---

## Project Structure

```
document-ingestion-service/
├── frontend/               # React application
│   └── src/
│       └── App.jsx
├── gateway/                # Express API gateway
│   └── index.js
├── ai-service/             # FastAPI processing service
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── uploads/
│   └── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Node.js
- Python 3.10+
- PostgreSQL 14

### 1. AI Service

```bash
cd ai-service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```
DATABASE_URL=postgresql://<user>@localhost:5432/<dbname>
```

Start the server:

```bash
uvicorn main:app --reload --port 8000
```

### 2. Gateway

```bash
cd gateway
npm install
node index.js
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`, upload a PDF, and observe the extracted chunks rendered on screen.

---

## API Reference

### `POST /upload`

Accepts a multipart form with a `file` field (PDF). Returns:

```json
{
  "document_id": "uuid",
  "chunks": ["chunk text 1", "chunk text 2", "..."]
}
```
