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
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to process PDF
def input_pdf_setup(upload_file):
    if upload_file is None:
        raise FileNotFoundError("No file uploaded")
    
    images = pdf2image.convert_from_bytes(upload_file.read())
    first_page = images[0]

    # Convert first page to base64
    img_byte_arr = io.BytesIO()
    first_page.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    pdf_parts = [{
        "mime_type": "image/jpeg",
        "data": base64.b64encode(img_byte_arr).decode()
    }]
    
    return pdf_parts

# Function to get Gemini response
def get_gemini_response(input_text, pdf_content, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content([input_text, pdf_content[0], prompt])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file:
    st.write("✅ PDF Uploaded Successfully")
    if "pdf_content" not in st.session_state:
        st.session_state.pdf_content = input_pdf_setup(uploaded_file)  


# Buttons
if st.button("Job Description and Resume Matching"):
    if not input_text.strip():
        st.write("⚠️ Please enter a job description.")
    else:
        response = get_gemini_response(input_text, st.session_state.pdf_content, """
            Analyze the job description and resume for compatibility. Provide a percentage match, missing skills, 
            and irrelevant information in the resume.
        """)
        st.subheader("Response:")
        st.write(response)

elif st.button("Missing Key Points and Skill Gap Analysis"):
    if not input_text.strip():
        st.write("⚠️ Please enter a job description.")
    else:
        response = get_gemini_response(input_text, st.session_state.pdf_content, """
            Identify missing skills and qualifications from the resume based on the job description. 
            Provide actionable steps to fill these gaps.
        """)
        st.subheader("Response:")
        st.write(response)

elif st.button("Resume Optimization Suggestions"):
    if not input_text.strip():
        st.write("⚠️ Please enter a job description.")
    else:
        response = get_gemini_response(input_text, st.session_state.pdf_content, """
            Suggest ATS-friendly resume modifications, including improved phrasing, keyword usage, 
            and formatting enhancements.
        """)
        st.subheader("Response:")
        st.write(response)

elif st.button("Job-Specific Customization Tips"):
    if not input_text.strip():
        st.write("⚠️ Please enter a job description.")
    else:
        response = get_gemini_response(input_text, st.session_state.pdf_content, """
            Provide industry-specific resume customization tips, emphasizing relevant skills and experiences.
        """)
        st.subheader("Response:")
        st.write(response)

elif st.button("Selection and Interview Preparation Suggestions"):
    if not input_text.strip():
        st.write("⚠️ Please enter a job description.")
    else:
        response = get_gemini_response(input_text, st.session_state.pdf_content, """
            Provide interview preparation tips, LinkedIn optimization suggestions, and common interview questions.
        """)
        st.subheader("Response:")
        st.write(response)
