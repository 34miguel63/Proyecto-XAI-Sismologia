# 🌍 XAI Seismology Project — 1D CNN with Explainable Artificial Intelligence

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

> **Team 6** | Advanced Artificial Intelligence | University of Informatics Sciences (UCI), Cuba

## 👥 Team Members

- **Addel Vidal García**
- **Alejandro Colón Álvarez**
- **Miguel Ángel Banteurt Blanco**

## 📋 Description

This project implements a **1D Convolutional Neural Network (CNN)** to classify seismic signals into two categories: **noise** and **seismic event**, combined with **Explainable AI (XAI)** techniques to interpret model decisions.

The system was validated on both synthetic data (generated through a computational model based on damped sinusoidal waves) and real data downloaded from the global FDSN network (station IU.ANMO).

##  Objectives

### General Objective
Apply an XAI method to interpret the predictions of a machine learning model designed to classify seismic signals.

### Specific Objectives
- Generate synthetic signals based on a physically-inspired computational model.
- Implement and train a 1D CNN from scratch using PyTorch.
- Apply **Integrated Gradients** (via Captum) to explain predictions.
- Download and process real seismic data from the FDSN network.
- Compare performance between synthetic and real data.
- Provide a reproducible pipeline for future extensions with CENAIS data.

## 🧠 Why a 1D CNN?

Seismic signals are **time series** representing ground amplitude evolution over time. A 1D CNN is the natural architecture for this type of data because:

1. **Preserves temporal structure:** Unlike 2D CNNs (which require transforming the signal into spectrograms), the 1D CNN operates directly on the waveform, avoiding information loss.
2. **Computational efficiency:** Requires fewer parameters and is faster to train than 2D or Transformer-based architectures.
3. **Interpretability:** XAI attributions on raw signals are more intuitive for seismologists.

This decision is based on recent works such as:
- *"Seismic Signal Classification using One Dimension CNN and Transformer Encoder"* (IEEE, 2025)
- *"Design of 1D CNN Kernels for Predicting Seismic Response of Nuclear Power Plants"* (NC State, 2024)

**Note:** The model was implemented from scratch by the team. No pre-trained network was used.

## 📊 Synthetic Data Generation

Synthetic data was generated using a **computational model** inspired by the physics of seismic waves:

$$x(t) = A(t) \left[ \sin(2\pi f_1 t) + \alpha \sin(2\pi f_2 t) \right] + \epsilon(t)$$

Where:
- $A(t) = A_0 e^{-\beta t}$ is a temporal envelope simulating amplitude attenuation.
- $f_1 = 5$ Hz and $f_2 = 9$ Hz are dominant frequencies typical of local seismic events.
- $\alpha = 0.5$ is a weighting factor.
- $\epsilon(t) \sim \mathcal{N}(0, 0.25)$ represents background noise.

A total of **1,000 signals** (500 noise + 500 events) were generated, each with 500 samples (5 seconds at 100 Hz), individually normalized to the range $[-1, 1]$.

## 🔬 Explainability Method: Integrated Gradients

**Integrated Gradients (IG)** was selected as the XAI method for the following reasons:

1. **Axiomatic foundation:** Satisfies completeness and sensitivity axioms [Sundararajan et al., 2017].
2. **Model-agnostic:** Works with any differentiable network without modifying its architecture.
3. **Temporal interpretability:** Produces per-sample attributions, ideal for time series.
4. **Mature implementation:** Available in the Captum library for PyTorch.

The method computes attributions by integrating gradients along a path from a baseline (zero signal) to the input:

