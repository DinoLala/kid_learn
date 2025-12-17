
import os
import random
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import streamlit as st

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

def create_worksheet_row_form(input_dict,worksheet_number):

    c = canvas.Canvas(input_dict['filename'], pagesize=letter)
    width, height = letter


    margin_left, margin_top = 50, 120
    column_width = (width - 2 * margin_left) / 3
    row_height = 60
    start_y = height - margin_top
    for _ in range(worksheet_number):
        problems=generate_math_problems_row_form(input_dict)
                    # Title
        title = input_dict['title']
        # c.setFont(font_name, 48)
        c.setFont("Helvetica-Bold", 24)
        c.setFillColorRGB(0.2, 0.6, 0.2)
        c.drawCentredString(width / 2, height - 40, title)
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 70, f"Date: {datetime.today().strftime('%B %d, %Y')}")
        c.setFillColorRGB(0,0,0)
        for row in range(10):
            y = start_y - row * row_height
            for col in range(3):
                idx = row * 3 + col
                if idx < len(problems):
                    x = margin_left + col * column_width
                    c.drawString(x, y, problems[idx])
        # After drawing all tracing rows
        c.setFont("Helvetica-Bold", 24)
        c.setFillColorRGB(0.2, 0.6, 0.2)  # a nice green color
        c.drawCentredString(width / 2, 40, "🌟 Great job, you did it! 🌟")
        c.showPage()

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

def create_math_worksheet_col_form( input_dict,worksheet_number):
    problems=generate_problems_col_form(input_dict)
    c = canvas.Canvas(input_dict['filename'], pagesize=letter)

    width, height = letter
    for _ in range(worksheet_number):
        problems=generate_problems_col_form(input_dict)

        title = input_dict['title']
        c.setFillColorRGB(0.2, 0.6, 0.2)
        # c.setFont(font_name, 48)
        c.setFont("Helvetica-Bold", 24)
        # c.drawCentredString(width / 2, y, title)
        c.drawCentredString(width / 2, height - 40, title)
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 70, f"Date: {datetime.today().strftime('%B %d, %Y')}")
        c.setFillColorRGB(0, 0, 0)
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
        # After drawing all tracing rows
        c.setFont("Helvetica-Bold", 24)
        c.setFillColorRGB(0.2, 0.6, 0.2)  # a nice green color
        c.drawCentredString(width / 2, 40, "🌟 Great job, you did it! 🌟")
        c.showPage()

    c.save()
