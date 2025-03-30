import streamlit as st
import requests
import json
from base64 import b64decode, b64encode

# GitHub Configuration
GITHUB_USER = "ThegreatJadefox"
GITHUB_REPO = "review-storage"
GITHUB_FILE = "reviews.json"
GITHUB_TOKEN = "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"


# Streamlit UI
st.title("Contact Us")

with st.form("Contact Form"):
    name = st.text_input("First Name")
    email = st.text_input("Email Address")
    message = st.text_area("Your Message")
    submit_button = st.form_submit_button("Submit")
    data = {
        "Sender": name,
        "Sender Email": email,
        "Message": message
    }

    if submit_button:
        if name and email and message:
            with open("customer_review.json", "a") as f:
                json.dump(
            st.success("Your review has been sent!")
            st.ballon()
        else:
            st.error("All fields are required!")

                st.error(f"Error sending review: {e}")

