import streamlit as st
import pandas as pd
import numpy as np
import requests
from streamlit_lottie import st_lottie
import plotly.graph_objects as go
from PIL import Image

# Postavke stranice
st.set_page_config(
    page_title="Architecto | Vaši savršeni tlocrti",
    layout="wide",
    page_icon="🏡",
    initial_sidebar_state="expanded"
)

# Prilagođeni CSS
st.markdown("""
<style>
    /* Glavni font i boje */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    h1, h2, h3 {
        font-weight: 600 !important;
        color: #2c3e50;
    }
    
    /* Prilagodba navigacije */
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    
    /* Glavni kontejneri */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Stilizacija kartica */
    .css-1r6slb0, .css-1kyxreq {
        border-radius: 10px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Gumbi */
    .stButton>button {
        border-radius: 5px;
        background-color: #3498db;
        color: white;
        font-weight: 500;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #2980b9;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Prilagođeni izgled formi */
    .stTextInput, .stNumberInput, .stSelectbox {
        margin-bottom: 1rem;
    }
    
    /* Korisni predmeti */
    .icon-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        transition: all 0.3s;
    }
    
    .icon-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Izbornik navigacije */
    .nav-link {
        color: #3498db;
        text-decoration: none;
        margin-right: 1rem;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: all 0.3s;
    }
    
    .nav-link:hover {
        background-color: #ecf0f1;
    }
    
    /* Galerija */
    .gallery-item {
        margin-bottom: 1rem;
        border-radius: 10px;
        overflow: hidden;
        transition: all 0.3s;
    }
    
    .gallery-item:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    
    /* Metri kvadratni badge */
    .m2-badge {
        background-color: #3498db;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    /* Oznake */
    .tag {
        display: inline-block;
        background-color: #e9f7fe;
        color: #3498db;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .divider {
        height: 3px;
        background: linear-gradient(90deg, #3498db, #2ecc71);
        margin: 2rem 0;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# === Funkcija za učitavanje Lottie animacije ===
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        st.warning(f"Greška pri učitavanju animacije: {e}")
        return None

# === Lottie animacije za različite stranice ===
lottie_home = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_7v6fiely.json")  # House blueprint animation
lottie_calculator = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_bbuyddcp.json")  # Calculator
lottie_gallery = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_2JGahp.json")  # Gallery
lottie_contact = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_5mhyg2hz.json")  # Contact message

# === Funkcija za generiranje primjera tlocrta ===
def generate_floor_plan(width=10, length=12, rooms=4):
    # Generiranje nasumičnog tlocrta
    fig = go.Figure()
    
    # Vanjski obris kuće
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=width, y1=length,
        line=dict(color="black", width=2),
        fillcolor="white"
    )
    
    # Dodavanje unutarnjih zidova (pojednostavljeno)
    for i in range(1, rooms):
        # Horizontalni zid
        y_pos = length * i / rooms
        fig.add_shape(
            type="line",
            x0=0, y0=y_pos, x1=width, y1=y_pos,
            line=dict(color="black", width=2)
        )
        
        # Vrata u zidu
        door_pos = np.random.uniform(1, width-1)
        fig.add_shape(
            type="line",
            x0=door_pos-0.5, y0=y_pos, x1=door_pos+0.5, y1=y_pos,
            line=dict(color="white", width=2)
        )
    
    # Dodavanje vanjskih vrata
    fig.add_shape(
        type="line",
        x0=width/2-0.5, y0=0, x1=width/2+0.5, y1=0,
        line=dict(color="red", width=3)
    )
    
    # Dodavanje prozora
    for i in range(1, 4):
        fig.add_shape(
            type="line",
            x0=width*i/4, y0=length, x1=width*i/4+1, y1=length,
            line=dict(color="blue", width=3)
        )
    
    # Izgled grafa
    fig.update_shapes(dict(xref='x', yref='y'))
    fig.update_layout(
        title="Tlocrt kuće",
        width=500,
        height=500,
        showlegend=False,
        plot_bgcolor='white',
        margin=dict(l=0, r=0, b=0, t=40),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False, scaleanchor="x", scaleratio=1)
    )
    
    return fig

# === Funkcija za generiranje 3D tlocrta ===
def generate_3d_floor_plan(width=10, length=12, height=3):
    # Generiranje 3D tlocrta
    x = np.array([0, width, width, 0, 0])
    y = np.array([0, 0, length, length, 0])
    z = np.array([0, 0, 0, 0, 0])
    
    x_roof = np.array([0, width, width, 0, 0])
    y_roof = np.array([0, 0, length, length, 0])
    z_roof = np.array([height, height, height, height, height])
    
    # Stvaranje bočnih strana
    fig = go.Figure()
    
    # Donji dio (pod)
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(color='black', width=4),
        name='Floor'
    ))
    
    # Gornji dio (krov)
    fig.add_trace(go.Scatter3d(
        x=x_roof, y=y_roof, z=z_roof,
        mode='lines',
        line=dict(color='black', width=4),
        name='Roof'
    ))
    
    # Povezivanje donjeg i gornjeg dijela (zidovi)
    for i in range(4):
        fig.add_trace(go.Scatter3d(
            x=[x[i], x[i]],
            y=[y[i], y[i]],
            z=[z[i], z_roof[i]],
            mode='lines',
            line=dict(color='black', width=4),
            name=f'Wall {i+1}'
        ))
    
    # Podešavanje pogleda
    fig.update_layout(
        title="3D prikaz kuće",
        width=600,
        height=500,
        scene=dict(
            aspectmode='data',
            xaxis=dict(
                showbackground=False,
                showticklabels=False,
                title=''
            ),
            yaxis=dict(
                showbackground=False,
                showticklabels=False,
                title=''
            ),
            zaxis=dict(
                showbackground=False,
                showticklabels=False,
                title=''
            )
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        showlegend=False
    )
    
    return fig

# === Primjeri tlocrta za galeriju ===
def sample_floor_plans():
    return [
        {
            "name": "Moderna vila",
            "area": 180,
            "rooms": 5,
            "description": "Moderna vila s otvorenim konceptom i velikim staklenim površinama.",
            "tags": ["Moderna", "Luksuzna", "Prizemnica"]
        },
        {
            "name": "Obiteljska kuća",
            "area": 120,
            "rooms": 4,
            "description": "Tradicionalna obiteljska kuća s funkcionalnim rasporedom prostorija.",
            "tags": ["Obiteljska", "Klasična", "Katnica"]
        },
        {
            "name": "Studio apartman",
            "area": 45,
            "rooms": 1,
            "description": "Kompaktni studio apartman s pametnim iskorištavanjem prostora.",
            "tags": ["Mali prostor", "Urbano", "Studio"]
        },
        {
            "name": "Duplex",
            "area": 160,
            "rooms": 6,
            "description": "Prostrani duplex s odvojenim spavaćim i dnevnim prostorom na različitim etažama.",
            "tags": ["Duplex", "Prostran", "Moderan"]
        },
        {
            "name": "Penthouse",
            "area": 220,
            "rooms": 7,
            "description": "Luksuzni penthouse s velikom terasom i panoramskim pogledom.",
            "tags": ["Luksuzni", "Penthouse", "Terasa"]
        },
        {
            "name": "Vikendica",
            "area": 80,
            "rooms": 3,
            "description": "Ugodna drvena vikendica s rustikalnim elementima i otvorenim krovištem.",
            "tags": ["Vikendica", "Rustikalna", "Drvo"]
        }
    ]

# === NAVIGACIJA ===
def main():
    with st.sidebar:
        st.image("/api/placeholder/150/50", use_column_width=True)
        st.markdown("# 🏡 Architecto")
        st.markdown("### Vaši savršeni tlocrti")
        
        st.markdown("---")
        
        st.markdown("### Navigacija")
        page = st.radio("", 
                       ["🏠 Početna", 
                        "🧮 Kalkulator prostora", 
                        "🖼️ Galerija projekata", 
                        "📞 Kontaktirajte nas"], 
                       label_visibility="collapsed")
        
        st.markdown("---")
        
        st.markdown("### Naši kontakti")
        st.markdown("""
        📍 Ulica arhitekata 123, Split  
        📱 +385 21 456 789  
        ✉️ info@architecto.hr
        """)

    if page == "🏠 Početna":
        home_page()
    elif page == "🧮 Kalkulator prostora":
        calculator_page()
    elif page == "🖼️ Galerija projekata":
        gallery_page()
    elif page == "📞 Kontaktirajte nas":
        contact_page()

# === HOME PAGE ===
def home_page():
    # Hero sekcija
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("# Projektiramo savršene tlocrte za vaš dom")
        st.markdown("""
        Specijalizirani smo za izradu funkcionalnih i estetski privlačnih tlocrta koji optimiziraju svaki centimetar vašeg životnog prostora.
        Pretvaramo vaše ideje i želje u stvarnost kroz precizno dizajnirane tlocrte koji odražavaju vaš životni stil.
        """)
        
        c1, c2 = st.columns(2)
        with c1:
            st.button("🧮 Izračunajte prostor", use_container_width=True)
        with c2:
            st.button("📋 Zatražite ponudu", use_container_width=True)
            
    with col2:
        if lottie_home:
            st_lottie(lottie_home, height=300, key="home_animation")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Naše usluge
    st.markdown("## Naše usluge")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="icon-box">', unsafe_allow_html=True)
        st.markdown("### 📝 Dizajn tlocrta")
        st.markdown("""
        Izrada detaljnih i preciznih tlocrta za stambene i poslovne prostore, prilagođenih vašim potrebama i željama.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="icon-box">', unsafe_allow_html=True)
        st.markdown("### 🔍 Optimizacija prostora")
        st.markdown("""
        Analiza prostornih mogućnosti i savjeti za maksimalno iskorištavanje dostupnog prostora uz zadržavanje funkcionalnosti.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="icon-box">', unsafe_allow_html=True)
        st.markdown("### 🏗️ 3D vizualizacija")
        st.markdown("""
        Pretvaranje 2D tlocrta u 3D modele kako biste mogli dobiti bolji uvid i osjećaj za budući prostor.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Kako radimo
    st.markdown("## Kako radimo")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        fig = generate_floor_plan(8, 10, 3)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("### Naš proces dizajniranja")
        st.markdown("""
        1. **Konzultacije** - Slušamo vaše potrebe i želje
        2. **Analiza prostora** - Procjenjujemo mogućnosti i ograničenja
        3. **Inicijalni koncept** - Izrađujemo prvu verziju tlocrta
        4. **Povratne informacije** - Prilagođavamo tlocrt prema vašim komentarima
        5. **Finalizacija** - Dovršavamo tlocrt s detaljima i specifikacijama
        6. **Isporuka** - Dobivate kompletnu dokumentaciju u željenim formatima
        """)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Statistika
    st.markdown("## Zašto nas odabrati")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        ### 250+
        #### Završenih projekata
        """)
    
    with col2:
        st.markdown("""
        ### 15+
        #### Godina iskustva
        """)
    
    with col3:
        st.markdown("""
        ### 98%
        #### Zadovoljnih klijenata
        """)
    
    with col4:
        st.markdown("""
        ### 20+
        #### Stručnih suradnika
        """)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Izdvojeni projekti
    st.markdown("## Izdvojeni projekti")
    
    col1, col2, col3 = st.columns(3)
    
    plans = sample_floor_plans()
    
    with col1:
        st.plotly_chart(generate_floor_plan(12, 10, 4), use_container_width=True)
        st.markdown(f"**{plans[0]['name']}** <span class='m2-badge'>{plans[0]['area']} m²</span>", unsafe_allow_html=True)
        st.markdown(f"{plans[0]['description']}")
        
    with col2:
        st.plotly_chart(generate_floor_plan(10, 12, 5), use_container_width=True)
        st.markdown(f"**{plans[1]['name']}** <span class='m2-badge'>{plans[1]['area']} m²</span>", unsafe_allow_html=True)
        st.markdown(f"{plans[1]['description']}")
        
    with col3:
        st.plotly_chart(generate_floor_plan(8, 8, 2), use_container_width=True)
        st.markdown(f"**{plans[2]['name']}** <span class='m2-badge'>{plans[2]['area']} m²</span>", unsafe_allow_html=True)
        st.markdown(f"{plans[2]['description']}")
    
    c1, c2 = st.columns([1, 4])
    with c1:
        st.button("Pogledajte sve projekte", use_container_width=True)

# === CALCULATOR PAGE ===
def calculator_page():
    st.markdown("# 🧮 Kalkulator prostora")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Koristite naš interaktivni kalkulator prostora za izračun veličina, proporcija i optimalne raspodjele prostorija u vašem budućem domu.
        """)
    
    with col2:
        if lottie_calculator:
            st_lottie(lottie_calculator, height=200, key="calc_animation")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Kalkulator
    col1, col2 = st.columns([1, 1])
    
    with col1:
        with st.form("calculator_form"):
            st.subheader("Osnovni parametri")
            
            ukupna_povrsina = st.number_input("Ukupna površina (m²)", min_value=20.0, max_value=1000.0, value=100.0, step=10.0)
            
            st.markdown("### Broj prostorija")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                br_spavacih = st.number_input("Spavaće sobe", min_value=0, max_value=10, value=2)
            with col_b:
                br_kupaonica = st.number_input("Kupaonice", min_value=1, max_value=5, value=1)
            with col_c:
                br_ostalih = st.number_input("Ostale prostorije", min_value=0, max_value=10, value=2)
            
            st.markdown("### Preferencije dizajna")
            stil = st.select_slider(
                "Stil dizajna",
                options=["Moderan", "Suvremeni", "Tradicionalan", "Minimalistički", "Rustikalan"],
                value="Suvremeni"
            )
            
            otvoreni_koncept = st.checkbox("Otvoreni koncept (dnevni boravak + kuhinja)", value=True)
            
            submitted = st.form_submit_button("Izračunaj i prikaži tlocrt")
    
    with col2:
        st.markdown("### Rezultati izračuna")
        
        # Simulacija izračuna
        if st.session_state.get('submitted') or submitted:
            st.session_state['submitted'] = True
            
            # Izračun veličina prostorija
            ukupno_soba = br_spavacih + br_kupaonica + br_ostalih + (0 if otvoreni_koncept else 2)
            
            # Prikazujemo rezultate
            st.markdown("#### Preporučene dimenzije prostorija")
            
            # Generiraj tablicu s podacima
            data = []
            
            # Dnevni boravak + kuhinja
            if otvoreni_koncept:
                area_living = ukupna_povrsina * 0.4
                data.append(["Dnevni boravak + kuhinja", f"{area_living:.1f} m²", f"{int(area_living / 3)}m × {int(area_living / 4)}m"])
            else:
                area_living = ukupna_povrsina * 0.25
                area_kitchen = ukupna_povrsina * 0.15
                data.append(["Dnevni boravak", f"{area_living:.1f} m²", f"{int(area_living / 3)}m × {int(area_living / 4)}m"])
                data.append(["Kuhinja", f"{area_kitchen:.1f} m²", f"{int(area_kitchen / 2)}m × {int(area_kitchen / 3)}m"])
            
            # Spavaće sobe
            room_area = ukupna_povrsina * 0.15
            for i in range(br_spavacih):
                area = room_area if i == 0 else room_area * 0.8
                data.append([f"Spavaća soba {i+1}", f"{area:.1f} m²", f"{int(area / 3)}m × {int(area / 4)}m"])
            
            # Kupaonice
            bath_area = ukupna_povrsina * 0.08
            for i in range(br_kupaonica):
                area = bath_area if i == 0 else bath_area * 0.7
                data.append([f"Kupaonica {i+1}", f"{area:.1f} m²", f"{int(area / 2)}m × {int(area / 2.5)}m"])
            
            # Ostale prostorije
            other_area = ukupna_povrsina * 0.05
            for i in range(br_ostalih):
                data.append([f"Prostorija {i+1}", f"{other_area:.1f} m²", f"{int(other_area / 2)}m × {int(other_area / 2.5)}m"])
            
            # Prikaz tablice
            df = pd.DataFrame(data, columns=["Prostorija", "Površina", "Približne dimenzije"])
            st.table(df)
            
            # Dodajemo 3D prikaz
            st.subheader("Vizualizacija tlocrta")
            total_rooms = br_spavacih + br_kupaonica + br_ostalih + (1 if otvoreni_koncept else 2)
            fig = generate_floor_plan(10, 12, total_rooms)
            st.plotly_chart(fig, use_container_width=True)
            
            # Opcija za 3D prikaz
            show_3d = st.checkbox("Prikaži 3D vizualizaciju")
            if show_3d:
                fig_3d = generate_3d_floor_plan(10, 12, 3)
                st.plotly_chart(fig_3d, use_container_width=True)
            
            st.info("Ovo su okvirne procjene bazirane na uobičajenim arhitektonskim standardima. Za precizniji tlocrt prilagođen vašim potrebama, kontaktirajte naše stručnjake.")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Savjeti za optimizaciju prostora
    st.markdown("## Savjeti za optimizaciju prostora")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🧩 Multifunkcionalni namještaj")
        st.markdown("""
        Koristite namještaj koji ima više funkcija, poput kreveta s ladicama za pohranu, sklopivih stolova ili sofa koje se mogu pretvoriti u krevet.
        """)
    
    with col2:
        st.markdown("### 📏 Proporcije prostorija")
        st.markdown("""
        Idealne proporcije za ugodnost boravka su 2:3 ili 3:5. Izbjegavajte dugačke, uske prostorije kad god je to moguće.
        """)
    
    with col3:
        st.markdown("### 🌳 Povezanost s vanjskim prostorima")
        st.markdown("""
        Dobro projektirani tlocrt uzima u obzir i vanjski prostor - orijentaciju, poglede i pristup terasi ili vrtu.
        """)

# === GALLERY PAGE ===
def gallery_page():
    st.markdown("# 🖼️ Galerija projekata")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Pregledajte našu galeriju prethodno realiziranih projekata. 
        Filtrirajte prema veličini, broju prostorija ili stilu kako biste pronašli inspiraciju za svoj dom.
        """)
    
    with col2:
        if lottie_gallery:
            st_lottie(lottie_gallery, height=200, key="gallery_animation")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Filteri
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_area = st.slider("Površina (m²)", 30, 300, (50, 150))
    
    with col2:
        filter_rooms = st.multiselect(
            "Broj prostorija",
            options=[1, 2, 3, 4, 5, 6, 7, "8+"],
            default=[3, 4, 5]
        )
    
    with col3:
        filter_style = st.selectbox(
            "Stil",
            options=["Svi stilovi", "Moderni", "Klasični", "Minimalistički", "Rustikalni", "Luksuzni"],
            index=0
        )
    
    st.markdown("---")
    
    # Prikaz projekata
    plans = sample_floor_plans()
    
    # Prikaz po redovima
    for i in range(0, len(plans), 3):
        cols = st.columns(3)
        
        for j in range(3):
            if i + j < len(plans):
                plan = plans[i + j]
                
                with cols[j]:
                    st.markdown('<div class="gallery-item">', unsafe_allow_html=True)
                    
                    # Tlocrt
                    fig = generate_floor_plan(10, 12, plan["rooms"])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Informacije
                    st.markdown(f"### {plan['name']}")
                    st.markdown(f"**Površina:** <span class='m2-badge'>{plan['area']} m²</span>", unsafe_allow_html=True)
                    st.markdown(f"**Broj prostorija:** {plan['rooms']}")
                    st.markdown(f"{plan['description']}")
                    
                    # Tagovi
                    tags_html = ""
                    for tag in plan["tags"]:
                        tags_html += f'<span class="tag">{tag}</span>'
                    st.markdown(tags_html, unsafe_allow_html=True)
                    
                    # Gumbi
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.button(f"Detalji {i+j+1}", key=f"details_{i+j}")
                    with col_b:
                        st.button(f"3D prikaz {i+j+1}", key=f"3d_{i+j}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
