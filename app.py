import streamlit as st
import requests

# Postavke stranice
st.set_page_config(page_title="Katastarski upit - Trogir", layout="wide")
st.title("📄 Katastarski upit za područje Trogira")

st.markdown("""
    Ovdje možete unijeti potrebne informacije kako bismo obradili vaš katastarski upit za područje Trogira. 
    Molimo vas da ispunite sve relevantne podatke kako bi upit bio što precizniji.
""")

# Nulti korak - Link prema ISPU sustavu i upute
st.markdown("### 🔗 Nulti korak: Provjerite zonu na ISPU sustavu")
st.markdown("""
    Prije nego što nastavite, pogledajte **[ISPU grafički prikaz](https://www.ispu.hr/)** i odredite kojoj zoni pripada vaša čestica:
    1. Otvorite stranicu ISPU.
    2. U lijevom padajućem izborniku uključite odgovarajući sloj (na primjer, sloj sa zonama).
    3. Pogledajte koja boja označava vašu zonu. 
    - **Najčešće žuta boja** označava **stambeno-poslovnu zonu** ili **mješovitu zonu (M1)**.
    - Svaka boja označava specifičnu zonu, npr. crvena za **komercijalne zone**, plava za **industrijske zone**, itd.
""", unsafe_allow_html=True)

# Layout za Streamlit (Stavljanje bota sa strane)
col1, col2 = st.columns([3, 1])

with col1:
    # Unos podataka
    st.markdown("### 📝 Podaci o katastarskoj čestici")
    
    # Unos broja katastarske čestice
    parcel_number = st.text_input("🔢 Broj katastarske čestice", placeholder="Unesite broj katastarske čestice")

    # Unos kvadrature katastarske čestice
    parcel_area = st.text_input("📐 Kvadratura katastarske čestice (u m²)", placeholder="Unesite kvadraturu u m²")

    # Naselje
    st.markdown("### 📍 Odaberite naselje:")
    naselje = st.selectbox("Naselje", [
        "Arbanija", "Divulje", "Drvenik Mali", "Drvenik Veli",
        "Mastrinka", "Plano", "Trogir", "Žedno"
    ])
    
    # UPU (Urbanistički plan uređenja)
    st.markdown("### 🏗️ Odaberite UPU (ako postoji):")
    upu = st.selectbox("UPU", [
        "",  # Prazno ako nije primjenjivo
        "UPU Krban",
        "UPU naselja Žedno",
        "UPU poslovne zone POS 3 (UPU 10)",
        "UPU ugostiteljsko – turističke zone Sveti Križ (UPU 17)",
        "UPU naselja Mastrinka 1 (UPU 6.1)",
        "UPU poslovne zone POS 2 (UPU 15)",
        "UPU naselja Plano (UPU 18)",
        "UPU proizvodne zone Plano 3 (UPU 7)"
    ])
    
    # DPU (Detaljni plan uređenja)
    st.markdown("### 🏘️ Odaberite DPU (ako postoji):")
    dpu = st.selectbox("DPU", [
        "",  # Prazno ako nije primjenjivo
        "DPU Brigi – Lokvice (DPU 5)",
        "DPU 1. faze obale od Madiracinog mula do Duhanke (DPU 4)"
    ])
    
    # Zona (Prema ISPU sustavu)
    st.markdown("### 🧭 Unesite zonu prema ISPU sustavu:")
    zone = st.text_input("Zona (prema ISPU sustavu)", placeholder="Unesite zonu iz ISPU sustava")
    
    # Dodatni upit
    st.markdown("### 💬 Dodatni upit:")
    additional_query = st.text_area("Dodatni upit (ako imate specifična pitanja)", placeholder="Ovdje možete dodati dodatna pitanja ili napomene")

    # Kombinirani input koji se automatski popunjava u box
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
    # Prikaz bota
    st.markdown("### 🤖 Bot odgovor")
    
    # Polje za odgovor od bota, automatski popunjeno
    user_input_box = st.text_area("Upit za bot", value=combined_input, height=300)
    
    # Submit button
    if st.button("✅ Pošaljite upit"):
        # Webhook adresa
        webhook_url = "https://primary-production-b791f.up.railway.app/webhook-test/03419cdb-f956-48b4-85d8-725a6a4db8fb"

        # Slanje podataka kao JSON
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
