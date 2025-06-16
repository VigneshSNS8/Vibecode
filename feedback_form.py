import streamlit as st
import pandas as pd
import os

# Set page configuration
st.set_page_config(page_title="Lecture Feedback Form", page_icon="📝", layout="centered")

# Title and description
st.title("Lecture Session Feedback Form")
st.write("Please provide your feedback for the lecture session.")

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
            # Store feedback in a CSV file
            feedback_data = {
                "Name": [name],
                "Register Number": [reg_number],
                "Feedback": [feedback],
                "Timestamp": [pd.Timestamp.now()]
            }
            df = pd.DataFrame(feedback_data)

            # Append to CSV file if it exists, else create new
            file_path = "feedback_data.csv"
            if os.path.exists(file_path):
                df.to_csv(file_path, mode='a', header=False, index=False)
            else:
                df.to_csv(file_path, index=False)

            st.session_state.submitted = True

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