import os
import random
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import streamlit as st

# Page config
st.set_page_config(layout="wide")
st.markdown("""
<h3 style='color: orange;'>🧠 Welcome to the Math Worksheet Maker! ✏️</h3>
Create fun and custom math practice worksheets for <b>K–2 kids</b>.

- ✅ Enter your child’s name  
- ➕ Choose the math operations (add, subtract, multiply, divide)  
- 🖨️ Generate printable worksheets instantly  

Perfect for learning at <b>home or in the classroom</b>!
""", unsafe_allow_html=True)


# Input UI
col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("Enter your name")
    output_form = st.selectbox("Worksheet form", ['Column', 'Row'])
    operations = st.multiselect("Please select operation", ['+', '-', '×']) or ['+'] #, '÷'

with col2:
    min_number = st.number_input('Min (0-999)', min_value=0, max_value=999, value=0)
    max_number = st.number_input('Max (0-999)', min_value=0, max_value=999, value=99)

with col3:
    in_order = st.selectbox("Put numbers in order", [True, False])
    easy_level = st.selectbox("Make it easy", [True, False])

submited = st.button('Generate worksheet')

def get_easy(a, b, op):
    a1, b1 = a % 10, b % 10
    if op == '-' and a1 < b1:
        a, b = a + b1, b + a1
    elif op == '+' and a1 + b1 >= 10:
        if a1 >= 5:
            a -= 5
        if b1 >= 5:
            b -= 5
    return a, b

def generate_math_problems_row_form(input_dict):
    problems = []
    for _ in range(input_dict['count']):
        op = random.choice(input_dict['operations'])
        a = random.randint(input_dict['min_number'], input_dict['max_number'])
        b = random.randint(input_dict['min_number'], input_dict['max_number'])

        if input_dict['order'] and b > a:
            a, b = b, a
        if op == '-' and b > a:
            a, b = b, a
        elif op == '÷':
            b = random.randint(2, 20)
            a = b * random.randint(2, 20)

        if input_dict['easy_level']:
            a, b = get_easy(a, b, op)

        problems.append(f"{a} {op} {b} = _______")
    return problems

def create_worksheet_row_form(problems, input_dict):
    c = canvas.Canvas(input_dict['filename'], pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 40, input_dict['title'])
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, f"Date: {datetime.today().strftime('%B %d, %Y')}")

    margin_left, margin_top = 50, 120
    column_width = (width - 2 * margin_left) / 3
    row_height = 60
    start_y = height - margin_top

    for row in range(10):
        y = start_y - row * row_height
        for col in range(3):
            idx = row * 3 + col
            if idx < len(problems):
                x = margin_left + col * column_width
                c.drawString(x, y, problems[idx])

    c.save()

def generate_problems_col_form(input_dict):
    problems = []
    for _ in range(input_dict['count']):
        op = random.choice(input_dict['operations'])
        a = random.randint(input_dict['min_number'], input_dict['max_number'])
        b = random.randint(input_dict['min_number'], input_dict['max_number'])

        if input_dict['order'] and b > a:
            a, b = b, a
        if op == '-' and b > a:
            a, b = b, a
        elif op == '÷':
            b = random.randint(2, 20)
            a = b * random.randint(2, 20)

        if input_dict['easy_level']:
            a, b = get_easy(a, b, op)

        problems.append((a, op, b))
    return problems

def create_math_worksheet_col_form(problems, input_dict):
    c = canvas.Canvas(input_dict['filename'], pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 40, input_dict['title'])
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, f"Date: {datetime.today().strftime('%B %d, %Y')}")

    margin_x, margin_top = 30, 120
    col_width = (width - 2 * margin_x) / 4
    row_height = 125
    c.setFont("Helvetica", 14)

    for i, (a, op, b) in enumerate(problems):
        col = i % 4
        row = i // 4
        x = margin_x + col * col_width
        y = height - margin_top - row * row_height

        c.drawRightString(x + 90, y, f"{a}")
        c.drawString(x + 10, y - 20, op)
        c.drawRightString(x + 90, y - 20, f"{b}")
        c.line(x + 10, y - 45, x + 100, y - 45)

    c.save()

if submited:
    st.write(f":orange[Hello {name} ! Here is your worksheet to download:]")

    dir = 'worksheet_output/'
    os.makedirs(dir, exist_ok=True)

    filename = os.path.join(dir, f"worksheet_{output_form.lower()}_form.pdf")
    input_dict = {
        'title': f"{name}'s Math Worksheet",
        'filename': filename,
        'count': 32 if output_form == 'Row' else 20,
        'order': in_order,
        'easy_level': easy_level,
        'operations': operations,
        'min_number': int(min_number),
        'max_number': int(max_number)
    }

    if output_form == 'Row':
        problems = generate_math_problems_row_form(input_dict)
        create_worksheet_row_form(problems, input_dict)
    else:
        problems = generate_problems_col_form(input_dict)
        create_math_worksheet_col_form(problems, input_dict)

    with open(filename, "rb") as pdf_file:
        st.download_button(
            label="📥 Download Worksheet PDF",
            data=pdf_file.read(),
            file_name=f"{name}_worksheet.pdf",
            mime="application/pdf"
        )
