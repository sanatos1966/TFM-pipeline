# 🏭 SISTEMA TFM COMPLETO - APLICACIÓN WEB CON CHAT INTEGRADO

## 📋 Descripción General

Sistema web completo para el TFM "Sistema de Mantenimiento Predictivo - Frío Pacífico 1" con **chat integrado especializado**, **base de conocimiento del TFM** y **búsqueda web sobre mantenimiento industrial**.

## 🎯 Funcionalidades Principales

### 📊 Dashboard Ejecutivo Completo
- **KPIs Principales**: Precisión 100%, ROI 42.5%, Disponibilidad 97.4%
- **Validación Agosto 2025**: Predicciones vs eventos reales
- **Estado de Compresores**: C1 (Anfitrión THD), C2 (Vibraciones), C3 (Básico)
- **Resumen de Validación**: Hipótesis confirmada, impacto económico

### 🏭 Análisis por Compresores
- **C1 - Anfitrión THD**: 7 variables THD, precisión 100%
- **C2 - Vibraciones**: 8 variables mecánicas, vibraciones activas
- **C3 - Básico**: 6 variables mecánicas, cobertura básica
- **Análisis Histórico**: Gráficos interactivos con datos reales

### 🔍 Detección Avanzada
- **Isolation Forest + DBSCAN**: Configuración validada
- **Resultados Agosto 2025**: 3 predicciones, 2 eventos reales
- **Métricas de Rendimiento**: Precisión, anticipación, sensibilidad
- **Configuración del Modelo**: Umbrales optimizados

### 📋 Gestión de OTs
- **Generación Automática**: Basada en anomalías detectadas
- **Filtros Avanzados**: Por severidad, estado, fecha
- **Exportación Excel**: Múltiples hojas con limpieza de timezone
- **Estados**: Pendiente, En Proceso, Completada

### 💰 Análisis Económico
- **Costos Reales 2025**: $25,607.38 validados
- **Ahorro Estimado**: $7,682.21 (30% del total)
- **Proyección 3 años**: ROI, VAN, TIR
- **Métricas de Confiabilidad**: MTBF, MTTR, disponibilidad

### 📈 Validación del Modelo
- **Período Entrenamiento**: Enero-Julio 2025 (182,670 registros)
- **Período Validación**: Agosto 2025 (24,359 registros)
- **Precisión C1**: 100% (2/2 eventos detectados)
- **Anticipación**: 6-24 días antes de fallas

### 📑 Reportes y Exportación
- **Reporte Ejecutivo**: KPIs, validación, impacto económico
- **Reporte Técnico**: Configuración, métricas, análisis detallado
- **Exportación**: JSON completo, CSV resumen, Excel OTs

## 🤖 CHAT INTEGRADO ESPECIALIZADO

### 🎯 Características del Chat
- **Experto en Mantenimiento Industrial**: GMAO, frío industrial, sistemas predictivos
- **Base de Conocimiento Integrada**: Datos completos del TFM
- **Búsqueda Web Especializada**: Información actualizada de mantenimiento
- **Modelos IA**: GPT-3.5 Turbo (gratuito) y GPT-4 (premium)

### 🧠 Base de Conocimiento Incluida
- **Datos del TFM**: Compresores C1, C2, C3 con especificaciones técnicas
- **Resultados Validados**: Agosto 2025 con precisión 100%
- **Análisis Económico**: Costos, ahorros, ROI detallado
- **Configuración ML**: Isolation Forest + DBSCAN
- **Conocimiento General**: MTBF, MTTR, vibraciones, termografía, etc.

### 🌐 Búsqueda Web Especializada
- **Sitios Especializados**: reliabilityweb.com, maintenanceworld.com, etc.
- **Temas Cubiertos**: 14 categorías de mantenimiento industrial
- **Información Actualizada**: Tendencias, normativas, mejores prácticas
- **Fuentes Citadas**: Referencias automáticas en las respuestas

