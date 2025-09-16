import streamlit as st
from db_helpers import setup_database, add_question, get_all_questions

# --- Page Configuration ---
st.set_page_config(
    page_title="Seminar Q&A",
    page_icon="❓",
    layout="centered"
)

# --- Database Setup ---
# This will run once to ensure the table exists.
setup_database()

# --- App Title ---
st.title("AI for Educators: Q&A Portal")
st.markdown("Submit your questions below. They will be reviewed by the seminar host.")

# --- Main Panel - Q&A Portal ---
with st.form(key='question_form', clear_on_submit=True):
    question_text = st.text_area("Please type your question here:", height=150, key="question_input")
    submit_button = st.form_submit_button(label='Submit Question')

    if submit_button and question_text:
        add_question(question_text)
        st.toast("Your question has been submitted!", icon="✅")

# --- Display Submitted Questions ---
st.subheader("Recently Submitted Questions")
st.markdown("_(This list shows the most recent submissions from all attendees)_")

questions = get_all_questions()

if not questions:
    st.info("No questions have been submitted yet. Be the first!")
else:
    # Display the 5 most recent questions to show activity
    for i, question in enumerate(questions[:5]):
        st.markdown(f"**Q:** {question}")
        st.divider()
    if len(questions) > 5:
        st.info(f"...and {len(questions) - 5} more.")

