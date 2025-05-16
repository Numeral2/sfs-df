import streamlit as st
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Katastarski upitnik Trogir", layout="wide", page_icon="🏠")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_house = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_j1adxtyb.json")

st.markdown("""
<style>
    .main {background-color: #f5f5f5;}
    .block-container {padding-top: 1rem;}
    .css-1d391kg {background-color: #fff; border-radius: 10px; padding: 2rem;}
</style>
""", unsafe_allow_html=True)

st.title("🏠 Katastarski tlocrt - Grad Trogir")
st.markdown("Unesite podatke kao da gradite svoj dom - svaka prostorija je važna!")

cols = st.columns([1,2,1])
with cols[0]:
    st_lottie(lottie_house, height=220)
with cols[1]:
    with st.form("katastar_form"):
        st.header("📋 Vaši podaci (Ulaz u kuću)")
        broj_cestice = st.text_input("Broj katastarske čestice *")
        kvadratura = st.number_input("Kvadratura čestice (m²) *", min_value=0.0, format="%.2f")
        
        st.header("🗺️ Lokacija (Dnevni boravak)")
        naselje = st.selectbox("Naselje *", ["Arbanija", "Divulje", "Drvenik Mali", "Drvenik Veli", "Mastrinka", "Plano", "Trogir", "Žedno"])
        upu = st.selectbox("UPU *", ["UPU Krban", "UPU naselja Žedno", "UPU poslovne zone POS 3 (UPU 10)", "UPU ugostiteljsko – turističke zone Sveti Križ (UPU 17)", "UPU naselja Mastrinka 1 (UPU 6.1)", "UPU poslovne zone POS 2 (UPU 15)", "UPU naselja Plano (UPU 18)", "UPU proizvodne zone Plano 3 (UPU 7)"])
        dpu = st.selectbox("DPU *", ["DPU Brigi – Lokvice (DPU 5)", "DPU 1.faze obale od Madiracnog mula do Duhanke (DPU 4)"])
        zona = st.selectbox("Zona *", ["Zona A - Historijska jezgra", "Zona B - Zaštitni pojas", "Zona C - Suvremeni razvoj"])
        dodatni_upit = st.text_area("Dodatni upit (opcionalno)", height=80)
        submitted = st.form_submit_button("📨 Pošalji podatke")
with cols[2]:
    st.info("🏗️ Zamislite da popunjavate tlocrt svog budućeg doma!")

if submitted:
    if not all([broj_cestice, kvadratura, naselje, upu, dpu, zona]):
        st.error("Molimo ispunite sva obavezna polja.")
    else:
        st.success("✅ Podaci uspješno poslani! Pogledajte svoj 'tlocrt' niže.")
        st.balloons()
        # Ovdje možeš prikazati vizualizaciju "tlocrt" rezultata

# Primjer prikaza rezultata kao tlocrt
st.markdown("---")
st.header("📐 Vaš tlocrt - rezultati")
colA, colB, colC = st.columns(3)
with colA:
    st.metric("KIS", "0.4", "Koef. iskoristivosti")
    st.metric("KIG", "0.25", "Koef. izgrađenosti")
with colB:
    st.image("https://cdn.pixabay.com/photo/2017/01/31/13/14/architecture-2026083_1280.png", caption="Primjer tlocrta", use_column_width=True)
with colC:
    st.metric("Katnost", "P+1", "Broj katova")
    st.metric("Max visina", "7.5 m", "Dozvoljena visina")

