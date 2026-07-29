"""
Word, Character & Sentence Counter
------------------------------------
Analyzes a text file (or pasted text) and reports counts for characters,
words, sentences, lines, and paragraphs, plus the most frequently used
words.

Usage:
    python text_counter.py path/to/file.txt
    python text_counter.py            # prompts you to paste text instead
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from dataclasses import dataclass

# Basic English stopwords to exclude from the "most common words" list,
# since otherwise "the", "a", "is" etc. would dominate every result.
STOPWORDS: set[str] = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "and", "or", "but", "if", "then", "so", "to", "of", "in", "on", "for",
    "with", "at", "by", "from", "as", "it", "its", "this", "that", "these",
    "those", "i", "you", "he", "she", "we", "they", "his", "her", "their",
    "our", "your", "my", "not", "no", "do", "does", "did", "have", "has",
    "had",
}

WORD_PATTERN = re.compile(r"[A-Za-z']+")
SENTENCE_END_PATTERN = re.compile(r"[.!?]+(?:\s|$)")


@dataclass
class TextStats:
    characters_with_spaces: int
    characters_without_spaces: int
    words: int
    sentences: int
    lines: int
    paragraphs: int
    most_common_words: list[tuple[str, int]]


def analyze(text: str, top_n: int = 5) -> TextStats:
    lines = text.splitlines()
    non_blank_lines = [line for line in lines if line.strip()]

    # Paragraphs are chunks of text separated by one or more blank lines.
    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]

    words = WORD_PATTERN.findall(text)

    sentence_matches = SENTENCE_END_PATTERN.findall(text)
    sentence_count = len(sentence_matches)
    # If the text has content but doesn't end with sentence-ending
    # punctuation, count the trailing fragment as one more sentence.
    stripped_text = text.strip()
    if stripped_text and not re.search(r"[.!?]$", stripped_text):
        sentence_count += 1

    word_counts = Counter(word.lower() for word in words if word.lower() not in STOPWORDS)

    return TextStats(
        characters_with_spaces=len(text),
        characters_without_spaces=len(text.replace(" ", "").replace("\n", "").replace("\t", "")),
        words=len(words),
        sentences=max(sentence_count, 1) if words else 0,
        lines=len(non_blank_lines),
        paragraphs=len(paragraphs) if paragraphs else (1 if text.strip() else 0),
        most_common_words=word_counts.most_common(top_n),
    )


def print_report(stats: TextStats) -> None:
    print("\n--- Text Statistics ---")
    print(f"Characters (with spaces):    {stats.characters_with_spaces}")
    print(f"Characters (without spaces): {stats.characters_without_spaces}")
    print(f"Words:                       {stats.words}")
    print(f"Sentences:                   {stats.sentences}")
    print(f"Lines (non-blank):           {stats.lines}")
    print(f"Paragraphs:                  {stats.paragraphs}")

    if stats.most_common_words:
        print("\nMost common words (excluding common stopwords):")
        for word, count in stats.most_common_words:
            print(f"  {word:<15} {count}")


def read_text_from_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def read_text_from_stdin() -> str:
    print("Paste or type your text below.")
    print("When finished, press Enter then Ctrl+D (Linux/Mac) or Ctrl+Z then Enter (Windows):\n")
    return sys.stdin.read()


def main() -> None:
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            text = read_text_from_file(file_path)
        except FileNotFoundError:
            print(f"Error: file not found: {file_path}")
            return
        except OSError as error:
            print(f"Error reading file: {error}")
            return
    else:
        text = read_text_from_stdin()

    if not text.strip():
        print("No text to analyze.")
        return

    stats = analyze(text)
    print_report(stats)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")