import os
import random
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from functions import *

import streamlit as st

# Page config
st.set_page_config(layout="wide")
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("""
    <h3 style='color: orange;'>🧠 Welcome to the Math Worksheet Maker! ✏️</h3>
    Create fun and custom math practice worksheets for <b>K–2 kids</b>.

    - ✅ Enter your child’s name  
    - ➕ Choose the math operations (add, subtract, multiply, divide)  
    - 🖨️ Generate printable worksheets instantly  

    Perfect for learning at <b>home or in the classroom</b>!
    """, unsafe_allow_html=True)
with col2:
    # st.image("app/data/happy-dance-excited.gif")
    st.image("app/data/math.png")
# Input UI

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
col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("Enter your name")
    output_form = st.selectbox("Worksheet form", ['Column', 'Row'])
    operations = st.multiselect("Please select operation", ['+', '-', '×']) or ['+'] #, '÷'
    worksheet_number = st.number_input('Worksheet pages', min_value=0, max_value=50, value=1)

with col2:
    min_number = st.number_input('Min (0-999)', min_value=0, max_value=999, value=0)
    max_number = st.number_input('Max (0-999)', min_value=0, max_value=999, value=99)

with col3:
    in_order = st.selectbox("Put numbers in order", [True, False])
    easy_level = st.selectbox("Make it easy", [True, False])

submited = st.button('Generate Maths Worksheet')

if submited:
    

    dir = 'worksheet_output/'
    os.makedirs(dir, exist_ok=True)

    filename = os.path.join(dir, f"worksheet_{output_form.lower()}_form.pdf")
    
    if name =='':
        title= 'Maths Worksheet'
    else:
        title= f"{name}'s Maths Worksheet"

    input_dict = {
        'title': title,
        'filename': filename,
        'count': 32 if output_form == 'Row' else 20,
        'order': in_order,
        'easy_level': easy_level,
        'operations': operations,
        'min_number': int(min_number),
        'max_number': int(max_number)
    }
    if int(max_number) < int(min_number):
        st.write(':orange[Ensure that min < max for valid input.]')
    else:
        
        if output_form == 'Row':
            create_worksheet_row_form( input_dict,worksheet_number)
        else:
            create_math_worksheet_col_form( input_dict,worksheet_number)

       
        # st.write(f":orange[Hello {name} ! Here is your worksheet to download:]")
        
        st.success("✅ Worksheet ready!")
        with open(filename, "rb") as pdf_file:
            st.download_button(
                label="📥 Download Worksheet PDF",
                data=pdf_file.read(),
                file_name=f"{name}_worksheet.pdf",
                mime="application/pdf"
            )
