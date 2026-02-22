import streamlit as st
import sys
import os

# Ensure src is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from pipeline import PHIDeidentificationPipeline

def init_page():
    st.set_page_config(
        page_title="PHI De-identification System",
        layout="wide"
    )
    st.title("PHI De-identification Pipeline")
    st.markdown("""
    This system provides a hybrid approach to clinical text de-identification, 
    combining deterministic rule-based matching with probabilistic Named Entity Recognition (NER).
    """)

@st.cache_resource
def load_pipeline():
    return PHIDeidentificationPipeline()

def main():
    init_page()
    pipeline = load_pipeline()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Source Clinical Data")
        default_text = (
            "John Smith is a 65-year-old male from Boston, MA who presented to UNC Hospital "
            "on 03/12/2024 with chest pain. His phone is (555) 123-4567 and email is "
            "john.smith@example.com. MRN: 1234567."
        )
        text = st.text_area(
            "Input Text:",
            value=default_text,
            height=300,
            label_visibility="collapsed"
        )

        strategy = st.selectbox(
            "Anonymization Strategy",
            options=["mask", "surrogate"],
            index=0,
            format_func=lambda x: "Tag Masking ([LABEL])" if x == "mask" else "Pseudonymization ([LABEL_001])"
        )

        if st.button("Apply De-identification", type="primary"):
            with st.spinner("Processing..."):
                result = pipeline.deidentify(text, strategy=strategy)
                st.session_state["result"] = result

    with col2:
        st.subheader("Processed Output")

        if "result" in st.session_state:
            result = st.session_state["result"]
            st.text_area(
                "De-identified text:",
                value=result.deidentified_text,
                height=300,
                label_visibility="collapsed"
            )

            with st.expander("Detected PHI Entity Details", expanded=True):
                if not result.spans:
                    st.info("No PHI identifiers were detected in the input text.")
                else:
                    for start, end, label in result.spans:
                        st.write(f"**{label}**: `{text[start:end]}` (indices {start}–{end})")
        else:
            st.info("Please input clinical text and run the pipeline to view results.")

if __name__ == "__main__":
    main()

