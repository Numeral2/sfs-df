import streamlit as st
import streamlit_authenticator as stauth
import requests

# Konfiguracija stranice
st.set_page_config(page_title="Katastarski upit - Trogir", layout="wide")

# --- Autentifikacija ---
names = ['Ivan Horvat']
usernames = ['ivan']
passwords = ['123']  # Demo lozinka

# Hashiranje lozinki
hashed_passwords = stauth.Hasher(passwords).generate()

credentials = {
    'usernames': {
        usernames[0]: {
            'name': names[0],
            'password': hashed_passwords[0]
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    'katastar_trogir_app',
    'abcdef',
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login('Prijava', 'main')

# --- Stilizacija ---
st.markdown("""
    <style>
    body {
        background-color: #f5f7fa;
    }
    .block-container {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stTextInput > div > input, .stSelectbox > div, .stTextArea > div > textarea {
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 10px;
    }
    button {
        background-color: #2980b9 !important;
        color: white !important;
        border-radius: 8px !important;
    }
    .stTextInput input {width: 150px;}
    .stSelectbox select {width: 150px;}
    .stTextArea textarea {width: 300px;}
    </style>
""", unsafe_allow_html=True)

# --- Glavni sadržaj ---
if authentication_status:
    authenticator.logout('Odjava', 'sidebar')
    st.sidebar.success(f'Prijavljeni ste kao: {name}')

    # Zaglavlje
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e2/Trogir_Harbor_Panorama.jpg", use_column_width=True)
    st.title("📄 Katastarski upit za područje Trogira")
    st.markdown("""
        Ovdje možete unijeti potrebne informacije kako bismo obradili vaš katastarski upit za područje Trogira. 
        Molimo vas da ispunite sve relevantne podatke kako bi upit bio što precizniji.
    """)

    # Nulti korak
    st.markdown("### 🔗 Nulti korak: Provjerite zonu na ISPU sustavu")
    st.markdown("""
        Pogledajte **[ISPU grafički prikaz](https://www.ispu.hr/)** i odredite kojoj zoni pripada vaša čestica:
        - Žuta: Stambeno-poslovna zona (M1)
        - Crvena: Komercijalne zone
        - Plava: Industrijske zone
    """, unsafe_allow_html=True)

    # Layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📝 Podaci o katastarskoj čestici")

        parcel_number = st.text_input("🔢 Broj katastarske čestice", placeholder="Broj kat. čestice", key="parcel_number")
        parcel_area = st.text_input("📐 Kvadratura (m²)", placeholder="Kvadratura u m²", key="parcel_area")

        naselje = st.selectbox("Naselje", [
            "Arbanija", "Divulje", "Drvenik Mali", "Drvenik Veli",
            "Mastrinka", "Plano", "Trogir", "Žedno"
        ], key="naselje", index=6)

        upu = st.selectbox("UPU", [
            "", "UPU Krban", "UPU naselja Žedno", "UPU poslovne zone POS 3 (UPU 10)",
            "UPU ugostiteljsko – turističke zone Sveti Križ (UPU 17)",
            "UPU naselja Mastrinka 1 (UPU 6.1)", "UPU poslovne zone POS 2 (UPU 15)",
            "UPU naselja Plano (UPU 18)", "UPU proizvodne zone Plano 3 (UPU 7)"
        ], key="upu", index=0)

        dpu = st.selectbox("DPU", [
            "", "DPU Brigi – Lokvice (DPU 5)", 
            "DPU 1. faze obale od Madiracinog mula do Duhanke (DPU 4)"
        ], key="dpu", index=0)

        zone = st.text_input("🧭 Zona", placeholder="Zona iz ISPU sustava", key="zone")
        additional_query = st.text_area("💬 Dodatni upit", placeholder="Dodatni upit ili napomena", height=100, key="additional_query")

        combined_input = f"""
Grad: Trogir
Katastarska čestica: {parcel_number}
Kvadratura: {parcel_area} m²
Naselje: {naselje}
UPU: {upu or 'nije odabrano'}
DPU: {dpu or 'nije odabrano'}
Zona: {zone}

Dodatni upit: {additional_query or 'Nema dodatnog upita.'}
        """.strip()

    with col2:
        st.markdown("### 🤖 Bot odgovor")
        user_input_box = st.text_area("Upit za bot", value=combined_input, height=250, key="user_input_box")

        if st.button("✅ Pošaljite upit"):
            webhook_url = "https://primary-production-b791f.up.railway.app/webhook-test/839b893b-f460-479c-9295-5f3bb8ab3488"
            response = requests.post(webhook_url, json={"text": combined_input})

            if response.status_code == 200:
                st.success("✅ Upit poslan uspješno!")
                try:
                    data = response.json()
                    st.markdown("### 📬 Odgovor bota:")
                    st.markdown(data.get("response", "⛔ Nema sadržaja u odgovoru."))
                except:
                    st.markdown("📝 Odgovor:")
                    st.text(response.text)
            else:
                st.error(f"Greška prilikom slanja (status kod {response.status_code})")

elif authentication_status is False:
    st.error("❌ Neispravni podaci za prijavu.")
elif authentication_status is None:
    st.warning("⏳ Unesite podatke za prijavu.")

