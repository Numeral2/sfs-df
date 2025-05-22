import streamlit as st
import requests
import pandas as pd
from fpdf import FPDF
from io import BytesIO

# Funkcija za latin1 encoding sa zamjenom znakova koje fpdf ne može prikazati
def to_latin1(text):
    if not text:
        return ""
    return text.encode('latin1', errors='replace').decode('latin1')

# PDF klasa s funkcijom za ispis T-konta
class PDFTConta(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, to_latin1("T-Konta Knjiženje"), 0, 1, "C")

    def add_t_konto(self, konto, dugovna, potrazna):
        self.set_font("Arial", "", 12)
        self.cell(70, 10, to_latin1(konto), 1)
        self.cell(40, 10, to_latin1(str(dugovna)), 1, 0, "R")
        self.cell(40, 10, to_latin1(str(potrazna)), 1, 1, "R")

# URL n8n webhooka - zamijeni sa svojim webhook URL-om
N8N_WEBHOOK_URL = "https://primary-production-b791f.up.railway.app/webhook-test/70299750-07ed-4701-ba52-13d63bbab711"

st.title("Unos knjiženja i T-Konta PDF")

# Text area za unos knjiženja (primjer)
knjizenja = st.text_area(
    "Unesi knjiženja (po jedan redak):",
    value=(
        "1. Sa zaliha sirovina i materijala dali smo 20.000 eura vrijednosti materijala drugom poduzetniku na plastificiranje (dorada).\n"
        "2. Poduzetnik je obavio plastificiranje i ispostavio račun na 4.000 eura + 1.000 eura PDV.\n"
        "3. Primljen je račun za usluge odvoza i dovoza materijala na iznos 2.000 eura +500 eura PDV.\n"
        "4. Primili smo dorađeni materijal i zadužili u skladište po novoj vrijednosti (na konto 3100A)."
    )
)

if st.button("Pošalji u n8n i generiraj T-Konta PDF"):
    try:
        # Poziv n8n s podacima u JSON-u
        response = requests.post(N8N_WEBHOOK_URL, json={"text": knjizenja})
        response.raise_for_status()
        data = response.json()

        # Pretpostavljam da n8n vraća listu konta pod ključem 'kontiranja'
        konta = data.get("kontiranja")
        if not konta:
            st.error("n8n nije vratio konta ili ključ 'kontiranja' nije pronađen.")
        else:
            # Prikaz podataka u tablici
            df = pd.DataFrame(konta)
            st.write("### Podaci iz n8n:")
            st.dataframe(df)

            # Generiraj PDF
            pdf = PDFTConta()
            pdf.add_page()
            for row in konta:
                pdf.add_t_konto(row["konto"], row["dugovna"], row["potrazna"])

            pdf_output = BytesIO()
            pdf.output(pdf_output)
            pdf_output.seek(0)

            st.download_button(
                label="Preuzmi T-Konta PDF",
                data=pdf_output,
                file_name="t_konta.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"Došlo je do greške: {e}")
