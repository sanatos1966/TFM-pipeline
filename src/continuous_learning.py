"""
Módulo de Aprendizaje Continuo para TFM-pipeline
Maneja la carga, procesamiento y diagnóstico de nuevos datos
"""

import pandas as pd
import numpy as np
import joblib
from datetime import datetime
from pathlib import Path
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContinuousLearningSystem:
    """Sistema de aprendizaje continuo para el modelo predictivo"""
    
    def __init__(self, base_path='C:/TFM-pipeline'):
        self.base_path = Path(base_path)
        self.data_path = self.base_path / 'data' / 'raw'
        self.model_path = self.base_path / 'output' / 'modelo_ensemble_tfm.pkl'
        self.output_path = self.base_path / 'output'
        
        # Cargar modelo actual
        self.modelo_actual = None
        self.version_actual = None
        self.cargar_modelo_produccion()
        
    def cargar_modelo_produccion(self):
        """Carga el modelo actualmente en producción"""
        try:
            self.modelo_actual = joblib.load(self.model_path)
            # Leer versión desde metadata
            metadata_path = self.base_path / 'models' / 'produccion' / 'metadata.json'
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    self.version_actual = metadata.get('version', 'v1.0')
            else:
                self.version_actual = 'v1.0'
            
            logger.info(f"Modelo {self.version_actual} cargado exitosamente")
            return True
        except Exception as e:
            logger.error(f"Error al cargar modelo: {e}")
            return False
    
    def cargar_datos_nuevos(self, archivo_path, mes, anio, compresor):
        """
        Carga y valida un nuevo archivo de datos
        
        Args:
            archivo_path: Ruta al archivo (CSV, Excel, PDF)
            mes: Mes de los datos (01-12)
            anio: Año de los datos
            compresor: ID del compresor (C1, C2, C3, TODOS)
        
        Returns:
            DataFrame con los datos cargados
        """
        logger.info(f"Cargando datos: {archivo_path}")
        
        try:
            # Detectar tipo de archivo y cargar
            if archivo_path.endswith('.csv'):
                df = pd.read_csv(archivo_path)
            elif archivo_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(archivo_path)
            elif archivo_path.endswith('.pdf'):
                # Para PDFs, necesitaríamos un parser específico
                raise NotImplementedError("Carga de PDF no implementada aún")
            else:
                raise ValueError(f"Formato de archivo no soportado: {archivo_path}")
            
            # Agregar metadata
            df['mes_carga'] = mes
            df['anio_carga'] = anio
            df['compresor_carga'] = compresor
            df['fecha_carga'] = datetime.now()
            
            logger.info(f"Datos cargados: {len(df)} registros")
            return df
            
        except Exception as e:
            logger.error(f"Error al cargar datos: {e}")
            raise
    
    def preprocesar_datos(self, df):
        """
        Preprocesa los datos siguiendo el mismo pipeline del entrenamiento
        
        Args:
            df: DataFrame con datos crudos
        
        Returns:
            DataFrame preprocesado
        """
        logger.info("Preprocesando datos...")
        
        df_procesado = df.copy()
        
        try:
            # 1. Convertir timestamp a datetime
            if 'timestamp' in df_procesado.columns:
                df_procesado['timestamp'] = pd.to_datetime(df_procesado['timestamp'])
            
            # 2. Eliminar duplicados
            df_procesado = df_procesado.drop_duplicates()
            
            # 3. Manejar valores faltantes
            # No imputar si Potencia_Activa == 0 (compresor parado)
            if 'Potencia_Activa' in df_procesado.columns:
                mask_funcionando = df_procesado['Potencia_Activa'] > 0
                
                # Solo procesar registros donde el compresor está funcionando
                df_funcionando = df_procesado[mask_funcionando].copy()
                
                # Imputar valores faltantes con la mediana
                columnas_numericas = df_funcionando.select_dtypes(include=[np.number]).columns
                for col in columnas_numericas:
                    if df_funcionando[col].isna().any():
                        mediana = df_funcionando[col].median()
                        df_funcionando[col].fillna(mediana, inplace=True)
                
                # Combinar de vuelta
                df_procesado = pd.concat([df_funcionando, df_procesado[~mask_funcionando]])
            
            # 4. Detectar y marcar outliers (pero no eliminar)
            # Los outliers son candidatos a anomalías
            columnas_excluir_outliers = ['Potencia_Total', 'Potencia_A', 'Potencia_B', 
                                         'Potencia_C', 'Potencia_Activa']
            
            for col in df_procesado.select_dtypes(include=[np.number]).columns:
                if col not in columnas_excluir_outliers:
                    Q1 = df_procesado[col].quantile(0.25)
                    Q3 = df_procesado[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower = Q1 - 1.5 * IQR
                    upper = Q3 + 1.5 * IQR
                    
                    df_procesado[f'{col}_is_outlier'] = (
                        (df_procesado[col] < lower) | (df_procesado[col] > upper)
                    )
            
            logger.info(f"Preprocesamiento completado: {len(df_procesado)} registros")
            return df_procesado
            
        except Exception as e:
            logger.error(f"Error en preprocesamiento: {e}")
            raise
    
    def diagnosticar_con_modelo_actual(self, df):
        """
        Ejecuta el modelo actual sobre los nuevos datos
        
        Args:
            df: DataFrame preprocesado
        
        Returns:
            DataFrame con predicciones agregadas
        """
        logger.info("Ejecutando diagnóstico con modelo actual...")
        
        try:
            # Seleccionar features relevantes (las mismas del entrenamiento)
            features = [
                'THD_V_A', 'THD_V_B', 'THD_V_C',
                'THD_I_A', 'THD_I_B', 'THD_I_C',
                'Potencia_Activa', 'Factor_Potencia',
                'Demanda_A', 'Demanda_B', 'Demanda_C'
            ]
            
            # Verificar que todas las features existen
            features_disponibles = [f for f in features if f in df.columns]
            
            if len(features_disponibles) < len(features):
                logger.warning(f"Faltan features: {set(features) - set(features_disponibles)}")
            
            # Preparar datos para el modelo
            X = df[features_disponibles].copy()
            
            # Eliminar filas con NaN en las features
            X_clean = X.dropna()
            indices_validos = X_clean.index
            
            # Predecir
            if hasattr(self.modelo_actual, 'predict'):
                predicciones = self.modelo_actual.predict(X_clean)
            else:
                # Si es un ensemble, puede tener diferentes métodos
                predicciones = self.modelo_actual.predict(X_clean)
            
            # Agregar predicciones al DataFrame
            df['prediccion'] = np.nan
            df.loc[indices_validos, 'prediccion'] = predicciones
            
            # -1 indica anomalía en Isolation Forest
            df['es_anomalia'] = df['prediccion'] == -1
            
            # Calcular score de anomalía si está disponible
            if hasattr(self.modelo_actual, 'score_samples'):
                scores = self.modelo_actual.score_samples(X_clean)
                df['anomaly_score'] = np.nan
                df.loc[indices_validos, 'anomaly_score'] = scores
                
                # Convertir score a confianza (0-100%)
                # Scores más negativos = más anómalos
                df['confianza_anomalia'] = np.nan
                df.loc[indices_validos, 'confianza_anomalia'] = (
                    100 * (1 - np.exp(scores))
                )
            
            num_anomalias = df['es_anomalia'].sum()
            logger.info(f"Diagnóstico completado: {num_anomalias} anomalías detectadas")
            
            return df
            
        except Exception as e:
            logger.error(f"Error en diagnóstico: {e}")
            raise
    
    def generar_predicciones(self, df, mes, anio):
        """
        Genera predicciones estructuradas desde el DataFrame diagnosticado
        
        Args:
            df: DataFrame con diagnóstico
            mes: Mes de los datos
            anio: Año de los datos
        
        Returns:
            Lista de diccionarios con predicciones
        """
        logger.info("Generando predicciones estructuradas...")
        
        predicciones = []
        
        # Filtrar solo anomalías
        df_anomalias = df[df['es_anomalia'] == True].copy()
        
        for idx, row in df_anomalias.iterrows():
            # Identificar tipo de anomalía basado en variables críticas
            tipo_anomalia = self._identificar_tipo_anomalia(row)
            severidad = self._calcular_severidad(row)
            
            prediccion = {
                'id': f"PRED-{anio}{mes}-{idx}",
                'fecha_prediccion': row.get('timestamp', datetime.now()),
                'compresor': row.get('compresor_carga', 'DESCONOCIDO'),
                'tipo_anomalia': tipo_anomalia,
                'severidad': severidad,
                'confianza': row.get('confianza_anomalia', 0),
                'variables_criticas': self._obtener_variables_criticas(row),
                'mes': mes,
                'anio': anio,
                'modelo_version': self.version_actual
            }
            
            predicciones.append(prediccion)
        
        logger.info(f"Generadas {len(predicciones)} predicciones")
        return predicciones
    
    def _identificar_tipo_anomalia(self, row):
        """Identifica el tipo de anomalía basado en las variables"""
        # Priorizar por THD
        if any(row.get(f'THD_V_{fase}_is_outlier', False) for fase in ['A', 'B', 'C']):
            return 'THD_Voltaje'
        elif any(row.get(f'THD_I_{fase}_is_outlier', False) for fase in ['A', 'B', 'C']):
            return 'THD_Corriente'
        elif row.get('Potencia_Activa_is_outlier', False):
            return 'Potencia_Activa'
        elif row.get('Factor_Potencia_is_outlier', False):
            return 'Factor_Potencia'
        else:
            return 'Anomalia_General'
    
    def _calcular_severidad(self, row):
        """Calcula la severidad de la anomalía"""
        confianza = row.get('confianza_anomalia', 0)
        
        if confianza >= 95:
            return 'CRITICA'
        elif confianza >= 85:
            return 'ALTA'
        elif confianza >= 70:
            return 'MEDIA'
        else:
            return 'BAJA'
    
    def _obtener_variables_criticas(self, row):
        """Obtiene las variables que están fuera de rango"""
        variables = []
        
        for col in row.index:
            if col.endswith('_is_outlier') and row[col]:
                var_name = col.replace('_is_outlier', '')
                variables.append(var_name)
        
        return variables
    
    def guardar_resultados(self, df, predicciones, mes, anio):
        """
        Guarda los resultados del diagnóstico
        
        Args:
            df: DataFrame con diagnóstico completo
            predicciones: Lista de predicciones
            mes: Mes de los datos
            anio: Año de los datos
        
        Returns:
            Diccionario con rutas de archivos guardados
        """
        logger.info("Guardando resultados...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        periodo = f"{anio}{mes}"
        
        # Crear carpeta para este periodo
        periodo_path = self.output_path / 'diagnosticos' / periodo
        periodo_path.mkdir(parents=True, exist_ok=True)
        
        archivos_guardados = {}
        
        try:
            # 1. Guardar DataFrame completo
            df_path = periodo_path / f'diagnostico_completo_{timestamp}.csv'
            df.to_csv(df_path, index=False)
            archivos_guardados['diagnostico_completo'] = str(df_path)
            
            # 2. Guardar solo anomalías
            df_anomalias = df[df['es_anomalia'] == True]
            anomalias_path = periodo_path / f'anomalias_{timestamp}.csv'
            df_anomalias.to_csv(anomalias_path, index=False)
            archivos_guardados['anomalias'] = str(anomalias_path)
            
            # 3. Guardar predicciones en JSON
            predicciones_path = periodo_path / f'predicciones_{timestamp}.json'
            with open(predicciones_path, 'w') as f:
                json.dump(predicciones, f, indent=2, default=str)
            archivos_guardados['predicciones'] = str(predicciones_path)
            
            # 4. Guardar resumen
            resumen = {
                'periodo': periodo,
                'timestamp': timestamp,
                'total_registros': len(df),
                'anomalias_detectadas': len(df_anomalias),
                'predicciones_generadas': len(predicciones),
                'modelo_version': self.version_actual,
                'archivos': archivos_guardados
            }
            
            resumen_path = periodo_path / f'resumen_{timestamp}.json'
            with open(resumen_path, 'w') as f:
                json.dump(resumen, f, indent=2)
            archivos_guardados['resumen'] = str(resumen_path)
            
            logger.info(f"Resultados guardados en: {periodo_path}")
            return archivos_guardados
            
        except Exception as e:
            logger.error(f"Error al guardar resultados: {e}")
            raise


# Funciones auxiliares para uso en Flask
def procesar_archivo_nuevo(archivo_path, mes, anio, compresor):
    """
    Función principal para procesar un archivo nuevo
    
    Returns:
        Diccionario con resultados del procesamiento
    """
    sistema = ContinuousLearningSystem()
    
    # 1. Cargar datos
    df = sistema.cargar_datos_nuevos(archivo_path, mes, anio, compresor)
    
    # 2. Preprocesar
    df_procesado = sistema.preprocesar_datos(df)
    
    # 3. Diagnosticar
    df_diagnosticado = sistema.diagnosticar_con_modelo_actual(df_procesado)
    
    # 4. Generar predicciones
    predicciones = sistema.generar_predicciones(df_diagnosticado, mes, anio)
    
    # 5. Guardar resultados
    archivos = sistema.guardar_resultados(df_diagnosticado, predicciones, mes, anio)
    
    return {
        'exito': True,
        'total_registros': len(df),
        'anomalias_detectadas': len(predicciones),
        'predicciones': predicciones,
        'archivos': archivos
    }


if __name__ == '__main__':
    # Ejemplo de uso
    print("Sistema de Aprendizaje Continuo - TFM Pipeline")
    print("=" * 50)
    
    sistema = ContinuousLearningSystem()
    print(f"Modelo actual: {sistema.version_actual}")
    print(f"Ruta del modelo: {sistema.model_path}")

