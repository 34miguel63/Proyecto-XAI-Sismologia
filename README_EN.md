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
This project implements a **1D Convolutional Neural Network (CNN)** to classify seismic signals into two categories: **noise** and **seismic event**, combined with **Explainable AI (XAI)** techniques to interpret the model's decisions.

The system was validated with synthetic data and, notably, with a **real processed dataset from the Cuban seismic network (Station CW.QMBU)**, demonstrating the pipeline's applicability in a local context.

## 🎯 Objectives
- Generate synthetic signals based on a physically inspired computational model.
- Process and label real Cuban seismic signals (CW.QMBU) applying Data Augmentation.
- Implement and train a 1D CNN from scratch using PyTorch.
- Apply **Integrated Gradients** (via Captum) to explain the model's predictions.
- Provide a reproducible and documented pipeline for future work with CENAIS data.

## 🧠 Why a 1D CNN?
Seismic signals are **time series**. A 1D CNN is the natural architecture because:
1. **Preserves temporal structure:** Operates directly on the raw waveform, avoiding information loss from spectrogram transformations.
2. **Computational efficiency:** Requires fewer parameters and is faster to train.
3. **Interpretability:** XAI attributions on raw signals are more intuitive for seismologists.

*Based on:* "Seismic Signal Classification using One Dimension CNN..." (IEEE, 2025) and "Design of 1D CNN Kernels..." (NC State, 2024).

## 📊 Data Generation
### 1. Synthetic Data
1,000 signals (500 noise + 500 events) of 500 samples (5s at 100 Hz) were generated using a damped sinusoidal wave model.

### 2. Real Cuban Dataset (CW.QMBU)
A continuous signal from the CW.QMBU station was processed. An amplitude threshold was applied to identify 5-second windows containing real events (based on the local catalog), and **Data Augmentation** (temporal shifting and Gaussian noise) was applied to balance the dataset to 1,000 signals (500 real events + 500 real noise).

## 🔬 Explainability Method: Integrated Gradients
**Integrated Gradients (IG)** was selected because:
1. It satisfies the axioms of completeness and sensitivity [Sundararajan et al., 2017].
2. It is model-agnostic and does not require architectural changes.
3. It produces per-sample attributions, ideal for time series.

## 📈 Results

### Synthetic Dataset
| Metric | Precision | Recall | F1-Score |
|--------|-----------|--------|----------|
| **Accuracy** | | | **1.00** |

### Real Cuban Dataset (CW.QMBU)
| Metric | Precision | Recall | F1-Score |
|--------|-----------|--------|----------|
| **Accuracy** | | | **1.00** |

### Visualizations
![Cuban Dataset](resultados/dataset_cubano.png)
*Figure: Examples of processed real signals from the CW.QMBU station.*

![Cuban XAI Explanation](resultados/explicacion_cubana_integrated_gradients.png)
*Figure: Integrated Gradients attributions on a real Cuban event. Bottom: per-sample relevance (red = positive contribution to the "event" class).*

![Cuban Confusion Matrix](resultados/matriz_confusion_cubano.png)
*Figure: Confusion matrix on the Cuban dataset test set.*

## 💡 Contributions and Applications
- Complete and functional pipeline for seismic signal classification with XAI.
- Methodology successfully tested with **real data from a Cuban station**.
- Solid foundation for decision-support systems in seismological centers.

*⚠️ Note: This prototype is for academic purposes and should not be used as an operational early warning system.*

## 🚀 Installation and Execution

1. **Clone and enter:**
```bash
   git clone https://github.com/34miguel63/Proyecto-XAI-Sismologia.git
   cd Proyecto-XAI-Sismologia
```
2. **Virtual environment:**
```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or .\.venv\Scripts\Activate.ps1 (Windows)
```
3. **Dependencies:**
```bash
   pip install -r requirements.txt
```
4. **Workflow:**
```bash
   python generar_datos.py               # 1. Generate synthetic data
   python procesar_datos_cubanos.py      # 2. Process real Cuban dataset
   python entrenar_cnn.py                # 3. Train the CNN (uses Cuban data by default)
   python explicar_modelo_cubano.py      # 4. Apply XAI to the Cuban model
```

## 📁 Project Structure
```text
Proyecto XAI Sismologia/
├── README.md                              # Documentation in Spanish
├── README_EN.md                           # Documentation in English
├── paper.tex                              # Pre-paper in LaTeX
├── requirements.txt                       # Python dependencies
├── .gitignore                             # Files ignored by Git
├── generar_datos.py                       # Synthetic data generator
├── procesar_datos_cubanos.py              # Processing and augmentation of Cuban data
├── entrenar_cnn.py                        # 1D CNN training
├── explicar_modelo_cubano.py              # XAI application (Integrated Gradients)
├── datos/                                 # Generated data (ignored by Git)
├── modelos/                               # Trained models (.pth)
├── resultados/                            # Plots and metrics (.png, .npy)
└── docs/                                  # Additional documentation
```

## 🙏 Credits and Acknowledgments

### 🏛️ Seismic Data Source
The real data used in this project comes from the **National Seismological Research Center (CENAIS)** of Cuba, the country's official seismic monitoring institution.

### 👥 Academic Collaboration
We especially thank:

- **Madeley Graham León** (Universidad de Oriente - IPSJAM) for sharing the data files and the technical characterization document (`docs/Caracterizacion_Datos_CENAIS_v2.docx`).
- **Dr.C Dionis López Ramos** (Universidad de Oriente) for the academic supervision of the source work.
- **Dr. Bladimir Moreno Toirán** (CENAIS) for facilitating access to the seismic traces during the technical visit on March 4, 2026.

### 🌐 Reference Institutions
- **CENAIS** (Cuba): Official source of the real data.
- **USGS** (USA): Global reference catalog.
- **IRIS DMC** (International): Worldwide seismic data backup.

📄 See the complete data provenance document at: [`docs/DATOS_CREDITOS.md`](docs/DATOS_CREDITOS.md)