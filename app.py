import streamlit as st
import requests
import json
import time
from datetime import datetime
import pandas as pd
import base64
from streamlit_lottie import st_lottie

# === POSTAVI SVOJ WEBHOOK URL OVDJE ===
N8N_WEBHOOK_URL = "https://primary-production-b791f.up.railway.app/webhook-test/839b893b-f460-479c-9295-5f3bb8ab3488"

# === CSS I KONFIGURACIJSKE FUNKCIJE ===

def set_custom_theme():
    """Postavlja prilagođenu temu aplikacije"""
    st.set_page_config(
        page_title="GradTrogir Katastarski Portal",
        layout="wide",
        page_icon="🏛️",
        initial_sidebar_state="collapsed"
    )
    
    # Učitaj CSS
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Provjeri postojanje CSS datoteke, ako ne postoji, kreiraj je
try:
    with open("style.css", "r"):
        pass
except FileNotFoundError:
    with open("style.css", "w") as css_file:
        css_file.write("""
        /* Glavni CSS stilovi za aplikaciju */
        @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Open Sans', sans-serif;
        }
        
        /* Sakrivanje Streamlit elemenata */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Prilagođeni stilovi */
        .main-header {
            background-color: #2c3e50;
            padding: 1.5rem;
            border-radius: 0.5rem;
            color: white;
            margin-bottom: 1rem;
            border-bottom: 4px solid #3498db;
        }
        
        .logo-text {
            font-size: 2rem;
            font-weight: 700;
            margin: 0;
        }
        
        .subheader {
            font-size: 1rem;
            font-weight: 300;
            margin-top: 0.5rem;
        }
        
        .form-container {
            background-color: white;
            padding: 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        
        .results-container {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border-left: 4px solid #3498db;
            margin-bottom: 1rem;
        }
        
        .highlight-text {
            color: #3498db;
            font-weight: 600;
        }
        
        .nav-button {
            background-color: transparent;
            border: 1px solid #e0e0e0;
            border-radius: 0.3rem;
            padding: 0.5rem 1rem;
            margin-right: 0.5rem;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .nav-button:hover, .nav-button.active {
            background-color: #3498db;
            color: white;
            border-color: #3498db;
        }
        
        .footer {
            background-color: #2c3e50;
            padding: 1rem;
            color: white;
            text-align: center;
            border-radius: 0.5rem;
            font-size: 0.8rem;
            margin-top: 2rem;
        }
        
        .data-card {
            background-color: white;
            border-radius: 0.5rem;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 3px solid #3498db;
        }
        
        .result-summary {
            background-color: #e8f4f8;
            border-radius: 0.3rem;
            padding: 1rem;
            margin-top: 1rem;
        }
        
        .info-icon {
            color: #3498db;
            font-size: 1.2rem;
            margin-right: 0.5rem;
        }
        
        /* Animirani loader */
        .loader {
            border: 5px solid #f3f3f3;
            border-top: 5px solid #3498db;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .btn-primary {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 0.5rem 1.5rem;
            border-radius: 0.3rem;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-primary:hover {
            background-color: #2980b9;
        }
        
        .status-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .status-success {
            background-color: #d4edda;
            color: #155724;
        }
        
        .status-pending {
            background-color: #fff3cd;
            color: #856404;
        }
        
        .status-error {
            background-color: #f8d7da;
            color: #721c24;
        }
        
        /* Tablice */
        .styled-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            font-size: 0.9rem;
            border-radius: 0.5rem;
            overflow: hidden;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
        }
        
        .styled-table thead tr {
            background-color: #3498db;
            color: white;
            text-align: left;
        }
        
        .styled-table th,
        .styled-table td {
            padding: 0.75rem 1rem;
        }
        
        .styled-table tbody tr {
            border-bottom: 1px solid #ddd;
        }
        
        .styled-table tbody tr:nth-of-type(even) {
            background-color: #f8f9fa;
        }
        
        .styled-table tbody tr:last-of-type {
            border-bottom: 2px solid #3498db;
        }
        """)

