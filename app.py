import streamlit as st
import google.generativeai as genai
import datetime
import time
from config import GOOGLE_API_KEY, SERVICIOS_PATH
from calendar_handler import leer_proximas_citas, crear_cita
from rag_db import buscar_contexto, indexar_documentos_locales
from prompts import obtener_system_prompt

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Paco's Barber Shop", page_icon="✂️", layout="centered")

def local_css(file_name):
    try:
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("style.css")

# --- 2. CABECERA VISUAL ---
st.title("💈 Perruqueria Paco ✂️")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Cambio: use_container_width por width='stretch' (evita warnings)
    st.image("img/logo.png", width=300)
st.markdown("<p style='text-align: center; font-style: italic;'>Tallat amb estil, cuidat amb tradició.</p>", unsafe_allow_html=True)

# CONFIGURACIÓN IA
genai.configure(api_key=GOOGLE_API_KEY)

# Inicialización BDD
if "db_inicializada" not in st.session_state:
    with st.spinner("Cregant base de coneixement..."):
        indexar_documentos_locales()
    st.session_state.db_inicializada = True

# LECTURA DE SERVICIOS
try:
    with open(SERVICIOS_PATH, "r", encoding="utf-8") as f:
        contingut_txt = f.read()
except FileNotFoundError:
    contingut_txt = "Tall Cavaller 15€, Senyora 22€."

# MEMORIA CHAT
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hola! Soc en Paco, el teu barber virtual. En què et puc ajudar avui?"}
    ]

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. BOTONES DE ACCESO RÁPIDO ---
if st.session_state.messages[-1]["role"] == "assistant":
    st.write("Triar una opció ràpida:")
    c1, c2, c3 = st.columns(3)
    if c1.button("💰 Veure preus"):
        st.session_state.messages.append({"role": "user", "content": "Quins preus teniu?"})
        st.rerun()
    if c2.button("📅 Demanar cita"):
        st.session_state.messages.append({"role": "user", "content": "Vull demanar una cita"})
        st.rerun()
    if c3.button("📍 On sou?"):
        st.session_state.messages.append({"role": "user", "content": "On està la barberia?"})
        st.rerun()

st.markdown("---")

# --- 4. LÓGICA DE PROCESAMIENTO ---
prompt = st.chat_input("Escriu la teva consulta...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Preparamos la respuesta
    avui = datetime.datetime.now().strftime("%A, %d de %B de %Y, %H:%M")

    with st.spinner("En Paco està pensant..."):
        try:
            info_calendari = leer_proximas_citas()
            contexto_rag = buscar_contexto(prompt)

            system_prompt = obtener_system_prompt(
                contexto_rag=contexto_rag,
                info_calendari=info_calendari,
                contingut_txt=contingut_txt,
                avui=avui
            )

            # Reconstrucción del historial para Gemini
            history_gemini = []
            for m in st.session_state.messages[:-1]:
                role = "user" if m["role"] == "user" else "model"
                history_gemini.append({"role": role, "parts": [m["content"]]})

            model = genai.GenerativeModel(
                model_name='gemini-3-flash-preview', # Nombre corregido sin 'models/'
                tools=[crear_cita],
                system_instruction=system_prompt
            )

            chat = model.start_chat(history=history_gemini, enable_automatic_function_calling=True)
            response = chat.send_message(prompt)

            resposta_text = response.text

            # --- RESPUESTA CON EFECTO STREAMING ---
            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_response = ""
                for chunk in resposta_text.split(" "):
                    full_response += chunk + " "
                    time.sleep(0.04)
                    placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": resposta_text})
            st.rerun()

        except Exception as e:
            st.error(f"Error detallat: {e}") # ESTO NOS DIRÁ EL FALLO REAL
            st.session_state.messages.append({"role": "assistant", "content": "Perdona, he tingut un error tècnic."})