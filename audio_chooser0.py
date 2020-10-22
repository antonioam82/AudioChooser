import glob
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
    print("********************LISTA DE AUDIOS********************")
    for elem,tema in enumerate(lista_temas):
        print(elem,tema)
            
    eleccion = OKI(input("Introduce número correspondiente al audio deseado: "))
            
    print(type(eleccion))
    try:
        assert eleccion in range(len(lista_temas))
        audio_selec = lista_temas[eleccion]
        print("AUDIO SELECCIONADO: {}".format(audio_selec))
        async_playback(audio_selec)
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


direc = input("Introduce directorio: ")
os.chdir(direc)
print(os.getcwd())
lista_temas = []
for i in glob.glob("*.wav"):
    lista_temas.append(i)

select_audio()
