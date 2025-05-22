import streamlit as st
import requests
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from io import BytesIO
import json
from datetime import datetime

# Konfiguracija stranice
st.set_page_config(
    page_title="Računovodstvo - AI Proknjižba",
    page_icon="🤖",
    layout="wide"
)

def send_to_n8n_webhook(webhook_url, data):
    """Pošalje podatke na n8n webhook"""
    try:
        response = requests.post(webhook_url, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Greška pri slanju na webhook: {str(e)}")
        return None
    except json.JSONDecodeError:
        st.error("Webhook je vratio nevaljan JSON odgovor")
        return None

def create_t_account_pdf(df, account_name):
    """Generiraj PDF s T-konto prikazom - poboljšana verzija"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Elementi za PDF
    elements = []
    styles = getSampleStyleSheet()
    
    # Naslov
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Centriranje
    )
    title = Paragraph(f"T-KONTO IZVJEŠTAJ", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))
    
    # Datum generiranja
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1
    )
    date_text = Paragraph(f"Generirano: {datetime.now().strftime('%d.%m.%Y %H:%M')}", date_style)
    elements.append(date_text)
    elements.append(Spacer(1, 30))
    
    # Priprema podataka za T-konto
    dugovna_strana = []
    potrazna_strana = []
    
    for _, row in df.iterrows():
        datum_str = str(row.get('datum', ''))[:10]  # Samo datum dio
        opis_str = str(row.get('opis', row.get('konto', 'Transakcija')))[:25]  # Skrati ako je predugačko
        
        if pd.notna(row.get('dugovna')) and float(row['dugovna']) > 0:
            dugovna_strana.append([
                datum_str,
                opis_str,
                f"{float(row['dugovna']):,.2f}"
            ])
        if pd.notna(row.get('potrazna')) and float(row['potrazna']) > 0:
            potrazna_strana.append([
                datum_str,
                opis_str, 
                f"{float(row['potrazna']):,.2f}"
            ])
    
    # Ako nema podataka, dodaj placeholder
    if not dugovna_strana and not potrazna_strana:
        dugovna_strana.append(['', 'Nema transakcija', '0,00'])
        potrazna_strana.append(['', 'Nema transakcija', '0,00'])
    
    # Izračunaj sume
    dugovna_suma = float(df['dugovna'].fillna(0).sum())
    potrazna_suma = float(df['potrazna'].fillna(0).sum())
    
    # Kreiraj T-konto tablicu
    max_rows = max(len(dugovna_strana), len(potrazna_strana), 1)
    
    # Dodaj prazan red ako je potrebno
    while len(dugovna_strana) < max_rows:
        dugovna_strana.append(['', '', ''])
    while len(potrazna_strana) < max_rows:
        potrazna_strana.append(['', '', ''])
    
    # Glavna tablica za T-konto
    t_account_data = []
    
    # Header
    t_account_data.append(['DUGOVNA STRANA', '', '', 'POTRAŽNA STRANA', '', ''])
    t_account_data.append(['Datum', 'Opis', 'Iznos (HRK)', 'Datum', 'Opis', 'Iznos (HRK)'])
    
    # Redovi s podacima
    for i in range(max_rows):
        row = dugovna_strana[i] + potrazna_strana[i]
        t_account_data.append(row)
    
    # Sume
    t_account_data.append(['','','','','',''])
    t_account_data.append(['', 'UKUPNO:', f"{dugovna_suma:,.2f}", '', 'UKUPNO:', f"{potrazna_suma:,.2f}"])
    
    # Saldo
    saldo = dugovna_suma - potrazna_suma
    if abs(saldo) > 0.01:  # Provjeri za manje razlike zbog floating point
        saldo_text = f"SALDO: {abs(saldo):,.2f} HRK"
        if saldo > 0:
            saldo_text += " (Dugovno)"
        else:
            saldo_text += " (Potražno)"
    else:
        saldo_text = "KONTO URAVNOTEŽEN"
    
    t_account_data.append(['','','','','',''])
    t_account_data.append(['', saldo_text, '', '', '', ''])
    
    # Kreiraj tablicu
    table = Table(t_account_data, colWidths=[1*inch, 1.8*inch, 1.2*inch, 1*inch, 1.8*inch, 1.2*inch])
    
    # Stiliziranje tablice
    table.setStyle(TableStyle([
        # Header stilovi
        ('BACKGROUND', (0, 0), (2, 0), colors.lightblue),
        ('BACKGROUND', (3, 0), (5, 0), colors.lightblue),
        ('BACKGROUND', (0, 1), (2, 1), colors.lightgrey),
        ('BACKGROUND', (3, 1), (5, 1), colors.lightgrey),
        
        # Okviri
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LINEABOVE', (0, 2), (-1, 2), 2, colors.black),
        
        # Tekst stilovi
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),  # Dugovna iznosi
        ('ALIGN', (5, 0), (5, -1), 'RIGHT'),  # Potražna iznosi
        ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Sume
        ('BACKGROUND', (0, -3), (-1, -3), colors.yellow),
        ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
        
        # Centralna linija T-konta
        ('LINEAFTER', (2, 0), (2, -1), 3, colors.black),
    ]))
    
    elements.append(table)
    
    # Dodaj detaljan pregled po kontovima
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("DETALJAN PREGLED PO KONTOVIMA:", styles['Heading2']))
    elements.append(Spacer(1, 15))
    
    # Grupiraj po kontovima
    konto_summary = []
    for _, row in df.iterrows():
        konto_name = str(row.get('konto', 'N/A'))
        dugovna_val = float(row.get('dugovna', 0))
        potrazna_val = float(row.get('potrazna', 0))
        if dugovna_val > 0 or potrazna_val > 0:
            konto_summary.append([konto_name, f"{dugovna_val:,.2f}", f"{potrazna_val:,.2f}"])
    
    if konto_summary:
        konto_table_data = [['KONTO', 'DUGOVNA (HRK)', 'POTRAŽNA (HRK)']] + konto_summary
        konto_table = Table(konto_table_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        konto_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        elements.append(konto_table)
    
    # Generiraj PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

def main():
    st.title("🤖 AI Računovodstvo - Automatska Proknjižba")
    st.markdown("*Opišite poslovnu promjenu, AI će napraviti proknjižbu*")
    st.markdown("---")
    
    # Sidebar za konfiguraciju
    with st.sidebar:
        st.header("⚙️ Konfiguracija")
        webhook_url = st.text_input(
            "n8n Webhook URL:",
            placeholder="https://your-n8n-instance.com/webhook/...",
            help="Unesite URL vašeg n8n webhook-a"
        )
        
        st.markdown("---")
        st.info("💡 **Kako funkcioniše:**\n1. Opišite što se dogodilo\n2. AI analizira i kreira proknjižbu\n3. Preuzmite T-konto PDF")
        
        st.markdown("---")
        st.success("✨ **Primjeri opisa:**\n• Kupljena roba za 5000 kn gotovinom\n• Prodaja usluga 15000 kn na račun\n• Plaćena struja 800 kn s računa\n• Primitak od kupca 10000 kn")
    
    # Glavna forma
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header("📝 Opišite poslovnu promjenu")
        
        # Forma za unos - pojednostavljeno
        with st.form("business_transaction_form"):
            # Datum
            datum = st.date_input(
                "📅 Datum transakcije:", 
                datetime.now()
            )
            
            # Glavni opis
            opis_promjene = st.text_area(
                "💬 Opišite što se dogodilo:",
                placeholder="Npr: 'Kupili smo robu za 10.000 kn i platili gotovinom'",
                height=120
            )
            
            # Dodatne informacije
            referenca = st.text_input(
                "🔗 Broj dokumenta (opcionalno):",
                placeholder="R-001/2024"
            )
            
            kontakt = st.text_input(
                "👤 Partner/Klijent (opcionalno):",
                placeholder="Naziv partnera"
            )
            
            # Submit button
            submit_button = st.form_submit_button(
                "🤖 Analiziraj i proknjižuj",
                use_container_width=True,
                type="primary"
            )
    
    with col2:
        st.header("📊 Status")
        
        # Provjera unosa
        if opis_promjene.strip():
            word_count = len(opis_promjene.split())
            st.success(f"✅ Opis unesen ({word_count} riječi)")
            
            # Osnovne provjere
            if any(keyword in opis_promjene.lower() for keyword in ['kn', 'kuna', 'euro', '€', 'hrk']):
                st.info("💰 Detektiran novčani iznos")
            
            if any(keyword in opis_promjene.lower() for keyword in ['kupio', 'platio', 'prodao', 'naplatio']):
                st.info("📈 Detektirana transakcija")
        else:
            st.warning("⚠️ Unesite opis promjene")
        
        st.markdown("---")
        st.markdown("**🎯 Savjeti za bolji opis:**")
        st.markdown("• Spomenite iznos\n• Navedite način plaćanja\n• Opišite što je kupljeno/prodano")
    
    # Obrada forme
    if submit_button:
        if not webhook_url.strip():
            st.error("❌ Molimo unesite n8n webhook URL u sidebar")
            return
        
        if not opis_promjene.strip():
            st.error("❌ Opis poslovne promjene je obavezan")
            return
        
        # Priprema podataka za n8n (AI analizu)
        webhook_data = {
            "datum": datum.strftime("%Y-%m-%d"),
            "opis_promjene": opis_promjene.strip(),
            "referenca": referenca.strip() if referenca else "",
            "kontakt": kontakt.strip() if kontakt else "",
            "timestamp": datetime.now().isoformat(),
            "jezik": "hrvatski"
        }
        
        with st.spinner("🤖 AI analizira poslovnu promjenu..."):
            response = send_to_n8n_webhook(webhook_url, webhook_data)
        
        if response:
            st.success("✅ Analiza završena uspješno!")
            
            # Prikaz analize
            if 'analiza' in response:
                st.header("🧠 AI Analiza")
                
                analiza = response['analiza']
                col_a, col_b = st.columns(2)
                
                with col_a:
                    if 'prepoznato' in analiza:
                        st.info(f"**Prepoznato:** {analiza['prepoznato']}")
                    if 'iznos' in analiza:
                        st.success(f"**Iznos:** {analiza['iznos']}")
                
                with col_b:
                    if 'tip_transakcije' in analiza:
                        st.info(f"**Tip:** {analiza['tip_transakcije']}")
                    if 'način_plaćanja' in analiza:
                        st.success(f"**Plaćanje:** {analiza['način_plaćanja']}")
            
            # Prikaz proknjižbe
            if 'proknjizba' in response:
                st.header("📚 Proknjižba")
                
                proknjizba = response['proknjizba']
                
                # Prikaz stavki
                for i, stavka in enumerate(proknjizba, 1):
                    with st.expander(f"Stavka {i}: {stavka.get('opis', 'Stavka')}", expanded=True):
                        col_x, col_y = st.columns(2)
                        
                        with col_x:
                            st.write(f"**Dugovna:** {stavka.get('konto_duguje', '')} - {stavka.get('dugovna', 0):.2f} HRK")
                        with col_y:
                            st.write(f"**Potražna:** {stavka.get('konto_potrazuje', '')} - {stavka.get('potrazna', 0):.2f} HRK")
            
            # Obradi podatke od n8n-a - podrška za različite formate
            st.header("📋 T-konto podaci")
            
            try:
                # Pokušaj parsirati različite formate
                df_data = []
                
                # Format 1: response['tablica'] (standardni)
                if 'tablica' in response:
                    if isinstance(response['tablica'], list):
                        df_data = response['tablica']
                    else:
                        df_data = pd.read_json(response['tablica']).to_dict('records')
                
                # Format 2: direktno numerički ključevi (vaš slučaj)
                elif any(key.isdigit() for key in response.keys()):
                    for key in sorted(response.keys()):
                        if key.isdigit() or key == str(key):
                            item = response[key]
                            if isinstance(item, dict):
                                # Dodaj datum ako nema
                                if 'datum' not in item:
                                    item['datum'] = datum.strftime("%Y-%m-%d")
                                # Dodaj opis ako nema
                                if 'opis' not in item:
                                    item['opis'] = f"Transakcija - {item.get('konto', 'N/A')}"
                                df_data.append(item)
                
                # Format 3: direktni format (fallback)
                else:
                    df_data = [response]
                
                if df_data:
                    df = pd.DataFrame(df_data)
                    
                    # Standardiziraj kolone
                    if 'dugovna' not in df.columns:
                        df['dugovna'] = 0
                    if 'potrazna' not in df.columns:
                        df['potrazna'] = 0
                    if 'datum' not in df.columns:
                        df['datum'] = datum.strftime("%Y-%m-%d")
                    if 'opis' not in df.columns:
                        df['opis'] = df.get('konto', 'Transakcija')
                    
                    # Konvertiraj u brojeve
                    df['dugovna'] = pd.to_numeric(df['dugovna'], errors='coerce').fillna(0)
                    df['potrazna'] = pd.to_numeric(df['potrazna'], errors='coerce').fillna(0)
                    
                    # Prikaz tablice
                    st.dataframe(df, use_container_width=True)
                    
                    # Prikaz sume za provjeru
                    dugovna_suma = df['dugovna'].sum()
                    potrazna_suma = df['potrazna'].sum()
                    
                    col_sum1, col_sum2, col_sum3 = st.columns(3)
                    with col_sum1:
                        st.metric("Ukupno dugovna", f"{dugovna_suma:,.2f} HRK")
                    with col_sum2:
                        st.metric("Ukupno potražna", f"{potrazna_suma:,.2f} HRK")
                    with col_sum3:
                        razlika = dugovna_suma - potrazna_suma
                        st.metric("Razlika", f"{razlika:,.2f} HRK", delta=f"{razlika:,.2f}")
                    
                    # PDF generiranje
                    account_name = "Svi_kontovi"
                    
                    col_pdf1, col_pdf2 = st.columns([1, 1])
                    
                    with col_pdf1:
                        if st.button("📄 Generiraj T-konto PDF", use_container_width=True, type="primary"):
                            with st.spinner("📄 Kreiram PDF izvještaj..."):
                                try:
                                    pdf_buffer = create_t_account_pdf(df, account_name)
                                    
                                    # Store PDF u session state
                                    st.session_state['pdf_buffer'] = pdf_buffer.getvalue()
                                    st.session_state['pdf_filename'] = f"T-konto_{account_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
                                    
                                    st.success("✅ PDF uspješno kreiran!")
                                    
                                except Exception as e:
                                    st.error(f"❌ Greška pri kreiranju PDF-a: {str(e)}")
                                    st.error(f"Debug info: {str(df.dtypes)}")
                    
                    with col_pdf2:
                        # Download dugme (pokazuje se samo ako je PDF kreiran)
                        if 'pdf_buffer' in st.session_state:
                            st.download_button(
                                label="⬇️ Preuzmi PDF",
                                data=st.session_state['pdf_buffer'],
                                file_name=st.session_state['pdf_filename'],
                                mime="application/pdf",
                                use_container_width=True
                            )
                else:
                    st.warning("⚠️ Nema podataka za T-konto")
                
            except Exception as e:
                st.error(f"❌ Greška pri obradi podataka: {str(e)}")
                st.json(response)  # Debug prikaz
            
            # Raw odgovor za debug
            with st.expander("🔧 Tehnički detalji (za debug)", expanded=False):
                st.json(response)
        
        else:
            st.error("❌ Greška u komunikaciji s n8n webhook-om")
    
    # Footer s primjerima
    st.markdown("---")
    st.markdown("### 💡 Primjeri opisа poslovnih promjena:")
    
    examples_col1, examples_col2 = st.columns(2)
    
    with examples_col1:
        st.markdown("""
        **Kupovina:**
        • Kupili smo materijal za 5.000 kn gotovinom
        • Kupnja opreme na kredit 15.000 kn
        • Nabava robe 8.000 kn, platili bankovnim transferom
        """)
        
        st.markdown("""
        **Prodaja:**
        • Prodali usluge klijentu za 12.000 kn na račun
        • Gotovinska prodaja 3.500 kn
        • Izdali račun za konsalting 25.000 kn
        """)
    
    with examples_col2:
        st.markdown("""
        **Plaćanja:**
        • Plaćena struja 800 kn s poslovnog računa
        • Isplata plaće radnicima 45.000 kn
        • Vraćen kredit banci 10.000 kn
        """)
        
        st.markdown("""
        **Primitci:**
        • Klijent platio račun 18.000 kn na žiro-račun
        • Primitak od partnera 7.500 kn gotovinom
        • Kamate od banke 250 kn
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray; font-size: 12px;'>
        🤖 AI Računovodstvo | Prirodni jezik ➡️ Proknjižba ➡️ T-konto PDF
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
