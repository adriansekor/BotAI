pasos a seguir:

Crea un entorn virtual (Recomanat): Això evita que les llibreries del projecte xoquin amb altres.
python -m venv venv

Activa'l (Windows):
venv\Scripts\activate

Dependències: Instal·lació automàtica mitjançant el fitxer de requeriments:
pip install -r requirements.txt

Execució: Llançament de l'aplicació:
streamlit run app.py