$$\text{IG}(x) = (x - x') \times \int_{\alpha=0}^{1} \frac{\partial F(x' + \alpha(x - x'))}{\partial x} d\alpha$$

In practice, the integral is approximated with $n = 100$ steps.

**Main reference:** Sundararajan, M., Taly, A., & Yan, Q. (2017). *Axiomatic Attribution for Deep Networks*. ICML 2017.

## 📈 Results

### Synthetic Data

| Metric | Precision | Recall | F1-Score | Support |
|--------|-----------|--------|----------|---------|
| Noise | 1.00 | 1.00 | 1.00 | 100 |
| Synthetic Event | 1.00 | 1.00 | 1.00 | 100 |
| **Accuracy** | | | **1.00** | 200 |

### Real Data (FDSN - IU.ANMO)

| Metric | Precision | Recall | F1-Score | Support |
|--------|-----------|--------|----------|---------|
| Real Noise | 0.88 | 0.87 | 0.87 | 100 |
| Real Event | 0.87 | 0.88 | 0.88 | 100 |
| **Accuracy** | | | **0.875** | 200 |

The 12.5% reduction when moving from synthetic to real data is expected and documented in the literature, justifying the use of XAI to understand model limitations.

### XAI Visualization

![XAI Explanation](resultados/explicacion_integrated_gradients.png)

*Figure: Integrated Gradients attributions on a correctly classified synthetic event. Top: input signal. Bottom: per-sample relevance (red = positive contribution to the "event" class).*

![Confusion Matrix](resultados/matriz_confusion.png)

*Figure: Confusion matrix on the synthetic test set.*

## 💡 Contributions and Applications

### Current Contributions
- Complete implementation of a 1D CNN for seismic signal classification.
- Application of Integrated Gradients to explain predictions on time series.
- Reproducible pipeline for FDSN data download and processing.
- Methodological foundation for future validation with CENAIS data.

### Future Applications
- Automatic seismic event detection system.
- Support tool for seismologists in catalog review.
- Comparative study of XAI methods on geophysical signals.
- Integration with real-time monitoring networks.

**⚠️ Note:** This prototype should not be used as an operational early warning system or as a substitute for official seismological services.

## 🚀 Installation and Execution

### Requirements
- Python 3.12+
- PowerShell (Windows) or Bash (Linux/Mac)

### Steps

1. **Clone the repository:**
```bash
   git clone https://github.com/[username]/Proyecto-XAI-Sismologia.git
   cd Proyecto-XAI-Sismologia
```

2. **Create and activate virtual environment:**
```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1  # Windows
   source .venv/bin/activate     # Linux/Mac
```

3. **Install dependencies:**
```bash
   pip install -r requirements.txt
```

4. **Generate synthetic data:**
```bash
   python generar_datos.py
```

5. **Train the CNN:**
```bash
   python entrenar_cnn.py
```

6. **Apply XAI:**
```bash
   python explicar_modelo.py
```

7. **Generate real dataset:**
```bash
   python preparar_dataset_real_final.py
```

8. **Train with real data:**
```bash
   python entrenar_cnn.py  # (already modified to use senales_reales.npy)
```

## 📁 Project Structure
Proyecto XAI Sismologia/
├── README.md                              # Documentation in Spanish
├── README_EN.md                           # Documentation in English
├── paper.tex                              # Pre-paper in LaTeX
├── requirements.txt                       # Python dependencies
├── .gitignore                             # Files ignored by Git
├── generar_datos.py                       # Synthetic data generator
├── entrenar_cnn.py                        # 1D CNN training
── explicar_modelo.py                     # XAI application (Integrated Gradients)
├── preparar_dataset_real.py               # Real data download and preparation
├── preparar_datos_stead.py                # STEAD dataset preparation (future)
├── descargar_senal_real.py                # Download real signal from FDSN
├── descargar_senal_evento.py              # Download specific event signal
├── analizar_senal_real.py                 # Analysis and visualization of real signal
├── analizar_evento_real.py                # Analysis of real seismic event
├── consultar_catalogo.py                  # USGS catalog query
├── comprobar_entorno.py                   # Development environment verification
├── inspeccionar_stead.py                  # STEAD dataset inspection
├── datos/                                 # Generated data (not committed to Git)
│   ├── senales.npy                        # Synthetic signals (1000 x 500)
│   ├── senales_reales.npy                 # Real signals (1000 x 500)
│   └── etiquetas.npy                      # Signal labels
├── modelos/                               # Trained models
│   ├── cnn_sismica.pth                    # Model trained with synthetic data
│   └── cnn_sismica_REAL.pth               # Model trained with real data
├── resultados/                            # Plots and metrics
│   ├── matriz_confusion.png               # Confusion matrix (synthetic data)
│   ├── matriz_confusion_real.png          # Confusion matrix (real data)
│   ├── explicacion_integrated_gradients.png  # XAI visualization
│   ├── dataset_real_ejemplos.png          # Real dataset examples
│   ├── y_real.npy                         # Real test labels
│   ├── predicciones.npy                   # Model predictions
│   └── probabilidades.npy                 # Model probabilities
── docs/                                  # Additional documentation
└── informe_metodologico.md            # Detailed methodological report

## 📚 References

1. Sundararajan, M., Taly, A., & Yan, Q. (2017). *Axiomatic Attribution for Deep Networks*. ICML 2017.
2. Mousavi, S.M. et al. (2019). *STEAD: A Global Data Set of Seismic Signals for AI*. IEEE Access.
3. IEEE (2024). *Various Signal Transformation for Optimizing CNN Model Performance of Earthquake Detection*.
4. IEEE (2025). *Seismic Signal Classification using One Dimension CNN and Transformer Encoder*.
5. ScienceDirect (2025). *Enhancing seismic signal quality assessment with CNNs: A focus on effective data augmentation techniques*.
6. Captum Documentation: https://captum.ai/
7. ObsPy Documentation: https://docs.obspy.org/
8. USGS Earthquake Catalog: https://earthquake.usgs.gov/

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🙏 Acknowledgments

- National Seismological Research Center (CENAIS), Cuba.
- United States Geological Survey (USGS).
- FDSN (Federated Digital Seismograph Networks).