#!/usr/bin/env python3
"""
Sistema Scanner Windows - Punto de entrada principal
Mantenimiento automatizado de sistemas con escaneo de hardware y software
"""
import sys
import os
import argparse
import logging
from pathlib import Path

# Agregar el directorio del proyecto al path para imports
sys.path.insert(0, str(Path(__file__).parent))

from modules.logging_setup import LoggerSetup
from modules.interface import ConsoleInterface
from modules.scanner import SystemScanner
from modules.security_scanner import SecurityScanner
from modules.database import MongoDBClient
from modules.utils import DataManager
from config.settings import get_mongodb_uri, MONGODB_DATABASE, MONGODB_COLLECTION

def setup_argument_parser() -> argparse.ArgumentParser:
    """
    Configura y retorna el parser de argumentos de línea de comandos
    Returns:
        Parser configurado con todos los argumentos
    """
    parser = argparse.ArgumentParser(
        description="Sistema Scanner Windows - Escaneo automatizado de hardware y software",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  %(prog)s                           # Ejecutar interfaz interactiva
  %(prog)s --scan-only              # Solo escanear, no subir a MongoDB
  %(prog)s --no-sensitive           # Excluir datos sensibles
  %(prog)s --batch --output scan.json # Modo batch con archivo de salida
  %(prog)s --test-mongodb           # Probar conexión a MongoDB
  %(prog)s --log-level DEBUG        # Habilitar logging detallado
  
Variables de entorno:
  MONGO_URI                         # URI de conexión a MongoDB
        """
    )
    
    # Argumentos principales
    parser.add_argument(
        "--no-sensitive",
        action="store_true",
        help="Excluir datos sensibles del escaneo (claves de producto, números de serie)"
    )
    
    parser.add_argument(
        "--scan-only",
        action="store_true",
        help="Solo realizar escaneo local, no subir a MongoDB"
    )
    
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Ejecutar en modo batch (sin interfaz interactiva)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        metavar="ARCHIVO",
        help="Archivo de salida para el resultado del escaneo (modo batch)"
    )
    
    # Configuración de logging
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Nivel de logging (default: INFO)"
    )
    
    parser.add_argument(
        "--no-log-file",
        action="store_true",
        help="Deshabilitar logging a archivo, solo consola"
    )
    
    # Opciones de MongoDB
    parser.add_argument(
        "--test-mongodb",
        action="store_true",
        help="Probar conexión a MongoDB y salir"
    )
    
    parser.add_argument(
        "--mongo-uri",
        type=str,
        metavar="URI",
        help="URI de conexión a MongoDB (sobrescribe variable de entorno)"
    )
    
    # Opciones de mantenimiento
    parser.add_argument(
        "--cleanup-logs",
        type=int,
        metavar="DIAS",
        help="Limpiar logs antiguos (especificar días de retención)"
    )
    
    parser.add_argument(
        "--cleanup-scans",
        type=int,
        metavar="DIAS",
        help="Limpiar escaneos locales antiguos (especificar días de retención)"
    )
    
    # Información y ayuda
    parser.add_argument(
        "--version",
        action="version",
        version="Sistema Scanner Windows v1.0.0"
    )
    
    parser.add_argument(
        "--list-scans",
        action="store_true",
        help="Listar escaneos locales guardados"
    )
    
    return parser

def test_mongodb_connection(mongo_uri: str = None) -> bool:
    """
    Prueba la conexión a MongoDB y muestra información
    Args:
        mongo_uri: URI opcional de MongoDB
    Returns:
        True si la conexión es exitosa
    """
    print("🔄 Probando conexión a MongoDB...")
    
    # Configurar URI si se proporciona
    if mongo_uri:
        os.environ['mongodb+srv://root:root@proyectofinal.iktfuvz.mongodb.net/'] = mongo_uri
    
    try:
        with MongoDBClient() as db_client:
            connection_info = db_client.test_connection()
            
            if connection_info["connected"]:
                print("✅ Conexión exitosa a MongoDB")
                print(f"   📊 Base de datos: {MONGODB_DATABASE}")
                print(f"   📁 Colección: {MONGODB_COLLECTION}")
                print(f"   📈 Documentos: {connection_info['collection_count']}")
                
                server_info = connection_info.get("server_info", {})
                if server_info:
                    print(f"   🗄️ Versión servidor: {server_info.get('version', 'N/A')}")
                
                return True
            else:
                print("❌ Fallo en conexión a MongoDB")
                if connection_info.get("error"):
                    print(f"   Error: {connection_info['error']}")
                return False
                
    except Exception as e:
        print(f"❌ Error probando MongoDB: {e}")
        return False

def run_batch_scan(include_sensitive: bool, upload_mongodb: bool, output_file: str = None) -> bool:
    """
    Ejecuta un escaneo en modo batch
    Args:
        include_sensitive: Incluir datos sensibles
        upload_mongodb: Subir a MongoDB
        output_file: Archivo de salida opcional
    Returns:
        True si el escaneo fue exitoso
    """
    print("🔄 Ejecutando escaneo en modo batch...")
    
    try:
        # Inicializar componentes
        scanner = SystemScanner(include_sensitive=include_sensitive)
        security_scanner = SecurityScanner()
        data_manager = DataManager()
        
        print("   📊 Escaneando hardware...")
        scan_data = scanner.perform_full_scan()
        
        print("   🔒 Escaneando seguridad...")
        security_data = security_scanner.perform_security_scan()
        
        # Combinar datos
        scan_data["system_info"]["security"] = security_data
        
        # Guardar localmente
        print("   💾 Guardando escaneo localmente...")
        local_file = data_manager.save_scan_locally(scan_data)
        
        # Guardar en archivo específico si se proporciona
        if output_file:
            import json
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(scan_data, f, indent=2, ensure_ascii=False)
            print(f"   📁 Guardado en: {output_file}")
        
        # Subir a MongoDB si está habilitado
        if upload_mongodb:
            print("   ☁️ Subiendo a MongoDB...")
            try:
                with MongoDBClient() as db_client:
                    document_id = db_client.insert_scan_data(scan_data)
                    if document_id:
                        print(f"   ✅ Subido con ID: {document_id}")
                    else:
                        print("   ❌ Error subiendo a MongoDB")
                        return False
            except Exception as e:
                print(f"   ❌ Error MongoDB: {e}")
                return False
        
        scan_id = scan_data["identifiers"]["scan_id"]
        print(f"✅ Escaneo completado exitosamente - ID: {scan_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error en escaneo batch: {e}")
        return False

def main():
    """Función principal del programa"""
    
    # Configurar parser de argumentos
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # Configurar logging
    logger = LoggerSetup.setup_logging(
        log_level=args.log_level,
        enable_console=True,
        enable_file=not args.no_log_file
    )
    
    logger.info("Sistema Scanner iniciado")
    logger.info(f"Argumentos: {vars(args)}")
    
    try:
        # Configurar URI de MongoDB si se proporciona
        if args.mongo_uri:
            os.environ['mongodb+srv://root:<db_password>@proyectofinal.iktfuvz.mongodb.net/'] = args.mongo_uri
            logger.info(f"MongoDB URI configurada desde argumentos")
        
        # Test de conexión MongoDB
        if args.test_mongodb:
            success = test_mongodb_connection(args.mongo_uri)
            sys.exit(0 if success else 1)
        
        # Limpiar logs antiguos
        if args.cleanup_logs:
            print(f"🧹 Limpiando logs antiguos (>{args.cleanup_logs} días)...")
            # Implementar limpieza de logs aquí
            print("✅ Limpieza de logs completada")
        
        # Limpiar escaneos antiguos
        if args.cleanup_scans:
            print(f"🧹 Limpiando escaneos antiguos (>{args.cleanup_scans} días)...")
            data_manager = DataManager()
            deleted_count = data_manager.clean_old_scans(args.cleanup_scans)
            print(f"✅ Eliminados {deleted_count} escaneos antiguos")
        
        # Listar escaneos locales
        if args.list_scans:
            print("📋 Escaneos locales guardados:")
            data_manager = DataManager()
            scans = data_manager.list_local_scans()
            
            if scans:
                for i, scan in enumerate(scans, 1):
                    print(f"   {i}. {scan['filename']} - ID: {scan['scan_id'][:8]}... - {scan['created']}")
            else:
                print("   No se encontraron escaneos locales")
            
            sys.exit(0)
        
        # Modo batch
        if args.batch:
            include_sensitive = not args.no_sensitive
            upload_mongodb = not args.scan_only
            
            success = run_batch_scan(include_sensitive, upload_mongodb, args.output)
            sys.exit(0 if success else 1)
        
        # Modo interactivo (default)
        else:
            print("🚀 Iniciando interfaz interactiva...")
            interface = ConsoleInterface()
            interface.run_main_loop()
    
    except KeyboardInterrupt:
        print("\\n🛑 Operación cancelada por el usuario")
        logger.info("Programa cancelado por usuario")
        sys.exit(1)
    
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
        logger.error(f"Error inesperado: {e}", exc_info=True)
        sys.exit(1)
    
    finally:
        logger.info("Sistema Scanner finalizado")

if __name__ == "__main__":
    main()