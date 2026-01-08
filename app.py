import streamlit as st
from docx import Document
from fpdf import FPDF
from io import BytesIO
import datetime
import re
from PIL import Image
from docx.shared import Inches

# ---------- Page Setup ----------
st.set_page_config(page_title="Premium Resume Builder", page_icon=":briefcase:", layout="wide")
st.title("📄 Premium Resume Builder")
st.write("Create professional resumes with multiple templates and color themes. Upload photo, preview live, and download!")

# ---------- Helper Functions ----------
def sanitize_filename(name):
    return re.sub(r"[^\w\d-]", "_", name)

def bullet_list(text):
    return [f"- {line.strip()}" for line in text.split("\n") if line.strip()]

def resize_image(image, max_size=(150, 150)):
    img = Image.open(image)
    img.thumbnail(max_size)
    return img

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

# ---------- Sidebar Input ----------
st.sidebar.header("Enter Your Details")

# Template & Theme
template_option = st.sidebar.selectbox("Choose Resume Template", ["Classic", "Modern", "Creative"])
color_theme = st.sidebar.selectbox("Choose Color Theme", ["Blue", "Navy", "Green", "Dark Gray"])

# Load sample resume
use_sample = st.sidebar.checkbox("Load Sample Resume")
if use_sample:
    name = "Jane Doe"
    email = "jane.doe@example.com"
    phone = "+234 801 234 5678"
    linkedin = "https://linkedin.com/in/janedoe"
    github = "https://github.com/janedoe"
    summary = "A motivated software engineer with experience in Python, Machine Learning, and Web Development."
    education = "B.Sc Computer Science, XYZ University, 2020"
    experience = "ABC Corp - Software Engineer (2020-2023)\n- Developed a machine learning pipeline\n- Improved app performance by 30%"
    skills = "Python, Machine Learning, Streamlit, Data Analysis"
    projects = "Resume Builder Project - Built a professional resume builder with Python and Streamlit"
else:
    name = st.sidebar.text_input("Full Name", placeholder="John Doe")
    email = st.sidebar.text_input("Email", placeholder="john@example.com")
    phone = st.sidebar.text_input("Phone Number", placeholder="+234 801 234 5678")
    linkedin = st.sidebar.text_input("LinkedIn (optional)", placeholder="https://linkedin.com/in/username")
    github = st.sidebar.text_input("GitHub (optional)", placeholder="https://github.com/username")
    summary = st.sidebar.text_area("Professional Summary", placeholder="Brief introduction about yourself", height=100)
    education = st.sidebar.text_area("Education", placeholder="B.Sc Computer Science, XYZ University, 2020")
    experience = st.sidebar.text_area("Work Experience", placeholder="Company - Role (Year-Year)\n- Achievement 1\n- Achievement 2")
    skills = st.sidebar.text_input("Skills (comma separated)", placeholder="Python, Data Analysis, Machine Learning")
    projects = st.sidebar.text_area("Projects", placeholder="Project Name - Description\n- Key achievement 1\n- Key achievement 2")

# Profile Photo
photo = st.sidebar.file_uploader("Upload Profile Photo (optional)", type=["jpg","png"])

# Preview & Generate
preview = st.sidebar.checkbox("Preview Resume")
submitted = st.sidebar.button("Generate Resume")

# ---------- Color Map ----------
color_map_hex = {
    "Blue": "#0066CC",
    "Navy": "#000066",
    "Green": "#009900",
    "Dark Gray": "#323232"
}
theme_color_hex = color_map_hex.get(color_theme, "#0066CC")
theme_color_rgb = {
    "Blue": (0,102,204),
    "Navy": (0,0,102),
    "Green": (0,153,0),
    "Dark Gray": (50,50,50)
}.get(color_theme, (0,102,204))

# ---------- Resume Preview with Live Theme ----------
if preview:
    st.subheader("📄 Resume Preview")

    st.markdown(f"<h2 style='color:{theme_color_hex};'>{name}</h2>", unsafe_allow_html=True)
    st.markdown(f"**Email:** {email} | **Phone:** {phone} | **LinkedIn:** {linkedin} | **GitHub:** {github}")

    if summary:
        st.markdown(f"<h4 style='color:{theme_color_hex};'>Profile Summary</h4>", unsafe_allow_html=True)
        st.markdown(summary)

    if education:
        st.markdown(f"<h4 style='color:{theme_color_hex};'>Education</h4>", unsafe_allow_html=True)
        for line in bullet_list(education):
            st.markdown(f"- {line}")

    if experience:
        st.markdown(f"<h4 style='color:{theme_color_hex};'>Work Experience</h4>", unsafe_allow_html=True)
        for line in bullet_list(experience):
            st.markdown(f"- {line}")

    if skills:
        st.markdown(f"<h4 style='color:{theme_color_hex};'>Skills</h4>", unsafe_allow_html=True)
        st.markdown(", ".join([s.strip() for s in skills.split(",")]))

    if projects:
        st.markdown(f"<h4 style='color:{theme_color_hex};'>Projects</h4>", unsafe_allow_html=True)
        for line in bullet_list(projects):
            st.markdown(f"- {line}")

    if photo:
        st.image(photo, width=150)

