import glob
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
import time
import os
import threading
import pyttsx3
from VALID import OKI


nums = {'cero':0,'uno':1,'dos':2,'tres':3,'cuatro':4,'cinco':5,'seis':6,'siete':7,'ocho':8,'nueve':9}
#C:\Users\Antonio\Documents\videos\audios

def async_playback(filename):
    data, fs = sf.read(filename)
    sd.play(data,fs)
    return data, fs

def listening():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        text = r.recognize_google(audio,language='es-ES')
        print(text)
        return text
            
def select_audio():
    while True:
        op = listening()
        if op == "lista":
            print("\n********************LISTA DE AUDIOS********************")
            for elem,tema in enumerate(lista_temas):
                print(elem,tema)
            print("********************************************************\n")
            current = "DIGA EN VOZ ALTA EL NÚMERO CORRESPONDIENTE AL AUDIO DESEADO"
            texto = "DIGA EN VOZ ALTA EL NÚMERO CORRESPONDIENTE AL AUDIO DESEADO"
            speaker(texto,1)
            numero = listening()
            if numero in nums:
                eleccion = nums[numero]
            else:
                eleccion = numero
            
            print(type(eleccion))
            try:
                tema = int(eleccion)
                assert tema in range(len(lista_temas))
                audio_selec = lista_temas[tema]
                print("AUDIO SELECCIONADO: {}".format(audio_selec))
                async_playback(audio_selec)
            except Exception as e:
                print(str(e))
                speaker("NO SE PUDO PROCESAR LA SOLICITUD",1)
                
        elif op == 'parar':
            sd.stop()
            print('STOPPED')
            speaker("audio interrumpido",0)
        elif op == 'fin':
            sd.stop()
            speaker("programa finalizado",0)
            break

def speaker(content,v):
    engine.say(content)
    if v == 1:
        print(content)
    engine.runAndWait()
    engine.stop()

engine = pyttsx3.init()
print("HOLA")
speaker("antes de empezar introduzca ruta al directorio",0)
while True:
    direc = input("Introduce directorio: ")
    try:
        os.chdir(direc)
        break
    except:
        pass
    
os.chdir(direc)
print(os.getcwd())
lista_temas = []
for i in glob.glob("*.wav"):
    lista_temas.append(i)

select_audio()
