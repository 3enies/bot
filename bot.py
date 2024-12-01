#!/usr/bin/env python3
import subprocess
import time
import os

def ejecutar_bot():
    """
    Ejecuta y monitorea un bot de IRC.
    Si el bot se detiene, lo reinicia automáticamente.
    """
    comando = ["python3", "index.py"]  # Comando para ejecutar el bot
    while True:
        try:
            print("Iniciando el bot de IRC...")
            proceso = subprocess.Popen(comando)
            
            # Esperar a que el proceso termine
            proceso.wait()
            print(f"El bot se detuvo con código: {proceso.returncode}")
            if proceso.returncode == 0:
                print("El bot se cerró normalmente con '!salir'. No se reiniciará.")
                break  # Salir del bucle sin reiniciar el bot
            
            # Si el proceso termina con un error específico, podemos agregar un manejo especial
            if proceso.returncode != 0:
                print(f"El bot se detuvo con un error (código {proceso.returncode}), reiniciando en 5 segundos...")
            
            # Si el proceso termina, esperar unos segundos antes de reiniciar
            time.sleep(5)
        except KeyboardInterrupt:
            print("Detenido manualmente. Cerrando...")
            if proceso:
                proceso.terminate()
            break
        except OSError as e:
            print(f"Error de sistema al ejecutar el bot: {e}")
            time.sleep(5)  # Esperar un poco antes de intentar de nuevo
        except subprocess.CalledProcessError as e:
            print(f"Error en el proceso: {e}")
            time.sleep(5)
        except Exception as e:
            print(f"Error inesperado: {e}")
            time.sleep(5)

if __name__ == "__main__":
    ejecutar_bot()
