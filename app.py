import os
import streamlit as st
from streamlit_authenticator import Authenticate
from dotenv import load_dotenv

# Učitaj varijable iz .env datoteke
load_dotenv()

# --- Authentication Setup ---
def configure_auth():
    """Create authenticator without caching since it uses widgets"""
    return Authenticate(
        credentials={
            'usernames': {
                os.getenv("APP_USERNAME", "admin"): {
                    'name': os.getenv("APP_NAME", "Admin User"),
                    'password': os.getenv("APP_PASSWORD_HASH, "$2b$12$QwbHdK.uHoGRkRgDXaWCcureqD0.XzRbBdR/wPbs1ZIvfuFEZ0rn")  # Pohranjeni hash lozinke iz .env
                }
            }
        },
        cookie_name='simple_auth',
        key='simple_auth_123',
        cookie_expiry_days=1
    )

# --- Page Configuration ---
st.set_page_config(
    page_title="Login / Sign Up",
    page_icon="🔒",
    layout="centered"
)

# --- Authentication Flow ---
def login_page():
    """Login page"""
    authenticator = configure_auth()

    st.title("Login to the Application")
    # Specify location explicitly for the login form
    username, authentication_status = authenticator.login("Prijava", location="main")

    if authentication_status:
        st.success(f"Welcome {username}")
        # After successful login, you can display the content here
    elif authentication_status is False:
        st.error("Invalid credentials")
    elif authentication_status is None:
        st.warning("Please enter your credentials")

def signup_page():
    """Sign-up page to create a new user"""
    st.title("Create an Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password == confirm_password:
            # Save the new user credentials here (in your database or file)
            st.success("Account successfully created!")
        else:
            st.error("Passwords do not match!")

# --- Main App Flow ---
page = st.radio("Select a page", ("Login", "Sign Up"))

if page == "Login":
    login_page()
elif page == "Sign Up":
    signup_page()
