import streamlit as st
import requests

st.set_page_config(page_title="Katastarski upit - Trogir", layout="centered")
st.markdown("<h2 style='text-align: center;'>📍 Katastarski upit – Grad Trogir</h2>", unsafe_allow_html=True)
st.markdown("Ispunite formu kako bi se automatski generirao tekst koji bot može razumjeti.")

with st.form("katastarski_upit"):
    col1, col2 = st.columns(2)
    with col1:
        parcel_number = st.text_input("🔢 Katastarska čestica", placeholder="npr. 1234/5")
    with col2:
        parcel_area = st.text_input("📐 Kvadratura (m²)", placeholder="npr. 545")

    col3, col4 = st.columns(2)
    with col3:
        naselje = st.selectbox("🏘️ Naselje", [
            "Arbanija", "Divulje", "Drvenik Mali", "Drvenik Veli",
            "Mastrinka", "Plano", "Trogir", "Žedno"
        ])
    with col4:
        zone = st.text_input("🧭 Zona (ISPU)", placeholder="npr. M1, K1, R3...")

    col5, col6 = st.columns(2)
    with col5:
        upu = st.selectbox("🏗️ UPU (ako postoji)", [
            "", "UPU Krban", "UPU naselja Žedno",
            "UPU poslovne zone POS 3 (UPU 10)",
            "UPU ugostiteljsko – turističke zone Sveti Križ (UPU 17)",
            "UPU naselja Mastrinka 1 (UPU 6.1)",
            "UPU poslovne zone POS 2 (UPU 15)",
            "UPU naselja Plano (UPU 18)",
            "UPU proizvodne zone Plano 3 (UPU 7)"
        ])
    with col6:
        dpu = st.selectbox("📄 DPU (ako postoji)", [
            "", "DPU Brigi – Lokvice (DPU 5)",
            "DPU 1. faze obale od Madiracinog mula do Duhanke (DPU 4)"
        ])

    st.markdown("---")
    submitted = st.form_submit_button("📤 Generiraj i pošalji upit")

if submitted:
    final_text = f"""
Molim te izvuci informacije za ovu katastarsku česticu:

1. Broj katastarske čestice: {parcel_number}
2. Kvadratura katastarske čestice: {parcel_area} m²
3. Područje: Grad Trogir
   - Naselje: {naselje}
   - UPU: {upu or 'nije navedeno'}
   - DPU: {dpu or 'nije navedeno'}
4. Zona prema ISPU sustavu: {zone}

Na temelju ovih podataka, molim te izvuci informacije iz odgovarajućih planova i PDF-ova.
""".strip()

    st.markdown("### 📝 Generirani upit:")
    st.code(final_text, language="markdown")

    webhook_url = "https://primary-production-b791f.up.railway.app/webhook-test/03419cdb-f956-48b4-85d8-725a6a4db8fb"

    try:
        response = requests.post(webhook_url, json={"text": final_text})

        if response.status_code == 200:
            st.success("✅ Upit poslan bota!")
            try:
                data = response.json()
                st.markdown("### 📬 Odgovor bota:")
                st.markdown(data.get("response", "⚠️ Nema teksta u odgovoru."))
            except:
                st.text(response.text)
        else:
            st.error(f"❌ Greška kod slanja ({response.status_code})")
    except Exception as e:
        st.error(f"⚠️ Došlo je do greške: {e}")
