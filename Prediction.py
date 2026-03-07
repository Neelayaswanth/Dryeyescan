#======================== IMPORT PACKAGES ===========================

import numpy as np
import matplotlib.pyplot as plt 
import cv2
import streamlit as st
import base64
from streamlit_option_menu import option_menu
import pickle
from sklearn.model_selection import train_test_split
from PIL import Image
import matplotlib.image as mpimg
import pandas as pd
import time
import os
import tensorflow as tf

# --- CACHED MODEL TRAINING ---
@st.cache_resource
def train_mlp_model():
    from sklearn import preprocessing
    from sklearn.neural_network import MLPClassifier

    dataframe = pd.read_excel("Dataset.xlsx")
    dataframe = dataframe.fillna(0)
    dataframe = dataframe.drop(['Timestamp', 'Consent', 'Academic Year'], axis=1)

    encoders = {}
    categorical_cols = [
        'Gender', 'What type of Digital display device do you use?',
        'How many hours in a day do you spend on your smartphones, laptops, etc?',
        'Eyes that are sensitive to light?', 'Eyes that feel gritty (itchy and Scratchy) ?',
        'Painful or Sore eyes?', 'Blurred vision?', 'Reading?', 'Driving at night?',
        'Working with a computer or bank machine ATM?', 'Watching TV?',
        'Windy conditions?', 'Places or areas with low humidity (very dry)?',
        'Areas that are air-conditioned?', 'Poor Vision?', 'Results'
    ]
    for col in categorical_cols:
        if col in dataframe.columns:
            le = preprocessing.LabelEncoder()
            dataframe[col] = le.fit_transform(dataframe[col].astype(str))
            encoders[col] = le

    X = dataframe.drop('Results', axis=1)
    y = dataframe['Results']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    mlpp = MLPClassifier()
    mlpp.fit(X_train, y_train)
    return mlpp, encoders

def show_prediction():
    selected = option_menu(
        menu_title=None, 
        options=["Dry Eye Prediction", "Eye Disease Prediction", "Eye Blink Detection"],  
        orientation="horizontal",
        styles={
            "container": {"padding": "5px!important", "background-color": "rgba(255,255,255,0.05)", "border-radius": "10px", "border": "1px solid rgba(255,255,255,0.1)", "margin-bottom": "20px", "display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "5px"},
            "icon": {"color": "#00C9FF", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0", "--hover-color": "rgba(255,255,255,0.1)", "color": "#e0e0e0", "transition": "0.3s", "white-space": "nowrap", "width": "100%", "padding": "10px 0"},
            "nav-link-selected": {"background": "linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%)", "color": "#111", "font-weight": "bold", "box-shadow": "0 4px 15px rgba(0, 201, 255, 0.4)", "white-space": "nowrap", "width": "100%", "padding": "10px 0"},
        }
    )

    if selected == 'Dry Eye Prediction':
        show_dry_eye_prediction()
    elif selected == 'Eye Disease Prediction':
        show_eye_disease_prediction()
    elif selected == 'Eye Blink Detection':
        show_eye_blink_detection()

def show_dry_eye_prediction():
    st.markdown(f'<h1 style="color:#00C9FF;text-align: center;font-size:32px;text-shadow: 2px 2px 5px rgba(0,0,0,0.5);">{"Interactive Dry Eye Scan"}</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ccc; margin-bottom: 30px;'>Please answer the following questionnaire to immediately assess your Dry Eye Risk.</p>", unsafe_allow_html=True)
    
    with st.spinner("Initializing Prediction Engine..."):
        mlpp, encoders = train_mlp_model()

    with st.form("dry_eye_questionnaire"):
        st.markdown(f'<h3 style="color:#92FE9D;">Basic Information</h3>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            q_age = st.number_input("Age", min_value=10, max_value=100, value=20)
        with col2:
            q_gender = st.selectbox("Gender", ["Female", "Male"])
            
        st.markdown(f'<h3 style="color:#92FE9D; margin-top:20px;">Screen Exposure</h3>', unsafe_allow_html=True)
        q_device = st.selectbox("What type of Digital display device do you use?", [
            'Smartphone, Tablet, Television', 'Smartphone', 'Smartphone, Laptop', 
            'Smartphone, Television', 'Smartphone, Laptop, Tablet, Television', 
            'Others', 'Laptop', 'Laptop, Television', 'Smartphone, Tablet', 
            'Smartphone, Laptop, Computer, Tablet, Television', 'Smartphone, Laptop, Television'
        ])
        q_hours = st.selectbox("How many hours in a day do you spend on screens?", [
            '3-5', '5-8', '>8', '1-3', '<1'
        ])
        
        st.markdown(f'<h3 style="color:#92FE9D; margin-top:20px;">Symptom History (Frequency)</h3>', unsafe_allow_html=True)
        freq_options = ['None of the time', 'some times', 'half of the times', 'most of the times', 'all the time']
        
        q_sensitive = st.selectbox("Eyes that are sensitive to light?", freq_options)
        q_gritty = st.selectbox("Eyes that feel gritty (itchy and Scratchy) ?", freq_options)
        q_painful = st.selectbox("Painful or Sore eyes?", freq_options)
        q_blurred = st.selectbox("Blurred vision?", freq_options)
        q_poorvision = st.selectbox("Poor Vision?", freq_options)
        q_osdi = st.number_input("OSDI Score (if known, else 0)", min_value=0.0, max_value=100.0, value=0.0)
        
        st.markdown(f'<h3 style="color:#92FE9D; margin-top:20px;">Environmental Triggers (Frequency)</h3>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            q_reading = st.selectbox("Reading?", freq_options)
            q_driving = st.selectbox("Driving at night?", freq_options)
            q_computer = st.selectbox("Working with a computer or ATM?", freq_options)
        with col2:
            q_tv = st.selectbox("Watching TV?", freq_options)
            q_windy = st.selectbox("Windy conditions?", freq_options)
            
        q_humidity = st.selectbox("Places or areas with low humidity (very dry)?", freq_options)
        q_ac = st.selectbox("Areas that are air-conditioned?", freq_options)
        
        st.write("")
        submit_btn = st.form_submit_button("Predict Dry Eye Risk", use_container_width=True)
        
    if submit_btn:
        st.write("-----------------------------------------------------------")
        st.markdown(f'<h1 style="color:#00C9FF;text-align: center;font-size:26px;text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">{"Your Custom Prediction"}</h1>', unsafe_allow_html=True)
        
        try:
            def safe_encode(col_name, val):
                le = encoders[col_name]
                if str(val) in le.classes_:
                    return le.transform([str(val)])[0]
                else:
                    return 0
                    
            user_data = [
                float(q_age),
                safe_encode('Gender', q_gender),
                safe_encode('What type of Digital display device do you use?', q_device),
                safe_encode('How many hours in a day do you spend on your smartphones, laptops, etc?', q_hours),
                safe_encode('Eyes that are sensitive to light?', q_sensitive),
                safe_encode('Eyes that feel gritty (itchy and Scratchy) ?', q_gritty),
                safe_encode('Painful or Sore eyes?', q_painful),
                safe_encode('Blurred vision?', q_blurred),
                safe_encode('Poor Vision?', q_poorvision),
                safe_encode('Reading?', q_reading),
                safe_encode('Driving at night?', q_driving),
                safe_encode('Working with a computer or bank machine ATM?', q_computer),
                safe_encode('Watching TV?', q_tv),
                safe_encode('Windy conditions?', q_windy),
                safe_encode('Places or areas with low humidity (very dry)?', q_humidity),
                safe_encode('Areas that are air-conditioned?', q_ac),
                float(q_osdi)
            ]
            
            user_array = np.array([user_data])
            raw_prediction = mlpp.predict(user_array)[0]
            
            if raw_prediction == 0:
                result_text = "MILD STAGE"
                color = "#FFD700"
            elif raw_prediction == 1:
                result_text = "MODERATE STAGE"
                color = "#FFA500"
            elif raw_prediction == 2:
                result_text = "NORMAL"
                color = "#92FE9D"
            else:
                result_text = "SEVERE STAGE"
                color = "#FF4500"
                
            st.markdown(f'<div style="background-color: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; border: 2px solid {color}; text-align: center;">'
                        f'<h2 style="color: {color}; margin:0; text-shadow: 1px 1px 5px rgba(0,0,0,0.8);">{result_text}</h2>'
                        f'<p style="color: #fff; margin-top: 10px;">Based on your responses, this is your estimated Dry Eye risk profile.</p>'
                        f'</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Prediction Error: {e}")

def show_eye_disease_prediction():
    st.markdown(f'<h1 style="color:#00C9FF;text-align: center;font-size:26px;text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">{"Eye Disease Prediction"}</h1>', unsafe_allow_html=True)
    source_choice = st.radio("Select Image Source:", ["Upload", "Camera"], horizontal=True, key="disease_source")
    
    if source_choice == "Upload":
        filename = st.file_uploader("Choose Image", ['jpg','png'], key="disease_upload")
    else:
        filename = st.camera_input("Take a Photo", key="disease_camera")

    if filename is not None:
        img = mpimg.imread(filename)
        st.image(img, caption="Original Image")
        # Simplified prediction logic (reconstruct full logic if needed)
        st.success("Image received for disease prediction.")

def show_eye_blink_detection():
    st.markdown(f'<h1 style="color:#00C9FF;text-align: center;font-size:26px;text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">{"Eye Blink Detection"}</h1>', unsafe_allow_html=True)
    source_choice = st.radio("Select Image Source:", ["Upload", "Camera"], horizontal=True, key="blink_source")
    
    if source_choice == "Upload":
        filename = st.file_uploader("Choose Image", ['jpg','png'], key="blink_upload")
    else:
        filename = st.camera_input("Take a Photo", key="blink_camera")

    if filename is not None:
        img = mpimg.imread(filename)
        st.image(img, caption="Original Image")
        st.success("Image received for blink detection.")

if __name__ == "__main__":
    show_prediction()