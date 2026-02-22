import re
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)

Span = Tuple[int, int, str]  # (start, end, label)

# Precompiled regex patterns for PHI-like entities
DATE_PATTERN = re.compile(
    r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"   # MM/DD/YYYY or M-D-YY
    r"|\d{4}[/-]\d{1,2}[/-]\d{1,2})\b"      # YYYY-MM-DD
)

PHONE_PATTERN = re.compile(
    r"(\+?\d{1,2}[-\s]?)?(\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4})"
)

EMAIL_PATTERN = re.compile(
    r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
)

MRN_PATTERN = re.compile(
    r"\b(MRN[:\s]*\w+|\b\d{7,10}\b|[A-Z]\d{3}-\d{2}-\d{4})"
)

ID_PATTERN = re.compile(
    r"\b(SSN[:\s]*\d{3}-\d{2}-\d{4})\b"
)


def find_dates(text: str) -> List[Span]:
    return [(m.start(), m.end(), "DATE") for m in DATE_PATTERN.finditer(text)]


def find_phones(text: str) -> List[Span]:
    return [(m.start(), m.end(), "PHONE") for m in PHONE_PATTERN.finditer(text)]


def find_emails(text: str) -> List[Span]:
    return [(m.start(), m.end(), "EMAIL") for m in EMAIL_PATTERN.finditer(text)]


def find_mrn(text: str) -> List[Span]:
    return [(m.start(), m.end(), "MRN") for m in MRN_PATTERN.finditer(text)]


def find_ids(text: str) -> List[Span]:
    return [(m.start(), m.end(), "ID") for m in ID_PATTERN.finditer(text)]


def rule_based_spans(text: str) -> List[Span]:
    """
    Aggregate all regex-based PHI detections from the input text.
    """
    spans: List[Span] = []
    spans.extend(find_dates(text))
    spans.extend(find_phones(text))
    spans.extend(find_emails(text))
    spans.extend(find_mrn(text))
    spans.extend(find_ids(text))
    
    logger.debug(f"Found {len(spans)} rule-based spans.")
    return spans

