import streamlit as st
from fpdf import FPDF

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Premium CV Builder", layout="wide")

st.title("Premium CV / Resume Builder")

# -------------------- STYLING --------------------
accent = st.color_picker("Accent Color", "#2E86C1")

# -------------------- PERSONAL INFO --------------------
st.header("Personal Information")

full_name = st.text_input("Full Name", key="name")
title = st.text_input("Professional Title", key="title")
email = st.text_input("Email", key="email")
phone = st.text_input("Phone", key="phone")
location = st.text_input("Location", key="location")
linkedin = st.text_input("LinkedIn URL", key="linkedin")
github = st.text_input("GitHub URL", key="github")
portfolio = st.text_input("Portfolio URL", key="portfolio")

summary = st.text_area("Professional Summary", height=120, key="summary")

# -------------------- DYNAMIC SECTIONS --------------------
def add_dynamic_section(section_name, fields):
    st.header(section_name)
    count = st.number_input(
        f"How many {section_name} entries?",
        min_value=1,
        max_value=10,
        value=1,
        step=1,
        key=f"{section_name}_count"
    )

    items = []
    for i in range(count):
        st.subheader(f"{section_name} #{i+1}")
        entry = {}
        for field in fields:
            entry[field] = st.text_input(
                f"{field} (Entry #{i+1})",
                key=f"{section_name}_{field}_{i}"
            )
        items.append(entry)
    return items

experience = add_dynamic_section(
    "Work Experience",
    ["Job Title", "Company", "Start Date - End Date", "Responsibilities"]
)

education = add_dynamic_section(
    "Education",
    ["Degree", "Institution"]
)

# -------------------- PDF GENERATION --------------------
class ResumePDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 10, full_name, ln=True)
        self.set_font("Helvetica", "", 12)
        self.cell(0, 8, title, ln=True)
        self.ln(4)

def generate_pdf():
    pdf = ResumePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(
        0,
        8,
        f"{email} | {phone} | {location}\n{linkedin} | {github} | {portfolio}"
    )
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "PROFESSIONAL SUMMARY", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 8, summary)
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "WORK EXPERIENCE", ln=True)
    pdf.set_font("Helvetica", "", 11)

    for exp in experience:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, f"{exp['Job Title']} — {exp['Company']}", ln=True)
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 6, exp["Start Date - End Date"], ln=True)
        pdf.set_font("Helvetica", "", 11)

        for r in exp["Responsibilities"].split(","):
            pdf.cell(5)
            pdf.multi_cell(0, 6, f"- {r.strip()}")
        pdf.ln(2)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "EDUCATION", ln=True)
    pdf.set_font("Helvetica", "", 11)

    for edu in education:
        pdf.cell(0, 8, f"{edu['Degree']} — {edu['Institution']}", ln=True)

    return pdf.output(dest="S").encode("latin-1")

# -------------------- DOWNLOAD --------------------
st.divider()

if st.button("Generate PDF"):
    pdf_bytes = generate_pdf()

    st.download_button(
        "Download Resume PDF",
        pdf_bytes,
        file_name="resume.pdf",
        mime="application/pdf"
    )
