import streamlit as st
from books_api import fetch_book
import time
import requests

st.markdown("""
<style>

div[data-testid="stRadio"] label {
    font-size: 20px;
    font-weight: bold;
}

div[data-testid="stSlider"] label {
    font-size: 20px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


st.title("Book Searcher")
st.caption("Find books instantly using the Open Library API 📚")
st.divider()

col1, col2 = st.columns(2)

with col1:
    search_condition = st.radio(
        "Search By",
        ["Author", "Title"]
    )

with col2:
    search_filter = st.slider(
        "Filter No.of Results",
        5, 20
    )

col1, col2 = st.columns([4,1])

with col1:
    user_query = ""
    if search_condition == "Author":
        user_query = st.text_input("Enter name of the Author", placeholder="e.g Charles Dickens")               

    else:
        user_query = st.text_input("Enter the Title of the Book", placeholder="e.g Oliver Twist")


with col2:
    st.write("")
    st.write("")
    search_clicked = st.button("Search")

if search_clicked and user_query.strip():
    time.sleep(1)
    with st.spinner("Fetching books..."):

        data = fetch_book(user_query, search_filter, search_condition)

        if not data:
            st.error("No data to be found!")
            st.stop()
        
        books = data.get('docs', [])

        if not books:
            st.error("❌ No books found for your search query!")
            st.stop()

        st.header(f"📚 Search Results for {user_query.title()}:")

        for i, book in enumerate(books, 1):
                with st.container(border=True):
                    col1, col2 = st.columns([1,3])

                book_title = book.get('title', 'Unknown Title')
                author = book.get('author_name', ['N/A'])[0]
                year = book.get('first_publish_year', 'N/A')


                book_key = book.get('key', 'N/A')

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
                        cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
                    else:
                        cover_edition = book.get('cover_edition_key')
                        if cover_edition:
                            cover_url = f"https://covers.openlibrary.org/b/olid/{cover_edition}-L.jpg"
                        else:
                            cover_url = "No cover available"

                except requests.exceptions.RequestException as e:
                    st.error(f"Error fetching data: {e}")
                

                with col1:
                    st.image(cover_url, width=150)
                
                with col2:
                    st.subheader(f"{i}. {book_title.title()}")
                    st.write("\tAuthor: ", author)
                    st.write("\tFirst Published Year: ", year)

                    with st.expander("Click for Plot"):
                        st.subheader("📖 Plot")
                        st.write(description)

        st.markdown("---")