# ---------- Generate Resume ----------
if submitted:
    if not name or not email:
        st.error("Please fill at least Name and Email.")
    else:
        st.success("Generating your resume...")

        # ---------- Word Resume ----------
        doc = Document()
        doc.add_heading(name, 0)
        if photo:
            try:
                doc.add_picture(photo, width=Inches(1.5))
            except:
                pass
        if summary:
            doc.add_heading("Profile Summary", level=1)
            doc.add_paragraph(summary)
        doc.add_heading("Contact Information", level=1)
        doc.add_paragraph(f"Email: {email}\nPhone: {phone}\nLinkedIn: {linkedin}\nGitHub: {github}")
        for section_name, content in [("Education", education), ("Work Experience", experience),
                                      ("Skills", skills), ("Projects", projects)]:
            if content:
                doc.add_heading(section_name, level=1)
                if section_name=="Skills":
                    doc.add_paragraph(", ".join([s.strip() for s in skills.split(",")]))
                else:
                    for line in bullet_list(content):
                        doc.add_paragraph(line)
        buffer_docx = BytesIO()
        doc.save(buffer_docx)
        buffer_docx.seek(0)
        st.download_button(
            label="Download Word Resume (.docx)",
            data=buffer_docx,
            file_name=f"{sanitize_filename(name)}_{template_option}_{color_theme}_Resume_{timestamp}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

        # ---------- PDF Resume ----------
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_margins(15, 15, 15)

        # Profile photo
        if photo:
            try:
                img = resize_image(photo)
                img.save("temp_photo.png")
                if template_option in ["Classic", "Modern"]:
                    pdf.image("temp_photo.png", x=160, y=15, w=30)
                else:
                    pdf.image("temp_photo.png", x=10, y=20, w=40)
            except:
                pass

        # Name
        pdf.set_font("Arial",'B',22)
        pdf.set_text_color(30,30,30)
        pdf.cell(0,12,name,ln=True,align="C" if template_option!="Creative" else "L")
        pdf.set_line_width(0.5)
        pdf.line(15,pdf.get_y(),195,pdf.get_y())
        pdf.ln(5)

        # Contact
        pdf.set_font("Arial",'',12)
        pdf.set_text_color(50,50,50)
        pdf.multi_cell(0,7,f"Email: {email}\nPhone: {phone}\nLinkedIn: {linkedin}\nGitHub: {github}")

        # Section heading helper
        def section_heading(title):
            pdf.ln(3)
            pdf.set_font("Arial",'B',14)
            pdf.set_text_color(*theme_color_rgb)
            pdf.cell(0,6,title,ln=True)
            pdf.set_text_color(50,50,50)
            pdf.set_line_width(0.3)
            pdf.line(15,pdf.get_y(),195,pdf.get_y())
            pdf.ln(2)

        # Sections
        if template_option == "Classic":
            for section_name, content in [("Education", education), ("Work Experience", experience),
                                          ("Skills", skills), ("Projects", projects)]:
                if content:
                    section_heading(section_name)
                    pdf.set_font("Arial",'',12)
                    if section_name=="Skills":
                        for s in [x.strip() for x in skills.split(",")]:
                            pdf.cell(5)
                            pdf.cell(0,6,f"- {s}",ln=True)
                    else:
                        for line in bullet_list(content):
                            pdf.cell(5)
                            pdf.multi_cell(0,6,line)

        elif template_option == "Modern":
            left_x = 10
            right_x = 105
            y_start = pdf.get_y()
            if skills:
                pdf.set_xy(left_x,y_start)
                section_heading("Skills")
                pdf.set_font("Arial",'',12)
                for s in [x.strip() for x in skills.split(",")]:
                    pdf.cell(5)
                    pdf.cell(0,6,f"- {s}",ln=True)
            pdf.set_xy(right_x,y_start)
            for section_name, content in [("Education", education), ("Work Experience", experience), ("Projects", projects)]:
                if content:
                    section_heading(section_name)
                    pdf.set_font("Arial",'',12)
                    for line in bullet_list(content):
                        pdf.multi_cell(0,6,line)

        elif template_option == "Creative":
            pdf.set_font("Arial",'B',14)
            pdf.cell(50,8,"Skills & Contact",ln=True)
            pdf.set_font("Arial",'',12)
            pdf.multi_cell(50,6,f"Email: {email}\nPhone: {phone}\nLinkedIn: {linkedin}\nGitHub: {github}\nSkills: {skills}")
            pdf.ln(2)
            pdf.set_xy(70,pdf.get_y())
            for section_name, content in [("Profile Summary", summary), ("Education", education),
                                          ("Work Experience", experience), ("Projects", projects)]:
                if content:
                    section_heading(section_name)
                    pdf.set_font("Arial",'',12)
                    for line in bullet_list(content):
                        pdf.multi_cell(0,6,line)

        # Page border
        pdf.set_draw_color(180,180,180)
        pdf.rect(5,5,200,287)

        buffer_pdf = BytesIO()
        pdf.output(buffer_pdf)
        buffer_pdf.seek(0)
        st.download_button(
            label="Download PDF Resume (.pdf)",
            data=buffer_pdf,
            file_name=f"{sanitize_filename(name)}_{template_option}_{color_theme}_Resume_{timestamp}.pdf",
            mime="application/pdf"
        )

st.markdown("---")
st.write("Made with ❤️ using Python and Streamlit")
