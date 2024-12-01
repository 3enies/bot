import threading
import time

### Info de los comandos disponibles del bot #####################################################
def commandamentsBot(self, nick):
    def enviar_comandos():
        info = [
            "\x0302Éstos son los comandos del bot. (\x0303!info\x0301)\n",
            "\x0303!alarma <minutos>\x0301 - Programa una alarma para dentro de <minutos> minutos.\n",
            "\x0303!astro <signo>\x0301 (sin acentos), muestra el horóscopo diario del signo.\n",
            "\x0303!frase\x0301 - Envía una frase aleatoria. \x0303!santo\x0301 - Muestra el sant@ del día.\n",
            "\x0303!radio\x0301 - Muestra información de los comandos de la radio.\n",
        ]
        self.privmsg(nick, "\x0303\u25A0\u25A1\u25A0\x0301")
        for funcio in info:
            print(f"Enviando a {nick}: {funcio}")
            self.privmsg(nick, funcio)
            time.sleep(1)
        self.privmsg(nick, "\x0302Fin de la !info.\x0301")
        self.privmsg(nick, "\x0303\u25A0\u25A1\u25A0\x0301")

        # Enviar comandos sólo a los DJs permitidos
        if nick in self.djs_permitidos:
            info = [
                "\x0302Éstos son los comandos de radio.\x0301\n",
                "Escribe \x0304!dj <nick>\x0301 para iniciar la emisión.",
                "\x0303\x0304!tematica <tematica>\x0301 establece una temática,",
                "\x0301y\x0303 !tematica off\x0301 elimina la temática.",

            ]
            for funcio in info:
                self.privmsg(nick, funcio)
                time.sleep(1)
            self.privmsg(nick, "\x0302Fin de los comandos de radio.\x0301")
            self.privmsg(nick, "\x0303\u25A0\u25A1\u25A0\x0301")

        # Enviar comandos sólo a los administradores
        if self.is_owner(nick):
            info = [
                "\x0302Éstos son los comandos del admin.\x0301\n",
                "\x0303!aradio <on|off>\x0301 - Gestiona el recordatorio de radio periódicamente, defecto off",
                "\x0303!afrase <on|off>\x0301 - Gestiona el envio de frases periódicas, defecto off",
                "\x0303!salir\x0301 - Para salir",
            ]
            for funcio in info:
                self.privmsg(nick, funcio)
                time.sleep(1)
            self.privmsg(nick, "\x0302Fin de los comandos de admin.\x0301")
            self.privmsg(nick, "\x0303\u25A0\u25A1\u25A0\x0301")

    # Ejecutar el envío de comandos en un hilo separado
    threading.Thread(target=enviar_comandos).start()
