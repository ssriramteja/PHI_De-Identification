import argparse
import logging
import sys

from pipeline import PHIDeidentificationPipeline

def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stderr
    )

def main():
    parser = argparse.ArgumentParser(description="PHI De-identification Pipeline CLI")
    parser.add_argument(
        "--text", 
        type=str, 
        help="Input text to de-identify. If omitted, a sample will be used."
    )
    parser.add_argument(
        "--strategy", 
        choices=["mask", "surrogate"], 
        default="mask",
        help="Masking strategy (default: mask)"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Enable verbose logging"
    )

    args = parser.parse_args()
    setup_logging(args.verbose)

    sample_text = args.text or (
        "John Smith is a 65-year-old male from Boston, MA who presented "
        "to UNC Hospital on 03/12/2024. His phone is (555) 123-4567 and "
        "email is john.smith@example.com. MRN: 1234567."
    )

    pipeline = PHIDeidentificationPipeline()
    result = pipeline.deidentify(sample_text, strategy=args.strategy)

    print("-" * 20)
    print("ORIGINAL TEXT:")
    print("-" * 20)
    print(sample_text)
    print("\n" + "-" * 20)
    print("DE-IDENTIFIED TEXT:")
    print("-" * 20)
    print(result.deidentified_text)
    print("\n" + "-" * 20)
    print("DETECTED SPANS:")
    print("-" * 20)
    for start, end, label in result.spans:
        print(f"[{label}] at {start}:{end} -> '{sample_text[start:end]}'")

if __name__ == "__main__":
    main()
