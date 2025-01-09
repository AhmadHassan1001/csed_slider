import io
import json
import base64
import PyPDF2
import asyncio
import streamlit as st
import google.generativeai as genai

from utils.quiz import Quiz

model = genai.GenerativeModel("gemini-1.5-flash")


if "api_key" in st.session_state:
    genai.configure(api_key=st.session_state.api_key)
  
class Explainer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.page_explanations = {}
        # self.get_summary()
        if "quiz" not in st.session_state:
            st.session_state.quiz = {}

    def set_api_key(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=api_key)

    def explain_page(self, page_number):
        explanation = self.fetch_page_explanation(page_number)
        self.prefetch_pages(page_number)
        return explanation
    

    def quiz_page(self, page_number):
        if page_number in st.session_state.quiz:
            return st.session_state.quiz[page_number]
        # Get the explanation for the page
        chat = model.start_chat(
            history=self.get_history(),
        )
        page_data = self.extract_page_as_base64(page_number)
        prompt = "Give me an MCQ question based on the most recent data"
        
        # Ask the AI model to answer the question
        response = chat.send_message([{'mime_type': 'application/pdf', 'data': page_data}, prompt],
                                     generation_config=genai.GenerationConfig(response_mime_type="application/json", response_schema=Quiz),)
        answer = json.loads(response.text)
        print(answer)
        st.session_state.quiz[page_number] = answer
        return answer

    def answer_question(self, page_number, question):
        # Get the explanation for the page
        chat = model.start_chat(
            history=self.get_history(),
        )
        page_data = self.extract_page_as_base64(page_number)
        
        # Ask the AI model to answer the question
        response = chat.send_message([{'mime_type': 'application/pdf', 'data': page_data}, question])
        answer = response.text
        return answer

    def get_summary(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        with open(self.file_path, "rb") as doc_file:
            doc_data = base64.standard_b64encode(doc_file.read()).decode("utf-8")
            response = model.generate_content([{'mime_type': 'application/pdf', 'data': doc_data}, 
                                               "Give me a summary of these slides to help me understand the content and context. It shouldn't exceed 3 sentences."])
            summary = response.text
            st.session_state.messages.append({"role": "model", "parts": summary})
        inital_slide = self.explain_page(1)
        st.session_state.messages.append({"role": "model", "parts": inital_slide}) 
    
    def get_history(self):
        return st.session_state.messages[-5:]
    

    def fetch_page_explanation(self, page_number):
        if page_number in self.page_explanations:
            return self.page_explanations[page_number]
        
        page_data = self.extract_page_as_base64(page_number)
        chat = model.start_chat(
            history=self.get_history(),
        )
        prompt = "Give me breif explanation of this slide"
        response = chat.send_message([{'mime_type': 'application/pdf', 'data': page_data}, prompt])
        explanation = response.text
        self.page_explanations[page_number] = explanation
        return explanation

    def prefetch_pages(self, page_number):
        pass

    def extract_page_as_base64(self, page_number):
        try:
            # Open the PDF file
            with open(self.file_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                
                # Check if the page number is valid
                if page_number < 1 or page_number > len(reader.pages):
                    raise ValueError("Invalid page number.")
                
                # Create a new PDF writer to extract the page
                writer = PyPDF2.PdfWriter()
                writer.add_page(reader.pages[page_number - 1])
                
                # Write the page to a binary buffer
                binary_buffer = io.BytesIO()
                writer.write(binary_buffer)
                
                # Get the binary content
                binary_content = binary_buffer.getvalue()
                
                # Encode to Base64
                base64_content = base64.b64encode(binary_content).decode('utf-8')
                return base64_content
        
        except Exception as e:
            print(f"Error: {e}")
            return None
    

