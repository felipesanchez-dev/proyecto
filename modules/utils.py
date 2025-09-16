import json
import uuid
import random
import string
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from config.settings import SCANS_DIR

class DataManager:
    """Gestor de datos y persistencia local"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.scans_dir = Path(SCANS_DIR)
        self.scans_dir.mkdir(exist_ok=True)
    
    def generate_scan_identifiers(self) -> Dict[str, str]:
        """
        Genera identificadores únicos para un escaneo
        Returns:
            Dict con scan_id (UUID v4), access_pin (4 chars), timestamp
        """
        scan_id = str(uuid.uuid4())
        access_pin = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        timestamp = datetime.now().isoformat()
        
        self.logger.info(f"Generados identificadores - ID: {scan_id}, PIN: {access_pin}")
        
        return {
            "scan_id": scan_id,
            "access_pin": access_pin,
            "timestamp": timestamp,
            "scan_date": datetime.now().strftime("%Y-%m-%d"),
            "scan_time": datetime.now().strftime("%H:%M:%S")
        }
    
    def save_scan_locally(self, scan_data: Dict[str, Any]) -> str:
        """
        Guarda el resultado del escaneo en un archivo JSON local
        Args:
            scan_data: Diccionario con los datos del escaneo
        Returns:
            Ruta del archivo guardado
        """
        try:
            # Crear nombre de archivo basado en timestamp y scan_id
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            scan_id_short = scan_data.get("identifiers", {}).get("scan_id", "unknown")[:8]
            filename = f"scan_{timestamp}_{scan_id_short}.json"
            file_path = self.scans_dir / filename
            
            # Agregar metadata adicional
            scan_data["file_info"] = {
                "filename": filename,
                "saved_at": datetime.now().isoformat(),
                "file_size_bytes": 0  # Se actualizará después
            }
            
            # Guardar archivo
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(scan_data, f, indent=2, ensure_ascii=False)
            
            # Actualizar tamaño del archivo
            file_size = file_path.stat().st_size
            scan_data["file_info"]["file_size_bytes"] = file_size
            
            # Re-guardar con el tamaño correcto
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(scan_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Escaneo guardado localmente: {file_path} ({file_size} bytes)")
            return str(file_path)
            
        except Exception as e:
            self.logger.error(f"Error guardando escaneo localmente: {e}")
            raise
    
    def load_scan_from_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Carga un escaneo desde archivo JSON
        Args:
            file_path: Ruta del archivo a cargar
        Returns:
            Diccionario con datos del escaneo o None si hay error
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                scan_data = json.load(f)
            
            self.logger.info(f"Escaneo cargado desde: {file_path}")
            return scan_data
            
        except FileNotFoundError:
            self.logger.error(f"Archivo no encontrado: {file_path}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decodificando JSON: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error cargando archivo: {e}")
            return None
    
    def list_local_scans(self) -> list:
        """
        Lista todos los escaneos guardados localmente
        Returns:
            Lista de diccionarios con información de archivos
        """
        scans = []
        
        try:
            for file_path in self.scans_dir.glob("scan_*.json"):
                try:
                    stat = file_path.stat()
                    scan_info = {
                        "filename": file_path.name,
                        "full_path": str(file_path),
                        "size_bytes": stat.st_size,
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    }
                    
                    # Intentar extraer scan_id del contenido
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            scan_info["scan_id"] = data.get("identifiers", {}).get("scan_id", "unknown")
                            scan_info["access_pin"] = data.get("identifiers", {}).get("access_pin", "unknown")
                    except:
                        scan_info["scan_id"] = "error_reading"
                        scan_info["access_pin"] = "error"
                    
                    scans.append(scan_info)
                    
                except Exception as e:
                    self.logger.warning(f"Error procesando archivo {file_path}: {e}")
                    continue
            
            # Ordenar por fecha de creación (más reciente primero)
            scans.sort(key=lambda x: x["created"], reverse=True)
            
        except Exception as e:
            self.logger.error(f"Error listando escaneos locales: {e}")
        
        return scans
    
    def clean_old_scans(self, keep_days: int = 30) -> int:
        """
        Elimina escaneos antiguos para liberar espacio
        Args:
            keep_days: Días de retención
        Returns:
            Número de archivos eliminados
        """
        deleted_count = 0
        cutoff_time = datetime.now().timestamp() - (keep_days * 24 * 60 * 60)
        
        try:
            for file_path in self.scans_dir.glob("scan_*.json"):
                try:
                    if file_path.stat().st_ctime < cutoff_time:
                        file_path.unlink()
                        deleted_count += 1
                        self.logger.info(f"Eliminado escaneo antiguo: {file_path.name}")
                        
                except Exception as e:
                    self.logger.warning(f"Error eliminando {file_path}: {e}")
                    continue
            
            if deleted_count > 0:
                self.logger.info(f"Limpieza completada: {deleted_count} archivos eliminados")
            
        except Exception as e:
            self.logger.error(f"Error en limpieza de archivos: {e}")
        
        return deleted_count
    
    def format_scan_summary(self, scan_data: Dict[str, Any]) -> str:
        """
        Formatea un resumen legible del escaneo
        Args:
            scan_data: Datos del escaneo
        Returns:
            Cadena con resumen formateado
        """
        try:
            identifiers = scan_data.get("identifiers", {})
            system_info = scan_data.get("system_info", {})
            hardware = system_info.get("hardware", {})
            
            summary = f"""
╔══════════════════════════════════════════════════════════════════════
║ RESUMEN DEL ESCANEO
╠══════════════════════════════════════════════════════════════════════
║ ID de Escaneo: {identifiers.get('scan_id', 'N/A')}
║ PIN de Acceso: {identifiers.get('access_pin', 'N/A')}
║ Fecha/Hora:    {identifiers.get('timestamp', 'N/A')}
╠══════════════════════════════════════════════════════════════════════
║ Sistema Operativo: {system_info.get('operating_system', {}).get('name', 'N/A')}
║ Hostname:          {system_info.get('operating_system', {}).get('hostname', 'N/A')}
║ Arquitectura:      {system_info.get('operating_system', {}).get('architecture', 'N/A')}
╠══════════════════════════════════════════════════════════════════════
║ CPU:    {hardware.get('cpu', {}).get('processor_name', 'N/A')}
║ RAM:    {hardware.get('memory', {}).get('total_gb', 'N/A')} GB
║ Discos: {len(hardware.get('disks', []))} detectados
║ GPU:    {len(hardware.get('gpu', []))} detectadas
╚══════════════════════════════════════════════════════════════════════
"""
            return summary
            
        except Exception as e:
            self.logger.error(f"Error formateando resumen: {e}")
            return f"Error formateando resumen: {e}"