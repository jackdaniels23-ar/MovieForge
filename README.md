# 🎬 MovieForge

**Forge your movie collection, watch anywhere**

A cloud-based movie streaming server with per-movie authentication.

## 🌐 Live Demo

[![Deployed on Railway](https://img.shields.io/badge/Railway-Deployed-blue)](https://movieforge.up.railway.app)

**Live URL:** https://movieforge.up.railway.app

## ✨ Features

- ☁️ **Cloud Hosted** - Always online, accessible from anywhere
- 🔐 **Per-Movie Authentication** - Each movie has unique credentials
  - Username = Movie Name
  - Password = Hero Name
- 📱 **Access Anywhere** - Desktop, mobile, tablet, smart TV
- 🚀 **One-Click Deploy** - Deploy to Railway, Render, or Heroku
- 📊 **API Endpoints** - Programmatic access
- 🔒 **Secure** - Password protected access

## 🔑 Credentials

| Movie | Username | Password |
|-------|----------|----------|
| Athiradi | adhiradi | basiljoseph |

## 🚀 Deploy Now

### Railway (Recommended)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/deploy)

### Render
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## 📦 Installation

```bash
git clone https://github.com/jackdaniels23-ar/MovieForge.git
cd MovieForge
pip install -r requirements.txt
python app.py
```

## 📡 API Endpoints

- `/api/movies` - List all movies
- `/api/auth` - Get credentials
- `/api/url` - Get server URL

## 🔧 Configuration
Add new movies in `app.py`:

```python
USERS = {
    "adhiradi": "basiljoseph",
    "new_movie": "hero_name",
}

MOVIES = {
    "adhiradi": {
        "name": "Athiradi",
        "hero": "Basil Joseph",
        "uploaded": False,
        "filename": None,
        "size": None
    },
    "new_movie": {
        "name": "New Movie",
        "hero": "Hero Name",
        "uploaded": False,
        "filename": None,
        "size": None
    }
}
```

## 📝 License
MIT License

## 👤 Author
**jackdaniels23-ar**

- GitHub: [@jackdaniels23-ar](https://github.com/jackdaniels23-ar)

---
**🎬 Watch your movies anywhere, anytime!**
