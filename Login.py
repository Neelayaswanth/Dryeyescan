import streamlit as st

import base64
import cv2
import psycopg2

# ================ Background image ===

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

# ----------------------


# Function to create a database connection
def create_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            host=st.secrets["db_host"],
            database=st.secrets["db_name"],
            user=st.secrets["db_user"],
            password=st.secrets["db_password"],
            port=st.secrets["db_port"]
        )
    except psycopg2.Error as e:
        print(f"Error connecting to Supabase: {e}")
    return conn

# Function to create a new user (unused in Login.py, but kept for parity)
def create_user(conn, user):
    sql = ''' INSERT INTO users(name, password, email, phone)
              VALUES(%s,%s,%s,%s) RETURNING id '''
    cur = conn.cursor()
    cur.execute(sql, user)
    new_id = cur.fetchone()[0]
    conn.commit()
    return new_id

# Function to validate user credentials
def validate_user(conn, name, password):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE name=%s AND password=%s", (name, password))
    user = cur.fetchone()
    if user:
        return True, user[1]  # Return True and user name
    return False, None

# Main function
def main():
    # st.title("User Login")
    # st.markdown(f'<h1 style="color:#000000;text-align: center;font-size:24px;">{"Login here"}</h1>', unsafe_allow_html=True)


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

        
        st.markdown(
            """
            <style>
            /* Custom styles handled in bg injection */
            </style>
            """,
            unsafe_allow_html=True
        )

        col_space1, col_main, col_space2 = st.columns([1, 1.5, 1])

        with col_main:
            st.write("") # spacer

            name = st.text_input("👤 Username", placeholder="Enter your registered name")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")

            st.write("") # spacer

            login_btn = st.button("LOGIN", use_container_width=True)
            if login_btn:
                is_valid, user_name = validate_user(conn, name, password)
                if is_valid:
                    st.success(f"Welcome back, {user_name}! Login successful!")
                    import subprocess
                    subprocess.run(['python','-m','streamlit','run','Prediction.py'])
                else:
                    st.error("Invalid user name or password!")

        conn.close()
    else:
        st.error("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
    
        
        
        
        
        
        
        
        
        
        
        
        