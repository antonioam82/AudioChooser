import glob
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
import time
import os
from VALID import OKI

#C:\Users\Antonio\Documents\videos\audios

def async_playback(filename):
    data, fs = sf.read(filename)
    sd.play(data,fs)
    return data, fs

def select_theme():
    print("\n********************LISTA DE AUDIOS********************")
    for elem,tema in enumerate(lista_temas):
        print(elem,tema)
    print("********************************************************\n")

    while True:
        eleccion = OKI(input("Introduce número correspondiente al audio deseado: "))

        try:
            assert eleccion in range(len(lista_temas))
            audio_selec = lista_temas[eleccion]
            print("AUDIO SELECCIONADO: {}".format(audio_selec))
            async_playback(audio_selec)
            break
        except Exception as e:
            print(str(e))    
    
def select_audio():
    while True:
        op = input('Opcion: ')

        if op == 'list':
            select_theme()
            
        elif op == 'STOP':
            sd.stop()
            print('STOPPED')
        elif op == 'END':
            sd.stop()
            break

while True:
    direc = input("Introduce un directorio válido: ")
    try:
        os.chdir(direc)
        break
    except:
        pass
    
print(os.getcwd())
lista_temas = []
for i in glob.glob("*.wav"):
    lista_temas.append(i)

select_audio()
