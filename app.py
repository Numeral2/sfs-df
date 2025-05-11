import streamlit as st
import requests

st.set_page_config(page_title="Katastarski upit – Trogir", layout="centered")

# Stilizacija stranice
st.markdown("""
    <style>
    .main {
        background-color: #f8f5f2;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stTextInput > div > div > input {
        background-color: #fff;
        border-radius: 0.5rem;
        border: 1px solid #ccc;
        padding: 0.6rem;
    }
    .stSelectbox > div > div {
        background-color: #fff;
        border-radius: 0.5rem;
        border: 1px solid #ccc;
        padding: 0.6rem;
    }
    </style>
""", unsafe_allow_html=True)

# Nulti korak - link prema ISPU stranici s uputama
st.markdown("""
    <h2 style='text-align: center; color: #333;'>Korak 0: Provjeri zonu na ISPU platformi</h2>
    <p style='text-align: center; color: #666;'>Prije nego nastaviš, provjeri u kojoj zoni se nalazi tvoje zemljište. Klikni na donji link kako bi otvorio ISPU platformu. Slijedi upute ispod kako bi pronašao odgovarajući sloj i zonu.</p>
    <p style='text-align: center;'>
    <a href="https://www.ispu.hr/" target="_blank" style="font-size: 16px; color: #0066cc; text-decoration: none;">Posjeti ISPU platformu</a>
    </p>
    <h4 style='text-align: center; color: #333;'>Upute:</h4>
    <ul style='text-align: center; color: #666;'>
        <li>1. Na stranici ISPU, u lijevom padajućem izborniku odaberi sloj \"Prostorni plan\".</li>
        <li>2. Uključi odgovarajući sloj za zonu koja te zanima (npr. \"Stambeno-poslovna zona\", \"Poslovna zona\", itd.).</li>
        <li>3. Provjeri boju na karti koja označava tvoju zonu. Najčešće žuta boja označava stambeno-poslovnu zonu (M1), dok je plava boja rezervirana za industrijske zone (M2).</li>
    </ul>
""", unsafe_allow_html=True)

# Glavni dio aplikacije
st.markdown("""
    <h2 style='text-align: center; color: #333;'>Katastarski upit za područje Grada Trogira</h2>
    <p style='text-align: center; color: #666;'>Popunite sve potrebne informacije kako bi se generirao strukturiran zahtjev za analiziranje čestice.</p>
    <hr style='border-top: 1px solid #bbb;'>
""", unsafe_allow_html=True)

with st.form("katastarski_form"):
    st.subheader("1. Podaci o čestici")
    col1, col2 = st.columns(2)
    with col1:
        parcel_number = st.text_input("Broj katastarske čestice", placeholder="npr. 1234/5")
    with col2:
        parcel_area = st.text_input("Kvadratura čestice (m²)", placeholder="npr. 545")

    st.subheader("2. Lokacija unutar Grada Trogira")
    col3, col4 = st.columns(2)
    with col3:
        naselje = st.selectbox("Naselje", [
            "Arbanija", "Divulje", "Drvenik Mali", "Drvenik Veli",
            "Mastrinka", "Plano", "Trogir", "Žedno"
        ])
    with col4:
        zona = st.text_input("Zona prema ISPU sustavu", placeholder="npr. M1, K1, R3")

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

    st.markdown("""<hr style='border-top: 1px solid #bbb;'>""", unsafe_allow_html=True)
    submitted = st.form_submit_button("Generiraj zahtjev")

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
    st.code(final_text, language="markdown")

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
