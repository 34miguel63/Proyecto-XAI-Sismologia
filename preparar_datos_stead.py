"""
Prepara una muestra de STEAD para el proyecto XAI de sismología.

Estructura esperada:
datos/
  stead/
    chunk1.csv
    chunk1.hdf5
    chunk2.csv
    chunk2.hdf5

Los nombres pueden variar, pero cada CSV debe tener un HDF5 con el mismo nombre base.
El script no descarga datos: procesa archivos STEAD que ya estén en datos/stead.
"""

from pathlib import Path
import random

import h5py
import numpy as np
import pandas as pd

CARPETA_STEAD = Path("datos/stead")
CARPETA_DATOS = Path("datos")
MUESTRAS_POR_CLASE = 500
LONGITUD = 500
SEMILLA = 42


def encontrar_hdf5(csv_path):
    """Busca el archivo HDF5 que comparte el nombre base del CSV."""
    for extension in (".hdf5", ".h5", ".hdf"):
        candidato = csv_path.with_suffix(extension)
        if candidato.exists():
            return candidato
    return None


def extraer_segmento(dataset, categoria, fila):
    """
    Extrae 500 muestras de la componente vertical (Z, índice 2).
    En eventos, intenta centrar la ventana cerca de la llegada de la onda P.
    En ruido, selecciona una ventana aleatoria.
    """
    datos = np.asarray(dataset)

    if datos.ndim != 2 or datos.shape[1] < 3:
        return None

    vertical = np.asarray(datos[:, 2], dtype=np.float32)
    if vertical.size == 0 or not np.all(np.isfinite(vertical)):
        return None

    if vertical.size >= LONGITUD:
        if categoria == "earthquake_local":
            p = fila.get("p_arrival_sample", np.nan)
            try:
                p = int(float(p))
            except (TypeError, ValueError, OverflowError):
                p = -1

            if 0 <= p < vertical.size:
                inicio = max(0, p - 200)
            else:
                inicio = random.randint(0, vertical.size - LONGITUD)

            inicio = min(inicio, vertical.size - LONGITUD)
        else:
            inicio = random.randint(0, vertical.size - LONGITUD)

        segmento = vertical[inicio:inicio + LONGITUD]
    else:
        segmento = np.pad(vertical, (0, LONGITUD - vertical.size))

    # Normalización por amplitud máxima absoluta.
    maximo = np.max(np.abs(segmento))
    if maximo > 0:
        segmento = segmento / maximo

    return segmento.astype(np.float32)


def main():
    random.seed(SEMILLA)
    np.random.seed(SEMILLA)

    if not CARPETA_STEAD.exists():
        print(f"No existe la carpeta: {CARPETA_STEAD.resolve()}")
        print("Crea datos/stead y coloca allí los CSV y HDF5 de STEAD.")
        return

    csvs = sorted(CARPETA_STEAD.glob("*.csv"))
    if not csvs:
        print(f"No se encontraron archivos CSV en {CARPETA_STEAD.resolve()}")
        print("Todavía no se han descargado/copiadolos metadatos de STEAD.")
        return

    señales = []
    etiquetas = []
    conteo = {"noise": 0, "earthquake_local": 0}
    usados = set()

    for csv_path in csvs:
        hdf5_path = encontrar_hdf5(csv_path)
        if hdf5_path is None:
            print(f"AVISO: no encontré el HDF5 correspondiente a {csv_path.name}; se omite.")
            continue

        print(f"\nLeyendo metadatos: {csv_path.name}")
        tabla = pd.read_csv(csv_path, low_memory=False)

        columnas_necesarias = {"trace_name", "trace_category"}
        if not columnas_necesarias.issubset(tabla.columns):
            print(f"AVISO: {csv_path.name} no contiene trace_name y trace_category.")
            continue

        tabla = tabla[tabla["trace_category"].isin(["noise", "earthquake_local"])]
        tabla = tabla.sample(frac=1, random_state=SEMILLA).reset_index(drop=True)

        print(f"Abriendo señales: {hdf5_path.name}")
        with h5py.File(hdf5_path, "r") as archivo:
            if "data" not in archivo:
                print(f"AVISO: {hdf5_path.name} no contiene el grupo 'data'.")
                continue

            grupo = archivo["data"]

            for _, fila in tabla.iterrows():
                categoria = str(fila["trace_category"])
                if conteo[categoria] >= MUESTRAS_POR_CLASE:
                    continue

                nombre = str(fila["trace_name"])
                clave = (str(hdf5_path.resolve()), nombre)
                if clave in usados:
                    continue

                ruta_dataset = f"data/{nombre}"
                if ruta_dataset not in archivo:
                    continue

                try:
                    segmento = extraer_segmento(archivo[ruta_dataset], categoria, fila)
                except (OSError, ValueError, TypeError, KeyError):
                    continue

                if segmento is None:
                    continue

                señales.append(segmento)
                etiquetas.append(0 if categoria == "noise" else 1)
                conteo[categoria] += 1
                usados.add(clave)

                if all(conteo[c] >= MUESTRAS_POR_CLASE for c in conteo):
                    break

        print(f"  Ruido: {conteo['noise']}/{MUESTRAS_POR_CLASE}")
        print(f"  Eventos: {conteo['earthquake_local']}/{MUESTRAS_POR_CLASE}")

        if all(conteo[c] >= MUESTRAS_POR_CLASE for c in conteo):
            break

    if conteo["noise"] == 0 or conteo["earthquake_local"] == 0:
        print("\nNo se pudo preparar una muestra de ambas clases.")
        print("Comprueba que tengas un CSV/HDF5 de ruido y otro de terremotos.")
        print("En STEAD, el campo trace_category suele usar 'noise' y 'earthquake_local'.")
        return

    if conteo["noise"] < MUESTRAS_POR_CLASE or conteo["earthquake_local"] < MUESTRAS_POR_CLASE:
        print("\nAVISO: se preparará una muestra más pequeña porque faltan registros.")

    CARPETA_DATOS.mkdir(parents=True, exist_ok=True)
    X = np.stack(señales).astype(np.float32)
    y = np.asarray(etiquetas, dtype=np.int64)

    # Mezclar las clases para que no queden agrupadas por orden de lectura.
    orden = np.random.permutation(len(y))
    X = X[orden]
    y = y[orden]

    np.save(CARPETA_DATOS / "senales.npy", X)
    np.save(CARPETA_DATOS / "etiquetas.npy", y)

    print("\n¡Preparación terminada!")
    print("Forma de las señales:", X.shape)
    print("Forma de las etiquetas:", y.shape)
    print("Ruido (etiqueta 0):", int(np.sum(y == 0)))
    print("Evento sísmico local (etiqueta 1):", int(np.sum(y == 1)))
    print("Guardado en datos/senales.npy y datos/etiquetas.npy")
    print("\nNOTA: las señales se han recortado a 500 muestras de la componente Z.")
    print("Antes de entrenar, revisa que entrenar_cnn.py cargue estos dos archivos.")


if __name__ == "__main__":
    main()
