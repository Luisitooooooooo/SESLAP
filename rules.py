from experta import *
import json

# Carga los datos del archivo JSON una sola vez
with open("data/laptops.json", encoding="utf-8") as f:
    laptops = json.load(f)

class UserInput(Fact):
    """Hecho con la información del usuario."""
    pass

class LaptopRecommender(KnowledgeEngine):
    @Rule(UserInput(uso=MATCH.uso, presupuesto=MATCH.presupuesto, marca=MATCH.marca,
                pantalla=MATCH.pantalla, sistema_operativo=MATCH.sistema_operativo,
                peso_maximo=MATCH.peso_maximo))
    
    def recomendar_laptops(self, uso, presupuesto, marca, pantalla, sistema_operativo, peso_maximo):
        print(f"\n🔍 Buscando laptops para '{uso}' con presupuesto hasta ${presupuesto}...\n")

        resultados = []
        for l in laptops:
            if uso not in l["uso_ideal"]:
                continue
            if l["precio"] > presupuesto:
                continue
            if marca and marca.lower() != l["marca"].lower():
                continue
            if float(l["pantalla"]) < pantalla:
                continue
            if sistema_operativo != "Cualquiera" and sistema_operativo.lower() != l["sistema_operativo"].lower():
                continue
            if float(l["peso"].replace("kg", "")) > peso_maximo:
                continue
        resultados.append(l)

        if resultados:
            print("✅ Laptops recomendadas:\n")
            for l in resultados:
                print(f"🖥️  {l['marca']} {l['modelo']} - ${l['precio']}")
                print(f"    RAM: {l['ram']} | CPU: {l['procesador']} | GPU: {l['gpu']}")
                print(f"    Pantalla: {l['pantalla']}'' | Peso: {l['peso']} | SO: {l['sistema_operativo']}\n")
        else:
            print("❌ No se encontraron laptops que coincidan con todos los criterios.")
