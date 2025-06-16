import streamlit as st
import requests
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Lecture Feedback Form", page_icon="📝", layout="centered")

# Title and description
st.title("Lecture Session Feedback Form")
st.write("Please provide your feedback for the lecture session.")

# Webhook URL (replace with your actual webhook URL)
WEBHOOK_URL = "https://vignesh8492.app.n8n.cloud/webhook-test/https://feedback-rfyolsubhttkzwrlffmt4g.streamlit.app/"

# Initialize session state for form submission
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Create a form
with st.form(key="feedback_form"):
    # Input fields
    name = st.text_input("Name", max_chars=50, placeholder="Enter your full name")
    reg_number = st.text_input("Register Number", max_chars=20, placeholder="Enter your register number")
    feedback = st.text_area("Feedback", height=150, placeholder="Share your thoughts about the lecture session")

    # Submit button
    submit_button = st.form_submit_button("Submit Feedback")

    # Handle form submission
    if submit_button:
        # Validate inputs
        if not name.strip() or not reg_number.strip() or not feedback.strip():
            st.error("Please fill out all fields before submitting.")
        else:
            # Prepare data for webhook
            feedback_data = {
                "name": name,
                "register_number": reg_number,
                "feedback": feedback,
                "timestamp": str(pd.Timestamp.now())
            }

            # Send data to webhook
            try:
                response = requests.post(WEBHOOK_URL, json=feedback_data)
                if response.status_code == 200:
                    st.session_state.submitted = True
                else:
                    st.error(f"Failed to send feedback. Webhook responded with status code: {response.status_code}")
            except requests.RequestException as e:
                st.error(f"Error sending feedback to webhook: {str(e)}")

# Display success message after submission
if st.session_state.submitted:
    st.success("Thank you for your feedback! You may close this page or submit another response.")
    st.session_state.submitted = False  # Reset for new submission

# Add some styling
st.markdown(
    """
    <style>
    .stTextInput, .stTextArea {
        border-radius: 5px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
