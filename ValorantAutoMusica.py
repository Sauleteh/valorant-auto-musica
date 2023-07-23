# Programa para escuchar música mientras juegas Valorant, muteando la música de forma automática al empezar las rondas
# La música se pone de forma manual en el Opera: Entras en Youtube y te pones una playlist. Con eso ya estaría preparado
from __future__ import print_function
import time
import re
import win32gui
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from superImagesearchMod import *
import warnings
warnings.simplefilter("ignore", UserWarning)
from pywinauto.application import Application

# TODO:
# Cuando se va a comprar arma también se está en estado de preparación
# Al pasar de 0 a X de volumen, el volumen pasa de golpe porque primero se cambia el volumen y luego se reanuda el video
# En Icebox todo está muy blanco
# Añadir imgCompra e imgProrroga

########## Asignación de variables globales ##########
### Estados:
# 0 - No está en partida
# 1 - En partida (preparación)
# 2 - En partida (vivo)
# 3 - En partida (muerto)
# 4 - Partida terminada
###
tiempoSleep = 0.2 # Tiempo de actualización del bucle de búsqueda (en segundos)
volumenEstado = [1, 0.7, 0, 0.4, 1] # Volúmenes para cada estado (de 0 a 1)
rutaPrograma = "D:\\Users\\Saulete\\PycharmProjects\\untitled\\ValorantAutoMusica"
imgDerrota = rutaPrograma + "\\imgDerrota.png" # Imagen cuando pierdes al final de la partida (en grande)
imgVictoria = rutaPrograma + "\\imgVictoria.png" # Imagen cuando ganas al final de la partida (en grande)
imgEmpate = rutaPrograma + "\\imgEmpate.png" # Imagen cuando empatas al final de la partida (en grande si existe)
imgPreparacion = rutaPrograma + "\\imgPreparacion.png" # Cuadro de texto que te indica que estás en fase de compra
imgMuerto = rutaPrograma + "\\imgMuerto.png" # Cuadro a la derecha que te indica que es un reporte de combate (alternativamente usar imagen en negro cuando se muere)
imgDecisivo = rutaPrograma + "\\imgDecisivo.png" # Imagen de preparación de la última ronda en la segunda parte
imgRondaCambio = rutaPrograma + "\\imgRondaCambio.png" # Imagen de preparación de la última ronda en la primera parte
imgProrroga = rutaPrograma + "\\imgProrroga.png" # Imagen de preparación cuando se está en prórroga TODO
imgCompra = rutaPrograma + "\\imgCompra.png" # Imagen cuando se abre la tienda en preparación TODO

########## Funciones ##########
# Conseguir el controlador del volumen de Opera
def getControladorMusica():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "opera.exe":
            return volume

def intentarBuscarImagen(valorant, imagen):
    exito = 1
    while exito > 0:
        try:
            res = imagesearch(valorant, imagen) # Buscar imagen en el juego
            exito = 0
            #print("Captura del juego realizada con éxito.")
        except:
            if exito == 1:
                print("No se pudo sacar una captura del juego, reintentando...")
            exito += 1
            time.sleep(tiempoSleep)
    return res

def actualizarEstado(valorant, estadoActual):
    derrota = intentarBuscarImagen(valorant, imgDerrota)
    estaImgDerrota = derrota[0] > 0 or derrota[1] > 0
    victoria = intentarBuscarImagen(valorant, imgVictoria)
    estaImgVictoria = victoria[0] > 0 or victoria[1] > 0
    empate = intentarBuscarImagen(valorant, imgEmpate)
    estaImgEmpate = empate[0] > 0 or empate[1] > 0
    preparacion = intentarBuscarImagen(valorant, imgPreparacion)
    estaImgPreparacion = preparacion[0] > 0 or preparacion[1] > 0
    muerto = intentarBuscarImagen(valorant, imgMuerto)
    estaImgMuerto = muerto[0] > 0 or muerto[1] > 0
    decisivo = intentarBuscarImagen(valorant, imgDecisivo)
    estaImgDecisivo = decisivo[0] > 0 or decisivo[1] > 0
    rondaCambio = intentarBuscarImagen(valorant, imgRondaCambio)
    estaImgRondaCambio = rondaCambio[0] > 0 or rondaCambio[1] > 0

    if (estaImgPreparacion and estadoActual == 0) or (estaImgDecisivo and estadoActual == 0) or (estaImgRondaCambio and estadoActual == 0): # 1 Se empezó la partida
        return 1
    elif estaImgMuerto and estadoActual == 2: # 3 Se murió mientras se estaba vivo
        return 3
    elif (estaImgPreparacion and estadoActual == 3) or (estaImgDecisivo and estadoActual == 3) or (estaImgRondaCambio and estadoActual == 3): # 4 Se murió y terminó la ronda, empezando otra nueva
        return 1
    elif (estaImgPreparacion and estadoActual == 2) or (estaImgDecisivo and estadoActual == 2) or (estaImgRondaCambio and estadoActual == 2): # 5 Se terminó la ronda sin morir, empezando otra nueva
        return 1
    elif (estaImgVictoria and estadoActual == 2) or (estaImgDerrota and estadoActual == 2) or (estaImgEmpate and estadoActual == 2): # 6 Se terminó la partida mientras se estaba vivo
        return 4
    elif (estaImgVictoria and estadoActual == 3) or (estaImgDerrota and estadoActual == 3) or (estaImgEmpate and estadoActual == 3): # 7 Se terminó la partida mientras se estaba muerto
        return 4
    elif (estaImgVictoria and estadoActual == 1) or (estaImgDerrota and estadoActual == 1) or (estaImgEmpate and estadoActual == 1):  # 8 Partida terminada por rendición en fase de compra
        return 4
    elif (not estaImgPreparacion and estadoActual == 1) and (not estaImgDecisivo and estadoActual == 1) and (not estaImgRondaCambio and estadoActual == 1): # 2 Se terminó la fase de compra y se empezó la ronda
        return 2
    elif not estaImgMuerto and estadoActual == 3: # 9 Estabas muerto y te revivieron
        return 2
    elif not estaImgVictoria and not estaImgDerrota and not estaImgEmpate and estadoActual == 4:  # 10 Ir al menú después de terminar la partida
        return 0
    else:
        return estadoActual

