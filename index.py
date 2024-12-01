import socket 
import ssl
import time
import random
import config
import sys
from alarma.alarma import Alarma # Importamos la clase Alarma
from frases.frases import Frases # Importamos la clase Frases
from astro.astro import HoroscopeReader, generarHoroscop # Importamos la clase HoroscopeReader
from radio.radio import Radio, TematicaThread, DJS_PERMITIDOS, TIEMPO_ENVIO_RECORDATORIO_RADIO  # Importa la clase Radio
from bienvenida.bienvenida import bienvenida
from respuestas.responses import responses
from comandos.comandos_bot import commandamentsBot
from santos.santoral import mostrar_santo_de_hoy
NUMERO_MENSAJES_SPAM = 15
TIEMPO_MENSAJES_SPAM = 10
TIEMPO_INICIO_BOT = 3
class IRCBot:
    def __init__(self):
        self.owner = config.OWNER  # Agrega aquí el propietario del bot
        self.server = config.SERVER
        self.port = config.PORT
        self.nickname = config.NICKNAME
        self.password = config.PASS
        self.realname = config.NAME
        self.channel = config.CHANNEL
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.messages = {}
        self.spam_limit = NUMERO_MENSAJES_SPAM
        self.time_limit = TIEMPO_MENSAJES_SPAM
        self.responses = responses
        # Inicializa el manejador de frases
        self.frases = Frases(self)  # Inicializa el manejador de frases
        self.frases_active = False  # Estado del envío de frases
        self.frases_thread = None  # Hilo para el envío de frases        # Inicializa el manejador de la tragaperras
        # Inicializa el lector de horóscopos         
        self.horoscope_reader = HoroscopeReader('horoscop')
        print("Inicializa el lector de horóscopos")
        # Instancia de la clase Radio
        self.radio = Radio(self)
        print("Inicializa el manejador de la radio")
        self.TIEMPO_ENVIO_RECORDATORIO_RADIO = TIEMPO_ENVIO_RECORDATORIO_RADIO  # Tiempo de espera en segundos (20 min)
        self.radio_thread = None  # Hilo para el recordatorio de radio
        self.radio_active = False  # Estado del recordatorio de radio
        print("Hilo recordatorio de radio iniciado.")
        self.djs_permitidos = DJS_PERMITIDOS
        self.tematica_thread = None  # Para almacenar el hilo de temática
    #Función que determina si un usuario es owner
    def is_owner(self, usuario): return (str(usuario.lower()) == self.owner.lower())

    def process_command(self, message, command): return message.lower().startswith(command)
    
    def privmsg(self, channel, message):
        """Envía un mensaje privado a un canal específico."""
        self.send_cmd(f"PRIVMSG {channel} :{message}")
        print(f"Mensaje privado enviado a {channel}: {message}")

    def connect(self):
        try:
            print(f"Conectando a {self.server}:{self.port}...")
            print(f"Conectando a {self.server}:{self.port}...")
            if self.port == 6697:
                self.sock = ssl.wrap_socket(self.sock)
            self.sock.connect((self.server, self.port))
            if self.password:
                self.send_cmd(f"PASS {self.password}")
            self.send_cmd(f"NICK {self.nickname}")
            self.send_cmd(f"USER {self.nickname} 0 * :{self.realname}")
            print("Conectado. Esperando el final del MOTD o respuesta del servidor...")
            self.wait_for_motd()
        except Exception as e:
            print(f"Error al conectarse: {e}")

    def disconnect_bot(self, mensaje_salida="Desconectando..."):
        try:
            if self.sock:  # Verificar si el socket existe
                # Enviar un mensaje de salida más claro
                self.sock.send(f"QUIT :{mensaje_salida}\r\n".encode('utf-8'))
                print("Enviando mensaje de desconexión al servidor.")
        except OSError as e:
            if e.errno == 9:  # Bad file descriptor
                print("No se puede enviar el mensaje de desconexión: el socket ya está cerrado.")
        finally:
            if self.sock:  # Asegurarse de que el socket se cierra si aún está abierto
                try:
                    self.sock.close()
                    print("Socket cerrado correctamente.")
                except OSError as close_error:
                    print(f"Error al cerrar el socket: {close_error}")
            else:
                print("El socket ya estaba cerrado.")

    def send_cmd(self, cmd):
        try:
            self.sock.send(f"{cmd}\r\n".encode('utf-8'))
        except (BrokenPipeError, ConnectionResetError) as e:
            print(f"Error al enviar comando: {e}")
            self.reconnect()  # Llama a un método para intentar reconectar
    
    def envia_mensaje(self, msg):
        """Envía un mensaje al canal IRC y lo registra en el log."""
        try:
            self.send_cmd(f"PRIVMSG {self.channel} :{msg}")
            #print(f"Mensaje enviado: {msg}")
        except (BrokenPipeError, ConnectionResetError) as e:
            print(f"Error al enviar mensaje: {e}")
            self.reconnect()  # Llama a un método para intentar reconectar

    def send_long_message(self, message):
        """Divide y envía mensajes que son demasiado largos para el IRC."""
        max_length = 400  # Ajusta este valor según el límite del servidor IRC
        for i in range(0, len(message), max_length):
            self.envia_mensaje(message[i:i + max_length])

    def wait_for_motd(self):
        while True:
            response = self.sock.recv(2048).decode('utf-8', errors='ignore').strip('\r\n')
            print(f"Recibido del servidor: {response}")
            # Responder a PING
            if response.startswith("PING"):
                self.send_cmd(f"PONG {response.split()[1]}")
                print("Respondiendo a PING con PONG.")
            # Comprobar si hemos llegado al final del MOTD
            if "376" in response or "422" in response:
                print(f"MOTD finalizado o no disponible. Intentando unirse al canal {self.channel}")
                self.send_cmd(f"JOIN {self.channel}")
                self.send_greeting()
                print("Saludo inicial enviado")
                break  # Sal de este bucle si es necesario

    def send_greeting(self):
        time.sleep(TIEMPO_INICIO_BOT)
        print(f"Enviando saludo inicial de {self.nickname}")
        greeting = f"¡Hola a todos! Soy {self.nickname}, ¡gracias por recibirme!."
        self.envia_mensaje(greeting)
        greeting = f"\x0303!info\x0301 para más información."
        self.envia_mensaje(greeting)
        self.radio.start_stream_listener()

