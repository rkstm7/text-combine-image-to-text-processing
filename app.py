# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from PIL import Image
from utils.ai_helper import describe_image, calculate_similarity
from utils.pdf_generator import generate_pdf
from werkzeug.utils import secure_filename
import os
import mysql.connector
import config

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Uploads folder config
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database connection
conn = mysql.connector.connect(
    host=config.MYSQL_HOST,
    user=config.MYSQL_USER,
    password=config.MYSQL_PASSWORD,
    database=config.MYSQL_DB
)
cursor = conn.cursor(dictionary=True)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            session["user"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))
        else:
            return render_template("index.html", error="Invalid credentials")
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return render_template("register.html", error="Username already exists")
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        file = request.files["image"]
        user_text = request.form["user_text"]

        # Save uploaded image
        filename = secure_filename(file.filename)
        relative_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        absolute_image_path = os.path.abspath(relative_image_path)
        file.save(absolute_image_path)

        # Process image and text
        image = Image.open(absolute_image_path).convert("RGB")
        ai_caption = describe_image(image)
        similarity = float(calculate_similarity(user_text, ai_caption))

        # Generate PDF path
        pdf_filename = f"{filename.split('.')[0]}_result.pdf"
        relative_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
        absolute_pdf_path = os.path.abspath(relative_pdf_path)
        generate_pdf(session["username"], user_text, ai_caption, similarity, relative_image_path, relative_pdf_path)

        # Insert into DB
        cursor.execute("""
            INSERT INTO results (user_id, image_path, user_text, ai_caption, similarity)
            VALUES (%s, %s, %s, %s, %s)
        """, (session["user"], relative_image_path, user_text, ai_caption, similarity))
        conn.commit()

        return render_template("result.html",
                               combined_caption=f"User Input: {user_text} | AI Description: {ai_caption}",
                               similarity=similarity,
                               image_url='/' + relative_image_path.replace('\\', '/'),
                               pdf_url='/' + relative_pdf_path.replace('\\', '/'))

    return render_template("dashboard.html", username=session["username"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)