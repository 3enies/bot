from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

class HoroscopeReader:
    def __init__(self, folder):
        self.folder = folder

    def read_horoscope(self, signo):
        """Lee el horóscopo del signo específico desde un archivo de texto."""
        file_path = os.path.join(self.folder, f"{signo.lower()}.txt")
        
        # Verifica si el archivo existe
        if not os.path.exists(file_path):
            return f"No se encontró el horóscopo para el signo: {signo.capitalize()}"
        
        # Lee el contenido del archivo
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()



URL = "https://www.horoscopeservices.com/horoscopes/spanish-daily-horoscopes/index.php"

def generarHoroscop():
    # Abrir URL.
    r = urlopen(URL)
    # Leer el contenido y imprimir su tamaño.
    contenido = r.read()
    # Cerrar para liberar recursos.
    with open("horoscop/text.txt", "wb") as f:
        f.write(contenido)
    r.close()


    # Leer el contenido del archivo HTML
    with open("horoscop/text.txt", "r", encoding="utf-8") as file:
        contenido = file.read()

    # Crear un objeto BeautifulSoup
    soup = BeautifulSoup(contenido, "html.parser")

    # Obtener solo el texto sin etiquetas HTML
    texto_limpio = soup.get_text()

    # Guardar el texto limpio en un nuevo archivo
    with open("horoscop/texto_limpio.txt", "w", encoding="utf-8") as file:
        file.write(texto_limpio)

    # Ruta del archivo de entrada y salida
    archivo_entrada = "horoscop/texto_limpio.txt"
    archivo_salida = "horoscop/blanc.txt"

    # Leer el contenido del archivo de entrada
    with open(archivo_entrada, "r", encoding="utf-8") as file:
        lineas = file.readlines()

    # Filtrar las líneas que no están en blanco
    lineas_sin_blanco = [linea for linea in lineas if linea.strip()]

    # Guardar las líneas filtradas en el archivo de salida
    with open(archivo_salida, "w", encoding="utf-8") as file:
        file.writelines(lineas_sin_blanco)

    # print(f"Las líneas en blanco han sido eliminadas y el resultado se ha guardado en '{archivo_salida}'.")

    archivo_salidas = "horoscop/archivo_modificado.txt"

    # Leer el contenido del archivo de entrada
    with open(archivo_salida, "r", encoding="utf-8") as file:
        lineas = file.readlines()

    # Omitir las primeras 10 líneas
    lineas_modificadas = lineas[45:]

    # Guardar las líneas modificadas en el archivo de salida
    with open(archivo_salidas, "w", encoding="utf-8") as file:
        file.writelines(lineas_modificadas)

    # Abrir el archivo en modo lectura
    with open(archivo_salidas, 'r', encoding='utf-8') as archivo:
        # Leer la primera línea
        primera_linea = archivo.readline().strip()  # Usar strip() para eliminar el salto de línea

    # Imprimir la primera línea
    #print(primera_linea)

    signos_zodiaco = [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces"
    ]
    posicions = {}
    for signo in signos_zodiaco:
        indice = primera_linea.find(signo)
        if indice != -1:
            # print(f"La palabra {signo} se encuentra en la posición {indice}.")
            posicions[signo] = indice
        else:
            pass
            #print(f"La palabra {signo} no está en la cadena.")
    #print(posicions)

    with open("horoscop/aries.txt", "w", encoding="utf-8") as file:
        file.writelines(primera_linea[posicions["Aries"]+5:posicions["Taurus"]])
    with open("horoscop/tauro.txt", "w", encoding="utf-8") as file:
        file.writelines(primera_linea[posicions["Taurus"]+6:posicions["Gemini"]])
    with open("horoscop/geminis.txt", "w", encoding="utf-8") as file:
        file.writelines(primera_linea[posicions["Gemini"]+6:posicions["Cancer"]])
    with open("horoscop/cancer.txt", "w", encoding="utf-8") as file:
        file.writelines(primera_linea[posicions["Cancer"]+6:posicions["Leo"]]) 
    with open("horoscop/leo.txt", "w", encoding="utf-8") as file:
        file.writelines(primera_linea[posicions["Leo"]+3:posicions["Virgo"]])
    with open("horoscop/virgo.txt", "w", encoding="utf-8") as file:
        file.writelines(primera_linea[posicions["Virgo"]+5:posicions["Libra"]]) 
    with open("horoscop/libra.txt", "w", encoding="utf-8") as file:
        file.writelines(primera_linea[posicions["Libra"]+5:posicions["Scorpio"]])  
    with open("horoscop/escorpio.txt", "w", encoding="utf-8") as file:
        file.writelines(primera_linea[posicions["Scorpio"]+7:posicions["Sagittarius"]]) 
    with open("horoscop/sagitario.txt", "w", encoding="utf-8") as file:
        file.writelines(primera_linea[posicions["Sagittarius"]+11:posicions["Capricorn"]])
    with open("horoscop/capricornio.txt", "w", encoding="utf-8") as file:
        file.writelines(primera_linea[posicions["Capricorn"]+9:posicions["Aquarius"]])
    with open("horoscop/acuario.txt", "w", encoding="utf-8") as file:
        file.writelines(primera_linea[posicions["Aquarius"]+8:posicions["Pisces"]])
    with open("horoscop/piscis.txt", "w", encoding="utf-8") as file:
        file.writelines(primera_linea[posicions["Pisces"]+6:])

    #https://horoscopeservices.com/horoscopes/spanish-daily-horoscopes/

    #Eliminación de los archivos de procesamiento intermedios
    def eliminar_archivo(file_path):
        """Intenta eliminar un archivo y maneja excepciones."""
        if os.path.exists(file_path):
            try:
                os.remove(file_path)  # Eliminar el archivo
                print(f"Archivo '{file_path}' eliminado.")
            except PermissionError:
                print(f"No se puede eliminar el archivo '{file_path}': permisos denegados.")
            except Exception as e:
                print(f"Error al eliminar el archivo '{file_path}': {e}")
        else:
            print(f"El archivo '{file_path}' no existe.")

    def eliminarArxius():
        # Rutas de los archivos que deseas eliminar
        archivos_a_eliminar = [
            'horoscop/text.txt',
            'horoscop/texto_limpio.txt',
            'horoscop/blanc.txt',
            'horoscop/archivo_modificado.txt',
        ]

        # Llamar a la función para eliminar cada archivo
        for archivo in archivos_a_eliminar:
            eliminar_archivo(archivo)
    
    eliminarArxius()
#generarHoroscop()

 


