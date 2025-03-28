import streamlit as st

# Title and introduction
st.title("Email Web Scraper Usage Tutorial")
st.markdown("""
Welcome to the Email Web Scraper Tutorial!  
This guide will walk you through how to use our two web scraping tools:
- **Simple Scraper**: Quickly scrapes web pages for email addresses using basic regex matching.
- **Advanced Scraper**: Checks the site's `robots.txt` file to respect crawling rules, then scrapes for emails if allowed.

""")

st.markdown("## 1. Using the Simple Scraper")
st.markdown("""
The **Simple Scraper** performs a Google search based on your query, then visits each resulting URL to extract email addresses.  
**How to use it:**
- **Step 1:** Enter your search query (e.g., `contact email`).
- **Step 2:** Specify how many emails you need.
- **Step 3:** Set the maximum number of URLs to search.
- **Step 4:** Click the **Scrape Emails** button.
  
The scraper will display the emails it finds in a copyable text area\n It is advised to use the advanced webscraper in order to respect websites `robots.txt`.
""")


st.markdown("## 2. Using the Advanced Scraper")
st.markdown("""
The **Advanced Scraper** works similarly to the Simple Scraper but first checks the site's `robots.txt` file. This ensures that the scraper respects the site owner's rules before extracting any emails.  
**How to use it:**
- Follow similar steps as the Simple Scraper.
- The tool would check if url is in blacklist
- The tool will indicate whether scraping is allowed for each URL.
- If allowed, it will scrape and display the emails.
- If a URL doesn't respond and is delaying program execution, the code automatically blacklists it.
- The domain name query currently only responds to @gmail.com.   
This is recommended when you need to be extra cautious and follow best practices regarding website scraping.
""")


st.markdown("## 3. General Info")
st.markdown("""
- The code automatically removes any duplicate emails so you may get less than the amount of emails you requested for.
- Make sure that the number of URL's is close to or more than two times the number of emails you need to ensure that you get close to that amount.
- Note that some URL's may take a long time to respond, that's a problem on their end not from the app.
""")
