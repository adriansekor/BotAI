# ✂️ BotAI: Perruqueria Paco

Aquest projecte és un assistent virtual intel·ligent que gestiona cites mitjançant Google Calendar i respon dubtes sobre la perruqueria utilitzant una base de coneixement (RAG).

## 🚀 PASSOS PER A LA INSTAL·LACIÓ

1.CREA UN ENTORN VIRTUAL (Recomanat)
Això evita conflictes entre llibreries:
python -m venv venv

2.ACTIVA L'ENTORN VIRTUAL
- Windows:
venv\Scripts\activate
- Mac/Linux:
source venv/bin/activate

3. INSTAL·LA LES DEPENDÈNCIES
Instal·lació automàtica de totes les llibreries necessàries:
pip install -r requirements.txt

## CONFIGURACIÓ ABANS DE COMENÇAR

Abans de llançar l'aplicació, assegura't de tenir:

1. El fitxer 'config.py' amb la teva GOOGLE_API_KEY.
2. El fitxer JSON de credencials de Google a la carpeta 'credentials/'.
3. Els preus actualitzats al fitxer 'data/servicios.txt'.
4. Els documents PDF o TXT de consulta a la carpeta 'data/documentos/'.

## EXECUCIÓ DE L'APLICACIÓ

Per obrir el xat d'en Paco al navegador, executa:
streamlit run app.py

## ESTRUCTURA DELS ARXIUS
- app.py: Arxiu principal de la interfície Streamlit.
- prompts.py: Definició de la personalitat i regles de l'assistent.
- calendar_handler.py: Lògica de lectura i creació de cites a Google.
- rag_db.py: Gestió de la base de dades vectorial (ChromaDB).
- config.py: Rutes de fitxers i claus de seguretat.