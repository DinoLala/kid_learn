import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd
# from app.common.search import process_html, get_player,get_tournaments,get_norm_summary,get_norm
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import random
from datetime import datetime

#Data Source
# import yfinance as yf

#Data viz
import plotly.graph_objs as go
import requests

st.set_page_config(layout="wide")

st.header(":orange[Math worksheet!]")

st.header('')
            
import os




col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("Enter your name")    
    output_form=st.selectbox("Worksheet form", [ 'Column','Row']) 
    operations = st.multiselect("Please select operation", ['+','-','×','÷'])
    if operations== []:
        operations=['+']
with col2:
    min_number=st.number_input('Min (0-999)',min_value=0, max_value=999,value=0 )
    max_number=st.number_input('max (0-999)',min_value=0, max_value=999,value=99 )
    # counts=st.number_input('Number of operation',min_value=0, max_value=99, )
with col3:
    in_order=st.selectbox("Put numbers in order", [True, False]) 
    easy_level=st.selectbox("Make it easy",  [True, False]) 


    
submited=st.button('Generate worksheet')
#Interval required 5 minutes
def get_easy(a,b,op):
    a1 = a % 10
    b1 = b % 10
    max_ab1=max(a1,b1)
    if  op =='-' and a1<b1:
        a, b = a+b1, b+a1
    
    elif op =='+' and a1+ b1>=10:
        if a1>=5:
            a=a-5
        if b1>=5:
            b=b-5
    return a, b
    
def generate_math_problems_row_form(input_dict):
    count=input_dict['count']
    min_number=input_dict['min_number']
    max_number=input_dict['max_number']
    # st.write(max_number)
    operations=input_dict['operations']
    order=input_dict['order']
    easy_level=input_dict['easy_level']
    problems = []
    for _ in range(count):
        op = random.choice(operations)
        a = random.randint(min_number, max_number)
        b = random.randint(min_number, max_number)
        if order==True and b > a:
            a, b = b, a
        if op == '-' and b > a:
            a, b = b, a
        elif op == '÷':
            b = random.randint(2, 20)
            a = b * random.randint(2, 20)  # ensure divisible

        if easy_level ==True:
            a,b=get_easy(a,b,op)
            
        if op == '+':
            problems.append(f"{a} + {b} = _______")
        elif op == '-':
            problems.append(f"{a} - {b} = _______")
        elif op == '×':
            problems.append(f"{a} × {b} = _______")
        elif op == '÷':
            a, b = a * b, b  # ensure a is divisible
            problems.append(f"{a} ÷ {b} = _______")
    return problems

def create_worksheet_row_form(problems, input_dict):
    title=input_dict['title']
    filename=input_dict['filename']
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 40, title)
    c.setFont("Helvetica", 12)
    today = datetime.today().strftime("%B %d, %Y")
   
    c.drawString(50, height - 70, f"Date: {today}")

    margin_left = 50
    margin_top = 120
    column_width = (width - 2 * margin_left) / 3
    row_height = 60
    start_y = height - margin_top

    for row in range(10):
        y = start_y - row * row_height
        for col in range(3):
            idx = row * 3 + col
            if idx >= len(problems):
                break
            x = margin_left + col * column_width
            # c.drawString(x, y, f"{idx+1}. {problems[idx]}")
            c.drawString(x, y, f" {problems[idx]}")

    c.save()
    print(f"Saved: {filename}")
def generate_problems_col_form(input_dict):

    count=input_dict['count']
    min_number=input_dict['min_number']
    max_number=input_dict['max_number']
    operations=input_dict['operations']
    order=input_dict['order']
    easy_level=input_dict['easy_level']
    
    problems = []
    for _ in range(count):
        op = random.choice(operations)
        a = random.randint(min_number, max_number)
        b = random.randint(min_number, max_number)
        if order==True and b > a:
            a, b = b, a
        if op == '-' and b > a:
            a, b = b, a
        elif op == '÷':
            b = random.randint(2, 20)
            a = b * random.randint(2, 20)  # ensure divisible

        if easy_level ==True:
            a,b=get_easy(a,b,op)
            
        problems.append((a, op, b))
    return problems
    


def create_math_worksheet_col_form(problems,input_dict):
    title=input_dict['title']
    filename=input_dict['filename']
    
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    # Get today's date
    today = datetime.today().strftime("%B %d, %Y")
    c.drawCentredString(width / 2, height - 40, title)
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, f"Date: {today}")

    # Layout config
    margin_x = 30
    margin_top = 120
    col_width = (width - 2 * margin_x) / 4
    row_height = 125 # room for 2 lines with spacing

    c.setFont("Helvetica", 14)

    for i, (a, op, b) in enumerate(problems):
        col = i % 4
        row = i // 4

        x = margin_x + col * col_width
        y = height - margin_top - row * row_height

        # First number, right-aligned
        c.drawRightString(x + 90, y, f"{a}")
        # Second number, with operator to the left
        c.drawString(x + 10, y - 20, op)
        c.drawRightString(x + 90, y - 20, f"{b}")
        # Answer line
        c.line(x + 10, y - 45, x + 100, y - 45)

    c.save()
    print(f"Worksheet saved as '{filename}'")

if submited:
    st.write(f":orange[Hello {name} ! here is you worksheet to download]" )

    dir=r'app/data/'

    if output_form =='Row':
        filename=dir+'worksheet_row_form.pdf'

        input_dict={'title':f"{name}'s Math Worksheet"
                    ,'filename':filename
                    ,'count': 32
                ,'order': in_order
                ,'easy_level': easy_level
                ,'operations': operations
                ,'min_number': int(min_number)
                ,'max_number': int(max_number)
                }
        # ,'operations': ['+', '-', '×', '÷']
        st.write(input_dict)
        problems = generate_math_problems_row_form(input_dict) 
        create_worksheet_row_form(problems,input_dict)
    if output_form =='Column':
        filename=dir+f'worksheet_col_form.pdf'

        input_dict={'title':f"{name}'s Math Worksheet"
                    ,'filename':filename
                    ,'count': 20
                ,'order': in_order
                ,'easy_level': easy_level
                ,'operations': operations
                ,'min_number': int(min_number)
                ,'max_number': int(max_number)
                }
        # ,'operations': ['+', '-', '×', '÷']
        st.write(input_dict)
        problems = generate_problems_col_form(input_dict) 

        create_math_worksheet_col_form(problems,input_dict)
    
    st.write(f'Worksheet saved as: {filename}')
    # Path to your PDF file
    pdf_path = filename

    # Open the PDF file in binary mode
    with open(pdf_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()

    # Show a download button
    st.download_button(
        label="📥 Download Worksheet PDF",
        data=pdf_bytes,
        file_name=f"{name}_worksheet.pdf",
        mime="application/pdf"
    )

 