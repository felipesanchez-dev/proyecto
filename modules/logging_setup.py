"""
Sistema de logging avanzado con rotación y múltiples niveles
"""
import logging
import logging.handlers
import os
from pathlib import Path
from datetime import datetime
from config.settings import LOGS_DIR, LOG_FORMAT, LOG_FILE

class LoggerSetup:
    """Configurador del sistema de logging"""
    
    @staticmethod
    def setup_logging(log_level: str = "INFO", enable_console: bool = True, enable_file: bool = True) -> logging.Logger:
        """
        Configura el sistema de logging completo
        Args:
            log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            enable_console: Habilitar logging en consola
            enable_file: Habilitar logging en archivo
        Returns:
            Logger configurado
        """
        # Crear directorio de logs si no existe
        LOGS_DIR.mkdir(exist_ok=True)
        
        # Configurar logger raíz
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_level.upper()))
        
        # Limpiar handlers existentes
        root_logger.handlers.clear()
        
        # Formatters
        detailed_formatter = logging.Formatter(LOG_FORMAT)
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        
        # Handler para consola
        if enable_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(console_formatter)
            root_logger.addHandler(console_handler)
        
        # Handler para archivo con rotación
        if enable_file:
            # Rotación diaria, mantener 30 días
            file_handler = logging.handlers.TimedRotatingFileHandler(
                filename=LOG_FILE,
                when='midnight',
                interval=1,
                backupCount=30,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(detailed_formatter)
            root_logger.addHandler(file_handler)
            
            # Handler adicional para errores críticos
            error_log_file = LOGS_DIR / "errors.log"
            error_handler = logging.handlers.RotatingFileHandler(
                filename=error_log_file,
                maxBytes=5*1024*1024,  # 5MB
                backupCount=5,
                encoding='utf-8'
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(detailed_formatter)
            root_logger.addHandler(error_handler)
        
        # Logger específico para el scanner
        scanner_logger = logging.getLogger('sistema_scanner')
        scanner_logger.info("Sistema de logging configurado correctamente")
        
        return scanner_logger

class OperationLogger:
    """Logger especializado para operaciones específicas"""
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.logger = logging.getLogger(f'sistema_scanner.{operation_name}')
        self.start_time = None
        self.operation_id = None
    
    def start_operation(self, operation_id: str = None) -> str:
        """
        Inicia el logging de una operación
        Args:
            operation_id: ID opcional de la operación
        Returns:
            ID de la operación
        """
        self.start_time = datetime.now()
        self.operation_id = operation_id or f"{self.operation_name}_{int(self.start_time.timestamp())}"
        
        self.logger.info(f"=== INICIO {self.operation_name.upper()} ===")
        self.logger.info(f"Operation ID: {self.operation_id}")
        self.logger.info(f"Timestamp: {self.start_time.isoformat()}")
        
        return self.operation_id
    
    def log_progress(self, message: str, progress_percent: int = None):
        """
        Registra progreso de la operación
        Args:
            message: Mensaje de progreso
            progress_percent: Porcentaje opcional de progreso
        """
        if progress_percent is not None:
            self.logger.info(f"[{progress_percent:3d}%] {message}")
        else:
            self.logger.info(f"[PROG] {message}")
    
    def log_step(self, step_name: str, details: str = None):
        """
        Registra un paso específico de la operación
        Args:
            step_name: Nombre del paso
            details: Detalles adicionales
        """
        message = f"[STEP] {step_name}"
        if details:
            message += f" - {details}"
        self.logger.info(message)
    
    def log_error(self, error_message: str, exception: Exception = None):
        """
        Registra un error durante la operación
        Args:
            error_message: Mensaje de error
            exception: Excepción opcional
        """
        self.logger.error(f"[ERROR] {error_message}")
        if exception:
            self.logger.exception(f"Exception details: {exception}")
    
    def log_warning(self, warning_message: str):
        """
        Registra una advertencia
        Args:
            warning_message: Mensaje de advertencia
        """
        self.logger.warning(f"[WARN] {warning_message}")
    
    def end_operation(self, success: bool = True, final_message: str = None):
        """
        Finaliza el logging de la operación
        Args:
            success: Si la operación fue exitosa
            final_message: Mensaje final opcional
        """
        end_time = datetime.now()
        duration = end_time - self.start_time if self.start_time else None
        
        status = "EXITOSA" if success else "FALLIDA"
        self.logger.info(f"=== FIN {self.operation_name.upper()} - {status} ===")
        
        if duration:
            self.logger.info(f"Duración: {duration.total_seconds():.2f} segundos")
        
        if final_message:
            self.logger.info(f"Resultado: {final_message}")
        
        self.logger.info("=" * 50)

class SecurityLogger:
    """Logger especializado para eventos de seguridad"""
    
    def __init__(self):
        self.logger = logging.getLogger('sistema_scanner.security')
        
        # Configurar handler específico para seguridad
        security_log_file = LOGS_DIR / "security.log"
        security_handler = logging.handlers.RotatingFileHandler(
            filename=security_log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=10,
            encoding='utf-8'
        )
        security_handler.setLevel(logging.INFO)
        security_formatter = logging.Formatter(
            '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
        )
        security_handler.setFormatter(security_formatter)
        self.logger.addHandler(security_handler)
    
    def log_sensitive_data_access(self, data_type: str, include_sensitive: bool):
        """
        Registra acceso a datos sensibles
        Args:
            data_type: Tipo de datos accedidos
            include_sensitive: Si se incluyeron datos sensibles
        """
        status = "INCLUIDOS" if include_sensitive else "EXCLUIDOS"
        self.logger.warning(f"Acceso a datos sensibles: {data_type} - {status}")
    
    def log_activation_attempt(self, activation_type: str, user_confirmed: bool):
        """
        Registra intento de activación
        Args:
            activation_type: Tipo de activación (Windows/Office)
            user_confirmed: Si el usuario confirmó la acción
        """
        status = "CONFIRMADO" if user_confirmed else "CANCELADO"
        self.logger.warning(f"Intento de activación {activation_type}: {status}")
    
    def log_external_command(self, command: str, executed: bool):
        """
        Registra ejecución de comandos externos
        Args:
            command: Comando ejecutado
            executed: Si se ejecutó realmente
        """
        status = "EJECUTADO" if executed else "CANCELADO"
        self.logger.warning(f"Comando externo {status}: {command}")
    
    def log_database_operation(self, operation: str, success: bool, details: str = None):
        """
        Registra operaciones de base de datos
        Args:
            operation: Tipo de operación
            success: Si fue exitosa
            details: Detalles adicionales
        """
        status = "EXITOSA" if success else "FALLIDA"
        message = f"Operación BD {operation}: {status}"
        if details:
            message += f" - {details}"
        self.logger.info(message)

def get_log_stats() -> dict:
    """
    Obtiene estadísticas de los archivos de log
    Returns:
        Diccionario con estadísticas
    """
    stats = {
        "log_files": [],
        "total_size_mb": 0,
        "oldest_log": None,
        "newest_log": None
    }
    
    try:
        log_files = list(LOGS_DIR.glob("*.log*"))
        
        for log_file in log_files:
            file_stat = log_file.stat()
            file_info = {
                "name": log_file.name,
                "size_mb": round(file_stat.st_size / (1024*1024), 2),
                "created": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
            }
            stats["log_files"].append(file_info)
            stats["total_size_mb"] += file_info["size_mb"]
        
        if stats["log_files"]:
            stats["oldest_log"] = min(stats["log_files"], key=lambda x: x["created"])["name"]
            stats["newest_log"] = max(stats["log_files"], key=lambda x: x["modified"])["name"]
    
    except Exception as e:
        logging.getLogger('sistema_scanner').error(f"Error obteniendo estadísticas de logs: {e}")
    
    return stats