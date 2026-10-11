"""
Genera un dataset realista basado en el catálogo de sismos cubanos (sismos.csv)
y los patrones de radiación (nohitexp.csv).
Cada señal sintética tiene parámetros físicos coherentes con magnitud y profundidad.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ==============================================================================
# 1. CONFIGURACIÓN
# ==============================================================================
fs = 100           # Frecuencia de muestreo (Hz)
ventana = 500      # 5 segundos por ventana
objetivo = 1000    # Total de señales (500 eventos + 500 ruido)

np.random.seed(42)

# ==============================================================================
# 2. CARGAR CATÁLOGO DE SISMOS CUBANOS
# ==============================================================================
print(" Cargando catálogo de sismos cubanos...")

df_sismos = pd.read_csv("datos/crudos/sismos.csv")
print(f"   ✅ Catálogo cargado: {len(df_sismos)} sismos reales")
print(df_sismos)

# ==============================================================================
# 3. CARGAR PATRONES DE RADIACIÓN (nohitexp.csv)
# ==============================================================================
print("\n📡 Cargando patrones de radiación sísmica...")

patrones_radiacion = []
with open("datos/crudos/nohitexp.csv", 'r') as f:
    for linea in f:
        linea = linea.strip()
        if linea:
            partes = linea.split()
            if len(partes) >= 3:
                try:
                    azimut = float(partes[0])
                    inclinacion = float(partes[1])
                    amplitud = float(partes[2])
                    patrones_radiacion.append((azimut, inclinacion, amplitud))
                except ValueError:
                    continue

print(f"   ✅ Patrones de radiación cargados: {len(patrones_radiacion)}")

# ==============================================================================
# 4. FUNCIÓN PARA GENERAR SEÑAL SÍSMICA REALISTA
# ==============================================================================
def generar_sismo_realista(magnitud, profundidad, patron_radiacion=None):
    """
    Genera una señal sísmica realista basada en magnitud y profundidad.
    Simula ondas P y S con parámetros físicos coherentes.
    """
    t = np.arange(ventana) / fs
    
    # Amplitud base escala con magnitud (escala logarítmica)
    amplitud_base = 10 ** (magnitud - 3)  # M3.0 = 1.0, M4.0 = 10.0, M5.0 = 100.0
    
    # Frecuencias dominantes (ondas P: alta freq, ondas S: baja freq)
    # La profundidad afecta la atenuación
    factor_atenuacion = np.exp(-profundidad / 50.0)  # Mayor profundidad = más atenuación
    
    # Onda P (llega primero, alta frecuencia ~8-12 Hz)
    freq_p = np.random.uniform(8, 12)
    inicio_p = np.random.randint(80, 150)  # Entre 0.8s y 1.5s
    duracion_p = np.random.randint(50, 100)
    t_p = np.arange(duracion_p) / fs
    envolvente_p = np.exp(-4.0 * t_p) * factor_atenuacion
    onda_p = np.sin(2 * np.pi * freq_p * t_p) * envolvente_p
    
    # Onda S (llega después, baja frecuencia ~3-6 Hz, mayor amplitud)
    freq_s = np.random.uniform(3, 6)
    inicio_s = inicio_p + np.random.randint(40, 80)  # Retardo P-S
    duracion_s = np.random.randint(100, 200)
    t_s = np.arange(duracion_s) / fs
    envolvente_s = np.exp(-2.5 * t_s) * factor_atenuacion
    onda_s = np.sin(2 * np.pi * freq_s * t_s) * envolvente_s
    
    # Construir señal
    senal = np.random.normal(0, 0.05, ventana)  # Ruido de fondo
    
    # Insertar onda P
    if inicio_p + duracion_p <= ventana:
        factor_amp = amplitud_base * 0.3  # Onda P tiene ~30% de la amplitud total
        if patron_radiacion:
            factor_amp *= (1.0 + patron_radiacion * 0.5)  # Modulación direccional
        senal[inicio_p:inicio_p+duracion_p] += factor_amp * onda_p
    
    # Insertar onda S
    if inicio_s + duracion_s <= ventana:
        factor_amp = amplitud_base * 1.0  # Onda S tiene amplitud completa
        if patron_radiacion:
            factor_amp *= (1.0 + patron_radiacion * 0.5)
        senal[inicio_s:inicio_s+duracion_s] += factor_amp * onda_s
    
    # Normalizar
    maximo = np.max(np.abs(senal))
    if maximo > 0:
        senal = senal / maximo
    
    return senal

def generar_ruido_realista():
    """Genera ruido sísmico realista (ruido cultural + microtemblores)."""
    senal = np.random.normal(0, 0.15, ventana)
    
    # Añadir ruido cultural (tráfico, viento, actividad humana)
    ruido_cultural = np.random.normal(0, 0.05, ventana)
    senal += ruido_cultural
    
    # Añadir microtemblores aleatorios (pequeñas oscilaciones)
    if np.random.random() < 0.3:  # 30% de probabilidad
        freq_micro = np.random.uniform(1, 3)
        t_micro = np.arange(ventana) / fs
        micro = np.sin(2 * np.pi * freq_micro * t_micro) * np.exp(-0.5 * t_micro)
        senal += 0.1 * micro
    
    # Normalizar
    maximo = np.max(np.abs(senal))
    if maximo > 0:
        senal = senal / maximo
    
    return senal

# ==============================================================================
# 5. GENERAR DATASET
# ==============================================================================
print(f"\n🔨 Generando dataset realista ({objetivo} señales)...")

X_cubano = []
y_cubano = []

# Generar eventos basados en el catálogo real
muestras_por_sismo = objetivo // (2 * len(df_sismos))  # Distribuir equitativamente

for idx, sismo in df_sismos.iterrows():
    magnitud = sismo['magnitud']
    profundidad = sismo['profundidad']
    estacion = sismo['estacion']
    
    print(f"   🌍 Generando eventos para sismo M{magnitud} en {estacion}...")
    
    for _ in range(muestras_por_sismo):
        # Seleccionar patrón de radiación aleatorio
        if patrones_radiacion:
            azimut, inclinacion, amp_rad = patrones_radiacion[np.random.randint(len(patrones_radiacion))]
            # Normalizar amplitud de radiación a [-1, 1]
            patron_norm = (amp_rad - 5.0) / 10.0  # Asumiendo rango típico 0-10
            patron_norm = np.clip(patron_norm, -1, 1)
        else:
            patron_norm = 0.0
        
        senal = generar_sismo_realista(magnitud, profundidad, patron_norm)
        X_cubano.append(senal)
        y_cubano.append(1)

# Completar con más eventos si es necesario
while len(X_cubano) < objetivo // 2:
    sismo_aleatorio = df_sismos.iloc[np.random.randint(len(df_sismos))]
    if patrones_radiacion:
        azimut, inclinacion, amp_rad = patrones_radiacion[np.random.randint(len(patrones_radiacion))]
        patron_norm = np.clip((amp_rad - 5.0) / 10.0, -1, 1)
    else:
        patron_norm = 0.0
    
    senal = generar_sismo_realista(sismo_aleatorio['magnitud'], sismo_aleatorio['profundidad'], patron_norm)
    X_cubano.append(senal)
    y_cubano.append(1)

# Generar ruidos
print(f"   🔇 Generando ruido de fondo...")
while len(X_cubano) < objetivo:
    senal = generar_ruido_realista()
    X_cubano.append(senal)
    y_cubano.append(0)

# Convertir a arrays
X_cubano = np.array(X_cubano[:objetivo], dtype=np.float32)
y_cubano = np.array(y_cubano[:objetivo], dtype=np.int64)

# Balancear exactamente
n_eventos = np.sum(y_cubano == 1)
n_ruido = np.sum(y_cubano == 0)
print(f"\n Dataset generado:")
print(f"   - Total: {len(X_cubano)} señales")
print(f"   - Eventos: {n_eventos}")
print(f"   - Ruido: {n_ruido}")

# ==============================================================================
# 6. GUARDAR
# ==============================================================================
carpeta = Path("datos")
carpeta.mkdir(exist_ok=True)

np.save(carpeta / "senales_cubanas.npy", X_cubano)
np.save(carpeta / "etiquetas_cubanas.npy", y_cubano)

print(f"\n✅ Guardado en:")
print(f"   - datos/senales_cubanas.npy")
print(f"   - datos/etiquetas_cubanas.npy")

# ==============================================================================
# 7. VISUALIZAR
# ==============================================================================
fig, ejes = plt.subplots(2, 2, figsize=(14, 8))

# Distribución de magnitudes del catálogo
ejes[0,0].bar(range(len(df_sismos)), df_sismos['magnitud'], color='red', alpha=0.7)
ejes[0,0].set_title("Magnitudes del catálogo de sismos cubanos")
ejes[0,0].set_xlabel("Índice del sismo")
ejes[0,0].set_ylabel("Magnitud")
ejes[0,0].grid(True, alpha=0.3)

# Distribución de amplitudes del dataset
amplitudes_max = np.max(np.abs(X_cubano), axis=1)
ejes[0,1].hist(amplitudes_max, bins=50, color='blue', alpha=0.7)
ejes[0,1].set_title("Distribución de amplitudes máximas")
ejes[0,1].set_xlabel("Amplitud máxima")
ejes[0,1].set_ylabel("Frecuencia")
ejes[0,1].grid(True, alpha=0.3)

# Ejemplo de evento
idx_ev = np.where(y_cubano == 1)[0][0]
tiempo = np.arange(ventana) / fs
ejes[1,0].plot(tiempo, X_cubano[idx_ev], color='red', linewidth=0.8)
ejes[1,0].set_title(f"Ejemplo de EVENTO realista (M{df_sismos.iloc[0]['magnitud']})")
ejes[1,0].set_xlabel("Tiempo (s)")
ejes[1,0].set_ylabel("Amplitud normalizada")
ejes[1,0].grid(True, alpha=0.3)

# Ejemplo de ruido
idx_ru = np.where(y_cubano == 0)[0][0]
ejes[1,1].plot(tiempo, X_cubano[idx_ru], color='blue', linewidth=0.8)
ejes[1,1].set_title("Ejemplo de RUIDO realista")
ejes[1,1].set_xlabel("Tiempo (s)")
ejes[1,1].set_ylabel("Amplitud normalizada")
ejes[1,1].grid(True, alpha=0.3)

plt.tight_layout()

carpeta_res = Path("resultados")
carpeta_res.mkdir(exist_ok=True)
plt.savefig(carpeta_res / "dataset_cubano.png", dpi=150)
plt.show()

print("\n🎉 ¡Dataset cubano realista listo! Ahora puedes entrenar la CNN.")