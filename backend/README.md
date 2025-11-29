# Meeting Summarizer Backend

FastAPI backend that wraps the Python ML models for speech-to-text and text summarization.

## Setup

### 1. Create a Python virtual environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** The first time you install `openai-whisper` and `transformers`, it will download the ML models (~2-3GB). This only happens once.

### 3. Run the server

```bash
# From the project root directory
cd backend
python app.py

# Or using uvicorn directly
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/health` | GET | Detailed health status |
| `/api/transcribe` | POST | Transcribe audio file to text |
| `/api/summarize` | POST | Summarize text |
| `/api/process-meeting` | POST | Full pipeline: transcribe + summarize |
| `/api/preload-models` | POST | Preload ML models in background |

## Usage Examples

### Transcribe Audio
```bash
curl -X POST "http://127.0.0.1:8000/api/transcribe" \
  -F "file=@recording.webm"
```

### Summarize Text
```bash
curl -X POST "http://127.0.0.1:8000/api/summarize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your long text here...", "max_length": 150}'
```

### Process Full Meeting
```bash
curl -X POST "http://127.0.0.1:8000/api/process-meeting" \
  -F "file=@meeting-recording.webm"
```

## Running with Frontend

1. Start the backend server (port 8000)
2. Start the Vue frontend: `npm run dev` (port 5173)
3. The Vite proxy will forward `/api/*` requests to the backend

## GPU Support

If you have an NVIDIA GPU with CUDA installed, the models will automatically use GPU acceleration for faster processing.

