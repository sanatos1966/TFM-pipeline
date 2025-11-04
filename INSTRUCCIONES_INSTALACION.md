# Instrucciones de Instalacion - TFM Pipeline v3.0

## Guia Rapida de Instalacion

### Paso 1: Descargar el Repositorio

```bash
git clone https://github.com/sanatos1966/TFM-pipeline.git
cd TFM-pipeline
```

### Paso 2: Instalar Python

Asegurate de tener **Python 3.9 o superior** instalado.

```bash
# Verificar version
python --version
```

Si no tienes Python instalado, descargalo desde: https://www.python.org/downloads/

### Paso 3: Crear Entorno Virtual

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 4: Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Paso 5: Crear Estructura de Carpetas

**Windows PowerShell:**
```powershell
# Crear carpetas necesarias
New-Item -ItemType Directory -Force -Path "models\produccion"
New-Item -ItemType Directory -Force -Path "models\versiones"
New-Item -ItemType Directory -Force -Path "output\diagnosticos"
New-Item -ItemType Directory -Force -Path "output\ots_generadas"
New-Item -ItemType Directory -Force -Path "output\reportes"
New-Item -ItemType Directory -Force -Path "temp\uploads"
New-Item -ItemType Directory -Force -Path "data\raw"
New-Item -ItemType Directory -Force -Path "data\processed"

# Crear archivos .gitkeep para mantener estructura
New-Item -ItemType File -Force -Path "models\produccion\.gitkeep"
New-Item -ItemType File -Force -Path "models\versiones\.gitkeep"
New-Item -ItemType File -Force -Path "output\diagnosticos\.gitkeep"
New-Item -ItemType File -Force -Path "output\ots_generadas\.gitkeep"
New-Item -ItemType File -Force -Path "output\reportes\.gitkeep"
New-Item -ItemType File -Force -Path "data\raw\.gitkeep"
New-Item -ItemType File -Force -Path "data\processed\.gitkeep"
```

**Linux/Mac:**
```bash
# Crear carpetas necesarias
mkdir -p models/produccion models/versiones
mkdir -p output/diagnosticos output/ots_generadas output/reportes
mkdir -p temp/uploads
mkdir -p data/raw data/processed

# Crear archivos .gitkeep
touch models/produccion/.gitkeep
touch models/versiones/.gitkeep
touch output/diagnosticos/.gitkeep
touch output/ots_generadas/.gitkeep
touch output/reportes/.gitkeep
touch data/raw/.gitkeep
touch data/processed/.gitkeep
```

### Paso 6: Copiar Modelo Entrenado (Si Existe)

Si tienes el archivo `modelo_ensemble_tfm.pkl`:

```bash
# Copiarlo a la carpeta de produccion
cp modelo_ensemble_tfm.pkl models/produccion/
```

### Paso 7: Ejecutar la Aplicacion

```bash
cd dashboard
python app.py
```

### Paso 8: Acceder al Dashboard

Abre tu navegador en: **http://localhost:5000**

## Verificacion de Instalacion

### Verificar que Todo Funciona

1. **Dashboard Principal**: http://localhost:5000
   - Debe mostrar KPIs y graficos

2. **Compresores**: http://localhost:5000/compresores
   - Debe mostrar analisis de los 3 compresores

3. **Chat IA**: http://localhost:5000/chat
   - Debe responder a preguntas basicas

4. **Sistema de Aprendizaje Continuo**:
   - **Carga de datos**: http://localhost:5000/carga
   - **Validacion**: http://localhost:5000/validacion_predicciones
   - **Evolucion**: http://localhost:5000/evolucion_modelo

Si alguna pagina muestra "Modulo de aprendizaje continuo no disponible", verifica que los archivos `continuous_learning.py` y `model_retraining.py` esten en la carpeta `src/`.

## Solucion de Problemas Comunes

### Error: "No module named 'flask'"

**Solucion:**
```bash
pip install Flask==2.3.2
```

### Error: "No module named 'continuous_learning'"

**Solucion:**
Verifica que los archivos esten en la ubicacion correcta:
```
TFM-pipeline/
├── src/
│   ├── continuous_learning.py
│   └── model_retraining.py
└── dashboard/
    └── app.py
```

### Error: "Address already in use"

**Solucion:**
El puerto 5000 ya esta en uso. Cambia el puerto en `app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Error de Codificacion en Windows

**Solucion:**
Antes de ejecutar `python app.py`:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
```

### Base de Datos No Se Crea

**Solucion:**
Verifica permisos de escritura en la carpeta `dashboard/database/`:
```bash
# Windows
icacls dashboard\database /grant Users:F

# Linux/Mac
chmod 755 dashboard/database
```

## Configuracion Adicional

### Configurar Reentrenamiento Automatico

Crear archivo `config/config.json`:

```json
{
  "sistema_aprendizaje": {
    "reentrenamiento": {
      "frecuencia": "mensual",
      "dia_ejecucion": 1,
      "hora_ejecucion": "02:00",
      "umbral_precision_minima": 0.85,
      "umbral_mejora_minima": 0.02
    }
  }
}
```

### Configurar Variables de Entorno (Opcional)

**Windows:**
```powershell
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"
```

**Linux/Mac:**
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
```

## Actualizacion desde Version Anterior

Si ya tienes una version anterior instalada:

### 1. Hacer Backup

```bash
# Backup de base de datos
cp dashboard/database/tfm_multipagina.db backups/

# Backup de modelos
cp -r models backups/models_backup
```

### 2. Actualizar Archivos

```bash
git pull origin main
```

### 3. Actualizar Dependencias

```bash
pip install --upgrade -r requirements.txt
```

### 4. Ejecutar Migraciones (Si es Necesario)

Si hay cambios en la base de datos, ejecutar:
```bash
cd dashboard
python -c "from app import init_database; init_database()"
```

## Desinstalacion

Para desinstalar completamente el sistema:

```bash
# 1. Desactivar entorno virtual
deactivate

# 2. Eliminar carpeta del proyecto
rm -rf TFM-pipeline  # Linux/Mac
Remove-Item -Recurse -Force TFM-pipeline  # Windows
```

## Soporte

Para problemas o consultas:
1. Revisar la documentacion en `docs/`
2. Revisar logs en `logs/`
3. Abrir un issue en GitHub

## Proximos Pasos

Despues de la instalacion:

1. **Cargar Datos Iniciales**: Sube los datos de entrenamiento en `/carga`
2. **Explorar Dashboard**: Navega por todas las paginas
3. **Configurar Sistema**: Ajusta parametros en `/configuracion`
4. **Generar Primera Prediccion**: Sube datos nuevos y genera diagnostico
5. **Validar Predicciones**: Valida resultados para mejorar el modelo

---

**TFM Pipeline v3.0 - Sistema de Mantenimiento Predictivo con Aprendizaje Continuo**