### 💬 Capacidades del Chat
- **Cálculos Técnicos**: MTBF, MTTR, ROI, disponibilidad, confiabilidad
- **Normativas**: ISO 55000, EN 13306, ISO 10816, ASHRAE
- **Frío Industrial**: COP, refrigerantes, eficiencia energética
- **Análisis de Fallas**: Diagnóstico, prescripciones, soluciones
- **Consultas del TFM**: Datos específicos del proyecto validado

## 🛠️ Arquitectura Técnica

### Backend (Flask)
```
src/
├── main.py                           # Aplicación principal Flask
├── routes/
│   ├── ots_routes.py                # Rutas originales de OTs
│   ├── tfm_dashboard_routes.py      # Rutas avanzadas del TFM
│   ├── chat_routes.py               # Chat con IA integrado
│   └── web_search_routes.py         # Búsqueda web especializada
├── database/
│   ├── tfm_knowledge_base.py        # Base de conocimiento del TFM
│   └── chroma_db/                   # Base de datos vectorial
└── static/
    ├── index.html                   # Frontend completo
    └── app.js                       # JavaScript con chat
```

### Tecnologías Utilizadas
- **Backend**: Flask, SQLAlchemy, ChromaDB, SentenceTransformers
- **Frontend**: HTML5, Tailwind CSS, JavaScript ES6
- **Chat**: OpenAI API, LangChain, búsqueda semántica
- **Gráficos**: Plotly.js para visualizaciones interactivas
- **Datos**: JSON, CSV, Excel con limpieza de timezone

## 🚀 Instalación y Ejecución

### Requisitos Previos
```bash
Python 3.8+
pip
virtualenv (recomendado)
OpenAI API Key (para el chat)
```

### Instalación
```bash
# 1. Extraer el código fuente
tar -xzf sistema_ots_web_completo.tar.gz
cd sistema_ots_web

# 2. Activar entorno virtual
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env y añadir tu OPENAI_API_KEY

# 5. Ejecutar la aplicación
python src/main.py
```

### Acceso
- **URL Local**: http://localhost:5000
- **Chat**: Botón flotante en esquina inferior derecha
- **Navegadores**: Chrome, Firefox, Safari, Edge

## 📊 Datos Validados Incluidos

### Entrenamiento (Enero-Julio 2025)
- **Registros Totales**: 182,670
- **C1**: 60,919 registros, 7 variables THD
- **C2**: 60,926 registros, 8 variables mecánicas
- **C3**: 60,825 registros, 6 variables mecánicas
- **Eventos Críticos**: 24 (11 C1, 4 C2, 9 C3)

### Validación (Agosto 2025)
- **Registros Totales**: 24,359
- **Predicciones IA**: 3 (fechas: 01, 03, 05 agosto)
- **Eventos Reales**: 2 (fechas: 07, 25 agosto)
- **Precisión C1**: 100%
- **Anticipación**: 15 días promedio

### Análisis Económico
- **Costo Total 2025**: $25,607.38
- **Mano de Obra**: $15,364.43 (60%)
- **Suministros**: $10,242.95 (40%)
- **Ahorro Estimado**: $7,682.21 (30%)
- **ROI**: 42.5% primer año

## 🔧 Configuración del Modelo

### Isolation Forest
```python
contamination: 0.15
n_estimators: 200
random_state: 42
```

### DBSCAN
```python
eps: 0.5
min_samples: 5
```

### Umbrales
```python
thd_normal: ≤ 1.0
thd_critico: > 4.0
ventana_predictiva: 72 horas
```

## 📱 Funcionalidades de la Interfaz

### Navegación
- **Sidebar Izquierdo**: Navegación principal entre secciones
- **Header Superior**: Información del sistema y acciones rápidas
- **Chat Flotante**: Botón en esquina inferior derecha
- **Responsive**: Adaptable a desktop, tablet y móvil

