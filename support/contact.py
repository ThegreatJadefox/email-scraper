import streamlit as st
import requests
import json
from base64 import b64decode, b64encode

# GitHub Configuration
GITHUB_USER = "ThegreatJadefox"
GITHUB_REPO = "review-storage"
GITHUB_FILE = "reviews.json"
GITHUB_TOKEN = "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"

# Function to save reviews to GitHub
def save_review(name, email, message):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{GITHUB_FILE}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    # Get the existing file from GitHub
    response = requests.get(url, headers=headers)
    data = response.json()

    if "content" in data:
        reviews = json.loads(b64decode(data["content"]).decode())  # Decode existing reviews
    else:
        reviews = []

    # Append new review
    reviews.append({"name": name, "email": email, "message": message})

    # Upload updated reviews back to GitHub
    update_data = {
        "message": "New review added",
        "content": b64encode(json.dumps(reviews).encode()).decode(),
        "sha": data.get("sha", "")  # Required to update the file
    }
    requests.put(url, headers=headers, json=update_data)

# Streamlit UI
st.title("Contact Us")

with st.form("Contact Form"):
    name = st.text_input("First Name")
    email = st.text_input("Email Address")
    message = st.text_area("Your Message")
    submit_button = st.form_submit_button("Submit")

    if submit_button:
        if name and email and message:
            save_review(name, email, message)
            st.success("Your review has been sent!")
            st.ballon()
        else:
            st.error("All fields are required!")

                st.error(f"Error sending review: {e}")

