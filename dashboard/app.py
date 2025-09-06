#!/usr/bin/env python3
"""
TFM - Sistema Predictivo Frío Pacífico 1
Aplicación Web Multi-página con HTML separados
Versión: 2.0 - Con páginas independientes
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
import random
import sqlite3
from pathlib import Path

# Configuración de la aplicación
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'tfm_sistema_predictivo_2025_multipagina'

# Crear directorio de base de datos si no existe
DB_DIR = Path(__file__).parent / 'database'
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / 'tfm_multipagina.db'

# ============================================================================
# DATOS DEL TFM VALIDADOS (mismo que antes)
# ============================================================================

TFM_DATA = {
    'sistema': {
        'nombre': 'TFM - Sistema Predictivo Frío Pacífico 1',
        'version': '2.0 Multi-página',
        'estado': 'Operativo',
        'institucion': 'EADIC 2025 - Máster en Mantenimiento Industrial',
        'autor': 'Antonio Cantos',
        'fecha_validacion': '2025-08-31'
    },
    'kpis_principales': {
        'precision_global': 100.0,
        'roi_primer_año': 42.5,
        'disponibilidad': 97.4,
        'mtbf_horas': 156.3,
        'mttr_horas': 4.2,
        'costo_total_2025': 25607.38,
        'ahorro_estimado': 7682.21,
        'reduccion_costos_porcentaje': 30.0
    },
    'compresores': [
        {
            'id': 'C1_REF-012',
            'nombre': 'Compresor C1 - Anfitrión THD',
            'tipo': 'Anfitrión con monitoreo THD',
            'estado': 'Operativo',
            'variables_monitoreadas': 7,
            'tipos_variables': ['THD_Voltaje_A', 'THD_Voltaje_B', 'THD_Voltaje_C', 'THD_Corriente_A', 'THD_Corriente_B', 'THD_Corriente_C', 'THD_Total'],
            'precision_validada': 100.0,
            'eventos_detectados_agosto': 2,
            'anticipacion_promedio_dias': 15,
            'confianza_promedio': 95.0
        },
        {
            'id': 'C2_REF-013',
            'nombre': 'Compresor C2 - Vibraciones',
            'tipo': 'Monitoreo de vibraciones mecánicas',
            'estado': 'Operativo',
            'variables_monitoreadas': 8,
            'tipos_variables': ['Presion', 'Temperatura', 'Vibracion_X', 'Vibracion_Y', 'Vibracion_Z', 'Velocidad', 'Aceleracion', 'Desplazamiento'],
            'precision_estimada': 87.5,
            'eventos_detectados_agosto': 0,
            'monitoreo_continuo': True
        },
        {
            'id': 'C3_REF-014',
            'nombre': 'Compresor C3 - Básico',
            'tipo': 'Monitoreo básico mecánico',
            'estado': 'Operativo',
            'variables_monitoreadas': 6,
            'tipos_variables': ['Presion', 'Temperatura', 'Caudal', 'Potencia', 'Corriente', 'Voltaje'],
            'precision_estimada': 65.0,
            'eventos_detectados_agosto': 0,
            'recomendacion': 'Añadir sensores de vibración'
        }
    ]
}

# ============================================================================
# FUNCIONES DE BASE DE DATOS (mismas que antes)
# ============================================================================

def init_database():
    """Inicializa la base de datos SQLite"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ordenes_trabajo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            compresor_id TEXT NOT NULL,
            tipo TEXT NOT NULL,
            severidad TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_vencimiento TIMESTAMP,
            estado TEXT DEFAULT 'Pendiente',
            costo_estimado REAL,
            tecnico_asignado TEXT,
            observaciones TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial_eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            compresor_id TEXT NOT NULL,
            fecha_evento TIMESTAMP NOT NULL,
            tipo_evento TEXT NOT NULL,
            descripcion TEXT,
            valor_thd REAL,
            temperatura REAL,
            presion REAL,
            prediccion_ia BOOLEAN DEFAULT FALSE,
            confianza REAL
        )
    ''')
    
    conn.commit()
    conn.close()

def cargar_datos_iniciales():
    """Carga datos iniciales en la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM ordenes_trabajo')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    # Insertar OTs de ejemplo
    ots_ejemplo = [
        ('OT-2025-001', 'C1_REF-012', 'Predictivo', 'CRÍTICO', 'THD elevado detectado - Revisión eléctrica requerida', '2025-08-01 10:30:00', '2025-08-08 10:30:00', 'Completada', 1250.00, 'Juan Pérez', 'Revisión completada, THD normalizado'),
        ('OT-2025-002', 'C1_REF-012', 'Predictivo', 'CRÍTICO', 'Anomalía en THD_Voltaje_A - Mantenimiento preventivo', '2025-08-03 14:15:00', '2025-08-10 14:15:00', 'Completada', 980.00, 'María García', 'Conexiones eléctricas revisadas'),
        ('OT-2025-003', 'C2_REF-013', 'Preventivo', 'ALERTA', 'Mantenimiento rutinario de vibraciones', '2025-08-15 09:00:00', '2025-08-22 09:00:00', 'En Proceso', 450.00, 'Carlos López', 'Análisis de vibraciones en curso'),
        ('OT-2025-004', 'C3_REF-014', 'Correctivo', 'ATENCIÓN', 'Revisión de presión - Lectura irregular', '2025-08-20 16:45:00', '2025-08-27 16:45:00', 'Pendiente', 320.00, None, None),
        ('OT-2025-005', 'C1_REF-012', 'Predictivo', 'ALERTA', 'Monitoreo THD - Tendencia ascendente', '2025-08-28 11:20:00', '2025-09-04 11:20:00', 'Pendiente', 180.00, None, None)
    ]
    
    for ot in ots_ejemplo:
        cursor.execute('''
            INSERT INTO ordenes_trabajo 
            (codigo, compresor_id, tipo, severidad, descripcion, fecha_creacion, fecha_vencimiento, estado, costo_estimado, tecnico_asignado, observaciones)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ot)
    
    conn.commit()
    conn.close()

