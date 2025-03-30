import streamlit as st
import json
import os

# File to store reviews
REVIEW_FILE = "reviews.json"

def contact_me():
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
                try:
                    with open("reviews.json", "a") as f:
                        json.dump(review, f, indent=4)
                        st.write("REVIEW SENT SUCCESSFULLY")
                except Exception as e:
                    st.write("ERROR, REVIEW UNABLE TO SEND")
                    
                
    
            
              
