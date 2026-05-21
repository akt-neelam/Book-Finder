import streamlit as st
from books_api import fetch_book

st.title("Book Searcher")
st.divider()

search_condition = st.radio(
    "Search By",
    ["Author", "Title"]
)

if search_condition == "Author":
    st.text_input("Enter name of the Author", placeholder="e.g Charles Dickens")

elif search_condition == "Title":
    st.text_input("Enter the Title of the Book", placeholder="e.g Oliver Twist")