# ============================================================================
# RUTAS PRINCIPALES - PÁGINAS HTML SEPARADAS
# ============================================================================

@app.route('/')
def dashboard():
    """Página principal - Dashboard Ejecutivo"""
    return render_template('dashboard.html', 
                         kpis=TFM_DATA['kpis_principales'],
                         compresores=TFM_DATA['compresores'],
                         sistema=TFM_DATA['sistema'])

@app.route('/compresores')
def compresores():
    """Página de Análisis de Compresores"""
    return render_template('compresores.html', 
                         compresores=TFM_DATA['compresores'],
                         sistema=TFM_DATA['sistema'])

@app.route('/deteccion')
def deteccion():
    """Página de Detección Avanzada"""
    return render_template('deteccion.html', 
                         sistema=TFM_DATA['sistema'])

@app.route('/ots')
def ots():
    """Página de Órdenes de Trabajo"""
    return render_template('ots.html', 
                         sistema=TFM_DATA['sistema'])

@app.route('/economico')
def economico():
    """Página de Análisis Económico"""
    return render_template('economico.html', 
                         kpis=TFM_DATA['kpis_principales'],
                         sistema=TFM_DATA['sistema'])

@app.route('/validacion')
def validacion():
    """Página de Validación del Modelo"""
    return render_template('validacion.html', 
                         sistema=TFM_DATA['sistema'])

@app.route('/reportes')
def reportes():
    """Página de Reportes"""
    return render_template('reportes.html', 
                         sistema=TFM_DATA['sistema'])

@app.route('/configuracion')
def configuracion():
    """Página de Configuración"""
    return render_template('configuracion.html', 
                         sistema=TFM_DATA['sistema'])

@app.route('/chat')
def chat_page():
    """Página dedicada al Chat"""
    return render_template('chat.html', 
                         sistema=TFM_DATA['sistema'])

# ============================================================================
# RUTAS DE API (mismas que antes)
# ============================================================================

@app.route('/api/sistema/estado')
def estado_sistema():
    """Estado general del sistema"""
    return jsonify({
        'sistema': TFM_DATA['sistema'],
        'estado': 'Operativo',
        'timestamp': datetime.now().isoformat(),
        'compresores_activos': 3,
        'precision_global': TFM_DATA['kpis_principales']['precision_global'],
        'base_datos': 'SQLite Multi-página',
        'chat_disponible': True
    })

