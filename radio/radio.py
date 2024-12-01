import threading
import time
import requests
import json

RADIO = "https://zeno.fm/radio/triskel/"
CANAL = "#Historia_de_O"
DJS_PERMITIDOS = ["auto", "Ka", "Dom-Spanker", "DarthNihilus", "nina[ZDm]", "_zarina"]  # Lista de DJs permitidos
TIEMPO_REPETICION_TEMATICA = 10 * 60  # Repetición cada 30 minutos (30 * 60) en segundos*60
TIEMPO_ENVIO_RECORDATORIO_RADIO = 15 * 60  # Tiempo entre envíos de recordatorio (60 segundos, ajusta según necesidad)

class Radio:
    def __init__(self, bot):
        self.bot = bot
        self.dj_actual = "auto"
        self.tematica = "Música variada"  # Tema predeterminado
        self.tematica_thread = None  # Para manejar el hilo de la temática
        self.radio_active = False  # Estado del hilo de recordatorio
        self.radio_thread = None  # Hilo de recordatorio

    def send_radio_message(self):
        """Envia el mensaje de radio y resetea el temporizador."""
        # Enviar mensaje con la temática actual
        self.bot.envia_mensaje("\x0303\u25A0\u25A1\u25A0")
        self.bot.envia_mensaje(f"\x0303Bienvenid@\x0302 a la radio del canal: \x0305{CANAL}\x0301")
        self.bot.envia_mensaje(f"Escúchanos en: {RADIO}. Emitiendo \x0304{self.dj_actual}\x0301.")
        self.bot.envia_mensaje(f"Escribe \x0304!peticion <Tema - Artista>\x0301 para pedir una canción.")
        # Aquí siempre enviamos la temática actualizada
        self.bot.envia_mensaje(f"La temática actual de la emisión es: \x0303{self.tematica}\x0301")
        self.bot.envia_mensaje("\x0303\u25A0\u25A1\u25A0\x0301")
        time.sleep(1)

    def set_dj(self, dj_name):
        """Establece el DJ actual."""
        if dj_name in DJS_PERMITIDOS:
            self.dj_actual = dj_name
            self.send_radio_message()
        else:
            self.bot.envia_mensaje(f"\x0304{dj_name}\x0301 no es un DJ permitido.")
    
    def actualizar_tematica(self, nueva_tematica):
        """Actualiza la temática actual de la radio."""
        self.tematica = nueva_tematica
        # Si el hilo de la temática está activo, también actualizamos la temática en él.
        if self.tematica_thread:
            self.tematica_thread.actualizar_tematica(nueva_tematica)
        print(f"Temática actualizada a: {nueva_tematica}")
    
    def enviar_recordatorio_periodico(self):
        """Envía mensajes de radio periódicamente."""
        while self.radio_active:
            print("Enviando mensaje de radio...")
            self.send_radio_message()  # Siempre enviará la temática actualizada
            time.sleep(TIEMPO_ENVIO_RECORDATORIO_RADIO)  # Espera entre envíos

    def start_radio_thread(self):
        """Inicia el hilo del recordatorio de radio si no está activo."""
        if not self.radio_active:
            self.radio_active = True
            self.radio_thread = threading.Thread(target=self.enviar_recordatorio_periodico)
            self.radio_thread.daemon = True
            self.radio_thread.start()
            print("Recordatorio de radio activado.")

    def stop_radio_thread(self):
        """Detiene el hilo del recordatorio de radio."""
        if self.radio_active:
            self.radio_active = False  # Cambia el estado para detener el bucle en enviar_recordatorio_periodico
            if self.radio_thread and self.radio_thread.is_alive():
                self.radio_thread.join(timeout=1)  # Intenta finalizar el hilo
            print("Recordatorio de radio desactivado.")
        else:
            self.radio_active = False  # Cambia el estado para detener el bucle en enviar_recordatorio_periodico

    # Función para escuchar el stream en un hilo
    def listen_stream(self):
        url = "https://api.zeno.fm/mounts/metadata/subscribe/exmhtgzpg5yvv"
        reconnection_attempts = 0  # Intentos de reconexión

        while True:
            try:
                # Conecta al flujo de eventos con 'requests'
                response = requests.get(url, stream=True, timeout=10)  # Timeout para evitar bloqueos
                response.raise_for_status()  # Verificar si la respuesta es exitosa (código 200)

                # Leer el flujo de datos línea por línea
                for line in response.iter_lines(decode_unicode=True):
                    if line:  # Si la línea no está vacía
                        # Eliminar el prefijo "data:" si existe
                        if line.startswith("data:"):
                            line = line[len("data:"):].strip()  # Elimina "data:" y posibles espacios

                        try:
                            # Intentar analizar el JSON
                            data = json.loads(line)
                            stream_title = data.get('streamTitle')
                            if stream_title:
                                print(f"Artista - Canción: {stream_title}")
                                self.bot.envia_mensaje(f"Sonando... \x0304{stream_title}\x0301")
                                
                        except json.JSONDecodeError:
                            #print(f"Error al parsear el JSON recibido: {line}")
                            continue

                reconnection_attempts = 0  # Reinicia el contador de reconexión tras una conexión exitosa

            except requests.exceptions.Timeout:
                print("Error de tiempo de espera. Intentando nuevamente...")
            except requests.exceptions.ConnectionError:
                print("Error de conexión. Intentando nuevamente...")
            except requests.exceptions.HTTPError as http_err:
                print(f"Error HTTP: {http_err}. Intentando nuevamente...")
            except Exception as e:
                print(f"Error inesperado: {e}. Intentando nuevamente...")

            reconnection_attempts += 1
            if reconnection_attempts >= 5:
                print("Demasiados intentos fallidos. Verifique la conexión o el servidor.")
                break  # Detenemos la reconexión si los intentos fallan muchas veces

            time.sleep(5)  # Espera antes de intentar nuevamente

    # Crear un hilo para escuchar el stream
    def start_stream_listener(self):
        if not hasattr(self, 'listener_thread') or not self.listener_thread.is_alive():
            self.listener_thread = threading.Thread(target=self.listen_stream, daemon=True)
            self.listener_thread.start()
            print("Hilo de escucha iniciado.")
            self.bot.envia_mensaje("Mostrando canciones desde \x0302zeno.fm\x0301")
        else:
            print("El hilo de escucha ya está en ejecución.")
            self.bot.envia_mensaje("\x0302zeno.fm\x0301 ya envía información de las canciones.")


class TematicaThread(threading.Thread):
    def __init__(self, bot, tematica, canal):
        super().__init__()
        self.bot = bot
        self.tematica = tematica
        self.canal = canal
        self.running = True

    def run(self):
        while self.running:
            # Aquí enviamos la temática actualizada cada vez que se envía un mensaje
            self.bot.envia_mensaje(f"{self.canal}, la temática actual de la emisión de radio es: \x0303{self.tematica}\x0301")
            time.sleep(TIEMPO_REPETICION_TEMATICA)  # Espera el tiempo definido

    def stop(self):
        self.running = False

    def actualizar_tematica(self, nueva_tematica):
        """Actualiza la temática en el hilo."""
        self.tematica = nueva_tematica
