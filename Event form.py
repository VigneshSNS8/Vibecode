import streamlit as st
from datetime import datetime
import requests

# ========== Header with Logo ==========
st.image("https://www.bing.com/th?id=OIP.N0Boxtyrfky73SS1LbG4sQHaDD", width=200)
st.title("📅 Event Registration Form")

# ========== Webhook URL ==========
WEBHOOK_URL = "https://vignesh8492.app.n8n.cloud/webhook-test/https://snseventbooking.streamlit.app/"

# ========== Validation Function ==========
def validate_form(institution, event_name, organizer, email_id, event_date, time_slot):
    errors = []
    if institution not in ["SNS iHub", "DT Team"]:
        errors.append("Select a valid Institution.")
    if not event_name.strip():
        errors.append("Event Name is required.")
    if not organizer.strip():
        errors.append("Event Organizer's Name is required.")
    if not email_id.strip():
        errors.append("Organizer's Email ID is required.")
    if not event_date:
        errors.append("Event Date is required.")
    if not time_slot.strip():
        errors.append("Time Slot is required.")
    return errors

# ========== Streamlit Form ==========
with st.form("registration_form"):
    st.subheader("📝 Please fill out the form below")
    
    institution = st.selectbox("🏫 Institution", ["Select", "SNS iHub", "DT Team"])
    event_name = st.text_input("🎯 Event Name")
    organizer = st.text_input("👨‍💼 Event Organizer's Name")
    email_id = st.text_input("📧 Organizer's Email ID")
    event_date = st.date_input("📅 Event Date")

    predefined_slots = ["10:00 AM - 12:00 PM", "01:00 PM - 03:00 PM", "03:00 PM - 05:00 PM", "Custom"]
    slot_choice = st.selectbox("🕒 Choose a Time Slot", predefined_slots)
    
    time_slot = st.text_input("✏️ Enter Custom Time Slot") if slot_choice == "Custom" else slot_choice

    submitted = st.form_submit_button("Register")

    if submitted:
        selected_institution = institution if institution != "Select" else ""
        errors = validate_form(selected_institution, event_name, organizer, email_id, event_date, time_slot)

        if errors:
            for error in errors:
                st.error(error)
        else:
            # Prepare data for webhook
            payload = {
                "institution": selected_institution,
                "event_name": event_name,
                "organizer": organizer,
                "email_id": email_id,
                "event_date": event_date.strftime("%Y-%m-%d"),
                "time_slot": time_slot
            }

            try:
                response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
                if response.status_code == 200:
                    st.success("✅ Registration Successful! Data sent to the system.")
                else:
                    st.warning(f"⚠️ Registered, but webhook returned status code {response.status_code}")
            except Exception as e:
                st.error(f"❌ Registration failed to send to webhook: {e}")

            # Display summary
            st.write("### 📋 Registration Summary")
            st.write(f"**Institution:** {selected_institution}")
            st.write(f"**Event Name:** {event_name}")
            st.write(f"**Organizer:** {organizer}")
            st.write(f"**Organizer's Email:** {email_id}")
            st.write(f"**Date:** {event_date.strftime('%Y-%m-%d')}")
            st.write(f"**Time Slot:** {time_slot}")


