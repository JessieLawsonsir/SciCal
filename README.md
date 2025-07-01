# 🔢 Scientific Calculator API (FastAPI)

A secure, full-featured **Scientific Calculator API** built using **FastAPI**.  
This project supports complex mathematical operations, user authentication, asynchronous background tasks, audio streaming, and logs operations to a MySQL database.

---

## 🚀 Features

- ✨ FastAPI-based backend
- 🔐 Token-based authentication with OAuth2
- 🔢 Scientific calculations (addition, subtraction, etc.)
- ⏱️ Async background logging with `loguru`
- 🎵 Audio streaming from `/music` directory
- 💾 Logging with MySQL + Seq support (optional)

---

## 📂 Project Structure

```
SciCal/
├── main.py               # Core FastAPI app with routes
├── requirements.txt      # All Python dependencies
├── README.md             # Project documentation
├── .gitignore            # File exclusion rules
└── music/                # MP3 tracks for streaming
    ├── track1.mp3
    ├── track2.mp3
```

---

## 🛠️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/SciCal.git
cd SciCal
```

2. **Create a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
uvicorn main:app --reload
```

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access the Swagger UI.

---

## 🔐 Authentication

This API uses OAuth2 password flow.

- Obtain a token via `/token` by passing username & password.
- Use the token to access protected endpoints.

---

## 🎧 Music Streaming

Use:
```
GET /music/{track_name}
```

Example:
```
GET /music/track1.mp3
```

Streams MP3s stored inside the `music/` folder.

---

## 📦 Tech Stack

- **FastAPI**
- **Uvicorn**
- **SQLAlchemy**
- **MySQL**
- **Loguru**
- **Python-JOSE + Passlib**
- **Swagger UI**

---

## 📌 Future Improvements

- Deploy online (Render, PythonAnywhere, etc.)
- Add calculator history per user
- Add frontend interface (React or Streamlit)
- Host sample demo video or GIF

---

## 👤 Author

**Palle Jessie Lawson**

> "Observe the way I observe."
