
import PyPDF2
import tempfile

import streamlit as st
import google.generativeai as genai

from explainer import Explainer


def render_api_key():
    api_key = st.text_input("Enter your Gemini API key", type="password")
    if st.button("Update"):
      st.session_state.api_key = api_key
      st.success("API key updated successfully!")
      genai.configure(api_key=st.session_state.api_key)

    st.markdown("[How to get a Gemini API key](https://youtu.be/OVnnVnLZPEo?si=Vi7EAf0nOhUeOUyK)")


def render_uploader():
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
      temp_file = tempfile.NamedTemporaryFile(delete=False)
      temp_file.write(uploaded_file.read())
      uploaded_file = temp_file
      st.session_state.file_path = uploaded_file.name
      reader = PyPDF2.PdfReader(st.session_state.file_path)
      st.session_state.pages_count = len(reader.pages)


def render_configurations():
  # Layout with two columns for configurations
  config_col1, config_col2 = st.columns(2)

  with config_col1:
    render_api_key()
    
  # File uploader in the right column
  with config_col2:
    render_uploader()

  if st.button("Start New Lecture", key="start_lecture", help="Click to start a new lecture"):
    if "file_path" in st.session_state and "api_key" in st.session_state:
      st.session_state.page_number = 1
      st.session_state.messages = []
      st.session_state.explainer = Explainer(st.session_state.file_path)
      st.success("New lecture started successfully!")
    else:
      if "file_path" not in st.session_state:
        st.error("Please upload a PDF file to start a new lecture.")
      if "api_key" not in st.session_state:
        st.error("Please enter your Gemini API key to start a new lecture.")
