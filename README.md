# 🧠 AI-Powered Image + Text Analyzer

An intelligent Flask-based web application that processes an image and user-provided text to:
- Generate an AI-powered image description (caption)
- Calculate semantic similarity between image and user text
- Generate a detailed result as a downloadable PDF
- Save everything in a MySQL database for user tracking

![Demo](static/assets/demo.gif) <!-- Replace with your actual demo path -->

---

## 🚀 Features

- 🔐 **User Authentication** – Register and login securely
- 🖼️ **Image Upload** – Upload and process any image
- ✍️ **Text Input** – Provide your own interpretation or caption
- 🤖 **AI Description** – Generate image caption using BLIP (or similar)
- 📊 **Similarity Score** – NLP-based semantic similarity comparison
- 📄 **Auto PDF Generation** – Generate and download a result report
- 🗂️ **Database Storage** – Save results with user ID in MySQL
- 📁 **File Uploads** – Automatically managed in `/static/uploads/`

---

## 🛠️ Technologies Used

- **Flask** – Lightweight Python web framework
- **MySQL** – Relational database
- **Pillow (PIL)** – Image processing
- **Transformers** – AI image captioning
- **PDF Generator** – Custom utility using `reportlab` or similar
- **Jinja2** – Templating engine
- **HTML/CSS/Bootstrap** – Frontend UI

---

## 🗃️ Project Structure

