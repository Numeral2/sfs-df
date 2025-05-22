import streamlit as st
import requests
import pandas as pd
from fpdf import FPDF
from io import BytesIO

st.title("Knjigovodstvene rečenice i T-konta")

webhook_url = st.text_input("Unesi URL n8n webhooka", 
                           value="https://primary-production-b791f.up.railway.app/webhook-test/70299750-07ed-4701-ba52-13d63bbab711")

knjizenja = st.text_area("Unesi knjigovodstvene rečenice (jednu po liniji)")

if st.button("Pošalji u n8n"):
    if not webhook_url or not knjizenja.strip():
        st.error("Unesi webhook URL i barem jednu knjigovodstvenu rečenicu!")
    else:
        try:
            response = requests.post(webhook_url, json={"text": knjizenja})
            response.raise_for_status()
            data = response.json()
            
            # Pretpostavimo da je data lista objekata s "konto", "dugovna", "potrazna"
            df = pd.DataFrame(data)
            st.success("Podaci primljeni iz n8n:")
            st.dataframe(df)

            # Spremimo df u session state za kasniju upotrebu pri generiranju PDF-a
            st.session_state['df'] = df

        except Exception as e:
            st.error(f"Greška kod slanja podataka ili parsiranja odgovora: {e}")

if 'df' in st.session_state:
    if st.button("Generiraj PDF s T-kontima"):
        df = st.session_state['df']

        # Funkcija za crtanje T-konta u PDF
        class PDF(FPDF):
            def header(self):
                self.set_font("Arial", "B", 14)
                self.cell(0, 10, "T-konta Knjizenja", 0, 1, "C")

            def add_t_konto(self, konto, dugovna, potrazna):
                self.set_font("Arial", "B", 12)
                self.cell(0, 10, konto, 0, 1)
                self.set_font("Arial", "", 11)
                w = 60
                self.cell(w, 10, "Dugovna", 1, 0, "C")
                self.cell(w, 10, "Potražna", 1, 1, "C")
                self.cell(w, 10, str(dugovna), 1, 0, "C")
                self.cell(w, 10, str(potrazna), 1, 1, "C")
                self.ln(5)

        pdf = PDF()
        pdf.add_page()

        for _, row in df.iterrows():
            pdf.add_t_konto(row["konto"], row["dugovna"], row["potrazna"])

        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)

        st.download_button(
            label="Preuzmi PDF s T-kontima",
            data=pdf_output,
            file_name="T-konta.pdf",
            mime="application/pdf"
        )

