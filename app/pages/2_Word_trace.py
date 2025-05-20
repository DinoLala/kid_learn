import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

import json
import random
# Page setup
st.set_page_config(page_title="Word Tracing Worksheet", layout="centered")
st.title("✏️ Word Tracing Worksheet Generator")
st.markdown("Create a **printable worksheet** with traceable dotted words – great for early writers!")

# Input
col1, col2, col3 = st.columns(3)
with col1:
    child_name = st.text_input("Child's Name (optional):")
    word_category= st.selectbox("Category", ['Common words', 'Animals', 'Numbers'])
    if word_category =='Animals':
        file_name="app/data/trace_words_animals.json"
    elif word_category=='Numbers':
        file_name="app/data/trace_words_numbers.json"
    else:
        file_name="app/data/trace_words_numbers.json"
   
# words_input = st.text_area("Enter words (one per line)", placeholder="e.g.\ncat\ndog\ntree")

st.write(file_name)
@st.cache_data
def load_words():
        with open(file_name, "r") as f:   
            return json.load(f)


        

words_all = load_words()
st.write(words_all)

# Pick 8 random words without repetition
words_to_trace = random.sample(words_all, 6)
st.write(words_to_trace)


# Font setup (you must provide a dotted tracing font)
FONT_PATH = "app/font/KGPrimaryDots.ttf"  # Change if you use a different path or font
if os.path.exists(FONT_PATH):
    pdfmetrics.registerFont(TTFont("Dotted", FONT_PATH))
    font_name = "Dotted"
else:
    font_name = "Helvetica"
    st.warning("⚠️ Dotted font not found — using default font instead.")

# Generate PDF
if st.button("Generate Tracing Worksheet"):
    # words = [line.strip() for line in words_input.split("\n") if line.strip()]
    words=words_to_trace
    if not words:
        st.error("Please enter at least one word.")
    else:
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        top = height - 45
        y = top
        line_height = 6080
        width, height = letter

        margin = 0.75 * inch
        line_spacing = 1.2 * inch
        word_font_size = 40
        guideline_width = width - 2 * margin

        # Starting vertical position
        y = height - margin

        # Title
        title = f"{child_name}'s Tracing Worksheet" if child_name else "Word Tracing Worksheet"
        c.setFont(font_name, 48)
        c.drawCentredString(width / 2, y, title)
        y -= 20

        c.setFont(font_name, 36)  # Large trace font

        for word in words:
            y -= line_spacing

            # Draw the word 5 times with spacing
            c.setFont(font_name, word_font_size)
            word_spacing = 1.5 * inch
            
            if len(word) > 5:
                word_count =3
                for i in range(word_count):
                    x = margin + i * word_spacing*1.5
                    c.drawString(x, y, word)
            else: 
                word_count =5

                for i in range(word_count):
                    x = margin + i * word_spacing
                    c.drawString(x, y, word)

            # Draw 3 notebook-style guidelines under each word line
            guideline_offsets = [y - 15, y - 30, y - 45]  # top, middle (dashed), bottom

            for i, offset in enumerate(guideline_offsets):
                c.setStrokeColor(colors.grey)
                if i == 1:
                    c.setDash(1, 2)  # dashed middle line
                else:
                    c.setDash()  # solid lines
                c.line(margin, offset, width - margin, offset)

        c.save()
        buffer.seek(0)

        st.success("✅ Worksheet ready!")
        st.download_button(
            label="📥 Download PDF",
            data=buffer,
            file_name="tracing_worksheet.pdf",
            mime="application/pdf"
        )
    