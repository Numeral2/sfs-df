import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
import time
import json
from pyproj import Transformer

# --- POSTAVKE ---
LOKALNA_BAZA_PLANOVA = 'samo_dpu_planovi.json' 

# --- FUNKCIJE (iste kao u prethodnim skriptama) ---
def get_coordinates_from_nominatim(address: str):
    """Koristi Nominatim za geokodiranje adrese."""
    headers = {'User-Agent': 'StreamlitMapApp/1.0 (saric.rokov@gmail.com)'} # Prilagođen User-Agent
    geocoding_url = "https://nominatim.openstreetmap.org/search"
    params = {'q': address, 'format': 'json', 'limit': 1, 'countrycodes': 'hr'}
    
    try:
        response = requests.get(geocoding_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data:
            loc = data[0]
            st.session_state.display_name = loc.get('display_name')
            return float(loc['lat']), float(loc['lon'])
    except Exception as e:
        st.error(f"Greška pri geokodiranju: {e}")
    finally:
        time.sleep(1)
    return None, None

def transform_wgs84_to_htrs96(lon: float, lat: float):
    """Transformira WGS84 (EPSG:4326) u HTRS96/TM (EPSG:3765)."""
    try:
        transformer = Transformer.from_crs("epsg:4326", "epsg:3765", always_xy=True)
        return transformer.transform(lon, lat)
    except Exception as e:
        st.error(f"Greška kod transformacije koordinata: {e}")
        return None, None

# --- Učitavanje baze planova ---
@st.cache_data # Keširanje podataka da se ne učitavaju svaki put
def load_plan_data():
    try:
        with open(LOKALNA_BAZA_PLANOVA, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"GREŠKA: Datoteka '{LOKALNA_BAZA_PLANOVA}' nije pronađena. Molim kreirajte je prvo.")
        return []

svi_dpu_planovi = load_plan_data()

# --- STREAMLIT APLIKACIJA ---
st.set_page_config(layout="wide")
st.title("🗺️ Interaktivna Mapa s DPU Pretragom")
st.write("Unesite adresu, a aplikacija će prikazati lokaciju na mapi i pronaći DPU planove koji je obuhvaćaju.")

# Inicijalizacija session state varijabli za mapu i koordinate
if 'map_center' not in st.session_state:
    st.session_state.map_center = [43.508133, 16.440193] # Centar Splita
if 'map_zoom' not in st.session_state:
    st.session_state.map_zoom = 13
if 'marker_location' not in st.session_state:
    st.session_state.marker_location = None
if 'display_name' not in st.session_state:
    st.session_state.display_name = ""

# Unos adrese
address_input = st.text_input("Unesite adresu (npr. 'Put Duilova 23, Split'):", key="address_input")

if st.button("Pronađi na mapi i pretraži DPU", key="search_button"):
    if address_input and svi_dpu_planovi:
        latitude, longitude = get_coordinates_from_nominatim(address_input)

        if latitude and longitude:
            st.session_state.map_center = [latitude, longitude]
            st.session_state.map_zoom = 16 # Približi mapu na pronađenu lokaciju
            st.session_state.marker_location = [latitude, longitude]
            
            st.subheader(f"Pronađena lokacija: {st.session_state.display_name}")
            st.write(f"Koordinate (WGS84): Lat: {latitude:.6f}, Lon: {longitude:.6f}")

            # Transformacija i pretraga DPU
            x_htrs, y_htrs = transform_wgs84_to_htrs96(longitude, latitude)
            if x_htrs and y_htrs:
                st.write(f"Koordinate (HTRS96/TM): X: {x_htrs:.2f}, Y: {y_htrs:.2f}")
                
                pronaslani_dpu_planovi = []
                for plan in svi_dpu_planovi:
                    bbox = plan['bbox_htrs96']
                    if (bbox['minx'] <= x_htrs <= bbox['maxx']) and \
                       (bbox['miny'] <= y_htrs <= bbox['maxy']):
                        pronaslani_dpu_planovi.append(plan)
                
                if pronaslani_dpu_planovi:
                    st.subheader(f"Pronađeno {len(pronaslani_dpu_planovi)} DPU planova koji obuhvaćaju adresu:")
                    for i, plan_info in enumerate(pronaslani_dpu_planovi, 1):
                        st.markdown(f"**{i}. {plan_info['naziv_plana']}** (Sloj: `{plan_info['ime_sloja']}`)")
                        # Ovdje možete dodati i iscrtavanje bounding boxa na mapu ako želite
                        # folium.Rectangle(bounds=[[min_lat, min_lon], [max_lat, max_lon]], ...).add_to(m)
                else:
                    st.warning("Za ovu lokaciju nije pronađen nijedan DPU plan u lokalnoj bazi.")
            else:
                st.error("Nije bilo moguće transformirati koordinate za pretragu DPU.")
        else:
            st.error("Adresa nije pronađena. Pokušajte s drugom adresom.")
    elif not svi_dpu_planovi:
        st.error(f"Baza DPU planova '{LOKALNA_BAZA_PLANOVA}' je prazna ili nije učitana.")
    else:
        st.warning("Molimo unesite adresu.")

# Prikaz Folium mape
m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.map_zoom, tiles="OpenStreetMap")

if st.session_state.marker_location:
    folium.Marker(
        st.session_state.marker_location, 
        popup=st.session_state.display_name if st.session_state.display_name else "Pronađena lokacija",
        tooltip="Pronađena lokacija"
    ).add_to(m)

# Koristimo st_folium za prikaz mape; output je rječnik s podacima o interakciji
st.subheader("Interaktivna Mapa")
map_data = st_folium(m, width=700, height=500)

# Možete ispisati podatke koje st_folium vraća (npr. zadnji kliknuti marker, centar mape, itd.)
# st.write("Podaci s mape (npr. zadnji klik):")
# st.write(map_data)

st.sidebar.info(
    """
    **Kako koristiti:**
    1. Unesite željenu adresu.
    2. Kliknite na gumb "Pronađi na mapi i pretraži DPU".
    3. Aplikacija će prikazati lokaciju na mapi i ispisati DPU planove koji je obuhvaćaju.
    """
)
