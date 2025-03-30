import streamlit as st
import re
import json

def is_valid_email(email):
    """Validate email using regex."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def contact_form():
    st.title("Contact Us")
    
    with st.form("Contact Form"):
        name = st.text_input("First Name")
        email = st.text_input("Email Address")
        message = st.text_area("Your Message")
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if not name:
                st.error("Please provide your name. 😩")
                st.stop()

            if not email:
                st.error("Please provide your email. 📧")
                st.stop()

            if not message:
                st.error("Please provide a message. 💬")
                st.stop()

            if not is_valid_email(email):
                st.error("Please provide a valid email address. 📧")
                st.stop()

            # Save data to a JSON file
            data = {"name": name, "email": email, "message": message}
            try:
                with open("customer_review.json", "a") as c:
                    json.dump(data, c, indent=4)
                    c.write("\n")  # Add newline for readability
                st.success("Your message has been submitted successfully! ✅")
            except Exception as e:
                st.error(f"Error saving data: {e}")
