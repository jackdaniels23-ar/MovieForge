#!/usr/bin/env python3
"""
MovieForge - Cloud movie server
"""

import json
import os
import secrets
from flask import Flask, request, jsonify, render_template_string, send_file, redirect
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

UPLOAD_FOLDER = "/tmp/movies" if os.environ.get("RAILWAY_ENV") else "movies"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def load_config():
    try:
        with open("config.json", "r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        return None


CONFIG = load_config()
if CONFIG:
    USERS = CONFIG.get("users", {})
    MOVIES = {}
    for username, movie in CONFIG.get("movies", {}).items():
        MOVIES[username] = {
            "name": movie.get("name", username),
            "hero": movie.get("hero", "Unknown"),
            "uploaded": movie.get("uploaded", False),
            "filename": movie.get("filename"),
            "size": movie.get("size"),
            "description": movie.get("description", ""),
        }
else:
    USERS = {"adhiradi": "basiljoseph"}
    MOVIES = {
        "adhiradi": {
            "name": "Athiradi",
            "hero": "Basil Joseph",
            "uploaded": False,
            "filename": None,
            "size": None,
            "description": "Action thriller movie",
        }
    }


def get_base_url():
    if os.environ.get("RAILWAY_STATIC_URL"):
        return f"https://{os.environ.get('RAILWAY_STATIC_URL')}"
    if os.environ.get("HEROKU_APP_NAME"):
        return f"https://{os.environ.get('HEROKU_APP_NAME')}.herokuapp.com"
    if os.environ.get("RENDER_EXTERNAL_URL"):
        return os.environ.get("RENDER_EXTERNAL_URL")
    return "http://localhost:5000"


@app.route("/")
def index():
    base_url = get_base_url()
    html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>🎬 MovieForge</title>
  <style>
    body {{ font-family: Arial, sans-serif; background: #111; color: #fff; margin: 0; padding: 20px; }}
    .container {{ max-width: 900px; margin: 0 auto; }}
    .card {{ background: #1b1b1b; padding: 20px; border-radius: 12px; margin-bottom: 20px; }}
    .btn {{ display: inline-block; padding: 10px 16px; background: #ff4d4d; color: #fff; text-decoration: none; border-radius: 8px; margin-top: 10px; }}
    input[type=file] {{ display: block; margin: 10px 0; }}
    input[type=submit] {{ background: #ff4d4d; color: #fff; border: none; padding: 10px 16px; border-radius: 8px; cursor: pointer; }}
  </style>
</head>
<body>
  <div class=\"container\">
    <h1>🎬 MovieForge</h1>
    <p>Cloud hosted movie server with credentials.</p>
    <div class=\"card\">
      <h2>🌐 Server URL</h2>
      <p>{base_url}</p>
      <a class=\"btn\" href=\"{base_url}\">Open Server</a>
    </div>
    <div class=\"card\">
      <h2>🔐 Credentials</h2>
      <p>Username: adhiradi</p>
      <p>Password: basiljoseph</p>
    </div>
    <div class=\"card\">
      <h2>🎥 Upload Movie</h2>
      <form action=\"{base_url}/upload/adhiradi\" method=\"post\" enctype=\"multipart/form-data\">
        <input type=\"file\" name=\"movie\" accept=\".mp4,.mkv,.avi,.mov\" required>
        <input type=\"submit\" value=\"Upload Movie\">
      </form>
    </div>
  </div>
</body>
</html>
"""
    return render_template_string(html)


@app.route("/upload/<username>", methods=["POST"])
def upload_movie(username):
    if username not in MOVIES:
        return "Movie not found", 404
    if "movie" not in request.files:
        return "No file uploaded", 400
    file = request.files["movie"]
    if file.filename == "":
        return "No file selected", 400
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    MOVIES[username]["uploaded"] = True
    MOVIES[username]["filename"] = filename
    MOVIES[username]["size"] = os.path.getsize(file_path)
    return redirect("/")


@app.route("/watch/<username>")
def watch_movie(username):
    if username not in MOVIES:
        return "Movie not found", 404
    movie = MOVIES[username]
    if not movie["uploaded"]:
        return "Movie not uploaded yet", 404
    html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>Watching {movie['name']}</title>
</head>
<body>
  <h1>{movie['name']}</h1>
  <video controls autoplay width=\"100%\">
    <source src=\"/stream/{username}\" type=\"video/mp4\">
  </video>
</body>
</html>
"""
    return render_template_string(html)


@app.route("/stream/<username>")
def stream_movie(username):
    if username not in MOVIES:
        return "Movie not found", 404
    movie = MOVIES[username]
    if not movie["uploaded"]:
        return "Movie not uploaded", 404
    file_path = os.path.join(UPLOAD_FOLDER, movie["filename"])
    if not os.path.exists(file_path):
        return "File not found", 404
    return send_file(file_path, conditional=True)


@app.route("/api/movies")
def api_movies():
    return jsonify(MOVIES)


@app.route("/api/auth")
def api_auth():
    return jsonify(USERS)


@app.route("/api/url")
def api_url():
    return jsonify({"url": get_base_url(), "credentials": USERS, "movies": MOVIES})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, threaded=True)
