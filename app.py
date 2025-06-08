from rules import LaptopRecommender, UserInput

def obtener_entrada_usuario():
    uso = input("¿Para qué usarás la laptop? (ej: oficina, edición de video, juegos): ").lower()
    presupuesto = int(input("¿Cuál es tu presupuesto máximo en USD?: "))
    marca = input("¿Tienes alguna marca preferida? (ej: Dell, Asus, Apple, etc.): ").capitalize()
    pantalla = float(input("Tamaño mínimo de pantalla en pulgadas (ej: 13.3): "))
    sistema = input("¿Qué sistema operativo prefieres? (Windows, macOS, Linux, cualquiera): ").capitalize()
    peso = float(input("¿Cuál es el peso máximo que deseas? (en kg): "))

    return {
        "uso": uso,
        "presupuesto": presupuesto,
        "marca": marca,
        "pantalla": pantalla,
        "sistema_operativo": sistema,
        "peso_maximo": peso
    }

if __name__ == "__main__":
    print("🔧 Bienvenido al recomendador de laptops.\n")
    datos_usuario = obtener_entrada_usuario()

    engine = LaptopRecommender()
    engine.reset()
    engine.declare(UserInput(**datos_usuario))
    engine.run()
