import requests
import textwrap

def fetch_book():
    """From here you can search for books either by Author name or by Book title.
    You can filter out how many results you want by entering your desired number.
    Its results are then passed to the next function where you can select the book you want."""
    
    url = "https://openlibrary.org/search.json"

    confirmation = input("\nDo you want to search by the book name or author? \n(Enter 'B' for book or 'A' for author)\n").strip().lower()
    if confirmation == 'b':
        title = input("\nEnter BOOK name: ")
        limit_filter = int(input("\nHow many results would you want to see? ".strip()))
        params = {"q": title, "limit": limit_filter}

    elif confirmation == 'a':
        author_name = input("\nEnter AUTHOR name: ")
        limit_filter = int(input("\nHow many results would you want to see? ").strip())
        params = {"q": author_name, "limit": limit_filter}

    else:
        print("Book or Author!!")
        exit()

    try:
        response = requests.get(url, params=params, timeout=10)
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