### Interactividad
- **Gráficos Plotly**: Zoom, pan, hover, exportación
- **Filtros Dinámicos**: Tiempo real sin recarga
- **Chat Inteligente**: Respuestas contextuales con fuentes
- **Exportación**: Un clic para descargar datos
- **Notificaciones**: Feedback visual de acciones

### Visualizaciones
- **Dashboard Ejecutivo**: 8 KPIs principales + gráficos
- **Análisis Compresores**: Comparativo + históricos
- **Detección Avanzada**: Configuración + resultados
- **Análisis Económico**: Costos + proyecciones

## 🔄 API Endpoints

### Dashboard Ejecutivo
- `GET /api/tfm/dashboard-ejecutivo` - KPIs y datos principales
- `GET /api/tfm/estado-sistema` - Estado actual del sistema

### Compresores
- `GET /api/tfm/compresores/<id>` - Detalles de compresor específico

### Análisis Económico
- `GET /api/tfm/analisis-economico` - Datos económicos completos

### Detección
- `GET /api/tfm/deteccion-avanzada` - Configuración y resultados

### Chat Integrado
- `POST /api/chat` - Enviar mensaje al chat
- `GET /api/chat/historial/<session_id>` - Obtener historial
- `POST /api/chat/limpiar/<session_id>` - Limpiar conversación
- `GET /api/chat/sugerencias` - Obtener sugerencias de preguntas
- `GET /api/chat/estado` - Estado del servicio de chat

### Búsqueda Web
- `POST /api/web-search` - Búsqueda web especializada
- `GET /api/web-search/topics` - Temas de mantenimiento disponibles
- `GET /api/web-search/trending` - Temas trending en mantenimiento

### Reportes
- `GET /api/tfm/reportes/ejecutivo` - Reporte ejecutivo JSON
- `GET /api/tfm/reportes/tecnico` - Reporte técnico JSON
- `GET /api/tfm/exportar/datos-completos` - Exportación JSON
- `GET /api/tfm/exportar/resumen-csv` - Exportación CSV

## 🎨 Diseño y UX

