import streamlit as st
from books_api import fetch_book


st.title("Book Searcher")
st.divider()

search_condition = st.radio(
    "Search By",
    ["Author", "Title"]
)

search_filter = st.slider(
    "Filter nunmber of resultes",
    5, 20
)

user_query = ""
if search_condition == "Author":
    user_query = st.text_input("Enter name of the Author", placeholder="e.g Charles Dickens")               

elif search_condition == "Title":
    user_query = st.text_input("Enter the Title of the Book", placeholder="e.g Oliver Twist")


if user_query.strip():

    if st.button("Search"):
        with st.spinner("Fetching books..."):

            data = fetch_book(user_query, search_filter, search_condition)

        if not data:
            st.error("No data to be found!")
            st.stop()
        
        books = data.get('docs', [])

        if not books:
            st.error("No books found for your search query!")
            st.stop()

        st.header(f"Search Results for {search_condition.title()}:")

        for i, book in enumerate(books, 1):
            st.subheader(f"{i}. Book Name: {book['title'].title()}")
            st.write("Author: ", book.get('author_name', ['N/A'])[0])
            st.write("First Published Year: ", book['first_publish_year'])

            st.divider()