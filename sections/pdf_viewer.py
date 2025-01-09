import os
import PyPDF2
import tempfile

import streamlit as st

from streamlit_pdf_viewer import pdf_viewer


# Initialize session state for page number
if 'page_number' not in st.session_state:
  st.session_state.page_number = 1

# Function to increment page number
def next_page():
  if st.session_state.page_number < st.session_state.pages_count:
    st.session_state.page_number += 1
    st.session_state.messages.append({"role": "model", "parts": st.session_state.explainer.explain_page(st.session_state.page_number)})


# Function to decrement page number
def prev_page():
  if st.session_state.page_number > 1:
    st.session_state.page_number -= 1
    st.session_state.messages.append({"role": "model", "parts": st.session_state.explainer.explain_page(st.session_state.page_number)})



def render_pdf_viewer():
  # Initialize session state for page number
  if 'page_number' not in st.session_state:
    st.session_state.page_number = 1
  # Navigation buttons in the same row with page number in the middle
  col1, col2, col3 = st.columns([1, 2, 1])
  
  with col1:
    if st.button("Previous"):
      prev_page()
  
  with col2:
    st.write(f"{st.session_state.page_number}/{st.session_state.pages_count}", align="center")
  
  with col3:
    if st.button("Next"):
      next_page()

  pdf_viewer(st.session_state.file_path, pages_to_render=[st.session_state.page_number], width=800, height=800)