### Detección de spam #########################################################
    def is_spamming(self, user):
        current_time = time.time()
        if user not in self.messages:
            self.messages[user] = []
        self.clean_old_messages(user)
        return len(self.messages[user]) >= self.spam_limit

    def clean_old_messages(self, user):
        current_time = time.time()
        self.messages[user] = [
            msg for msg in self.messages[user]
            if current_time - msg['time'] <= self.time_limit
        ]

    def add_message(self, user, message):
        current_time = time.time()
        if user not in self.messages:
            self.messages[user] = []
        self.messages[user].append({
            'message': message,
            'time': current_time
        })
        self.clean_old_messages(user)
##########################################################################

    def responde_a_mencion(self, message, nick):
        #print(f"Comprobando mención para: {nick} - Mensaje: {message}")
        if self.nickname.lower() in message.lower():
            print("El bot ha sido mencionado.")
            response = random.choice(self.responses)
            self.envia_mensaje(f"{nick}, {response}")

    def ejecutar(self):
        while True:
            try:
                response = self.sock.recv(4096).decode('utf-8', errors='ignore').strip('\r\n')
                print(f"Recibida respuesta del servidor: {response}")
                # Responder a PING
                if response.startswith("PING"):
                    self.send_cmd(f"PONG {response.split()[1]}")
                    print("Respondiendo a PING con PONG")
                # Procesar los mensajes recibidos del canal
                if f"PRIVMSG {self.channel}" in response:
                    nick = response.split('!')[0][1:]
                    message = response.split(f"PRIVMSG {self.channel} :")[1]
                    #print(f"nick fora {nick}")
                    # Si el mensaje empieza con !, tratar como comando
                    if self.process_command(message, "!"):
                        if self.process_command(message, "!salir"):
                            if self.is_owner(nick):  # Verificar si el usuario es el owner
                                #self.disconnect_bot()
                                print("Comando '!salir' recibido. Deteniendo el bot...")
                                sys.exit(0)  # El bot se cerrará correctamente con el código de salida 0
                            else:
                                self.envia_mensaje(f"\x0303{nick}\x0301, sólo \x0302{self.owner}\x0301 puede usar este comando.")
                                print(f"\x0303{nick}\x0301, sólo \x0302{self.owner}\x0301 puede usar este comando.")
                        elif self.process_command(message, "!radio"):
                            print(f"Ejecutando comando !radio por {nick}.")
                            self.radio.send_radio_message()  # Envía el mensaje de radio al instante
                            print(f"Ejecutando comando !radio por {nick}.")
                        elif self.process_command(message, "!dj"):
                            try:
                                # Extrae el nombre del DJ que sigue al comando !dj
                                dj_name = message.split(' ', 1)[1].strip()  # El nombre del DJ es lo que sigue a !dj
                                if not dj_name:  # Si no se proporciona nombre, asigna "auto"
                                    dj_name = "auto"
                                    self.tematica_thread.stop()
                                    self.radio.actualizar_tematica("Música variada")
                                # Verificar si el usuario (nick) está en la lista de DJs permitidos
                                if nick.lower() in [dj.lower() for dj in self.djs_permitidos]:
                                    # Si el DJ está permitido, cambiar el DJ
                                    if dj_name.lower() in [dj.lower() for dj in self.djs_permitidos]:
                                        self.radio.set_dj(dj_name)
                                        self.envia_mensaje(f"El DJ ahora es \x0302{dj_name}\x0301.")
                                    else:
                                        self.envia_mensaje(f"{nick}, {dj_name} no está en la lista de DJs permitidos.")
                                else:
                                    self.envia_mensaje(f"{nick}, no tienes permisos para usar el comando !dj.")
                            except IndexError:
                                self.envia_mensaje(f"{nick}, uso incorrecto. Debes escribir: !dj <nombre del DJ>.")
                        # Verifica si el mensaje contiene el comando !peticion
                        elif self.process_command(message, "!peticion"):
                            try:
                                # Extrae la petición del usuario que sigue al comando !peticion
                                peticion = message.split(' ', 1)[1]
                                dj_name = self.radio.dj_actual
                                # Envía un mensaje privado al DJ con la petición
                                self.privmsg(dj_name, f"{nick} te ha enviado una petición: {peticion}")
                                self.privmsg(nick, f"Tu petición {peticion} se ha enviado a {dj_name}")#
                            except IndexError:
                                self.envia_mensaje(f"{nick}, uso incorrecto. Debes escribir: !peticion <tu petición>.")
                            except Exception as e:
                                self.envia_mensaje(f"{nick}, ocurrió un error al enviar la petición: {e}")
                                print(f"{nick}, ocurrió un error al enviar la petición: {e}")
                        elif message.startswith("!santo"):
                            santo_del_dia = mostrar_santo_de_hoy("santoral")
                            self.envia_mensaje(f"{nick}, el santo del día es: {santo_del_dia}")
                        elif self.process_command(message, "!astro"):
                            partes = message.split()
                            if len(partes) >= 2:
                                signo = partes[1]
                                horoscopo = self.horoscope_reader.read_horoscope(signo)
                                self.send_long_message(f"{nick}: \x0305{signo.capitalize()}\x0301. {horoscopo} Fin.")
                            else:
                                self.envia_mensaje(f"{nick}, debe especificar un signo.")
                        elif self.process_command(message, "!alarma"):
                            try:
                                minutos = message.split()[1]
                                alarma = Alarma(nick, minutos, self)
                                alarma.start()
                                tiempo = "minuto" if minutos == "1" else "minutos"
                                self.privmsg(nick, f"Su alarma ha sido programada para {minutos} {tiempo}.")
                            except (IndexError, ValueError):
                                self.privmsg(nick, f"Formato incorrecto. Use: !alarma <minutos>")
                        elif self.process_command(message, "!frase"):
                            self.frases.send_random_frase(self)
                            print("Frase aleatoria enviada.")
                        elif self.process_command(message, "!info"):
                            commandamentsBot(self, nick)
                        elif self.process_command(message, "!aradio on") and self.is_owner(nick):
                            self.radio.start_radio_thread()
                            self.privmsg(self.owner, "Autoradio activada, repetición cada 15 minutos.")
                        elif self.process_command(message, "!aradio off") and self.is_owner(nick):
                            self.radio.stop_radio_thread()
                            self.privmsg(self.owner, "Autoradio desactivada.")
                        elif (self.process_command(message, "!aradio on") or self.process_command(message, "!aradio off")) and not self.is_owner(nick):
                            self.envia_mensaje(f"Lo siento {nick}, sólo {self.owner} puede utilizar este comando.")
                        elif self.process_command(message, "!afrase on") and self.is_owner(nick):
                            self.frases.start_random_frases_thread()
                            self.privmsg(self.owner, "Frases periódicas activadas, repetición cada 20 minutos.")
                        elif self.process_command(message, "!afrase off") and self.is_owner(nick):
                            self.frases.stop_random_frases_thread()
                            self.privmsg(self.owner, "Frases periódicas desactivadas.")
                        elif (self.process_command(message, "!afrase on") or self.process_command(message, "!afrase off")) and not self.is_owner(nick):
                            self.envia_mensaje(f"Lo siento {nick}, sólo {self.owner} puede utilizar este comando.")
                        elif self.process_command(message, "!tematica"):
                            if nick in self.djs_permitidos:
                                # Caso para detener la temática si recibe `!tematica off`
                                if message.strip().lower() == "!tematica off":
                                    if self.tematica_thread is not None and self.tematica_thread.is_alive():
                                        self.tematica_thread.stop()  # Detener el hilo existente
                                        self.radio.actualizar_tematica("Música variada")
                                        self.privmsg(nick, "La temática se ha detenido.")
                                        self.tematica_thread = None
                                    else:
                                        self.privmsg(nick, "No hay una temática activa para detener.")
                                # Caso para iniciar o cambiar la temática
                                else:
                                    try:
                                        # Extraer la temática del mensaje después de `!tematica`
                                        parts = message.split(" ", 1)  # Dividir en dos partes
                                        if len(parts) < 2:
                                            raise ValueError("Temática vacía.")
                                        tematica = parts[1].strip()  # Obtener la temática
                                        # Detener cualquier hilo activo anterior
                                        if self.tematica_thread is not None and self.tematica_thread.is_alive():
                                            self.tematica_thread.stop()
                                        # Crear e iniciar un nuevo hilo de temática
                                        self.tematica_thread = TematicaThread(self, tematica, self.channel)
                                        self.tematica_thread.start()
                                        self.radio.actualizar_tematica(tematica)
                                        # Envía confirmación de la nueva temática
                                        self.privmsg(nick, f"La temática ha sido establecida a: \x0303{tematica}\x03. Se repetirá cada 15 minutos.")
                                    except ValueError:
                                        # Manejar el caso de temática vacía
                                        self.privmsg(nick, f"{nick}, uso incorrecto. Debes escribir: !tematica <temática>.")
                                    except Exception as e:
                                        # Manejar otros errores
                                        self.envia_mensaje(f"{nick}, ocurrió un error: {e}")
                            else:
                                self.privmsg(nick, f"Lo siento sólo el DJ puede utilizar este comando.")
                        else:
                            self.privmsg(nick, f"Lo siento, comando desconocido.")
                if f"PRIVMSG {self.channel}" in response:
                    nick = response.split('!')[0][1:]  # Extrae el nick
                    message = response.split(f"PRIVMSG {self.channel} :")[1]  # Obtiene el mensaje
                    # Agrega este bloque para manejar menciones
                    self.add_message(nick, message)  # Añade el mensaje para control de spam
                    if self.is_spamming(nick):  # Comprueba si es spam
                        self.envia_mensaje(f"{nick}, has alcanzado el límite de 10 mensajes seguidos.")
                        print(f"Spam detectado de {nick}")
                    self.responde_a_mencion(message, nick)  # Responde a la mención
                # Detectar cuando un nuevo usuario se une al canal
                if "JOIN" in response and self.nickname not in response:
                    # Extraer el nick del usuario que se unió
                    new_nick = response.split('!')[0][1:]
                    self.envia_mensaje(bienvenida(new_nick))
                    print("Enviada bienvenida.")
                    # Verificar si el usuario que se unió es el owner
                    if self.is_owner(new_nick):
                        generarHoroscop()
                        print("Nuevo horóscopo generado")
                if response and any(command in response for command in ("PART", "QUIT")):
                    # Extraer el nick del usuario que salió
                    nick = response.split('!')[0][1:]  # Eliminar el prefijo ':' del nick
                    #print(f"n {nick}, sda {self.radio.dj_actual}")
                    if self.radio.dj_actual.lower() == nick.lower():
                        if self.tematica_thread is not None and self.tematica_thread.is_alive():
                            self.tematica_thread.stop()
                    #if self.dj_actual.lower() == "auto":
                        self.radio.set_dj("auto")
                        self.radio.actualizar_tematica("Música variada")
                        self.envia_mensaje(f"Caída o partida del DJ: {nick}. El DJ pasa a ser auto.")
            except OSError as e:
                if e.errno == 9:  # "Bad file descriptor" error
                    print("El socket ya está cerrado. Deteniendo el bot.")
                    self.disconnect_bot()  # Asegurar el cierre correcto
                    break  # Salir del bucle y detener el bot
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")
                break  # Salir del bucle si ocurre otro error inesperado
            except KeyboardInterrupt:
                print("Bot detenido manualmente por KeyboardInterrupt.")  # Registrar el evento en el log
                self.disconnect_bot()  # Asegurar que el bot se desconecte correctamente

if __name__ == "__main__":
    bot = IRCBot()
    bot.connect()
    bot.ejecutar()