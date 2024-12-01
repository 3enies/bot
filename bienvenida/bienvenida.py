import random
import time
TIEMPO_ESPERA_BIENVENIDA = 3

def bienvenida(nickname):
    nickname = "\x0302" + nickname + "\x0301"
    messages = [
        f"\x0301¡Bienvenido al canal, {nickname}! :)  \x0302!info\x0301 para más información.",
        f"\x0301¡Hola {nickname}! Es genial verte aquí. \x0302!info\x0301 para más información.",
        f"\x0301¡Saludos, {nickname}! Espero que disfrutes tu estancia. \x0302!info\x0301 para más información.",
        f"\x0301¡Bienvenido, {nickname}! Si necesitas algo, ¡aquí estoy! \x0302!info\x0301 para más información.",
        f"\x0301¡Qué alegría verte aquí, {nickname}! Usa \x0302!info\x0301 para descubrir más.",
        f"\x0301¡Hola, {nickname}! Bienvenido al canal. \x0302!info\x0301 para más detalles.",
        f"¡{nickname}, llegaste al lugar correcto! Para saber más, escribe \x0302!info\x0301.",
        f"\x0301¡Hola {nickname}! Qué bueno verte. \x0302!info\x0301 es tu comando para información adicional.",
        f"\x0301¡Bienvenido, {nickname}! Si tienes preguntas, usa \x0302!info\x0301 para comenzar.",
        f"¡{nickname},\x0301 bienvenido a nuestra comunidad! \x0302!info\x0301 para obtener más detalles.",
        f"\x0301¡Saludos, {nickname}!\x0301 Échale un vistazo a \x0302!info\x0301 para ver qué hay aquí.",
        f"¡{nickname}, encantado de tenerte aquí! \x0302!info\x0301 para más información.",
        f"\x0301¡Hola y bienvenido, {nickname}! Descubre más usando \x0302!info\x0301.",
        f"\x0301¡Gracias por unirte, {nickname}! Escribe \x0302!info\x0301 si deseas saber más.",
        f"\x0301¡Saludos, {nickname}! Échale un vistazo a \x0302!info\x0301 para ver qué hay aquí.",
        f"\x0301¡Bienvenido, {nickname}! Usa \x0302!info\x0301 para ver más detalles.",
        f"\x0301¡Hola, {nickname}! Mira \x0302!info\x0301 y descubre todo lo que tenemos.",
        f"\x0301¡Hey, {nickname}! Prueba \x0302!info\x0301 para conocer las opciones.",
        f"\x0301¡Qué alegría verte, {nickname}! Explora \x0302!info\x0301 para empezar.",
        f"\x0301¡Hola, {nickname}! Dale un vistazo a \x0302!info\x0301 para ponerte al día.",
        f"\x0301¡Genial tenerte aquí, {nickname}! Consulta \x0302!info\x0301 para saber más.",
        f"\x0301¡Hey, {nickname}! No olvides revisar \x0302!info\x0301 para ver qué hacer.",
        f"\x0301¡Qué gusto verte, {nickname}! Usa \x0302!info\x0301 para ver lo nuevo.",
        f"\x0301¡Hola, {nickname}! Échale un vistazo a \x0302!info\x0301 y disfruta explorando.",
        f"\x0301¡Bienvenido, {nickname}! Explora \x0302!info\x0301 para ver todo lo que ofrecemos.",
        f"\x0301¡Saludos, {nickname}! Prueba \x0302!info\x0301 y conoce todas las opciones.",
        f"\x0301¡Qué emoción verte aquí, {nickname}! Entra a \x0302!info\x0301 para empezar.",
        f"\x0301¡Bienvenido de vuelta, {nickname}! Usa \x0302!info\x0301 y ponte al tanto.",
        f"\x0301¡Hola, {nickname}! Explora \x0302!info\x0301 y descubre lo nuevo.",
        f"\x0301¡Hey, {nickname}! Visita \x0302!info\x0301 para aprender rápidamente.",
        f"\x0301¡Hola, {nickname}! Usa \x0302!info\x0301 y ve qué hay aquí.",
        f"\x0301¡Bienvenido, {nickname}! Consulta \x0302!info\x0301 para ver todo lo disponible.",
        f"\x0301¡Hey, {nickname}! En \x0302!info\x0301 tienes toda la información que necesitas.",
        f"\x0301¡Qué gusto tenerte aquí, {nickname}! Échale un vistazo a \x0302!info\x0301 para comenzar.",
    ]
    
    time.sleep(TIEMPO_ESPERA_BIENVENIDA)
    message = random.choice(messages)
    return (message)

