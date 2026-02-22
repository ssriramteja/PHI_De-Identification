import logging
import spacy
from typing import List, Tuple

logger = logging.getLogger(__name__)

Span = Tuple[int, int, str]

class SpacyPHINER:
    """
    Wrapper for spaCy NER model to detect PHI entities.
    """

    def __init__(self, model_name: str = "en_core_web_sm"):
        try:
            self.nlp = spacy.load(model_name)
            logger.info(f"Loaded spaCy model: {model_name}")
        except OSError as e:
            logger.error(f"Failed to load spaCy model '{model_name}': {e}")
            raise RuntimeError(
                f"spaCy model '{model_name}' is not installed. "
                f"Run: python -m spacy download {model_name}"
            )

        # Map spaCy entity labels to standardized PHI labels
        self.label_map = {
            "PERSON": "NAME",
            "ORG":    "HOSPITAL",
            "GPE":    "LOCATION",
            "LOC":    "LOCATION",
        }

    def detect_phi_spans(self, text: str) -> List[Span]:
        """
        Processes text using spaCy NER and maps entities to PHI tags.
        """
        doc = self.nlp(text)
        spans: List[Span] = []

        for ent in doc.ents:
            if ent.label_ in self.label_map:
                phi_label = self.label_map[ent.label_]
                spans.append((ent.start_char, ent.end_char, phi_label))

        logger.debug(f"Detected {len(spans)} NER-based spans.")
        return spans

