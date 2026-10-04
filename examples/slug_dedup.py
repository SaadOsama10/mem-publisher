"""Illustration: pick a slug that WordPress doesn't suffix with -2, -3, ...

`set_slug` stands in for the browser step that types a slug into the editor and
returns the slug WordPress actually kept. Not the production implementation.
"""
import re
from typing import Callable, Iterable


def suffix_count(slug: str) -> int:
    match = re.search(r"-(\d+)$", slug)
    return int(match.group(1)) if match else 0


def pick_unique_slug(set_slug: Callable[[str], str], focus_keyword: str,
                     alternatives: Iterable[str], max_tries: int = 10) -> str:
    """Try the focus keyword first, then alternatives, keeping the best result."""
    best = set_slug(focus_keyword)
    if suffix_count(best) == 0:
        return best
    for tries, candidate in enumerate(alternatives, start=1):
        if tries > max_tries:
            break
        slug = set_slug(candidate)
        if suffix_count(slug) == 0:
            return slug
        if suffix_count(slug) < suffix_count(best):
            best = slug
    return set_slug(focus_keyword) if best == focus_keyword else best
