import streamlit as st
import os
import random
import math
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader


# -----------------------------
# Page config
# -----------------------------
st.set_page_config(layout="wide")
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("""
    <h3 style='color: #ff66a3;'>🎨 Welcome to the Coloring Page Creator! 🖍️</h3>
    Create adorable and printable coloring pages for <b>kids</b>.

    - 🐾 Browse cute animals and fun scenes  
    - 🎨 Let kids color, relax, and be creative  
    - 🖨️ Create a printable PDF instantly  

    Perfect for <b>creative time at home, school, or playdates</b>!
    """, unsafe_allow_html=True)

with col2:
    # Change this to any image you want for the intro
    st.image("app/data/color_pic/Animals/lion.png")
    st.write(' Note: All images are AI generated.')

# -----------------------------
# Load all images
# -----------------------------

with col1:
    categories=['Animals','Vehicles','Princess','Landscapes']
    selected_category = st.selectbox(
    "📂 Choose a category:",
    categories,
    index=0
    )
DATA_FOLDER = "app/data/color_pic/"+selected_category
animal_files = {
    f.replace(os.path.splitext(f)[1], ""): os.path.join(DATA_FOLDER, f)
    for f in os.listdir(DATA_FOLDER)
    if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
}
animal_items = sorted(animal_files.items())  # [(name, path)]

# st.title("Animal Coloring Page Generator")
# st.write("Browse animals and create printable coloring pages (styled like your tracing worksheet).")

# Child name (optional)
child_name=''
# child_name = st.text_input("Child's name (optional)", "")

# -----------------------------
# Session state for navigation
# -----------------------------
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0

total = len(animal_items)

if total == 0:
    st.error("No images found in app/data/color_pic")
    st.stop()

animal_name, img_path = animal_items[st.session_state.current_idx]


# -----------------------------
# Helper: draw flowers (PDF)
# -----------------------------
def draw_flowers_pdf(c, center_y, page_width):
    flower_spacing = 70
    flower_radius = 10
    center_x0 = page_width / 2

    for i in range(5):
        cx = (center_x0 - (flower_spacing * 2)) + (i * flower_spacing)

        # petals
        c.setFillColorRGB(1, 0.6, 0.8)  # pink
        for angle in [0, 72, 144, 216, 288]:
            rad = math.radians(angle)
            px = cx + flower_radius * 1.5 * math.cos(rad)
            py = center_y + flower_radius * 1.5 * math.sin(rad)
            c.circle(px, py, flower_radius, fill=1, stroke=0)

        # center
        c.setFillColorRGB(1, 1, 0)  # yellow
        c.circle(cx, center_y, flower_radius, fill=1, stroke=0)


