from experta import *
import json
import os

# Cargar datos de laptops desde archivo JSON
with open("data/laptops.json", "r", encoding="utf-8") as f:
    laptops = json.load(f)

class UserInput(Fact):
    """Hechos ingresados por el usuario"""
    uso = Field(str)
    presupuesto = Field(int)
    marca = Field(str)
    pantalla = Field(float)
    sistema_operativo = Field(str)
    peso_maximo = Field(float)
    ram_min = Field(str)
    gpu_req = Field(str)

class LaptopRecommender(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.resultados = []

    @Rule(UserInput(uso=MATCH.uso, presupuesto=MATCH.presupuesto, marca=MATCH.marca,
                    pantalla=MATCH.pantalla, sistema_operativo=MATCH.sistema_operativo,
                    peso_maximo=MATCH.peso_maximo, ram_min=MATCH.ram_min, gpu_req=MATCH.gpu_req))
    def recomendar_laptops(self, uso, presupuesto, marca, pantalla, sistema_operativo, peso_maximo,ram_min,gpu_req):
        for l in laptops:
            # Filtrar por uso que se le dará al equipo
            if uso not in l["uso_ideal"]:
                continue
            # Filtrar por presupuesto disponible
            if l["precio"] > presupuesto:
                continue
            # Filtrar por marca de preferencia
            if marca and marca.lower() != l["marca"].lower():
                continue
            # Filtrar por tamaño de la pantalla
            if float(l["pantalla"]) < pantalla:
                continue
            # Filtrar por Sistema operativo preferido
            if sistema_operativo != "Cualquiera" and sistema_operativo.lower() != l["sistema_operativo"].lower():
                continue
            # Filtrar por peso máximo del equipo
            if float(l["peso"].replace("kg", "")) > peso_maximo:
                continue
            # Filtrar por RAM mínima
            if int(l["ram"].replace("GB", "")) < int(ram_min.replace("GB", "")):
                continue
            # Filtrar por GPU requerida
            if gpu_req and gpu_req.lower() not in l["gpu"].lower():
                continue
            self.resultados.append(l)
