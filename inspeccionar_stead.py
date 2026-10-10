from pathlib import Path
import pandas as pd

carpeta = Path("datos/stead")

print("Buscando archivos de STEAD...")
print("Carpeta:", carpeta.resolve())

if not carpeta.exists():
    print("\nLa carpeta datos/stead todavía no existe.")
    print("Crea esa carpeta cuando tengas los archivos del conjunto.")
else:
    archivos = list(carpeta.glob("*"))

    if not archivos:
        print("\nLa carpeta está vacía.")
    else:
        for archivo in archivos:
            print(archivo.name, "-", archivo.stat().st_size, "bytes")

    csvs = list(carpeta.glob("*.csv"))

    if csvs:
        tabla = pd.read_csv(csvs[0], nrows=5)

        print("\nColumnas encontradas:")
        print(tabla.columns.tolist())

        print("\nPrimeros registros:")
        print(tabla.to_string(index=False))
    else:
        print("\nTodavía no se encontró ningún archivo CSV.")