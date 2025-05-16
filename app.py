import streamlit as st
import requests
from streamlit_lottie import st_lottie

# Postavke stranice
st.set_page_config(
    page_title="Katastarski upitnik Trogir",
    layout="wide",
    page_icon="🏠"
)

# Funkcija za učitavanje Lottie animacije s URL-a
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        st.warning(f"Greška pri učitavanju animacije: {e}")
        return None

# Učitavanje animacije
lottie_house = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_j1adxtyb.json")

# Custom CSS za izgled
st.markdown("""
    <style>
        .main {background-color: #f5f5f5;}
        .block-container {padding-top: 1rem;}
        .css-1d391kg {background-color: #fff; border-radius: 10px; padding: 2rem;}
    </style>
""", unsafe_allow_html=True)

st.title("🏠 Katastarski tlocrt - Grad Trogir")
st.markdown("Unesite podatke kao da gradite svoj dom - svaka prostorija je važna!")

# Layout s tri kolone
cols = st.columns([1, 2, 1])

with cols[0]:
    if lottie_house:
        st_lottie(lottie_house, height=220, key="house")
    else:
        st.info("Animacija nije dostupna.")

with cols[1]:
    with st.form("katastar_form"):
        st.header("📋 Vaši podaci (Ulaz u kuću)")
        broj_cestice = st.text_input("Broj katastarske čestice *")
        kvadratura = st.number_input("Kvadratura čestice (m²) *", min_value=0.0, format="%.2f")

        st.header("🗺️ Lokacija (Dnevni boravak)")
        naselja = [
            "Arbanija", "Divulje", "Drvenik Mali", "Drvenik Veli",
            "Mastrinka", "Plano", "Trogir", "Žedno"
        ]
        naselje = st.selectbox("Naselje *", naselja)

        upu_opcije = [
            "UPU Krban", "UPU naselja Žedno", "UPU poslovne zone POS 3 (UPU 10)",
            "UPU ugostiteljsko – turističke zone Sveti Križ (UPU 17)",
            "UPU naselja Mastrinka 1 (UPU 6.1)", "UPU poslovne zone POS 2 (UPU 15)",
            "UPU naselja Plano (UPU 18)", "UPU proizvodne zone Plano 3 (UPU 7)"
        ]
        upu = st.selectbox("UPU *", upu_opcije)

        dpu_opcije = [
            "DPU Brigi – Lokvice (DPU 5)",
            "DPU 1.faze obale od Madiracnog mula do Duhanke (DPU 4)"
        ]
        dpu = st.selectbox("DPU *", dpu_opcije)

        zona_opcije = [
            "Zona A - Historijska jezgra",
            "Zona B - Zaštitni pojas",
            "Zona C - Suvremeni razvoj"
        ]
        zona = st.selectbox("Zona *", zona_opcije)

        dodatni_upit = st.text_area("Dodatni upit (opcionalno)", height=80)
        submitted = st.form_submit_button("📨 Pošalji podatke")

with cols[2]:
    st.info("🏗️ Zamislite da popunjavate tlocrt svog budućeg doma!")

# Provjera i prikaz rezultata
if submitted:
    if not broj_cestice or kvadratura == 0.0 or not naselje or not upu or not dpu or not zona:
        st.error("Molimo ispunite sva obavezna polja.")
    else:
        st.success("✅ Podaci uspješno poslani! Pogledajte svoj 'tlocrt' niže.")
        st.balloons()
        # Ovdje možeš prikazati vizualizaciju "tlocrt" rezultata

# Prikaz rezultata
st.markdown("---")
st.header("📐 Vaš tlocrt - rezultati")
colA, colB, colC = st.columns(3)
with colA:
    st.metric("KIS", "0.4", "Koef. iskoristivosti")
    st.metric("KIG", "0.25", "Koef. izgrađenosti")
with colB:
    st.image(
        "https://cdn.pixabay.com/photo/2017/01/31/13/14/architecture-2026083_1280.png",
        caption="Primjer tlocrta",
        use_column_width=True
    )
with colC:
    st.metric("Katnost", "P+1", "Broj katova")
    st.metric("Max visina", "7.5 m", "Dozvoljena visina")
