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
)


#NAVIGATION WITH SECTIONS
pg = st.navigation({
    "ABOUT": [about_page, tutorial_page],
    "SCRAPING": [simple_page, advanced_page],
})

#SHARED ON ALL PAGES
st.logo("static/2.jpg")
st.sidebar.text("Made with ❤ by Dapo\n Advanced Email verification features coming soon...")

#RUN NAVIGATION
pg.run()
