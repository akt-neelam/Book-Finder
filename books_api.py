import requests
import textwrap

def fetch_book(search_query, limit_filter, search_type):
    """The core logic function for fetching the book details."""
    
    url = "https://openlibrary.org/search.json"

    if search_type == "Author":
        payload={"author": search_query, "limit": limit_filter}

    elif search_type == "Title":
        payload = {"title": search_query, "limit": limit_filter}
    
    else:
        payload = {"q": search_query, "limit": limit_filter}

    try:
        response = requests.get(url, params=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return data
        
    except requests.exceptions.HTTPError:
        if response.status_code == 400:
            print("You sent bad request! Check again.")
            return None

    except requests.exceptions.ConnectionError:
        print("No internet connection!")
        return None

    except requests.exceptions.Timeout:
        print("Request timed out!")
        return None


def display_book_details():
    """From here you can choose any one book by entering its corresponding no. for -
        viewing its description."""
    
    data = fetch_book()

    if not data:
        print("Nothing to be found!")
        return
    
    books = data['docs']

    if not books:
        print("\nNo books found! Check your spelling or try a different search.")
        return

    print("-" * 50)
    print("Your search results:")
    print("-" * 50)

    for i, book in enumerate (books, 1):
        print(f"\n{i}. Book Name: ", book['title'])
        print(f"   Author: ", book.get('author_name', ['N/A'])[0])
        print("   First published year: ", book['first_publish_year'])

    num_results = len(books)


    try:
        choice = int(input(f"\nEnter the book number (1 - {num_results}) to see full details of the book: ").strip())

        if choice < 1 or choice > num_results:
            print(f"Invalid choice! Enter only numericals from 1 and {num_results}.")
            exit()

        selected_book = books[choice - 1]
        book_key = selected_book['key']

        # URL for further details
        url = f"https://openlibrary.org{book_key}.json"

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        details = response.json()

        description = details.get('description', 'No description available')
        if isinstance(description, dict):
            description = description.get('value', 'No description available')

        wrapped_description = textwrap.fill(description, 70)

        # Extracting the selected book's cover page.
        cover_id = selected_book.get('cover_i')
        if cover_id:
            cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
        else:
            cover_edition = selected_book.get('cover_edition_key')
            if cover_edition:
                cover_url = f"https://covers.openlibrary.org/b/olid/{cover_edition}-L.jpg"
            else:
                cover_url = "No cover avilable"

        print("=" * 70)
        print("\nYou selected the following book")
        print("=" * 70)
        print(f"\nTitle: {selected_book.get('title', 'N/A')}")
        print(f"Author: {selected_book.get('author_name', ['N/A'])[0]}")
        print(f"Year: {selected_book.get('first_publish_year')}")
        print(f"Cover URL: {cover_url}")
        print("-" * 70)
        print("\nDescription: ", wrapped_description)

    except (ValueError, IndexError):
        print("Invalid input!")
        exit()
    
    except requests.exceptions.Timeout:
        print("Request timed out!")

if __name__ == "___main__":
    display_book_details()