import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from rules import LaptopRecommender, UserInput
from experta import *

#Inicializar estado
if "resultados" not in st.session_state:
    st.session_state.resultados = []
if "mostrar_todos" not in st.session_state:
    st.session_state.mostrar_todos = False

# Título
st.title("🤖 Asistente Experto en Laptops")

st.write("Completa el siguiente formulario para obtener recomendaciones sobre que laptop deberías comprar:")

# Formulario tipo chat
with st.form("formulario"):
    uso = st.selectbox("¿Para qué usarás la laptop?", ["oficina", "videojuegos", "edición de video", "escuela", "portabilidad"])
    presupuesto = st.number_input("¿Cuál es tu presupuesto máximo (MXN)?", min_value=1000, step=100)
    marca = st.selectbox("Marca preferida (opcional)", ["Cualquiera", "Acer", "Apple", "Asus", "Avita", "Axl", "Chuwi", "Dell", "Fujitsu", 
                                                        "Gigabyte", "Honor", "Hp", "Iball", "Infinix", "Jio", "Lenovo", "Lg", 
                                                        "Microsoft", "Msi", "Primebook", "Realme", "Samsung", "Tecno", "Ultimus", 
                                                        "Walker", "Wings", "Zebronics"]).capitalize()
    pantalla = st.number_input("Tamaño mínimo de pantalla (pulgadas)", min_value=10.0, max_value=18.0, step=0.1)
    sistema = st.selectbox("Sistema operativo preferido", ["Cualquiera", "Windows", "macOS", "Linux"])
    peso = st.number_input("Peso máximo (kg)", min_value=1.5, max_value=5.0, step=0.1)
    ram_min = st.selectbox("Memoria RAM mínima", ["4 GB", "8 GB", "16 GB", "32 GB"])
    gpu_req = st.text_input("¿Qué GPU o Tarjeta gráfica prefieres? (opcional)")
    resolucion = st.text_input("Resolución de pantalla preferida (opcional, ej. 1920x1080)")
    almacenamiento_primario = st.text_input("Almacenamiento primario requerido (opcional, ej. 512 SSD)")
    #almacenamiento_secundario = st.text_input("Almacenamiento secundario requerido (opcional, ej. 1 TB HDD o '0' si no aplica)")

    submitted = st.form_submit_button("Buscar laptops")
if st.button("🔄 Reiniciar búsqueda"):
    st.rerun()

#Proceso de busqueda
if submitted:
    engine = LaptopRecommender()
    engine.reset()
    engine.declare(UserInput(
        uso=uso,
        presupuesto=presupuesto,
        marca=marca,
        pantalla=pantalla,
        sistema_operativo=sistema,
        peso_maximo=peso,
        ram_min=ram_min,
        gpu_req=gpu_req,
        resolucion=resolucion,
        almacenamiento_primario=almacenamiento_primario,
       #almacenamiento_secundario=almacenamiento_secundario
    ))


    with st.spinner("🔎 Buscando laptops que se ajusten a tus necesidades..."):
        engine.run()
        resultados = engine.resultados
        st.session_state.resultados = engine.resultados
        st.session_state.mostrar_todos = False

    #Mostrar error en caso de no haber resultados
    if not st.session_state.resultados:
        st.error("❌ No se encontraron laptops que cumplan todos los criterios.")

if st.session_state.resultados:
    resultados = st.session_state.resultados
    mostrar = resultados if st.session_state.mostrar_todos else resultados[:20]

    if not st.session_state.mostrar_todos and len(resultados) > 20:
        st.info(f"Mostrando 20 de {len(resultados)} resultados.")

    for l in mostrar:    
        st.markdown(f"""
        **🖥️ {l['marca']} {l['modelo']}** - ${l['precio']}MXN  
        - 💾 RAM: {l['ram']}  
        - 🧠 CPU: {l['procesador']}  
        - 🎮 GPU: {l['gpu']}  
        - 🖼️ Pantalla: {l['pantalla']}''
        - 📊 Resolucion: {l['resolucion']}
        - ⚖️ Peso: {l['peso']}  
        - 🧑‍💻 SO: {l['sistema_operativo']}
        - 💾 Almacenamiento Primario: {l['almacenamiento_primario']}
        ---
        """)
        
    if not st.session_state.mostrar_todos and len(st.session_state.resultados) > 20:
        if st.button("🔽 Ver más resultados"):
            st.session_state.mostrar_todos = True
            st.rerun()

# VISUALIZACIÓN SOLO SI HAY RESULTADOS
# Crear DataFrame
if st.session_state.resultados:
    df = pd.DataFrame(st.session_state.resultados)
    df["Precio"] = df["precio"]
    df["Modelo"] = df["marca"] + " " + df["modelo"]
    df = df.sort_values(by="Precio", ascending=True).head(10)

    st.subheader("📊 Comparación de precios")
    fig, ax = plt.subplots()
    df.plot(kind="barh", y="Precio", x="Modelo", ax=ax, legend=False)
    st.pyplot(fig)


