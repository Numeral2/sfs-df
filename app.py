import streamlit as st

st.set_page_config(page_title="Prostorni Plan Trogir", layout="centered")

# CSS za izgled aplikacije
st.markdown("""
    <style>
    /* Globalni stilovi */
    .main {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f4; /* Svijetla pozadina */
        color: #333333; /* Tamna boja za tekst */
    }

    .block-container {
        padding: 2rem;
        background-color: white;
        border-radius: 1rem;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* Blaga sjena za uočljivost */
        margin-top: 2rem;
    }

    /* Stilovi za tekstualne elemente */
    h2, h4 {
        text-align: center;
        font-weight: 700;
    }
    p {
        text-align: center;
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Stil za formu */
    .stTextInput > div > div > input {
        background-color: #fff;
        border: 1px solid #ccc;
        padding: 0.8rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        width: 100%;
    }
    .stSelectbox > div > div {
        background-color: #fff;
        border: 1px solid #ccc;
        padding: 0.8rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        width: 100%;
    }

    /* Posebni stilovi za gumb za slanje */
    .stButton > button {
        background-color: #5c6bc0;
        color: white;
        border-radius: 1rem;
        font-weight: 600;
        padding: 0.8rem 2rem;
        font-size: 18px;
        margin-top: 1rem;
    }
    .stButton > button:hover {
        background-color: #3f4d9d;
    }

    /* Stil za prikazivanje generiranog teksta */
    .stCode {
        background-color: #fff;
        border: 1px solid #ccc;
        border-radius: 1rem;
        padding: 1rem;
        font-family: 'Courier New', Courier, monospace;
        font-size: 16px;
        color: #333;
        margin-top: 2rem;
    }

    /* Raspored za formu */
    .form-section {
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Glavni dio aplikacije
st.markdown("""
    <h2>Prostorni Plan za Grad Trogir</h2>
    <p>Upišite podatke o katastarskoj čestici kako biste generirali relevantne informacije iz prostornog plana.</p>
    <hr style='border-top: 2px solid #5c6bc0;'>
""", unsafe_allow_html=True)

with st.form("katastarski_form"):
    # Prvi korak - Podaci o čestici
    st.markdown("<h4>1. Podaci o čestici</h4>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        parcel_number = st.text_input("Broj katastarske čestice", placeholder="npr. 1234/5")
    with col2:
        parcel_area = st.text_input("Kvadratura čestice (m²)", placeholder="npr. 545")

    # Drugi korak - Lokacija
    st.markdown("<h4>2. Lokacija unutar Grada Trogira</h4>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        naselje = st.selectbox("Naselje", [
            "Arbanija", "Divulje", "Drvenik Mali", "Drvenik Veli",
            "Mastrinka", "Plano", "Trogir", "Žedno"
        ])
    with col4:
        zona = st.text_input("Zona prema ISPU sustavu", placeholder="npr. M1, K1, R3")

    # Treći korak - Prostorni planovi
    st.markdown("<h4>3. Planovi prostornog uređenja</h4>", unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        upu = st.selectbox("UPU (ako postoji)", [
            "", "UPU Krban", "UPU naselja Žedno",
            "UPU poslovne zone POS 3 (UPU 10)",
            "UPU ugostiteljsko – turističke zone Sveti Križ (UPU 17)",
            "UPU naselja Mastrinka 1 (UPU 6.1)",
            "UPU poslovne zone POS 2 (UPU 15)",
            "UPU naselja Plano (UPU 18)",
            "UPU proizvodne zone Plano 3 (UPU 7)"
        ])
    with col6:
        dpu = st.selectbox("DPU (ako postoji)", [
            "", "DPU Brigi – Lokvice (DPU 5)",
            "DPU 1. faze obale od Madiracinog mula do Duhanke (DPU 4)"
        ])

    # Gumb za slanje
    submitted = st.form_submit_button("Generiraj zahtjev", use_container_width=True)

if submitted:
    final_text = f"""
Molim vas da na temelju niže navedenih informacija izvučete sve relevantne prostorno-planske podatke:

1. Broj katastarske čestice: {parcel_number}
2. Kvadratura katastarske čestice: {parcel_area} m²
3. Područje: Grad Trogir
   - Naselje: {naselje}
   - Zona (ISPU): {zona}
4. UPU: {upu if upu else 'nije navedeno'}
5. DPU: {dpu if dpu else 'nije navedeno'}

Zahvaljujem unaprijed na uvidu u relevantne dokumente i planove.
    """.strip()

    st.markdown("### ✅ Generirani tekstualni zahtjev:")
    st.code(final_text, language="markdown", class_="stCode")