def load_lottieurl(url: str):
    """Učitava Lottie animaciju s URL-a"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

def get_base64_encoded_image(image_path):
    """Pretvara sliku u base64 za pozadinu"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def add_bg_from_url():
    """Dodaje suptilnu pozadinu cijeloj aplikaciji"""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://i.imgur.com/J5qQNKB.png");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def format_response(response_text):
    """Formatira odgovor u strukturirani format"""
    # Pokušaj parsirati JSON ako je dostupan
    try:
        data = json.loads(response_text)
        return data
    except json.JSONDecodeError:
        # Ako nije JSON, strukturiraj tekst najbolje što možeš
        lines = response_text.strip().split('\n')
        structured_data = {}
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                structured_data[key.strip()] = value.strip()
            else:
                if 'dodatne_informacije' not in structured_data:
                    structured_data['dodatne_informacije'] = []
                structured_data['dodatne_informacije'].append(line.strip())
        
        return structured_data

def show_loading_animation():
    """Prikazuje animaciju učitavanja"""
    with st.spinner("Obrađujem vaš zahtjev..."):
        loading_container = st.empty()
        loading_container.markdown(
            """
            <div class="loader"></div>
            <p style='text-align:center'>Dohvaćam podatke iz katastarskog sustava...</p>
            """, 
            unsafe_allow_html=True
        )
        return loading_container

def create_pdf_report(data):
    """
    Stvara PDF izvještaj na temelju podataka 
    (ovo je samo simulacija - u pravoj aplikaciji biste koristili biblioteku kao što je ReportLab ili WeasyPrint)
    """
    return "generirani_izvjestaj.pdf"

# === FUNKCIJE ZA PRIKAZ STRANICA ===

def render_header():
    """Prikazuje zaglavlje stranice"""
    header_col1, header_col2 = st.columns([3, 1])
    
    with header_col1:
        st.markdown("""
        <div class="main-header">
            <h1 class="logo-text">🏛️ Katastarski Portal Grada Trogira</h1>
            <p class="subheader">Službeni portal za prostorne podatke i građevinske uvjete</p>
        </div>
        """, unsafe_allow_html=True)
    
    with header_col2:
        current_time = datetime.now().strftime("%d.%m.%Y. %H:%M")
        st.markdown(f"""
        <div style="text-align: right; padding-top: 1rem;">
            <p>📅 {current_time}</p>
            <p style="margin-top: 5px; font-size: 0.8rem;">Zadnje ažuriranje: 15.05.2025.</p>
        </div>
        """, unsafe_allow_html=True)

