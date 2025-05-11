import streamlit as st

st.set_page_config(page_title="Katastarski Upit - Trogir", layout="centered")

# CSS za izgled aplikacije
st.markdown("""
    <style>
    /* Globalni stilovi */
    .main {
        background: linear-gradient(135deg, #f4f2ec, #d6d4c9); /* Zemljani tonovi */
        color: #2b2a2a; /* Tamno smeđa boja za tekst */
        font-family: 'Arial', sans-serif;
    }
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Stilovi za tekstualne elemente */
    h2, h4 {
        color: #5f4b3b; /* Topla tamno smeđa za naslove */
        text-align: center;
        font-weight: 700;
    }
    p, ul {
        color: #7d6a4e; /* Svjetlija smeđa za tekst */
        text-align: center;
        font-size: 16px;
    }
    a {
        color: #ba9d5b; /* Zlato žuta za linkove */
        text-decoration: none;
        font-weight: 600;
    }
    a:hover {
        color: #d1b07b; /* Svjetlija žuta pri hoveru */
        text-decoration: underline;
    }

    /* Stil za formu */
    .stTextInput > div > div > input {
        background-color: #f0ebe1; /* Svijetli bež za inpute */
        border: 2px solid #d1b07b; /* Zlata boja za granicu */
        padding: 0.8rem;
        border-radius: 0.8rem;
    }
    .stSelectbox > div > div {
        background-color: #f0ebe1;
        border: 2px solid #d1b07b;
        padding: 0.8rem;
        border-radius: 0.8rem;
    }

    /* Posebni stilovi za gumb za slanje */
    .stButton > button {
        background-color: #ba9d5b; /* Zlato žuta boja za gumb */
        color: white;
        border-radius: 1.5rem;
        font-weight: 600;
        padding: 0.8rem 2rem;
        font-size: 18px;
    }
    .stButton > button:hover {
        background-color: #d1b07b;
    }

    /* Stilovi za prikazivanje generiranog teksta */
    .stCode {
        background-color: #f4f2ec;
        border: 2px solid #d1b07b;
        border-radius: 1rem;
        padding: 1rem;
        font-family: 'Courier New', Courier, monospace;
        font-size: 16px;
        color: #5f4b3b;
    }

    /* Animacije */
    .animated-btn {
        animation: fadeIn 1s ease-in-out;
    }

    /* Animacija za gumbe */
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }

    </style>
""", unsafe_allow_html=True)

# Glavni dio aplikacije
st.markdown("""
    <h2>Katastarski Upit za Grad Trogir</h2>
    <p>Popunite informacije o čestici kako bi generirali zahtjev za analizu.</p>
    <hr style='border-top: 2px solid #d1b07b;'>
""", unsafe_allow_html=True)

with st.form("katastarski_form"):
    # Prvi korak - Podaci o čestici
    st.subheader("1. Podaci o čestici")
    col1, col2 = st.columns(2)
    with col1:
        parcel_number = st.text_input("Broj katastarske čestice", placeholder="npr. 1234/5")
    with col2:
        parcel_area = st.text_input("Kvadratura čestice (m²)", placeholder="npr. 545")

    # Drugi korak - Lokacija
    st.subheader("2. Lokacija unutar Grada Trogira")
    col3, col4 = st.columns(2)
    with col3:
        naselje = st.selectbox("Naselje", [
            "Arbanija", "Divulje", "Drvenik Mali", "Drvenik Veli",
            "Mastrinka", "Plano", "Trogir", "Žedno"
        ])
    with col4:
        zona = st.text_input("Zona prema ISPU sustavu", placeholder="npr. M1, K1, R3")

    # Treći korak - Prostorni planovi
    st.subheader("3. Planovi prostornog uređenja")
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

    # Webhook opcionalno
    webhook_url = "https://primary-production-b791f.up.railway.app/webhook-test/03419cdb-f956-48b4-85d8-725a6a4db8fb"
    try:
        response = requests.post(webhook_url, json={"text": final_text})
        if response.status_code == 200:
            st.success("Zahtjev uspješno poslan.")
            try:
                data = response.json()
                st.markdown("### 📬 Odgovor:")
                st.markdown(data.get("response", "⚠️ Nema teksta u odgovoru."))
            except:
                st.text(response.text)
        else:
            st.error(f"Greška kod slanja: {response.status_code}")
    except Exception as e:
        st.error(f"Došlo je do greške: {e}")
