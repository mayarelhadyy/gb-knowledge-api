import re


def split_large_text(
    text: str,
    max_chunk_size: int = 700
):
    """
    Split large text into smaller chunks
    without cutting sentences when possible.
    """

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:

            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence

        else:

            if current_chunk:
                chunks.append(current_chunk.strip())

            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def chunk_text(
    text: str,
    max_chunk_size: int = 700
):
    """
    Split a document using numbered sections when available.

    Example:
    1. Purpose & Scope
    2. Core Principles
    3. Working Hours & Attendance
    """

    section_pattern = r'(?m)(?=^\d+\.\s+)'

    sections = re.split(
        section_pattern,
        text
    )

    sections = [
        section.strip()
        for section in sections
        if section.strip()
    ]

    chunks = []

    for section in sections:

        if len(section) <= max_chunk_size:
            chunks.append(section)

        else:
            smaller_chunks = split_large_text(
                section,
                max_chunk_size
            )

            chunks.extend(smaller_chunks)

    return chunks