### Paleta de Colores
- **Primario**: Azul (#2563eb)
- **Secundario**: Verde (#16a34a)
- **Acentos**: Naranja (#ea580c), Púrpura (#9333ea)
- **Estados**: Rojo (#dc2626), Amarillo (#ca8a04)

### Tipografía
- **Fuente**: Inter (Google Fonts)
- **Tamaños**: 12px-32px escalados
- **Pesos**: 400 (normal), 600 (semibold), 700 (bold)

### Componentes
- **Cards**: Sombras suaves, bordes redondeados
- **Botones**: Estados hover, focus, disabled
- **Chat**: Ventana flotante con animaciones
- **Formularios**: Validación visual, feedback
- **Gráficos**: Tema consistente, colores corporativos

## 📈 Métricas de Validación

### Precisión del Modelo
- **C1 (Anfitrión)**: 100% (2/2 eventos)
- **Anticipación**: 6-24 días
- **Confianza**: 92.1-97.8%
- **Sobre-predicción**: 1 evento (conservador)

### Impacto Operacional
- **MTBF**: 156.3 horas (objetivo >100h)
- **MTTR**: 4.2 horas (objetivo <6h)
- **Disponibilidad**: 97.4% (objetivo >95%)
- **Eficiencia**: 30% reducción costos

## 🤖 Guía de Uso del Chat

### Configuración Inicial
1. **Obtener API Key de OpenAI**:
   - Visita https://platform.openai.com/api-keys
   - Crea una cuenta o inicia sesión
   - Genera una nueva API key
   - Copia la key

2. **Configurar en la Aplicación**:
   - Edita el archivo `.env`
   - Reemplaza `tu_api_key_aqui` con tu API key real
   - Reinicia la aplicación

### Uso del Chat
1. **Abrir Chat**: Haz clic en el botón flotante 💬
2. **Seleccionar Modelo**: 
   - GPT-3.5 Turbo (gratuito, rápido)
   - GPT-4 (premium, más avanzado)
3. **Hacer Preguntas**: Escribe tu consulta sobre mantenimiento
4. **Usar Sugerencias**: Haz clic en los botones de sugerencias
5. **Exportar Conversación**: Usa las opciones de exportación

### Ejemplos de Preguntas
```
¿Cómo funciona el modelo de detección del TFM?
Calcula el MTBF si tengo 3 fallas en 2000 horas
¿Cuáles son las fallas más comunes en compresores?
¿Qué dice la norma ISO 10816 sobre vibraciones?
Explícame los resultados de validación de agosto 2025
¿Cómo optimizar el COP de un sistema de refrigeración?
```

## 🔒 Seguridad y Rendimiento

### Seguridad
- **API Key**: Almacenada en variables de entorno
- **Validación**: Entrada de datos sanitizada
- **CORS**: Configurado para desarrollo
- **Headers**: Seguridad básica implementada

### Rendimiento
- **Carga Lazy**: Gráficos bajo demanda
- **Caché**: Datos estáticos en memoria
- **Base Vectorial**: Búsquedas semánticas rápidas
- **Compresión**: Assets minificados
- **Responsive**: Optimizado para móviles

## 🚀 Despliegue

### Desarrollo Local
```bash
python src/main.py
# Acceso: http://localhost:5000
```

### Producción (Recomendado)
```bash
# Usar Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app

# Variables de entorno para producción
export FLASK_ENV=production
export FLASK_DEBUG=False
export OPENAI_API_KEY=tu_api_key_real
```

## 📦 Dependencias Principales

### Backend
```
flask>=2.0.0
flask-cors>=3.0.0
flask-sqlalchemy>=2.5.0
openai>=1.0.0
pandas>=1.3.0
numpy>=1.21.0
scikit-learn>=1.0.0
plotly>=5.0.0
chromadb>=0.4.0
sentence-transformers>=2.2.0
langchain>=0.1.0
requests>=2.28.0
beautifulsoup4>=4.11.0
```

### Frontend
```
Tailwind CSS 3.x
Plotly.js (latest)
Font Awesome 6.x
```

## 📞 Soporte y Contacto

### Desarrolladores
- **Antonio Cantos** - Análisis y Validación TFM
- **Renzo Chavez** - Implementación Técnica

### Institución
- **EADIC 2025** - Máster en Mantenimiento Industrial

### Documentación Adicional
- **TFM Completo**: Disponible en repositorio
- **Datos Validados**: Enero-Agosto 2025
- **Código Fuente**: Completamente documentado
- **Informe de Incidencias**: Análisis detallado GMAO

## 🎉 Características Destacadas

### ✅ Sistema Completo
- **Dashboard Interactivo** con todos los datos del TFM
- **Chat Especializado** en mantenimiento industrial
- **Base de Conocimiento** integrada y actualizable
- **Búsqueda Web** en sitios especializados
- **Exportación Completa** en múltiples formatos

### ✅ Validación Real
- **Datos Reales** de Enero-Agosto 2025
- **Precisión Comprobada** 100% en C1
- **ROI Demostrado** 42.5% primer año
- **Hipótesis Confirmada** THD predice fallas mecánicas

### ✅ Tecnología Avanzada
- **Machine Learning** con Isolation Forest + DBSCAN
- **Inteligencia Artificial** con OpenAI GPT
- **Búsqueda Semántica** con embeddings
- **Interfaz Moderna** responsive y accesible

### ✅ Funcionalidad Completa
- **Generación Automática** de órdenes de trabajo
- **Análisis Económico** detallado con proyecciones
- **Monitoreo en Tiempo Real** de 3 compresores
- **Exportación Avanzada** con limpieza de datos

## 📄 Licencia

Proyecto académico desarrollado para el TFM de EADIC 2025.
Uso educativo y de investigación.

---

**🎉 Sistema TFM Completo - Chat Integrado | Precisión 100% | ROI 42.5% | Base de Conocimiento | Búsqueda Web**

*Versión 2.0 - Sistema Completo con Chat Especializado*

