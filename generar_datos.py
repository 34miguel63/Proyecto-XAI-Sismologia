import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Reproducibilidad del experimento
np.random.seed(42)

# Parámetros de las señales
cantidad = 1000
longitud = 500
frecuencia_muestreo = 100

# 0 = ruido, 1 = señal sintética de terremoto
X = np.zeros((cantidad, longitud), dtype=np.float32)
y = np.zeros(cantidad, dtype=np.int64)

tiempo = np.arange(longitud) / frecuencia_muestreo

for i in range(cantidad):
    # Ruido de fondo
    senal = np.random.normal(0, 0.25, longitud)

    if i >= cantidad // 2:
        # Generar un evento sintético con oscilaciones
        inicio = np.random.randint(80, 200)
        duracion = longitud - inicio
        t = np.arange(duracion) / frecuencia_muestreo

        envolvente = np.exp(-2.0 * t)
        evento = (
            np.sin(2 * np.pi * 5 * t)
            + 0.5 * np.sin(2 * np.pi * 9 * t)
        ) * envolvente

        senal[inicio:] += 2.0 * evento
        y[i] = 1

    # Normalización individual
    maximo = np.max(np.abs(senal))
    if maximo > 0:
        senal = senal / maximo

    X[i] = senal

# Crear la carpeta de datos
carpeta = Path("datos")
carpeta.mkdir(exist_ok=True)

# Guardar señales y etiquetas
np.save(carpeta / "senales.npy", X)
np.save(carpeta / "etiquetas.npy", y)

print("Datos generados correctamente")
print("Forma de las señales:", X.shape)
print("Forma de las etiquetas:", y.shape)
print("Ruido:", np.sum(y == 0))
print("Eventos sintéticos:", np.sum(y == 1))

# Representar un ejemplo de cada clase
fig, ejes = plt.subplots(2, 1, figsize=(10, 6))

ejes[0].plot(tiempo, X[0])
ejes[0].set_title("Ejemplo de ruido sintético")
ejes[0].set_xlabel("Tiempo (s)")

indice_evento = cantidad - 1
ejes[1].plot(tiempo, X[indice_evento])
ejes[1].set_title("Ejemplo de evento sísmico sintético")
ejes[1].set_xlabel("Tiempo (s)")

plt.tight_layout()
plt.show()