from pathlib import Path
from obspy import UTCDateTime
from obspy.clients.fdsn import Client

carpeta = Path("datos/senales_reales")
carpeta.mkdir(parents=True, exist_ok=True)

salida = carpeta / "muestra_evento_chile.mseed"

cliente = Client("EARTHSCOPE")
inicio = UTCDateTime("2010-02-27T06:30:00")
fin = inicio + 30 * 60  # 30 minutos

try:
    print("Descargando registro sísmico...")
    senales = cliente.get_waveforms(
        network="IU",
        station="ANMO",
        location="00",
        channel="BHZ",
        starttime=inicio,
        endtime=fin
    )

    if len(senales) == 0:
        print("No se recibieron datos para ese intervalo.")
    else:
        senales.write(str(salida), format="MSEED")
        tamano_mb = salida.stat().st_size / (1024 * 1024)

        print("\nDescarga completada.")
        print("Archivo:", salida)
        print(f"Tamaño: {tamano_mb:.3f} MB")
        print(senales)

        if tamano_mb > 10:
            print("ADVERTENCIA: el archivo supera los 10 MB.")
        else:
            print("Tamaño dentro del límite de 10 MB.")

except Exception as error:
    print("No se pudo descargar el registro.")
    print("Detalle:", error)