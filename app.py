import streamlit as st
import requests

st.title("Katastarski podaci - unos")

with st.form("katastar_form"):
    st.subheader("Osnovni podaci")
    broj_cestice = st.text_input("Broj katastarske čestice *", help="Unesite broj iz zemljišnika")
    kvadratura = st.number_input("Kvadratura katastarske čestice (m²) *", min_value=0.0, format="%.2f")
    
    st.subheader("Prostornoplanerske odredbe")
    ppuo_option = st.selectbox(
        "Odaberite PPUO/PPUG/UPU/DPU *",
        options=["Trogir - Centar", "Trogir - Luka", "Trogir - Prigradsko područje"],
        help="Odaberite iz predefinirane liste za Trogir"
    )
    
    zona = st.selectbox(
        "Zona *",
        options=["Zona A - Historijska jezgra", "Zona B - Zaštitni pojas", "Zona C - Suvremeni razvoj"],
        help="Odaberite zonu iz ISPU sustava"
    )
    
    dodatni_upit = st.text_area("Dodatni upit (opcijski)", height=100)
    
    submitted = st.form_submit_button("Pošalji podatke")
    
    if submitted:
        if not broj_cestice or not kvadratura:
            st.error("Molimo ispunite obavezna polja (označena zvjezdicom *)")
        else:
            payload = {
                "broj_katastarske_cestice": broj_cestice,
                "kvadratura": kvadratura,
                "prostorni_plan": ppuo_option,
                "zona": zona,
                "dodatni_upit": dodatni_upit if dodatni_upit else None
            }
            
            try:
                response = requests.post(
                    "https://primary-production-b791f.up.railway.app/webhook-test/839b893b-f460-479c-9295-5f3bb8ab3488",
                    json=payload
                )
                
                if response.status_code == 200:
                    st.success("Podaci uspješno poslani!")
                    st.json(response.json())
                else:
                    st.error(f"Greška pri slanju: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Došlo je do greške: {str(e)}")

