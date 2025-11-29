#fastapi backend for meeting summarizer
#exposes speech-to-text and text summarization as rest api endpoints

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import tempfile
import os
import sys
import uuid
from datetime import datetime

#add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#lazy load models to avoid loading on startup
speech_to_text = None
text_summarizer = None

app = FastAPI(
    title="Meeting Summarizer API",
    description="API for transcribing audio and summarizing text",
    version="1.0.0"
)

#cors middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#request/response models
class SummarizeRequest(BaseModel):
    text: str
    max_length: Optional[int] = 150
    min_length: Optional[int] = 30


class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int


class TranscriptionResponse(BaseModel):
    text: str
    language: str
    duration_seconds: Optional[float] = None


class ProcessMeetingRequest(BaseModel):
    audio_base64: Optional[str] = None
    text: Optional[str] = None
    max_summary_length: Optional[int] = 150
    min_summary_length: Optional[int] = 30


class ProcessMeetingResponse(BaseModel):
    meeting_id: str
    transcription: Optional[str] = None
    summary: str
    language: Optional[str] = None
    processed_at: str


#helper functions to lazy-load models
def get_speech_to_text():
    global speech_to_text
    if speech_to_text is None:
        from models.speechToText import SpeechToText
        speech_to_text = SpeechToText(model_size="base")
    return speech_to_text


def get_text_summarizer():
    global text_summarizer
    if text_summarizer is None:
        from models.textSummarizer import TextSummarizer
        text_summarizer = TextSummarizer()
    return text_summarizer


#api endpoints
@app.get("/")
async def root():
    return {"message": "Meeting Summarizer API", "status": "running"}


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "models": {
            "speech_to_text": speech_to_text is not None,
            "text_summarizer": text_summarizer is not None
        }
    }


#transcribe an audio file to text using whisper
#accepts audio files (mp3, wav, webm, m4a, etc.)
@app.post("/api/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    #save uploaded file temporarily
    suffix = os.path.splitext(file.filename)[1] or ".webm"
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        #transcribe
        stt = get_speech_to_text()
        result = stt.transcribe(tmp_path)
        
        return TranscriptionResponse(
            text=result["text"],
            language=result["language"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    
    finally:
        #clean up temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


#summarize the given text using bart model
@app.post("/api/summarize", response_model=SummarizeResponse)
async def summarize_text(request: SummarizeRequest):
    if not request.text or len(request.text.strip()) < 50:
        raise HTTPException(
            status_code=400, 
            detail="Text is too short to summarize. Minimum 50 characters required."
        )
    
    try:
        summarizer = get_text_summarizer()
        summary = summarizer.summarize(
            request.text,
            max_length=request.max_length,
            min_length=request.min_length
        )
        
        return SummarizeResponse(
            summary=summary,
            original_length=len(request.text.split()),
            summary_length=len(summary.split())
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")


#full pipeline: transcribe audio and summarize in one call
#this is the main endpoint for processing meeting recordings
@app.post("/api/process-meeting", response_model=ProcessMeetingResponse)
async def process_meeting(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No audio file provided")
    
    suffix = os.path.splitext(file.filename)[1] or ".webm"
    tmp_path = None
    
    try:
        #save uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        #step 1: transcribe
        stt = get_speech_to_text()
        transcription_result = stt.transcribe(tmp_path)
        transcription_text = transcription_result["text"]
        detected_language = transcription_result["language"]
        
        #step 2: summarize
        summarizer = get_text_summarizer()
        
        if len(transcription_text.split()) < 20:
            #too short to summarize, return transcription as summary
            summary = transcription_text
        else:
            summary = summarizer.summarize(
                transcription_text,
                max_length=150,
                min_length=30
            )
        
        return ProcessMeetingResponse(
            meeting_id=str(uuid.uuid4()),
            transcription=transcription_text,
            summary=summary,
            language=detected_language,
            processed_at=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


#preload ml models in the background for faster first request
#call this on app startup
@app.post("/api/preload-models")
async def preload_models(background_tasks: BackgroundTasks):
    def load():
        get_speech_to_text()
        get_text_summarizer()
    
    background_tasks.add_task(load)
    return {"message": "Models loading in background"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
