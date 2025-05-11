import streamlit as st
import requests
import pyperclip

# Postavke stranice
st.set_page_config(
    page_title="Katastarski upit - Trogir", 
    page_icon="🏛️",
    layout="wide",
    menu_items={
        'Get Help': 'https://www.ispu.hr',
        'Report a bug': "mailto:podrska@trogir.hr"
    }
)

# CSS prilagodbe
st.markdown("""
    <style>
    .stTextInput input, .stTextArea textarea, .stSelectbox div {
        border-radius: 8px !important;
        padding: 12px !important;
    }
    .stMarkdown h3 {
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 0.3rem;
    }
    .stButton button {
        width: 100%;
        transition: all 0.3s ease;
        background-color: #4CAF50 !important;
        color: white !important;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar s uputama
with st.sidebar:
    st.markdown("## 📚 Korisne upute")
    with st.expander("Kako koristiti aplikaciju?"):
        st.markdown("""
        1. Popunite osnovne podatke o čestici
        2. Odaberite relevantne planove uređenja
        3. Pritisnite "Pošalji upit"
        4. Pregledajte odgovor sustava
        """)
    
    st.markdown("## 🔗 Brzi linkovi")
    st.page_link("https://www.ispu.hr/", label="ISPU sustav", icon="🌐")
    st.page_link("https://www.trogir.hr/", label="Grad Trogir", icon="🏠")

# Glavni sadržaj
st.title("🏛️ Katastarski upit za područje Trogira")
st.markdown("*Pomoćni sustav za izradu katastarskih upita*")

# Forma za unos podataka
with st.form("katastarski_upit", border=True):
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown("### 📋 Osnovni podaci")
        
        # Redovi za kompaktniji unos
        r1 = st.columns(2)
        with r1[0]:
            parcel_number = st.text_input(
                "**🔢 Broj katastarske čestice**",
                placeholder="npr. 123/45",
                help="Unesite broj prema zemljišniku"
            )
        with r1[1]:
            parcel_area = st.number_input(
                "**📐 Kvadratura (m²)**",
                min_value=0.0,
                format="%.2f",
                help="Unesite kvadraturu prema vlasničkom listu"
            )
        
        st.markdown("### 🗺️ Lokacijski podaci")
        naselje = st.selectbox(
            "**🏘️ Naselje**",
            options=[
                "Arbanija", "Divulje", "Drvenik Mali", "Drvenik Veli",
                "Mastrinka", "Plano", "Trogir", "Žedno"
            ],
            index=6
        )
        
        st.selectbox(
            "**📑 UPU dokument**",
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
        
        st.selectbox(
            "**📄 DPU dokument**",
            options=[
                "DPU Brigi – Lokvice (DPU 5)",
                "DPU 1. faze obale od Madiracinog mula do Duhanke (DPU 4)"
            ],
            index=0
        )
        
        zona = st.text_input(
            "**🧭 Zona prema ISPU**",
            placeholder="npr. M1",
            help="Unesite oznaku zone prema grafičkom prikazu"
        )
    
    with col2:
        st.markdown("### 💬 Dodatni upit")
        additional_query = st.text_area(
            "Unesite dodatne napomene ili pitanja",
            height=250,
            placeholder="Opišite dodatne zahtjeve...",
            help="Maksimalno 500 znakova",
            max_chars=500
        )
    
    # Submit gumb
    submitted = st.form_submit_button(
        "🚀 Pošalji upit", 
        use_container_width=True
    )

# Obrada podataka nakon sl

