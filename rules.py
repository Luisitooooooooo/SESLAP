from experta import *
import json
import os

# Cargar datos de laptops desde archivo JSON
with open("data/laptops.json", "r", encoding="utf-8") as f:
    laptops = json.load(f)

class UserInput(Fact):
    uso = Field(str)
    presupuesto = Field(int)
    marca = Field(str)
    pantalla = Field(float)
    sistema_operativo = Field(str)
    peso_maximo = Field(float)
    ram_min = Field(str)
    gpu_req = Field(str)
    resolucion = Field(str, default="")
    almacenamiento_primario = Field(str, default="")
    almacenamiento_secundario = Field(str, default="")



class LaptopRecommender(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.resultados = []

    @Rule(UserInput(uso=MATCH.uso, presupuesto=MATCH.presupuesto, marca=MATCH.marca,
                pantalla=MATCH.pantalla, sistema_operativo=MATCH.sistema_operativo,
                peso_maximo=MATCH.peso_maximo, ram_min=MATCH.ram_min, gpu_req=MATCH.gpu_req,
                resolucion=MATCH.resolucion, almacenamiento_primario=MATCH.almacenamiento_primario,
                almacenamiento_secundario=MATCH.almacenamiento_secundario))
    def recomendar_laptops(self, uso, presupuesto, marca, pantalla, sistema_operativo,
                       peso_maximo, ram_min, gpu_req, resolucion,
                       almacenamiento_primario, almacenamiento_secundario):
        for l in laptops:
            if uso not in l["uso_ideal"]:
                continue
            if l["precio"] > presupuesto:
                continue
            if marca != "Cualquiera" and marca.lower() != l["marca"].lower():
                continue
            if float(l["pantalla"]) < pantalla:
                continue
            if sistema_operativo != "Cualquiera" and sistema_operativo.lower() != l["sistema_operativo"].lower():
                continue
            peso_valor = float(str(l["peso"]).replace("kg", "").strip())
            if peso_valor > peso_maximo:
                continue
            if int(l["ram"].replace("GB", "")) < int(ram_min.replace("GB", "")):
                continue
            if gpu_req and gpu_req.lower() not in l["gpu"].lower():
                continue
            if resolucion and resolucion.lower() != l.get("resolucion", "").lower():
                continue
            if almacenamiento_primario and almacenamiento_primario.lower() not in l.get("almacenamiento_primario", "").lower():
                continue
            if almacenamiento_secundario and almacenamiento_secundario.lower() not in l.get("almacenamiento_secundario", "").lower():
                continue
            self.resultados.append(l)

    