@app.route('/api/ots')
def obtener_ots():
    """Obtiene las órdenes de trabajo de la base de datos"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT codigo, compresor_id, tipo, severidad, descripcion, 
                   fecha_creacion, estado, costo_estimado, tecnico_asignado
            FROM ordenes_trabajo
            ORDER BY fecha_creacion DESC
        ''')
        rows = cursor.fetchall()
        
        ots = []
        for row in rows:
            ots.append({
                'codigo': row[0],
                'compresor_id': row[1],
                'tipo': row[2],
                'severidad': row[3],
                'descripcion': row[4],
                'fecha_creacion': row[5],
                'estado': row[6],
                'costo_estimado': row[7],
                'tecnico_asignado': row[8]
            })
        
        conn.close()
        
        return jsonify({
            'ots': ots,
            'total': len(ots)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ots/generar', methods=['POST'])
def generar_ots():
    """Genera nuevas órdenes de trabajo"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Generar OTs simuladas
        nuevas_ots = []
        compresores = ['C1_REF-012', 'C2_REF-013', 'C3_REF-014']
        tipos = ['Predictivo', 'Preventivo', 'Correctivo']
        severidades = ['CRÍTICO', 'ALERTA', 'ATENCIÓN']
        
        for i in range(random.randint(1, 3)):
            codigo = f'OT-2025-{random.randint(100, 999)}'
            compresor = random.choice(compresores)
            tipo = random.choice(tipos)
            severidad = random.choice(severidades)
            
            descripcion_templates = {
                'Predictivo': f'Anomalía detectada en {compresor} - Mantenimiento predictivo requerido',
                'Preventivo': f'Mantenimiento preventivo programado para {compresor}',
                'Correctivo': f'Falla detectada en {compresor} - Reparación necesaria'
            }
            
            descripcion = descripcion_templates[tipo]
            costo = round(random.uniform(200, 1500), 2)
            fecha_vencimiento = (datetime.now() + timedelta(days=7)).isoformat()
            
            cursor.execute('''
                INSERT INTO ordenes_trabajo 
                (codigo, compresor_id, tipo, severidad, descripcion, fecha_vencimiento, costo_estimado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (codigo, compresor, tipo, severidad, descripcion, fecha_vencimiento, costo))
            
            nuevas_ots.append({
                'codigo': codigo,
                'compresor_id': compresor,
                'tipo': tipo,
                'severidad': severidad,
                'descripcion': descripcion,
                'costo_estimado': costo
            })
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'ots_generadas': nuevas_ots,
            'total_generadas': len(nuevas_ots),
            'mensaje': f'Se generaron {len(nuevas_ots)} órdenes de trabajo exitosamente'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """Endpoint del chat"""
    try:
        data = request.get_json()
        mensaje = data.get('mensaje', '')
        
        # Respuestas predefinidas basadas en el TFM
        respuesta = generar_respuesta_local(mensaje)
        
        return jsonify({
            'respuesta': respuesta,
            'success': True,
            'modelo_usado': 'Local Knowledge Base',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def generar_respuesta_local(mensaje):
    """Genera respuestas basadas en conocimiento local del TFM"""
    mensaje_lower = mensaje.lower()
    
    if any(word in mensaje_lower for word in ['tfm', 'validacion', 'agosto', 'hipotesis']):
        return """🎯 **Validación TFM Agosto 2025 - Resultados Confirmados:**

• **Precisión**: 100% en compresor C1 (2/2 eventos detectados)
• **Anticipación**: 15 días promedio (rango 6-24 días)
• **Confianza**: 95% promedio (92.1% - 97.8%)
• **Hipótesis Confirmada**: THD predice fallas mecánicas

**Eventos Validados:**
- 01 Ago: Predicción IA → 07 Ago: ICM real (6 días anticipación)
- 03 Ago: Predicción IA → 25 Ago: ICM real (22 días anticipación)"""

    elif any(word in mensaje_lower for word in ['mtbf', 'mttr', 'disponibilidad']):
        return """⚡ **KPIs de Confiabilidad del Sistema:**

• **MTBF**: 156.3 horas (objetivo >100h ✅)
• **MTTR**: 4.2 horas (objetivo <6h ✅)  
• **Disponibilidad**: 97.4% (objetivo >95% ✅)

**Fórmulas:**
- MTBF = Tiempo total operativo / Número de fallos
- MTTR = Tiempo total reparación / Número de reparaciones
- Disponibilidad = MTBF / (MTBF + MTTR) × 100"""

    else:
        return """🤖 **Experto en Mantenimiento Industrial TFM**

Puedo ayudarte con:
• Validación agosto 2025 (precisión 100%)
• Cálculos técnicos (MTBF, MTTR, ROI)
• Análisis de compresores C1, C2, C3
• THD y análisis eléctrico
• Mantenimiento predictivo

**¿Qué te interesa saber específicamente?**"""

# ============================================================================
# INICIALIZACIÓN
# ============================================================================

def inicializar_aplicacion():
    """Inicializa la aplicación y la base de datos"""
    print("🎉 Inicializando Sistema TFM Multi-página...")
    
    # Crear base de datos si no existe
    init_database()
    cargar_datos_iniciales()
    
    print("✅ Base de datos SQLite inicializada")
    print("📊 Datos del TFM cargados")
    print("🌐 Páginas HTML separadas creadas")
    print("🤖 Chat disponible en /chat")

if __name__ == '__main__':
    inicializar_aplicacion()
    
    port = int(os.environ.get('PORT', 5001))
    print(f"\n🚀 Sistema TFM Multi-página ejecutándose en: http://localhost:{port}")
    print("📱 Cada sección tiene su propia página HTML")
    print("🔗 Navegación entre páginas independientes")
    
    app.run(host='0.0.0.0', port=port, debug=True)

