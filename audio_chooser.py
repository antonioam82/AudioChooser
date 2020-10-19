import glob
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
import time
import os
from VALID import OKI

def async_playback(filename):
    data, fs = sf.read(filename)
    sd.play(data,fs)
    return data, fs

def select_audio():
    while True:
        for elem,tema in enumerate(lista_temas):
            print(elem,tema)
        eleccion = OKI(input("Introduzca número correspondiente a su eleccion: "))
        while int(eleccion) > (len(lista_temas)-1):
            eleccion = OKI(input("Introduzca indice válido correspondiente a su opción: "))
        assert eleccion in range(len(lista_temas))
        audio_selec = lista_temas[eleccion]
        print("AUDIO SELECCIONADO: {}".format(audio_selec))
        async_playback(audio_selec)
        op = input("Opcion: ")
        if op == "STOP":
            sd.stop()
        elif op == "END":
            sd.stop()
            break


direc = input("Introduce directorio: ")
os.chdir(direc)
print(os.getcwd())
lista_temas = []
for i in glob.glob("*.wav"):
    lista_temas.append(i)

select_audio()
