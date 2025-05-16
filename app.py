import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import json

# === POSTAVI SVOJ WEBHOOK URL OVDJE ===
N8N_WEBHOOK_URL = "https://primary-production-b791f.up.railway.app/webhook-test/839b893b-f460-479c-9295-5f3bb8ab3488"

st.set_page_config(page_title="Katastarski upitnik Trogir", layout="wide", page_icon="🏗️")

# === Funkcija za učitavanje lokalne Lottie animacije ===
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception:
        return None

# === Učitaj animaciju i slike ===
lottie_animation = load_lottiefile("header_animation.json")
tlocrt_img = Image.open("tlocrt_example.png") if "tlocrt_example.png" else None  # zamijeni ako je drugačije ime

# === Naslov i animacija ===
col_hero1, col_hero2 = st.columns([2, 1])
with col_hero1:
    st.title("🏗️ Katastarski podaci - Grad Trogir")
    st.markdown("""
    Dobijte sve informacije o vašoj čestici na jednom mjestu. Unesite osnovne podatke, a mi ćemo izračunati:
    - 🧮 **KIS** (Koeficijent iskoristivosti)** – koliko ukupno možete izgraditi
    - 📐 **KIG** (Koeficijent izgrađenosti)** – koliki može biti tlocrt objekta
    - 🏢 Katnost, udaljenosti, visine, uvjeti gradnje i više!
    """)

with col_hero2:
    if lottie_animation:
        st_lottie(lottie_animation, height=250, key="header_animation")
    else:
        st.info("🎬 Animacija trenutno nije dostupna.")

st.markdown("---")

# === Glavni dio forme ===
col1, col2 = st.columns([3, 2])

with col1:
    with st.form("katastar_form"):
        st.subheader("📋 Unos podataka")
        broj_cestice = st.text_input("📌 Broj katastarske čestice *", help="Unesite broj iz zemljišnika")
        kvadratura = st.number_input("📏 Kvadratura čestice (m²) *", min_value=0.0, format="%.2f")

        st.subheader("🗺️ Lokacija i zona")
        naselje = st.selectbox("🏘️ Naselje *", options=[
            "Arbanija", "Divulje", "Drvenik Mali", "Drvenik Veli",
            "Mastrinka", "Plano", "Trogir", "Žedno"
        ])

        upu = st.selectbox("📑 UPU *", options=[
            "UPU Krban",
            "UPU naselja Žedno",
            "UPU poslovne zone POS 3 (UPU 10)",
            "UPU ugostiteljsko – turističke zone Sveti Križ (UPU 17)",
            "UPU naselja Mastrinka 1 (UPU 6.1)",
            "UPU poslovne zone POS 2 (UPU 15)",
            "UPU naselja Plano (UPU 18)",
            "UPU proizvodne zone Plano 3 (UPU 7)"
        ])

        dpu = st.selectbox("📄 DPU *", options=[
            "DPU Brigi – Lokvice (DPU 5)",
            "DPU 1.faze obale od Madiracnog mula do Duhanke (DPU 4)"
        ])

        zona = st.selectbox("📌 Zona *", options=[
            "Zona A - Historijska jezgra",
            "Zona B - Zaštitni pojas",
            "Zona C - Suvremeni razvoj"
        ])

        dodatni_upit = st.text_area("📝 Dodatni upit (opcionalno)", height=100)

        submitted = st.form_submit_button("📨 Pošalji")

with col2:
    st.subheader("📊 Vizualizacija - Tlocrt")
    if tlocrt_img:
        st.image(tlocrt_img, caption="Primjer tlocrta građevinske čestice", use_column_width=True)
    st.subheader("📨 Odgovor sustava")
    output_placeholder = st.empty()

# === Slanje podataka ===
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

            output_placeholder.code(response.text)
            st.success("✅ Podaci uspješno poslani!")
            st.balloons()

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Greška pri slanju: {str(e)}")
