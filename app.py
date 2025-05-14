import streamlit as st
import streamlit_authenticator as stauth
import requests
import yaml
from yaml.loader import SafeLoader
from pathlib import Path

# -- Priprema korisnika i autentikacije --
names = ['Ivan Horvat']
usernames = ['ivan']
passwords = ['123']  # obična lozinka, hashirat ćemo je

hashed_passwords = stauth.Hasher(passwords).generate()

# Konfiguracija autentikatora
credentials = {
    "usernames": {
        usernames[0]: {
            "name": names[0],
            "password": hashed_passwords[0]
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "katastar_app",  # cookie name
    "abcdef",        # cookie key
    cookie_expiry_days=1
)

# -- Prikaz login forme --
name, authentication_status, username = authenticator.login('Login', 'main')

# -- Ako je autentikacija uspješna --
if authentication_status:
    authenticator.logout("Odjava", "sidebar")
    st.sidebar.success(f"Dobrodošli, {name} 👋")

    # -- Postavke stranice --
    st.set_page_config(page_title="Katastarski upit - Trogir", layout="wide")
    st.title("📄 Katastarski upit za područje Trogira")

    st.markdown("""
        Ovdje možete unijeti potrebne informacije kako bismo obradili vaš katastarski upit za područje Trogira. 
        Molimo vas da ispunite sve relevantne podatke kako bi upit bio što precizniji.
    """)

    st.markdown("### 🔗 Nulti korak: Provjerite zonu na ISPU sustavu")
    st.markdown("""
        Prije nego što nastavite, pogledajte **[ISPU grafički prikaz](https://www.ispu.hr/)** i odredite kojoj zoni pripada vaša čestica:
        - Najčešće žuta boja označava **stambeno-poslovnu zonu** ili **mješovitu zonu (M1)**.
        - Crvena za **komercijalne zone**, plava za **industrijske zone**, itd.
    """, unsafe_allow_html=True)

    # -- Stil stranice --
    st.markdown("""
        <style>
            .stTextInput input, .stSelectbox select, .stTextArea textarea {
                background-color: #f0f2f6;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 6px;
            }
            .stButton>button {
                background-color: #007bff;
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
            }
            .stButton>button:hover {
                background-color: #0056b3;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📝 Podaci o katastarskoj čestici")

        parcel_number = st.text_input("🔢 Broj katastarske čestice", placeholder="Broj kat. čestice")
        parcel_area = st.text_input("📐 Kvadratura katastarske čestice (u m²)", placeholder="Kvadratura u m²")

        naselje = st.selectbox("Naselje", [
            "Arbanija", "Divulje", "Drvenik Mali", "Drvenik Veli",
            "Mastrinka", "Plano", "Trogir", "Žedno"
        ], index=6)

        upu = st.selectbox("UPU", [
            "", "UPU Krban", "UPU naselja Žedno", "UPU poslovne zone POS 3 (UPU 10)",
            "UPU ugostiteljsko – turističke zone Sveti Križ (UPU 17)", "UPU naselja Mastrinka 1 (UPU 6.1)",
            "UPU poslovne zone POS 2 (UPU 15)", "UPU naselja Plano (UPU 18)", "UPU proizvodne zone Plano 3 (UPU 7)"
        ])

        dpu = st.selectbox("DPU", [
            "", "DPU Brigi – Lokvice (DPU 5)", "DPU 1. faze obale od Madiracinog mula do Duhanke (DPU 4)"
        ])

        zone = st.text_input("🧭 Zona", placeholder="Zona iz ISPU sustava")
        additional_query = st.text_area("💬 Dodatni upit", placeholder="Dodatni upit ili napomena", height=100)

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
        user_input_box = st.text_area("Upit za bot", value=combined_input, height=250)

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
                    st.text(response.text)
            else:
                st.error(f"Greška prilikom slanja (status kod {response.status_code})")

# -- Ako login nije točan --
elif authentication_status is False:
    st.error("❌ Pogrešno korisničko ime ili lozinka.")

# -- Ako korisnik nije još pokušao login --
elif authentication_status is None:
    st.info("🔐 Unesite korisničke podatke.")

