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
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #e8f1f8, #ffffff);
            color: #333;
        }

        .header {
            text-align: center;
            color: #0078D7;
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 5px;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        }

        .sub-header {
            text-align: center;
            color: #666;
            font-size: 1.3rem;
            font-weight: 300;
            margin-top: -10px;
        }

        hr {
            border: 0;
            height: 1px;
            background: linear-gradient(to right, #0078D7, #00a8ff);
        }

        footer {
            text-align: center;
            font-size: small;
            color: #666;
            margin-top: 50px;
        }

        footer a {
            text-decoration: none;
            color: #0078D7;
            font-weight: bold;
        }

        footer a:hover {
            color: #0056b3;
        }
    </style>
    <h1 class="header">ATS Resume Analysis</h1>
    <p class="sub-header">Optimize your resume and increase your chances of landing your dream job!</p>
    <hr>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("ats_logo.webp", use_container_width=True)  # Placeholder for logo
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

# Footer Section with Interactive Links
st.markdown("""
    <footer>
        <hr>
        Powered by <a href="https://streamlit.io/" target="_blank">Streamlit</a> | 
        AI Models by Google Gemini | Designed with ❤️ by [Your Name]
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