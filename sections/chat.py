
import streamlit as st


def render_chat():
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