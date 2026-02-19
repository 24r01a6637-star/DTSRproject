from typing import List, Dict


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50):
    """
    Splits text into overlapping chunks.

    chunk_size = number of words
    overlap = overlapping words between chunks
    """

    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))

        start += chunk_size - overlap

    return chunks


def chunk_pages(structured_pages: List[Dict]):
    """
    Takes output from parsing.py and returns chunked documents.
    """

    all_chunks = []

    for page_data in structured_pages:
        text = page_data["text"]
        page = page_data["page"]
        section = page_data["section"]

        text_chunks = chunk_text(text)

        for chunk in text_chunks:
            all_chunks.append({
                "text": chunk,
                "page": page,
                "section": section
            })

    return all_chunks
