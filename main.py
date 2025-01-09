import PyPDF2
import tempfile

import streamlit as st
import google.generativeai as genai

from explainer import Explainer
from pdf_viewer import render_pdf_viewer
from streamlit_pdf_viewer import pdf_viewer
from quiz import render_quiz
from st_circular_progress import CircularProgress


st.set_page_config(layout="wide")
# Layout with two columns for configurations
config_col1, config_col2 = st.columns(2)

# Text box to input API key in the left column
with config_col1:
  api_key = st.text_input("Enter your Gemini API key", type="password")
  if st.button("Update"):
    st.session_state.api_key = api_key
    st.success("API key updated successfully!")
    genai.configure(api_key=st.session_state.api_key)

  # Tip for how to get Gemini API key
  st.markdown("[How to get a Gemini API key](https://youtu.be/OVnnVnLZPEo?si=Vi7EAf0nOhUeOUyK)")

# File uploader in the right column
with config_col2:
  uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
  if uploaded_file is not None:
    # save file to temp
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())
    uploaded_file = temp_file
    st.session_state.file_path = uploaded_file.name
    reader = PyPDF2.PdfReader(st.session_state.file_path)
    st.session_state.pages_count = len(reader.pages)
  elif 'file_path' in st.session_state:
    file_path = st.session_state.file_path
    reader = PyPDF2.PdfReader(file_path)
    pages_count = st.session_state.pages_count

if st.button("Start New Lecture", key="start_lecture", help="Click to start a new lecture"):
  if "file_path" in st.session_state and "api_key" in st.session_state:
    st.session_state.explainer = Explainer(st.session_state.file_path)
    st.session_state.messages = []
    st.success("New lecture started successfully!")
  else:
    if "file_path" not in st.session_state:
      st.error("Please upload a PDF file to start a new lecture.")
    if "api_key" not in st.session_state:
      st.error("Please enter your Gemini API key to start a new lecture.")


if "file_path" not in st.session_state or "explainer" not in st.session_state:
  st.stop()


# Layout with two columns
col1, col2 = st.columns([2, 1])

# PDF viewer in the left column
with col1:
  render_pdf_viewer()


# Chat interface in the right column
with col2:
  st.header("Chat with slides")
  if 'messages' not in st.session_state:
    st.session_state.messages = []

  messages = st.container(height=500)
  if user_input := st.chat_input("Type a message..."):
    st.session_state.messages.append({"role": "user", "parts": user_input})
    # Here you would add the chatbot response logic
    st.session_state.messages.append({"role": "model", "parts": st.session_state.explainer.answer_question(st.session_state.page_number, user_input)})

  for message in st.session_state.messages:
    messages.chat_message(message["role"]).write(message["parts"])
  
  render_quiz()
    
