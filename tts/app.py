import tempfile
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.tts_service import TTSService
from services.gpt_service import GPTService
import os
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import whisper
# Initialize FastAPI
app = FastAPI(title="AI Voice TTS Microservice", version="1.0.0")

# Enable CORS (Allow frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or set to ["http://localhost:5173"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize TTS Service
tts_service = TTSService()

# Initialize GPT Service
gpt_service = GPTService(tts_service)
model = whisper.load_model("base")

# Request Model
class TextRequest(BaseModel):
    text: str

# Health Check Endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# TTS Endpoint
@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_file:
            temp_file.write(await audio.read())
            temp_path = temp_file.name

        result = model.transcribe(temp_path)
        os.remove(temp_path)
        return {"text": result["text"]}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/ask")
async def askingQuestion(request: TextRequest):
    return gpt_service.chat_and_speak(request.text, 1)

# Serve static audio files
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# Run FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)