import time
import threading

import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx

PREFETCH_LIMIT = 3

class PrefetcherThread(threading.Thread):
  def __init__(self):
    super().__init__()
    self._stop_event = threading.Event()
    add_script_run_ctx(self)

  def run(self):
    while not self._stop_event.is_set():
      if "page_number" in st.session_state and "explainer" in st.session_state:
        current_page = st.session_state.page_number
        for page in range(current_page + 1, current_page + PREFETCH_LIMIT + 1):
          print("Fetching page", page)
          st.session_state.explainer.fetch_page_explanation(page)
          st.session_state.explainer.quiz_page(page)
      time.sleep(1)

  def stop(self):
    self._stop_event.set()
