import glob
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
import os
import pyttsx3
import pickle

lista_temas = []
direc = pickle.load(open('directorios','rb'))
list_inn = False
nums = {'cero':0,'uno':1,'dos':2,'tres':3,'cuatro':4,'cinco':5,'seis':6,'siete':7,'ocho':8,'nueve':9,
        'diez':10,'once':11,'doce':12,'trece':13,'catorce':14,'quince':15}
#C:\Users\Antonio\Documents\videos\audios

def async_playback(filename):
    global list_inn
    data, fs = sf.read(filename)
    sd.play(data,fs)
    list_inn = False
    return data, fs

def cambia_microfono():
    sd.stop()###################################################################################
    while True:
        print("\n****************************MICROFONOS DISPONIBLES****************************")
        for i in enumerate(sr.Microphone.list_microphone_names()):
            print(i)
        print("******************************************************************************\n")
        speaker("DIGA EN ALTO EL NÚMERO CORRESPONDIENTE AL MICRÓFONO DESEADO.",1)
        #print("DIGA EN ALTO EL NÚMERO.")
        try:
            reco = listening()
            if reco in nums:
                opcion = nums[reco]
            else:
                opcion = int(reco)
            sd.default.device=opcion
            print("\nINDICE MICRÓFONO: ",opcion)
            speaker("nuevo microfono establecido correctamente",0)
            break
        except Exception as e:
            print(str(e))

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
                print("*******************************************************\n")
                texto = "DIGA EN VOZ ALTA EL NÚMERO CORRESPONDIENTE AL AUDIO DESEADO."
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
                    speaker("NO SE PUDO PROCESAR LA SOLICITUD.",1)
                
        elif op == 'para':
            list_inn = False
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
        elif op == 'colecciones':
            change_dir()
    
def speaker(content,v):
    engine.say(content)
    if v == 1:
        print(content)
    engine.runAndWait()
    engine.stop()

def validate_num(value):
    if value in nums:
        return nums[value]
    else:
        return value

def change_dir():
    global lista_temas
    sd.stop()
    while True:
        print("\n****************************COLECCIONES****************************")
        for elem,di in enumerate(direc):
            print(elem,di)
        print("*******************************************************************\n")

        speaker("DIGA EN VOZ ALTA EL NÚMERO CORRESPONDIENTE AL DIRECTORIO DESEADO.",1)
        numero = validate_num(listening())
        try:
            os.chdir(direc[int(numero)])
            lista_temas = []
            collect()
            speaker("DIRECTORIO ESTABLECIDO CORRECTAMENTE.",1)
            print("\nCARPETA: ",os.getcwd())
            break
        except:
            speaker("NO SE PUDO PROCESAR LA SOLICITUD.",1)
        
def comandos():
    print("\n********************COMANDOS DE VOZ********************")
    print("'lista'-------------------------MUESTRA LISTA DE AUDIOS")
    print("'para'------------------FINALIZA REPRODUCCIÓN DEL AUDIO")
    print("'fin'------------------------------FINALIZA EL PROGRAMA")
    print("'cambia micrófono'--------------------CAMBIAR MICROFONO")
    print("'comandos'----------------------MUESTRA COMANDOS DE VOZ")
    print("'colecciones'-----------------CAMBIAR CARPETA DE AUDIOS")
    print("********************************************************\n")

def collect():
    for i in glob.glob("*.wav"):
        lista_temas.append(i)
    if len(lista_temas) == 0:
        print("CARPETA VACÍA\n")
        speaker("la carpeta seleccionada no contiene archivos válidos",0)

            
#sd.default.device=9 #CAMBIAR DISPOSITIVO DE "ENTRADA/SALIDA"

engine = pyttsx3.init()
engine.setProperty('rate',160)

while len(lista_temas) == 0:
    comandos()


    print("\n****************************COLECCIONES****************************")
    for elem,di in enumerate(direc):
        print(elem,di)
    print("*******************************************************************\n")

    speaker("DIGA EN VOZ ALTA EL NÚMERO CORRESPONDIENTE AL DIRECTORIO DESEADO O DIGA NUEVO PARA AÑADIR UNO NUEVO.",1)
    opcionn = listening()
    print(opcionn)

    if opcionn == 'nuevo':
        speaker("introduzca nuevo directorio",0)
        new_dir = input("INTRODUZCA NUEVO DIRECTORIO: ")
        if os.path.isdir(new_dir):
            direc.append(new_dir)
            pickle.dump(direc,open("directorios","wb"))
            os.chdir(new_dir)
            collect()
            speaker("DIRECTORIO ESTABLECIDO CORRECTAMENTE.",1)
    else:
        numero = validate_num(opcionn)
        if str(numero).isdigit() and len(direc)>0:
            try:
                new_dir = direc[int(numero)]
                os.chdir(new_dir)
                collect()
                speaker("DIRECTORIO ESTABLECIDO CORRECTAMENTE.",1)
            except Exception as e:
                print(str(e))
                speaker("NO SE PUDO PROCESAR LA SOLICITUD.",1)
    
    print("\nCARPETA: ",os.getcwd())


select_audio()
