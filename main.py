from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.utils import platform
import random
import csv

import os

class PracticarInglesApp(App):

    def build(self):
        self.reiniciar()
        self.layout = BoxLayout(orientation='vertical')
        self.etiqueta = Label(text='Pregunta aparecerá aquí')
        self.layout.add_widget(self.etiqueta)
        self.opciones_layout = BoxLayout(size_hint=(1, 0.5))
        self.layout.add_widget(self.opciones_layout)
        self.contador_etiqueta = Label(text=f'Contador: {self.contador}')
        self.layout.add_widget(self.contador_etiqueta)
        self.siguiente_pregunta()

        return self.layout

    def reiniciar(self):
        self.contador = 0
        self.intentos = 0
        self.N = 10
        self.diccionario = {}
        self.respuestas_correctas = []


        if platform == 'android':
            from android.storage import app_storage_path
            storage_path = app_storage_path()
            csv_path = f"{storage_path}/preguntas.csv"
        else:
            csv_path = "preguntas.csv"


        with open(csv_path, 'r', encoding="utf-8") as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == 0:
                    continue
                pregunta = row[0]
                correcta = row[1]
                opciones = [opcion for opcion in row[1:] if opcion]  # Ignora las celdas vacías
                self.diccionario[pregunta] = opciones
                self.respuestas_correctas.append((pregunta, correcta))

    def siguiente_pregunta(self):
        self.intentos += 1
        if self.intentos > self.N:
            popup = Popup(title='Resultado',
                          content=Label(text=f'Hiciste {self.contador} correctas de {self.N} intentos. ¿Quieres continuar?'),
                          size_hint=(None, None), size=(400, 400),
                          auto_dismiss=False)

            continuar_btn = Button(text='Continuar')
            continuar_btn.bind(on_press=lambda x: [popup.dismiss(), self.reiniciar(), self.siguiente_pregunta()])
            popup.content.add_widget(continuar_btn)
            
            popup.open()
            return

        pregunta, opciones = random.choice(list(self.diccionario.items()))
        random.shuffle(opciones)
        self.etiqueta.text = pregunta
        self.opciones_layout.clear_widgets()

        for opcion in opciones:
            btn = Button(text=opcion)
            btn.bind(on_press=self.verificar_respuesta)
            self.opciones_layout.add_widget(btn)

    def verificar_respuesta(self, instancia):
        pregunta_actual = self.etiqueta.text
        respuesta_elegida = instancia.text

        if (pregunta_actual, respuesta_elegida) in self.respuestas_correctas:
            self.contador += 1
            popup = Popup(title='Correcto',
                          content=Label(text='Correcto'),
                          size_hint=(None, None), size=(200, 200))
            popup.open()
        else:
            respuesta_correcta = [respuesta for pregunta, respuesta in self.respuestas_correctas if pregunta == pregunta_actual][0]
            popup = Popup(title='Incorrecto',
                        content=Label(text=f'Incorrecto, la respuesta correcta es: [size=20]{pregunta_actual} [b]{respuesta_correcta}[/b][/size]',
                                        markup=True),
                        size_hint=(None, None), size=(300, 300))
            popup.open()
        self.contador_etiqueta.text = f'Contador: {self.contador}'
        self.siguiente_pregunta()

if __name__ == '__main__':
    PracticarInglesApp().run()
