import streamlit as st
from books_api import fetch_book
import time
import requests

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
            time.sleep(3)

            data = fetch_book(user_query, search_filter, search_condition)

        if not data:
            st.error("No data to be found!")
            st.stop()
        
        books = data.get('docs', [])

        if not books:
            st.error("No books found for your search query!")
            st.stop()

        st.header(f"Search Results for {user_query.title()}:")

        for i, book in enumerate(books, 1):
            st.subheader(f"{i}. {book['title'].title()}")
            st.write("\tAuthor: ", book.get('author_name', ['N/A'])[0])
            st.write("\tFirst Published Year: ", book['first_publish_year'])

            book_key = book['key']

            url = f"https://openlibrary.org{book_key}.json"

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                details = response.json()
                
                # To get the plot of the book
                description = details.get('description', 'No description available')
                if isinstance(description, dict):
                    description = description.get('value', 'No description available')
                
                # To get the cover page of the book
                cover_id = book.get('cover_i')
                if cover_id:
                    cover_url = f"https://covers.openlibrary.org/b/id{cover_id}-L.jpg"
                else:
                    cover_edition = book.get('cover_edition_key')
                    if cover_edition:
                        cover_url = f"https://covers.openlibrary.org/b/olid/{cover_edition}-L.jpg"
                    else:
                        cover_url = "No cover available"

            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching data: {e}")
            
            if st.button("Click for more details"):
                st.subheader("Plot")
                st.write(description)

                st.subheader("Cover Image URL")
                st.write(cover_url)
            st.divider()