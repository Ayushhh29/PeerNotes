# 📚 PeerNotes – AI-Powered Smart Study Platform

PeerNotes is an AI-powered study assistant that enables students to upload PDF notes and instantly generate summaries, quizzes, flashcards, and interact with their notes through an AI chatbot.

The project aims to make studying faster, smarter, and more interactive using Generative AI.

---

## 🚀 Live Demo

**Deployed Application:**

https://peernotes-57gk.onrender.com

---

## ✨ Features

* 🔐 User Registration & Login Authentication
* 📄 Upload PDF Notes
* 📖 View Uploaded PDFs
* 🧠 AI-Powered Note Summarization
* ❓ Automatic Quiz Generation
* 📝 AI Flashcard Generation
* 💬 Chat with Uploaded Notes
* ⭐ Bookmark Important Notes
* 📚 Study History Tracking
* 📥 Export Summaries as PDF
* 📂 Personal Dashboard
* 📅 Upload Date Tracking

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* SQLAlchemy
* SQLite
* PyPDF2
* ReportLab

### AI

* Google Gemini API

### Frontend

* HTML
* CSS
* Bootstrap
* JavaScript

### Deployment

* Render
* GitHub

---

## 📂 Project Structure

```
PeerNotes
│
├── backend
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── services
│   ├── templates
│   ├── static
│   ├── uploads
│   └── requirements.txt
│
├── .gitignore
├── Procfile
└── README.md
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone <repository-url>
```

Navigate to the backend

```bash
cd backend
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```
GEMINI_API_KEY=YOUR_API_KEY
```

Run the application

```bash
python app.py
```

---

## 🧠 AI Features

* Intelligent PDF Summarization
* Quiz Generation
* Flashcard Generation
* Chat with Uploaded Notes
* Context-aware Responses

---

## 🌐 Deployment

Backend deployed on Render.

---

## 📌 Future Improvements

* PostgreSQL / MongoDB integration
* Cloudinary or AWS S3 for PDF storage
* JWT Authentication
* React Frontend
* Multi-language Support
* Dark Mode
* AI Study Planner
* OCR for scanned PDFs

---

## 👨‍💻 Author

Ayush

---

## 📄 License

This project is intended for educational and portfolio purposes.
