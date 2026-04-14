import streamlit as st
import google.generativeai as genai
import os
import datetime
from pathlib import Path
from calendar_handler import leer_proximas_citas, crear_cita
<<<<<<< HEAD
from rag_db import vector_db, buscar_contexto
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

# ==============================
# CONFIGURACIÓN CARPETAS
# ==============================
DOCS_DIR = "documentos"
os.makedirs(DOCS_DIR, exist_ok=True)

# ==============================
# GUARDAR ARCHIVOS SUBIDOS
# ==============================
def guardar_archivo(file):
    ruta = os.path.join(DOCS_DIR, file.name)
    with open(ruta, "wb") as f:
        f.write(file.getbuffer())
    return ruta

# ==============================
# INDEXAR DOCUMENTOS EN CHROMA
# ==============================
def indexar_documentos():
    textos = []

    for archivo in os.listdir(DOCS_DIR):
        ruta = os.path.join(DOCS_DIR, archivo)

        if archivo.endswith(".pdf"):
            pdf = PdfReader(ruta)
            for page in pdf.pages:
                texto = page.extract_text()
                if texto:
                    textos.append(texto)

        elif archivo.endswith(".txt") or archivo.endswith(".md"):
            with open(ruta, "r", encoding="utf-8") as f:
                textos.append(f.read())

    if not textos:
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    docs = splitter.create_documents(textos)
    vector_db.add_documents(docs)
    vector_db.persist()

# ==============================
# API GEMINI
# ==============================
GOOGLE_API_KEY = "AIzaSyB_RmAFs1m2LG-7K4JVdMflyqjBT2w43rA"
genai.configure(api_key=GOOGLE_API_KEY)

# ==============================
# INTERFAZ STREAMLIT
# ==============================
st.set_page_config(page_title="BotAI: Perruqueria Paco", page_icon="✂️")
st.title("BotAI: Assistent Perruqueria Paco")

# Indexar documentos al arrancar la app
if "db_inicializada" not in st.session_state:
    indexar_documentos()
    st.session_state.db_inicializada = True

# ==============================
# SIDEBAR — SUBIR DOCUMENTOS
# ==============================
st.sidebar.title("Base de conocimiento")

uploaded_files = st.sidebar.file_uploader(
    "Sube documentos para entrenar al bot",
    type=["txt", "pdf", "md"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        guardar_archivo(file)

    with st.spinner("Indexando documentos..."):
        indexar_documentos()

    st.sidebar.success("Documentos guardados e indexados ✅")

st.write("Benvingut! Soc en Paco, com et puc ajudar avui?")

# ==============================
# MEMORIA CHAT
# ==============================
=======

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

>>>>>>> c724ab16306a0c0a0511bbf7a7535658797a1535
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

<<<<<<< HEAD
# ==============================
# INPUT USUARIO
# ==============================
if prompt := st.chat_input("Escriu la teva consulta..."):

=======
# 4. ENTRADA DE L'USUARI
if prompt := st.chat_input("Escriu la teva consulta..."):
>>>>>>> c724ab16306a0c0a0511bbf7a7535658797a1535
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

<<<<<<< HEAD
    # Leer servicios
=======
    # Lectura de serveis
>>>>>>> c724ab16306a0c0a0511bbf7a7535658797a1535
    ruta_fitxer = Path(__file__).parent / "servicios.txt"
    try:
        with open(ruta_fitxer, "r", encoding="utf-8") as f:
            contingut_txt = f.read()
    except FileNotFoundError:
<<<<<<< HEAD
        contingut_txt = "Tall Cavaller 15€, Senyora 22€."

    avui = datetime.datetime.now().strftime("%A, %d de %B de %Y, %H:%M")

    with st.spinner("Consultant agenda..."):
        info_calendari = leer_proximas_citas()

    # RAG
    try:
        contexto_rag = buscar_contexto(prompt)
    except:
        contexto_rag = ""

    # ==============================
    # SYSTEM PROMPT
    # ==============================
    system_prompt = f"""
Ets en Paco, assistent d'una perruqueria. Parles català i ets amable.

BASE DE CONEIXEMENT:
{contexto_rag}

DATA: {avui}
SERVEIS: {contingut_txt}
AGENDA: {info_calendari}

REGLES:
- Respostes curtes i naturals
- Usa la base de coneixement si existeix
- Si no saps alguna cosa, digues-ho
- Si vol reservar -> usa crear_cita
"""

    chat = genai.GenerativeModel(
        model_name='models/gemini-3-flash-preview',
        tools=[crear_cita],
        system_instruction=system_prompt
    ).start_chat(enable_automatic_function_calling=True)

    # Enviar historial SIN role (fix error)
    for msg in st.session_state.messages[:-1]:
        chat.send_message(msg["content"])

    # RESPUESTA IA
    try:
        with st.spinner("En Paco està pensant..."):
            response = chat.send_message(
                prompt,
                generation_config={"temperature": 0.4}
            )
        resposta_text = response.text or "Perfecte! ✂️"
    except:
        resposta_text = "Hi ha hagut un error, pots repetir?"

    # Mostrar respuesta
    with st.chat_message("assistant"):
        st.markdown(resposta_text)

    st.session_state.messages.append({
        "role": "assistant",
        "content": resposta_text
    })
=======
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
>>>>>>> c724ab16306a0c0a0511bbf7a7535658797a1535
