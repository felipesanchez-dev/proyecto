# Sistema Scanner Windows

**Versión:** 1.0.0  
**Autor:** Sistema de Mantenimiento Automatizado  
**Plataforma:** Windows 7/8/10/11  

## 📋 Descripción

Sistema Scanner Windows es una herramienta avanzada de escaneo y mantenimiento automatizado para sistemas Windows. Proporciona análisis profundo de hardware, software y configuraciones de seguridad, con integración a MongoDB para almacenamiento centralizado de datos.

## ✨ Características Principales

### 🔍 Escaneo de Hardware
- **Discos:** Modelo, marca, tipo (SSD/HDD), particiones, espacio libre/usado
- **Tarjeta Gráfica:** Nombre, VRAM, versión de driver  
- **Memoria RAM:** Capacidad instalada, velocidad, módulos detectados
- **Procesador:** Fabricante, modelo, núcleos físicos/lógicos, velocidades

### 🖥️ Información del Sistema
- **Sistema Operativo:** Versión completa de Windows, arquitectura (32/64 bits)
- **Identificación:** Hostname, Device ID, Product ID
- **Clave de Producto:** Detección automática (opcional, configurable)

### 🔒 Análisis de Seguridad
- **Firewall:** Estado por perfil, conteo de reglas
- **Puertos Abiertos:** Conexiones de escucha activas con procesos
- **Actualizaciones:** Hotfixes y parches instalados (wmic qfe)
- **Software Instalado:** Lista completa de programas detectados
- **Drivers:** Estado y problemas detectados

### 🔧 Funcionalidades Adicionales
- **Activación Windows/Office:** Scripts automatizados con confirmaciones de seguridad
- **Base de Datos MongoDB:** Almacenamiento centralizado con reintentos automáticos
- **Logging Avanzado:** Rotación automática, múltiples niveles, archivos separados
- **Interfaz Rich:** Menús coloridos, barras de progreso, tablas formateadas

## 📁 Estructura del Proyecto

```
sistema_scanner/
├── main.py                    # Punto de entrada principal
├── requirements.txt           # Dependencias Python
├── test_system.py            # Script de pruebas
├── modules/                   # Módulos principales
│   ├── __init__.py
│   ├── scanner.py            # Escaneo de hardware
│   ├── security_scanner.py   # Análisis de seguridad
│   ├── database.py           # Integración MongoDB
│   ├── interface.py          # Interfaz Rich
│   ├── activation.py         # Activación Windows/Office
│   ├── utils.py              # Utilidades y persistencia
│   └── logging_setup.py      # Sistema de logging
├── config/                    # Configuraciones
│   ├── __init__.py
│   └── settings.py           # Configuraciones globales
├── logs/                      # Archivos de log
├── scans/                     # Escaneos JSON locales
└── README.md                  # Esta documentación
```

## 🚀 Instalación

### Prerrequisitos
- **Python 3.7+** (recomendado Python 3.9+)
- **Windows 7/8/10/11** (64-bit recomendado)
- **Privilegios de Administrador** (para algunas funciones)

### Paso 1: Clonar/Descargar el Proyecto
```bash
# Si usa Git
git clone <repository-url>
cd sistema_scanner

# O descomprimir el archivo ZIP en una carpeta
```

### Paso 2: Instalar Dependencias
```bash
# Instalar dependencias requeridas
pip install -r requirements.txt

# O instalar individualmente:
pip install psutil==5.9.6 pymongo==4.6.0 rich==13.7.0 wmi==1.5.1
```

### Paso 3: Configurar MongoDB (Opcional)
```bash
# Configurar variable de entorno (opcional)
set MONGO_URI=mongodb://usuario:password@servidor:27017/

# O usar la URI por defecto: mongodb://localhost:27017/
```

### Paso 4: Verificar Instalación
```bash
# Ejecutar pruebas del sistema
python test_system.py

# Probar conexión MongoDB (opcional)
python main.py --test-mongodb
```

## 🎮 Uso del Sistema

### Modo Interactivo (Recomendado)
```bash
# Ejecutar interfaz completa
python main.py
```

**Menú Principal:**
1. **Escaneo Profundo del Sistema** - Análisis completo + subida MongoDB
2. **Activación Windows/Office** - Scripts de activación con advertencias
3. **Salir** - Cierre seguro del sistema

### Modo Línea de Comandos (Avanzado)

#### Escaneo Básico
```bash
# Escaneo completo con datos sensibles
python main.py --batch

# Escaneo sin datos sensibles
python main.py --batch --no-sensitive

# Solo escaneo local (sin MongoDB)
python main.py --batch --scan-only

# Guardar en archivo específico
python main.py --batch --output mi_escaneo.json
```

#### Configuración y Mantenimiento
```bash
# Probar conexión MongoDB
python main.py --test-mongodb

# Configurar URI personalizada
python main.py --mongo-uri "mongodb://miservidor:27017/" --test-mongodb

# Limpiar archivos antiguos
python main.py --cleanup-logs 30        # Logs > 30 días
python main.py --cleanup-scans 7        # Escaneos > 7 días

# Listar escaneos guardados
python main.py --list-scans

# Habilitar logging detallado
python main.py --log-level DEBUG --batch
```

#### Opciones de Logging
```bash
# Sin archivos de log (solo consola)
python main.py --no-log-file

# Nivel específico de logging
python main.py --log-level WARNING
```

### Variables de Entorno Soportadas

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `MONGO_URI` | URI de conexión a MongoDB | `mongodb://localhost:27017/` |

