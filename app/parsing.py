import fitz  # PyMuPDF
import re


SECTION_PATTERN = re.compile(
    r"^(?:\d+\.?\s+)?([A-Z][A-Za-z0-9\s\-]{2,})$"
)


def clean_text(text: str) -> str:
    """
    Cleans raw PDF text.
    - Fixes broken line splits
    - Removes excessive whitespace
    """
    # Fix hyphenated line breaks
    text = re.sub(r"-\n", "", text)

    # Replace single newlines inside paragraphs
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # Normalize multiple newlines
    text = re.sub(r"\n{2,}", "\n\n", text)

    return text.strip()


def detect_section(line: str):
    """
    Detects section headers like:
    - 1 Introduction
    - Abstract
    - METHODS
    """
    line = line.strip()

    match = SECTION_PATTERN.match(line)
    if match:
        return match.group(1)

    return None


def extract_pdf(path: str):
    """
    Extracts structured text from PDF.

    Returns:
        List of dicts:
        [
            {"page": int, "section": str, "text": str}
        ]
    """
    doc = fitz.open(path)
    structured_pages = []

    current_section = "Unknown"

    for page_number, page in enumerate(doc, start=1):
        raw_text = page.get_text("text")

        if not raw_text.strip():
            continue

        cleaned = clean_text(raw_text)

        lines = cleaned.split("\n")
        page_text_lines = []

        for line in lines:
            detected = detect_section(line)
            if detected:
                current_section = detected
                continue

            page_text_lines.append(line)

        page_text = "\n".join(page_text_lines).strip()

        if page_text:
            structured_pages.append({
                "page": page_number,
                "section": current_section,
                "text": page_text
            })

    return structured_pages
