import glob
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
#import time
import os
import threading
import pyttsx3
from VALID import OKI

list_inn = False
nums = {'cero':0,'uno':1,'dos':2,'tres':3,'cuatro':4,'cinco':5,'seis':6,'siete':7,'ocho':8,'nueve':9}
#C:\Users\Antonio\Documents\videos\audios

def async_playback(filename):
    global list_inn
    data, fs = sf.read(filename)
    sd.play(data,fs)
    list_inn = False
    return data, fs

def listening():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        r.adjust_for_ambient_noise(source)
        r.energy_threshold=10000

        audio = r.listen(source)
        try:
            text = r.recognize_google(audio,language='es-ES')
            print("TEXTO: ",text)
            if list_inn == True:
                if text in nums or text.isdigit():
                    return text
            else:
                return text
        except:
            print("Sin entrada")
            pass
            
def select_audio():
    while True:
        global list_inn
        op = listening()
        if op == "lista":
            list_inn = True
            while True:
                print("\n********************LISTA DE AUDIOS********************")
                for elem,tema in enumerate(lista_temas):
                    print(elem,tema)
                print("********************************************************\n")
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
                    break
                except Exception as e:
                    print(str(e))
                    list_inn = False
                    speaker("NO SE PUDO PROCESAR LA SOLICITUD",1)
                
        elif op == 'para':
            list_inn = False
            sd.stop()
            print('STOPPED')
            speaker("audio interrumpido",0)
        elif op == 'fin':
            sd.stop()
            speaker("programa finalizado",0)
            break
        
def correct_dir():
    while True:
        direc = input("Introduce directorio: ")
        try:
            os.chdir(direc)
            break
        except:
            pass
    

def speaker(content,v):
    engine.say(content)
    if v == 1:
        print(content)
    engine.runAndWait()
    engine.stop()

engine = pyttsx3.init()
print("HOLA")
speaker("antes de empezar introduzca ruta al directorio",0)
correct_dir()

print(os.getcwd())
lista_temas = []
for i in glob.glob("*.wav"):
    lista_temas.append(i)

select_audio()

