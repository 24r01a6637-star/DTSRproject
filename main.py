from app.parsing import extract_pdf
from app.chunking import chunk_pages

# Step 1: Parse
structured_pages = extract_pdf("paper.pdf")

# Step 2: Chunk
chunks = chunk_pages(structured_pages)

print(f"Total chunks: {len(chunks)}")
