from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .files import list_ticket_file_paths
from .tickets import list_ticket_numbers
from .word import read_docx_text


TEXT_EXTENSIONS = {
    ".css",
    ".csv",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
SNIPPET_CONTEXT = 90
MAX_RESULTS = 30


@dataclass(frozen=True)
class SearchResult:
    ticket_number: int
    path: Path
    snippet: str

    @property
    def filename(self) -> str:
        return self.path.name


def search_tickets(query: str, limit: int = MAX_RESULTS) -> tuple[SearchResult, ...]:
    normalized_query = normalize_search_text(query)
    if not normalized_query:
        return ()

    results: list[SearchResult] = []
    for ticket_number in list_ticket_numbers():
        for path in list_ticket_file_paths(ticket_number):
            text = read_searchable_text(path)
            if not text:
                continue
            if matches_query(text, query, normalized_query):
                results.append(
                    SearchResult(
                        ticket_number=ticket_number,
                        path=path,
                        snippet=make_snippet(text, query, normalized_query),
                    )
                )
                if len(results) >= limit:
                    return tuple(results)

    return tuple(results)


def read_searchable_text(path: Path) -> str | None:
    suffix = path.suffix.casefold()
    if suffix == ".docx":
        try:
            return read_docx_text(path)
        except Exception:
            return None

    if suffix not in TEXT_EXTENSIONS:
        return None

    for encoding in ("utf-8-sig", "utf-8", "cp1251"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
        except OSError:
            return None

    return None


def normalize_search_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


def search_terms(text: str) -> tuple[str, ...]:
    return tuple(re.findall(r"[0-9a-zа-яё]+", text.casefold()))


def matches_query(text: str, query: str, normalized_query: str) -> bool:
    normalized_text = normalize_search_text(text)
    if normalized_query in normalized_text:
        return True

    terms = search_terms(query)
    if len(terms) < 2:
        return False

    text_terms = set(search_terms(text))
    return all(term in text_terms for term in terms)


def make_snippet(text: str, query: str, normalized_query: str) -> str:
    compact_text = re.sub(r"\s+", " ", text).strip()
    haystack = compact_text.casefold()
    position = haystack.find(normalized_query)
    match_length = len(normalized_query)
    if position < 0:
        for term in search_terms(query):
            position = haystack.find(term)
            if position >= 0:
                match_length = len(term)
                break
    if position < 0:
        return compact_text[: SNIPPET_CONTEXT * 2].strip()

    start = max(0, position - SNIPPET_CONTEXT)
    end = min(len(compact_text), position + match_length + SNIPPET_CONTEXT)
    prefix = "..." if start else ""
    suffix = "..." if end < len(compact_text) else ""
    return f"{prefix}{compact_text[start:end].strip()}{suffix}"


def format_search_results(query: str, results: tuple[SearchResult, ...]) -> str:
    if not results:
        return f'Ничего не найдено по запросу: "{query}"'

    lines = [f'Найдено совпадений по запросу "{query}": {len(results)}', ""]
    for index, result in enumerate(results, start=1):
        lines.append(f"{index}. Билет {result.ticket_number}: {result.filename}")
        lines.append(f"   {result.snippet}")
        lines.append(f"   Читать: ist-ticket {result.ticket_number}")
        lines.append(f"   Открыть файлы: ist-ticket open {result.ticket_number}")
        if index != len(results):
            lines.append("")
    return "\n".join(lines)
