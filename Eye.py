#======================== IMPORT PACKAGES ===========================

import streamlit as st
import base64


st.markdown(f'<h1 style="color:#ffffff;text-align: center;font-size:40px;font-weight:bold;text-shadow: 2px 2px 8px rgba(0,0,0,0.8);">{"Dry Eye Scan"}</h1>', unsafe_allow_html=True)

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
    div[data-testid="stVerticalBlock"] > div > div > div > div {
        /* Styling the card container specifically when we place it */
    }
    </style>
    """,
    unsafe_allow_html=True
    )
add_custom_bg()


# --------------------- REGISTER PAGE




import streamlit as st
import psycopg2
import re

# Function to create a database connection
def create_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            host="db.sebkxixuxpydifogmttc.supabase.co",
            database="postgres",
            user="postgres",
            password="Yash00435210@",
            port="5432"
        )
    except psycopg2.Error as e:
        print(f"Error connecting to Supabase: {e}")
    return conn

# Function to create a new user
def create_user(conn, user):
    sql = ''' INSERT INTO users(name, password, email, phone)
              VALUES(%s,%s,%s,%s) RETURNING id '''
    cur = conn.cursor()
    cur.execute(sql, user)
    new_id = cur.fetchone()[0]
    conn.commit()
    return new_id

# Function to check if a user already exists
def user_exists(conn, email):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    if cur.fetchone():
        return True
    return False

# Function to validate email
def validate_email(email):
    pattern = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return re.match(pattern, email)

# Function to validate phone number
def validate_phone(phone):
    pattern = r'^[6-9]\d{9}$'
    return re.match(pattern, phone)

# Main function
def main():
    # st.title("User Registration")

    # Create a database connection
    conn = create_connection()

    if conn is not None:
        # Create users table if it doesn't exist
        try:
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS users
                         (id SERIAL PRIMARY KEY,
                         name TEXT NOT NULL,
                         password TEXT NOT NULL,
                         email TEXT NOT NULL UNIQUE,
                         phone TEXT NOT NULL);''')
            conn.commit()
        except psycopg2.Error as e:
            print(f"Error creating table: {e}")

        # User input fields
        
        st.markdown(
            """
            <style>
            /* Custom styles handled in bg injection */
            </style>
            """,
            unsafe_allow_html=True
        )

        # Centered card-like layout
        col_space1, col_main, col_space2 = st.columns([1, 1.5, 1])

        with col_main:
            st.write("") # spacer

            name = st.text_input("👤 Full Name", placeholder="Enter your full name")
            email = st.text_input("📧 Email Address", placeholder="Enter your email ID")
            phone = st.text_input("📱 Phone Number", placeholder="Enter your 10-digit phone number")
            password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
            
            st.write("") # spacer

            col1, col2 = st.columns(2)

            with col1:
                register_btn = st.button("REGISTER", use_container_width=True)
                if register_btn:
                    if password == confirm_password:
                        if not user_exists(conn, email):
                            if validate_email(email) and validate_phone(phone):
                                user = (name, password, email, phone)
                                create_user(conn, user)
                                st.success("User registered successfully!")
                            else:
                                st.error("Invalid email or phone number!")
                        else:
                            st.error("User with this email already exists!")
                    else:
                        st.error("Passwords do not match!")
                    
            with col2:
                login_btn = st.button("GO TO LOGIN", use_container_width=True)
                if login_btn:
                    import subprocess
                    subprocess.run(['python','-m','streamlit','run','Login.py'])

        conn.close()



  
if __name__ == '__main__':
    main()


