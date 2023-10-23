from flask import Flask, render_template, request, redirect, session
import random
import csv
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
preguntas_path = os.path.join(dir_path, 'preguntas.csv')



app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

preguntas = []
respuestas_correctas = []

def cargar_preguntas():
    global preguntas, respuestas_correctas
    preguntas = []
    respuestas_correctas = []
    with open(preguntas_path, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                continue  # Salta la primera fila si es un encabezado
            pregunta = row[0]
            correcta = row[1]
            opciones = [opcion for opcion in row[1:] if opcion]
            preguntas.append({'pregunta': pregunta, 'opciones': opciones})
            respuestas_correctas.append((pregunta, correcta))

@app.route('/', methods=['GET', 'POST'])
def inicio():
    session['contador'] = 0
    session['intentos'] = 0
    session['N'] = 10
    return redirect('/pregunta')

@app.route('/pregunta', methods=['GET', 'POST'])
def pregunta():
    session['intentos'] += 1
    if session['intentos'] > session['N']:
        return render_template('resultado.html', contador=session['contador'], N=session['N'])

    pregunta_dict = random.choice(preguntas)
    pregunta = pregunta_dict['pregunta']
    opciones = pregunta_dict['opciones']
    random.shuffle(opciones)
    session['pregunta_actual'] = pregunta
    session['opciones_actuales'] = opciones
    return render_template('pregunta.html', pregunta=pregunta, opciones=opciones, contador=session['contador'], intentos=session['intentos'])

@app.route('/verificar', methods=['POST'])
def verificar():
    pregunta = session.get('pregunta_actual')
    opciones = session.get('opciones_actuales')
    respuesta_elegida = request.form['opcion']

    if (pregunta, respuesta_elegida) in respuestas_correctas:
        session['contador'] += 1
        return render_template('verificar.html', correcto=True, correcta=respuesta_elegida, intentos=session['intentos'], pregunta=pregunta)
    else:
        correcta = [respuesta for pregunta, respuesta in respuestas_correctas if pregunta == session['pregunta_actual']][0]
        return render_template('verificar.html', correcto=False, correcta=correcta, intentos=session['intentos'], pregunta=pregunta)

cargar_preguntas()

if __name__ == '__main__':
    app.run(port=5000, debug=True)

