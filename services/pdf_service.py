import re
from collections import Counter

from pypdf import PdfReader


def clean_page_text(text: str):
    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if re.fullmatch(
            r"Page\s+\d+",
            line,
            re.IGNORECASE
        ):
            continue

        cleaned_lines.append(line)

    return cleaned_lines


def extract_text_from_pdf(file_path: str):
    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            cleaned_lines = clean_page_text(
                page_text
            )

            pages.append(cleaned_lines)


    first_lines = [
        page[0]
        for page in pages
        if page
    ]

    line_counts = Counter(first_lines)

    repeated_headers = {
        line
        for line, count in line_counts.items()
        if count >= 2
    }

    cleaned_pages = []

    for page in pages:

        if (
            page
            and page[0] in repeated_headers
        ):
            page = page[1:]

        cleaned_pages.append(
            "\n".join(page)
        )

    # --------------------------------
    # 4. Combine all pages
    # --------------------------------

    return "\n\n".join(cleaned_pages)