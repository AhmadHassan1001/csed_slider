import streamlit as st

from st_circular_progress import CircularProgress

def render_quiz():
  if "answers_verdicts" not in st.session_state:
    st.session_state.answers_verdicts = [0] * st.session_state.pages_count

  quiz_data = st.session_state.explainer.quiz_page(st.session_state.page_number)
  values = [quiz_data["options"][i]["text"] for i in range(len(quiz_data["options"]))]
  answer = [quiz_data["options"][i]["text"] for i in range(len(quiz_data["options"])) if quiz_data["options"][i]["index"] == quiz_data["answer_index"]][0]
  print("Answer: ", answer)
  st.write(quiz_data["question"])
  user_answer = st.radio("Choose an option", values, index=None)
  
  if user_answer == answer:
    st.success("Correct!\n" + quiz_data["explanation"])
    st.session_state.answers_verdicts[st.session_state.page_number] = 1
  elif user_answer:
    st.error("Incorrect!\n" + quiz_data["explanation"])
    st.session_state.answers_verdicts[st.session_state.page_number] = 0


def render_progress():
  if "answers_verdicts" not in st.session_state:
    st.session_state.answers_verdicts = [0] * st.session_state.pages_count

  progress = int(sum(st.session_state.answers_verdicts) / st.session_state.pages_count*100)
  CircularProgress(
      label="Understand Progress",
      value=progress,
      key=f"understand_progress-${progress}").st_circular_progress()



  

