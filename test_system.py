#!/usr/bin/env python3
"""
Script de pruebas básicas para el Sistema Scanner
Valida funcionamiento de componentes principales
"""
import sys
import os
from pathlib import Path
import traceback

# Agregar el directorio del proyecto al path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Prueba que todos los módulos se puedan importar"""
    print("🧪 Probando importaciones de módulos...")
    
    modules_to_test = [
        ("psutil", "Información de hardware"),
        ("pymongo", "Conexión a MongoDB"),
        ("rich", "Interfaz de consola"),
        ("wmi", "Información de Windows (opcional)")
    ]
    
    failed_imports = []
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"   ✅ {module_name} - {description}")
        except ImportError as e:
            failed_imports.append((module_name, description, e))
            print(f"   ❌ {module_name} - {description} - ERROR: {e}")
    
    if failed_imports:
        print(f"\\n⚠️ {len(failed_imports)} módulos no disponibles. Instale con:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def test_project_modules():
    """Prueba que los módulos del proyecto se puedan importar"""
    print("\\n🧪 Probando módulos del proyecto...")
    
    project_modules = [
        ("config.settings", "Configuraciones"),
        ("modules.scanner", "Escáner de hardware"),
        ("modules.security_scanner", "Escáner de seguridad"),
        ("modules.database", "Cliente MongoDB"),
        ("modules.utils", "Utilidades"),
        ("modules.logging_setup", "Sistema de logging"),
        ("modules.interface", "Interfaz de consola"),
        ("modules.activation", "Módulo de activación")
    ]
    
    failed_modules = []
    
    for module_name, description in project_modules:
        try:
            __import__(module_name)
            print(f"   ✅ {module_name} - {description}")
        except Exception as e:
            failed_modules.append((module_name, description, e))
            print(f"   ❌ {module_name} - {description} - ERROR: {e}")
    
    return len(failed_modules) == 0

def test_basic_functionality():
    """Prueba funcionalidad básica sin dependencies externas"""
    print("\\n🧪 Probando funcionalidad básica...")
    
    try:
        # Test generación de identificadores
        from modules.utils import DataManager
        data_manager = DataManager()
        identifiers = data_manager.generate_scan_identifiers()
        
        assert "scan_id" in identifiers
        assert "access_pin" in identifiers
        assert len(identifiers["access_pin"]) == 4
        print("   ✅ Generación de identificadores")
        
        # Test configuraciones
        from config.settings import get_mongodb_uri, MONGODB_DATABASE, MONGODB_COLLECTION
        uri = get_mongodb_uri()
        assert uri is not None
        assert MONGODB_DATABASE == "proyectofinal"
        assert MONGODB_COLLECTION == "scans"
        print("   ✅ Configuraciones básicas")
        
        # Test logging setup
        from modules.logging_setup import LoggerSetup
        logger = LoggerSetup.setup_logging(log_level="INFO", enable_console=False, enable_file=False)
        logger.info("Test log message")
        print("   ✅ Sistema de logging")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en funcionalidad básica: {e}")
        traceback.print_exc()
        return False

def test_hardware_scanning():
    """Prueba el escaneo de hardware (requiere psutil)"""
    print("\\n🧪 Probando escaneo de hardware...")
    
    try:
        import psutil
        from modules.scanner import SystemScanner
        
        scanner = SystemScanner(include_sensitive=False)
        
        # Test escaneo de discos
        disks = scanner.scan_disks()
        assert isinstance(disks, list)
        print(f"   ✅ Discos detectados: {len(disks)}")
        
        # Test escaneo de memoria
        memory = scanner.scan_memory()
        assert "total_gb" in memory
        print(f"   ✅ RAM detectada: {memory.get('total_gb', 'N/A')} GB")
        
        # Test escaneo de CPU
        cpu = scanner.scan_cpu()
        assert "processor_name" in cpu
        print(f"   ✅ CPU detectado: {cpu.get('logical_cores', 'N/A')} cores")
        
        return True
        
    except ImportError:
        print("   ⚠️ psutil no disponible, omitiendo pruebas de hardware")
        return True
    except Exception as e:
        print(f"   ❌ Error en escaneo de hardware: {e}")
        return False

def test_mongodb_connection():
    """Prueba la conexión a MongoDB (opcional)"""
    print("\\n🧪 Probando conexión a MongoDB...")
    
    try:
        import pymongo
        from modules.database import MongoDBClient
        
        # Solo probar si pymongo está disponible
        db_client = MongoDBClient()
        connection_info = db_client.test_connection()
        
        if connection_info["connected"]:
            print("   ✅ MongoDB conectado correctamente")
            print(f"      📊 Documentos en colección: {connection_info.get('collection_count', 0)}")
            return True
        else:
            print("   ⚠️ MongoDB no disponible (esto es normal si no está configurado)")
            error = connection_info.get("error")
            if error:
                print(f"      Detalle: {error}")
            return True  # No es un fallo crítico
            
    except ImportError:
        print("   ⚠️ pymongo no disponible, omitiendo prueba de MongoDB")
        return True
    except Exception as e:
        print(f"   ❌ Error probando MongoDB: {e}")
        return True  # No es un fallo crítico

def test_directory_structure():
    """Verifica que la estructura de directorios sea correcta"""
    print("\\n🧪 Verificando estructura de directorios...")
    
    base_dir = Path(__file__).parent
    required_dirs = ["modules", "config", "logs", "scans"]
    required_files = [
        "main.py",
        "requirements.txt",
        "modules/__init__.py",
        "config/__init__.py",
        "config/settings.py"
    ]
    
    # Verificar directorios
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"   ✅ Directorio: {dir_name}")
        else:
            print(f"   ❌ Directorio faltante: {dir_name}")
            return False
    
    # Verificar archivos
    for file_path in required_files:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"   ✅ Archivo: {file_path}")
        else:
            print(f"   ❌ Archivo faltante: {file_path}")
            return False
    
    return True

def main():
    """Ejecuta todas las pruebas"""
    print("🔬 SISTEMA SCANNER - PRUEBAS DE VALIDACIÓN")
    print("=" * 50)
    
    tests = [
        ("Estructura de directorios", test_directory_structure),
        ("Importaciones externas", test_imports),
        ("Módulos del proyecto", test_project_modules),
        ("Funcionalidad básica", test_basic_functionality),
        ("Escaneo de hardware", test_hardware_scanning),
        ("Conexión MongoDB", test_mongodb_connection)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_function in tests:
        print(f"\\n{'─' * 30}")
        try:
            if test_function():
                passed_tests += 1
                print(f"✅ {test_name}: PASÓ")
            else:
                print(f"❌ {test_name}: FALLÓ")
        except Exception as e:
            print(f"💥 {test_name}: ERROR - {e}")
    
    print(f"\\n{'═' * 50}")
    print(f"📊 RESULTADO FINAL: {passed_tests}/{total_tests} pruebas pasaron")
    
    if passed_tests == total_tests:
        print("🎉 ¡Todos los tests pasaron! El sistema está listo para usar.")
        return_code = 0
    else:
        print("⚠️ Algunos tests fallaron. Revise los errores antes de usar el sistema.")
        return_code = 1
    
    print("\\n💡 Para ejecutar el sistema:")
    print("   python main.py                    # Interfaz interactiva")
    print("   python main.py --help            # Ver todas las opciones")
    print("   python main.py --test-mongodb    # Probar MongoDB")
    
    sys.exit(return_code)

if __name__ == "__main__":
    main()