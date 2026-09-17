"""
Download the text of a book from Project Gutenberg in plain text format 
using the public Gutendex API (https://gutendex.com) and save it locally.

Usage:
    python corpus/download_corpus.py <book_id> <output_path>

Example:
    python3 corpus/download_corpus.py 1342 corpus_medium.txt
"""

import sys
import re
import urllib.request
import json


USER_AGENT = "Mozilla/5.0"

def open_url(url):
    """
    Open a URL with a custom User-Agent header to avoid being blocked by the server.

    Args:
        url (str): The URL to open.

    Returns:
        The response from the server.
    """
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(request)


def get_book_metadata(book_id):
    """
    Fetch the metadata of a book from the Gutendex API using its book ID.

    Args:
        book_id (int): The ID of the book to fetch metadata for.

    Returns:
        A dictionary containing the book's metadata.
    """
    url = f"https://gutendex.com/books/{book_id}"
    with open_url(url) as response:
        return json.loads(response.read().decode("utf-8"))


def get_plain_text_url(metadata):
    """
    Get the URL of the plain text version of a book from its metadata.

    Args:
        metadata (dict): A dictionary containing the book's metadata.

    Returns:
        The URL of the plain text version of the book.
    """
    formats = metadata.get("formats", {})
    for key, url in formats.items():
        if key.startswith("text/plain"):
            return url
    raise ValueError("No plain text format available for this book.")   


def get_plain_text_url(metadata):
    """
    Get the URL of the plain text version of a book from its metadata.

    Args:
        metadata (dict): A dictionary containing the book's metadata.

    Returns:
        The URL of the plain text version of the book.
    """
    formats = metadata.get("formats", {})
    for key, url in formats.items():
        if key.startswith("text/plain"):
            return url
    raise ValueError("No plain text format available for this book.")


def strip_gutenberg_boilerplate(text):
    """
    Filter the text to remove the standard header and footer of Project Gutenberg,
    keeping only the main content of the book.

    The texts from Project Gutenberg use markers to delimit the beginning and end
    of the content:
        *** START OF THE PROJECT GUTENBERG EBOOK <TITLE> ***
        *** END OF THE PROJECT GUTENBERG EBOOK <TITLE> ***

    As the text between <TITLE> varies from book to book, the search is done
    by default (regex), not by fixed text.

    If the markers are not found (which can happen in older editions that use 
    a slightly different format), the entire text is kept and a warning is printed, 
    so the user can verify it manually.
    """
    start_pattern = re.compile(r"\*\*\*\s*START OF THE PROJECT GUTENBERG EBOOK.*?\*\*\*", re.IGNORECASE)
    end_pattern = re.compile(r"\*\*\*\s*END OF THE PROJECT GUTENBERG EBOOK.*?\*\*\*", re.IGNORECASE)

    start_match = start_pattern.search(text)
    end_match = end_pattern.search(text)

    if not start_match or not end_match:
        print("Warning: start/end markers for Project Gutenberg not found. " \
            "Keeping the full text, including possible header/footer. " \
            "Please check the file manually.")
        return text

    content = text[start_match.end():end_match.start()]
    return content.strip()


def download_text(url, output_path):
    """
    Download the plain text of a book from a given URL and save it to a 
    specified output path.

    Args:
        url (str): The URL of the plain text version of the book.
        output_path (str): The local file path where the text will be saved.
    """
    with open_url(url) as response:
        text = response.read().decode("utf-8", errors="replace")
        text = strip_gutenberg_boilerplate(text)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 corpus/download_corpus.py <book_id> <output_path>")
        sys.exit(1)

    book_id = sys.argv[1]
    output_path = sys.argv[2]

    print(f"Fetching metadata for book {book_id} via Gutendex...")
    metadata = get_book_metadata(book_id)
    print(f"Book found: {metadata.get('title', 'unknown title')} by {', '.join(author['name'] for author in metadata.get('authors', []))}")

    text_url = get_plain_text_url(metadata)
    print(f"Downloading text from {text_url}...")
    download_text(text_url, output_path)

    print(f"Corpus saved to {output_path}")


if __name__ == "__main__":
    main()