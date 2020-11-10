#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
import os
import pyttsx3


nums = {'cero':0,'uno':1,'dos':2,'tres':3,'cuatro':4,'cinco':5,'seis':6,'siete':7,'ocho':8,'nueve':9,
        'diez':10,'once':11,'doce':12,'trece':13,'catorce':14,'quince':15}

def async_playback(filename):
    data, fs = sf.read(filename)
    sd.play(data,fs)
    return data, fs

def cambia_microfono():
    sd.stop()###################################################################################
    while True:
        counter = -1
        print("\n****************************MICROFONOS DISPONIBLES****************************")
        for i in enumerate(sr.Microphone.list_microphone_names()):
            print(i)
            counter += 1
        print("******************************************************************************\n")
        default_devices = sd.default.device#######
        print("INDICE MICRÓFONO ACTUAL: ",default_devices[0])
        speaker("DIGA EN ALTO EL NÚMERO CORRESPONDIENTE AL MICRÓFONO DESEADO.",1)
        try:
            opcion = int(validate_num(listening()))
            if opcion >= 0 and opcion <= counter:
                #default_input = default_devices[0]##########
                sd.default.device=opcion
                print("\nINDICE MICRÓFONO: ",default_devices[0])
                speaker("nuevo microfono establecido correctamente",0)
                break
            else:
                speaker("INDICE FUERA DE RANGO",1)
        except Exception as e:
            print(str(e))
            speaker("NO SE PUDO PROCESAR LA SOLICITUD",1)

def validate_num(value):
    if value in nums:
        return nums[value]
    else:
        return value

def listening():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        r.adjust_for_ambient_noise(source)
        r.energy_threshold=400#10050

        audio = r.listen(source)
        try:
            text = r.recognize_google(audio,language='es-ES')
            print("TEXTO: ",text)
            return text
        except:
            print("Sin entrada")
            pass
            
def select_audio():
    while True:
        op = listening()
        if op == "lista":
            while True:
                print("\n********************LISTA DE AUDIOS********************")
                for elem,tema in enumerate(lista_temas):
                    print(elem,tema)
                print("*******************************************************\n")
                texto = "DIGA EN VOZ ALTA EL NÚMERO CORRESPONDIENTE AL AUDIO DESEADO."
                speaker(texto,1)
                
                try:
                    numero = int(validate_num(listening()))
                    print(type(numero))
                    assert numero in range(len(lista_temas))
                    audio_selec = lista_temas[numero]
                    print("AUDIO SELECCIONADO: {}".format(audio_selec))
                    async_playback(audio_selec)
                    break
                except Exception as e:
                    print(str(e))
                    speaker("NO SE PUDO PROCESAR LA SOLICITUD",1)
                
        elif op == 'para':
            sd.stop()
            print('STOPPED')
            speaker("audio interrumpido",0)
        elif op == 'fin':
            sd.stop()
            speaker("programa finalizado, hasta pronto",0)
            break
        elif op == 'cambia micrófono':
            cambia_microfono()
        elif op == 'comandos':
            comandos()
        
def correct_dir():
    while True:
        direc = input("Introduce directorio válido: ")
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

def comandos():
    print("\n********************COMANDOS DE VOZ********************")
    print("'lista'-------------------------MUESTRA LISTA DE AUDIOS")
    print("'para'------------------FINALIZA REPRODUCCIÓN DEL AUDIO")
    print("'fin'------------------------------FINALIZA EL PROGRAMA")
    print("'cambia micrófono'--------------------CAMBIAR MICROFONO")
    print("'comandos'----------------------MUESTRA COMANDOS DE VOZ")
    print("********************************************************\n")    

    
#sd.default.device=9 #CAMBIAR DISPOSITIVO DE "ENTRADA/SALIDA"

engine = pyttsx3.init()
engine.setProperty('rate',160)
lista_temas = []

while len(lista_temas) == 0:
    comandos()
    speaker("antes de empezar introduzca ruta al directorio",0)
    correct_dir()

    print("\nCARPETA: ",os.getcwd())

    for i in glob.glob("*.wav"):
        lista_temas.append(i)

    if len(lista_temas) == 0:
        print("CARPETA VACÍA\n")
        speaker("la carpeta seleccionada no contiene archivos válidos",0)

select_audio()




