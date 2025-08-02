from flask import Flask, request, jsonify, send_from_directory
from yt_dlp import YoutubeDL
import os, uuid

app = Flask(__name__)
DOWNLOAD_DIR = "./downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL"}), 400

    filename = str(uuid.uuid4())
    output = f"{DOWNLOAD_DIR}/{filename}.%(ext)s"

    opts = {
        "outtmpl": output,
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True
    }

    try:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
        ext = "mp4"
        file_url = f"{request.host_url}downloads/{filename}.{ext}"
        return jsonify({"title": info.get("title"), "file_url": file_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/downloads/<name>")
def serve(name):
    return send_from_directory(DOWNLOAD_DIR, name)
