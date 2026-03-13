import os
import runpy
import streamlit as st
from PIL import Image


def configure_page():
    """Configure Streamlit page and favicon once."""
    favicon_path = os.path.join(os.path.dirname(__file__), "a4644549-5dcd-52fe-8cdf-2733b3e03417.jpg")
    try:
        favicon_img = Image.open(favicon_path)
        st.set_page_config(page_title="Dry Eye Scan", page_icon=favicon_img, layout="wide")
    except Exception:
        # Fallback eye emoji if the image is missing or cannot be opened
        st.set_page_config(page_title="Dry Eye Scan", page_icon="👁️", layout="wide")


def main():
    configure_page()
    prediction_path = os.path.join(os.path.dirname(__file__), "Prediction.py")
    # Execute the main Streamlit app defined in Prediction.py
    runpy.run_path(prediction_path, init_globals={"__name__": "__main__"})


if __name__ == "__main__":
    main()

