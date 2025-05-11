import streamlit as st
import requests

# Webhook URL
webhook_url = 'https://primary-production-b791f.up.railway.app/webhook-test/839b893b-f460-479c-9295-5f3bb8ab3488'

# ChatGPT API URL (zamijeni s vlastitim API-jem)
chatgpt_api_url = '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'

# Funkcija za slanje podataka na webhook
def send_to_webhook(kvart, upit):
    payload = {
        'kvart': kvart,
        'upit': upit
    }
    response = requests.post(webhook_url, json=payload)
    return response.json()  # assuming webhook returns a JSON response

# Funkcija za komunikaciju s ChatGPT
def chat_with_gpt(question):
    payload = {'question': question}
    response = requests.post(chatgpt_api_url, json=payload)
    return response.json().get('answer', 'No answer from ChatGPT')

# Streamlit Layout
st.title('Dobrodošli na Interaktivnu Aplikaciju')
st.write('Odaberite splitski kvart i postavite upit.')

# Popis kvartova prema vašem popisu
kvartovi = [
    'Bačvice', 'Blatine-Škrape', 'Bol', 'Brda', 'Grad', 'Gripe', 'Kman', 'Kocunar',
    'Lokve', 'Lovret', 'Lučac-Manuš', 'Mejaši', 'Meje', 'Mertojak', 'Neslanovac', 
    'Plokite', 'Pujanke', 'Ravne njive', 'Sirobuja', 'Spinut', 'Split 3', 'Sućidar', 
    'Šine', 'Trstenik', 'Varoš', 'Visoka', 'Žnjan-Pazdigrad'
]

# Odabir kvarta
kvart = st.selectbox('Odaberite kvart:', kvartovi)

# Unos upita
upit = st.text_area('Unesite svoj upit:', '')

# Slanje podataka na webhook kad korisnik klikne
if st.button('Pošaljite'):
    if upit:  # Provjerava ako je upit popunjen
        webhook_response = send_to_webhook(kvart, upit)
        st.write(f'Webhook odgovor: {webhook_response}')
        
        # ChatGPT odgovara na postavljeni upit
        chatgpt_response = chat_with_gpt(upit)
        st.write(f'ChatGPT odgovor: {chatgpt_response}')
    else:
        st.error('Molimo unesite upit prije slanja.')

# Polje za dodatna pitanja ChatGPT-u
additional_question = st.text_area('Pitajte ChatGPT bilo što:', '')

if additional_question:
    if st.button('Postavite ChatGPT pitanje'):
        chatgpt_answer = chat_with_gpt(additional_question)
        st.write(f'ChatGPT odgovor: {chatgpt_answer}')
        st.text_area('Upit', additional_question, key="copy_question", disabled=True)  # Copy option

# Dodavanje natuknica za savršen upit za pretraživanje prostornog plana kvarta
st.subheader('Savjeti za postavljanje savršenog upita:')
st.write("""
Da biste dobili najprecizniji odgovor vezano uz prostorni plan kvarta, slijedite ove smjernice:

- **Specifičnost**: Budite precizni u svom upitu. Na primjer, umjesto "Koje su zgrade dozvoljene?", pitajte "Koje visine zgrade su dozvoljene u kvartu [ime kvarta]?"
- **Lokacija**: Ako postavljate pitanje o određenom dijelu kvarta, navedite specifičnu ulicu ili područje unutar kvarta. Na primjer, "Koje su namjene zemljišta na ulici [ime ulice]?"
- **Vrsta građevinskih dozvola**: Pitajte specifično o građevinskim dozvolama, kao što su "Koje vrste objekata mogu biti izgrađene u [ime kvarta]?"
- **Dostupni planovi**: Ako tražite određeni plan, pitajte: "Je li dostupna detaljna prostorna regulacija za [ime kvarta]?" ili "Kako mogu pristupiti informacijama o prostornom planu za [ime kvarta]?"
- **Datumi i promjene**: Ako vas zanima hoće li biti promjena, pitajte: "Hoće li biti promjena u prostornom planu kvarta [ime kvarta] u sljedećih 5 godina?"
""")
