import glob
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
import time
import os
from VALID import OKI

nums = {'uno':1,'dos':2,'tres':3,'cinco':5,'seis':6,'siete':7,'ocho':8,'nueve':9}

def async_playback(filename):
    data, fs = sf.read(filename)
    sd.play(data,fs)
    return data, fs

def listening():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio,language='es-ES')
            print(text)
            return text
        except:
            print("Sorry could not recognize what you said")
            
            

def select_audio():
    while True:
        op = listening()
        if op == "lista":
            for elem,tema in enumerate(lista_temas):
                print(elem,tema)
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
                
        elif op == "para":
            sd.stop()
            print('STOPPED')
        elif op == "fin":
            sd.stop()
            break


direc = input("Introduce directorio: ")
os.chdir(direc)
print(os.getcwd())
lista_temas = []
for i in glob.glob("*.wav"):
    lista_temas.append(i)

select_audio()
