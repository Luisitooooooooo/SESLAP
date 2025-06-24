import streamlit as st
from experta import *
from rules import LaptopRecommender, UserInput
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de la página de Streamlit
st.set_page_config(page_title="Chatbot de Laptops")

st.title("SESLAP: Sistema Experto para Selección de Laptops")

# --- Inicialización de variables de sesión ---
# Se usan para controlar el flujo de la conversación y almacenar respuestas/resultados
if "step" not in st.session_state:
    st.session_state.step = 0
if "respuestas" not in st.session_state:
    st.session_state.respuestas = {}
if "chat" not in st.session_state:
    st.session_state.chat = []
if "mostrar_mas" not in st.session_state:
    st.session_state.mostrar_mas = 10
if "resultados" not in st.session_state:
    st.session_state.resultados = []
if "resultados_mostrados" not in st.session_state:
    st.session_state.resultados_mostrados = False

# Botón para reiniciar la conversación y limpiar el estado
if st.button("Reiniciar"):
    st.session_state.step = 0
    st.session_state.respuestas = {}
    st.session_state.chat = []
    st.session_state.mostrar_mas = 10
    st.session_state.resultados = []
    st.session_state.resultados_mostrados = False
    st.rerun()

# --- Definición de preguntas y opciones válidas ---
preguntas = [
    ("uso", "¿Para qué usarás la laptop? (ej: oficina, videojuegos, edición de video)"),
    ("presupuesto", "¿Cuál es tu presupuesto máximo en MXN?"),
    ("marca", "¿Marca preferida? (ej: HP, Apple, Asus, Lenovo, Infinix, Acer, Lg, msi, honor, gigabyte, dell)"),
    ("pantalla", "¿Tamaño mínimo de pantalla en pulgadas? (ej: 15.6)"),
    ("sistema_operativo", "¿Sistema operativo? (Windows, macOS, Linux)"),
    ("peso_maximo", "¿Peso máximo del equipo (kg)? (ej: 5.0)"),
    ("ram_min", "¿RAM mínima? (ej: 8 GB, 16 GB)"),
    ("gpu_req", "¿GPU/Tarjeta gráfica deseada? (opcional: En caso de no querer agregar una respuesta responder con '0')"),
    ("resolucion", "¿Resolución deseada? ej: HD, FHD, 2k, 4k (opcional: En caso de no querer agregar una respuesta responder con '0')"),
    ("almacenamiento_primario", "¿Almacenamiento primario? ej: 512 SSD, 64 HDD, 1024 SDD (opcional: En caso de no querer agregar una respuesta responder con '0')"),
    ("almacenamiento_secundario", "¿Almacenamiento secundario? ej: 1 TB HDD (opcional: En caso de no querer agregar una respuesta responder con '0')"),
]

# Opciones válidas para ciertas preguntas (validación de entrada)
opciones_validas = {
    "sistema_operativo": ["windows", "macos", "linux"],
    "marca": ["hp","asus","lenovo","infinix","acer","apple","avita","axl","chuwi","dell","fujitsu","gigabyte","honor","iball",
              "jio","lg","microsoft","msi","primebook","realme","samsung","tecno","ultimus","walker","wings","zebronics"],
    "ram_min": ["4", "8", "16", "32"],
    "uso": ["oficina", "videojuegos", "edición de video", "escuela", "portabilidad"],
    "almacenamiento_primario": [ "32 HDD", "64 HDD", "64 SSD", "128 SSD", "256 SSD", "512 SSD", "1024 SSD", "2048 SSD", "0"],
    "almacenamiento_secundario": ["0", "256 SSD", "256 HDD", "512 SSD", "1024 SSD", "1 TB HDD", "2 TB HDD"    ]
}

# Diccionario para normalizar resoluciones
RESOLUCIONES_EQUIVALENTES = {
    "hd": "1366x768",
    "fhd": "1920x1080",
    "2k": "2560x1440",
    "4k": "3840x2160"
}

opcionales = ["gpu_req", "resolucion", "almacenamiento_primario", "almacenamiento_secundario"]

