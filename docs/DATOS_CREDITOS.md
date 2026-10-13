# 📋 Créditos y Procedencia de los Datos Sísmicos

Este documento detalla la procedencia de los datos sísmicos utilizados en este proyecto, 
garantizando la transparencia y reproducibilidad de la investigación.

## 🏛️ Fuente Oficial de los Datos

**Institución:** Centro Nacional de Investigaciones Sismológicas (CENAIS), Cuba  
**Sitio web:** https://www.cenais.gob.cu  
**Tipo de organización:** Institución científica nacional, adscrita al CITMA (Ministerio de Ciencia, Tecnología y Medio Ambiente de Cuba)

## 👥 Colaboración Académica

Los datos fueron obtenidos en el marco de una colaboración académica entre:

### Universidad de Oriente (UO) - IPSJAM
- **Investigadora principal:** Madeley Graham León
- **Supervisor:** Dr.C Dionis López Ramos
- **Proyecto:** Trabajo de Diploma sobre Deep Learning con XAI para detección de onda P
- **Fecha de adquisición:** Marzo 2026

### CENAIS - Contacto Técnico
- **Especialista:** Dr. Bladimir Moreno Toirán
- **Fecha de visita técnica:** 4 de marzo de 2026
- **Acuerdo:** Suministro de trazas sísmicas de estaciones cubanas para investigación académica

## 📡 Datos Específicos Utilizados

### Estación Principal del Proyecto
| Parámetro | Valor |
|-----------|-------|
| **Código de estación** | CW.QMBU (también CW.RCC.00.HHZ) |
| **Nombre** | Estación Sísmica QMBU / Río Carpintero |
| **Ubicación** | Santiago de Cuba, Cuba |
| **Red** | CW — Red sísmica nacional de Cuba (CENAIS) |
| **Canal** | HH* (High Broadband) - Componentes HHN, HHE, HHZ |
| **Frecuencia de muestreo** | 100 Hz |
| **Formato** | SAC / CSV (compatible con ObsPy) |
| **Sensor** | Trillium Compact (alta sensibilidad) |

### Dataset Cubano Procesado
- **Archivo fuente:** `categoria_sismos.csv` (7,792,650 muestras ≈ 21.6 horas de señal continua)
- **Catálogo de eventos:** `sismos.csv` (6 eventos verificados, magnitudes 3.5 a 4.2, año 2023)
- **Patrones de radiación:** `nohitexp.csv` (distribución direccional de energía sísmica)

## 🔗 Trazabilidad de los Datos

1. **Adquisición original:** Los datos crudos fueron capturados por la red de estaciones del CENAIS 
   que monitorea continuamente la actividad sísmica en Cuba.
2. **Respaldo internacional:** Toda la información se respalda automáticamente en el centro 
   internacional de datos sísmicos **IRIS DMC** (Incorporated Research Institutions for Seismology).
3. **Transferencia académica:** El CENAIS suministró las trazas a la Universidad de Oriente 
   para el trabajo de diploma de Madeley Graham León.
4. **Uso en este proyecto:** Los archivos fueron compartidos dentro del contexto académico 
   de la asignatura "Inteligencia Artificial Avanzada" de la Universidad de las Ciencias 
   Informáticas (UCI), con fines de investigación y reproducción metodológica.

## 📜 Documentación Complementaria

El análisis técnico completo de los datos del CENAIS se encuentra en el documento:

📄 **`Caracterizacion_Datos_CENAIS_v2.docx`**

Elaborado por:
- **Autora:** Madeley Graham León
- **Institución:** Universidad de Oriente (IPSJAM) · CENAIS Cuba
- **Fecha:** Marzo 2026
- **Supervisión:** Dr.C Dionis López Ramos

Este documento incluye:
- Caracterización técnica del vector de medición (timestamp, HHN, HHE, HHZ)
- Análisis de ondas P y S
- Comparación con datasets benchmark (STEAD, INSTANCE, DiTing, TXED)
- Evaluación de modelos implementables (PhaseNet, EQTransformer, EQCCT)
- Volúmenes de datos de la red CENAIS

## ⚖️ Licencia y Uso

Los datos son utilizados bajo los siguientes principios:
- ✅ **Fines académicos y de investigación exclusivamente**
- ✅ **Reconocimiento explícito de la fuente (CENAIS)**
- ✅ **No商业用途 (no uso comercial)**
- ✅ **Atribución a los colaboradores (UO, CENAIS)**

El código fuente de este proyecto está bajo licencia MIT, pero los datos sísmicos 
permanecen bajo la custodia y regulación del CENAIS.

## 📞 Contacto para Verificación

Para validar la procedencia de estos datos, se puede contactar a:

- **CENAIS:** https://www.cenais.gob.cu
- **Universidad de Oriente:** https://www.uo.edu.cu
- **IRIS DMC (respaldo internacional):** https://www.iris.edu/hq/

---

**Nota de integridad académica:** Este proyecto se desarrolla con total transparencia 
sobre el origen de los datos, siguiendo los estándares éticos de investigación en 
ciencias de la tierra e inteligencia artificial.