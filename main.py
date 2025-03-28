import streamlit as st

# *** PAGE SETUP ***
about_page = st.Page(
    page = "views/about_me.py",
    title = "About Me",
    icon = "ℹ",
    default = True
)
simple_page = st.Page(
    page = "views/simple_scrape.py",
    title = "SIMPLE SCRAPE",
    icon = "🔍",
)
advanced_page = st.Page(
    page = "views/advanced_scrape.py",
    title = "ADVANCED SCRAPER(RECOMMENDED)",
    icon = "🤖",
)

tutorial_page = st.Page(
    page = "views/tutorial.py",
    title = "TUTORIAL(READ FIRST)",
    icon = "👨‍🏫",
    default = True
)

chat_page = st.Page(
    page = "views/chatbot.py",
    title = "Bot",
    icon = "🤖",
)


#NAVIGATION WITH SECTIONS
pg = st.navigation({
    "INFO": [about_page, tutorial_page, chat_page],
    "SCRAPING": [simple_page, advanced_page],
})

#SHARED ON ALL PAGES
st.logo("static/2.jpg")
st.sidebar.text("Made with ❤ by Dapo\nAdvanced Email verification features coming soon...")

#RUN NAVIGATION
pg.run()
