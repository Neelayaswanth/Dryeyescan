import os
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Dry Eye Scan", layout="wide")

st.markdown(
    '<h1 style="color:#ffffff;text-align: center;font-size:40px;font-weight:bold;'
    'text-shadow: 2px 2px 8px rgba(0,0,0,0.8);">Dry Eye Scan</h1>',
    unsafe_allow_html=True,
)


def add_custom_bg():
    st.markdown(
        """
        <style>
        .stApp {
            background: radial-gradient(circle at 50% -20%, #1e3c72 0%, #000000 100%);
            background-size: cover;
            background-attachment: fixed;
            color: #e0e0e0;
        }
        .stTextInput>div>div>input {
            background-color: rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 10px;
            padding: 10px;
        }
        .stTextInput>div>div>input::placeholder {
            color: rgba(255, 255, 255, 0.5) !important;
        }
        .stTextInput>label {
            color: #ffffff !important;
        }
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            font-weight: bold;
            padding: 10px;
            background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
            color: #111;
            border: none;
            transition: 0.3s;
            box-shadow: 0 4px 15px rgba(0, 201, 255, 0.4);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 201, 255, 0.6);
            color: #000;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


add_custom_bg()


def main():
    import runpy

    prediction_path = os.path.join(os.path.dirname(__file__), "Prediction.py")
    runpy.run_path(prediction_path, init_globals={"__name__": "prediction_runner"})


if __name__ == "__main__":
    main()
