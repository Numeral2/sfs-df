import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json

# === POSTAVI SVOJ WEBHOOK URL OVDJE ===
N8N_WEBHOOK_URL = "https://primary-production-b791f.up.railway.app/webhook-test/839b893b-f460-479c-9295-5f3bb8ab3488"

st.set_page_config(page_title="Katastarski podaci - unos", layout="wide")

# === Lottie animacija funkcija ===
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_animation = load_lottieurl("https://lottie.host/8b77f137-57c2-4d66-8990-c99810411c74/8kY0WMaL2M.json")

# === Sidebar ===
with st.sidebar:
    st.header("Što možete saznati?")
    st.markdown("""
    - **KIS**: maksimalna ukupna kvadratura svih etaža (*KIS × površina parcele*)  
    - **KIG**: maksimalna tlocrtna kvadratura zgrada (*KIG × površina parcele*)  
    - **Katnost**: koliko etaža je dozvoljeno  
    - **Visina**: maksimalna visina vijenca krova ili građevine  
    - **Udaljenosti**: od regulacijske linije i susjednih čestica  
    - **Ostalo**: uvjeti za okućnicu, parkirna mjesta, ozelenjene površine i građevine bez dozvole (npr. garaža, kamin)  
    """)

st.title("📐 Katastarski upitnik za grad Trogir")

st_lottie(lottie_animation, speed=1, width=800, height=250, key="header_anim")

col1, col2 = st.columns([2, 1])

with col1:
    with st.form("katastar_form"):
        st.subheader("🗂️ Unesite podatke")

        broj_cestice = st.text_input("📄 Broj katastarske čestice *", help="Unesite broj iz zemljišnika")
        kvadratura = st.number_input("📏 Kvadratura čestice (m²) *", min_value=0.0, format="%.2f")

        st.markdown("---")

        naselje = st.selectbox("🏘️ Naselje *", options=[
            "Arbanija", "Divulje", "Drvenik Mali", "Drvenik Veli",
            "Mastrinka", "Plano", "Trogir", "Žedno"
        ])

        upu = st.selectbox("📐 UPU plan *", options=[
            "UPU Krban", "UPU naselja Žedno", "UPU poslovne zone POS 3 (UPU 10)",
            "UPU ugostiteljsko – turističke zone Sveti Križ (UPU 17)",
            "UPU naselja Mastrinka 1 (UPU 6.1)", "UPU poslovne zone POS 2 (UPU 15)",
            "UPU naselja Plano (UPU 18)", "UPU proizvodne zone Plano 3 (UPU 7)"
        ])

        dpu = st.selectbox("📌 DPU plan *", options=[
            "DPU Brigi – Lokvice (DPU 5)",
            "DPU 1.faze obale od Madiracnog mula do Duhanke (DPU 4)"
        ])

        zona = st.selectbox("📊 Zona *", options=[
            "Zona A - Historijska jezgra",
            "Zona B - Zaštitni pojas",
            "Zona C - Suvremeni razvoj"
        ])

        dodatni_upit = st.text_area("✏️ Dodatni upit (neobavezno)", height=100)

        submitted = st.form_submit_button("📨 Pošalji upit")

with col2:
    st.subheader("📬 Odgovor sustava")
    output_placeholder = st.empty()
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Tlocrt_kuce.png/640px-Tlocrt_kuce.png", caption="Primjer tlocrta")

if submitted:
    if not all([broj_cestice, kvadratura, naselje, upu, dpu, zona]):
        st.error("Molimo ispunite sva obavezna polja (označena zvjezdicom *)")
    else:
        combined_input = (
            f"Broj katastarske čestice: {broj_cestice}\n"
            f"Kvadratura: {kvadratura} m²\n"
            f"Naselje: {naselje}\n"
            f"UPU: {upu}\n"
            f"DPU: {dpu}\n"
            f"Zona: {zona}\n"
        )
        if dodatni_upit:
            combined_input += f"Dodatni upit: {dodatni_upit}\n"

        payload = {"combined_input": combined_input}

        try:
            response = requests.post(
                N8N_WEBHOOK_URL,
                json=payload,
                timeout=15,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            output_placeholder.success(response.text)
            st.balloons()
        except requests.exceptions.RequestException as e:
            st.error(f"Greška pri slanju: {str(e)}")