def establecerVolumen(volumenAnterior, volumenNuevo, controladorMusica, divisiones=20, tiempoEntreSuma=0.035): # Volúmenes de 0 a 1, hacer progresivamente
    valor = volumenAnterior
    addValor = volumenNuevo - volumenAnterior
    for i in range(divisiones, 1, -1): # Desde el volumen anterior hasta el volumen nuevo poco a poco (menos el valor nuevo)
        valor = valor + addValor / divisiones
        controladorMusica.SetMasterVolume(round(valor, 2), None)
        time.sleep(tiempoEntreSuma)
    controladorMusica.SetMasterVolume(volumenNuevo, None) # Añadimos al final el volumen nuevo

def pulsarVideo(volumenAnterior, volumenActual, youtube, titulo):
    if (volumenAnterior == 0 and volumenActual > 0) or (volumenActual == 0 and volumenAnterior > 0):
        youtube[titulo.texts()[0]].send_keystrokes(" ") # Mandar evento de pulsación de barra espaciadora para pausar/reanudar el video

########## Programa principal ##########
if __name__ == "__main__":
    # Antes de poder empezar a realizar el bucle, es necesario conocer:
    volumenMusica = getControladorMusica() # El controlador de volumen
    intentos = 1
    while volumenMusica is None:
        if intentos == 1:
            print("No se encontró el controlador de volumen del navegador, esperando a que el usuario abra el navegador...")
        volumenMusica = getControladorMusica()
        intentos += 1
        time.sleep(tiempoSleep)
    print("Controlador de volumen encontrado.")

    hwndOpera = win32gui.GetForegroundWindow() # El controlador de ventana de Opera (este es el detector)
    intentos = 1
    while " - YouTube" not in win32gui.GetWindowText(hwndOpera):
        if intentos == 1:
            print("Esperando a que el usuario abra Youtube y ponga la ventana en primer plano...")
        hwndOpera = win32gui.GetForegroundWindow()
        intentos += 1
        time.sleep(tiempoSleep)
    app = Application(backend='win32').connect(title_re=u'.* - YouTube - Opera') # Este es el controlador de Opera
    wnd = app.top_window() # Ventana de obtención de título
    print("Controlador de ventana de Youtube encontrado. Recuerda: no minimices el Opera y pon el video en pausa.")

    hwndValorant = buscarValorant("UnrealWindow", None) # El controlador de ventana de Valorant
    intentos = 1
    while "VALORANT" not in win32gui.GetWindowText(hwndValorant):
        if intentos == 1:
            print("Esperando a que el usuario abra Valorant y ponga la ventana en primer plano...")
        hwndValorant = win32gui.GetForegroundWindow()
        intentos += 1
        time.sleep(tiempoSleep)
    print("Controlador de ventana de Valorant encontrado.")
    print("Control de volumen automático empezado, no hace falta que haga nada más.")

    estadoJuego = 0  # Estado del juego
    estadoAnterior = 0 # Estado anterior del juego
    salirJuego = False
    while not salirJuego:
        estadoJuego = actualizarEstado(hwndValorant, estadoJuego) # Actualizar el estado en el que se encuentra el juego
        if estadoJuego != estadoAnterior:
            establecerVolumen(volumenEstado[estadoAnterior], volumenEstado[estadoJuego], volumenMusica) # Poner el volumen según el estado, de forma progresiva
            pulsarVideo(volumenEstado[estadoAnterior], volumenEstado[estadoJuego], app, wnd) # Si el volumen a poner es 0, pausar el video también
            print(str(estadoAnterior) + " -> " + str(estadoJuego))
            estadoAnterior = estadoJuego
        time.sleep(tiempoSleep) # Tiempo de espera entre comprobaciones