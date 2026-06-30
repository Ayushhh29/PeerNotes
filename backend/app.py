from flask import Flask, request, jsonify
import PyPDF2
from services.summarizer import generate_summary      #function made in summarizer.py
from services.summarizer import summarize_large_text
from services.summarizer import generate_answer
from flask import send_file
from flask import render_template
import os
from flask import send_from_directory
from services.quiz_generator import generate_quiz
from services.flashcards import generate_flashcards
from database import db
from models import Note, User
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import session
from flask import redirect
from models import SavedSummary,  SavedQuiz, SavedFlashcard
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_file
from models import Bookmark
from models import StudyHistory
from services.gemini import chat_with_notes

app = Flask(__name__)
app.secret_key = "peernotes_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

with app.app_context():
    db.create_all()

    print("Database created successfully")
print(app.config["SQLALCHEMY_DATABASE_URI"])

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/register-page")
def register_page():
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html"
    )

@app.route("/summarize", methods = ["POST", "GET"])
def summarize():
    data = request.get_json()                  
    text = data.get("text")

    if not text:
        return jsonify({"error": "no text provided"}) , 400

    summary = generate_summary(text)
    return jsonify({"summary" : summary})





@app.route("/summarize-pdf" , methods = ["POST"])
def summarize_pdf():
    if "file" not in request.files:
        return jsonify({"errror":"file not found"})
    
    file = request.files["file"]

    pdf_reader = PyPDF2.PdfReader(file)

    text =""

    for page in pdf_reader.pages:
        text = text + page.extract_text()

    summary = summarize_large_text(text)

    return jsonify({"summary" : summary})


@app.route("/download-summary/<int:summary_id>")
def download_summary(summary_id):

    if "user_id" not in session:
        return jsonify({
            "error": "Please login first"
        }), 401

    summary = SavedSummary.query.get(summary_id)

    if not summary:
        return jsonify({
            "error": "Summary not found"
        }), 404

    pdf_path = f"summary_{summary.id}.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            summary.content,
            styles["BodyText"]
        )
    )

    doc.build(content)

    return send_file(
        pdf_path,
        as_attachment=True
    )

# @app.route("/flowchart", methods=["POST"])
# def flowchart():

#     data = request.get_json()
#     text = data.get("text")

#     if not text:
#         return jsonify({"error": "No text provided"}), 400

   
#     summary = generate_summary(text)

   
#     image_path = generate_flowchart(summary)

#     return jsonify({
#         "summary": summary,
#         "flowchart": f"http://127.0.0.1:5000/{image_path}"

#       })




def extract_pdf_text(filepath):

    text = ""

    with open(filepath, "rb") as file:

        pdf_reader = PyPDF2.PdfReader(file)

        for page in pdf_reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

    return text



@app.route("/process-pdf", methods=["POST"])
def process_pdf(filepath):

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    # Step 1: Read PDF
    import PyPDF2
    pdf_reader = PyPDF2.PdfReader(file)

    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    # Step 2: Generate Summary
    summary = summarize_large_text(text)

    

    return jsonify({
    "summary": summary,
    
})




@app.route("/get-flowchart/<filename>")
def get_flowchart(filename):
    return send_file(filename, mimetype="image/png")





@app.route("/upload-note", methods=["POST"])
def upload_note():

    if "user_id" not in session:
     return jsonify({
        "error": "Please login first"
    }), 401

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    file.save(filepath)

    subject = request.form.get(
    "subject",
    "General"
)

    print("PDF saved")

    note = Note(
    title=file.filename.replace(".pdf", ""),
    filename=file.filename,
    subject=subject,
    user_id=session["user_id"]
)

  

    print("Note object created")

    db.session.add(note)
    db.session.commit()

    print("Inserted into database")

    return jsonify({
        "message": "File uploaded successfully",
        "filename": file.filename
    })

@app.route("/notes")
def notes():

    notes = Note.query.all()

    result = []

    for note in notes:

        result.append({
            "id": note.id,
            "title": note.title,
            "filename": note.filename,
            "subject": note.subject,
            "upload_date": str(note.upload_date)
        })

    return jsonify({
        "notes": result
    })


