import streamlit as st
import json
import os

# File to store reviews
REVIEW_FILE = "reviews/customer_review.json"

# Streamlit UI
st.title("Contact Us")

with st.form("Contact Form"):
    name = st.text_input("First Name")
    email = st.text_input("Email Address")
    message = st.text_area("Your Message")
    submit_button = st.form_submit_button("Submit")

    if submit_button:
        if name and email and message:
            # Create review object
            review = {
                "Sender": name,
                "Sender Email": email,
                "Message": message
            }

            # Check if the file exists and read existing reviews
            if os.path.exists(REVIEW_FILE):
                with open(REVIEW_FILE, "r", encoding="utf-8") as f:
                    try:
                        reviews = json.load(f)
                        if not isinstance(reviews, list):
                            reviews = []
                    except json.JSONDecodeError:
                        reviews = []
            else:
                reviews = []

            # Append new review
            reviews.append(review)

            # Save back to file
            with open(REVIEW_FILE, "w", encoding="utf-8") as f:
                json.dump(reviews, f, indent=4)

            st.success("Your review has been sent!")
            st.balloons()
        else:
            st.error("All fields are required!")
