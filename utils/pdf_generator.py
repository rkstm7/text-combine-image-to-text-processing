from fpdf import FPDF
import os

def generate_pdf(username, user_text, ai_caption, similarity, image_path, output_path):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"Report for {username}", ln=True, align='C')

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"User Text: {user_text}", ln=True)
    pdf.cell(200, 10, f"AI Caption: {ai_caption}", ln=True)
    pdf.cell(200, 10, f"Similarity Score: {similarity}%", ln=True)

    if os.path.exists(image_path):
        pdf.image(image_path, x=10, y=60, w=180)

    pdf.output(output_path)