# --- Mostrar historial de chat ---
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Flujo principal de preguntas y respuestas ---
if st.session_state.step < len(preguntas):
    clave, pregunta = preguntas[st.session_state.step]
    with st.chat_message("assistant"):
        st.markdown(pregunta)

    user_input = st.chat_input("Tu respuesta...")

    if user_input is not None:
        entrada = user_input.strip()
        if entrada.lower() in ["ninguno", "no", "0"]:
            entrada = ""

        clave, _ = preguntas[st.session_state.step]

        # Validación de opciones fijas
        if clave in opciones_validas:
            if entrada.lower() in opciones_validas[clave] or entrada == "" or clave in opcionales:
                st.session_state.chat.append({"role": "assistant", "content": pregunta})

                # Si es opcional y está vacío, muestra "(sin respuesta)"
                respuesta_mostrada = entrada if entrada != "" else "(sin respuesta)" if clave in opcionales else ""
                st.session_state.chat.append({"role": "user", "content": respuesta_mostrada})
                
                # Guarda la entrada tal como está para procesarla luego
                st.session_state.respuestas[clave] = entrada
                st.session_state.step += 1
                st.rerun()
            else:
                st.chat_message("assistant").markdown(
                    f"⚠️ Opción no válida. Opciones válidas: {', '.join(opciones_validas[clave])}"
                )
        else:
        # Validación especial para presupuesto (debe ser entero)
            if clave == "presupuesto":
                try:
                    valor_entero = int(entrada)
                    if valor_entero <= 0:
                        raise ValueError
                    st.session_state.chat.append({"role": "assistant", "content": pregunta})
                    st.session_state.chat.append({"role": "user", "content": str(valor_entero)})
                    st.session_state.respuestas[clave] = str(valor_entero)
                    st.session_state.step += 1
                    st.rerun()
                except ValueError:
                    st.chat_message("assistant").markdown(
                        "⚠️ El presupuesto debe ser un número entero positivo. Intenta nuevamente."
                    )
            else:
                # Si no requiere validación especial, se acepta cualquier entrada
                st.session_state.chat.append({"role": "assistant", "content": pregunta})
                st.session_state.chat.append({"role": "user", "content": user_input})
                st.session_state.respuestas[clave] = entrada
                st.session_state.step += 1
                st.rerun()

# --- Procesamiento de respuestas y recomendación ---
elif st.session_state.step == len(preguntas) and not st.session_state.resultados_mostrados:
    with st.chat_message("assistant"):
        st.markdown("Procesando tus respuestas...")

    r = st.session_state.respuestas
    resolucion_usuario = r.get("resolucion", "").lower()
    resolucion_normalizada = RESOLUCIONES_EQUIVALENTES.get(resolucion_usuario, resolucion_usuario)


    try:
        # Se inicializa el motor de reglas y se le pasan los datos del usuario
        engine = LaptopRecommender()
        engine.reset()
        engine.declare(UserInput(
            uso=r.get("uso", ""),
            presupuesto=int(float(r.get("presupuesto", 0))),
            marca=r.get("marca", ""),
            pantalla=float(r.get("pantalla", 0)),
            sistema_operativo=r.get("sistema_operativo", ""),
            peso_maximo=float(r.get("peso_maximo", 0)),
            ram_min=r.get("ram_min", ""),
            gpu_req=r.get("gpu_req", ""),
            resolucion=resolucion_normalizada,
            almacenamiento_primario=r.get("almacenamiento_primario", ""),
            almacenamiento_secundario=r.get("almacenamiento_secundario", "")
        ))
        engine.run()
        resultados = engine.resultados

        # Se muestran los resultados encontrados o un mensaje si no hay coincidencias
        if resultados:
            st.session_state.resultados = resultados
            st.session_state.chat.append({
                "role": "assistant",
                "content": f"Se encontraron {len(resultados)} laptops recomendadas. Mostrando las primeras {st.session_state.mostrar_mas}."
            })
        else:
            st.session_state.chat.append({
                "role": "assistant",
                "content": "No se encontraron laptops que cumplan con tus criterios."
            })

        st.session_state.resultados_mostrados = True
        st.rerun()

    except Exception as e:
        st.chat_message("assistant").error(f"Ocurrió un error: {e}")

# --- Mostrar resultados y comparación ---
if st.session_state.resultados_mostrados and st.session_state.resultados:
    visibles = st.session_state.resultados[:st.session_state.mostrar_mas]
    for l in visibles:
        st.chat_message("assistant").markdown(f"""
**{l['marca']} {l['modelo']}** - ${l['precio']}  
- RAM: {l['ram']}  
- CPU: {l['procesador']}  
- GPU: {l['gpu']}  
- Pantalla: {l['pantalla']}''  
- Peso: {l['peso']}  
- SO: {l['sistema_operativo']}  
---
""")

    # Botón para mostrar más resultados si hay más de los visibles
    if st.session_state.mostrar_mas < len(st.session_state.resultados):
        if st.button("Mostrar más resultados"):
            st.session_state.mostrar_mas += 5
            st.rerun()

    # Visualización de comparación de precios usando matplotlib
    df = pd.DataFrame(st.session_state.resultados)
    df["Precio"] = df["precio"]
    df["Modelo"] = df["marca"] + " " + df["modelo"]
    st.subheader("Comparación de precios")
    fig, ax = plt.subplots()
    df.head(15).plot(kind="barh", y="Precio", x="Modelo", ax=ax, legend=False)
    st.pyplot(fig)
