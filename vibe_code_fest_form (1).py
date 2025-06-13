import streamlit as st
import re
import requests

st.set_page_config(page_title="Vibe Code Fest Registration", page_icon=":computer:", layout="centered")

st.title("Vibe Code Fest Registration")

# Initialize session state to store form submissions
if 'submissions' not in st.session_state:
    st.session_state.submissions = []

# Webhook URL (replace with your actual webhook URL)
WEBHOOK_URL = "https://vignesh8492.app.n8n.cloud/webhook-test/https://vibecodenew.streamlit.app/"  # e.g., "https://hooks.zapier.com/hooks/catch/1234567/abcdef/"

# Create form
with st.form(key="registration_form"):
    name = st.text_input("Name", placeholder="Enter your full name")
    contact = st.text_input("Contact Number", placeholder="Enter 10-digit phone number")
    occupation = st.selectbox("Occupation", ["Select your occupation", "Student", "Company"])
    email = st.text_input("Email ID", placeholder="Enter your email")
    expertise = st.selectbox("Technical Expertise", ["Select your expertise level", "Beginner", "Intermediate", "Professional"])
    submit_button = st.form_submit_button("Register")

    # Validation and submission logic
    if submit_button:
        # Check if all fields are filled
        if not name or not contact or occupation == "Select your occupation" or not email or expertise == "Select your expertise level":
            st.error("Please fill out all fields.")
        # Validate contact number (10 digits)
        elif not re.match(r"^\d{10}$", contact):
            st.error("Please enter a valid 10-digit phone number.")
        # Validate email format
        elif not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            st.error("Please enter a valid email address.")
        else:
            # Store submission in session state
            submission = {
                "Name": name,
                "Contact Number": contact,
                "Occupation": occupation,
                "Email ID": email,
                "Technical Expertise": expertise
            }
            st.session_state.submissions.append(submission)

            # Send data to webhook
            try:
                response = requests.post(WEBHOOK_URL, json=submission)
                if response.status_code == 200:
                    st.success("Registration successful! Data sent to webhook and you'll receive a confirmation email soon.")
                else:
                    st.warning(f"Registration stored, but webhook failed with status code {response.status_code}.")
            except requests.exceptions.RequestException as e:
                st.warning(f"Registration stored, but webhook failed: {str(e)}")

# Display important details
st.markdown("""
### Important Details:
- **Registration is mandatory** for all participants.
- Ensure your **contact number** is valid (10 digits) for event updates.
- **Email ID** will be used for confirmation and further communication.
- Vibe Code Fest is a **coding competition**; please select your technical expertise accurately.
- For queries, contact us at [support@vibecodefest.com](mailto:support@vibecodefest.com).
""")

# Display submitted data (for demo purposes)
if st.session_state.submissions:
    st.subheader("Registered Participants")
    for i, submission in enumerate(st.session_state.submissions, 1):
        st.write(f"**Participant {i}:**")
        st.json(submission)