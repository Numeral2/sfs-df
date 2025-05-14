import os
import streamlit as st
from streamlit_authenticator import Authenticate
from dotenv import load_dotenv
import requests

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
                    'password': os.getenv("APP_PASSWORD_HASH")  # Pohranjeni hash lozinke iz .env
                }
            }
        },
        cookie_name='katastar_auth',
        key='trogir_katastar_123',
        cookie_expiry_days=1
    )

# --- Page Configuration ---
st.set_page_config(
    page_title="Katastarski upit - Trogir",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Authentication Flow ---
def main_application():
    """Main application content after successful login"""
    authenticator.logout('Odjava', 'sidebar')
    st.sidebar.success(f'Dobrodošli, {st.session_state["name"]}')
    
    # Header Section
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e2/Trogir_Harbor_Panorama.jpg", use_column_width=True, caption="Panorama Trogira")
    st.title("🏛️ Katastarski upit za područje Trogira")
    st.markdown(""" **Ovdje možete izvršiti katastarski upit za područje Grada Trogira.** """)
    
    # Form Sections
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        # Katastar Data Input
        with st.form("katastar_form"):
            st.subheader("📝 Podaci o čestici")
            parcel_number = st.text_input("Katastarski broj čestice")
            parcel_area = st.number_input("Kvadratura (m²)", min_value=0, step=10)
            naselje = st.selectbox("Naselje", options=["Trogir", "Arbanija", "Divulje", "Drvenik Mali", "Drvenik Veli"])
            
            if st.form_submit_button("📤 Pošalji upit"):
                st.success("Upit poslan!")
                # Tu možeš dodati kod za slanje podataka na webhook ili procesiranje
                send_query({
                    "parcel_number": parcel_number,
                    "parcel_area": parcel_area,
                    "naselje": naselje
                })

    with col2:
        # Bot Response Section
        st.subheader("🤖 Odgovor sustava")
        st.markdown("Ovdje će biti odgovor od sustava.")

# --- Send Query to Webhook ---
def send_query(data: dict):
    """Send query to backend service (webhook)"""
    webhook_url = os.getenv("WEBHOOK_URL", "https://senderrr.streamlit.app/")  # Podesi URL webhoka
    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()  # Provjeri status odgovora
        st.success("Zahtjev uspješno poslan na webhook!")
    except requests.exceptions.RequestException as e:
        st.error(f"Greška u slanju podataka na webhook: {e}")

# --- Main Execution Flow ---
authenticator = configure_auth()

# Try logging in without passing the location argument
name, authentication_status, username = authenticator.login("Prijava")  # No location argument

if authentication_status:
    main_application()
elif authentication_status is False:
    st.error("🔐 Neispravni pristupni podaci")
elif authentication_status is None:
    st.warning("⏳ Molimo prijavite se za pristup sustavu")

