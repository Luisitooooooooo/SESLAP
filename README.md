# SESLAP
 Sistema Experto Seleccionador de laptops

INSTRUCCIONES PARA EJECUTAR EL PROYECTO: Chatbot Experto en Laptops (Streamlit)

REQUISITOS
- Python 3.9 o superior
- Entorno virtual creado (venv)
- Proyecto con los archivos: chatbot_app_chat.py, rules.py, y data/laptops.json

PASOS PARA INICIAR EL PROYECTO

1. Activa tu entorno virtual (venv)
   - En Windows:
     venv\Scripts\activate
   - En macOS/Linux:
     source venv/bin/activate

2. Instala las dependencias necesarias:
   pip install -r requirements.txt

   Si no tienes requirements.txt, puedes instalar manualmente:
   pip install streamlit experta matplotlib pandas

3.  Ejecuta la aplicación:
   streamlit run chatbot_app_chat.py