## 📊 Formato de Datos

### Estructura del Escaneo JSON
```json
{
  "identifiers": {
    "scan_id": "uuid-v4-generado",
    "access_pin": "PIN4",
    "timestamp": "2024-01-15T10:30:00.000Z"
  },
  "system_info": {
    "hardware": {
      "disks": [...],
      "gpu": [...],
      "memory": {...},
      "cpu": {...}
    },
    "operating_system": {...},
    "security": {
      "firewall": {...},
      "open_ports": [...],
      "hotfixes": [...],
      "installed_software_summary": {...}
    }
  },
  "scan_settings": {
    "include_sensitive": true/false,
    "scanner_version": "1.0.0"
  }
}
```

### Base de Datos MongoDB
- **Base de Datos:** `proyectofinal`
- **Colección:** `scans`
- **Índices Recomendados:** 
  - `identifiers.scan_id` (único)
  - `identifiers.timestamp` (descendente)

## 🔒 Consideraciones de Seguridad

### Datos Sensibles Manejados
- **Clave de Producto Windows** (opcional con `--no-sensitive`)
- **Números de Serie** del hardware
- **Información de Red** detallada
- **Lista Completa de Software** instalado

### Logging de Seguridad
Todos los eventos sensibles se registran en:
- **Archivo:** `logs/security.log`
- **Eventos:** Acceso a datos, activaciones, comandos externos, operaciones BD

### Recomendaciones
1. **Ejecutar como Administrador** solo cuando sea necesario
2. **Usar `--no-sensitive`** en entornos de producción
3. **Configurar MongoDB** con autenticación habilitada
4. **Revisar logs regularmente** para detectar actividad sospechosa
5. **Mantener backups** antes de usar funciones de activación

## ⚡ Activación Windows/Office

### ⚠️ ADVERTENCIA CRÍTICA
**Esta funcionalidad ejecuta scripts de terceros que pueden:**
- Modificar configuraciones críticas del sistema
- Ser detectados por software antivirus
- Afectar la estabilidad del sistema
- Violar términos de licencia

### Comandos Utilizados

**Windows 8/10/11:**
```powershell
irm https://get.activated.win | iex
```

**Windows 7 y anteriores:**
```powershell
iex ((New-Object Net.WebClient).DownloadString('https://get.activated.win'))
```

### Proceso de Confirmación
1. **Advertencia de riesgo** con detalles completos
2. **Confirmación de comprensión** de riesgos
3. **Revisión del comando** específico a ejecutar
4. **Confirmación final** antes de ejecución

## 🐛 Solución de Problemas

### Errores Comunes

#### ImportError: No module named 'psutil'
```bash
# Solución: Instalar dependencias
pip install -r requirements.txt
```

#### Error de Conexión MongoDB
```bash
# Verificar MongoDB ejecutándose
python main.py --test-mongodb

# Configurar URI personalizada
set MONGO_URI=mongodb://localhost:27017/
```

#### Permiso Denegado (wmic, netsh)
```bash
# Ejecutar como Administrador
# Botón derecho → "Ejecutar como administrador"
```

#### Timeout en Comandos del Sistema
```bash
# Incrementar timeout o ejecutar con más privilegios
# Verificar que no haya software de seguridad bloqueando
```

### Archivos de Log para Diagnóstico

| Archivo | Contenido |
|---------|-----------|
| `logs/sistema_scanner.log` | Log principal con rotación diaria |
| `logs/errors.log` | Solo errores críticos |
| `logs/security.log` | Eventos de seguridad |

### Comandos de Diagnóstico
```bash
# Verificar sistema completo
python test_system.py

# Ver logs recientes
type logs\\sistema_scanner.log | findstr ERROR
type logs\\errors.log

# Limpiar y reiniciar
python main.py --cleanup-logs 1 --cleanup-scans 1
```

## 🔧 Desarrollo y Personalización

### Agregar Nuevos Escáneres
1. Crear clase en `modules/`
2. Implementar métodos de escaneo
3. Integrar en `scanner.py` o `security_scanner.py`
4. Actualizar interfaz si es necesario

### Modificar Base de Datos
1. Editar `config/settings.py` para nuevas configuraciones
2. Actualizar `modules/database.py` para cambios de esquema
3. Considerar migración de datos existentes

### Personalizar Interfaz
1. Modificar `modules/interface.py` para nuevos menús
2. Usar componentes Rich para consistencia visual
3. Mantener confirmaciones de seguridad

## 📄 Licencia y Responsabilidades

### Uso del Software
- **Propósito:** Educativo y de diagnóstico únicamente
- **Responsabilidad:** Usuario asume todos los riesgos
- **Garantía:** Sin garantía expresada o implícita

### Funcionalidades de Activación
- **Riesgo:** Scripts de terceros no auditados
- **Legalidad:** Usuario responsable del cumplimiento legal
- **Soporte:** Sin soporte para problemas derivados del uso

## 🤝 Contribución

### Reportar Problemas
1. Ejecutar `python test_system.py`
2. Incluir logs relevantes
3. Describir pasos para reproducir
4. Especificar versión de Windows y Python

### Mejoras Sugeridas
- Nuevos tipos de escaneo
- Optimizaciones de rendimiento
- Mejoras en la interfaz
- Compatibilidad con otros sistemas

---

**© 2025 Sistema Scanner Windows v1.0.0**  
*Herramienta de mantenimiento automatizado para Windows*