import streamlit as st
from openai import OpenAI
from db_helpers import get_all_questions, clear_all_questions

# --- Page Configuration ---
st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="⚙️",
    layout="wide"
)

# --- Helper Function for Summary ---
def get_summary(api_key, all_questions):
    if not api_key:
        st.error("Please enter your OpenAI API key to generate a summary.")
        return None
    try:
        client = OpenAI(api_key=api_key)
        questions_text = "\n".join(f"- {q}" for q in all_questions)
        system_prompt = "You are a helpful assistant designed to summarize and categorize questions from a seminar for educators."
        user_prompt = (
            "Analyze the following questions from a teachers' seminar on AI. "
            "Group them into logical categories (e.g., 'Classroom Implementation', 'Ethical Concerns'). "
            "Under each category, list the full, original questions as bullet points. "
            "Ensure the full context of every question is preserved. Here are the questions:\n\n"
            f"{questions_text}"
        )
        with st.spinner('AI is thinking...'):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred with the OpenAI API: {e}")
        return None

# --- Simple Password Protection ---
def password_entered():
    """Checks whether a password entered by the user is correct."""
    # Use st.secrets for deployed apps
    if st.secrets.get("ADMIN_PASSWORD") and st.session_state["password"] == st.secrets["ADMIN_PASSWORD"]:
        st.session_state["password_correct"] = True
        del st.session_state["password"]  # don't store password
    # Fallback for local development
    elif st.session_state["password"] == "admin123":
        st.session_state["password_correct"] = True
        del st.session_state["password"]
    else:
        st.session_state["password_correct"] = False

# --- Main Admin UI ---
st.title("⚙️ Admin Dashboard")

if not st.session_state.get("password_correct", False):
    st.text_input("Password", type="password", on_change=password_entered, key="password")
    if "password_correct" in st.session_state and not st.session_state.password_correct:
        st.error("😕 Password incorrect")
    st.stop() # Do not render the rest of the page

# --- Full Admin Interface (after password) ---
st.success("Authenticated successfully.")

# Get questions from the database
all_questions = get_all_questions()

# Layout with two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"📥 Submitted Questions ({len(all_questions)})")
    if st.button("Clear All Questions", type="primary"):
        clear_all_questions()
        st.toast("All questions have been cleared.")
        st.rerun() # Rerun to update the view
    
    if not all_questions:
        st.info("The question queue is empty.")
    else:
        for i, question in enumerate(all_questions):
            st.markdown(f"**{i+1}.** {question}")
            st.divider()

with col2:
    st.subheader("🤖 AI Summary")
    # Use st.secrets for the API key in deployed app
    api_key_input = st.text_input(
        "Enter OpenAI API Key", 
        type="password",
        value=st.secrets.get("OPENAI_API_KEY", ""), # Pre-fill from secrets if available
        help="Your API key is used only for this session."
    )
    
    if st.button("Generate Summary", disabled=(len(all_questions) == 0)):
        summary = get_summary(api_key_input, all_questions)
        if summary:
            st.session_state.summary = summary
    
    if "summary" in st.session_state:
        st.markdown(st.session_state.summary)
