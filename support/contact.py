import streamlit as st
import re
import requests

def is_valid_email(email):
    """Validate email using regex."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def contact_me():
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
    
            # Prepare the review data
            review_data = {
                "name": name,
                "email": email,
                "message": message,
            }
    
            # Send the review to the viewer app's API endpoint (deployed URL)
            try:
                response = requests.post("https://scraperreviews.streamlit.app/api/reviews", json=review_data)
                if response.status_code == 200:
                    st.success("Your review was sent successfully!")
                else:
                    st.error("Failed to send review to the viewer app.")
            except Exception as e:
                st.error(f"Error sending review: {e}")

