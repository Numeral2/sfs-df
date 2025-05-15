import streamlit as st
import requests

st.title("Katastarski podaci - unos")

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
    
    if submitted:
        if not all([broj_cestice, kvadratura, naselje, upu, dpu, zona]):
            st.error("Molimo ispunite sva obavezna polja (označena zvjezdicom *)")
        else:
            # Kombiniramo sve podatke u jedan string za slanje
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
            
            payload = {
                "combined_input": combined_input
            }
            
            try:
                response = requests.post(
                    "https://primary-production-b791f.up.railway.app/webhook-test/839b893b-f460-479c-9295-5f3bb8ab3488",
                    json=payload
                )
                
                if response.status_code == 200:
                    st.success("Podaci uspješno poslani!")
                    try:
                        response_data = response.json()
                        with st.expander("Kompletan pregled podataka", expanded=True):
                            st.markdown("**Poslani i obrađeni podaci:**")
                            st.markdown(f"``````")
                            st.markdown("**Odgovor webhooka:**")
                            # Prikaz odgovora kao tekst ili kao markdown, ovisno o tipu
                            if isinstance(response_data, dict):
                                for key, value in response_data.items():
                                    st.markdown(f"- **{key}:** {value}")
                            else:
                                st.markdown(str(response_data))
                        with st.expander("Tehnički detalji (JSON)"):
                            st.json(response_data)
                    except Exception as parsing_error:
                        st.error(f"Greška pri obradi odgovora: {str(parsing_error)}")
                        st.text(response.text)
                else:
                    st.error(f"Greška pri slanju: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Došlo je do greške: {str(e)}")

