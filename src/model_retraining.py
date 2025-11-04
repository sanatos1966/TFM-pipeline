"""
Módulo de Reentrenamiento Automático para TFM-pipeline
Maneja el reentrenamiento del modelo con datos validados
"""

import pandas as pd
import numpy as np
import joblib
from datetime import datetime
from pathlib import Path
import json
import logging
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelRetrainingSystem:
    """Sistema de reentrenamiento automático del modelo"""
    
    def __init__(self, base_path='C:/TFM-pipeline'):
        self.base_path = Path(base_path)
        self.data_path = self.base_path / 'data' / 'raw'
        self.models_path = self.base_path / 'models'
        self.output_path = self.base_path / 'output'
        
        # Crear estructura de carpetas
        (self.models_path / 'produccion').mkdir(parents=True, exist_ok=True)
        (self.models_path / 'versiones').mkdir(parents=True, exist_ok=True)
        
    def obtener_datos_validados(self, hasta_mes=None, hasta_anio=None):
        """
        Obtiene todos los datos validados hasta un periodo específico
        
        Args:
            hasta_mes: Mes límite (None = todos)
            hasta_anio: Año límite (None = todos)
        
        Returns:
            DataFrame con todos los datos validados
        """
        logger.info("Obteniendo datos validados...")
        
        # Buscar todos los archivos de datos
        archivos_datos = []
        
        # Datos originales de entrenamiento (Ene-Jul 2025)
        for archivo in self.data_path.glob('Compresor*.xlsx'):
            archivos_datos.append(archivo)
        
        # Datos nuevos procesados
        diagnosticos_path = self.output_path / 'diagnosticos'
        if diagnosticos_path.exists():
            for periodo_dir in diagnosticos_path.iterdir():
                if periodo_dir.is_dir():
                    # Buscar archivos de diagnóstico
                    for archivo in periodo_dir.glob('diagnostico_completo_*.csv'):
                        archivos_datos.append(archivo)
        
        # Cargar y combinar todos los datos
        dfs = []
        for archivo in archivos_datos:
            try:
                if archivo.suffix == '.xlsx':
                    df = pd.read_excel(archivo)
                elif archivo.suffix == '.csv':
                    df = pd.read_csv(archivo)
                else:
                    continue
                
                dfs.append(df)
                logger.info(f"Cargado: {archivo.name} ({len(df)} registros)")
            except Exception as e:
                logger.warning(f"Error al cargar {archivo}: {e}")
        
        if not dfs:
            raise ValueError("No se encontraron datos para entrenar")
        
        # Combinar todos los DataFrames
        df_completo = pd.concat(dfs, ignore_index=True)
        
        # Eliminar duplicados
        df_completo = df_completo.drop_duplicates()
        
        logger.info(f"Total de datos obtenidos: {len(df_completo)} registros")
        return df_completo
    
    def preprocesar_datos_entrenamiento(self, df):
        """
        Preprocesa datos para entrenamiento
        
        Args:
            df: DataFrame con datos crudos
        
        Returns:
            X: Features preprocesadas
            y: Labels (si existen)
        """
        logger.info("Preprocesando datos para entrenamiento...")
        
        df_procesado = df.copy()
        
        # Seleccionar features relevantes
        features = [
            'THD_V_A', 'THD_V_B', 'THD_V_C',
            'THD_I_A', 'THD_I_B', 'THD_I_C',
            'Potencia_Activa', 'Factor_Potencia',
            'Demanda_A', 'Demanda_B', 'Demanda_C'
        ]
        
        # Verificar features disponibles
        features_disponibles = [f for f in features if f in df_procesado.columns]
        
        if len(features_disponibles) < len(features):
            logger.warning(f"Faltan features: {set(features) - set(features_disponibles)}")
        
        # Extraer features
        X = df_procesado[features_disponibles].copy()
        
        # Eliminar filas con NaN
        X = X.dropna()
        
        # Normalizar
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=features_disponibles, index=X.index)
        
        # Si existen labels (para validación supervisada)
        y = None
        if 'es_anomalia' in df_procesado.columns:
            y = df_procesado.loc[X.index, 'es_anomalia']
        
        logger.info(f"Datos preprocesados: {len(X_scaled)} registros, {len(features_disponibles)} features")
        
        return X_scaled, y, scaler
    
    def entrenar_modelo_ensemble(self, X, y=None):
        """
        Entrena el modelo Ensemble (Isolation Forest + DBSCAN)
        
        Args:
            X: Features preprocesadas
            y: Labels (opcional, para validación)
        
        Returns:
            Modelo entrenado
        """
        logger.info("Entrenando modelo Ensemble...")
        
        # Configuración del modelo (mismos parámetros que el original)
        iso_forest = IsolationForest(
            n_estimators=100,
            contamination=0.1,
            random_state=42,
            n_jobs=-1
        )
        
        # Entrenar Isolation Forest
        logger.info("Entrenando Isolation Forest...")
        iso_forest.fit(X)
        
        # Predecir con Isolation Forest
        pred_iso = iso_forest.predict(X)
        
        # Entrenar DBSCAN en las anomalías detectadas por Isolation Forest
        logger.info("Entrenando DBSCAN...")
        anomalias_iso = X[pred_iso == -1]
        
        if len(anomalias_iso) > 0:
            dbscan = DBSCAN(eps=0.5, min_samples=5)
            dbscan.fit(anomalias_iso)
            
            # Crear modelo ensemble
            modelo_ensemble = {
                'isolation_forest': iso_forest,
                'dbscan': dbscan,
                'tipo': 'ensemble',
                'features': list(X.columns)
            }
        else:
            logger.warning("No se detectaron anomalías con Isolation Forest, solo se usará IF")
            modelo_ensemble = {
                'isolation_forest': iso_forest,
                'dbscan': None,
                'tipo': 'isolation_forest_only',
                'features': list(X.columns)
            }
        
        logger.info("Modelo Ensemble entrenado exitosamente")
        return modelo_ensemble
    
    def evaluar_modelo(self, modelo, X, y=None):
        """
        Evalúa el modelo entrenado
        
        Args:
            modelo: Modelo a evaluar
            X: Features de test
            y: Labels reales (opcional)
        
        Returns:
            Diccionario con métricas
        """
        logger.info("Evaluando modelo...")
        
        # Predecir
        if isinstance(modelo, dict):
            predicciones = modelo['isolation_forest'].predict(X)
        else:
            predicciones = modelo.predict(X)
        
        metricas = {
            'total_registros': len(X),
            'anomalias_detectadas': int((predicciones == -1).sum()),
            'tasa_anomalias': float((predicciones == -1).mean() * 100)
        }
        
        # Si hay labels reales, calcular métricas supervisadas
        if y is not None:
            # Convertir predicciones: -1 (anomalía) -> 1, 1 (normal) -> 0
            y_pred = (predicciones == -1).astype(int)
            y_true = y.astype(int)
            
            metricas['precision'] = float(precision_score(y_true, y_pred, zero_division=0))
            metricas['recall'] = float(recall_score(y_true, y_pred, zero_division=0))
            metricas['f1_score'] = float(f1_score(y_true, y_pred, zero_division=0))
            
            try:
                metricas['auc_roc'] = float(roc_auc_score(y_true, y_pred))
            except:
                metricas['auc_roc'] = None
        
        logger.info(f"Evaluación completada: {metricas}")
        return metricas
    
    def guardar_version_modelo(self, modelo, scaler, version, metricas, datos_entrenamiento_info):
        """
        Guarda una versión del modelo con su metadata
        
        Args:
            modelo: Modelo entrenado
            scaler: Scaler usado
            version: Versión del modelo (ej: 'v1.2')
            metricas: Métricas de evaluación
            datos_entrenamiento_info: Info sobre datos de entrenamiento
        
        Returns:
            Ruta donde se guardó el modelo
        """
        logger.info(f"Guardando modelo {version}...")
        
        # Crear carpeta para esta versión
        version_path = self.models_path / 'versiones' / version
        version_path.mkdir(parents=True, exist_ok=True)
        
        # Guardar modelo
        modelo_path = version_path / 'modelo_ensemble_tfm.pkl'
        joblib.dump(modelo, modelo_path)
        
        # Guardar scaler
        scaler_path = version_path / 'scaler.pkl'
        joblib.dump(scaler, scaler_path)
        
        # Guardar metadata
        metadata = {
            'version': version,
            'fecha_creacion': datetime.now().isoformat(),
            'metricas': metricas,
            'datos_entrenamiento': datos_entrenamiento_info,
            'archivos': {
                'modelo': str(modelo_path),
                'scaler': str(scaler_path)
            }
        }
        
        metadata_path = version_path / 'metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Modelo guardado en: {version_path}")
        return version_path
    
    def actualizar_modelo_produccion(self, version, umbral_mejora=0.02):
        """
        Actualiza el modelo en producción si la nueva versión es mejor
        
        Args:
            version: Versión del modelo a poner en producción
            umbral_mejora: Mejora mínima requerida (%)
        
        Returns:
            Boolean indicando si se actualizó
        """
        logger.info(f"Evaluando actualización a {version}...")
        
        # Leer metadata de la nueva versión
        nueva_version_path = self.models_path / 'versiones' / version
        nueva_metadata_path = nueva_version_path / 'metadata.json'
        
        if not nueva_metadata_path.exists():
            logger.error(f"No se encontró metadata para {version}")
            return False
        
        with open(nueva_metadata_path, 'r') as f:
            nueva_metadata = json.load(f)
        
        # Leer metadata de la versión en producción
        prod_metadata_path = self.models_path / 'produccion' / 'metadata.json'
        
        if prod_metadata_path.exists():
            with open(prod_metadata_path, 'r') as f:
                prod_metadata = json.load(f)
            
            # Comparar métricas
            nueva_precision = nueva_metadata['metricas'].get('precision', 0)
            prod_precision = prod_metadata['metricas'].get('precision', 0)
            
            mejora = nueva_precision - prod_precision
            
            if mejora < umbral_mejora:
                logger.info(f"Mejora insuficiente ({mejora:.4f} < {umbral_mejora}). No se actualiza.")
                return False
            
            logger.info(f"Mejora detectada: {mejora:.4f}. Actualizando producción...")
        else:
            logger.info("No hay modelo en producción. Instalando primera versión...")
        
        # Copiar archivos a producción
        import shutil
        
        prod_path = self.models_path / 'produccion'
        
        # Copiar modelo
        shutil.copy(
            nueva_version_path / 'modelo_ensemble_tfm.pkl',
            prod_path / 'modelo_ensemble_tfm.pkl'
        )
        
        # Copiar scaler
        shutil.copy(
            nueva_version_path / 'scaler.pkl',
            prod_path / 'scaler.pkl'
        )
        
        # Copiar metadata
        shutil.copy(
            nueva_metadata_path,
            prod_metadata_path
        )
        
        # También copiar a la raíz del proyecto (para compatibilidad)
        shutil.copy(
            nueva_version_path / 'modelo_ensemble_tfm.pkl',
            self.base_path / 'modelo_ensemble_tfm.pkl'
        )
        
        logger.info(f"Modelo {version} instalado en producción exitosamente")
        return True
    
    def reentrenar_automatico(self, hasta_mes=None, hasta_anio=None, nueva_version=None):
        """
        Ejecuta el proceso completo de reentrenamiento automático
        
        Args:
            hasta_mes: Mes límite de datos
            hasta_anio: Año límite de datos
            nueva_version: Nombre de la nueva versión (auto si None)
        
        Returns:
            Diccionario con resultados del reentrenamiento
        """
        logger.info("=" * 60)
        logger.info("INICIANDO REENTRENAMIENTO AUTOMÁTICO")
        logger.info("=" * 60)
        
        try:
            # 1. Obtener datos validados
            df = self.obtener_datos_validados(hasta_mes, hasta_anio)
            
            # 2. Preprocesar datos
            X, y, scaler = self.preprocesar_datos_entrenamiento(df)
            
            # 3. Entrenar nuevo modelo
            modelo_nuevo = self.entrenar_modelo_ensemble(X, y)
            
            # 4. Evaluar modelo
            metricas = self.evaluar_modelo(modelo_nuevo, X, y)
            
            # 5. Determinar versión
            if nueva_version is None:
                # Auto-incrementar versión
                versiones_existentes = list((self.models_path / 'versiones').glob('v*'))
                if versiones_existentes:
                    ultima_version = max([v.name for v in versiones_existentes])
                    num = int(ultima_version.split('.')[1]) + 1
                    nueva_version = f"v1.{num}"
                else:
                    nueva_version = "v1.0"
            
            # 6. Guardar versión
            datos_info = {
                'total_registros': len(df),
                'registros_entrenamiento': len(X),
                'periodo': f"{hasta_anio}-{hasta_mes}" if hasta_mes else "todos",
                'features': list(X.columns)
            }
            
            version_path = self.guardar_version_modelo(
                modelo_nuevo, scaler, nueva_version, metricas, datos_info
            )
            
            # 7. Actualizar producción si es mejor
            actualizado = self.actualizar_modelo_produccion(nueva_version)
            
            resultado = {
                'exito': True,
                'version': nueva_version,
                'metricas': metricas,
                'actualizado_produccion': actualizado,
                'ruta_modelo': str(version_path)
            }
            
            logger.info("=" * 60)
            logger.info("REENTRENAMIENTO COMPLETADO EXITOSAMENTE")
            logger.info(f"Nueva versión: {nueva_version}")
            logger.info(f"Precisión: {metricas.get('precision', 'N/A')}")
            logger.info(f"En producción: {actualizado}")
            logger.info("=" * 60)
            
            return resultado
            
        except Exception as e:
            logger.error(f"Error en reentrenamiento: {e}")
            return {
                'exito': False,
                'error': str(e)
            }


if __name__ == '__main__':
    # Ejemplo de uso
    print("Sistema de Reentrenamiento Automático - TFM Pipeline")
    print("=" * 50)
    
    sistema = ModelRetrainingSystem()
    
    # Ejecutar reentrenamiento
    resultado = sistema.reentrenar_automatico()
    
    if resultado['exito']:
        print(f"\nReentrenamiento exitoso!")
        print(f"Versión: {resultado['version']}")
        print(f"Métricas: {resultado['metricas']}")
    else:
        print(f"\nError: {resultado['error']}")

