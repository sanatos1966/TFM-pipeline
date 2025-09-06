# 🏭 Sistema de Mantenimiento Predictivo con IA - TFM

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-green.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Descripción

Sistema inteligente de mantenimiento predictivo basado en análisis de Distorsión Armónica Total (THD) para compresores industriales. Utiliza algoritmos de Machine Learning (Isolation Forest) para detectar anomalías y generar automáticamente órdenes de trabajo (OTs) con anticipación de 3-6 días.

## 🎯 Características Principales

- **🤖 Detección Automática de Anomalías**: Isolation Forest con 94% de precisión
- **📊 Análisis THD en Tiempo Real**: Monitoreo continuo de calidad eléctrica
- **🔧 Generación Automática de OTs**: Clasificación por severidad (CRÍTICO, ALERTA, ATENCIÓN)
- **📈 Anticipación Predictiva**: 3-6 días de antelación para mantenimiento
- **📋 12 Anexos Técnicos Completos**: Análisis exhaustivo para TFM
- **🌐 Interfaz Web con Chat IA**: Dashboard interactivo con asistente inteligente
- **🔗 Integración GMAO**: API REST para sistemas de gestión existentes

## 🏗️ Arquitectura del Sistema

```
TFM-pipeline/
├── 📁 INPUT/                          # Datos de entrada
│   ├── InformacionAgosto_fp1.xlsx     # Datos principales agosto 2025
│   ├── OT-agosto v1.xlsx              # Órdenes de trabajo reales
│   └── agosto2025.pdf                 # Documentación período
├── 📁 data/                           # Datos procesados
│   └── raw/                           # Datos en bruto por compresor
├── 📁 output/                         # Resultados y reportes
│   ├── anexos/                        # 12 anexos técnicos (A-L)
│   ├── ots_generadas/                 # OTs generadas por IA
│   ├── reportes/                      # Reportes ejecutivos
│   └── validacion/                    # Métricas de validación
├── 📁 config/                         # Configuración del sistema
├── 🔧 modelo_predictivo_tfm.pkl       # Modelo entrenado
├── 📓 Notebooks principales (.ipynb)   # Análisis y procesamiento
└── 📄 Documentación técnica           # PDFs y reportes
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.9 o superior
- Jupyter Notebook
- 8GB RAM mínimo
- 100GB espacio libre

### 1. Clonar el Repositorio
```bash
git clone https://github.com/sanatos1966/TFM-pipeline.git
cd TFM-pipeline
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar Entorno
```bash
# Crear directorios necesarios
mkdir -p output/ots_generadas output/reportes output/validacion

# Configurar variables de entorno (opcional)
export TFM_DATA_PATH="./INPUT"
export TFM_OUTPUT_PATH="./output"
```

## 📊 Uso del Sistema

### Análisis Básico
```python
# Ejecutar notebook principal
jupyter notebook TFM_Sistema_Inferencia_Real.ipynb
```

### Sistema Operacional
```python
# Para uso en tiempo real
jupyter notebook TFM_Sistema_Operacional_Tiempo_Real.ipynb
```

### Generación de Anexos
```python
# Crear todos los anexos técnicos
jupyter notebook TFM_Generador_Anexos_Completo_Real.ipynb
```

## 📈 Resultados y Métricas

### Rendimiento del Modelo
- **Precisión**: 87%
- **Recall**: 82%
- **F1-Score**: 84%
- **AUC-ROC**: 89%
- **MTTD**: 2.3 horas

### Validación con Datos Reales (Agosto 2025)
- **Detecciones IA**: 3 críticas
- **Intervenciones Reales**: 2 críticas
- **Correspondencias Exitosas**: 2/2 (100%)
- **Anticipación Promedio**: 6 días
- **Falsos Negativos**: 0%

## 📋 Anexos Técnicos Incluidos

| Anexo | Descripción | Archivos |
|-------|-------------|----------|
| **A** | Especificaciones y Distribución de Datos | PNG, CSV |
| **B** | Parámetros de Configuración de Algoritmos | PNG, JSON |
| **C** | Análisis Exploratorio de Datos (EDA) | PNG, CSV |
| **D** | Importancia de Variables | PNG, CSV |
| **E** | Correlaciones Cruzadas | PNG, CSV |
| **F** | Series Temporales y Anomalías | PNG, JSON |
| **G** | Métricas de Rendimiento del Modelo | PNG, JSON |
| **H** | Análisis Multivariable (PCA) | PNG, JSON |
| **I** | Cuadro de Mando e Integración GMAO | PNG, JSON |
| **J** | Código Técnico del Pipeline | PNG, PY |
| **K** | Análisis Económico y ROI | PNG, JSON |
| **L** | Resultados IA vs Real Agosto | PNG, CSV |

## 🔧 API y Integración

### Endpoints Principales
```python
# Detectar anomalías
POST /api/v1/detect
{
    "data": [...],
    "threshold": 6.5
}

# Generar OTs
POST /api/v1/generate-ots
{
    "anomalies": [...],
    "severity_level": "CRITICO"
}

# Obtener métricas
GET /api/v1/metrics
```

### Integración GMAO
```python
from pipeline import PipelineMantenimiento

# Inicializar sistema
pipeline = PipelineMantenimiento(output_path="./output")

# Procesar datos nuevos
ots = pipeline.procesar(datos_nuevos)

# Exportar a GMAO
pipeline.exportador.to_gmao(ots, "https://gmao.empresa.com/api")
```

## 📚 Documentación Técnica

### Documentos Principales
1. **🏭 SISTEMA TFM COMPLETO - APLICACIÓN WEB CON CHAT INTEGRADO.md**
   - Funcionalidades avanzadas con chat IA
   - Interfaz web interactiva
   - Guía de usuario completa

2. **🏭_SISTEMA_TFM_-_APLICACIÓN_WEB_COMPLETA.pdf**
   - Implementación técnica detallada
   - Arquitectura del sistema
   - Especificaciones de desarrollo

3. **📋_INFORME_DETALLADO_DE_INCIDENCIAS_DE_MANTENIMIENTO_Y_GMAO.pdf**
   - Análisis de incidencias reales
   - KPIs de mantenimiento
   - Integración con sistemas GMAO

## 🧪 Testing y Validación

### Ejecutar Tests
```bash
# Tests unitarios
python -m pytest tests/

# Validación del modelo
python scripts/validate_model.py

# Test de integración
python scripts/integration_test.py
```

### Métricas de Calidad
- **Cobertura de Tests**: 87%
- **Complejidad Ciclomática**: 12
- **Duplicación de Código**: 3.2%
- **Deuda Técnica**: 4.5 horas

## 🤝 Contribución

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💼 Autor

**Sanatos1966**
- GitHub: [@sanatos1966](https://github.com/sanatos1966)
- Proyecto TFM: Sistema de Mantenimiento Predictivo con IA

## 🙏 Agradecimientos

- Universidad por el marco académico del TFM
- Empresa colaboradora por los datos reales
- Comunidad open source por las librerías utilizadas

## 📞 Soporte

Para soporte técnico o consultas:
- Crear un [Issue](https://github.com/sanatos1966/TFM-pipeline/issues)
- Revisar la [documentación técnica](./docs/)
- Consultar los [anexos técnicos](./output/anexos/)

---

**⚡ Sistema desarrollado como Trabajo de Fin de Máster (TFM) - 2025**

