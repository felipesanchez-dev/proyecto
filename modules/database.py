"""
Módulo de integración con MongoDB
Maneja conexión, reintentos y envío de datos
"""
import pymongo
import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime
from config.settings import get_mongodb_uri, MONGODB_DATABASE, MONGODB_COLLECTION

class MongoDBClient:
    """Cliente para interaccionar con MongoDB"""
    
    def __init__(self, max_retries: int = 3, retry_delay: int = 2):
        self.logger = logging.getLogger(__name__)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.client = None
        self.db = None
        self.collection = None
        
    def connect(self) -> bool:
        """
        Establece conexión con MongoDB
        Returns:
            True si la conexión es exitosa, False en caso contrario
        """
        try:
            uri = get_mongodb_uri()
            self.logger.info(f"Conectando a MongoDB...")
            
            # Crear cliente con configuración de timeout
            self.client = pymongo.MongoClient(
                uri,
                serverSelectionTimeoutMS=5000,  # 5 segundos timeout
                connectTimeoutMS=10000,         # 10 segundos para conectar
                socketTimeoutMS=10000,          # 10 segundos para operaciones
                retryWrites=True
            )
            
            # Verificar conexión
            self.client.admin.command('ping')
            
            # Seleccionar base de datos y colección
            self.db = self.client[MONGODB_DATABASE]
            self.collection = self.db[MONGODB_COLLECTION]
            
            self.logger.info(f"Conexión exitosa a MongoDB - DB: {MONGODB_DATABASE}, Collection: {MONGODB_COLLECTION}")
            return True
            
        except pymongo.errors.ServerSelectionTimeoutError:
            self.logger.error("Timeout conectando a MongoDB - Servidor no disponible")
            return False
        except pymongo.errors.ConfigurationError as e:
            self.logger.error(f"Error de configuración MongoDB: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error conectando a MongoDB: {e}")
            return False
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Prueba la conexión y obtiene información del servidor
        Returns:
            Diccionario con información de la conexión
        """
        connection_info = {
            "connected": False,
            "server_info": None,
            "database_stats": None,
            "collection_count": 0,
            "error": None
        }
        
        try:
            if not self.client:
                if not self.connect():
                    connection_info["error"] = "No se pudo establecer conexión"
                    return connection_info
            
            # Obtener información del servidor
            connection_info["server_info"] = self.client.server_info()
            connection_info["connected"] = True
            
            # Estadísticas de la base de datos
            if self.db is not None:
                connection_info["database_stats"] = self.db.command("dbstats")
                connection_info["collection_count"] = self.collection.count_documents({})
            
            self.logger.info("Test de conexión MongoDB exitoso")
            
        except Exception as e:
            connection_info["error"] = str(e)
            self.logger.error(f"Error en test de conexión: {e}")
        
        return connection_info
    
    def insert_scan_data(self, scan_data: Dict[str, Any]) -> Optional[str]:
        """
        Inserta datos de escaneo en MongoDB con reintentos
        Args:
            scan_data: Diccionario con los datos del escaneo
        Returns:
            ID del documento insertado o None si falla
        """
        for attempt in range(self.max_retries):
            try:
                # Asegurar conexión
                if not self.client:
                    if not self.connect():
                        raise Exception("No se pudo conectar a MongoDB")
                
                # Agregar metadata de inserción
                scan_data["mongodb_info"] = {
                    "inserted_at": datetime.now().isoformat(),
                    "database": MONGODB_DATABASE,
                    "collection": MONGODB_COLLECTION,
                    "attempt": attempt + 1
                }
                
                # Insertar documento
                result = self.collection.insert_one(scan_data)
                document_id = str(result.inserted_id)
                
                self.logger.info(f"Escaneo insertado en MongoDB - ID: {document_id}")
                return document_id
                
            except pymongo.errors.DuplicateKeyError:
                self.logger.warning("Documento duplicado en MongoDB")
                return None
                
            except pymongo.errors.NetworkTimeout:
                self.logger.warning(f"Timeout en intento {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))  # Backoff exponencial
                    continue
                else:
                    self.logger.error("Todos los intentos de conexión fallaron")
                    return None
                    
            except Exception as e:
                self.logger.error(f"Error insertando en MongoDB (intento {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    return None
        
        return None
    
    def find_scan_by_id(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca un escaneo por su scan_id
        Args:
            scan_id: ID del escaneo a buscar
        Returns:
            Diccionario con datos del escaneo o None si no se encuentra
        """
        try:
            if not self.client:
                if not self.connect():
                    return None
            
            document = self.collection.find_one({"identifiers.scan_id": scan_id})
            
            if document:
                # Convertir ObjectId a string
                document["_id"] = str(document["_id"])
                self.logger.info(f"Escaneo encontrado: {scan_id}")
                return document
            else:
                self.logger.info(f"Escaneo no encontrado: {scan_id}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error buscando escaneo: {e}")
            return None
    
    def get_recent_scans(self, limit: int = 10) -> list:
        """
        Obtiene los escaneos más recientes
        Args:
            limit: Número máximo de escaneos a retornar
        Returns:
            Lista de diccionarios con escaneos recientes
        """
        scans = []
        
        try:
            if not self.client:
                if not self.connect():
                    return scans
            
            cursor = self.collection.find().sort("identifiers.timestamp", -1).limit(limit)
            
            for document in cursor:
                # Convertir ObjectId a string y mantener solo campos esenciales
                scan_summary = {
                    "_id": str(document["_id"]),
                    "scan_id": document.get("identifiers", {}).get("scan_id", "unknown"),
                    "timestamp": document.get("identifiers", {}).get("timestamp", "unknown"),
                    "hostname": document.get("system_info", {}).get("operating_system", {}).get("hostname", "unknown"),
                    "os_name": document.get("system_info", {}).get("operating_system", {}).get("name", "unknown")
                }
                scans.append(scan_summary)
            
            self.logger.info(f"Obtenidos {len(scans)} escaneos recientes")
            
        except Exception as e:
            self.logger.error(f"Error obteniendo escaneos recientes: {e}")
        
        return scans
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de la colección
        Returns:
            Diccionario con estadísticas
        """
        stats = {
            "total_documents": 0,
            "collection_size_mb": 0,
            "avg_document_size": 0,
            "indexes_count": 0,
            "error": None
        }
        
        try:
            if not self.client:
                if not self.connect():
                    stats["error"] = "No conectado"
                    return stats
            
            # Estadísticas de la colección
            collection_stats = self.db.command("collstats", MONGODB_COLLECTION)
            
            stats["total_documents"] = collection_stats.get("count", 0)
            stats["collection_size_mb"] = round(collection_stats.get("size", 0) / (1024*1024), 2)
            stats["avg_document_size"] = collection_stats.get("avgObjSize", 0)
            stats["indexes_count"] = collection_stats.get("nindexes", 0)
            
            self.logger.info("Estadísticas de colección obtenidas")
            
        except Exception as e:
            stats["error"] = str(e)
            self.logger.error(f"Error obteniendo estadísticas: {e}")
        
        return stats
    
    def close_connection(self):
        """Cierra la conexión a MongoDB"""
        try:
            if self.client:
                self.client.close()
                self.logger.info("Conexión MongoDB cerrada")
        except Exception as e:
            self.logger.error(f"Error cerrando conexión: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close_connection()