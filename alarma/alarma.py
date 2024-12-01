import threading
import time

class Alarma(threading.Thread):
    def __init__(self, nick, minutos, bot):
        super().__init__()
        self.nick = nick
        self.minutos = int(minutos)
        self.bot = bot

    def run(self):
        # Espera el tiempo especificado en minutos
        time.sleep(self.minutos * 60)
        if (self.minutos == 1):
            tiempo = "minuto"
        else:
            tiempo = "minutos"
        # Envía un mensaje al canal cuando la alarma se active
        self.bot.privmsg(self.nick, f"¡su alarma de {self.minutos} {tiempo} ha sonado!")
        #self.bot.privmsg(f"{self.nick}, ¡su alarma de {self.minutos} {tiempo} ha sonado!")
