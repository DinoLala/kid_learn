import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
import os
import math
import json
import random
# st.set_page_config(page_title="Word Tracing Worksheet", layout="centered")
st.set_page_config(page_title="Word Tracing Worksheet",layout="wide")
col1, col2 = st.columns([3, 2])

# Page setup
with col1:

    st.markdown("""
    <h3 style='color: orange;'>✏️ Word Tracing Worksheet Generator</h3>

    Welcome to a fun and easy way to help little learners practice writing! 💖  
    - Choose from exciting word categories like **Animals**, **Common words**, or **Numbers**, and we’ll create a magical tracing worksheet just for you.  

    - Perfect for preschoolers and early learners to build confidence, one dotted letter at a time!  
    Ready, set, trace! 🌟📄🖍️
    """, unsafe_allow_html=True)
    st.markdown("- Create a ** 🖨️printable worksheet** with traceable dotted words – great for early writers!")
with col2:
    # st.write('Sample output')
    st.image('./app/data/trace1.png')



st.html(
    """
    <style>
    hr.thick-line {
        border: none;
        height: 3px; /* Adjust the height for thickness */
        background-color: #FFA500   ; /* Adjust the color (e.g., black or hex code) */
        margin-top: 20px; /* Adjust top margin for spacing */
        margin-bottom: 20px; /* Adjust bottom margin for spacing */
    }
    </style>
    <hr class="thick-line" />
    """
)
# Input
col1, col2= st.columns(2)
with col1:
    child_name = st.text_input("Child's Name (optional):")
    word_category= st.selectbox("Category", ['School words', 'Common words', 'Animals', 'Numbers'])
    worksheet_number = st.number_input('Worksheet pages', min_value=0, max_value=50, value=1)
    if word_category =='School words':
        # word_list = st.text_input("input words list from teacher:")
        file_name="app/data/trace_words_from_school.json"
    elif word_category =='Animals':
        file_name="app/data/trace_words_animals.json"
    elif word_category=='Numbers':
        file_name="app/data/trace_words_numbers.json"
    else:
        file_name="app/data/trace_words.json"
with col2:
    st.write('input words list from teacher:(optional))' )
    # st.write('School words - category only')
    word_list = st.text_input("Teacher word list (School words - category only) ")

# with col2:
#     st.write('Sample output')
#     st.image('./app/data/trace.png')


# @st.cache_data
def load_words():
        with open(file_name, "r") as f:   
            return json.load(f)
      
words_all = load_words()
word_list1=[]

if word_category =='School words':
     
    word_list1= word_list.split(',')
    for word in word_list1:
        if word not in words_all and len(word) > 1:   # avoid duplicates
            words_all.append(word)
    print(words_all)
    with open(file_name, "w") as f:
        json.dump(words_all, f, indent=2)

FONT_PATH = "app/font/KGPrimaryDots.ttf"  # Change if you use a different path or font
if os.path.exists(FONT_PATH):
    pdfmetrics.registerFont(TTFont("Dotted", FONT_PATH))
    font_name = "Dotted"
else:
    font_name = "Helvetica"
    st.warning("⚠️ Dotted font not found — using default font instead.")

# Generate PDF
if st.button("Generate Tracing Worksheet"):
    if len(words_all) < 6:
        st.error("Not enough words to create worksheets.")
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

        for _ in range(worksheet_number):
            if word_list1 !=[]:
                words_to_trace = random.sample(word_list1, 6)
            else:
                words_to_trace = random.sample(words_all, 6)

            words = [ c.replace("'",'') for c in words_to_trace]
            words = [ c for c in words if c != '']

            y = height - margin

            # Title
            title = f"{child_name}'s Tracing Worksheet" if child_name else "Tracing Worksheet"
            c.setFillColorRGB(0.2, 0.6, 0.2)
            # c.setFont(font_name, 48)
            c.setFont("Helvetica-Bold", 24)
            c.setFillColorRGB(1, 0.6, 0.8)
            c.drawCentredString(width / 2, y, title)


            # Draw flowers under the title
            flower_y = y - 40
            flower_spacing = 70
            flower_radius = 10

            for i in range(5):
                center_x = (width / 2) - (flower_spacing * 2) + (i * flower_spacing)

                c.setFillColorRGB(1, 0.6, 0.8)
                for angle in [0, 72, 144, 216, 288]:
                    rad = math.radians(angle)
                    petal_x = center_x + flower_radius * 1.5 * math.cos(rad)
                    petal_y = flower_y + flower_radius * 1.5 * math.sin(rad)
                    c.circle(petal_x, petal_y, flower_radius, fill=1)

                c.setFillColorRGB(1, 1, 0)
                c.circle(center_x, flower_y, flower_radius, fill=1)



            c.setFillColorRGB(0, 0, 0)
            y -= 30
            c.setFont(font_name, 36)

            for word in words:
                y -= line_spacing
                c.setFont(font_name, word_font_size)
                word_spacing = 1.5 * inch

                if len(word) > 8:
                    word_count = 2
                    for i in range(word_count):
                        x = margin + i * word_spacing * 1.5
                        c.drawString(x, y, word)
                elif len(word) > 5:
                    word_count = 3
                    for i in range(word_count):
                        x = margin + i * word_spacing * 1.5
                        c.drawString(x, y, word)
                else:
                    word_count = 5
                    for i in range(word_count):
                        x = margin + i * word_spacing
                        c.drawString(x, y, word)

                guideline_offsets = [y - 15, y - 30, y - 45]
                for i, offset in enumerate(guideline_offsets):
                    c.setStrokeColor(colors.grey)
                    if i == 1:
                        c.setDash(1, 2)
                    else:
                        c.setDash()
                    c.line(margin, offset, width - margin, offset)

            c.setFont("Helvetica-Bold", 24)
            c.setFillColorRGB(0.2, 0.6, 0.2)
            c.drawCentredString(width / 2, 40, "🌟 Great job, you did it! 🌟")

            c.showPage()

        c.save()
        buffer.seek(0)

        st.success("✅ Worksheet ready!")
        st.download_button(
            label="📥 Download Worksheet PDF",
            data=buffer,
            file_name="tracing_worksheet.pdf",
            mime="application/pdf"
        )
