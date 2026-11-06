from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import uuid

app = FastAPI(title="VOICE GRIND AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["null"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".flac", ".m4a"}

@app.get("/")
def home():
    return {
        "status": "online",
        "message": "VOICE GRIND AI Backend is running"
    }

@app.post("/upload")
async def upload_audio(
    audio: UploadFile = File(...)
):
    extension = Path(audio.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only WAV, MP3, FLAC and M4A files are allowed."
        )

    filename = f"{uuid.uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
    finally:
        await audio.close()

    return {
        "status": "uploaded",
        "filename": filename
    }