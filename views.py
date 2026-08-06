from django.shortcuts import render
from .forms import PacienteForm  # <-- Asegúrate de que esta línea esté presente
from .models import CalculadoraNutricional

def index(request):
    resultado = None
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            # Obtener variables del formulario
            peso = data['peso']
            altura = data['altura']
            edad = data['edad']
            sexo = data['sexo']
            nivel = data['nivel_actividad']
            objetivo = int(data['objetivo'])
            condicion = int(data['condicion'])
            hora_cena = data['hora_cena']

            # Cálculos
            calc = CalculadoraNutricional
            tmb = calc.calcular_tmb(sexo, peso, altura, edad)
            calorias = calc.calcular_calorias(tmb, nivel, objetivo)
            agua = calc.calcular_agua(peso)

            if condicion in [1, 3, 6, 7]: calorias -= 300
            if condicion in [4, 5, 6, 7]: calorias -= 200

            imc = calc.calcular_imc(peso, altura)
            clas_imc = calc.clasificar_imc(imc)

            if condicion in [2, 3, 5, 7] and data.get('sistolica') and data.get('diastolica'):
                presion = calc.clasificar_presion(data['sistolica'], data['diastolica'])
            else:
                presion = "No aplica / No especificada"

            riesgo = calc.evaluar_riesgo_metabolico(imc, presion)
            actividad = calc.recomendar_actividad(objetivo, condicion)
            menu, sodio = calc.generar_menu(calorias, condicion, hora_cena)
            prot, carb, gras = calc.estimar_macros(menu)

            resultado = {
                'nombre': data['nombre'],
                'tmb': round(tmb),
                'calorias': round(calorias),
                'agua': agua,
                'imc': round(imc, 2),
                'clas_imc': clas_imc,
                'presion': presion,
                'riesgo': riesgo,
                'actividad': actividad,
                'menu': menu,
                'sodio': sodio,
                'macros': {'prot': prot, 'carb': carb, 'gras': gras}
            }
    else:
        form = PacienteForm()

    return render(request, 'puapp/index.html', {'form': form, 'resultado': resultado})