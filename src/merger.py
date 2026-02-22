import logging
from dataclasses import dataclass
from typing import List, Tuple, Dict

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class PHISpan:
    start: int
    end: int
    label: str
    source: str = "UNKNOWN"

def merge_spans(rule_spans: List[Tuple[int, int, str]], 
                ner_spans: List[Tuple[int, int, str]]) -> List[Tuple[int, int, str]]:
    """
    Merges rule-based and NER-based spans, resolving overlaps.
    Overlaps are resolved by prioritizing rule-based spans for higher precision.
    """
    
    # Convert to internal PHISpan representation for processing
    all_spans = [PHISpan(*s, source="RULE") for s in rule_spans] + \
                [PHISpan(*s, source="NER")  for s in ner_spans]

    # Sort by start position, then end position
    all_spans.sort(key=lambda x: (x.start, x.end))

    merged_internal: List[PHISpan] = []
    
    for current in all_spans:
        if not merged_internal:
            merged_internal.append(current)
            continue

        previous = merged_internal[-1]

        # Check for overlap
        if current.start >= previous.end:
            # No overlap
            merged_internal.append(current)
        else:
            # Overlap detected: prioritize RULE source
            if current.source == "RULE" and previous.source != "RULE":
                merged_internal[-1] = current
            elif previous.source == "RULE":
                # Keep previous if it's RULE
                continue
            else:
                # Both are NER, keep the more expansive one or the first one
                if current.end > previous.end:
                     merged_internal[-1] = current

    # Return as original Tuple format for compatibility
    return [(s.start, s.end, s.label) for s in merged_internal]


def apply_spans(text: str, spans: List[Tuple[int, int, str]], strategy: str = "mask") -> str:
    """
    Applies de-identification spans to the text using the specified strategy.
    
    Strategies:
        'mask': Replaces PHI with generic [LABEL] tags.
        'surrogate': Replaces PHI with numbered [LABEL_NNN] surrogates.
    """
    if not spans:
        return text

    # Ensure spans are sorted
    sorted_spans = sorted(spans, key=lambda x: x[0])
    
    output = []
    last_idx = 0
    counters: Dict[str, int] = {}

    for start, end, label in sorted_spans:
        # Append preceding non-PHI text
        if start > last_idx:
            output.append(text[last_idx:start])

        if strategy == "mask":
            replacement = f"[{label}]"
        else:
            counters[label] = counters.get(label, 0) + 1
            replacement = f"[{label}_{counters[label]:03d}]"

        output.append(replacement)
        last_idx = end

    # Append remaining text
    if last_idx < len(text):
        output.append(text[last_idx:])

    return "".join(output)

