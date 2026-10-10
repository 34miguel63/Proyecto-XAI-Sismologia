from pathlib import Path
import requests
import pandas as pd

# Catálogo oficial de terremotos del USGS
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

parametros = {
    "format": "geojson",
    "starttime": "2010-02-27T00:00:00",
    "endtime": "2010-02-28T00:00:00",
    "minmagnitude": 7.5,
    "orderby": "magnitude"
}

carpeta = Path("resultados")
carpeta.mkdir(parents=True, exist_ok=True)

try:
    print("Consultando el catálogo sísmico del USGS...")

    respuesta = requests.get(
        url,
        params=parametros,
        timeout=30
    )
    respuesta.raise_for_status()
    datos = respuesta.json()

    eventos = []

    for elemento in datos.get("features", []):
        propiedades = elemento["properties"]
        coordenadas = elemento["geometry"]["coordinates"]

        eventos.append({
            "id": elemento["id"],
            "fecha_utc": pd.to_datetime(
                propiedades["time"], unit="ms", utc=True
            ),
            "magnitud": propiedades["mag"],
            "lugar": propiedades["place"],
            "longitud": coordenadas[0],
            "latitud": coordenadas[1],
            "profundidad_km": coordenadas[2]
        })

    if eventos:
        tabla = pd.DataFrame(eventos)
        tabla = tabla.sort_values("fecha_utc")

        archivo = carpeta / "catalogo_eventos.csv"
        tabla.to_csv(archivo, index=False)

        print("\nEventos encontrados:", len(tabla))
        print(tabla.to_string(index=False))
        print("\nCatálogo guardado en:", archivo)
    else:
        print("No se encontraron eventos con esos criterios.")

except requests.RequestException as error:
    print("No se pudo consultar el catálogo.")
    print("Comprueba la conexión a Internet.")
    print("Detalle:", error)