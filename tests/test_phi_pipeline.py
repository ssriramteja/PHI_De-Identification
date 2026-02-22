import pytest
import sys
import os

# Ensure src is in the import search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from pipeline import PHIDeidentificationPipeline

@pytest.fixture(scope="module")
def deid_pipeline():
    """ Provides a singleton pipeline instance for testing. """
    return PHIDeidentificationPipeline()

def test_hybrid_deidentification(deid_pipeline):
    """ Verifies that the hybrid pipeline correctly masks various PHI entities. """
    input_text = (
        "Patient: John Smith. DOB: 05/14/1980. "
        "Presented to Memorial Hospital on 2024-03-12. "
        "Contact: (555) 012-3456 or j.smith@provider.net. MRN: 987654321."
    )
    
    # 1. Test Masking Strategy
    mask_result = deid_pipeline.deidentify(input_text, strategy="mask")
    mask_text = mask_result.deidentified_text

    # Verify sensitive data is removed
    sensitive_values = [
        "John Smith", "05/14/1980", "Memorial Hospital", 
        "2024-03-12", "(555) 012-3456", "j.smith@provider.net", "987654321"
    ]
    for value in sensitive_values:
        assert value not in mask_text, f"Sensitive value '{value}' found in de-identified text."

    # Verify tags are present
    expected_tags = ["[NAME]", "[DATE]", "[HOSPITAL]", "[PHONE]", "[EMAIL]", "[MRN]"]
    for tag in expected_tags:
        # Note: Depending on NER/Regex performance, some tags might be missing if detection fails,
        # but for this specific input, they should all be triggered.
        assert tag in mask_text, f"Expected tag '{tag}' missing from de-identified text."

def test_surrogate_strategy(deid_pipeline):
    """ Verifies that the surrogate strategy produces unique, numbered replacement tokens. """
    input_text = "John Smith saw Dr. Jane Doe. Both are located in Boston."
    result = deid_pipeline.deidentify(input_text, strategy="surrogate")
    
    # Check for surrogate pattern [LABEL_NNN]
    assert "[NAME_001]" in result.deidentified_text
    assert "[NAME_002]" in result.deidentified_text
    assert "[LOCATION_001]" in result.deidentified_text

