import os
import random
from datetime import datetime
from fractions import Fraction
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import streamlit as st

# Page setup
st.set_page_config(page_title="Pre-Algebra Equations Worksheet", layout="centered")
st.markdown("""
<h3 style='color: orange;'>📐 Pre-Algebra Equations Worksheet Generator</h3>
Practice solving **one-variable equations** like `x + 3 = 8` with this printable worksheet.

- ✏️ Custom equations for early algebra learners  
- 🖨️ Space to write answers  
- 📄 Generate multiple pages instantly  
""", unsafe_allow_html=True)

# Input controls
col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("Student's Name (optional)")
    page_count = st.number_input("Number of pages", min_value=1, max_value=10, value=1)
with col2:
    min_val = st.number_input("Min value", min_value=-100, max_value=100, value=1)
    max_val = st.number_input("Max value", min_value=-100, max_value=100, value=20)
with col3:
    topic = st.selectbox("topic", ['One side Euqation'])
    difficult_level = st.selectbox("Level", ['Level 1', 'Level 2', 'Level 3'])

generate = st.button("Generate Worksheet")

def random_number(use_fractions=True):
    if use_fractions:
        numerator = random.randint(min_val, max_val)
        denominator = random.randint(2, 10)
        # Avoid zero denominator or zero numerator for prettier fractions
        if denominator == 0:
            denominator = 1
        if numerator == 0:
            numerator = 1
        return Fraction(numerator, denominator)
    else:
        return random.randint(min_val, max_val)

# Equation generator
def generate_equation(min_val, max_val, difficult_level):
    ops = ['+', '-']
    op = random.choice(ops)

    
    use_fractions=False
    if difficult_level == "Level 1":
        a = Fraction(1,1)
    else:
        if difficult_level=='Level 3':
            use_fractions=True
        a = random_number(use_fractions)

    # a = random_number(use_fractions)
    b = random_number(use_fractions)
    x = random_number(use_fractions)

    # Calculate result: ax + b
    result = a * x + b

    # Format parts as strings
    def frac_to_str(frac):
        if frac.denominator == 1:
            return str(frac.numerator)
        else:
            return f"{frac.numerator}/{frac.denominator}"

    a_str = "" if a == 1 else f"{frac_to_str(a)}"
    # st.write(a_str)
    b_str = frac_to_str(b)
    # st.write(b_str)
    result_str = frac_to_str(result)
    op_str = op

    # Construct equation string:
    # If a==1, omit coefficient
    if a == 1:
        eq = f"x {op_str} {b_str} = {result_str}"
    else:
        eq = f"{a_str} x {op_str} {b_str} = {result_str}"

    return eq

def draw_fraction(c, x, y, frac, font_size=14):
    """Draw vertical fraction at (x, y) on canvas c."""
    c.setFont("Helvetica", font_size)
    width = max(
        c.stringWidth(str(frac.numerator), "Helvetica", font_size),
        c.stringWidth(str(frac.denominator), "Helvetica", font_size)
    ) + 10
    # Draw numerator (above line)
    c.drawCentredString(x + width / 2, y + 8, str(frac.numerator))
    # Draw denominator (below line)
    c.drawCentredString(x + width / 2, y - 10, str(frac.denominator))
    # Draw fraction bar
    c.line(x, y, x + width, y)

    return width + 8  # return width plus spacing

def draw_equation(c, x, y, eq_str, font_size=12):
    """Draw equation with fractions rendered vertically on canvas c at (x,y)."""
    c.setFont("Helvetica", font_size)
    parts = eq_str.split()
    cursor_x = x

    for part in parts:
        try:
            # Check if part is a fraction (e.g., "11/3")
            if '/' in part:
                frac = Fraction(part)
                shift = draw_fraction(c, cursor_x, y, frac, font_size)
                cursor_x += shift
            else:
                c.drawString(cursor_x, y, part)
                cursor_x += c.stringWidth(part, "Helvetica", font_size) + 8
        except Exception:
            # If Fraction conversion fails, just draw normally
            c.drawString(cursor_x, y, part)
            cursor_x += c.stringWidth(part, "Helvetica", font_size) + 8

# Create PDF
def create_equation_worksheet(input_dict):
    from io import BytesIO
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    for page in range(input_dict['pages']):
        # Title and metadata
        c.setFont("Helvetica-Bold", 20)
        title = f"{input_dict['name']}'s Pre-Algebra Worksheet" if input_dict['name'] else "Pre-Algebra Worksheet"
        c.drawCentredString(width / 2, height - 40, title)
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 70, f"Date: {datetime.today().strftime('%B %d, %Y')}")

        # Equations
        c.setFont("Helvetica", 14)
        y_start = height - 100
        spacing = 120

        for i in range(5):
            eq = generate_equation(input_dict['min'], input_dict['max'], input_dict['difficult_level'])
            y = y_start - i * spacing
            c.drawString(50, y, f"{i+1}.")  # Draw problem number
            st.write(eq)
            draw_equation(c, 80, y, eq)     # Draw formatted equation with fractions
            c.drawString(250, y, "Answer: x= ")
            c.line(310, y - 5, 450, y - 5)

        # Footer
        c.setFont("Helvetica-Bold", 18)
        c.setFillColorRGB(0.2, 0.6, 0.2)
        c.drawCentredString(width / 2, 40, "🌟 Keep going, you're doing great! 🌟")

        c.showPage()

    c.save()
    buffer.seek(0)
    return buffer

# Generate and download
if generate:
    input_dict = {
        'name': name,
        'pages': page_count,
        'min': int(min_val),
        'max': int(max_val),
        'difficult_level': difficult_level
    }
    pdf = create_equation_worksheet(input_dict)
    st.success("✅ Worksheet ready!")
    st.download_button(
        label="📥 Download Pre-Algebra PDF",
        data=pdf,
        file_name=f"{name or 'pre_algebra'}_worksheet.pdf",
        mime="application/pdf"
    )
