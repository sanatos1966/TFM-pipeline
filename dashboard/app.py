#!/usr/bin/env python3
"""
TFM - Sistema Predictivo Frio Pacifico 1
Aplicacion Web Multi-pagina con HTML separados
Version: 3.0 - Con sistema de aprendizaje continuo
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
import random
import sqlite3
from pathlib import Path
import sys

# Agregar ruta de modulos
sys.path.append(str(Path(__file__).parent.parent / 'src'))

# Importar modulos de aprendizaje continuo
try:
    from continuous_learning import procesar_archivo_nuevo, ContinuousLearningSystem
    from model_retraining import ModelRetrainingSystem
    APRENDIZAJE_CONTINUO_DISPONIBLE = True
except ImportError:
    APRENDIZAJE_CONTINUO_DISPONIBLE = False
    print("ADVERTENCIA: Modulos de aprendizaje continuo no disponibles")

# Configuracion de la aplicacion
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'tfm_sistema_predictivo_2025_multipagina'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Crear directorio de base de datos si no existe
DB_DIR = Path(__file__).parent / 'database'
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / 'tfm_multipagina.db'

# Crear directorio temporal para uploads
UPLOAD_DIR = Path(__file__).parent.parent / 'temp' / 'uploads'
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# DATOS DEL TFM VALIDADOS
# ============================================================================

TFM_DATA = {
    'sistema': {
        'nombre': 'TFM - Sistema Predictivo Frio Pacifico 1',
        'version': '3.0 Multi-pagina con Aprendizaje Continuo',
        'estado': 'Operativo',
        'institucion': 'EADIC 2025 - Master en Mantenimiento Industrial',
        'autor': 'Antonio Cantos',
        'fecha_validacion': '2025-08-31',
        'aprendizaje_continuo': APRENDIZAJE_CONTINUO_DISPONIBLE
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
            'nombre': 'Compresor C1 - Anfitrion THD',
            'tipo': 'Anfitrion con monitoreo THD',
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
            'tipo': 'Monitoreo de vibraciones mecanicas',
            'estado': 'Operativo',
            'variables_monitoreadas': 8,
            'tipos_variables': ['Presion', 'Temperatura', 'Vibracion_X', 'Vibracion_Y', 'Vibracion_Z', 'Velocidad', 'Aceleracion', 'Desplazamiento'],
            'precision_estimada': 87.5,
            'eventos_detectados_agosto': 0,
            'monitoreo_continuo': True
        },
        {
            'id': 'C3_REF-014',
            'nombre': 'Compresor C3 - Basico',
            'tipo': 'Monitoreo basico mecanico',
            'estado': 'Operativo',
            'variables_monitoreadas': 6,
            'tipos_variables': ['Presion', 'Temperatura', 'Caudal', 'Potencia', 'Corriente', 'Voltaje'],
            'precision_estimada': 65.0,
            'eventos_detectados_agosto': 0,
            'recomendacion': 'Añadir sensores de vibracion'
        }
    ]
}

# ============================================================================
# FUNCIONES DE BASE DE DATOS
# ============================================================================

def init_database():
    """Inicializa la base de datos SQLite"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabla de ordenes de trabajo
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
    
    # Tabla de historial de eventos
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
    
    # Tabla de predicciones (para aprendizaje continuo)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predicciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pred_id TEXT UNIQUE NOT NULL,
            mes TEXT NOT NULL,
            anio TEXT NOT NULL,
            compresor TEXT NOT NULL,
            fecha_prediccion DATE NOT NULL,
            tipo_anomalia TEXT,
            severidad TEXT,
            confianza REAL,
            variables_criticas TEXT,
            modelo_version TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de validaciones (para aprendizaje continuo)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS validaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pred_id TEXT NOT NULL,
            evento_ocurrio BOOLEAN NOT NULL,
            fecha_evento_real DATE,
            tipo_falla_real TEXT,
            ot_real TEXT,
            notas TEXT,
            validado_por TEXT,
            validado_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pred_id) REFERENCES predicciones(pred_id)
        )
    ''')
    
    # Tabla de versiones del modelo (para aprendizaje continuo)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS versiones_modelo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT UNIQUE NOT NULL,
            fecha_creacion TIMESTAMP NOT NULL,
            ruta_archivo TEXT NOT NULL,
            datos_entrenamiento TEXT,
            precision REAL,
            recall REAL,
            f1_score REAL,
            auc_roc REAL,
            registros_entrenamiento INTEGER,
            en_produccion BOOLEAN DEFAULT 0,
            metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        ('OT-2025-001', 'C1_REF-012', 'Predictivo', 'CRITICO', 'THD elevado detectado - Revision electrica requerida', '2025-08-01 10:30:00', '2025-08-08 10:30:00', 'Completada', 1250.00, 'Juan Perez', 'Revision completada, THD normalizado'),
        ('OT-2025-002', 'C1_REF-012', 'Predictivo', 'CRITICO', 'Anomalia en THD_Voltaje_A - Mantenimiento preventivo', '2025-08-03 14:15:00', '2025-08-10 14:15:00', 'Completada', 980.00, 'Maria Garcia', 'Conexiones electricas revisadas'),
        ('OT-2025-003', 'C2_REF-013', 'Preventivo', 'ALERTA', 'Mantenimiento rutinario de vibraciones', '2025-08-15 09:00:00', '2025-08-22 09:00:00', 'En Proceso', 450.00, 'Carlos Lopez', 'Analisis de vibraciones en curso'),
        ('OT-2025-004', 'C3_REF-014', 'Correctivo', 'ATENCION', 'Revision de presion - Lectura irregular', '2025-08-20 16:45:00', '2025-08-27 16:45:00', 'Pendiente', 320.00, None, None),
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
# RUTAS PRINCIPALES - PAGINAS HTML SEPARADAS
# ============================================================================

@app.route('/')
def dashboard():
    """Pagina principal - Dashboard Ejecutivo"""
    return render_template('dashboard.html', 
                         kpis=TFM_DATA['kpis_principales'],
                         compresores=TFM_DATA['compresores'],
                         sistema=TFM_DATA['sistema'])

@app.route('/compresores')
def compresores():
    """Pagina de Analisis de Compresores"""
    return render_template('compresores.html', 
                         compresores=TFM_DATA['compresores'],
                         sistema=TFM_DATA['sistema'])

@app.route('/deteccion')
def deteccion():
    """Pagina de Deteccion Avanzada"""
    return render_template('deteccion.html', 
                         sistema=TFM_DATA['sistema'])

@app.route('/ots')
def ots():
    """Pagina de Ordenes de Trabajo"""
    return render_template('ots.html', 
                         sistema=TFM_DATA['sistema'])

@app.route('/economico')
def economico():
    """Pagina de Analisis Economico"""
    return render_template('economico.html', 
                         kpis=TFM_DATA['kpis_principales'],
                         sistema=TFM_DATA['sistema'])

@app.route('/validacion')
def validacion():
    """Pagina de Validacion del Modelo"""
    return render_template('validacion.html', 
                         sistema=TFM_DATA['sistema'])

@app.route('/reportes')
def reportes():
    """Pagina de Reportes"""
    return render_template('reportes.html', 
                         sistema=TFM_DATA['sistema'])

@app.route('/configuracion')
def configuracion():
    """Pagina de Configuracion"""
    return render_template('configuracion.html', 
                         sistema=TFM_DATA['sistema'])

@app.route('/chat')
def chat_page():
    """Pagina dedicada al Chat"""
    return render_template('chat.html', 
                         sistema=TFM_DATA['sistema'])

# ============================================================================
# RUTAS DE APRENDIZAJE CONTINUO
# ============================================================================

@app.route('/carga')
def carga_datos():
    """Pagina de carga de datos"""
    if not APRENDIZAJE_CONTINUO_DISPONIBLE:
        return "Modulo de aprendizaje continuo no disponible", 503
    
    return render_template('carga_datos.html', 
                         sistema=TFM_DATA['sistema'])

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """API para procesar archivo subido"""
    if not APRENDIZAJE_CONTINUO_DISPONIBLE:
        return jsonify({'exito': False, 'error': 'Modulo no disponible'}), 503
    
    try:
        # Verificar que se subio un archivo
        if 'archivo' not in request.files:
            return jsonify({'exito': False, 'error': 'No se subio ningun archivo'}), 400
        
        archivo = request.files['archivo']
        if archivo.filename == '':
            return jsonify({'exito': False, 'error': 'Nombre de archivo vacio'}), 400
        
        # Obtener parametros
        mes = request.form.get('mes')
        anio = request.form.get('anio')
        compresor = request.form.get('compresor')
        
        if not all([mes, anio, compresor]):
            return jsonify({'exito': False, 'error': 'Faltan parametros requeridos'}), 400
        
        # Guardar archivo temporalmente
        filename = f"{anio}{mes}_{compresor}_{archivo.filename}"
        temp_path = UPLOAD_DIR / filename
        archivo.save(temp_path)
        
        # Procesar archivo
        resultado = procesar_archivo_nuevo(str(temp_path), mes, anio, compresor)
        
        # Guardar predicciones en base de datos
        if resultado['exito'] and resultado.get('predicciones'):
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            for pred in resultado['predicciones']:
                try:
                    cursor.execute('''
                        INSERT INTO predicciones 
                        (pred_id, mes, anio, compresor, fecha_prediccion, tipo_anomalia, 
                         severidad, confianza, variables_criticas, modelo_version)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        pred['id'], pred['mes'], pred['anio'], pred['compresor'],
                        pred['fecha_prediccion'], pred['tipo_anomalia'], pred['severidad'],
                        pred['confianza'], json.dumps(pred['variables_criticas']), pred['modelo_version']
                    ))
                except sqlite3.IntegrityError:
                    pass  # Prediccion ya existe
            
            conn.commit()
            conn.close()
        
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 500

