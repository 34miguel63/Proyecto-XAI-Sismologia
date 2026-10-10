from pathlib import Path

import matplotlib.pyplot as plt
from obspy import read
from obspy.signal.filter import bandpass

# Archivo descargado en el paso anterior
archivo = Path(
    "datos/senales_reales/muestra_evento_chile.mseed"
)

carpeta_resultados = Path("resultados")
carpeta_resultados.mkdir(parents=True, exist_ok=True)

if not archivo.exists():
    raise FileNotFoundError(
        f"No se encontró el archivo: {archivo}"
    )

# Leer el registro
senales = read(str(archivo))

print("ANÁLISIS DEL REGISTRO SÍSMICO")
print("=" * 45)
print("Tamaño del archivo:",
      round(archivo.stat().st_size / (1024 * 1024), 3),
      "MB")

for numero, traza in enumerate(senales, start=1):
    datos = traza.copy()
    datos.detrend("demean")

    muestras = datos.data.astype(float)
    frecuencia = float(datos.stats.sampling_rate)
    tiempo = datos.times()

    print(f"\nTraza {numero}")
    print("Identificador:", datos.id)
    print("Inicio:", datos.stats.starttime)
    print("Fin:", datos.stats.endtime)
    print("Frecuencia:", frecuencia, "Hz")
    print("Cantidad de muestras:", datos.stats.npts)
    print("Duración:", round(float(tiempo[-1]), 2), "segundos")
    print("Amplitud mínima:", float(muestras.min()))
    print("Amplitud máxima:", float(muestras.max()))

    # Primera gráfica: señal original sin su valor medio
    fig, ejes = plt.subplots(2, 1, figsize=(12, 7))

    ejes[0].plot(tiempo, muestras, linewidth=0.6)
    ejes[0].set_title(f"Señal sísmica - {datos.id}")
    ejes[0].set_ylabel("Amplitud")
    ejes[0].set_xlabel("Tiempo (segundos)")
    ejes[0].grid(True, alpha=0.3)

    # Segunda gráfica: filtro entre 0.5 y 5 Hz,
    # únicamente si la frecuencia de muestreo lo permite.
    if frecuencia > 10:
        filtrada = bandpass(
            muestras,
            freqmin=0.5,
            freqmax=5.0,
            df=frecuencia,
            corners=4,
            zerophase=True
        )

        ejes[1].plot(tiempo, filtrada, linewidth=0.6)
        ejes[1].set_title("Señal filtrada entre 0.5 y 5 Hz")
        ejes[1].set_ylabel("Amplitud filtrada")
        ejes[1].set_xlabel("Tiempo (segundos)")
        ejes[1].grid(True, alpha=0.3)
    else:
        ejes[1].text(
            0.5, 0.5,
            "Frecuencia insuficiente para aplicar este filtro",
            ha="center", va="center",
            transform=ejes[1].transAxes
        )
        ejes[1].set_axis_off()

    fig.tight_layout()

    salida = carpeta_resultados / f"analisis_evento_{numero}.png"
    fig.savefig(salida, dpi=150)
    plt.show()
    plt.close(fig)

    print("Gráfica guardada en:", salida)

print("\nAnálisis terminado.")