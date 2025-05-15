import streamlit as st
import requests

# === POSTAVI SVOJ WEBHOOK URL OVDJE ===
N8N_WEBHOOK_URL = "https://primary-production-b791f.up.railway.app/webhook-test/839b893b-f460-479c-9295-5f3bb8ab3488"

st.set_page_config(page_title="Katastarski podaci - unos", layout="wide")

# Sidebar s uputama/pomoći
with st.sidebar:
    st.header("Što možete pretražiti?")
    st.markdown("""
    1. Tekst što može graditi opisni  
    2. Kis + moguća ukupna kvadratura koju može ukupno izgraditi  
       *(potrebna formula bota za izračunavanje: Kis × kvadratura parcele)*  
    3. Kig + moguća tlocrtna kvadratura koju može ukupno izgraditi  
       *(potrebna formula bota za izračunavanje: Kig × kvadratura parcele)*  
    4. Kolika je dozvoljena katnost objekta  
    5. Maksimalna visina vijenca krova ili maksimalna visina građevine  
    6. Udaljenost od regulacijske linije  
    7. Udaljenost od susjednih čestica  
    8. Ostali uvjeti - minimalna površina okućnice, parkirna mjesta, površina ozelenjenog područja,  
       visina ogradnog zida, što se može graditi na toj parceli bez građevinske dozvole  
       (često kamin, garaža i slično)  
    """)

st.title("Katastarski podaci - unos")

col1, col2 = st.columns([3,1])  # 3 dijela za formu, 1 dio za output

with col1:
    with st.form("katastar_form"):
        st.subheader("Osnovni podaci")
        broj_cestice = st.text_input("Broj katastarske čestice *", help="Unesite broj iz zemljišnika")
        kvadratura = st.number_input("Kvadratura katastarske čestice (m²) *", min_value=0.0, format="%.2f")

        st.subheader("Prostornoplanerske odredbe")
        naselje = st.selectbox(
            "Odaberite naselje Trogira *",
            options=[
                "Arbanija", "Divulje", "Drvenik Mali", "Drvenik Veli",
                "Mastrinka", "Plano", "Trogir", "Žedno"
            ]
        )

        upu = st.selectbox(
            "Odaberite UPU pod Trogir *",
            options=[
                "UPU Krban",
                "UPU naselja Žedno",
                "UPU poslovne zone POS 3 (UPU 10)",
                "UPU ugostiteljsko – turističke zone Sveti Križ (UPU 17)",
                "UPU naselja Mastrinka 1 (UPU 6.1)",
                "UPU poslovne zone POS 2 (UPU 15)",
                "UPU naselja Plano (UPU 18)",
                "UPU proizvodne zone Plano 3 (UPU 7)"
            ]
        )

        dpu = st.selectbox(
            "Odaberite DPU pod Trogir *",
            options=[
                "DPU Brigi – Lokvice (DPU 5)",
                "DPU 1.faze obale od Madiracnog mula do Duhanke (DPU 4)"
            ]
        )

        zona = st.selectbox(
            "Zona *",
            options=[
                "Zona A - Historijska jezgra",
                "Zona B - Zaštitni pojas",
                "Zona C - Suvremeni razvoj"
            ],
            help="Odaberite zonu iz ISPU sustava"
        )

        dodatni_upit = st.text_area("Dodatni upit (opcijski)", height=100)

        submitted = st.form_submit_button("Pošalji podatke")

with col2:
    st.subheader("Odgovor iz n8n webhooka:")
    output_placeholder = st.empty()  # Dinamički ispis odgovora

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

            # Prikazi odgovor kao plain text
            output_placeholder.text(response.text)

            st.success("Podaci uspješno poslani!")

        except requests.exceptions.RequestException as e:
            st.error(f"Greška pri slanju: {str(e)}")