# -----------------------------
# IMAGE VIEWER (with styling)
# -----------------------------
with st.container():
    st.markdown(
        f"""
        <div style="
            background: #fff7fb;
            border: 2px solid #ffd1e8;
            padding: 18px;
            border-radius: 18px;
            text-align: center;
        ">
            <div style="font-size: 28px; font-weight: 800; color: #ff66a3;">
                {child_name + "'s " if child_name else ""}Coloring Page
            </div>
              <!--
        <div style="margin-top:6px; font-size: 18px; font-weight: 700; color: #333;">
            {animal_name.replace('_',' ').title()}
        </div>
        -->
            <div style="margin-top:6px;">🌸 🌸 🌸 🌸 🌸</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 2, 1])


    with center:
        st.image(img_path, width=420)
        


    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅️ Previous") and st.session_state.current_idx > 0:
            st.session_state.current_idx -= 1
            st.rerun()

    with col3:
        if st.button("Next ➡️") and st.session_state.current_idx < total - 1:
            st.session_state.current_idx += 1
            st.rerun()

    # -----------------------------
    # Create single-page PDF
    # -----------------------------
    with col2:
        if st.button("📄 Create PDF for this picture"):
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter
            margin = 0.75 * inch

            # Title (pink)
            y = height - margin
            title = f"{child_name}'s Coloring Page" if child_name else "Coloring Page"
            c.setFont("Helvetica-Bold", 24)
            c.setFillColorRGB(1, 0.4, 0.7)  # pink
            c.drawCentredString(width / 2, y, title)

            # Flowers
            flower_y = y - 30
            draw_flowers_pdf(c, flower_y, width)

            # Animal name
            c.setFillColorRGB(0, 0, 0)
            c.setFont("Helvetica-Bold", 18)
            # c.drawCentredString(width / 2, y - 60, animal_name.replace("_", " ").title())

            # Name line
            name_y = y - 90
            c.setFont("Helvetica", 14)
            c.drawString(margin, name_y, "Name:")
            
            c.line(margin + 45, name_y - 2, width - margin, name_y - 2)
            name_y = y - 140
            c.drawString(margin, name_y, "What do you see:")
            c.line(margin + 120, name_y - 2, width - margin, name_y - 2)

            # Image placement
            img_reader = ImageReader(img_path)
            img_w, img_h = img_reader.getSize()

            top = name_y - 40
            bottom = 0.9 * inch
            max_h = top - bottom
            max_w = width - 2 * margin

            scale = min(max_w / img_w, max_h / img_h)
            new_w = img_w * scale
            new_h = img_h * scale

            x = (width - new_w) / 2
            y_img = bottom + (max_h - new_h) / 2

            c.drawImage(img_reader, x, y_img, width=new_w, height=new_h, preserveAspectRatio=True)

            # Footer
            c.setFont("Helvetica-Bold", 18)
            c.setFillColorRGB(0.2, 0.6, 0.2)  # green
            c.drawCentredString(width / 2, 0.6 * inch, "🌟 Great job, you did it! 🌟")

            c.showPage()
            c.save()
            buffer.seek(0)
            st.success("✅ Coloring page ready!")
            st.download_button(
                label="📥 Download Coloring Page PDF",
                data=buffer,
                file_name=f"{animal_name}_coloring_page.pdf",
                mime="application/pdf",
            )


# # -----------------------------
# # MULTI-PAGE RANDOM PDF
# # -----------------------------
# st.subheader("📘 Create Random Multi-Page Coloring Book")

# selected_animals = st.multiselect(
#     "Choose animals to include:",
#     [name for name, _ in animal_items],
#     default=[name for name, _ in animal_items][:3],
# )

# num_pages = st.number_input("How many pages?", min_value=1, max_value=50, value=10)

# if st.button("Generate Coloring Book PDF"):
#     if not selected_animals:
#         st.error("Please select at least one animal.")
#     else:
#         buffer = BytesIO()
#         c = canvas.Canvas(buffer, pagesize=letter)
#         width, height = letter
#         margin = 0.75 * inch

#         for _ in range(num_pages):
#             animal = random.choice(selected_animals)
#             img_path = animal_files[animal]

#             # Title
#             y = height - margin
#             title = f"{child_name}'s Coloring Page" if child_name else "Coloring Page"
#             c.setFont("Helvetica-Bold", 24)
#             c.setFillColorRGB(1, 0.4, 0.7)
#             c.drawCentredString(width / 2, y, title)

#             # Flowers
#             draw_flowers_pdf(c, y - 30, width)

#             # Animal name
#             # c.setFillColorRGB(0, 0, 0)
#             # c.setFont("Helvetica-Bold", 18)
#             # c.drawCentredString(width / 2, y - 60, animal.replace("_", " ").title())

#             # Name line
#             name_y = y - 90
#             c.setFont("Helvetica", 14)
#             # c.drawString(margin, name_y, "Name:")
#             # c.line(margin + 45, name_y - 2, width - margin, name_y - 2)

#             # Image placement
#             img_reader = ImageReader(img_path)
#             img_w, img_h = img_reader.getSize()

#             top = name_y - 40
#             bottom = 0.9 * inch
#             max_h = top - bottom
#             max_w = width - 2 * margin

#             scale = min(max_w / img_w, max_h / img_h)
#             new_w = img_w * scale
#             new_h = img_h * scale

#             x = (width - new_w) / 2
#             y_img = bottom + (max_h - new_h) / 2

#             c.drawImage(img_reader, x, y_img, width=new_w, height=new_h)

#             # Footer
#             c.setFont("Helvetica-Bold", 18)
#             c.setFillColorRGB(0.2, 0.6, 0.2)
#             c.drawCentredString(width / 2, 0.6 * inch, "🌟 Great job, you did it! 🌟")

#             c.showPage()

#         c.save()
#         buffer.seek(0)

#         st.success("✅ Multi-page coloring book created!")
#         st.download_button(
#             label="📥 Download Coloring Book PDF",
#             data=buffer,
#             file_name="animal_coloring_book.pdf",
#             mime="application/pdf",
#         )
