# TFM Pipeline - Sistema Predictivo de Mantenimiento

Sistema predictivo de mantenimiento basado en THD para compresores industriales con aprendizaje continuo.

## Descripcion

Sistema completo de mantenimiento predictivo que utiliza Machine Learning (Isolation Forest + DBSCAN) para detectar anomalias en compresores industriales mediante analisis de distorsion armonica total (THD) y otras variables electricas y mecanicas.

**Version:** 3.0 - Con Sistema de Aprendizaje Continuo

## Caracteristicas Principales

### Sistema Predictivo Base
- Deteccion de anomalias con 100% de precision validada
- Monitoreo de 3 compresores industriales
- Analisis de THD, vibraciones y parametros electricos
- Dashboard web interactivo con multiples paginas
- Generacion automatica de Ordenes de Trabajo (OTs)
- Chat IA para consultas del sistema
- Analisis economico y ROI

### Sistema de Aprendizaje Continuo (NUEVO)
- **Carga de datos mensuales**: Interfaz para subir nuevos archivos
- **Diagnostico automatico**: Procesamiento con modelo actual
- **Validacion de predicciones**: Sistema de feedback
- **Reentrenamiento automatico**: Mejora continua del modelo
- **Versionado de modelos**: Historial completo de versiones
- **Dashboard de evolucion**: Metricas de mejora en el tiempo

## Estructura del Proyecto

```
TFM-pipeline/
├── dashboard/
│   ├── app.py                          # Aplicacion Flask principal
│   ├── templates/
│   │   ├── base.html                   # Plantilla base
│   │   ├── dashboard.html              # Dashboard principal
│   │   ├── compresores.html            # Analisis de compresores
│   │   ├── deteccion.html              # Deteccion avanzada
│   │   ├── ots.html                    # Ordenes de trabajo
│   │   ├── economico.html              # Analisis economico
│   │   ├── validacion.html             # Validacion del modelo
│   │   ├── reportes.html               # Generacion de reportes
│   │   ├── configuracion.html          # Configuracion
│   │   ├── chat.html                   # Chat IA
│   │   ├── carga_datos.html            # Carga de datos (NUEVO)
│   │   ├── validacion_predicciones.html # Validacion predicciones (NUEVO)
│   │   └── evolucion_modelo.html       # Evolucion del modelo (NUEVO)
│   └── database/
│       └── tfm_multipagina.db          # Base de datos SQLite
├── src/
│   ├── continuous_learning.py          # Modulo de aprendizaje continuo (NUEVO)
│   └── model_retraining.py             # Modulo de reentrenamiento (NUEVO)
├── data/
│   └── raw/                            # Datos de entrenamiento
├── models/
│   ├── produccion/                     # Modelo en produccion
│   └── versiones/                      # Historial de versiones
├── output/
│   ├── diagnosticos/                   # Resultados de diagnosticos
│   ├── ots_generadas/                  # OTs generadas
│   └── reportes/                       # Reportes generados
├── docs/
│   └── DOCUMENTACION_SISTEMA_APRENDIZAJE_CONTINUO.md
├── requirements.txt                    # Dependencias Python
└── README.md                           # Este archivo
```

## Requisitos del Sistema

### Software
- Python 3.9 o superior
- Navegador web moderno (Chrome, Firefox, Edge)

### Hardware Recomendado
- 8GB RAM minimo
- 100GB espacio en disco
- Procesador multi-core

## Instalacion

### 1. Clonar el Repositorio

```bash
git clone https://github.com/sanatos1966/TFM-pipeline.git
cd TFM-pipeline
```

### 2. Crear Entorno Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Dependencias principales:**
- Flask 2.3.2
- Flask-CORS 4.0.0
- pandas 1.5.3
- numpy 1.24.3
- scikit-learn 1.3.0
- matplotlib 3.7.1
- seaborn 0.12.2
- plotly 5.15.0
- joblib 1.3.1

### 4. Crear Estructura de Carpetas

```bash
# Windows PowerShell
New-Item -ItemType Directory -Force -Path "models\produccion"
New-Item -ItemType Directory -Force -Path "models\versiones"
New-Item -ItemType Directory -Force -Path "output\diagnosticos"
New-Item -ItemType Directory -Force -Path "output\ots_generadas"
New-Item -ItemType Directory -Force -Path "output\reportes"
New-Item -ItemType Directory -Force -Path "temp\uploads"

# Linux/Mac
mkdir -p models/produccion models/versiones
mkdir -p output/diagnosticos output/ots_generadas output/reportes
mkdir -p temp/uploads
```

