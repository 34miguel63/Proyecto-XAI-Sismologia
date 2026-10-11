import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn

from pathlib import Path
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# 1. Configurar el experimento
torch.manual_seed(42)
np.random.seed(42)

dispositivo = torch.device("cpu")
print("Dispositivo:", dispositivo)

# 2. Cargar las señales REALES (dataset CENAIS/Caribe)
print("\n📂 Cargando dataset REAL (CENAIS/Caribe)...")
X = np.load("datos/senales_reales.npy")
y = np.load("datos/etiquetas_reales.npy")

print(f"   - Señales cargadas: {X.shape}")
print(f"   - Etiquetas cargadas: {y.shape}")
print(f"   - Distribución: {np.sum(y==0)} Ruido, {np.sum(y==1)} Evento Real")

# CNN 1D espera: muestras, canales, longitud
X = X[:, np.newaxis, :]

# 3. Separar entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"   - Train: {len(X_train)} señales | Test: {len(X_test)} señales")

# 4. Convertir los datos a tensores de PyTorch
X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.long)
y_test = torch.tensor(y_test, dtype=torch.long)

datos_train = TensorDataset(X_train, y_train)

cargador = DataLoader(
    datos_train,
    batch_size=32,
    shuffle=True
)

# 5. Definir la arquitectura de la CNN 1D
class CNN1D(nn.Module):
    def __init__(self):
        super().__init__()

        self.capas = nn.Sequential(
            nn.Conv1d(1, 16, kernel_size=7, padding=3),
            nn.ReLU(),
            nn.MaxPool1d(2),

            nn.Conv1d(16, 32, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.MaxPool1d(2),

            nn.AdaptiveAvgPool1d(1),
            nn.Flatten(),
            nn.Linear(32, 2)
        )

    def forward(self, x):
        return self.capas(x)


modelo = CNN1D().to(dispositivo)

# 6. Configurar entrenamiento
funcion_perdida = nn.CrossEntropyLoss()

optimizador = torch.optim.Adam(
    modelo.parameters(),
    lr=0.001
)

# 7. Entrenar la red neuronal
epocas = 20  # Aumentamos a 20 épocas para datos reales (más difíciles)

print(f"\n🚀 Iniciando entrenamiento con {epocas} épocas...")
for epoca in range(epocas):
    modelo.train()
    perdida_total = 0.0

    for senales, etiquetas in cargador:
        senales = senales.to(dispositivo)
        etiquetas = etiquetas.to(dispositivo)

        optimizador.zero_grad()

        salidas = modelo(senales)
        perdida = funcion_perdida(salidas, etiquetas)

        perdida.backward()
        optimizador.step()

        perdida_total += perdida.item()

    promedio = perdida_total / len(cargador)

    print(
        f"Época {epoca + 1}/{epocas} "
        f"- Pérdida: {promedio:.4f}"
    )

# 8. Evaluar en los datos de prueba
modelo.eval()

with torch.no_grad():
    salidas = modelo(X_test)
    probabilidades = torch.softmax(salidas, dim=1)
    predicciones = torch.argmax(salidas, dim=1).numpy()

y_real = y_test.numpy()

exactitud = accuracy_score(y_real, predicciones)

print("\n" + "="*50)
print("📊 RESULTADOS DE LA CNN (DATOS REALES)")
print("="*50)
print(f"Exactitud (accuracy): {exactitud:.4f}")

print("\nInforme de clasificación:")
print(
    classification_report(
        y_real,
        predicciones,
        labels=[0, 1],
        target_names=["Ruido Real", "Evento Real"],
        zero_division=0
    )
)

# 9. Mostrar matriz de confusión
matriz = confusion_matrix(
    y_real,
    predicciones,
    labels=[0, 1]
)

visualizador = ConfusionMatrixDisplay(
    confusion_matrix=matriz,
    display_labels=["Ruido Real", "Evento Real"]
)

visualizador.plot(cmap="Blues")
plt.title("Matriz de confusión - CNN 1D (Datos Reales CENAIS)")
plt.tight_layout()

# 10. Guardar modelo y resultados
carpeta = Path("modelos")
carpeta.mkdir(exist_ok=True)

torch.save(
    modelo.state_dict(),
    carpeta / "cnn_sismica_REAL.pth"
)

carpeta_resultados = Path("resultados")
carpeta_resultados.mkdir(exist_ok=True)

np.save(
    carpeta_resultados / "y_real_reales.npy",
    y_real
)

np.save(
    carpeta_resultados / "predicciones_reales.npy",
    predicciones
)

np.save(
    carpeta_resultados / "probabilidades_reales.npy",
    probabilidades.numpy()
)

plt.savefig(
    carpeta_resultados / "matriz_confusion_real.png",
    dpi=150
)

print("\n✅ Modelo guardado en modelos/cnn_sismica_REAL.pth")
print("✅ Resultados guardados en la carpeta resultados.")

plt.show()