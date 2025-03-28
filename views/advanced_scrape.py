import streamlit as st
import requests
import re
import logging
from bs4 import BeautifulSoup
from googlesearch import search  # pip install google
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse, urljoin
import os

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.write("Loaded Advanced Scrape Page with Blacklist and Filters")

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
blacklist = load_blacklist()

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

def main():
    st.title("Email Web Scraper - Advanced Version (with Persistent Blacklist & Filters)")
    st.write(
        """
        This tool will:
        - Perform a Google search based on your query.
        - Append a country filter to the search (to narrow results by location).
        - Check the site's robots.txt to ensure scraping is allowed.
        - Skip URLs that are blacklisted.
        - Automatically add URLs that time out to the blacklist.
        - Allow you to manually add URLs to the blacklist.
        - Scrape the page for emails.
        - Filter emails by the specified email domain.
        """
    )
    
    # Display current blacklist
    st.sidebar.subheader("Current Blacklisted URLs")
    if blacklist:
        st.sidebar.write("\n".join(sorted(blacklist)))
    else:
        st.sidebar.write("No URLs blacklisted.")
    
    # Allow user to add URLs to the blacklist manually
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
    
    # Additional filters
    email_domain_filter = st.text_input("Enter email domain filter (e.g. @gmail.com):", "@gmail.com")
    country_filter = st.text_input("Enter country to filter results (e.g. USA):", "")
    
    # User inputs for scraping
    query = st.text_input("Enter your search query:", "contact email")
    num_emails_needed = st.number_input("How many emails do you need?", min_value=1, value=10, step=1)
    max_urls = st.number_input("Maximum number of URLs to scrape:", min_value=1, value=20, step=1)
    
    # Modify query with country filter if provided
    final_query = f"{query} {country_filter}" if country_filter.strip() else query
    
    if st.button("Scrape Emails"):
        found_emails = set()
        st.info("Searching and scraping emails... please wait.")
        
        try:
            # 'num' sets how many results per page, 'stop' sets the total number of results to fetch.
            for url in search(final_query, tld="com", lang="en", num=max_urls, stop=max_urls, pause=2):
                st.write(f"Checking: {url}")
                emails = scrape_emails_from_url(url)
                if emails:
                    found_emails.update(emails)
                if len(found_emails) >= num_emails_needed:
                    break
        except Exception as e:
            st.error(f"An error occurred during the search: {e}")
            logger.exception(f"Search error: {e}")
        
        # Filter emails by domain if specified
        if email_domain_filter.strip():
            found_emails = {email for email in found_emails if email.endswith(email_domain_filter)}
        
        # Limit emails to the user requested number
        found_emails = list(found_emails)[:num_emails_needed]
        
        if found_emails:
            st.success(f"Found {len(found_emails)} email(s):")
            st.text_area("Emails (copy them below):", value="\n".join(found_emails), height=200)
        else:
            st.info("No emails found. Try a different query or adjust parameters.")

# Run main unconditionally so that it executes when imported
main()

