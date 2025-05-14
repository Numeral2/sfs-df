import os
import streamlit as st
from streamlit_authenticator import Authenticate, Hasher
import requests
from dotenv import load_dotenv
import bcrypt
print(bcrypt.hashpw(b"tvoja_lozinka", bcrypt.gensalt()).decode())


@st.cache_resource
def configure_auth():
    return Authenticate(
        credentials={
            'usernames': {
                os.getenv("APP_USERNAME", "admin"): {
                    'name': os.getenv("APP_NAME", "Admin User"),
                    'password': os.getenv("APP_PASSWORD_HASH")
                }
            }
        },
        cookie_name='katastar_auth',
        key='trogir_katastar_123',
        cookie_expiry_days=1
    )


authenticator = configure_auth()

# --- Page Configuration ---
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown(f"""
    <style>
    :root {{
        --primary-color: #2c3e50;
        --secondary-color: #2980b9;
        --background-color: #f8f9fa;
    }}
    
    .block-container {{
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 1rem;
    }}
    
    .stTextInput input, .stSelectbox select, .stTextArea textarea {{
        border: 1px solid #dee2e6 !important;
        border-radius: 8px;
        transition: border-color 0.3s ease;
    }}
    
    .stButton>button {{
        background-color: var(--secondary-color) !important;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 8px;
        font-weight: 500;
    }}
    
    .error-message {{
        color: #dc3545;
        padding: 1rem;
        border-radius: 8px;
        background-color: #f8d7da;
        margin: 1rem 0;
    }}
    </style>
""", unsafe_allow_html=True)

# --- Authentication Flow ---
def main_application():
    """Main application content after successful login"""
    authenticator.logout('Odjava', 'sidebar')
    st.sidebar.success(f'Dobrodošli, {st.session_state["name"]}')
    
    # Header Section
    st.image(LOGO_URL, use_column_width=True, caption="Panorama Trogira")
    st.title("🏛️ Katastarski upit za područje Trogira")
    st.markdown("""
        **Ovdje možete izvršiti katastarski upit za područje Grada Trogira.**  
        Molimo ispunite sve potrebne podatke kako bi upit bio što precizniji.
    """)
    
    # Form Sections
    with st.expander("🔗 Nulti korak: Provjera zone na ISPU sustavu", expanded=True):
        st.markdown("""
            Prije slanja upita provjerite pripadnost čestice na službenom portalu:
            [ISPU grafički prikaz](https://www.ispu.hr/)
            - 🟡 Žuta zona: Stambeno-poslovna (M1)
            - 🔴 Crvena zona: Komercijalna
            - 🔵 Plava zona: Industrijska
        """)
    
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        # Katastar Data Input
        with st.form("katastar_form"):
            st.subheader("📝 Podaci o čestici")
            
            parcel_number = st.text_input(
                "Katastarski broj čestice",
                placeholder="Unesite broj čestice",
                help="Primjer: KN-123/45"
            )
            
            parcel_area = st.number_input(
                "Kvadratura (m²)",
                min_value=0,
                step=10,
                help="Ukupna površina čestice u kvadratnim metrima"
            )
            
            naselje = st.selectbox(
                "Naselje",
                options=[
                    "Trogir", "Arbanija", "Divulje", "Drvenik Mali",
                    "Drvenik Veli", "Mastrinka", "Plano", "Žedno"
                ],
                index=0
            )
            
            upu = st.selectbox(
                "UPU",
                options=[
                    "UPU Krban", "UPU naselja Žedno", 
                    "UPU poslovne zone POS 3 (UPU 10)",
                    "UPU ugostiteljsko – turističke zone Sveti Križ (UPU 17)",
                    "UPU naselja Mastrinka 1 (UPU 6.1)", 
                    "UPU poslovne zone POS 2 (UPU 15)",
                    "UPU naselja Plano (UPU 18)", 
                    "UPU proizvodne zone Plano 3 (UPU 7)"
                ],
                index=0
            )
            
            dpu = st.selectbox(
                "DPU",
                options=[
                    "DPU Brigi – Lokvice (DPU 5)", 
                    "DPU 1. faze obale od Madiracinog mula do Duhanke (DPU 4)"
                ],
                index=0
            )
            
            zone = st.text_input(
                "Zona prema ISPU",
                placeholder="Unesite oznaku zone",
                help="Primjer: M1, K2, I3"
            )
            
            additional_query = st.text_area(
                "Dodatni upit",
                placeholder="Opišite dodatne zahtjeve...",
                height=100
            )
            
            if st.form_submit_button("📤 Pošalji upit"):
                if validate_inputs(parcel_number, parcel_area, zone):
                    send_query({
                        "parcel_number": parcel_number,
                        "parcel_area": parcel_area,
                        "naselje": naselje,
                        "upu": upu,
                        "dpu": dpu,
                        "zone": zone,
                        "additional_query": additional_query
                    })

    with col2:
        # Bot Response Section
        st.subheader("🤖 Odgovor sustava")
        if "bot_response" in st.session_state:
            st.markdown(f"""
                <div class="block-container">
                    <p style="color: var(--primary-color);">{st.session_state.bot_response}</p>
                </div>
            """, unsafe_allow_html=True)

# --- Helper Functions ---
def validate_inputs(parcel_number: str, parcel_area: float, zone: str) -> bool:
    """Validate form inputs"""
    if not parcel_number.strip():
        st.error("❌ Unesite ispravan katastarski broj čestice")
        return False
    if parcel_area <= 0:
        st.error("❌ Kvadratura mora biti pozitivan broj")
        return False
    if not zone.strip():
        st.error("❌ Odredite zonu prema ISPU sustavu")
        return False
    return True

def send_query(data: dict):
    """Send query to backend service"""
    try:
        with st.spinner("🔍 Obrada zahtjeva..."):
            response = requests.post(
                WEBHOOK_URL,
                json=data,
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            st.session_state.bot_response = result.get("response", "Nema odgovora")
            st.rerun()
            
    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Greška u komunikaciji: {str(e)}")
    except ValueError:
        st.error("⚠️ Nevažeći format odgovora")

# --- Main Execution Flow ---
name, authentication_status, username = authenticator.login("Prijava", "main")

if authentication_status:
    main_application()
elif authentication_status is False:
    st.error("🔐 Neispravni pristupni podaci")
elif authentication_status is None:
    st.warning("⏳ Molimo prijavite se za pristup sustavu")

