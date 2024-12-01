import random
import os
import time
import threading

TIEMPO_ESPERA_FRASES_PERIODICAS = 30

class Frases:
    def __init__(self, bot):
        self.load_frases()
        self.bot = bot
        self.frases_active = False
        self.TIEMPO_ESPERA_FRASES_PERIODICAS = TIEMPO_ESPERA_FRASES_PERIODICAS  # Tiempo en segundos
    def load_frases(self):
        """Carga las frases desde un archivo de texto y devuelve una lista de frases."""
        try:
            if os.path.exists('frases/frases.txt'):
                with open('frases/frases.txt', 'r', encoding='utf-8') as file:
                    self.frases = [line.strip() for line in file if line.strip()]
            else:
                print("El archivo 'frases/frases.txt' no existe.")
                self.frases = []
        except Exception as e:
            print(f"Error al cargar frases: {e}")
            self.frases = []  # Asegurarse de que self.frases sea una lista vacía en caso de error
        
        return self.frases  # Asegúrate de retornar la lista de frases


    def send_random_frase(self, bot):
        """Envía una frase aleatoria al canal."""
        if self.frases:
            frase = random.choice(self.frases)
            bot.envia_mensaje(f"{frase}")
            #print(f"Frase enviada: {frase}")  # Registro para verificar el envío

### Frases aleatorias ################################################################

    def start_random_frases_thread(self):
        """Inicia un hilo que envía frases aleatorias cada cierto tiempo."""
        if not self.frases_active:
            self.frases_active = True
            print("Iniciando hilo de frases aleatorias.")
            self.frases_thread = threading.Thread(target=self.send_frases_periodically)
            self.frases_thread.daemon = True  # Permite que el hilo se cierre cuando el programa principal finaliza
            self.frases_thread.start()
        print("Iniciado hilo de frases aleatorias.")

    def stop_random_frases_thread(self):
        """Detiene el hilo que envía frases aleatorias."""
        if self.frases_active:  # Solo detener si está activo
            self.frases_active = False  # Cambia el estado para detener el bucle en send_frases_periodically
            print("Deteniendo hilo de frases aleatorias.")
            if self.frases_thread and self.frases_thread.is_alive():
                self.frases_thread.join(timeout=1)  # Intenta finalizar el hilo
        print("Detenido hilo de frases aleatorias.")


    def send_frases_periodically(self):
        while self.frases_active:
            time.sleep(self.TIEMPO_ESPERA_FRASES_PERIODICAS)  # Espera el tiempo definido
            frase = random.choice(self.load_frases())
            try:
                self.bot.envia_mensaje(frase)  # Intenta enviar la frase
                print("Enviada frase aleatoria.")
            except Exception as e:
                print(f"Error al enviar frase: {e}")


#########################################################################################