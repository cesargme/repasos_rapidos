from flask import Flask, render_template, request, redirect, session
import random
import csv

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

preguntas = {}
respuestas_correctas = []

def cargar_preguntas():
    global preguntas, respuestas_correctas
    preguntas = {}
    respuestas_correctas = []
    with open("preguntas.csv", 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                continue
            pregunta = row[0]
            correcta = row[1]
            opciones = [opcion for opcion in row[1:] if opcion]
            preguntas[pregunta] = opciones
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

    pregunta, opciones = random.choice(list(preguntas.items()))
    random.shuffle(opciones)
    return render_template('pregunta.html', pregunta=pregunta, opciones=opciones, contador=session['contador'], intentos=session['intentos'])

@app.route('/verificar', methods=['POST'])
def verificar():
    pregunta = request.form['pregunta']
    respuesta_elegida = request.form['opcion']

    if (pregunta, respuesta_elegida) in respuestas_correctas:
        session['contador'] += 1

    return redirect('/pregunta')

if __name__ == '__main__':
    cargar_preguntas()
    app.run(debug=True)
