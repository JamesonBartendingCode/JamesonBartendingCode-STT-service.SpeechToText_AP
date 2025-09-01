# Speech-to-Text (STT) Service

English-only Speech-to-Text microservice using **FastAPI** + **Whisper** (`faster-whisper`).
Designed to be plug-and-play: output JSON can later be passed to a translator
module and the triage engine with no code changes here.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn stt_api:app --reload --port 8000
