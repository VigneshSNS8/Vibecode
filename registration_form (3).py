import streamlit as st
import re
import requests
from datetime import datetime, date, timedelta
import smtplib
from email.message import EmailMessage
import os

st.set_page_config(page_title="Vibe Code Fest Registration", page_icon=":computer:", layout="centered")

st.title("Vibe Code Fest Registration")

# Initialize session state to store form submissions
if 'submissions' not in st.session_state:
    st.session_state.submissions = []

# Webhook URL (replace with your actual webhook URL)
WEBHOOK_URL = "https://vignesh8492.app.n8n.cloud/webhook-test/https://vibecode-2ddrhjbwkhadznzmruffxe.streamlit.app/"

# SMTP configuration for sending emails (load from environment variables)
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "your-email@gmail.com")
SMTP_PASS = os.getenv("SMTP_PASS", "your-app-password")

# Function to send reminder email
def send_reminder_email(email, name, event_date):
    msg = EmailMessage()
    msg.set_content(f"""
Dear {name},

This is a reminder for your participation in Vibe Code Fest on {event_date}.
Please ensure you arrive on time and bring any necessary materials.
For any questions, contact us at support@vibecodefest.com.

Best regards,
Vibe Code Fest Team
""")
    msg["Subject"] = "Vibe Code Fest Reminder: Event Tomorrow"
    msg["From"] = SMTP_USER
    msg["To"] = email

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Failed to send reminder to {email}: {str(e)}")
        return False

# Check for reminders (run on app load)
today = date.today()
tomorrow = today + timedelta(days=1)
for submission in st.session_state.submissions:
    event_date = datetime.strptime(submission["Event Date"], "%Y-%m-%d").date()
    if event_date == tomorrow:
        email = submission["Email ID"]
        name = submission["Name"]
        if send_reminder_email(email, name, submission["Event Date"]):
            st.success(f"Reminder email sent to {email} for event on {submission['Event Date']}.")

# Create form
with st.form(key="registration_form"):
    name = st.text_input("Name", placeholder="Enter your full name")
    contact = st.text_input("Contact Number", placeholder="Enter 10-digit phone number")
    occupation = st.selectbox("Occupation", ["Select your occupation", "Student", "Company"])
    email = st.text_input("Email ID", placeholder="Enter your email")
    expertise = st.selectbox("Technical Expertise", ["Select your expertise level", "Beginner", "Intermediate", "Professional"])
    event_date = st.date_input(
        "Event Date",
        help="Click to open the calendar and select any date. Use the arrows or dropdowns to navigate months and years."
    )
    submit_button = st.form_submit_button("Register")

    # Validation and submission logic
    if submit_button:
        # Check if all fields are filled
        if not name or not contact or occupation == "Select your occupation" or not email or expertise == "Select your expertise level" or not event_date:
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
                "Technical Expertise": expertise,
                "Event Date": event_date.strftime("%Y-%m-%d")
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
- **Event Date** selection is required to confirm your participation slot (choose from July 1-3, 2025).
- Vibe Code Fest is a **coding competition**; please select your technical expertise accurately.
- For queries, contact us at [support@vibecodefest.com](mailto:support@vibecodefest.com).
""")

# Display submitted data (for demo purposes)
if st.session_state.submissions:
    st.subheader("Registered Participants")
    for i, submission in enumerate(st.session_state.submissions, 1):
        st.write(f"**Participant {i}:**")
        st.json(submission)