@app.route('/validacion_predicciones')
def validacion_predicciones():
    """Pagina de validacion de predicciones"""
    if not APRENDIZAJE_CONTINUO_DISPONIBLE:
        return "Modulo de aprendizaje continuo no disponible", 503
    
    return render_template('validacion_predicciones.html', 
                         sistema=TFM_DATA['sistema'])

@app.route('/api/predicciones')
def api_predicciones():
    """API para obtener predicciones"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Filtros opcionales
        mes = request.args.get('mes')
        anio = request.args.get('anio')
        compresor = request.args.get('compresor')
        
        query = 'SELECT * FROM predicciones WHERE 1=1'
        params = []
        
        if mes:
            query += ' AND mes = ?'
            params.append(mes)
        if anio:
            query += ' AND anio = ?'
            params.append(anio)
        if compresor:
            query += ' AND compresor = ?'
            params.append(compresor)
        
        query += ' ORDER BY fecha_prediccion DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        predicciones = []
        for row in rows:
            predicciones.append({
                'id': row[0],
                'pred_id': row[1],
                'mes': row[2],
                'anio': row[3],
                'compresor': row[4],
                'fecha_prediccion': row[5],
                'tipo_anomalia': row[6],
                'severidad': row[7],
                'confianza': row[8],
                'variables_criticas': json.loads(row[9]) if row[9] else [],
                'modelo_version': row[10]
            })
        
        conn.close()
        
        return jsonify({
            'exito': True,
            'predicciones': predicciones,
            'total': len(predicciones)
        })
        
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 500

@app.route('/api/validar', methods=['POST'])
def api_validar():
    """API para guardar validacion de prediccion"""
    try:
        datos = request.json
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO validaciones 
            (pred_id, evento_ocurrio, fecha_evento_real, tipo_falla_real, 
             ot_real, notas, validado_por)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datos['pred_id'],
            datos['evento_ocurrio'],
            datos.get('fecha_evento_real'),
            datos.get('tipo_falla_real'),
            datos.get('ot_real'),
            datos.get('notas'),
            datos.get('validado_por', 'Sistema')
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'exito': True})
        
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 500

@app.route('/evolucion_modelo')
def evolucion_modelo():
    """Dashboard de evolucion del modelo"""
    if not APRENDIZAJE_CONTINUO_DISPONIBLE:
        return "Modulo de aprendizaje continuo no disponible", 503
    
    return render_template('evolucion_modelo.html', 
                         sistema=TFM_DATA['sistema'])

@app.route('/api/versiones_modelo')
def api_versiones_modelo():
    """API para obtener versiones del modelo"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT version, fecha_creacion, precision, f1_score, 
                   registros_entrenamiento, en_produccion
            FROM versiones_modelo
            ORDER BY fecha_creacion DESC
        ''')
        rows = cursor.fetchall()
        
        versiones = []
        for row in rows:
            versiones.append({
                'version': row[0],
                'fecha_creacion': row[1],
                'precision': row[2],
                'f1_score': row[3],
                'registros_entrenamiento': row[4],
                'en_produccion': bool(row[5])
            })
        
        conn.close()
        
        return jsonify({
            'exito': True,
            'versiones': versiones,
            'total': len(versiones)
        })
        
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 500

@app.route('/api/reentrenar', methods=['POST'])
def api_reentrenar():
    """API para ejecutar reentrenamiento manual"""
    if not APRENDIZAJE_CONTINUO_DISPONIBLE:
        return jsonify({'exito': False, 'error': 'Modulo no disponible'}), 503
    
    try:
        datos = request.json or {}
        hasta_mes = datos.get('hasta_mes')
        hasta_anio = datos.get('hasta_anio')
        nueva_version = datos.get('nueva_version')
        
        sistema = ModelRetrainingSystem()
        resultado = sistema.reentrenar_automatico(hasta_mes, hasta_anio, nueva_version)
        
        # Guardar version en base de datos si fue exitoso
        if resultado['exito']:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    INSERT INTO versiones_modelo 
                    (version, fecha_creacion, ruta_archivo, precision, f1_score, 
                     registros_entrenamiento, en_produccion, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    resultado['version'],
                    datetime.now().isoformat(),
                    resultado['ruta_modelo'],
                    resultado['metricas'].get('precision'),
                    resultado['metricas'].get('f1_score'),
                    resultado['metricas'].get('total_registros'),
                    resultado['actualizado_produccion'],
                    json.dumps(resultado['metricas'])
                ))
                
                # Si se actualizo produccion, marcar otras versiones como no produccion
                if resultado['actualizado_produccion']:
                    cursor.execute('''
                        UPDATE versiones_modelo 
                        SET en_produccion = 0 
                        WHERE version != ?
                    ''', (resultado['version'],))
                
                conn.commit()
            except sqlite3.IntegrityError:
                pass  # Version ya existe
            
            conn.close()
        
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 500

# ============================================================================
# RUTAS DE API ORIGINALES
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
        'base_datos': 'SQLite Multi-pagina',
        'chat_disponible': True,
        'aprendizaje_continuo': APRENDIZAJE_CONTINUO_DISPONIBLE
    })

@app.route('/api/ots')
def obtener_ots():
    """Obtiene las ordenes de trabajo de la base de datos"""
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

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint del chat IA"""
    try:
        data = request.json
        mensaje_usuario = data.get('mensaje', '')
        
        # Respuestas predefinidas basadas en el TFM
        respuestas = {
            'precision': f"La precision global del sistema es del {TFM_DATA['kpis_principales']['precision_global']}%, validada en agosto 2025.",
            'roi': f"El ROI del primer año es del {TFM_DATA['kpis_principales']['roi_primer_año']}%.",
            'costos': f"El costo total del 2025 es de ${TFM_DATA['kpis_principales']['costo_total_2025']:,.2f}, con un ahorro estimado de ${TFM_DATA['kpis_principales']['ahorro_estimado']:,.2f}.",
            'compresores': f"Actualmente monitoreamos {len(TFM_DATA['compresores'])} compresores: C1 (THD), C2 (Vibraciones) y C3 (Basico).",
            'c1': "El Compresor C1 es el anfitrion con monitoreo THD. Tiene una precision validada del 100% y detecto 2 eventos en agosto 2025.",
            'c2': "El Compresor C2 monitorea vibraciones mecanicas con 8 variables. Tiene una precision estimada del 87.5%.",
            'c3': "El Compresor C3 tiene monitoreo basico con 6 variables. Se recomienda añadir sensores de vibracion.",
            'mtbf': f"El MTBF (Mean Time Between Failures) es de {TFM_DATA['kpis_principales']['mtbf_horas']} horas.",
            'mttr': f"El MTTR (Mean Time To Repair) es de {TFM_DATA['kpis_principales']['mttr_horas']} horas."
        }
        
        # Buscar palabra clave en el mensaje
        mensaje_lower = mensaje_usuario.lower()
        respuesta = "Lo siento, no tengo informacion especifica sobre eso. Puedes preguntar sobre: precision, ROI, costos, compresores, MTBF, MTTR, C1, C2 o C3."
        
        for palabra_clave, texto_respuesta in respuestas.items():
            if palabra_clave in mensaje_lower:
                respuesta = texto_respuesta
                break
        
        return jsonify({
            'respuesta': respuesta,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# INICIALIZACION Y EJECUCION
# ============================================================================

def inicializar_aplicacion():
    """Inicializa la aplicacion y la base de datos"""
    print("Inicializando Sistema TFM Multi-pagina...")
    print("Accede a: http://localhost:5000")
    print("Paginas HTML separadas creadas")
    print("Chat disponible en /chat")
    if APRENDIZAJE_CONTINUO_DISPONIBLE:
        print("Sistema de aprendizaje continuo disponible")
        print("- Carga de datos: /carga")
        print("- Validacion: /validacion_predicciones")
        print("- Evolucion: /evolucion_modelo")
    else:
        print("ADVERTENCIA: Sistema de aprendizaje continuo no disponible")
    
    # Crear base de datos
    init_database()
    print("Base de datos SQLite inicializada")
    
    # Cargar datos iniciales
    cargar_datos_iniciales()
    print("Datos del TFM cargados")
    
    print("\nSistema TFM Multi-pagina ejecutandose en: http://localhost:5000")
    print("Cada seccion tiene su propia pagina HTML")
    print("Navegacion entre paginas independientes")

if __name__ == '__main__':
    inicializar_aplicacion()
    
    # Ejecutar aplicacion
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )

