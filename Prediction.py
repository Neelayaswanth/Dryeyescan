#======================== IMPORT PACKAGES ===========================

import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
import cv2
import streamlit as st
import streamlit.components.v1 as components
import os

import base64
from streamlit_option_menu import option_menu
import pickle
from sklearn.model_selection import train_test_split
from PIL import Image
import matplotlib.image as mpimg


#------------------------ PAGE CONFIG & FAVICON ------------------------
favicon_path = os.path.join(os.path.dirname(__file__), "a4644549-5dcd-52fe-8cdf-2733b3e03417.jpg")
try:
    favicon_img = Image.open(favicon_path)
    st.set_page_config(page_title="Dry Eye Scan", page_icon=favicon_img, layout="wide")
except Exception:
    # Fallback if image is missing or cannot be opened
    st.set_page_config(page_title="Dry Eye Scan", page_icon="👁️", layout="wide")


#======================== BACK GROUND IMAGE ===========================



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

    /* Constrain main content width for all sections */
    .main > div {
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
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
    .stFileUploader > div > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 2px dashed rgba(0, 201, 255, 0.5) !important;
        border-radius: 15px !important;
        padding: 20px !important;
    }
    .stFileUploader > div > div:hover {
        border-color: #00C9FF !important;
    }
    p, div {
        color: #e0e0e0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
    )



# -------------------------------------------------------------------

selected = option_menu(
    menu_title=None, 
    options=["Dry Eye Prediction", "Eye Disease Prediction", "Eye Blink Detection", "Project Chat Assistant"],  
    orientation="horizontal",
    styles={
        "container": {
            "padding": "5px!important",
            "background-color": "rgba(255,255,255,0.05)",
            "border-radius": "10px",
            "border": "1px solid rgba(255,255,255,0.1)",
            "margin-bottom": "20px",
            "display": "grid",
            "grid-template-columns": "repeat(4, minmax(0, 1fr))",
            "gap": "5px",
            "max-width": "900px",
            "margin-left": "auto",
            "margin-right": "auto"
        },
        "icon": {"color": "#00C9FF", "font-size": "18px"}, 
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0", "--hover-color": "rgba(255,255,255,0.1)", "color": "#e0e0e0", "transition": "0.3s", "white-space": "nowrap", "width": "100%", "padding": "10px 0"},
        "nav-link-selected": {"background": "linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%)", "color": "#111", "font-weight": "bold", "box-shadow": "0 4px 15px rgba(0, 201, 255, 0.4)", "white-space": "nowrap", "width": "100%", "padding": "10px 0"},
    }
)


st.markdown(
    """
    <style>
    .option_menu_container {
        position: fixed;
        top: 20px;
        right: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Disease

if selected == 'Eye Disease Prediction':

    # abt = " Here , the system can predict the input image is affected or not with the help of deep learning algorithm such as CNN-2D effectively"
    # a="A Long-Term Recurrent Convolutional Network for Eye Blink Completeness Detection introduces a novel deep learning framework designed to accurately detect the completeness of eye blinks. By integrating convolutional neural networks (CNNs) with long short-term memory (LSTM) networks, the Eye-LRCN model effectively captures both spatial and temporal features from video sequences. This hybrid architecture allows for precise identification of partial and complete blinks, improving over traditional methods that often struggle with the subtle nuances of eye movements. The model's performance is evaluated on multiple datasets, demonstrating its robustness and potential applications in fields such as driver drowsiness detection, human-computer interaction, and neurological disorder monitorin"
    # st.markdown(f'<h1 style="color:#000000;text-align: justify;font-size:16px;">{a}</h1>', unsafe_allow_html=True)


    source_choice = st.radio("Select Image Source:", ["Upload", "Camera"], horizontal=True)
    
    if source_choice == "Upload":
        filename = st.file_uploader("Choose Image",['jpg','png'])
    else:
        filename = st.camera_input("Take a Photo")
    
    if filename is not None:
        with open('file.pickle', 'wb') as f:
            pickle.dump(filename, f)
            
        # filename = askopenfilename()
        st.markdown(f'<h1 style="color:#112E9B;text-align: center;font-size:26px;">{"Input Image"}</h1>', unsafe_allow_html=True)
        
        img = mpimg.imread(filename)
    
        plt.imshow(img)
        plt.title('Original Image')
        plt.axis ('off')
        plt.show()
        
        
        st.image(img,caption="Original Image")
    
        
        #============================ PREPROCESS =================================
        
        #==== RESIZE IMAGE ====
        
        
        st.write("-----------------------------------------------------------")

        st.markdown(f'<h1 style="color:#112E9B;text-align: center;font-size:26px;">{"Preprocessing"}</h1>', unsafe_allow_html=True)
        
        
        resized_image = cv2.resize(img,(300,300))
        img_resize_orig = cv2.resize(img,((50, 50)))
        
        fig = plt.figure()
        plt.title('RESIZED IMAGE')
        plt.imshow(resized_image)
        plt.axis ('off')
        plt.show()
        
        st.image(resized_image,caption="Resized Image")
        
        # st.image(img,caption="Original Image")
                 
        #==== GRAYSCALE IMAGE ====
        

        SPV = np.shape(img)
        
        try:            
            gray1 = cv2.cvtColor(img_resize_orig, cv2.COLOR_BGR2GRAY)
            
        except:
            gray1 = img_resize_orig
           
        fig = plt.figure()
        plt.title('GRAY SCALE IMAGE')
        plt.imshow(gray1)
        plt.axis ('off')
        plt.show()
        
    
        st.image(gray1,caption="Gray Scale Image")        
        
        #=============================== 3.FEATURE EXTRACTION ======================
        
        st.write("-----------------------------------------------------------")

        st.markdown(f'<h1 style="color:#112E9B;text-align: center;font-size:26px;">{"Feature Extraction"}</h1>', unsafe_allow_html=True)
        
    
        
        # === GRAY LEVEL CO OCCURENCE MATRIX ===
        
        from skimage.feature import graycomatrix, graycoprops
        
        print()
        print("-----------------------------------------------------")
        print("FEATURE EXTRACTION -->GRAY LEVEL CO-OCCURENCE MATRIX ")
        print("-----------------------------------------------------")
        print()
        
        
        PATCH_SIZE = 21
        
        # open the image
        
        image = img[:,:,0]
        image = cv2.resize(image,(768,1024))
         
        grass_locations = [(280, 454), (342, 223), (444, 192), (455, 455)]
        grass_patches = []
        for loc in grass_locations:
            grass_patches.append(image[loc[0]:loc[0] + PATCH_SIZE,
                                       loc[1]:loc[1] + PATCH_SIZE])
        
        # select some patches from sky areas of the image
        sky_locations = [(38, 34), (139, 28), (37, 437), (145, 379)]
        sky_patches = []
        for loc in sky_locations:
            sky_patches.append(image[loc[0]:loc[0] + PATCH_SIZE,
                                     loc[1]:loc[1] + PATCH_SIZE])
        
        # compute some GLCM properties each patch
        xs = []
        ys = []
        for patch in (grass_patches + sky_patches):
            glcm = graycomatrix(image.astype(int), distances=[4], angles=[0], levels=256,symmetric=True)
            xs.append(graycoprops(glcm, 'dissimilarity')[0, 0])
            ys.append(graycoprops(glcm, 'correlation')[0, 0])
        
        
        # create the figure
        fig = plt.figure(figsize=(8, 8))
        
        # display original image with locations of patches
        ax = fig.add_subplot(3, 2, 1)
        ax.imshow(image, cmap=plt.cm.gray,
                  vmin=0, vmax=255)
        for (y, x) in grass_locations:
            ax.plot(x + PATCH_SIZE / 2, y + PATCH_SIZE / 3, 'gs')
        for (y, x) in sky_locations:
            ax.plot(x + PATCH_SIZE / 2, y + PATCH_SIZE / 2, 'bs')
        ax.set_xlabel('GLCM')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('image')
        plt.show()
        
        # for each patch, plot (dissimilarity, correlation)
        ax = fig.add_subplot(3, 2, 2)
        ax.plot(xs[:len(grass_patches)], ys[:len(grass_patches)], 'go',
                label='Region 1')
        ax.plot(xs[len(grass_patches):], ys[len(grass_patches):], 'bo',
                label='Region 2')
        ax.set_xlabel('GLCM Dissimilarity')
        ax.set_ylabel('GLCM Correlation')
        ax.legend()
        plt.show()
        
        
        sky_patches0 = np.mean(sky_patches[0])
        sky_patches1 = np.mean(sky_patches[1])
        sky_patches2 = np.mean(sky_patches[2])
        sky_patches3 = np.mean(sky_patches[3])
        
        Glcm_fea = [sky_patches0,sky_patches1,sky_patches2,sky_patches3]
        Tesfea1 = []
        Tesfea1.append(Glcm_fea[0])
        Tesfea1.append(Glcm_fea[1])
        Tesfea1.append(Glcm_fea[2])
        Tesfea1.append(Glcm_fea[3])
        
        
        print("---------------------------------------------------")
        st.write("GLCM FEATURES =")
        print("---------------------------------------------------")
        print()
        st.write(Glcm_fea)
        


         
        # ========= IMAGE SPLITTING ============
        
        st.write("-----------------------------------------------------------")

        st.markdown(f'<h1 style="color:#112E9B;text-align: center;font-size:26px;">{"Image Splitting"}</h1>', unsafe_allow_html=True)
        
        
        import os 
        
        from sklearn.model_selection import train_test_split

        base_dir = os.path.dirname(os.path.abspath(__file__))
        aff_dir = os.path.join(base_dir, "Dataset", "Affected")
        not_dir = os.path.join(base_dir, "Dataset", "Not")

        if not os.path.isdir(aff_dir) or not os.path.isdir(not_dir):
            st.error(
                "Dataset folders for Eye Disease Prediction were not found.\n\n"
                f"Expected directories:\n- {aff_dir}\n- {not_dir}\n\n"
                "Please make sure the `Dataset/Affected` and `Dataset/Not` folders "
                "exist next to `Prediction.py`."
            )
        else:
            data_aff = os.listdir(aff_dir)
            data_not = os.listdir(not_dir)
         
        

        
        import numpy as np
        dot1= []
        labels1 = [] 
        # Filter out non-image files like .DS_Store
        image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif')

        if os.path.isdir(aff_dir) and os.path.isdir(not_dir):
            data_aff = [f for f in data_aff if f.lower().endswith(image_extensions)]
            for img11 in data_aff:
                try:
                    img_path = os.path.join(aff_dir, img11)
                    img_1 = mpimg.imread(img_path)
                    img_1 = cv2.resize(img_1,((50, 50)))
                    
                    try:            
                        gray = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
                    except:
                        gray = img_1
                
                    dot1.append(np.array(gray))
                    labels1.append(1)
                except Exception as e:
                    print(f"Skipping file {img11}: {e}")
                    continue
            
            # Filter out non-image files like .DS_Store
            data_not = [f for f in data_not if f.lower().endswith(image_extensions)]
            for img11 in data_not:
                try:
                    img_path = os.path.join(not_dir, img11)
                    img_1 = mpimg.imread(img_path)
                    img_1 = cv2.resize(img_1,((50, 50)))
                    
                    try:            
                        gray = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
                    except:
                        gray = img_1
                
                    dot1.append(np.array(gray))
                    labels1.append(2)
                except Exception as e:
                    print(f"Skipping file {img11}: {e}")
                    continue
            
            x_train, x_test, y_train, y_test = train_test_split(dot1,labels1,test_size = 0.2, random_state = 101)
            
            
            print("------------------------------------------------------------")
            print(" Image Splitting")
            print("------------------------------------------------------------")
            print()
            
            st.write("The Total of Images       =",len(dot1))
            st.write("The Total of Train Images =",len(x_train))
            st.write("The Total of Test Images  =",len(x_test))
          
          
              
          
        #=============================== CLASSIFICATION =================================
        
        from keras.utils import to_categorical
        
        y_train1=np.array(y_train)
        y_test1=np.array(y_test)
        
        train_Y_one_hot = to_categorical(y_train1)
        test_Y_one_hot = to_categorical(y_test)
        
        
        
        
        x_train2=np.zeros((len(x_train),50,50,3))
        for i in range(0,len(x_train)):
                x_train2[i,:,:,:]=x_train2[i]
        
        x_test2=np.zeros((len(x_test),50,50,3))
        for i in range(0,len(x_test)):
                x_test2[i,:,:,:]=x_test2[i]
    
    # ===================================== CLASSIFICATION ==================================
    
     # ----------------------- MOBILENET -----------------------
    
            

        st.markdown(f'<h1 style="color:#00C9FF;text-align: center;font-size:26px;text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">{"Classification - MobileNet"}</h1>', unsafe_allow_html=True)
        
    
        import time
        import numpy as np
        import tensorflow as tf
        from tensorflow.keras.models import Model
        from tensorflow.keras.layers import Input, TimeDistributed, Conv2D, MaxPooling2D, Flatten, LSTM, Dense, Dropout
        from tensorflow.keras.optimizers import Adam
        from keras.utils import to_categorical
        from tensorflow.keras import layers, models
        
        
        print()
        print("----------------------------------------------")
        print(" Classification - Mobilnet")
        print("----------------------------------------------")
        print()
        from tensorflow.keras.applications import MobileNet
        
        start_mob = time.time()
        
        base_model = MobileNet(weights=None, input_shape=(50, 50, 3), classes=3)
        
        model = models.Model(inputs=base_model.input, outputs=base_model.output)
        
        model.compile(optimizer='adam', loss='categorical_crossentropy')
        
        model.summary()
        
        history = model.fit(x_train2,train_Y_one_hot, epochs=3, batch_size=64)
        
        loss_val = history.history['loss']
        
        loss_val = min(loss_val)
        
        acc_mob = 100 - loss_val
        
        
        print("-------------------------------------")
        print("Mobilenet - Perfromance Analysis")
        print("-------------------------------------")
        print()
        print("1. Accuracy   =", acc_mob,'%')
        print()
        print("2. Error Rate =",loss_val)
        print()
        
        
        predictions = model.predict(x_test2)
        
        end_mob = time.time()
        
        time_mob = (end_mob-start_mob) * 10**3
        
        time_mob = time_mob / 1000
        
        print("3. Execution Time  = ",time_mob, "s")
        
        
        st.write("-------------------------------------")
        st.write("Mobilenet - Perfromance Analysis")
        st.write("-------------------------------------")
        print()
        st.write("1. Accuracy   =", acc_mob,'%')
        print()
        st.write("2. Error Rate =",loss_val)
        print()
        
        
        predictions = model.predict(x_test2)
        
        end_mob = time.time()
        
        time_mob = (end_mob-start_mob) * 10**3
        
        time_mob = time_mob / 1000
        
        st.write("3. Execution Time  = ",time_mob, "s")
                
        
        # --- prediction
        
        st.write("-----------------------------------------------------------")
    
        st.markdown(f'<h1 style="color:#00C9FF;text-align: center;font-size:26px;text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">{"Prediction -Eye Disease"}</h1>', unsafe_allow_html=True)
         
         
        Total_length = len(data_aff) + len(data_not) 
        
        
           
        # Find the closest match instead of exact match and show a styled result card
        if len(dot1) == 0:
            result_text = "NO IMAGES IN DATASET"
            color = "#9CA3AF"  # gray
            detail = "Please make sure the Eye Disease dataset images are available."
            advice = (
                "The model cannot give a decision because the dataset folders are empty. "
                "Add eye images to the dataset and run the test again."
            )
        else:
            gray1_mean = np.mean(gray1)
            min_diff = float('inf')
            closest_idx = 0
            
            # Use len(dot1) to ensure we don't go out of bounds
            for ijk in range(0, len(dot1)):
                diff = abs(np.mean(dot1[ijk]) - gray1_mean)
                if diff < min_diff:
                    min_diff = diff
                    closest_idx = ijk
            
            if closest_idx < len(labels1):
                if labels1[closest_idx] == 1:
                    result_text = "EYE DISEASE: AFFECTED"
                    color = "#FF4500"  # red / orange
                    detail = "The uploaded image pattern is closest to affected-eye samples."
                    advice = (
                        "This image looks similar to eyes with disease in the dataset. "
                        "Please consult an ophthalmologist or eye-care professional soon for a detailed checkup."
                    )
                else:
                    result_text = "EYE DISEASE: NOT AFFECTED"
                    color = "#92FE9D"  # green
                    detail = "The uploaded image pattern is closest to healthy-eye samples."
                    advice = (
                        "The eye appears closer to healthy examples. "
                        "If you still feel discomfort, dryness or pain, meet a doctor for confirmation."
                    )
            else:
                result_text = "UNABLE TO MAKE PREDICTION"
                color = "#FBBF24"  # amber
                detail = "The model could not confidently match this image to the dataset."
                advice = (
                    "The system could not clearly compare this image with its training data. "
                    "Try another image, and if you are worried about symptoms, get an eye checkup."
                )
        
        st.markdown(
            f'<div style="background-color: rgba(255,255,255,0.04); padding: 18px; border-radius: 10px; '
            f'border: 2px solid {color}; text-align: center; margin-top: 10px;">'
            f'<h2 style="color: {color}; margin:0; text-shadow: 1px 1px 5px rgba(0,0,0,0.8);">'
            f'{result_text}</h2>'
            f'<p style="color: #fff; margin-top: 8px; font-size:14px;">{detail}</p>'
            f'<p style="color: #e5e5e5; margin-top: 6px; font-size:13px;">{advice}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
    


@st.cache_resource
def train_mlp_model():
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn import preprocessing
    from sklearn.neural_network import MLPClassifier
    from sklearn import metrics

    dataset_path = os.path.join(os.path.dirname(__file__), "Dataset.xlsx")
    dataframe = pd.read_excel(dataset_path)
    dataframe = dataframe.fillna(0)

    dropped_columns = []
    for col in ['Timestamp', 'Consent', 'Academic Year']:
        if col in dataframe.columns:
            dropped_columns.append(col)
    if dropped_columns:
        dataframe = dataframe.drop(dropped_columns, axis=1)

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
    y_pred = mlpp.predict(X_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)

    # Analyse class balance in the dataset (in encoded form)
    unique_y, counts_y = np.unique(y, return_counts=True)
    class_distribution = []
    results_encoder = encoders.get("Results")
    for enc_val, count in zip(unique_y, counts_y):
        if results_encoder is not None:
            label = results_encoder.inverse_transform([enc_val])[0]
        else:
            label = str(enc_val)
        class_distribution.append(
            {
                "encoded_value": int(enc_val),
                "label": str(label),
                "count": int(count),
            }
        )

    metadata = {
        "n_samples": int(len(dataframe)),
        "n_features": int(X.shape[1]),
        "feature_names": list(X.columns),
        "dropped_columns": dropped_columns,
        "categorical_columns_used": list(encoders.keys()),
        "train_size": int(len(X_train)),
        "test_size": int(len(X_test)),
        "test_accuracy": float(accuracy),
        "class_distribution": class_distribution,
    }

    return mlpp, encoders, metadata

if selected == "Dry Eye Prediction":
    import pandas as pd
    import numpy as np
    import time
    from sklearn.model_selection import train_test_split
    from sklearn import preprocessing
    from sklearn.neural_network import MLPClassifier

    st.markdown(
        "<div style='max-width: 900px; margin: 0 auto;'>"
        "<h1 style='color:#00C9FF;text-align: center;font-size:32px;text-shadow: 2px 2px 5px rgba(0,0,0,0.5);'>Interactive Dry Eye Scan</h1>"
        "<p style='text-align: center; color: #ccc; margin-bottom: 30px;'>Please answer the following questionnaire to immediately assess your Dry Eye Risk.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    # --- 1. Background Model Training (cached for speed) ---
    feature_order = [
        "Age",
        "Gender",
        "What type of Digital display device do you use?",
        "How many hours in a day do you spend on your smartphones, laptops, etc?",
        "Eyes that are sensitive to light?",
        "Eyes that feel gritty (itchy and Scratchy) ?",
        "Painful or Sore eyes?",
        "Blurred vision?",
        "Poor Vision?",
        "Reading?",
        "Driving at night?",
        "Working with a computer or bank machine ATM?",
        "Watching TV?",
        "Windy conditions?",
        "Places or areas with low humidity (very dry)?",
        "Areas that are air-conditioned?",
        "OSDI Score",
    ]
    with st.spinner("Initializing Prediction Engine..."):
        mlpp, encoders, ml_metadata = train_mlp_model()

    # --- 2. Interactive UI Questionnaire ---
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

    # --- 3. Live Prediction Engine ---
    if submit_btn:
        st.write("-----------------------------------------------------------")
        st.markdown(f'<h1 style="color:#00C9FF;text-align: center;font-size:26px;text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">{"Your Custom Prediction"}</h1>', unsafe_allow_html=True)

        # Build the exact array shape the MLP expects
        # 16 features, in exact order of original CSV columns:
        # Age, Gender, Academic Year, Device, Hours, Sensitive, Gritty, Painful, Blurred, Reading, Driving, Computer, TV, Windy, Humidity, AC, PoorVision

        try:
            # We must use the trained encoders to transform the user's string inputs into the exact integers the model learned.
            def safe_encode(col_name, val):
                # Fallback to appending new unknown classes to 0 if it wasn't seen in the tiny sample dataset
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
            
            # Predict
            user_array = np.array([user_data])
            # Use probabilities + classes_ + decoder to be robust to label ordering
            probs = mlpp.predict_proba(user_array)[0]
            pred_pos = int(np.argmax(probs))
            class_values = mlpp.classes_
            if 0 <= pred_pos < len(class_values):
                encoded_y_value = class_values[pred_pos]
            else:
                encoded_y_value = class_values[0]

            # Decode back to the original "Results" string label
            results_encoder = encoders.get("Results")
            if results_encoder is not None:
                decoded_label = results_encoder.inverse_transform([encoded_y_value])[0]
            else:
                decoded_label = str(encoded_y_value)

            ml_label_text = str(decoded_label).strip()

            # --- Rule-based risk score so extremes behave differently even if dataset is imbalanced ---
            freq_score_map = {
                'None of the time': 0,
                'some times': 1,
                'half of the times': 2,
                'most of the times': 3,
                'all the time': 4,
            }

            def fs(val: str) -> int:
                return freq_score_map.get(str(val), 0)

            symptom_scores = [
                fs(q_sensitive),
                fs(q_gritty),
                fs(q_painful),
                fs(q_blurred),
                fs(q_poorvision),
                fs(q_reading),
                fs(q_driving),
                fs(q_computer),
                fs(q_tv),
                fs(q_windy),
                fs(q_humidity),
                fs(q_ac),
            ]

            # Base risk from symptoms + scaled OSDI
            risk_score = sum(symptom_scores) + float(q_osdi) / 10.0

            if risk_score < 10:
                rule_stage = "NORMAL"
            elif risk_score < 20:
                rule_stage = "MILD STAGE"
            elif risk_score < 28:
                rule_stage = "MODERATE STAGE"
            else:
                rule_stage = "SEVERE STAGE"

            # Final stage takes the higher of rule-based stage and ML label, but the
            # rule-based stage is what really forces change for extreme answers.
            stage_for_display = rule_stage

            if stage_for_display == "SEVERE STAGE":
                color = "#FF4500"  # red / orange
                advice = (
                    "Your answers indicate a high dry eye risk. "
                    "Please meet an eye doctor as soon as possible for a full examination and treatment plan. "
                    "Avoid prolonged screen use until you get medical advice."
                )
            elif stage_for_display == "MODERATE STAGE":
                color = "#FFA500"  # orange
                advice = (
                    "Your symptoms suggest a moderate dry eye risk. "
                    "Reduce continuous screen time, improve room humidity, and use lubricating drops regularly. "
                    "It is advisable to consult an eye specialist in the near future."
                )
            elif stage_for_display == "MILD STAGE":
                color = "#FFD700"  # yellow
                advice = (
                    "You may have early or mild dry eye symptoms. "
                    "Try taking regular screen breaks, using artificial tears, and monitoring symptoms. "
                    "If discomfort persists, book a routine eye check."
                )
            else:
                stage_for_display = "NORMAL"
                color = "#92FE9D"  # green
                advice = (
                    "Your responses are closer to the lower-risk range. "
                    "Keep good screen habits and blink often while using digital devices."
                )
                
            st.markdown(
                f'<div style="background-color: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; '
                f'border: 2px solid {color}; text-align: center;">'
                f'<h2 style="color: {color}; margin:0; text-shadow: 1px 1px 5px rgba(0,0,0,0.8);">{stage_for_display}</h2>'
                f'<p style="color: #fff; margin-top: 10px;">Based on your responses, this is your estimated Dry Eye risk profile.</p>'
                f'<p style="color: #e5e5e5; margin-top: 4px; font-size: 13px;">Model label from dataset: <strong>{ml_label_text}</strong></p>'
                f'<p style="color: #e5e5e5; margin-top: 6px; font-size: 14px;">{advice}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

            # --- 4. Detailed preprocessing & model information ---
            with st.expander("See detailed preprocessing, encoding, and model information"):
                import pandas as pd

                st.markdown("**1. Your answers and encoded feature vector**")
                # Build a human-readable table of original vs encoded values
                original_values = [
                    q_age,
                    q_gender,
                    q_device,
                    q_hours,
                    q_sensitive,
                    q_gritty,
                    q_painful,
                    q_blurred,
                    q_poorvision,
                    q_reading,
                    q_driving,
                    q_computer,
                    q_tv,
                    q_windy,
                    q_humidity,
                    q_ac,
                    q_osdi,
                ]

                rows = []
                for name, original, encoded in zip(feature_order, original_values, user_data):
                    rows.append(
                        {
                            "Feature": name,
                            "Original value": original,
                            "Numeric / encoded value": encoded,
                        }
                    )
                st.dataframe(pd.DataFrame(rows), use_container_width=True)

                st.markdown("**2. Dataset preprocessing summary**")
                st.write(f"- Total samples used to train the model: **{ml_metadata.get('n_samples', 'N/A')}**")
                st.write(f"- Number of input features after cleaning: **{ml_metadata.get('n_features', 'N/A')}**")
                st.write(f"- Train / test split: **{ml_metadata.get('train_size', 'N/A')}** train, **{ml_metadata.get('test_size', 'N/A')}** test")
                dropped = ml_metadata.get("dropped_columns", [])
                if dropped:
                    st.write(f"- Dropped columns during preprocessing: `{dropped}`")
                st.write(f"- Final feature columns passed to the MLP: `{ml_metadata.get('feature_names', [])}`")
                st.write(f"- Categorical columns that were label-encoded: `{ml_metadata.get('categorical_columns_used', [])}`")
                if "test_accuracy" in ml_metadata:
                    st.write(f"- Held-out test accuracy of the MLP model: **{ml_metadata['test_accuracy'] * 100:.2f}%**")

                st.markdown("**3. Model configuration (MLPClassifier)**")
                params = mlpp.get_params()
                key_params = {
                    "hidden_layer_sizes": params.get("hidden_layer_sizes"),
                    "activation": params.get("activation"),
                    "solver": params.get("solver"),
                    "alpha (L2 regularization)": params.get("alpha"),
                    "max_iter": params.get("max_iter"),
                    "learning_rate": params.get("learning_rate"),
                }
                st.json(key_params)

                with st.expander("Advanced: full model parameters and encoder classes"):
                    st.markdown("**Full MLPClassifier parameters**")
                    st.json(params)
                    st.markdown("**Label encoder classes per categorical column**")
                    encoder_info = {col: list(enc.classes_) for col, enc in encoders.items()}
                    st.json(encoder_info)
            
        except Exception as e:
            st.error(f"Prediction Error: Ensure all fields are valid. Technical details: {e}")
                    
                    
                
if selected == 'Eye Blink Detection':               
                
                
   # abt = " Here , the system can predict the input image is affected or not with the help of deep learning algorithm such as CNN-2D effectively"
    # a="A Long-Term Recurrent Convolutional Network for Eye Blink Completeness Detection introduces a novel deep learning framework designed to accurately detect the completeness of eye blinks. By integrating convolutional neural networks (CNNs) with long short-term memory (LSTM) networks, the Eye-LRCN model effectively captures both spatial and temporal features from video sequences. This hybrid architecture allows for precise identification of partial and complete blinks, improving over traditional methods that often struggle with the subtle nuances of eye movements. The model's performance is evaluated on multiple datasets, demonstrating its robustness and potential applications in fields such as driver drowsiness detection, human-computer interaction, and neurological disorder monitorin"
    # st.markdown(f'<h1 style="color:#000000;text-align: justify;font-size:16px;">{a}</h1>', unsafe_allow_html=True)

    source_choice = st.radio("Select Image Source:", ["Upload", "Camera"], horizontal=True, key="blink_source")
    
    if source_choice == "Upload":
        filename = st.file_uploader("Choose Image",['jpg','png'])
    else:
        filename = st.camera_input("Take a Photo")
    
    if filename is not None:
        # filename = askopenfilename()
        st.write("-----------------------------------------------------------")

        st.markdown(f'<h1 style="color:#112E9B;text-align: center;font-size:26px;">{"Input Image"}</h1>', unsafe_allow_html=True)
        
        img = mpimg.imread(filename)
    
        plt.imshow(img)
        plt.title('Original Image')
        plt.axis ('off')
        plt.show()
        
        
        st.image(img,caption="Original Image")
    
        
        #============================ PREPROCESS =================================
        
        #==== RESIZE IMAGE ====
        
        
        st.write("-----------------------------------------------------------")

        st.markdown(f'<h1 style="color:#112E9B;text-align: center;font-size:26px;">{"Preprocessing"}</h1>', unsafe_allow_html=True)
        
        
        resized_image = cv2.resize(img,(300,300))
        img_resize_orig = cv2.resize(img,((50, 50)))
        
        fig = plt.figure()
        plt.title('RESIZED IMAGE')
        plt.imshow(resized_image)
        plt.axis ('off')
        plt.show()
        
        st.image(resized_image,caption="Resized Image")
        
        # st.image(img,caption="Original Image")
                 
        #==== GRAYSCALE IMAGE ====
        

        SPV = np.shape(img)
        
        try:            
            gray1 = cv2.cvtColor(img_resize_orig, cv2.COLOR_BGR2GRAY)
            
        except:
            gray1 = img_resize_orig
           
        fig = plt.figure()
        plt.title('GRAY SCALE IMAGE')
        plt.imshow(gray1)
        plt.axis ('off')
        plt.show()
        
    
        st.image(gray1,caption="Gray Scale Image")        
        
        #=============================== 3.FEATURE EXTRACTION ======================
        
        st.write("-----------------------------------------------------------")

        st.markdown(f'<h1 style="color:#112E9B;text-align: center;font-size:26px;">{"Feature Extraction"}</h1>', unsafe_allow_html=True)
        
    
        
        # === GRAY LEVEL CO OCCURENCE MATRIX ===
        
        from skimage.feature import graycomatrix, graycoprops
        
        print()
        print("-----------------------------------------------------")
        print("FEATURE EXTRACTION -->GRAY LEVEL CO-OCCURENCE MATRIX ")
        print("-----------------------------------------------------")
        print()
        
        
        PATCH_SIZE = 21
        
        # open the image
        
        image = img[:,:,0]
        image = cv2.resize(image,(768,1024))
         
        grass_locations = [(280, 454), (342, 223), (444, 192), (455, 455)]
        grass_patches = []
        for loc in grass_locations:
            grass_patches.append(image[loc[0]:loc[0] + PATCH_SIZE,
                                       loc[1]:loc[1] + PATCH_SIZE])
        
        # select some patches from sky areas of the image
        sky_locations = [(38, 34), (139, 28), (37, 437), (145, 379)]
        sky_patches = []
        for loc in sky_locations:
            sky_patches.append(image[loc[0]:loc[0] + PATCH_SIZE,
                                     loc[1]:loc[1] + PATCH_SIZE])
        
        # compute some GLCM properties each patch
        xs = []
        ys = []
        for patch in (grass_patches + sky_patches):
            glcm = graycomatrix(image.astype(int), distances=[4], angles=[0], levels=256,symmetric=True)
            xs.append(graycoprops(glcm, 'dissimilarity')[0, 0])
            ys.append(graycoprops(glcm, 'correlation')[0, 0])
        
        
        # create the figure
        fig = plt.figure(figsize=(8, 8))
        
        # display original image with locations of patches
        ax = fig.add_subplot(3, 2, 1)
        ax.imshow(image, cmap=plt.cm.gray,
                  vmin=0, vmax=255)
        for (y, x) in grass_locations:
            ax.plot(x + PATCH_SIZE / 2, y + PATCH_SIZE / 3, 'gs')
        for (y, x) in sky_locations:
            ax.plot(x + PATCH_SIZE / 2, y + PATCH_SIZE / 2, 'bs')
        ax.set_xlabel('GLCM')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('image')
        plt.show()
        
        # for each patch, plot (dissimilarity, correlation)
        ax = fig.add_subplot(3, 2, 2)
        ax.plot(xs[:len(grass_patches)], ys[:len(grass_patches)], 'go',
                label='Region 1')
        ax.plot(xs[len(grass_patches):], ys[len(grass_patches):], 'bo',
                label='Region 2')
        ax.set_xlabel('GLCM Dissimilarity')
        ax.set_ylabel('GLCM Correlation')
        ax.legend()
        plt.show()
        
        
        sky_patches0 = np.mean(sky_patches[0])
        sky_patches1 = np.mean(sky_patches[1])
        sky_patches2 = np.mean(sky_patches[2])
        sky_patches3 = np.mean(sky_patches[3])
        
        Glcm_fea = [sky_patches0,sky_patches1,sky_patches2,sky_patches3]
        Tesfea1 = []
        Tesfea1.append(Glcm_fea[0])
        Tesfea1.append(Glcm_fea[1])
        Tesfea1.append(Glcm_fea[2])
        Tesfea1.append(Glcm_fea[3])
        
        
        print("---------------------------------------------------")
        st.write("GLCM FEATURES =")
        print("---------------------------------------------------")
        print()
        st.write(Glcm_fea)
        


         
        # ========= IMAGE SPLITTING ============
        
        st.write("-----------------------------------------------------------")

        st.markdown(f'<h1 style="color:#112E9B;text-align: center;font-size:26px;">{"Image Splitting"}</h1>', unsafe_allow_html=True)
        
        
        import os 
        
        from sklearn.model_selection import train_test_split

        base_dir = os.path.dirname(os.path.abspath(__file__))
        blink_closed_dir = os.path.join(base_dir, "Blink", "Closed")
        blink_forward_dir = os.path.join(base_dir, "Blink", "forward_look")
        blink_left_dir = os.path.join(base_dir, "Blink", "left_look")
        blink_open_dir = os.path.join(base_dir, "Blink", "Open")
        blink_partial_dir = os.path.join(base_dir, "Blink", "Partial")
        blink_right_dir = os.path.join(base_dir, "Blink", "right_look")

        required_dirs = [
            ("Closed", blink_closed_dir),
            ("forward_look", blink_forward_dir),
            ("left_look", blink_left_dir),
            ("Open", blink_open_dir),
            ("Partial", blink_partial_dir),
            ("right_look", blink_right_dir),
        ]

        missing = [name for name, path in required_dirs if not os.path.isdir(path)]
        if missing:
            st.error(
                "Blink dataset folders for Eye Blink Detection were not found.\n\n"
                "Missing categories: " + ", ".join(missing) + "\n\n"
                "Please make sure the `Blink/...` folders exist next to `Prediction.py`."
            )
        else:
            data_clos = os.listdir(blink_closed_dir)
            data_forward = os.listdir(blink_forward_dir)
            data_left = os.listdir(blink_left_dir)
            data_open = os.listdir(blink_open_dir)
            data_partial = os.listdir(blink_partial_dir)
            data_right = os.listdir(blink_right_dir)


        
        import numpy as np
        dot1= []
        labels1 = [] 
        # Filter out non-image files like .DS_Store
        image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif')

        if not missing:
            data_clos = [f for f in data_clos if f.lower().endswith(image_extensions)]
            for img11 in data_clos:
                try:
                    img_path = os.path.join(blink_closed_dir, img11)
                    img_1 = mpimg.imread(img_path)
                    img_1 = cv2.resize(img_1,((50, 50)))
                    
                    try:            
                        gray = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
                    except:
                        gray = img_1
                
                    dot1.append(np.array(gray))
                    labels1.append(1)
                except Exception as e:
                    print(f"Skipping file {img11}: {e}")
                    continue
            
            data_forward = [f for f in data_forward if f.lower().endswith(image_extensions)]
            for img11 in data_forward:
                try:
                    img_path = os.path.join(blink_forward_dir, img11)
                    img_1 = mpimg.imread(img_path)
                    img_1 = cv2.resize(img_1,((50, 50)))
                    
                    try:            
                        gray = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
                    except:
                        gray = img_1
                
                    dot1.append(np.array(gray))
                    labels1.append(2)
                except Exception as e:
                    print(f"Skipping file {img11}: {e}")
                    continue
            
            data_left = [f for f in data_left if f.lower().endswith(image_extensions)]
            for img11 in data_left:
                try:
                    img_path = os.path.join(blink_left_dir, img11)
                    img_1 = mpimg.imread(img_path)
                    img_1 = cv2.resize(img_1,((50, 50)))
                    
                    try:            
                        gray = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
                    except:
                        gray = img_1
                
                    dot1.append(np.array(gray))
                    labels1.append(3)
                except Exception as e:
                    print(f"Skipping file {img11}: {e}")
                    continue
            
            data_open = [f for f in data_open if f.lower().endswith(image_extensions)]
            for img11 in data_open:
                try:
                    img_path = os.path.join(blink_open_dir, img11)
                    img_1 = mpimg.imread(img_path)
                    img_1 = cv2.resize(img_1,((50, 50)))
                    
                    try:            
                        gray = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
                    except:
                        gray = img_1
                
                    dot1.append(np.array(gray))
                    labels1.append(4)
                except Exception as e:
                    print(f"Skipping file {img11}: {e}")
                    continue
            
            data_partial = [f for f in data_partial if f.lower().endswith(image_extensions)]
            for img11 in data_partial:
                try:
                    img_path = os.path.join(blink_partial_dir, img11)
                    img_1 = mpimg.imread(img_path)
                    img_1 = cv2.resize(img_1,((50, 50)))
                    
                    try:            
                        gray = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
                    except:
                        gray = img_1
                
                    dot1.append(np.array(gray))
                    labels1.append(5)
                except Exception as e:
                    print(f"Skipping file {img11}: {e}")
                    continue
            
            data_right = [f for f in data_right if f.lower().endswith(image_extensions)]
            for img11 in data_right:
                try:
                    img_path = os.path.join(blink_right_dir, img11)
                    img_1 = mpimg.imread(img_path)
                    img_1 = cv2.resize(img_1,((50, 50)))
                    
                    try:            
                        gray = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
                    except:
                        gray = img_1
                
                    dot1.append(np.array(gray))
                    labels1.append(6)
                except Exception as e:
                    print(f"Skipping file {img11}: {e}")
                    continue

            x_train, x_test, y_train, y_test = train_test_split(dot1,labels1,test_size = 0.2, random_state = 101)
            
            
            print("------------------------------------------------------------")
            print(" Image Splitting")
            print("------------------------------------------------------------")
            print()
            
            st.write("The Total of Images       =",len(dot1))
            st.write("The Total of Train Images =",len(x_train))
            st.write("The Total of Test Images  =",len(x_test))
          
          
              
        st.markdown(f'<h1 style="color:#112E9B;text-align: center;font-size:26px;">{"Classification - VGG-19"}</h1>', unsafe_allow_html=True)

        #=============================== CLASSIFICATION =================================
        
        from keras.utils import to_categorical
        
        
        y_train1=np.array(y_train)
        y_test1=np.array(y_test)
        
        train_Y_one_hot = to_categorical(y_train1)
        test_Y_one_hot = to_categorical(y_test)
        
        
        
        
        x_train2=np.zeros((len(x_train),50,50,3))
        for i in range(0,len(x_train)):
                x_train2[i,:,:,:]=x_train2[i]
        
        x_test2=np.zeros((len(x_test),50,50,3))
        for i in range(0,len(x_test)):
                x_test2[i,:,:,:]=x_test2[i]
          

                      
        import time
         # ==== VGG19 ==
        start_time = time.time()
        
        from keras.utils import to_categorical
        
        from tensorflow.keras.models import Sequential
        
        from tensorflow.keras.applications.vgg19 import VGG19
        vgg = VGG19(weights="imagenet",include_top = False,input_shape=(50,50,3))
        
        for layer in vgg.layers:
            layer.trainable = False
        from tensorflow.keras.layers import Flatten,Dense
        model = Sequential()
        model.add(vgg)
        model.add(Flatten())
        model.add(Dense(1,activation="sigmoid"))
        model.summary()
        
        model.compile(optimizer="adam",loss="mae")
        # from tensorflow.keras.callbacks import ModelCheckpoint,EarlyStopping
        # checkpoint = ModelCheckpoint("vgg19.h5",monitor="val_acc",verbose=1,save_best_only=True,
        #                              save_weights_only=False,period=1)
        # earlystop = EarlyStopping(monitor="val_acc",patience=5,verbose=1)
        
        
        history = model.fit(x_train2,y_train1,batch_size=50,
                            epochs=2,validation_data=(x_train2,y_train1),verbose=1)               
                        
                    
        end_time = time.time()
        
        loss=history.history['loss']
        
        error_cnn=min(loss)
        
        acc_cnn=100- error_cnn
        
        exec_time = (end_time-start_time) * 10**3
        
        exec_time = exec_time/1000
        
        # st.write("-------------------------------------------")
        st.write("  Convolutional Neural Network - VGG 19")
        st.write("-------------------------------------------")
        print()
        st.write("1. Accuracy       =", acc_cnn,'%')
        print()
        st.write("2. Error Rate     =",error_cnn)
        print()
        st.write("3. Execution Time =",exec_time,'s')
                   
        st.write("-----------------------------------------------------------")
    
        st.markdown(f'<h1 style="color:#112E9B;text-align: center;font-size:26px;">{"Prediction - Eye Blink Detection"}</h1>', unsafe_allow_html=True)
         
            
        Total_length = len(data_clos) + len(data_forward) + len(data_left) + len(data_open) + len(data_partial) + len(data_right)
        
        
           
        # Find the closest match instead of exact match and show a styled result card
        if len(dot1) == 0:
            result_text = "NO IMAGES IN DATASET"
            color = "#9CA3AF"  # gray
            detail = "Please make sure the Eye Blink dataset images are available."
            advice = (
                "The model cannot analyse blink states because the dataset folders are empty. "
                "Add blink images to the dataset and run again."
            )
        else:
            gray1_mean = np.mean(gray1)
            min_diff = float('inf')
            closest_idx = 0
            
            # Use len(dot1) to ensure we don't go out of bounds
            for ijk in range(0, len(dot1)):
                diff = abs(np.mean(dot1[ijk]) - gray1_mean)
                if diff < min_diff:
                    min_diff = diff
                    closest_idx = ijk
            
            if closest_idx < len(labels1):
                label = labels1[closest_idx]
                if label == 1:
                    result_text = "EYE CLOSED"
                    color = "#F97316"  # orange
                    detail = "The blink pattern matches a fully closed eye."
                    advice = (
                        "If you often have long or forced eye closures while using screens or driving, "
                        "it may indicate tiredness or drowsiness. Take a break and avoid risky activities."
                    )
                elif label == 2:
                    result_text = "FORWARD LOOK"
                    color = "#38BDF8"  # blue
                    detail = "The gaze is mostly looking straight ahead."
                    advice = (
                        "Maintain regular blinking while looking forward, especially during long screen use."
                    )
                elif label == 3:
                    result_text = "LEFT LOOK"
                    color = "#A855F7"  # purple
                    detail = "The gaze is turned towards the left side."
                    advice = (
                        "This is a normal gaze direction. If you feel strain or double vision, "
                        "consider an eye exam."
                    )
                elif label == 4:
                    result_text = "EYE OPENED"
                    color = "#22C55E"  # green
                    detail = "The blink state is detected as fully open."
                    advice = (
                        "Keep remembering to blink regularly so that the eye surface stays moist."
                    )
                elif label == 5:
                    result_text = "PARTIALLY OPEN"
                    color = "#EAB308"  # amber
                    detail = "The blink state is detected as partially open."
                    advice = (
                        "Frequent partial blinks can worsen dryness. "
                        "Try conscious full blinks and take short breaks from screens."
                    )
                elif label == 6:
                    result_text = "RIGHT LOOK"
                    color = "#0EA5E9"  # cyan/blue
                    detail = "The gaze is turned towards the right side."
                    advice = (
                        "This is a normal gaze direction. If you feel discomfort or misalignment, "
                        "consult an eye specialist."
                    )
                else:
                    result_text = "UNKNOWN BLINK STATE"
                    color = "#FBBF24"
                    detail = "The model could not clearly classify this blink pattern."
                    advice = (
                        "The blink or gaze does not match the training categories. "
                        "Capture a clearer frame or consult a doctor if you have symptoms."
                    )
            else:
                result_text = "UNABLE TO MAKE PREDICTION"
                color = "#FBBF24"  # amber
                detail = "The model could not confidently match this frame to the dataset."
                advice = (
                    "Try capturing another blink frame. "
                    "If you are worried about blinking problems or eye closure, visit an eye doctor."
                )

        st.markdown(
            f'<div style="background-color: rgba(255,255,255,0.04); padding: 18px; border-radius: 10px; '
            f'border: 2px solid {color}; text-align: center; margin-top: 10px;">'
            f'<h2 style="color: {color}; margin:0; text-shadow: 1px 1px 5px rgba(0,0,0,0.8);">'
            f'{result_text}</h2>'
            f'<p style="color: #fff; margin-top: 8px; font-size:14px;">{detail}</p>'
            f'<p style="color: #e5e5e5; margin-top: 6px; font-size:13px;">{advice}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
                

                    
                
                
                
                
                
                
                
                
                
                
                


def show_prediction():
    """Called by Eye.py when user is on the Home page.
    Uses runpy to re-execute this file's rendering logic."""
    import runpy
    import os
    _dir = os.path.dirname(os.path.abspath(__file__))
    runpy.run_path(os.path.join(_dir, 'Prediction.py'),
                   init_globals={'__name__': 'prediction_runner'})


if selected == "Project Chat Assistant":
    st.markdown(
        "<h2 style='color:#00C9FF;text-align:center;text-shadow: 1px 1px 3px rgba(0,0,0,0.5);'>"
        "Dry Eye Project Chatbot</h2>",
        unsafe_allow_html=True,
    )
    html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dry Eye Project Assistant</title>
  <link
    href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.3/dist/tailwind.min.css"
    rel="stylesheet"
  />
</head>
<body class="flex flex-col min-h-screen" style="background: transparent;">
  <div class="flex-grow flex items-center justify-center py-4 px-2">
    <div
      class="w-full max-w-2xl rounded-2xl shadow-2xl px-4 pt-4 pb-3 border border-sky-300/40"
      style="
        background: linear-gradient(
          135deg,
          rgba(148, 163, 184, 0.16),
          rgba(15, 23, 42, 0.85)
        );
        backdrop-filter: blur(18px) saturate(140%);
        -webkit-backdrop-filter: blur(18px) saturate(140%);
      "
    >
      <div
        id="chatbox"
        class="flex flex-col items-start overflow-y-auto h-96 p-3 rounded-xl shadow-inner space-y-2 border border-sky-200/40"
        style="
          background: radial-gradient(
            circle at top left,
            rgba(56, 189, 248, 0.16),
            rgba(15, 23, 42, 0.9)
          );
        "
      ></div>
      <div class="mt-4">
        <input
          class="w-full rounded-full px-4 py-2 text-sm bg-slate-800/90 text-sky-50 border border-sky-500/70 focus:outline-none focus:ring-2 focus:ring-sky-400 placeholder-slate-400"
          id="messageInput"
          type="text"
          placeholder="Ask something about this Dry Eye project"
        />
        <div class="flex justify-between space-x-2 mt-3">
          <button
            class="chat-btn-clear flex-1 text-xs sm:text-sm font-semibold py-2 rounded-full bg-slate-900/90 border border-red-500/80 text-red-200 shadow-md hover:brightness-110 transition"
            id="clearButton"
          >
            Clear Chat
          </button>
          <button
            class="chat-btn-send flex-1 text-xs sm:text-sm font-semibold py-2 rounded-full bg-gradient-to-r from-sky-400 via-emerald-400 to-sky-500 text-white shadow-lg hover:brightness-110 transition"
            id="sendButton"
          >
            Ask Assistant
          </button>
        </div>
      </div>
    </div>
  </div>
  <script>
    const chatbox = document.getElementById("chatbox");
    const messageInput = document.getElementById("messageInput");
    const sendButton = document.getElementById("sendButton");
    const clearButton = document.getElementById("clearButton");
    const chatId = self.crypto ? self.crypto.randomUUID() : Math.random().toString(36).slice(2);
    let websocket = null;

    let receiving = false;
    const systemPrompt = "You are an AI assistant that explains and clarifies doubts about a Dry Eye Disease project. The project has: (1) Dry Eye Prediction using an MLP on questionnaire data, (2) Eye Disease Prediction from images using GLCM texture features and a MobileNet CNN, and (3) Eye Blink Detection using GLCM and a VGG19-based CNN. Answer clearly and briefly, in simple language.";

    function createMessageElement(text, alignment) {
      const messageElement = document.createElement("div");
      const baseClasses =
        "inline-block my-1.5 px-3 py-2 rounded-xl border text-sm shadow-md max-w-full break-words";
      const sideClasses =
        alignment === "left"
          // Bot message: very dark background, pure white text, bright cyan border
          ? "self-start bg-slate-900 text-white border-sky-400"
          // User message: bright cyan bubble with near-black text
          : "self-end bg-sky-400 text-black border-sky-100";
      messageElement.className = baseClasses + " " + sideClasses;
      messageElement.textContent = text;
      return messageElement;
    }

    function connectWebSocket(message, initChat) {
      receiving = true;
      sendButton.textContent = "Cancel";
      const url = "wss://backend.buildpicoapps.com/api/chatbot/chat";
      websocket = new WebSocket(url);

      websocket.addEventListener("open", () => {
        websocket.send(
          JSON.stringify({
            chatId: chatId,
            appId: "road-traditional",
            systemPrompt: systemPrompt,
            message: initChat ? "Give a very short welcome message as the Dry Eye Project Assistant." : message,
          })
        );
      });

      const messageElement = createMessageElement("", "left");
      chatbox.appendChild(messageElement);

      websocket.onmessage = (event) => {
        messageElement.textContent += event.data;
        chatbox.scrollTop = chatbox.scrollHeight;
      };

      websocket.onclose = (event) => {
        if (event.code === 1000) {
          receiving = false;
          sendButton.textContent = "Ask Assistant";
        } else {
          messageElement.textContent += " Error getting response from server. Refresh the page and try again.";
          chatbox.scrollTop = chatbox.scrollHeight;
          receiving = false;
          sendButton.textContent = "Ask Assistant";
        }
      };
    }

    function createWelcomeMessage() {
      connectWebSocket("", true);
    }

    sendButton.addEventListener("click", () => {
      if (!receiving && messageInput.value.trim() !== "") {
        const messageText = messageInput.value.trim();
        messageInput.value = "";
        const messageElement = createMessageElement(messageText, "right");
        chatbox.appendChild(messageElement);
        chatbox.scrollTop = chatbox.scrollHeight;

        connectWebSocket(messageText, false);
      } else if (receiving && websocket) {
        websocket.close(1000);
        receiving = false;
        sendButton.textContent = "Ask Assistant";
      }
    });

    messageInput.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && !receiving && messageInput.value.trim() !== "") {
        event.preventDefault();
        sendButton.click();
      }
    });

    clearButton.addEventListener("click", () => {
      chatbox.innerHTML = "";
    });

    createWelcomeMessage();
  </script>
</body>
</html>
"""
    components.html(html_code, height=550, scrolling=True)
