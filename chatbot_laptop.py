import streamlit as st
from experta import *
from rules import LaptopRecommender, UserInput
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Chatbot de Laptops")

st.title("SESLAP: Sistema Experto para Selección de Laptops")

# Inicializar estados
if "step" not in st.session_state:
    st.session_state.step = 0
if "respuestas" not in st.session_state:
    st.session_state.respuestas = {}
if "chat" not in st.session_state:
    st.session_state.chat = []
if "mostrar_mas" not in st.session_state:
    st.session_state.mostrar_mas = 5
if "resultados" not in st.session_state:
    st.session_state.resultados = []
if "resultados_mostrados" not in st.session_state:
    st.session_state.resultados_mostrados = False

if st.button("Reiniciar"):
    st.session_state.step = 0
    st.session_state.respuestas = {}
    st.session_state.chat = []
    st.session_state.mostrar_mas = 5
    st.session_state.resultados = []
    st.session_state.resultados_mostrados = False
    st.rerun()

preguntas = [
    ("uso", "¿Para qué usarás la laptop? (ej: oficina, videojuegos, edición de video...)"),
    ("presupuesto", "¿Cuál es tu presupuesto máximo en MXN?"),
    ("marca", "¿Marca preferida? (ej: HP, Asus, Lenovo, Infinix, Acer, Lg, msi, honor, gigabyte, dell)"),
    ("pantalla", "¿Tamaño mínimo de pantalla en pulgadas? (ej: 15.6)"),
    ("sistema_operativo", "¿Sistema operativo? (Windows, macOS, Linux)"),
    ("peso_maximo", "¿Peso máximo del equipo (kg)? (ej: 5.0)"),
    ("ram_min", "¿RAM mínima? (ej: 8 GB, 16 GB)"),
    ("gpu_req", "¿GPU/Tarjeta gráfica deseada? (opcional: En caso de no querer agregar una respuesta responder con '0')"),
    ("resolucion", "¿Resolución deseada? ej: 1920x1080 (opcional: En caso de no querer agregar una respuesta responder con '0')"),
    ("almacenamiento_primario", "¿Almacenamiento primario? ej: 512 SSD"),
    ("almacenamiento_secundario", "¿Almacenamiento secundario? ej: 1 TB HDD o 0 (opcional: En caso de no querer agregar una respuesta responder con '0')"),
]

opciones_validas = {
    "sistema_operativo": ["windows", "macos", "linux"],
    "marca": ["hp","asus","lenovo","infinix","acer","avita","axl","chuwi","dell","fujitsu","gigabyte","honor","iball","jio","lg","microsoft","msi","primebook","realme","samsung","tecno","ultimus","walker","wings","zebronics"],
    "ram_min": ["4", "8", "16", "32"],
    "uso": ["oficina", "videojuegos", "edición de video", "escuela", "portabilidad"]
}

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if st.session_state.step < len(preguntas):
    clave, pregunta = preguntas[st.session_state.step]
    with st.chat_message("assistant"):
        st.markdown(pregunta)

    user_input = st.chat_input("Tu respuesta...")

    if user_input is not None:
        entrada = user_input.strip()
        if entrada.lower() in ["ninguno", "no", "0"]:
            entrada = ""

        # Validar si es una pregunta con opciones fijas
        if clave in opciones_validas:
            if entrada.lower() in opciones_validas[clave]:
                st.session_state.chat.append({"role": "assistant", "content": pregunta})
                st.session_state.chat.append({"role": "user", "content": user_input})
                st.session_state.respuestas[clave] = entrada
                st.session_state.step += 1
                st.rerun()
            else:
                st.chat_message("assistant").markdown(
                    f"⚠️ Opción no válida. Opciones válidas: {', '.join(opciones_validas[clave])}"
                )
        else:
            # Sin validación: continuar
            st.session_state.chat.append({"role": "assistant", "content": pregunta})
            st.session_state.chat.append({"role": "user", "content": user_input})
            st.session_state.respuestas[clave] = entrada
            st.session_state.step += 1
            st.rerun()

elif st.session_state.step == len(preguntas) and not st.session_state.resultados_mostrados:
    with st.chat_message("assistant"):
        st.markdown("Procesando tus respuestas...")

    r = st.session_state.respuestas

    try:
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
            resolucion=r.get("resolucion", ""),
            almacenamiento_primario=r.get("almacenamiento_primario", ""),
            almacenamiento_secundario=r.get("almacenamiento_secundario", "")
        ))
        engine.run()
        resultados = engine.resultados

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

# Mostrar resultados
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

    if st.session_state.mostrar_mas < len(st.session_state.resultados):
        if st.button("Mostrar más resultados"):
            st.session_state.mostrar_mas += 5
            st.rerun()

    df = pd.DataFrame(st.session_state.resultados)
    df["Precio"] = df["precio"]
    df["Modelo"] = df["marca"] + " " + df["modelo"]
    st.subheader("Comparación de precios")
    fig, ax = plt.subplots()
    df.head(15).plot(kind="barh", y="Precio", x="Modelo", ax=ax, legend=False)
    st.pyplot(fig)
