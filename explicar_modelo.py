import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn

from pathlib import Path
from sklearn.model_selection import train_test_split
from captum.attr import IntegratedGradients

# 1. Configuracion
torch.manual_seed(42)
dispositivo = torch.device("cpu")

# 2. Definir la misma arquitectura utilizada al entrenar
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


# 3. Cargar el modelo entrenado
modelo = CNN1D().to(dispositivo)

modelo.load_state_dict(
    torch.load(
        "modelos/cnn_sismica.pth",
        map_location=dispositivo,
        weights_only=True
    )
)

modelo.eval()

# 4. Cargar los datos y recuperar la particion de prueba
X = np.load("datos/senales.npy")
y = np.load("datos/etiquetas.npy")

indices = np.arange(len(y))

_, indices_test = train_test_split(
    indices,
    test_size=0.20,
    random_state=42,
    stratify=y
)

X_test = X[indices_test]
y_test = y[indices_test]

# 5. Buscar un evento sintetico correctamente clasificado
with torch.no_grad():
    entradas = torch.tensor(
        X_test[:, np.newaxis, :],
        dtype=torch.float32
    )

    salidas = modelo(entradas)
    predicciones = salidas.argmax(dim=1).numpy()

candidatos = np.where(
    (y_test == 1) & (predicciones == 1)
)[0]

if len(candidatos) == 0:
    raise RuntimeError(
        "No se encontro un evento correctamente clasificado."
    )

indice = int(candidatos[0])

senal = torch.tensor(
    X_test[indice:indice + 1, np.newaxis, :],
    dtype=torch.float32,
    requires_grad=True
)

# 6. Aplicar Integrated Gradients
xai = IntegratedGradients(modelo)

atribuciones, diferencia = xai.attribute(
    senal,
    baselines=torch.zeros_like(senal),
    target=1,
    n_steps=100,
    return_convergence_delta=True
)

senal_np = senal.detach().numpy()[0, 0]
relevancia = atribuciones.detach().numpy()[0, 0]

# 7. Mostrar la prediccion y sus probabilidades
with torch.no_grad():
    probabilidades = torch.softmax(
        modelo(senal), dim=1
    )[0].numpy()

print("Clase real: evento sintetico")
print("Clase predicha: evento sintetico")
print(f"Probabilidad de ruido: {probabilidades[0]:.4f}")
print(
    "Probabilidad de evento sintetico: "
    f"{probabilidades[1]:.4f}"
)
print(
    "Diferencia de convergencia IG: "
    f"{diferencia.item():.6f}"
)

# 8. Graficar la señal y su explicacion
tiempo = np.arange(len(senal_np)) / 100

fig, ejes = plt.subplots(
    2, 1, figsize=(12, 7), sharex=True
)

ejes[0].plot(tiempo, senal_np)
ejes[0].set_title("Senal analizada por la CNN 1D")
ejes[0].set_ylabel("Amplitud")
ejes[0].grid(True, alpha=0.3)

ejes[1].plot(tiempo, relevancia)
ejes[1].axhline(0, color="black", linewidth=0.8)
ejes[1].set_title(
    "XAI: atribuciones de Integrated Gradients"
)
ejes[1].set_xlabel("Tiempo (s)")
ejes[1].set_ylabel("Relevancia")
ejes[1].grid(True, alpha=0.3)

plt.tight_layout()

carpeta = Path("resultados")
carpeta.mkdir(exist_ok=True)

plt.savefig(
    carpeta / "explicacion_integrated_gradients.png",
    dpi=150
)

print(
    "Grafico guardado en "
    "resultados/explicacion_integrated_gradients.png"
)

plt.show()