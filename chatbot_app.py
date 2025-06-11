import streamlit as st
from rules import LaptopRecommender, UserInput
from experta import *

# Título
st.title("🤖 Asistente Experto en Laptops")
if st.button("🔄 Reiniciar búsqueda"):
    st.rerun()

st.write("Completa el siguiente formulario para obtener recomendaciones sobre que laptop deberías comprar:")


# Formulario tipo chat
with st.form("formulario"):
    uso = st.selectbox("¿Para qué usarás la laptop?", ["oficina", "juegos", "edición de video", "estudio", "diseño gráfico"])
    presupuesto = st.number_input("¿Cuál es tu presupuesto máximo (USD)?", min_value=100, step=50)
    marca = st.text_input("Marca preferida (opcional)").capitalize()
    pantalla = st.number_input("Tamaño mínimo de pantalla (pulgadas)", min_value=10.0, max_value=18.0, step=0.1)
    sistema = st.selectbox("Sistema operativo preferido", ["Cualquiera", "Windows", "macOS", "Linux"])
    peso = st.number_input("Peso máximo (kg)", min_value=0.5, max_value=5.0, step=0.1)
    ram_min = st.selectbox("Memoria RAM mínima", ["4 GB", "8 GB", "16 GB", "32 GB"])
    gpu_req = st.text_input("¿Qué GPU o Tarjeta gráfica prefieres? (opcional)")


    submitted = st.form_submit_button("Buscar laptops")

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
        gpu_req=gpu_req
    ))

    with st.spinner("🔎 Buscando laptops que se ajusten a tus necesidades..."):
        engine.run()
        resultados = engine.resultados

    if resultados:
        st.success(f"Se encontraron {len(resultados)} laptops recomendadas:")
        for l in resultados:
            st.markdown(f"""
            **🖥️ {l['marca']} {l['modelo']}** - ${l['precio']}  
            - 💾 RAM: {l['ram']}  
            - 🧠 CPU: {l['procesador']}  
            - 🎮 GPU: {l['gpu']}  
            - 🖼️ Pantalla: {l['pantalla']}''  
            - ⚖️ Peso: {l['peso']}  
            - 🧑‍💻 SO: {l['sistema_operativo']}  
            ---
            """)
    
        #VISUALIZACIÓN SOLO SI HAY RESULTADOS
        import pandas as pd
        import matplotlib.pyplot as plt
        # Crear DataFrame
        df = pd.DataFrame(resultados)
        df["Precio"] = df["precio"]
        df["Modelo"] = df["marca"] + " " + df["modelo"]

        # Gráfico de precios
        st.subheader("📊 Comparación de precios")
        fig, ax = plt.subplots()
        df.plot(kind="barh", y="Precio", x="Modelo", ax=ax, legend=False)
        st.pyplot(fig)

    else:
        st.error("❌ No se encontraron laptops que cumplan todos los criterios.")

