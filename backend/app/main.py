from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from .video_gen import generate_video_from_prompt

load_dotenv()  # Load .env variables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for dev. Restrict in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate-video/")
async def generate_video(request: PromptRequest):
    try:
        video_path = await generate_video_from_prompt(request.prompt)
        if not video_path or not os.path.exists(video_path):
            print("❌ Video generation failed in backend.")
            raise HTTPException(status_code=500, detail="Video generation failed.")
        return {"video_url": f"/video?path={os.path.basename(video_path)}"}
    except Exception as e:
        print("❌ Exception in generate_video:", e)
        return JSONResponse(status_code=500, content={"error": "Video generation failed."})

@app.get("/video")
def get_video(path: str):
    temp_dir = "/tmp"
    video_path = os.path.join(temp_dir, path)
    if not os.path.exists(video_path):
        print("❌ Requested video not found:", video_path)
        raise HTTPException(status_code=404, detail="Video not found.")
    return FileResponse(video_path, media_type="video/mp4")