@app.route("/view-note/<filename>")
def view_note(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


@app.route("/summarize-note/<filename>")
def summarize_note(filename):

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    pdf_reader = PyPDF2.PdfReader(filepath)

    text = ""

    for page in pdf_reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    summary = summarize_large_text(text)

    return jsonify({
        "summary": summary
    })

@app.route("/generate-quiz/<filename>")
def generate_quiz_route(filename):

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    pdf_reader = PyPDF2.PdfReader(filepath)

    text = ""

    for page in pdf_reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    # limit text
    text = text[:2000]

    quiz = generate_quiz(text)

    return jsonify({
        "quiz": quiz
    })


@app.route("/generate-flashcards/<filename>")
def flashcards_route(filename):

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    pdf_reader = PyPDF2.PdfReader(filepath)

    text = ""

    for page in pdf_reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    text = text[:2000]

    flashcards = generate_flashcards(text)

    return jsonify({
        "flashcards": flashcards
    })

@app.route("/delete-note/<int:id>", methods=["DELETE"])
def delete_note(id):

    note = Note.query.get(id)

    if not note:
        return jsonify({
            "error": "Note not found"
        }), 404

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        note.filename
    )

    if os.path.exists(filepath):
        os.remove(filepath)

    db.session.delete(note)
    db.session.commit()

    return jsonify({
        "message": "Note deleted successfully"
    })

@app.route("/search-notes/<keyword>")
def search_notes(keyword):

    notes = Note.query.filter(
        Note.title.ilike(f"%{keyword}%")
    ).all()

    result = []

    for note in notes:

        result.append({
            "id": note.id,
            "title": note.title,
            "filename": note.filename,
            "subject": note.subject,
            "upload_date": str(note.upload_date)
        })

    return jsonify({
        "notes": result
    })

@app.route("/filter-notes/<subject>")
def filter_notes(subject):

    if subject == "All":
        notes = Note.query.all()

    else:
        notes = Note.query.filter_by(
            subject=subject
        ).all()

    result = []

    for note in notes:

        result.append({
            "id": note.id,
            "title": note.title,
            "filename": note.filename,
            "subject": note.subject,
            "upload_date": str(note.upload_date)
        })

    return jsonify({
        "notes": result
    })

@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({
            "error": "All fields are required"
        }), 400

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return jsonify({
            "error": "Email already registered"
        }), 400

    hashed_password = generate_password_hash(password)

    user = User(
        name=name,
        email=email,
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully"
    })

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    if not check_password_hash(
        user.password,
        password
    ):
        return jsonify({
            "error": "Invalid password"
        }), 401
    
    session["user_id"] = user.id

    return jsonify({
            "message": "Login successful",
            "user_id": user.id,
            "name": user.name

 
    })


@app.route("/me")
def me():

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    user = db.session.get(User, user_id)   # preferred in SQLAlchemy 2.x

    if user is None:
        session.clear()
        return jsonify({"error": "User not found"}), 401

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email
    })


@app.route("/logout")
def logout():

    session.clear()

    return jsonify({
        "message": "Logged out"
    })

@app.route("/my-notes")
def my_notes():

    if "user_id" not in session:
        return jsonify({
            "error": "Please login first"
        }), 401

    notes = Note.query.filter_by(
        user_id=session["user_id"]
    ).all()

    result = []

    for note in notes:

        result.append({
            "id": note.id,
            "title": note.title,
            "filename": note.filename,
            "subject": note.subject,
            "upload_date": str(note.upload_date)
        })

    return jsonify({
        "notes": result
    })

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return jsonify({"error":"Login required"}), 401

    user = User.query.get(session["user_id"])

    notes_count = Note.query.filter_by(
        user_id=user.id
    ).count()

    return jsonify({
        "name": user.name,
        "email": user.email,
        "notes_count": notes_count
    })


@app.route("/save-summary", methods=["POST"])
def save_summary():

    if "user_id" not in session:
        return jsonify({
            "error":"Please login first"
        }), 401

    data = request.get_json()

    content = data.get("content")
    note_id = data.get("note_id")

    summary = SavedSummary(
        user_id=session["user_id"],
        note_id=note_id,
        content=content
    )

    db.session.add(summary)
    db.session.commit()

    return jsonify({
        "message":"Summary saved"
    })

@app.route("/summaries")
def get_summaries():

    if "user_id" not in session:
        return jsonify({
            "error": "Please login first"
        }), 401

    summaries = SavedSummary.query.filter_by(
        user_id=session["user_id"]
    ).all()

    result = []

    for summary in summaries:

        note = Note.query.get(summary.note_id)

        result.append({
            "id": summary.id,
            "title": note.title if note else "Unknown Note",
            "content": summary.content,
            "created_at": summary.created_at
        })

    return jsonify({
        "summaries": result
    })

