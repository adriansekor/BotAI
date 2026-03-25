import streamlit as st
import google.generativeai as genai
import os
from pathlib import Path

# 1. CONFIGURACIÓ DE L'API
GOOGLE_API_KEY = "AIzaSyCJO0UTAzfcgjSHxFZvECKEy0cd7O-Idkg"
genai.configure(api_key=GOOGLE_API_KEY)

# 2. CONFIGURACIÓ DEL MODEL (Versió 2026)
model = genai.GenerativeModel('models/gemini-3-flash-preview')

# 3. INTERFÍCIE STREAMLIT
st.set_page_config(page_title="BotAI: Perruqueria Paco", page_icon="✂️")
st.title("✂️ BotAI: Assistent Perruqueria Paco")
st.write("Benvingut! Soc en Paco, com et puc ajudar avui?")

# Inicialitzar l'historial del xat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar l'historial de missatges
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. ENTRADA DE L'USUARI I LÒGICA DEL BOT
if prompt := st.chat_input("Escriu la teva consulta..."):
    # Afegir el missatge de l'usuari a l'historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # LECTURA ROBUSTA DEL FITXER (Path detecta la carpeta automàticament)
    ruta_fitxer = Path(__file__).parent / "servicios.txt"
    
    try:
        with open(ruta_fitxer, "r", encoding="utf-8") as f:
            contingut_txt = f.read()
    except FileNotFoundError:
        # Roda de recanvi si el fitxer es perd: dades crítiques
        contingut_txt = "Adreça: Carrer Falsa 123. Preu tall: Cavaller 15€, Senyora 22€. Horari: 10-20h."

    # 5. GENERACIÓ DE LA RESPOSTA AMB EL PROMPT D'EN PACO
    prompt_complet = f"""
    Ets en Paco, l'amo de la Perruqueria Paco. Ets amable, directe i professional.
    
    AQUÍ TENS LA TEVA BASE DE DADES REAL:
    ---
    {contingut_txt}
    ---
    
    INSTRUCCIONS DE RESPOSTA:
    1. TOTA la informació està al text de dalt. No diguis mai que no la saps.
    2. Si et pregunten preus genèrics, dóna les opcions (ex: Cavaller 15€, Senyora 22€, Infantil 12€).
    3. Si pregunten on estàs, digues "Carrer Falsa 123".
    4. Respon sempre en l'idioma que t'ha parlat el client (Català o Castellà).
    
    Pregunta del client: {prompt}
    """
    
    try:
        # Cridar a l'IA
        with st.spinner("En Paco està buscant la info..."):
            response = model.generate_content(prompt_complet)
            resposta_text = response.text
    except Exception as e:
        resposta_text = "Em sap greu, tinc un problema tècnic. Em pots trucar al local?"

    # Mostrar i guardar la resposta
    with st.chat_message("assistant"):
        st.markdown(resposta_text)
    st.session_state.messages.append({"role": "assistant", "content": resposta_text})