### 5. Ejecutar la Aplicacion

```bash
cd dashboard
python app.py
```

La aplicacion estara disponible en: **http://localhost:5000**

## Uso del Sistema

### Dashboard Principal

Accede a `http://localhost:5000` para ver:
- KPIs principales del sistema
- Estado de los 3 compresores
- Graficos de metricas
- Acceso rapido a todas las funcionalidades

### Paginas Disponibles

| Ruta | Descripcion |
|------|-------------|
| `/` | Dashboard principal con KPIs |
| `/compresores` | Analisis detallado de compresores |
| `/deteccion` | Deteccion avanzada de anomalias |
| `/ots` | Gestion de ordenes de trabajo |
| `/economico` | Analisis economico y ROI |
| `/validacion` | Validacion del modelo predictivo |
| `/reportes` | Generacion de reportes |
| `/configuracion` | Configuracion del sistema |
| `/chat` | Chat IA del sistema |
| `/carga` | Carga de nuevos datos (NUEVO) |
| `/validacion_predicciones` | Validacion de predicciones (NUEVO) |
| `/evolucion_modelo` | Dashboard de evolucion (NUEVO) |

### Sistema de Aprendizaje Continuo

#### 1. Cargar Nuevos Datos

1. Accede a `http://localhost:5000/carga`
2. Selecciona mes, año y compresor
3. Sube archivo CSV o Excel
4. El sistema procesara y generara predicciones automaticamente

#### 2. Validar Predicciones

1. Accede a `http://localhost:5000/validacion_predicciones`
2. Selecciona periodo a validar
3. Marca cada prediccion como correcta/incorrecta
4. Proporciona detalles de eventos reales
5. Guarda las validaciones

#### 3. Reentrenar Modelo

El reentrenamiento puede ser:

**Automatico:**
- Configurado mensualmente
- Se ejecuta el dia 1 de cada mes a las 02:00 AM
- Solo actualiza si mejora > umbral configurado

**Manual:**
- Accede a `http://localhost:5000/evolucion_modelo`
- Haz clic en "Reentrenar Ahora"
- Espera a que termine el proceso

#### 4. Ver Evolucion

1. Accede a `http://localhost:5000/evolucion_modelo`
2. Revisa graficos de evolucion de metricas
3. Consulta historial de versiones
4. Compara versiones del modelo

## Flujo de Trabajo Mensual

```
Dia 1-5 del Mes N:
├── Usuario sube datos del mes N-1
├── Sistema diagnostica con modelo actual
├── Genera predicciones y OTs
└── Predicciones guardadas en BD

Dia 25-30 del Mes N:
├── Usuario valida predicciones
├── Marca eventos ocurridos/no ocurridos
└── Validaciones guardadas en BD

Dia 1 del Mes N+1 (02:00 AM):
├── Sistema reentrena automaticamente
├── Combina datos historicos + nuevos
├── Evalua nueva version
├── Actualiza produccion si mejora
└── Guarda version anterior como backup
```

## API Endpoints

