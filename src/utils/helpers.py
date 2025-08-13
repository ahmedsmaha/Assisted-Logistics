"""Utility Functions Module
This module provides utility functions for data processing and normalization.
It includes functions to normalize order IDs, parse datetime strings,
normalize text, and calculate string similarity. It also includes a function to create
directories if they do not exist."""
import re
from datetime import datetime
import unicodedata


def normalize_order_id(order_id):
    """Normalize order ID by removing non-alphanumeric characters and ensuring a consistent format."""
    # Remove all non-alphanumeric characters and standardize format
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', str(order_id))
    if not cleaned:
        return ""

    # Find the transition between letters and numbers
    i = 0
    while i < len(cleaned) and not cleaned[i].isdigit():
        i += 1

    if i == 0 or i == len(cleaned):
        return cleaned.upper()

    prefix = cleaned[:i].upper()
    suffix = cleaned[i:]
    return f"{prefix}-{suffix}"


def parse_datetime(dt_str):
    """Parse a datetime string into a datetime object.
    Supports multiple formats."""
    # Clean and normalize datetime string
    dt_str = re.sub(r'\s+', ' ', dt_str.strip())

    # Try different formats
    formats = [
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(dt_str, fmt)
        except ValueError:
            continue

    # Fallback for other formats
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError:
        pass

    raise ValueError(f"Unparseable datetime: {dt_str}")


def normalize_text(text):
    """Normalize text by removing non-alphanumeric characters and converting to lowercase."""
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', text).encode(
        'ascii', 'ignore').decode()
    return re.sub(r'\W+', ' ', text).strip().lower()


def calculate_similarity(str1, str2):
    """Calculate the similarity between two strings based on Jaccard index."""
    if not str1 or not str2:
        return 0.0
    set1 = set(str1.split())
    set2 = set(str2.split())
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union else 0.0
