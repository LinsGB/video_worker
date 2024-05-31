from fastapi import FastAPI
from src.video_worker import VideoWorker
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ISetUrl(BaseModel):
    url: str

@app.post("/set_url")
async def set_url(payload: ISetUrl):
    return VideoWorker.set_url(payload.url)

@app.get("/saved_data")
async def get_saved_data():
    return VideoWorker.get_cached_data()

@app.get("/original_audio")
async def get_original_audio():
    VideoWorker.stream_original_audio()
    return StreamingResponse(VideoWorker.stream_original_audio(), media_type="audio/mpeg")

@app.get("/translated_audio")
async def get_translated_audio():
    VideoWorker.stream_original_audio()
    return StreamingResponse(VideoWorker.stream_translated_audio(), media_type="audio/mpeg")
