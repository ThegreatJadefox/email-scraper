import streamlit as st
import requests
import re
import logging
from bs4 import BeautifulSoup
from googlesearch import search  # pip install google
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse, urljoin

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# Regex for email validation
EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

def extract_emails_from_text(text):
    """Return a set of valid emails found in the given text."""
    return set(match.group() for match in EMAIL_REGEX.finditer(text))

def can_scrape(url):
    """
    Check the site's robots.txt to see if scraping is allowed
    for User-agent: * on the specific URL.
    """
    parsed = urlparse(url)
    robots_url = urljoin(f"{parsed.scheme}://{parsed.netloc}", "robots.txt")
    
    rp = RobotFileParser()
    rp.set_url(robots_url)
    try:
        # This call may be slow; you can adjust behavior here if needed.
        rp.read()
    except Exception as e:
        st.warning(f"Error reading robots.txt from {robots_url}: {e}")
        logger.exception(f"robots.txt error for {robots_url}: {e}")
        return False
    return rp.can_fetch("*", url)

def scrape_emails_from_url(url):
    """Scrape emails from a given URL, if allowed by robots.txt."""
    emails = set()
    if not can_scrape(url):
        st.info(f"Scraping disallowed by robots.txt for: {url}")
        logger.info(f"Scraping disallowed for {url}")
        return emails
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()
            emails = extract_emails_from_text(text)
        else:
            logger.warning(f"URL {url} returned status code: {response.status_code}")
    except Exception as e:
        st.warning(f"Error fetching {url}: {e}")
        logger.exception(f"Error fetching {url}: {e}")
    return emails

def main():
    st.title("Email Web Scraper - Advanced Version (Respects robots.txt)")
    st.write(
        """
        This tool will:
        - Perform a Google search based on your query.
        - For each result, check the site's robots.txt to ensure scraping is allowed.
        - If allowed, scrape the page for emails and validate them using regex.
        - Display them in a copyable format.
        """
    )
    
    # User inputs
    query = st.text_input("Enter your search query:", "contact email")
    num_emails_needed = st.number_input("How many emails do you need?", min_value=1, value=10, step=1)
    max_urls = st.number_input("Maximum number of URLs to scrape:", min_value=1, value=20, step=1)
    
    if st.button("Scrape Emails"):
        found_emails = set()
        st.info("Searching and scraping emails... please wait.")
        
        try:
            for url in search(query, tld="com", lang="en", num=max_urls, stop=max_urls, pause=2):
                st.write(f"Checking robots.txt for: {url}")
                if can_scrape(url):
                    st.write(f"Scraping allowed for: {url}")
                    emails = scrape_emails_from_url(url)
                    if emails:
                        found_emails.update(emails)
                    if len(found_emails) >= num_emails_needed:
                        break
                else:
                    st.write(f"Scraping disallowed by robots.txt: {url}")
        except Exception as e:
            st.error(f"An error occurred during the search: {e}")
            logger.exception(f"Search error: {e}")
        
        # Limit emails to the user requested number
        found_emails = list(found_emails)[:num_emails_needed]
        
        if found_emails:
            st.success(f"Found {len(found_emails)} email(s):")
            st.text_area("Emails (copy them below):", value="\n".join(found_emails), height=200)
        else:
            st.info("No emails found. Try a different query or adjust parameters.")

# Run main unconditionally so that it executes when imported
main()
