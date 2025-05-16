import streamlit as st
import requests
from streamlit_lottie import st_lottie

# === POSTAVI SVOJ WEBHOOK URL OVDJE ===
N8N_WEBHOOK_URL = "https://primary-production-b791f.up.railway.app/webhook-test/839b893b-f460-479c-9295-5f3bb8ab3488"

st.set_page_config(
    page_title="Katastarski upitnik Trogir",
    layout="wide",
    page_icon="🏗️",
    initial_sidebar_state="expanded"
)

# === Funkcija za učitavanje Lottie animacije ===
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        st.warning(f"Greška pri učitavanju animacije: {e}")
        return None

# === Lottie animacije za različite stranice ===
lottie_home = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_1pxqjqps.json")
lottie_about = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_j1adxtyb.json")
lottie_contact = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_2LdLq6.json")

# === Navigacija ===
def main():
    st.sidebar.title("Navigacija")
    page = st.sidebar.radio("Izaberi stranicu:", ["🏠 Početna", "ℹ️ O nama", "📞 Kontakt"])

    if page == "🏠 Početna":
        home_page()
    elif page == "ℹ️ O nama":
        about_page()
    elif page == "📞 Kontakt":
        contact_page()

# === HOME PAGE ===
def home_page():
    col_hero1, col_hero2 = st.columns([2, 1])
    with col_hero1:
        st.title("🏗️ Katastarski podaci - Grad Trogir")
        st.markdown("""
        Dobijte sve informacije o vašoj čestici na jednom mjestu. Unesite osnovne podatke, a mi ćemo izračunati:
        - 🧮 **KIS** (Koeficijent iskoristivosti) – koliko ukupno možete izgraditi
        - 📐 **KIG** (Koeficijent izgrađenosti) – koliki može biti tlocrt objekta
        - 🏢 Katnost, udaljenosti, visine, uvjeti gradnje i više!
        """)
    with col_hero2:
        if lottie_home:
            st_lottie(lottie_home, height=250, key="header_animation")

    st.markdown("---")

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

# === ABOUT PAGE ===
def about_page():
    st.title("ℹ️ O nama")
    st.markdown("""
    Dobijte sve informacije o vašoj čestici na jednom mjestu. Unesite osnovne podatke, a mi ćemo izračunati:
    - 🧮 **KIS** (Koeficijent iskoristivosti) – koliko ukupno možete izgraditi
    - 📐 **KIG** (Koeficijent izgrađenosti) – koliki može biti tlocrt objekta
    - 🏢 Katnost, udaljenosti, visine, uvjeti gradnje i više!

    Dobrodošli na Katastarski upitnik za Grad Trogir!  
    Naša misija je pružiti transparentne i brze informacije o katastarskim podacima,  
    kako bi građani i profesionalci mogli donositi bolje odluke vezane uz nekretnine i gradnju.

    **Što nudimo?**
    - Jednostavan i brz upitnik za katastarske podatke
    - Automatsko slanje podataka na backend sustav za daljnju obradu
    - Podršku i savjete u području prostornog planiranja

    Hvala što koristite naš servis!
    """)
    if lottie_about:
        st_lottie(lottie_about, height=300)

# === CONTACT PAGE ===
def contact_page():
    st.title("📞 Kontakt")
    st.markdown("""
    Imate pitanja ili trebate pomoć?  
    Kontaktirajte nas putem obrasca ispod ili na navedene kontakte.

    - 📧 Email: info@katastar-trogir.hr  
    - 📞 Telefon: +385 21 123 456  
    - 📍 Adresa: Trg Republike Hrvatske 1, Trogir
    """)

    with st.form("contact_form"):
        name = st.text_input("Vaše ime *")
        email = st.text_input("Vaša email adresa *")
        message = st.text_area("Poruka *", height=150)
        send = st.form_submit_button("Pošalji poruku")

    if send:
        if not all([name, email, message]):
            st.error("Molimo ispunite sva obavezna polja.")
        else:
            # Ovdje možeš dodati slanje emaila ili webhook
            st.success(f"Hvala, {name}! Vaša poruka je primljena.")
            st.balloons()

    if lottie_contact:
        st_lottie(lottie_contact, height=250)

if __name__ == "__main__":
    main()
