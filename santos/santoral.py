import os
from datetime import datetime
directorio = "santoral"
def cargar_santoral(directorio):
    """
    Carga los santos de cada día desde los archivos del directorio.
    Cada archivo representa un mes del año y debe tener 31 líneas máximo,
    una para cada día.
    """
    santoral = {}  # Inicializa el diccionario para almacenar los santos
    for mes in range(1, 13):
        nombre_archivo = f"{mes:02}.txt"  # Nombres de archivo: '01.txt', '02.txt', ..., '12.txt'
        ruta_archivo = os.path.join(directorio, nombre_archivo)

        if os.path.exists(ruta_archivo):
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                # Guardamos el contenido del archivo en la estructura
                santoral[mes] = [linea.strip() for linea in archivo.readlines()]
        else:
            print(f"Archivo {nombre_archivo} no encontrado.")

    return santoral

def obtener_santo_del_dia(santoral, mes, dia):
    """
    Retorna el santo correspondiente al día y mes indicados.
    Si el día no existe, se maneja la excepción.
    """
    try:
        return santoral[mes][dia - 1]
    except (KeyError, IndexError):
        return "No hay datos para este día."

def mostrar_santo_de_hoy(directorio):
    """
    Muestra el santo del día de hoy basado en la fecha actual del sistema.
    """
    santoral = cargar_santoral(directorio)  # Carga los datos
    hoy = datetime.today()
    mes = hoy.month
    dia = hoy.day

    santo = obtener_santo_del_dia(santoral, mes, dia)
    print(f"Santoral del día {dia}/{mes}: {santo[3:]}")
    return santo[3:] # Li lleve el nombre i l'espai
# # Prueba de la función
# if __name__ == "__main__":
#     # Directorio donde se encuentran los archivos
#     directorio = "santoral"
    
#     # Mostrar el santo del día actual
#     mostrar_santo_de_hoy(directorio)
