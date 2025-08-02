from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/')
def home():
    return 'yt-dlp server is running!'

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing YouTube URL'}), 400

    video_url = data['url']
    temp_id = str(uuid.uuid4())
    output_path = f'/tmp/{temp_id}.mp4'

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': output_path,
        'merge_output_format': 'mp4',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return send_file(output_path, mimetype='video/mp4', as_attachment=True, download_name='video.mp4')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