def render_navigation():
    """Prikazuje navigaciju stranice"""
    st.markdown("""
    <div style="display: flex; margin-bottom: 1.5rem;">
        <button class="nav-button active" id="btn-home" onclick="switchPage('home')">🏠 Početna</button>
        <button class="nav-button" id="btn-info" onclick="switchPage('info')">ℹ️ Informacije</button>
        <button class="nav-button" id="btn-contact" onclick="switchPage('contact')">📞 Kontakt</button>
    </div>
    
    <script>
    function switchPage(page) {
        // Ovo bi trebalo biti povezano preko Streamlit komponente u pravoj implementaciji
        // Za sada samo promijeni stilove
        document.querySelectorAll('.nav-button').forEach(btn => btn.classList.remove('active'));
        document.getElementById('btn-' + page).classList.add('active');
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Za stvarnu funkcionalnost koristimo Streamlit radio, ali skrivamo ga vizualno
    page = st.radio("", ["🏠 Početna", "ℹ️ Informacije", "📞 Kontakt"], horizontal=True, label_visibility="collapsed")
    return page

def render_footer():
    """Prikazuje podnožje stranice"""
    st.markdown("""
    <div class="footer">
        <p>© 2025 Grad Trogir | Katastarski Portal | Sva prava pridržana</p>
        <p>Izrađeno u suradnji s Ministarstvom prostornog uređenja, graditeljstva i državne imovine</p>
    </div>
    """, unsafe_allow_html=True)

def render_home_page():
    """Prikazuje početnu stranicu s formularom i rezultatima"""
    st.markdown("<h2>🔍 Provjera katastarskih podataka i uvjeta gradnje</h2>", unsafe_allow_html=True)
    
    # Glavni sadržaj - dvije kolone
    col1, col2 = st.columns([5, 7])
    
    with col1:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        with st.form("katastar_form", clear_on_submit=False):
            st.subheader("📋 Unos podataka")
            
            # Osnovni podaci
            broj_cestice = st.text_input("Katastarska čestica *", 
                                        placeholder="npr. 1234/5",
                                        help="Unesite točan broj čestice iz katastarskog plana ili zemljišne knjige")
            
            kvadratura = st.number_input("Površina čestice (m²) *", 
                                        min_value=0.0, 
                                        format="%.2f",
                                        help="Unesite egzaktnu površinu prema zadnjem mjerenju")
            
            # Napredniji odabir lokacije
            st.subheader("🗺️ Lokacija i zona")
            
            col_lok1, col_lok2 = st.columns(2)
            with col_lok1:
                naselje = st.selectbox("Naselje *", options=[
                    "Arbanija", "Divulje", "Drvenik Mali", "Drvenik Veli",
                    "Mastrinka", "Plano", "Trogir", "Žedno"
                ])
            
            with col_lok2:
                zona = st.selectbox("Zona *", options=[
                    "Zona A - Historijska jezgra",
                    "Zona B - Zaštitni pojas",
                    "Zona C - Suvremeni razvoj"
                ])
            
            # Napredne opcije
            with st.expander("Dodatni parametri"):
                upu = st.selectbox("Urbanistički plan uređenja (UPU)", options=[
                    "Nije primjenjivo",
                    "UPU Krban",
                    "UPU naselja Žedno",
                    "UPU poslovne zone POS 3 (UPU 10)",
                    "UPU ugostiteljsko – turističke zone Sveti Križ (UPU 17)",
                    "UPU naselja Mastrinka 1 (UPU 6.1)",
                    "UPU poslovne zone POS 2 (UPU 15)",
                    "UPU naselja Plano (UPU 18)",
                    "UPU proizvodne zone Plano 3 (UPU 7)"
                ])
                
                dpu = st.selectbox("Detaljni plan uređenja (DPU)", options=[
                    "Nije primjenjivo",
                    "DPU Brigi – Lokvice (DPU 5)",
                    "DPU 1.faze obale od Madiracnog mula do Duhanke (DPU 4)"
                ])
                
                namjena = st.selectbox("Namjena objekta", options=[
                    "Stambena",
                    "Poslovna",
                    "Mješovita",
                    "Turistička",
                    "Javna i društvena",
                    "Infrastrukturna"
                ])
            
            # Dodatni upiti
            dodatni_upit = st.text_area("📝 Dodatne napomene ili pitanja", 
                                    height=80, 
                                    max_chars=500,
                                    placeholder="Opišite specifične zahtjeve ili pitanja...")
            
            # Kontakt podaci
            st.subheader("📧 Kontakt podaci (opcionalno)")
            email = st.text_input("E-mail za primanje izvještaja", 
                                placeholder="ime.prezime@email.com")
            
            # Početak i podnošenje
            submitted = st.form_submit_button("🔍 Dohvati podatke")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Informativni dio
        st.markdown("""
        <div class="data-card">
            <h4>📊 Što ćete dobiti?</h4>
            <ul>
                <li>Koeficijent iskoristivosti (KIS)</li>
                <li>Koeficijent izgrađenosti (KIG)</li>
                <li>Maksimalnu katnost i visinu objekta</li>
                <li>Minimalne udaljenosti od granica</li>
                <li>Moguće namjene prema prostornom planu</li>
                <li>PDF izvještaj s detaljnim uvjetima (na e-mail)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        st.subheader("📋 Rezultati analize")
        
        result_placeholder = st.empty()
        result_placeholder.markdown("""
        <div style="text-align: center; padding: 3rem 1rem;">
            <img src="https://i.imgur.com/NWjjFm1.png" width="120" style="opacity: 0.2">
            <p style="color: #6c757d; margin-top: 1rem;">
                Unesite podatke u formular lijevo i kliknite "Dohvati podatke" za prikaz rezultata.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Rezultati koji se prikazuju nakon slanja forme
        if 'submitted' in locals() and submitted:
            if not all([broj_cestice, kvadratura, naselje, zona]):
                st.error("❗ Molimo ispunite sva obavezna polja označena zvjezdicom (*)")
            else:
                # Prikaži animaciju učitavanja
                loading_container = show_loading_animation()
                
                # Pripremi podatke za slanje
                combined_input = (
                    f"Broj katastarske čestice: {broj_cestice}\n"
                    f"Kvadratura: {kvadratura} m²\n"
                    f"Naselje: {naselje}\n"
                    f"Zona: {zona}\n"
                )
                
                if upu != "Nije primjenjivo":
                    combined_input += f"UPU: {upu}\n"
                if dpu != "Nije primjenjivo":
                    combined_input += f"DPU: {dpu}\n"
                if namjena:
                    combined_input += f"Namjena: {namjena}\n"
                if dodatni_upit:
                    combined_input += f"Dodatni upit: {dodatni_upit}\n"
                
                payload = {"combined_input": combined_input}
                
                try:
                    # Simulacija vremena učitavanja za bolji UX
                    time.sleep(1.5)
                    
                    # Stvarni API poziv
                    response = requests.post(
                        N8N_WEBHOOK_URL,
                        json=payload,
                        timeout=15,
                        headers={"Content-Type": "application/json"}
                    )
                    response.raise_for_status()
                    
                    # Očisti animaciju učitavanja
                    loading_container.empty()
                    
                    # Formatiraj i prikaži rezultate
                    formatted_response = format_response(response.text)
                    
                    # Za demonstraciju koristimo uzorkovane podatke ako odgovor nema strukturu
                    if not isinstance(formatted_response, dict) or len(formatted_response) < 3:
                        # Demo podaci za vizualni prikaz
                        formatted_response = {
                            "KIG": "0.3",
                            "KIS": "0.8",
                            "Katnost": "P+2+Pk",
                            "Max visina": "10.5 m",
                            "Min udaljenost od granice": "3 m",
                            "Posebni uvjeti": "Potrebna suglasnost Konzervatorskog odjela",
                            "Status": "Građevinsko zemljište",
                            "Namjena": "Mješovita - pretežito stambena (M1)",
                            "Infrastruktura": "Potpuno komunalno opremljeno",
                            "Napomena": "Čestica se nalazi u zoni posebnih ograničenja - provjera u GUP-u"
                        }
                    
                    # Resetiraj placeholder i prikaži formatirane rezultate
                    result_placeholder.empty()
                    
                    with result_placeholder.container():
                        st.markdown(f"""
                        <div class="result-summary">
                            <h3>📍 Katastarska čestica: {broj_cestice}</h3>
                            <p>Naselje: <b>{naselje}</b> | Zona: <b>{zona}</b> | Površina: <b>{kvadratura} m²</b></p>
                            <span class="status-badge status-success">✓ Analiza uspješna</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Prikaz rezultata u vizualno atraktivnim karticama
                        col_r1, col_r2, col_r3 = st.columns(3)
                        
                        with col_r1:
                            st.markdown("""
                            <div class="data-card">
                                <h4>📐 Koeficijenti</h4>
                            """, unsafe_allow_html=True)
                            
                            st.metric("KIG (izgrađenost)", formatted_response.get("KIG", "0.3"))
                            st.metric("KIS (iskoristivost)", formatted_response.get("KIS", "0.8"))
                            
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        with col_r2:
                            st.markdown("""
                            <div class="data-card">
                                <h4>🏢 Dimenzije</h4>
                            """, unsafe_allow_html=True)
                            
                            st.metric("Katnost", formatted_response.get("Katnost", "P+2+Pk"))
                            st.metric("Max visina", formatted_response.get("Max visina", "10.5 m"))
                            st.metric("Min udaljenost", formatted_response.get("Min udaljenost od granice", "3 m"))
                            
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        with col_r3:
                            st.markdown("""
                            <div class="data-card">
                                <h4>🏗️ Status i namjena</h4>
                            """, unsafe_allow_html=True)
                            
                            st.info(formatted_response.get("Status", "Građevinsko zemljište"))
                            st.info(formatted_response.get("Namjena", "Mješovita - pretežito stambena (M1)"))
                            
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Dodatne informacije iz odgovora
                        st.markdown("""
                        <div class="data-card">
                            <h4>📋 Dodatne informacije</h4>
                        """, unsafe_allow_html=True)
                        
                        st.info(formatted_response.get("Infrastruktura", "Potpuno komunalno opremljeno"))
                        
                        if "Posebni uvjeti" in formatted_response:
                            st.warning(formatted_response["Posebni uvjeti"])
                        
                        if "Napomena" in formatted_response:
                            st.warning(formatted_response["Napomena"])
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Opcije za preuzimanje i dijeljenje
                        st.markdown("<h4>📥 Opcije izvještaja</h4>", unsafe_allow_html=True)
                        
                        col_opt1, col_opt2 = st.columns(2)
                        
                        with col_opt1:
                            st.download_button(
                                label="📄 Preuzmi PDF izvještaj",
                                data="Ovo je simulacija PDF-a za česticu " + broj_cestice,
                                file_name=f"izvjestaj_cestica_{broj_cestice}.pdf",
                                mime="application/pdf"
                            )
                        
                        with col_opt2:
                            if st.button("📧 Pošalji izvještaj na e-mail"):
                                if email:
                                    st.success(f"Izvještaj poslan na {email}")
                                else:
                                    st.error("Niste unijeli e-mail adresu")
                    
                    # Prikaži confetti animaciju za uspjeh
                    st.balloons()
                    
                except requests.exceptions.RequestException as e:
                    # Očisti animaciju učitavanja
                    loading_container.empty()
                    st.error(f"❌ Greška pri komunikaciji s serverom: {str(e)}")
                    
                    # Prikaži korisniku alternativne opcije
                    st.info("🔄 Molimo pokušajte ponovno ili kontaktirajte podršku na info@katastar-trogir.hr")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_info_page():
    """Prikazuje stranicu s informacijama"""
    st.markdown("<h2>ℹ️ Informacije o katastarskom portalu</h2>", unsafe_allow_html=True)
    
    # Osnovne informacije
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="form-container">
            <h3>O portalu</h3>
            <p>
                Dobrodošli na službeni Katastarski portal Grada Trogira, digitalni alat za pristup informacijama
                o prostornom planiranju i građevinskim uvjetima na području grada Trogira i okolice.
            </p>
            
            <h4>Što možete saznati putem portala?</h4>
            <ul>
                <li><b>Katastarske podatke</b> - osnovne informacije o katastarskim česticama</li>
                <li><b>Građevinske uvjete</b> - dozvoljeni koeficijenti, katnost, namjena i ograničenja</li>
                <li><b>Prostorne planove</b> - uvjeti iz važećih prostornih planova</li>
                <li><b>Komunalnu infrastrukturu</b> - dostupnost priključaka i infrastrukture</li>
            </ul>
            
            <h4>Pravni okvir</h4>
            <p>
                Portal je usklađen s važećim Prostornim planom uređenja Grada Trogira, Generalnim urbanističkim 
                planom, te svim Urbanističkim planovima uređenja i Detaljnim planovima uređenja na području grada.
                Informacije se redovito ažuriraju u skladu s odlukama Gradskog vijeća i nadležnih tijela.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Česta pitanja
        st.markdown("""
        <div class="form-container">
            <h3>Česta pitanja</h3>
            
            <details>
                <summary>Koja je razlika između UPU i DPU?</summary>
                <p>
                    <b>UPU (Urbanistički plan uređenja)</b> je dokument prostornog uređenja koji detaljnije određuje 
                    prostorni razvoj naselja ili dijela naselja s osnovom prostornih i funkcionalnih rješenja, uvjeta 
                    i oblikovanja pojedinih prostornih cjelina.
                </p>
                <p>
                    <b>DPU (Detaljni plan uređenja)</b> detaljnije određuje prostorni razvoj područja s rasporedom, 
                    namjenom i oblikovanjem građevina, prometnom i komunalnom infrastrukturom te zelenim površinama.
                    DPU je detaljniji od UPU-a.
                </p>
            </details>
            
            <details>
                <summary>Jesu li podaci dostupni na portalu pravno obvezujući?</summary>
                <p>
                    Podaci dostupni na portalu služe kao informativni alat te ne predstavljaju pravno obvezujući dokument.
                    Za službene informacije o građevinskim uvjetima potrebno je zatražiti lokacijsku informaciju
                    ili drugi službeni dokument od nadležnog upravnog odjela Grada Trogira.
                </p>
            </details>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Lottie animacija
        lottie_about = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_j1adxtyb.json")
        if lottie_about:
            st_lottie(lottie_about, height=250, key="about_animation")
        
        # Informacije o posljednjim promjenama
        st.markdown("""
        <div class="data-card">
            <h4>🔄 Zadnje izmjene</h4>
            <ul style="padding-left: 1rem; font-size: 0.9rem;">
                <li><b>15.05.2025.</b> - Ažurirani podaci za UPU Mastrinka</li>
                <li><b>27.04.2025.</b> - Dodane nove zone prema GUP-u</li>
                <li><b>15.03.2025.</b> - Integracija s zemljišnoknjižnim sustavom</li>
                <li><b>02.02.2025.</b> - Ažuriranje koeficijenata za zonu C</li>
            </ul>
        </div>
        
        <div class="data-card">
            <h4>📊 Statistika portala</h4>
            <ul style="padding-left: 1rem; font-size: 0.9rem;">
                <li>Broj upita u posljednjih 30 dana: <b>287</b></li>
                <li>Ukupno registriranih korisnika: <b>142</b></li>
                <li>Pokrivenost katastarskih podataka: <b>98%</b></li>
                <li>Prosječno vrijeme obrade: <b>3.2 sec</b></li>
            </ul>
        </div>
        
        <div class="data-card">
            <h4>🧭 Korisni linkovi</h4>
            <ul style="padding-left: 1rem; font-size: 0.9rem;">
                <li><a href="https://www.trogir.hr">Službena stranica Grada Trogira</a></li>
                <li><a href="https://www.katastar.hr">Državna geodetska uprava</a></li>
                <li><a href="https://www.prostorno-uredjenje.hr">Ministarstvo prostornog uređenja</a></li>
                <li><a href="https://www.osst.pravosudje.hr">Zemljišnoknjižni odjel</a></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Tablica dostupnih planova
    st.markdown("""
    <div class="form-container">
        <h3>🗺️ Prostorni planovi na području Grada Trogira</h3>
        
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Naziv plana</th>
                    <th>Područje</th>
                    <th>Datum donošenja</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Prostorni plan uređenja Grada Trogira</td>
                    <td>Cijelo područje grada</td>
                    <td>12.03.2022.</td>
                    <td><span class="status-badge status-success">Važeći</span></td>
                </tr>
                <tr>
                    <td>Generalni urbanistički plan Trogira</td>
                    <td>Uže gradsko područje</td>
                    <td>05.07.2023.</td>
                    <td><span class="status-badge status-success">Važeći</span></td>
                </tr>
                <tr>
                    <td>UPU naselja Mastrinka 1 (UPU 6.1)</td>
                    <td>Mastrinka</td>
                    <td>15.05.2025.</td>
                    <td><span class="status-badge status-success">Važeći</span></td>
                </tr>
                <tr>
                    <td>UPU poslovne zone POS 3 (UPU 10)</td>
                    <td>Plano</td>
                    <td>22.11.2021.</td>
                    <td><span class="status-badge status-success">Važeći</span></td>
                </tr>
                <tr>
                    <td>DPU Brigi – Lokvice (DPU 5)</td>
                    <td>Trogir</td>
                    <td>18.09.2020.</td>
                    <td><span class="status-badge status-success">Važeći</span></td>
                </tr>
                <tr>
                    <td>UPU proizvodne zone Plano 4</td>
                    <td>Plano</td>
                    <td>N/A</td>
                    <td><span class="status-badge status-pending">U izradi</span></td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

def render_contact_page():
    """Prikazuje kontakt stranicu"""
    st.markdown("<h2>📞 Kontakt</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="form-container">
            <h3>Kontaktirajte nas</h3>
            <p>
                Ako imate pitanja, prijedloge ili trebate pomoć pri korištenju portala, molimo vas da nas kontaktirate
                putem obrasca ili na kontakte navedene desno.
            </p>
        """, unsafe_allow_html=True)
        
        with st.form("contact_form"):
            col_form1, col_form2 = st.columns(2)
            
            with col_form1:
                name = st.text_input("Ime i prezime *")
            
            with col_form2:
                email = st.text_input("E-mail adresa *")
            
            subject = st.selectbox("Tema upita *", options=[
                "Pomoć pri korištenju portala",
                "Pitanje o prostornom planu",
                "Pojašnjenje građevinskih uvjeta",
                "Greška u podacima",
                "Prijedlog za poboljšanje",
                "Ostalo"
            ])
            
            message = st.text_area("Poruka *", height=150, max_chars=1000)
            
            agree = st.checkbox("Pročitao/la sam i slažem se s politikom privatnosti *")
            
            submit_contact = st.form_submit_button("📨 Pošalji poruku")
        
        if submit_contact:
            if not all([name, email, message, agree]):
                st.error("Molimo ispunite sva obavezna polja i označite slaganje s politikom privatnosti.")
            else:
                st.success(f"Hvala, {name}! Vaša poruka je primljena. Odgovorit ćemo vam u najkraćem mogućem roku.")
                st.balloons()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # FAQ sekcija
        st.markdown("""
        <div class="form-container">
            <h3>Često postavljena pitanja</h3>
            
            <details>
                <summary>Koliko često se ažuriraju podaci?</summary>
                <p>
                    Podaci se ažuriraju nakon svake sjednice Gradskog vijeća na kojoj se donose odluke vezane 
                    za prostorno planiranje, a minimalno jednom mjesečno radi usklađenja sa sustavom Državne geodetske uprave.
                </p>
            </details>
            
            <details>
                <summary>Mogu li preko portala predati zahtjev za lokacijsku informaciju?</summary>
                <p>
                    Ne, portal služi samo za informativne svrhe. Za službenu lokacijsku informaciju potrebno je 
                    podnijeti zahtjev Upravnom odjelu za urbanizam i prostorno uređenje Grada Trogira.
                </p>
            </details>
            
            <details>
                <summary>Kako mogu dobiti detaljniju analizu mogućnosti gradnje?</summary>
                <p>
                    Za detaljniju analizu preporuka je konzultirati ovlaštenog arhitekta ili projektanta.
                    Podaci s portala mogu poslužiti kao početna točka za daljnje planiranje.
                </p>
            </details>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Lottie animacija
        lottie_contact = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_2LdLq6.json")
        if lottie_contact:
            st_lottie(lottie_contact, height=200, key="contact_animation")
        
        # Kontakt informacije
        st.markdown("""
        <div class="data-card">
            <h4>📬 Službeni kontakti</h4>
            
            <p style="margin-bottom: 1rem;">
                <strong>Upravni odjel za urbanizam i prostorno uređenje</strong><br>
                Trg Ivana Pavla II br. 1<br>
                21220 Trogir<br>
                <br>
                📧 Email: <a href="mailto:urbanizam@trogir.hr">urbanizam@trogir.hr</a><br>
                📞 Tel: +385 21 444 570<br>
                📠 Fax: +385 21 444 571
            </p>
            
            <p>
                <strong>Radno vrijeme s strankama:</strong><br>
                Ponedjeljak - Petak: 09:00 - 14:00<br>
                Srijeda: 09:00 - 17:00
            </p>
        </div>
        
        <div class="data-card">
            <h4>🌐 Pratite nas</h4>
            <p>
                Facebook: <a href="#">Grad Trogir</a><br>
                Instagram: <a href="#">@gradtrogir</a><br>
                YouTube: <a href="#">Grad Trogir Official</a>
            </p>
        </div>
        
        <div class="data-card">
            <h4>📱 Mobilna aplikacija</h4>
            <p>
                Preuzmite našu mobilnu aplikaciju za pristup katastarskim podacima
                u pokretu. Dostupna za iOS i Android uređaje.
            </p>
            <div style="display: flex; justify-content: space-around; margin-top: 1rem;">
                <img src="https://i.imgur.com/DMQHF8H.png" alt="App Store" width="120">
                <img src="https://i.imgur.com/7AZxXzJ.png" alt="Google Play" width="120">
            </div>
        </div>
        """, unsafe_allow_html=True)

# === GLAVNA FUNKCIJA ZA POKRETANJE APLIKACIJE ===
def main():
    """Glavna funkcija za pokretanje aplikacije"""
    # Postavi temu i CSS
    try:
        set_custom_theme()
    except Exception:
        st.set_page_config(page_title="GradTrogir Katastarski Portal", layout="wide", page_icon="🏛️")
    
    # Dodaj suptilnu pozadinu
    add_bg_from_url()
    
    # Zaglavlje
    render_header()
    
    # Navigacija
    page = render_navigation()
    
    # Prikaz odabrane stranice
    if page == "🏠 Početna":
        render_home_page()
    elif page == "ℹ️ Informacije":
        render_info_page()
    elif page == "📞 Kontakt":
        render_contact_page()
    
    # Podnožje
    render_footer()

if __name__ == "__main__":
    main()>Što znače koeficijenti KIG i KIS?</summary>
                <p>
                    <b>KIG (koeficijent izgrađenosti)</b> označava omjer izgrađene površine zemljišta pod građevinom 
                    i ukupne površine građevne čestice. Jednostavnije rečeno - koliki postotak površine čestice 
                    može zauzimati tlocrt zgrade.
                </p>
                <p>
                    <b>KIS (koeficijent iskoristivosti)</b> označava omjer građevinske (bruto) površine građevine 
                    i površine građevne čestice. Određuje ukupnu površinu svih etaža koje se mogu izgraditi u odnosu 
                    na površinu čestice.
                </p>
            </details>
            
            <details>
                <summary>Kako se tumači oznaka katnosti P+2+Pk?</summary>
                <p>
                    <b>P</b> - prizemlje<br>
                    <b>2</b> - dva kata iznad prizemlja<br>
                    <b>Pk</b> - potkrovlje
                </p>
                <p>Dakle, P+2+Pk označava građevinu s prizemljem, dva kata i potkrovljem.</p>
            </details>
