import random

# Base de Alimentos
ALIMENTOS = {
    "proteina": [
        ("Pechuga pollo", 250, 80, "proteina"),
        ("Carne asada", 330, 95, "proteina"),
        ("Cecina", 320, 950, "proteina"),
        ("Cochinita", 400, 870, "proteina"),
        ("Huevos mexicanos", 250, 220, "proteina"),
    ],
    "carbohidrato": [
        ("Arroz rojo", 210, 400, "carbohidrato"),
        ("Frijoles olla", 220, 15, "carbohidrato"),
        ("Tamales", 250, 600, "carbohidrato"),
        ("Pan dulce", 300, 350, "carbohidrato"),
        ("Tortillas", 180, 15, "carbohidrato"),
    ],
    "grasa": [
        ("Aguacate", 240, 10, "grasa"),
        ("Queso Oaxaca", 180, 320, "grasa"),
        ("Chicharrón", 290, 700, "grasa"),
        ("Nueces", 200, 5, "grasa"),
    ],
    "fruta_verdura": [
        ("Ensalada verde", 70, 20, "carbohidrato"),
        ("Verduras vapor", 80, 30, "carbohidrato"),
        ("Papaya", 60, 5, "carbohidrato"),
        ("Guayaba", 90, 3, "carbohidrato"),
    ],
}

CARNES_PESADAS = ["Cochinita", "Cecina", "Chicharrón"]
ALTO_IG = ["Tamales", "Pan dulce"]
ALTO_SODIO = ["Cecina", "Cochinita", "Chicharrón"]


class CalculadoraNutricional:

    @staticmethod
    def calcular_tmb(sexo, peso, altura, edad):
        if sexo.lower() == "h":
            return (10 * peso) + (6.25 * altura) - (5 * edad) + 5
        return (10 * peso) + (6.25 * altura) - (5 * edad) - 161

    @staticmethod
    def factor_actividad(nivel):
        factores = {1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9}
        return factores.get(nivel, 1.2)

    @staticmethod
    def calcular_calorias(tmb, nivel, objetivo):
        calorias = tmb * CalculadoraNutricional.factor_actividad(nivel)
        if objetivo == 1:
            calorias -= 500
        elif objetivo == 2:
            calorias += 300
        return calorias

    @staticmethod
    def calcular_agua(peso):
        return round((peso * 35) / 1000, 2)

    @staticmethod
    def calcular_imc(peso, altura):
        return peso / ((altura / 100) ** 2)

    @staticmethod
    def clasificar_imc(imc):
        if imc < 18.5: return "Bajo peso"
        elif imc < 25: return "Normal"
        elif imc < 30: return "Sobrepeso"
        elif imc < 35: return "Obesidad grado I"
        elif imc < 40: return "Obesidad grado II"
        else: return "Obesidad grado III"

    @staticmethod
    def clasificar_presion(sis, dias):
        if sis < 120 and dias < 80: return "Normal"
        elif sis < 130 and dias < 80: return "Elevada"
        elif sis < 140 or dias < 90: return "Hipertensión etapa 1"
        else: return "Hipertensión etapa 2"

    @staticmethod
    def evaluar_riesgo_metabolico(imc, presion):
        if imc >= 30 and "Hipertensión" in presion:
            return "RIESGO CARDIOVASCULAR ALTO"
        elif imc >= 25:
            return "RIESGO MODERADO"
        return "RIESGO BAJO"

    @staticmethod
    def recomendar_actividad(objetivo, condicion):
        if condicion in [2, 3, 5, 7]:
            return "Actividad cardiovascular controlada: Caminata 30 min, Respiración diafragmática. Evitar HIIT."
        if condicion in [1, 6]:
            return "Actividad bajo impacto: Bicicleta estática, Natación ligera."
        if objetivo == 1:
            return "Cardio 4x semana + fuerza 2x semana."
        elif objetivo == 2:
            return "Fuerza 4x semana + cardio ligero."
        return "Rutina equilibrada."

    @staticmethod
    def generar_menu(calorias_obj, condicion, hora_cena):
        comidas = ["Desayuno", "Snack1", "Comida", "Snack2", "Cena"]
        kcal_por_comida = round(calorias_obj / 5)
        menu = {}
        sodio_dia = 0

        for comida in comidas:
            if comida == "Desayuno":
                grupos = ["proteina", "carbohidrato", "fruta_verdura"]
            elif comida in ["Snack1", "Snack2"]:
                grupos = ["fruta_verdura", "proteina"]
            elif comida == "Comida":
                grupos = ["proteina", "carbohidrato", "grasa", "fruta_verdura"]
            else:
                grupos = ["proteina", "fruta_verdura"]

            seleccion = []
            kcal_total = 0
            sodio_total = 0
            intentos = 0

            while kcal_total < kcal_por_comida and intentos < 50:
                grupo = random.choice(grupos)
                posibles = ALIMENTOS[grupo]

                if condicion in [4, 5, 6, 7]:
                    posibles = [a for a in posibles if a[0] not in ALTO_IG]
                if condicion in [2, 3, 5, 7]:
                    posibles = [a for a in posibles if a[0] not in ALTO_SODIO]
                if comida == "Cena" and hora_cena >= 19:
                    posibles = [a for a in posibles if a[0] not in CARNES_PESADAS and a[0] not in ALTO_IG]

                if posibles:
                    item = random.choice(posibles)
                    if kcal_total + item[1] <= kcal_por_comida + 50:
                        seleccion.append(item)
                        kcal_total += item[1]
                        sodio_total += item[2]

                intentos += 1

            sodio_dia += sodio_total
            menu[comida] = {"items": seleccion, "kcal": kcal_total, "sodio": sodio_total}

        return menu, sodio_dia

    @staticmethod
    def estimar_macros(menu):
        prot, carb, grasa = 0, 0, 0
        for comida in menu.values():
            for item in comida["items"]:
                kcal, tipo = item[1], item[3]
                if tipo == "proteina": prot += kcal * 0.3 / 4
                elif tipo == "carbohidrato": carb += kcal * 0.6 / 4
                elif tipo == "grasa": grasa += kcal * 0.7 / 9
        return round(prot, 1), round(carb, 1), round(grasa, 1)