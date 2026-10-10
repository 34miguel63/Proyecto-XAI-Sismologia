from pathlib import Path
from obspy import UTCDateTime
from obspy.clients.fdsn import Client

# Carpeta donde se guardará la muestra
carpeta = Path("datos/senales_reales")
carpeta.mkdir(parents=True, exist_ok=True)

# Servicio público de datos sísmicos
cliente = Client("EARTHSCOPE")

# Intervalo corto de prueba: 60 segundos
inicio = UTCDateTime("2010-02-27T06:30:00")
fin = inicio + 60

try:
    print("Solicitando una muestra sísmica...")
    senales = cliente.get_waveforms(
        network="IU",
        station="ANMO",
        location="00",
        channel="BHZ",
        starttime=inicio,
        endtime=fin
    )

    if len(senales) == 0:
        print("El servicio no devolvió señales para ese intervalo.")
    else:
        salida = carpeta / "muestra_real.mseed"
        senales.write(str(salida), format="MSEED")

        print("Descarga completada.")
        print("Archivo:", salida.resolve())
        print("Tamaño:", round(salida.stat().st_size / 1024, 2), "KB")
        print(senales)

except Exception as error:
    print("No se pudo obtener la señal.")
    print("Detalles:", error)
    print("Comprueba la conexión a Internet e inténtalo de nuevo.")