"""Illustration: keep article paragraphs inside a word range.

Simplified sample for this showcase, not the production implementation.
"""
import re


def split_long_paragraph(paragraph: str, max_words: int) -> list[str]:
    """Split on sentence boundaries so no chunk exceeds max_words (when possible)."""
    sentences = re.split(r"(?<=[.!?؟])\s+", paragraph.strip())
    chunks, current = [], []
    for sentence in sentences:
        words = sentence.split()
        if current and len(" ".join(current).split()) + len(words) > max_words:
            chunks.append(" ".join(current))
            current = []
        current.append(sentence)
    if current:
        chunks.append(" ".join(current))
    return chunks


def enforce_paragraph_length(body: str, min_words: int = 25, max_words: int = 35) -> str:
    out: list[str] = []
    for paragraph in filter(None, (p.strip() for p in body.split("\n\n"))):
        for chunk in split_long_paragraph(paragraph, max_words):
            # merge a too-short chunk into the previous paragraph if it still fits
            if out and len(chunk.split()) < min_words and len((out[-1] + " " + chunk).split()) <= max_words + min_words:
                out[-1] += " " + chunk
            else:
                out.append(chunk)
    return "\n\n".join(out)
