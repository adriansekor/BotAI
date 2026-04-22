import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from config import DOCS_DIR

DB_DIR = "chroma_db"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_db = Chroma(
    collection_name="peluqueria_docs",
    embedding_function=embeddings,
    persist_directory=DB_DIR
)

def indexar_documentos_locales():
    """Lee la carpeta documentos/ y los mete en la BDD Vectorial."""
    textos = []
    if not os.path.exists(DOCS_DIR): return

    for archivo in os.listdir(DOCS_DIR):
        ruta = os.path.join(DOCS_DIR, archivo)
        if archivo.endswith(".pdf"):
            pdf = PdfReader(ruta)
            for page in pdf.pages:
                texto = page.extract_text()
                if texto: textos.append(texto)
        elif archivo.endswith(".txt") or archivo.endswith(".md"):
            with open(ruta, "r", encoding="utf-8") as f:
                textos.append(f.read())

    if textos:
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        docs = splitter.create_documents(textos)
        vector_db.add_documents(docs)

def buscar_contexto(pregunta, k=3):
    docs = vector_db.similarity_search(pregunta, k=k)
    return "\n\n".join([doc.page_content for doc in docs])