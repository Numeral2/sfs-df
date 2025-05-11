import streamlit as st
import requests
import json
import pyperclip

# Konfiguracija
WEBHOOK_URL = "https://primary-production-b791f.up.railway.app/webhook-test/03419cdb-f956-48b4-85d8-725a6a4db8fb"
CHATGPT_API_ENDPOINT = "YOUR_CHATGPT_API_ENDPOINT"  # Zamijeni sa stvarnim endpointom

# Inicijalizacija session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "upit_data" not in st.session_state:
    st.session_state.upit_data = {}

# CSS za bolji izgled
st.markdown("""
<style>
.stTextInput>div>div>input {border-radius: 8px;}
.stSelectbox>div>div>div {border-radius: 8px;}
.stTextArea>div>div>textarea {border-radius: 8px;}
</style>
""", unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([2, 3])

with col1:
    with st.form("upit_forma"):
        st.header("📄 Katastarski upit podaci")
        
        # Podaci o čestici
        broj_cestice = st.text_input("1. Broj katastarske čestice*", help="Unesite broj iz zemljišnika")
        kvadratura = st.number_input("2. Kvadratura (m²)*", min_value=0.0, format="%.2f")
        
        # Dropdowni
        tip_podrucja = st.selectbox("3. Vrsta planskog dokumenta*", 
                                  ["Naselje", "UPU", "DPU"], index=0)
        
        podrucje_map = {
            "Naselje": ["Arbanija", "Divulje", "Drvenik Mali", "Drvenik Veli",
                       "Mastrinka", "Plano", "Trogir", "Žedno"],
            "UPU": ["UPU Krban", "UPU naselja Žedno", "UPU poslovne zone POS 3 (UPU 10)",
                   "UPU ugostiteljsko – turističke zone Sveti Križ (UPU 17)",
                   "UPU naselja Mastrinka 1 (UPU 6.1)", "UPU poslovne zone POS 2 (UPU 15)",
                   "UPU naselja Plano (UPU 18)", "UPU proizvodne zone Plano 3 (UPU 7)"],
            "DPU": ["DPU Brigi – Lokvice (DPU 5)",
                   "DPU 1. faze obale od Madiracinog mula do Duhanke (DPU 4)"]
        }
        
        podrucje = st.selectbox(f"4. Odaberi {tip_podrucja.lower()}*", podrucje_map[tip_podrucja])
        zona = st.text_input("5. Zona prema ISPU*")

        # Submit button
        submitted = st.form_submit_button("🚀 Pošalji upit")
        
        if submitted:
            if all([broj_cestice, kvadratura, zona]):
                payload = {
                    "broj_cestice": broj_cestice,
                    "kvadratura": kvadratura,
                    "tip_podrucja": tip_podrucja,
                    "podrucje": podrucje,
                    "zona": zona
                }
                
                try:
                    response = requests.post(
                        WEBHOOK_URL,
                        data=json.dumps(payload),
                        headers={"Content-Type": "application/json"}
                    )
                    
                    st.session_state.upit_data = payload
                    st.success("✅ Upit uspješno poslan!")
                    
                except Exception as e:
                    st.error(f"❌ Greška pri slanju: {str(e)}")
            else:
                st.warning("⚠️ Molimo popunite sva obavezna polja (označena sa *)")

with col2:
    st.header("💬 Chat za upite")
    
    # Prikaz chat poruka
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Postavite pitanje o upitu..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Slanje na ChatGPT API
        with st.spinner("Razmišljam..."):
            try:
                chat_response = f"Odgovor za: {prompt}"  # Zamijeni sa stvarnim API pozivom
                st.session_state.messages.append({"role": "assistant", "content": chat_response})
                
                with st.chat_message("assistant"):
                    st.markdown(chat_response)
                    
            except Exception as e:
                st.error(f"Greška u komunikaciji s API-jem: {str(e)}")

    # Kopiranje upit podataka
    if st.session_state.upit_data:
        st.divider()
        with st.expander("📋 Kopiraj upit podatke"):
            data_str = json.dumps(st.session_state.upit_data, indent=2)
            st.code(data_str, language="json")
            
            if st.button("📄 Kopiraj u clipboard"):
                try:
                    pyperclip.copy(data_str)
                    st.toast("Podaci kopirani u clipboard!", icon="✅")
                except:
                    st.warning("Kopiranje nije podržano na ovom uređaju")

# Sidebar info
with st.sidebar:
    st.markdown("## ℹ️ Upute za korištenje")
    st.markdown("""
    1. Popunite sva obavezna polja u formi
    2. Pritisnite gumb za slanje
    3. Koristite chat za dodatna pitanja
    4. Kopirajte podatke preko ikone 📄
    """)
    
    st.markdown("---")
    st.markdown("**Tehničke specifikacije:**")
    st.markdown("- Python 3.10+")
    st.markdown("- Streamlit 1.33+")
    st.markdown("- Za kopiranje: `pip install pyperclip`")