### Endpoints Originales

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/api/sistema/estado` | Estado general del sistema |
| GET | `/api/ots` | Obtener ordenes de trabajo |
| POST | `/api/chat` | Enviar mensaje al chat IA |

### Endpoints de Aprendizaje Continuo (NUEVO)

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| POST | `/api/upload` | Subir y procesar archivo |
| GET | `/api/predicciones` | Obtener predicciones |
| POST | `/api/validar` | Guardar validacion |
| GET | `/api/versiones_modelo` | Obtener versiones del modelo |
| POST | `/api/reentrenar` | Ejecutar reentrenamiento |

## Modelo Predictivo

### Algoritmo

**Ensemble de modelos no supervisados:**
- **Isolation Forest**: Deteccion de anomalias globales
- **DBSCAN**: Clustering de anomalias detectadas

### Variables Monitoreadas

**Compresor C1 (THD):**
- THD_V_A, THD_V_B, THD_V_C (Voltaje)
- THD_I_A, THD_I_B, THD_I_C (Corriente)
- Potencia_Activa, Factor_Potencia
- Demanda_A, Demanda_B, Demanda_C

**Compresor C2 (Vibraciones):**
- Presion, Temperatura
- Vibracion_X, Vibracion_Y, Vibracion_Z
- Velocidad, Aceleracion, Desplazamiento

**Compresor C3 (Basico):**
- Presion, Temperatura, Caudal
- Potencia, Corriente, Voltaje

### Metricas de Rendimiento

| Metrica | Valor |
|---------|-------|
| Precision Global | 100% |
| F1-Score | 1.000 |
| AUC-ROC | 1.000 |
| MTBF | 156.3 horas |
| MTTR | 4.2 horas |
| Anticipacion Promedio | 15 dias |

## Base de Datos

### Tablas Principales

#### `ordenes_trabajo`
Almacena las OTs generadas por el sistema.

#### `historial_eventos`
Registro historico de eventos detectados.

#### `predicciones` (NUEVO)
Predicciones generadas por el sistema.

#### `validaciones` (NUEVO)
Validaciones de predicciones vs eventos reales.

#### `versiones_modelo` (NUEVO)
Historial de versiones del modelo.

## Configuracion

### Archivo de Configuracion

Crear `config/config.json`:

```json
{
  "sistema_aprendizaje": {
    "reentrenamiento": {
      "frecuencia": "mensual",
      "dia_ejecucion": 1,
      "hora_ejecucion": "02:00",
      "umbral_precision_minima": 0.85,
      "umbral_mejora_minima": 0.02
    },
    "validacion": {
      "periodo_validacion_dias": 30
    },
    "diagnostico": {
      "umbral_confianza_minimo": 70
    }
  }
}
```

## Mantenimiento

### Backup

```bash
# Backup de base de datos
cp dashboard/database/tfm_multipagina.db backups/tfm_$(date +%Y%m%d).db

# Backup de modelos
cp -r models backups/models_$(date +%Y%m%d)
```

### Limpieza

```bash
# Limpiar archivos temporales (mas de 30 dias)
find temp -type f -mtime +30 -delete

# Limpiar logs antiguos (mas de 90 dias)
find logs -type f -mtime +90 -delete
```

## Solucion de Problemas

### Error: "Modulo de aprendizaje continuo no disponible"

**Causa:** Los modulos Python no estan en la ruta correcta.

**Solucion:**
1. Verificar que `continuous_learning.py` y `model_retraining.py` esten en `src/`
2. Verificar que la carpeta `src/` este al mismo nivel que `dashboard/`

### Error al cargar archivo

**Causa:** Formato de archivo no soportado o columnas faltantes.

**Solucion:**
1. Verificar que el archivo sea CSV o Excel
2. Verificar que tenga las columnas necesarias (THD_V_A, THD_I_A, etc.)
3. Revisar logs en `logs/` para mas detalles

### Reentrenamiento no se ejecuta

**Causa:** No hay suficientes datos validados.

**Solucion:**
1. Verificar que hay predicciones validadas en la BD
2. Ejecutar reentrenamiento manual desde el dashboard
3. Revisar logs de errores

## Contribuciones

Este proyecto es parte de un Trabajo Final de Master (TFM) para EADIC 2025.

**Autor:** Antonio Cantos  
**Institucion:** EADIC - Master en Mantenimiento Industrial  
**Año:** 2025

## Licencia

Este proyecto es de uso academico y educativo.

## Contacto

Para consultas sobre el proyecto, contactar a traves del repositorio de GitHub.

## Documentacion Adicional

Para documentacion detallada del sistema de aprendizaje continuo, consultar:
- `docs/DOCUMENTACION_SISTEMA_APRENDIZAJE_CONTINUO.md`

## Changelog

### Version 3.0 (Noviembre 2025)
- Sistema de aprendizaje continuo completo
- Carga de datos mensuales
- Validacion de predicciones
- Reentrenamiento automatico
- Dashboard de evolucion del modelo
- Versionado de modelos

### Version 2.0 (Octubre 2025)
- Dashboard multi-pagina
- Paginas HTML independientes
- Chat IA integrado
- Base de datos SQLite

### Version 1.0 (Agosto 2025)
- Sistema predictivo base
- Modelo Ensemble (Isolation Forest + DBSCAN)
- Precision 100% validada
- Generacion de OTs

---

**TFM Pipeline - Sistema Predictivo de Mantenimiento v3.0**

