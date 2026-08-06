from django import forms

SEXO_CHOICES = [
    ('H', 'Hombre'),
    ('M', 'Mujer'),
]

OBJETIVO_CHOICES = [
    (1, 'Bajar peso'),
    (2, 'Subir peso'),
    (3, 'Mantener'),
]

CONDICION_CHOICES = [
    (0, 'Ninguna'),
    (1, 'Obesidad'),
    (2, 'Hipertensión'),
    (3, 'Ambas (Obesidad e Hipertensión)'),
    (4, 'Diabetes'),
    (5, 'Diabetes + Hipertensión'),
    (6, 'Obesidad + Diabetes'),
    (7, 'Todas las condiciones'),
]

class PacienteForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre completo", 
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Ej. Juan Pérez'})
    )
    edad = forms.IntegerField(
        label="Edad", 
        min_value=1, 
        max_value=120
    )
    peso = forms.FloatField(
        label="Peso (kg)", 
        min_value=1.0
    )
    altura = forms.FloatField(
        label="Altura (cm)", 
        min_value=1.0
    )
    sexo = forms.ChoiceField(
        label="Sexo", 
        choices=SEXO_CHOICES
    )
    nivel_actividad = forms.IntegerField(
        label="Nivel de Actividad (1 a 5)", 
        min_value=1, 
        max_value=5
    )
    objetivo = forms.ChoiceField(
        label="Objetivo", 
        choices=OBJETIVO_CHOICES
    )
    condicion = forms.ChoiceField(
        label="Condición médica", 
        choices=CONDICION_CHOICES
    )
    hora_cena = forms.IntegerField(
        label="Hora habitual de cena (0-23 hrs)", 
        min_value=0, 
        max_value=23
    )
    
    # Campos opcionales para presión arterial
    sistolica = forms.IntegerField(
        label="Presión Sistólica (Opcional)", 
        required=False
    )
    diastolica = forms.IntegerField(
        label="Presión Diastólica (Opcional)", 
        required=False
    )