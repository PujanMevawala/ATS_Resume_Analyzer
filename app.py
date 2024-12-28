from dotenv import load_dotenv
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Functions for Gemini Response and PDF Setup
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit Layout Configuration
st.set_page_config(page_title="ATS Resume using Gemini", page_icon="🧠", layout="wide")

# Header Section with Styling
st.markdown("""
    <style>
        /* Background Gradient */
        .gradient-background {
            background: linear-gradient(135deg, #00bcd4, #80deea);
            color: #ffffff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* Header Styling */
        .header {
            text-align: center;
            font-size: 3rem;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 20px;
            text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.2);
        }

        /* Sub-header Styling */
        .sub-header {
            text-align: center;
            font-size: 1.3rem;
            color: #e1f5fe;
            margin-top: -10px;
            font-weight: 300;
        }

        /* Cards Section Styling */
        .info-card {
            background-color: #f9f9f9;
            border-radius: 10px;
            padding: 20px;
            margin: 15px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            color: #333;
            font-size: 1rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .info-card:hover {
            transform: translateY(-5px);
            box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.2);
        }

        .info-card h3 {
            color: #0078D7;
            margin-bottom: 10px;
        }

        .info-card p {
            color: #333;
        }

        /* Button Styling */
        .btn {
            background-color: #00acc1;
            color: #ffffff;
            padding: 12px 25px;
            border-radius: 5px;
            border: none;
            font-size: 1rem;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .btn:hover {
            background-color: #007c91;
        }

        /* Footer Styling */
        footer {
            text-align: center;
            font-size: 1rem;
            color: #ffffff;
            margin-top: 30px;
            padding: 10px;
            background-color: #007c91;
            width: 100%;
        }

        footer a {
            text-decoration: none;
            color: #ffffff;
            font-weight: bold;
        }

        footer a:hover {
            color: #00bcd4;
        }
    </style>
    <div>
        <h1 class="header">ATS Resume Analysis</h1>
        <p class="sub-header">Optimize your resume and increase your chances of landing your dream job!</p>
        <hr>
    </div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("ats_logo.webp", use_column_width=True)  # Placeholder for logo
    st.header("Upload & Analyze")
    input = st.text_area("Paste Job Description Here 👇", key="input", placeholder="Paste the job description to analyze...")

# File Uploader Section
uploaded_file = st.file_uploader("Upload Your Resume PDF", type=["pdf"])
if uploaded_file is not None:
    st.success("PDF Uploaded Successfully ✅")

# Action Buttons Section - All in One Row
if uploaded_file is not None:
    pdf_content = input_pdf_setup(uploaded_file)
    st.write("### Actions")
    
    # Organizing buttons in a single row with three equal columns
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Placeholder for the response display
    response_placeholder = st.container()

    with col1:
        if st.button("Analyze Resume", key="analyze"):
            with st.spinner("Analyzing Resume..."):
                response = get_gemini_response(input=input, pdf_content=pdf_content, prompt="""
                You are an experienced Technical Human Resource Manager. 
                Review the provided resume against the job description and share a professional evaluation with the strengths and weaknesses of the candidate with respect to the job description.
                """)
                st.success("Analysis Complete ✅")
                
                # Update the placeholder with the response
                with response_placeholder:
                    st.subheader("Analysis Response:")
                    st.write(response)
                    
                    # Download Button for Analysis
                    analysis_report = f"Resume Analysis:\n\n{response}"
                    st.download_button(
                        label="Download Analysis Report",
                        data=analysis_report.encode('utf-8', 'replace'),
                        file_name="analysis_report.txt",
                        mime="text/plain"
                    )

    with col2:
        if st.button("Percentage Match", key="match"):
            with st.spinner("Calculating Match..."):
                response = get_gemini_response(input=input, pdf_content=pdf_content, prompt="""
                You are an ATS scanner. Evaluate the resume against the job description and provide:
                - Percentage match
                - Missing keywords
                - Final evaluation.
                """)
                st.success("Match Calculation Complete ✅")
                
                # Update the placeholder with the response
                with response_placeholder:
                    st.subheader("Percentage Match Response:")
                    st.write(response)
                    
                    # Download Button for Match Report
                    match_report = f"Percentage Match Analysis:\n\n{response}"
                    st.download_button(
                        label="Download Match Report",
                        data=match_report.encode('utf-8', 'replace'),
                        file_name="match_report.txt",
                        mime="text/plain"
                    )

    with col3:
        if st.button("Extract Keywords", key="keywords"):
            with st.spinner("Extracting Keywords..."):
                response = get_gemini_response(input=input, pdf_content=pdf_content, prompt="""
                Extract the most relevant keywords from the job description and the resume.
                Provide them as a bullet-point list.
                """)
                st.success("Keywords Extraction Complete ✅")
                
                # Update the placeholder with the response
                with response_placeholder:
                    st.subheader("Extracted Keywords:")
                    st.write(response)
                    
                    # Download Button for Keywords
                    keywords_report = f"Extracted Keywords:\n\n{response}"
                    st.download_button(
                        label="Download Keywords",
                        data=keywords_report.encode('utf-8', 'replace'),
                        file_name="keywords_report.txt",
                        mime="text/plain"
                    )

# Information Cards Section
st.markdown("""
    <h2 style="text-align:center; color:#0078D7;">What is ATS (Applicant Tracking System)?</h2>
    <hr style="border: 1px solid #0078D7;">
""", unsafe_allow_html=True)

# Creating three columns for the information cards
col1, col2, col3 = st.columns(3)

# Card 1: What is ATS?
with col1:
    st.markdown("""
        <div class="info-card">
            <h3>What is ATS?</h3>
            <p>
                ATS (Applicant Tracking System) is a software used by companies to streamline the hiring process. 
                It helps recruiters to sort, filter, and rank candidates based on specific keywords and other criteria from resumes.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Card 2: Why ATS is Important for Your Resume
with col2:
    st.markdown("""
        <div class="info-card">
            <h3>Importance of ATS?</h3>
            <p>
                Many companies rely on ATS to screen resumes before they are even seen by human recruiters. 
                Your resume must be optimized with relevant keywords & pass through ATS filters & hiring managers.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Card 3: ATS Role in Interviews
with col3:
    st.markdown("""
        <div class="info-card">
            <h3>ATS in Interviews</h3>
            <p>
                ATS plays a critical role in determining whether you get an interview call. 
                Resumes that pass through the ATS filters are then reviewed by HR, leading to interview opportunities.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Additional section to explain ATS tips for improving your resume
st.markdown("""
    <h3 style="text-align:center; color:#0078D7;">ATS Resume Optimization Tips</h3>
    <hr style="border: 1px solid #0078D7;">
""", unsafe_allow_html=True)

# Tips for optimizing resume for ATS
st.markdown("""
    <div class="info-card">
        <h4>Tips for ATS Optimization:</h4>
        <ul>
            <li>Use standard resume headings like "Experience", "Skills", and "Education".</li>
            <li>Incorporate relevant keywords from the job description.</li>
            <li>Avoid complex formatting like tables, graphics, or images.</li>
            <li>Use simple, clean fonts like Arial or Times New Roman.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Footer Section
st.markdown("""
    <footer>
        <p>&copy; 2024 ATS Resume Analyzer. All rights reserved. <a href="https://www.example.com">Privacy Policy</a></p>
    </footer>
""", unsafe_allow_html=True)


# Job Title: Business Analyst
# Company: Biz Solutions Inc.
# Location: Chicago, IL

# Job Description:
# As a Business Analyst, you will bridge the gap between business needs and technical solutions by analyzing requirements and creating data-driven strategies.

# Responsibilities:

# Gather and document business requirements.
# Analyze processes to identify improvement areas.
# Create detailed reports using visualization tools.
# Required Skills:

# Strong communication and analytical skills
# Proficiency in Excel, SQL, Tableau, or Power BI
# Experience in writing requirement documents
# Preferred Qualifications:

# Knowledge of Agile methodology
# Certification in Business Analysis