@app.route("/save-quiz", methods=["POST"])
def save_quiz():

    if "user_id" not in session:
        return jsonify({
            "error": "Please login first"
        }), 401

    data = request.get_json()

    quiz = SavedQuiz(
        user_id=session["user_id"],
        note_id=data.get("note_id"),
        content=data.get("content")
    )

    db.session.add(quiz)
    db.session.commit()

    return jsonify({
        "message": "Quiz saved"
    })

@app.route("/quizzes")
def get_quizzes():

    if "user_id" not in session:
        return jsonify({
            "error": "Please login first"
        }), 401

    quizzes = SavedQuiz.query.filter_by(
        user_id=session["user_id"]
    ).all()

    result = []

    for quiz in quizzes:

        note = Note.query.get(
            quiz.note_id
        )

        result.append({
            "title":
                note.title if note else "Unknown Note",

            "content":
                quiz.content
        })

    return jsonify({
        "quizzes": result
    })

@app.route(
    "/save-flashcards",
    methods=["POST"]
)
def save_flashcards():

    if "user_id" not in session:
        return jsonify({
            "error":"Please login first"
        }), 401

    data = request.get_json()

    flashcard = SavedFlashcard(

        user_id=session["user_id"],

        note_id=data.get(
            "note_id"
        ),

        content=data.get(
            "content"
        )

    )

    db.session.add(flashcard)
    db.session.commit()

    return jsonify({
        "message":"Flashcards saved"
    })

@app.route("/flashcards")
def get_flashcards():

    if "user_id" not in session:
        return jsonify({
            "error":
            "Please login first"
        }), 401

    flashcards = SavedFlashcard.query.filter_by(
            user_id=session["user_id"]
        ).all()

    result = []

    for card in flashcards:

        note = Note.query.get(
            card.note_id
        )

        result.append({

            "title":
                note.title
                if note
                else "Unknown Note",

            "content":
                card.content

        })

    return jsonify({
        "flashcards":
        result
    })

@app.route("/chat-notes", methods=["POST"])
def chat_notes():

    if "user_id" not in session:
        return jsonify({"error": "Please login first"}), 401

    data = request.get_json()

    filename = data.get("filename")
    question = data.get("question")

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    text = extract_pdf_text(filepath)

    stop_words = {
        "what", "is", "the", "of", "for",
        "a", "an", "to", "in", "on",
        "and", "or", "does", "do"
    }

    keywords = [
        word.lower()
        for word in question.split()
        if word.lower() not in stop_words
    ]

    sentences = text.split(".")

    relevant = []

    for sentence in sentences:
        for word in keywords:
            if word in sentence.lower():
                relevant.append(sentence)
                break

    context = " ".join(relevant[:15])

    if not context:
        context = text[:3000]

    answer = chat_with_notes(context, question)

    return jsonify({
        "answer": answer
    })

@app.route("/bookmark-note", methods=["POST"])
def bookmark_note():

    if "user_id" not in session:
        return jsonify({
            "error":"Please login first"
        }), 401

    data = request.get_json()

    note_id = data.get("note_id")

    existing = Bookmark.query.filter_by(
        user_id=session["user_id"],
        note_id=note_id
    ).first()

    if existing:
        return jsonify({
            "message":"Already bookmarked"
        })

    bookmark = Bookmark(
        user_id=session["user_id"],
        note_id=note_id
    )

    db.session.add(bookmark)
    db.session.commit()

    return jsonify({
        "message":"Bookmarked successfully"
    })

@app.route("/bookmarks")
def get_bookmarks():

    if "user_id" not in session:
        return jsonify([])

    bookmarks = Bookmark.query.filter_by(
        user_id=session["user_id"]
    ).all()

    result = []

    for bookmark in bookmarks:

        note = Note.query.get(
            bookmark.note_id
        )

        if note:

            result.append({
                "id": note.id,
                "title": note.title,
                "subject": note.subject,
                "filename": note.filename
            })

    return jsonify(result)

@app.route("/add-history", methods=["POST"])
def add_history():

    if "user_id" not in session:
        return jsonify({
            "error":"Login first"
        }),401

    data = request.get_json()

    history = StudyHistory(
        user_id=session["user_id"],
        note_id=data["note_id"],
        action=data["action"]
    )

    db.session.add(history)
    db.session.commit()

    return jsonify({
        "message":"added"
    })

@app.route("/history")
def get_history():

    if "user_id" not in session:
        return jsonify([])

    records = StudyHistory.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        StudyHistory.viewed_at.desc()
    ).limit(20).all()

    result = []

    for record in records:

        note = Note.query.get(record.note_id)

        if note:

            result.append({

                "title": note.title,

                "action": record.action,

                "time": record.viewed_at

            })

    return jsonify(result)



if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
