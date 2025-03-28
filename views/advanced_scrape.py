import streamlit as st
import requests
import re
import logging
import threading
from bs4 import BeautifulSoup
from googlesearch import search  # pip install google
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse, urljoin
import os
import time

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.write("Loaded Advanced Scrape Page with Blacklist, Filters, and Stop Option (Threaded)")

# Regex for email validation
EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

# File to store blacklisted URLs
BLACKLIST_FILE = "blacklist.txt"

def load_blacklist():
    """Load blacklisted URLs from file."""
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, "r") as f:
            # Remove whitespace and empty lines
            return set(line.strip() for line in f if line.strip())
    return set()

def update_blacklist(url, blacklist):
    """Add a URL to the blacklist file if not already present."""
    if url not in blacklist:
        with open(BLACKLIST_FILE, "a") as f:
            f.write(url + "\n")
        blacklist.add(url)
        st.info(f"URL added to blacklist: {url}")
        logger.info(f"URL added to blacklist: {url}")

# Load blacklist on startup
if "blacklist" not in st.session_state:
    st.session_state.blacklist = load_blacklist()

blacklist = st.session_state.blacklist

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
        rp.read()
    except Exception as e:
        st.warning(f"Error reading robots.txt from {robots_url}: {e}")
        logger.exception(f"robots.txt error for {robots_url}: {e}")
        return False
    return rp.can_fetch("*", url)

def scrape_emails_from_url(url):
    """Scrape emails from a given URL, if allowed by robots.txt and not blacklisted."""
    emails = set()
    # Skip URL if it is blacklisted
    if url in blacklist:
        st.info(f"Skipping blacklisted URL: {url}")
        return emails
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
    except requests.exceptions.Timeout as e:
        st.warning(f"Timeout fetching {url}: {e}. Adding to blacklist.")
        logger.exception(f"Timeout fetching {url}: {e}")
        update_blacklist(url, blacklist)
    except Exception as e:
        st.warning(f"Error fetching {url}: {e}")
        logger.exception(f"Error fetching {url}: {e}")
    return emails

# Initialize threading-related session state variables
if "scraping_thread" not in st.session_state:
    st.session_state.scraping_thread = None
if "stop_scraping" not in st.session_state:
    st.session_state.stop_scraping = False
if "found_emails" not in st.session_state:
    st.session_state.found_emails = set()

def scraping_worker(final_query, max_urls, num_emails_needed, email_domain_filter):
    results = set()
    try:
        for url in search(final_query, tld="com", lang="en", num=max_urls, stop=max_urls, pause=2):
            # Check for stop flag before processing each URL
            if st.session_state.stop_scraping:
                logger.info("Scraping stopped by user request.")
                break
            st.write(f"Checking: {url}")
            emails = scrape_emails_from_url(url)
            if emails:
                results.update(emails)
            if len(results) >= num_emails_needed:
                break
    except Exception as e:
        st.error(f"An error occurred during the search: {e}")
        logger.exception(f"Search error: {e}")
    # Filter emails by domain if specified
    if email_domain_filter.strip():
        results = {email for email in results if email.endswith(email_domain_filter)}
    st.session_state.found_emails = results

def main():
    st.title("Email Web Scraper - Advanced Version (Threaded Stop Option)")
    st.write(
        """
        This tool will:
        - Perform a Google search based on your query (optionally filtered by country).
        - Check the site's robots.txt to ensure scraping is allowed.
        - Skip URLs that are blacklisted.
        - Automatically add URLs that time out to the blacklist.
        - Allow you to manually add URLs to the blacklist.
        - Scrape pages for emails and filter them by domain.
        - Allow you to stop the scraping process and view the emails found so far.
        """
    )
    
    # Sidebar: Display current blacklist and manual update option
    st.sidebar.subheader("Current Blacklisted URLs")
    if blacklist:
        st.sidebar.write("\n".join(sorted(blacklist)))
    else:
        st.sidebar.write("No URLs blacklisted.")
    
    manual_blacklist = st.sidebar.text_area("Add URLs to blacklist (one per line):")
    if st.sidebar.button("Update Blacklist"):
        if manual_blacklist:
            for url in manual_blacklist.splitlines():
                url = url.strip()
                if url:
                    update_blacklist(url, blacklist)
            st.sidebar.success("Blacklist updated!")
        else:
            st.sidebar.info("No URLs entered.")
    
    # Additional filters: email domain and country filter
    email_domain_filter = st.text_input("Enter email domain filter (e.g. @gmail.com):", "@gmail.com")
    country_filter = st.text_input("Enter country to filter results (e.g. USA):", "")
    
    # User inputs for scraping
    query = st.text_input("Enter your search query:", "contact email")
    num_emails_needed = st.number_input("How many emails do you need?", min_value=1, value=10, step=1)
    max_urls = st.number_input("Maximum number of URLs to scrape:", min_value=1, value=20, step=1)
    
    # Modify query with country filter if provided
    final_query = f"{query} {country_filter}" if country_filter.strip() else query

    # Buttons to start and stop scraping
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Scrape Emails"):
            st.session_state.stop_scraping = False  # Reset stop flag
            st.session_state.found_emails = set()     # Reset results
            # Start scraping in a background thread
            thread = threading.Thread(
                target=scraping_worker,
                args=(final_query, max_urls, num_emails_needed, email_domain_filter),
                daemon=True
            )
            st.session_state.scraping_thread = thread
            thread.start()
    with col2:
        if st.button("Stop Scraping"):
            st.session_state.stop_scraping = True
            st.write("Stop flag set. Waiting for current operation to finish...")
            # Optionally, wait a moment for the thread to finish its current iteration
            if st.session_state.scraping_thread is not None:
                st.session_state.scraping_thread.join(timeout=1)
    
    # Display found emails if available
    if st.session_state.found_emails:
        st.success(f"Found {len(st.session_state.found_emails)} email(s):")
        st.text_area("Emails (copy them below):", value="\n".join(st.session_state.found_emails), height=200)
    else:
        st.info("No emails found yet.")

# Run main unconditionally so that it executes when imported
main()
