import logging
from dataclasses import dataclass
from typing import List, Tuple

from rules import rule_based_spans
from ner_model import SpacyPHINER
from merger import merge_spans, apply_spans

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class DeidResult:
    """
    Container for de-identification results.
    """
    original_text: str
    deidentified_text: str
    spans: List[Tuple[int, int, str]]


class PHIDeidentificationPipeline:
    """
    Hybrid PHI de-identification pipeline combining rule-based heuristics
    and Named Entity Recognition (NER).
    """

    def __init__(self, model_name: str = "en_core_web_sm"):
        """
        Initializes the pipeline with a specified spaCy model.
        """
        self.ner = SpacyPHINER(model_name=model_name)
        logger.info("PHIDeidentificationPipeline initialized.")

    def deidentify(
        self,
        text: str,
        strategy: str = "mask"
    ) -> DeidResult:
        """
        Executes the de-identification process on the input text.
        
        Args:
            text: The raw clinical text to process.
            strategy: The masking strategy ('mask' or 'surrogate').
            
        Returns:
            A DeidResult object containing the de-identified text and detected spans.
        """
        logger.info(f"Processing text of length {len(text)} with strategy: {strategy}")
        
        # 1. Extract spans from regex rules
        rule_spans = rule_based_spans(text)

        # 2. Extract spans from NER model
        ner_spans = self.ner.detect_phi_spans(text)

        # 3. Merge overlapping spans and resolve conflicts
        merged_spans = merge_spans(rule_spans, ner_spans)

        # 4. Apply the chosen masking strategy
        deidentified_text = apply_spans(text, merged_spans, strategy=strategy)

        return DeidResult(
            original_text    = text,
            deidentified_text= deidentified_text,
            spans            = merged_spans
        )

