from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from obspy import read

# Archivos del proyecto
archivo = Path("datos/senales_reales/muestra_real.mseed")
carpeta_resultados = Path("resultados")
carpeta_resultados.mkdir(parents=True, exist_ok=True)

if not archivo.exists():
    raise FileNotFoundError(f"No existe el archivo: {archivo}")

# Leer el registro sísmico
senales = read(str(archivo))

for traza in senales:
    muestras = np.asarray(traza.data, dtype=float)
    tiempo = traza.times()

    # Estadísticas descriptivas
    print("\nANÁLISIS DE LA SEÑAL SÍSMICA")
    print("-" * 40)
    print("Red:", traza.stats.network)
    print("Estación:", traza.stats.station)
    print("Canal:", traza.stats.channel)
    print("Inicio:", traza.stats.starttime)
    print("Frecuencia:", traza.stats.sampling_rate, "Hz")
    print("Número de muestras:", len(muestras))
    print("Duración (s):", round(tiempo[-1], 3))
    print("Media:", round(float(np.mean(muestras)), 6))
    print("Desviación estándar:",
          round(float(np.std(muestras)), 6))
    print("Amplitud mínima:", float(np.min(muestras)))
    print("Amplitud máxima:", float(np.max(muestras)))

    # Guardar muestras y tiempo en CSV
    tabla = pd.DataFrame({
        "tiempo_segundos": tiempo,
        "amplitud": muestras
    })

    archivo_csv = carpeta_resultados / "senal_real.csv"
    tabla.to_csv(archivo_csv, index=False)

    # Crear y guardar gráfica
    plt.figure(figsize=(12, 4))
    plt.plot(tiempo, muestras, linewidth=0.8)
    plt.title(
        f"Registro sísmico real: "
        f"{traza.stats.network}.{traza.stats.station}."
        f"{traza.stats.channel}"
    )
    plt.xlabel("Tiempo (segundos)")
    plt.ylabel("Amplitud registrada")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    archivo_png = carpeta_resultados / "senal_real.png"
    plt.savefig(archivo_png, dpi=150)
    plt.show()
    plt.close()

    print("\nArchivos generados:")
    print(archivo_csv)
    print(archivo_png)