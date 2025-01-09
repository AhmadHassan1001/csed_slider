import streamlit as st

from sections.quiz import render_quiz, render_progress
from sections.chat import render_chat
from sections.pdf_viewer import render_pdf_viewer
from sections.configurations import render_configurations


st.set_page_config(layout="wide")

render_configurations()

if "file_path" not in st.session_state or "explainer" not in st.session_state:
  st.stop()

render_progress()

col1, col2 = st.columns([2, 1])

with col1:
  render_pdf_viewer()

with col2:
  render_chat()
  render_quiz()
    
