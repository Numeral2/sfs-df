import streamlit as st
import requests

# Custom CSS za poboljšani izgled
st.markdown("""
    <style>
    /* Glavni kontejner */
    .main {background-color: #f8f9fa;}
    
    /* Input polja */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        border-radius: 8px;
        border: 1px solid #dee2e6;
        transition: all 0.3s ease;
    }
    
    /* Hover efekti */
    .stTextInput input:hover, .stTextArea textarea:hover, .stSelectbox select:hover {
        border-color: #4CAF50;
        box-shadow: 0 0 8px rgba(76,175,80,0.2);
    }
    
    /* Naslovi */
    h1, h2, h3 {
        color: #2c3e50;
        margin-bottom: 1rem !important;
    }
    
    /* Gumbi */
    .stButton>button {
        border-radius: 8px;
        background: #4CAF50;
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border: none;
        transition: transform 0.2s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(76,175,80,0.3);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-right: 1px solid #dee2e6;
    }
    </style>
""", unsafe_allow_html=True)

# Postavke stranice
st.set_page_config(
    page_title="Katastarski upit - Trogir", 
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Sidebar sa uputama
with st.sidebar:
    st.markdown("## ℹ️ Upute za korištenje")
    st.markdown("""
    1. Popunite osnovne podatke o čestici
    2. Odaberite relevantne planove uređenja
    3. Pritisnite "Pošalji upit"
    4. Pregledajte odgovor sustava
    """)
    st.markdown("---")
    st.page_link("https://www.ispu.hr/", label="🌐 ISPU sustav", help="Grafički prikaz zona")
    st.page_link("https://www.trogir.hr/", label="🏠 Grad Trogir", help="Službene informacije")

# Glavni sadržaj
st.title("🏛️ Katastarski upit za područje Trogira")
st.caption("Digitalna obrada katastarskih upita - brzo i jednostavno")

# Nulti korak - ISPU upute
with st.expander("🔍 Kako pronaći zonu na ISPU sustavu?", expanded=True):
    st.markdown("""
    1. Otvorite [ISPU grafički prikaz](https://www.ispu.hr/)
    2. U izborniku slojeva odaberite **"Prostorni planovi"**
    3. Pronađite svoju parcelu na karti
    4. Zabilježite oznaku zone (npr. M1, K2)
    5. Pomoćne oznake boja:
        - 🟡 **Žuta**: Stambeno-poslovna zona (M1)
        - 🔴 **Crvena**: Komercijalne zone
        - 🔵 **Plava**: Industrijske zone
    """, unsafe_allow_html=True)

# Glavni layout
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    with st.container(border=True):
        st.markdown("### 📋 Podaci o čestici")
        
        # Grid layout za osnovne podatke
        col1a, col1b = st.columns(2)
        with col1a:
            parcel_number = st.text_input(
                "**🔢 Broj katastarske čestice**",
                placeholder="npr. 123/45",
                help="Unesite broj prema zemljišniku",
                key="parcel_number"
            )
        with col1b:
            parcel_area = st.text_input(
                "**📐 Kvadratura (m²)**",
                placeholder="npr. 250.50",
                help="Unesite kvadraturu prema vlasničkom listu",
                key="parcel_area"
            )
        
        # Lokacijski podaci
        naselje = st.selectbox(
            "**🏘️ Naselje**",
            options=[
                "Arbanija", "Divulje", "Drvenik Mali", "Drvenik Veli",
                "Mastrinka", "Plano", "Trogir", "Žedno"
            ],
            index=6,
            key="naselje"
        )
        
        # Planska dokumenta
        upu = st.selectbox(
            "**📑 UPU dokument**",
            options=[
                "", "UPU Krban", "UPU naselja Žedno", 
                "UPU poslovne zone POS 3 (UPU 10)",
                "UPU ugostiteljsko – turističke zone Sveti Križ (UPU 17)",
                "UPU naselja Mastrinka 1 (UPU 6.1)",
                "UPU poslovne zone POS 2 (UPU 15)",
                "UPU naselja Plano (UPU 18)", 
                "UPU proizvodne zone Plano 3 (UPU 7)"
            ],
            index=0,
            key="upu"
        )
        
        dpu = st.selectbox(
            "**📄 DPU dokument**",
            options=[
                "", "DPU Brigi – Lokvice (DPU 5)",
                "DPU 1. faze obale od Madiracinog mula do Duhanke (DPU 4)"
            ],
            index=0,
            key="dpu"
        )
        
        zona = st.text_input(
            "**🧭 Zona prema ISPU**",
            placeholder="npr. M1",
            help="Unesite oznaku zone prema grafičkom prikazu",
            key="zone"
        )
        
        additional_query = st.text_area(
            "**💬 Dodatni upit**",
            placeholder="Opišite dodatne zahtjeve...",
            height=100,
            key="additional_query"
        )

with col2:
    with st.container(border=True):
        st.markdown("### 🤖 Interaktivni odgovor")
        
        # Generiranje upita
        combined_input = f"""**Katastarski upit za česticu {parcel_number}**
        
        - **Lokacija**: {naselje}
        - **Kvadratura**: {parcel_area} m²
        - **Zona**: {zona}
        - **Dodatni upit**: {additional_query or 'Nema dodatnog upita'}
        """
        
        # Prikaz i slanje upita
        with st.form("webhook_form"):
            user_input = st.text_area(
                "Upit za sustav",
                value=combined_input.strip(),
                height=250,
                key="user_input_box"
            )
            
            if st.form_submit_button(
                "🚀 Pošalji upit", 
                use_container_width=True,
                type="primary"
            ):
                with st.spinner("Šaljem podatke..."):
                    try:
                        response = requests.post(
                            "https://primary-production-b791f.up.railway.app/webhook-test/03419cdb-f956-48b4-85d8-725a6a4db8fb",
                            json={"text": user_input},
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            st.success("✅ Upit uspješno poslan!")
                            try:
                                st.markdown("### 📬 Odgovor sustava")
                                st.json(response.json())
                            except:
                                st.markdown("**📝 Tekstualni odgovor:**")
                                st.code(response.text, language="text")
                        else:
                            st.error(f"❌ Greška {response.status_code}: {response.text}")
                            
                    except Exception as e:
                        st.error(f"❌ Greška u komunikaciji: {str(e)}")
