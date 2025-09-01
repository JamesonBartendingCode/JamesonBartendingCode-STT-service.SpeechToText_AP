from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from faster_whisper import WhisperModel
import tempfile

app = FastAPI(title="STT Service", version="0.1.0", description="English-only STT, plug-and-play for translation later.")

# Allow your frontend (or anyone during dev) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model once at startup (small = quick to test)
model = WhisperModel("small", device="cpu")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/stt/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    # save uploaded audio to a temp file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(await audio.read())
        audio_path = f.name

    # force English for MVP; keep language="en"
    segments, info = model.transcribe(audio_path, language="en", vad_filter=True)
    text = "".join(s.text for s in segments).strip()

    return {
        "text": text,
        "lang": "en",
        "confidence": getattr(info, "language_probability", None)
    }
