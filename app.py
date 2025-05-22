import streamlit as st
import requests
import pandas as pd
from fpdf import FPDF
from io import BytesIO

def to_latin1(text):
    if text is None:
        return ""
    return text.encode('latin1', errors='replace').decode('latin1')

def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, to_latin1("T-Konta knjiženja"), ln=True, align="C")
    pdf.ln(5)

    for d in data:
        konto = to_latin1(d.get("konto", ""))
        dugovna = str(d.get("dugovna", "0"))
        potrazna = str(d.get("potrazna", "0"))

        pdf.cell(60, 10, konto, border=1)
        pdf.cell(60, 10, dugovna, border=1, align="R")
        pdf.cell(60, 10, potrazna, border=1, align="R")
        pdf.ln()

    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

st.title("Knjizenja -> n8n -> T-konta PDF")

tekst = st.text_area("Upiši knjiženja (npr. opisne rečenice)", height=200)

if st.button("Pošalji u n8n"):
    if not tekst.strip():
        st.error("Unesi tekst knjiženja prije slanja!")
    else:
        webhook_url = "https://primary-production-b791f.up.railway.app/webhook-test/70299750-07ed-4701-ba52-13d63bbab711"  # <-- zamijeni ovdje svoj URL

        # Salji POST zahtjev
        try:
            response = requests.post(webhook_url, json={"text": tekst})
            response.raise_for_status()
            result = response.json()

            # Pretpostavka: rezultat je lista dictova s kontima
            if isinstance(result, list):
                df = pd.DataFrame(result)
                st.success("Podaci uspješno primljeni iz n8n:")
                st.dataframe(df)

                if st.button("Generiraj PDF s T-kontima"):
                    pdf_file = generate_pdf(result)
                    st.download_button(
                        label="Preuzmi PDF",
                        data=pdf_file,
                        file_name="t_konta_knjizenja.pdf",
                        mime="application/pdf"
                    )
            else:
                st.error(f"Očekivao sam listu podataka, ali dobio sam:\n{result}")

        except Exception as e:
            st.error(f"Greška prilikom poziva n8n webhooka:\n{e}")

