import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import tempfile
import os


# ----------------------------------------------------
# Function to create the worksheet PDF
# ----------------------------------------------------
def create_reading_worksheet(
    output_path,
    title,
    instruction,
    words,
    image_files,
):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    left_margin = 0.75 * inch
    right_margin = 0.75 * inch

    # ---------- Header ----------
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2.0, height - 0.75 * inch, title)

    # Name line
    c.setFont("Helvetica", 12)
    name_y = height - 1.1 * inch
    c.drawString(left_margin, name_y, "Name:")
    c.line(left_margin + 45, name_y - 2, width - right_margin, name_y - 2)

    # Instruction
    c.setFont("Helvetica", 14)
    instr_y = height - 1.7 * inch
    c.drawCentredString(width / 2.0, instr_y, instruction)

    # ---------- Rows (picture + bullet + word) ----------
    start_y = height - 2.6 * inch
    row_height = 1.7 * inch

    img_w = 2.6 * inch
    img_h = 1.2 * inch

    bullet_x = left_margin + img_w + 0.6 * inch
    word_x = bullet_x + 0.35 * inch

    for i, word in enumerate(words):
        row_top = start_y - i * row_height
        img_y = row_top - img_h

        # Rectangle for image
        c.setLineWidth(1)
        c.rect(left_margin, img_y, img_w, img_h)

        # Draw uploaded image if provided
        if image_files[i]:
            temp_img_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
            with open(temp_img_path, "wb") as f:
                f.write(image_files[i].read())

            padding = 0.1 * inch
            c.drawImage(
                temp_img_path,
                left_margin + padding,
                img_y + padding,
                img_w - 2 * padding,
                img_h - 2 * padding,
                preserveAspectRatio=True,
                anchor="sw",
            )

            os.remove(temp_img_path)

        # Bullet
        bullet_y = img_y + img_h / 2.0
        c.setFont("Helvetica-Bold", 20)
        c.drawString(bullet_x, bullet_y - 7, "•")

        # Word
        c.setFont("Helvetica", 26)
        c.drawString(word_x, bullet_y - 9, word)

    c.showPage()
    c.save()


# ----------------------------------------------------
# Streamlit UI
# ----------------------------------------------------
st.title("📘 Reading Practice Worksheet Generator")
st.write("Create a printable matching worksheet for young learners (K–3).")

st.divider()

# Worksheet settings
title = st.text_input("Worksheet Title", "Reading Practice Worksheet")
instruction = st.text_input("Instruction", "Match the pictures with the words.")
num_items = st.slider("How many matching items?", 3, 5, 3)

# Input words
words = []
st.subheader("Enter Words")
for i in range(num_items):
    words.append(st.text_input(f"Word {i+1}", ""))

# Upload images
st.subheader("Upload Images (Optional)")
image_files = []
for i in range(num_items):
    img = st.file_uploader(f"Image for Word {i+1}", type=["png", "jpg", "jpeg"])
    image_files.append(img)

st.divider()

# Generate PDF
if st.button("Generate Worksheet"):
    # Validate inputs
    if any(w.strip() == "" for w in words):
        st.error("Please fill in all words.")
    else:
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name

        create_reading_worksheet(
            output_path=temp_pdf,
            title=title,
            instruction=instruction,
            words=words,
            image_files=image_files,
        )

        with open(temp_pdf, "rb") as pdf_file:
            st.success("Worksheet generated successfully!")
            st.download_button(
                label="⬇️ Download PDF Worksheet",
                data=pdf_file.read(),
                file_name="reading_practice_worksheet.pdf",
                mime="application/pdf",
            )

        os.remove(temp_pdf)
