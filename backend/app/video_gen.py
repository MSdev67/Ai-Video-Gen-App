import os
import requests
import tempfile

STABILITY_API_URL = "https://api.stability.ai/v2beta/video/generate"

def get_api_key():
    return os.getenv("STABILITY_API_KEY")

async def generate_video_from_prompt(prompt: str) -> str:
    api_key = get_api_key()
    if not api_key:
        print("❌ Stability AI API key is missing in environment variables.")
        return None

    headers = {
        "Authorization": f"Bearer ",
        "Accept": "application/json"
    }
    payload = {
        "prompt": prompt,
        "output_format": "mp4"
    }
    try:
        response = requests.post(STABILITY_API_URL, headers=headers, json=payload, timeout=120)
    except Exception as e:
        print("❌ Error during POST to Stability API:", e)
        return None

    if response.status_code != 200:
        print("❌ Stability API returned error:", response.text)
        return None

    resp_json = response.json()
    video_url = resp_json.get("video_url")
    if not video_url:
        print("❌ No video_url in Stability API response:", resp_json)
        return None

    # Download the video file
    try:
        video_response = requests.get(video_url, stream=True)
        if video_response.status_code != 200:
            print("❌ Error downloading video from", video_url)
            return None
        temp_dir = tempfile.gettempdir()
        temp_video_path = os.path.join(temp_dir, f"result_{os.getpid()}.mp4")
        with open(temp_video_path, "wb") as f:
            for chunk in video_response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return temp_video_path
    except Exception as e:
        print("❌ Error saving video:", e)
        return None