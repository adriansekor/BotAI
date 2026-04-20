from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Carpeta donde se guarda la base vectorial, se crea sola
DB_DIR = "chroma_db"

# Embeddings gratuitos y rápidos
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Crear o cargar la base vectorial persistente
vector_db = Chroma(
    collection_name="peluqueria_docs",
    embedding_function=embeddings,
    persist_directory=DB_DIR
)

# Función que usa el chatbot para buscar contexto
def buscar_contexto(pregunta, k=3):
    docs = vector_db.similarity_search(pregunta, k=k)
    return "\n\n".join([doc.page_content for doc in docs])