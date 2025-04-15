from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from yt_dlp import YoutubeDL

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PreviewRequest(BaseModel):
    url: str
    format: str  # "mp4" or "mp3"

@app.post("/preview")
async def preview_reel(req: PreviewRequest):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
        "extract_flat": False,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(req.url, download=False)

        formats = info.get("formats", [])
        selected_url = None

        # Handle MP4 (video) or MP3 (audio-only)
        if req.format == "mp4":
            for fmt in formats:
                if (
                    fmt.get("ext") == "mp4"
                    and fmt.get("vcodec") != "none"
                    and fmt.get("acodec") != "none"
                ):
                    selected_url = fmt.get("url")
                    break
        elif req.format == "mp3":
            for fmt in formats:
                if (
                    fmt.get("vcodec") == "none"
                    and fmt.get("acodec") != "none"
                ):
                    selected_url = fmt.get("url")
                    break

        if not selected_url:
            return {"error": f"No {req.format.upper()} format found."}

        return {
            "caption": info.get("description", "No caption"),
            "uploader": info.get("uploader", "Unknown"),
            "video_url": selected_url,
        }

    except Exception as e:
        return {"error": str(e)}
