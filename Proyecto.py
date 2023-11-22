from array import array
import math

def music(archivo_salida, duracion_por_nota=4, frecuencia_muestreo=44100, profundidad_bits=16, num_canales=1):
    # Frecuencia base de Sol (G)
    frecuencia_base = 392.0

    # Grados de la escala de Sol
    grados_escala = [0, 2, 4, 5, 7, 9, 11, 12]

    # Calcular el número total de muestras para una nota
    num_muestras_por_nota = int(duracion_por_nota * frecuencia_muestreo)

    # Calcular el número total de muestras
    num_muestras_total = len(grados_escala) * num_muestras_por_nota

    # Inicializar un array para almacenar las muestras
    muestras = array('h', [0] * num_muestras_total)

    # Generar datos de audio para la escala de sol ascendente
    for i, grado in enumerate(grados_escala):
        frecuencia = frecuencia_base * 2 ** (grado / 12.0)

        # Calcular el tiempo para cada muestra
        for j in range(num_muestras_por_nota):
            tiempo = j / frecuencia_muestreo
            valor = int(32767.0 * 0.5 * math.sin(2 * math.pi * frecuencia * tiempo))
            indice = i * num_muestras_por_nota + j
            muestras[indice] += valor

    # Escribir el array de muestras en el archivo WAV
    with open(archivo_salida, 'wb') as archivo:
        archivo.write(b'RIFF')
        archivo.write((36 + num_muestras_total * num_canales * profundidad_bits // 8).to_bytes(4, 'little'))
        archivo.write(b'WAVE')
        archivo.write(b'fmt ')
        archivo.write((16).to_bytes(4, 'little'))
        archivo.write((1).to_bytes(2, 'little'))
        archivo.write((num_canales).to_bytes(2, 'little'))
        archivo.write((frecuencia_muestreo).to_bytes(4, 'little'))
        archivo.write((frecuencia_muestreo * num_canales * profundidad_bits // 8).to_bytes(4, 'little'))
        archivo.write((num_canales * profundidad_bits // 8).to_bytes(2, 'little'))
        archivo.write((profundidad_bits).to_bytes(2, 'little'))
        archivo.write(b'data')
        archivo.write((num_muestras_total * num_canales * profundidad_bits // 8).to_bytes(4, 'little'))

        # Escribir el array de muestras en el archivo WAV
        muestras.tofile(archivo)

# Construccion del archivo ejecutable
music('proyecto.wav', duracion_por_nota=5, frecuencia_muestreo=44100, profundidad_bits=16, num_canales=1)