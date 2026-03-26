import streamlit as st
import google.generativeai as genai
import os
import datetime
from pathlib import Path
from calendar_handler import leer_proximas_citas, crear_cita

# 1. CONFIGURACIÓ DE L'API
GOOGLE_API_KEY = "INSERTAR AQUI LA API" 
genai.configure(api_key=GOOGLE_API_KEY)

# 2. CONFIGURACIÓ DEL MODEL (Amb el teu model triat)
model = genai.GenerativeModel(
    model_name='models/gemini-3-flash-preview',
    tools=[crear_cita]
)

# 3. INTERFÍCIE STREAMLIT
st.set_page_config(page_title="BotAI: Perruqueria Paco", page_icon="✂️")
st.title("✂️ BotAI: Assistent Perruqueria Paco")
st.write("Benvingut! Soc en Paco, com et puc ajudar avui?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. ENTRADA DE L'USUARI
if prompt := st.chat_input("Escriu la teva consulta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Lectura de serveis
    ruta_fitxer = Path(__file__).parent / "servicios.txt"
    try:
        with open(ruta_fitxer, "r", encoding="utf-8") as f:
            contingut_txt = f.read()
    except FileNotFoundError:
        contingut_txt = "Adreça: Carrer Falsa 123. Tall Cavaller 15€, Senyora 22€."

    # Context temporal
    avui = datetime.datetime.now().strftime("%A, %d de %B de %Y, %H:%M")
    
    with st.spinner("En Paco està mirant l'agenda..."):
        info_calendari = leer_proximas_citas()

    # Prompt de sistema
    prompt_complet = f"""
    Ets en Paco, amable i professional. Parles català.
    DATA ACTUAL: {avui}.
    SERVEIS: {contingut_txt}
    AGENDA: {info_calendari}
    
    INSTRUCCIONS:
    1. Per reservar, CRIDA a la funció 'crear_cita'.
    2. Usa el format ISO (YYYY-MM-DDTHH:MM:SS) per a la data.
    3. Si ja està ocupat, proposa una alternativa.
    """
    
    try:
        chat = model.start_chat(enable_automatic_function_calling=True)
        with st.spinner("En Paco està gestionant la teva petició..."):
            response = chat.send_message(f"{prompt_complet}\n\nClient: {prompt}")
            try:
                resposta_text = response.text
            except (ValueError, IndexError):
                resposta_text = "Fet! Ja t'he anotat la reserva al calendari. Ens veiem! ✂️"

    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        resposta_text = "Em sap greu, hi ha un error amb l'agenda. Me'l pots repetir?"

    with st.chat_message("assistant"):
        st.markdown(resposta_text)
    st.session_state.messages.append({"role": "assistant", "content": resposta_text})