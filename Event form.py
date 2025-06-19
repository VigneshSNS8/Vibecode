import streamlit as st
from datetime import datetime

# Title
st.title("🎉 Event Registration Form")

# Function to validate inputs
def validate_form(name, institution, event_name, organizer, event_date, time_slot):
    errors = []
    if not name.strip():
        errors.append("Participant's Name is required.")
    if institution not in ["SNS iHub", "DT Team"]:
        errors.append("Select a valid Institution.")
    if not event_name.strip():
        errors.append("Event Name is required.")
    if not organizer.strip():
        errors.append("Event Organizer's Name is required.")
    if not event_date:
        errors.append("Event Date is required.")
    if not time_slot.strip():
        errors.append("Time Slot is required.")
    return errors

# Form Inputs
with st.form("registration_form"):
    name = st.text_input("👤 Participant's Name")
    institution = st.selectbox("🏫 Institution", ["Select", "SNS iHub", "DT Team"])
    event_name = st.text_input("🎯 Event Name")
    organizer = st.text_input("👨‍💼 Event Organizer's Name")
    event_date = st.date_input("📅 Event Date")
    
    predefined_slots = ["10:00 AM - 12:00 PM", "01:00 PM - 03:00 PM", "03:00 PM - 05:00 PM", "Custom"]
    slot_choice = st.selectbox("🕒 Choose a Time Slot", predefined_slots)
    
    time_slot = ""
    if slot_choice == "Custom":
        time_slot = st.text_input("✏️ Enter Custom Time Slot")
    else:
        time_slot = slot_choice

    submitted = st.form_submit_button("Register")

    if submitted:
        # Validate
        errors = validate_form(name, institution if institution != "Select" else "", event_name, organizer, event_date, time_slot)
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            st.success("✅ Registration Successful!")
            st.write("### Registration Details")
            st.write(f"**Name:** {name}")
            st.write(f"**Institution:** {institution}")
            st.write(f"**Event Name:** {event_name}")
            st.write(f"**Organizer:** {organizer}")
            st.write(f"**Date:** {event_date.strftime('%Y-%m-%d')}")
            st.write(f"**Time Slot:** {time_slot}")