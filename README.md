# 🖥️ Sistema Scanner Windows

<div align="center">

![Version](https://img.shields.io/badge/version-1.1.0-blue.svg?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.7%2B-brightgreen.svg?style=for-the-badge)
![Windows](https://img.shields.io/badge/platform-Windows%207%2F8%2F10%2F11-lightgrey.svg?style=for-the-badge)
![License](https://img.shields.io/badge/license-Educational-orange.svg?style=for-the-badge)

**🔍 Herramienta Avanzada de Escaneo y Mantenimiento Automatizado**

_Análisis profundo de hardware, software y configuraciones de seguridad con integración MongoDB_

</div>

---

## 📋 Descripción

Sistema Scanner Windows es una herramienta avanzada de escaneo y mantenimiento automatizado para sistemas Windows. Proporciona análisis profundo de hardware, software y configuraciones de seguridad, con integración a MongoDB para almacenamiento centralizado de datos.

## ✨ Características Principales

<table>
<tr>
<td width="50%">

### 🔍 **Escaneo de Hardware Avanzado**

- 💽 **Discos:** Modelo, marca, tipo (SSD/HDD), particiones, espacio libre/usado
- 🖼️ **Tarjeta Gráfica:** Nombre, VRAM, versión de driver, temperaturas
- 🧠 **Memoria RAM:** Capacidad instalada, velocidad, módulos detectados
- ⚡ **Procesador Detallado:**
  - 🔢 Núcleos físicos y lógicos
  - 🧵 Hilos por núcleo (Hyperthreading)
  - 📊 Uso por núcleo en tiempo real
  - 🏭 Arquitectura y especificaciones técnicas

### 🖥️ **Información del Sistema**

- 🪟 **Sistema Operativo:** Versión completa, arquitectura (32/64 bits)
- 🆔 **Identificación:** Hostname, Device ID, Product ID
- 🔑 **Clave de Producto:** Detección automática (opcional)

</td>
<td width="50%">

### 🔒 **Análisis de Seguridad Optimizado**

- 🛡️ **Firewall:** Estado por perfil, conteo de reglas
- 🔌 **Puertos Inteligentes:**
  - ⚡ **Filtrado crítico** (solo puertos importantes)
  - 📊 **Resumen optimizado** para MongoDB
  - 🔍 Conexiones activas con procesos
- 📦 **Actualizaciones Avanzadas:**
  - 🆕 **Sistema:** Actualizaciones pendientes de Windows
  - 🔄 **Drivers:** Detección de drivers obsoletos
  - ⚠️ **Alertas:** Reinicio requerido, auto-updates
- 💿 **Software Instalado:** Lista completa optimizada
- 🔧 **Drivers:** Estado y problemas detectados

### 📈 **Monitoreo en Tiempo Real**

- 📊 Uso de CPU por núcleo
- 🌡️ Temperaturas de componentes
- 💾 Estado de memoria en tiempo real

</td>
</tr>
</table>

### 🔧 Funcionalidades Adicionales

- ⚡ **Activación Windows/Office:** Scripts automatizados con confirmaciones de seguridad
- 🗃️ **Base de Datos MongoDB:** Almacenamiento centralizado con reintentos automáticos
- 📝 **Logging Avanzado:** Rotación automática, múltiples niveles, archivos separados
- 🎨 **Interfaz Rich:** Menús coloridos, barras de progreso, tablas formateadas

---

## 🏗️ Arquitectura del Sistema

### 📊 Flujo de Datos

```mermaid
graph TB
    A[🖥️ Sistema Windows] --> B[🔍 System Scanner]
    A --> C[🔒 Security Scanner]

    B --> D[💽 Hardware Info]
    B --> E[🖥️ OS Info]
    B --> F[🔄 Updates Info]

    C --> G[🛡️ Firewall Status]
    C --> H[🔌 Critical Ports Only]
    C --> I[📦 Software Summary]

    D --> J[📊 Data Aggregator]
    E --> J
    F --> J
    G --> J
    H --> J
    I --> J

    J --> K[💾 Local Storage]
    J --> L[🗃️ MongoDB Atlas]

    K --> M[📄 JSON Files]
    L --> N[📈 Centralized Database]

    style A fill:#e1f5fe
    style J fill:#f3e5f5
    style L fill:#e8f5e8
    style H fill:#fff3e0
```

### 🧩 Componentes del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    🖥️ SISTEMA SCANNER WINDOWS                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   🔍 SCANNER    │  │  🔒 SECURITY   │  │  🎨 INTERFACE  │ │
│  │    MODULE       │  │     MODULE      │  │     MODULE     │ │
│  │                 │  │                 │  │                │ │
│  │ • Hardware      │  │ • Firewall     │  │ • Rich Console │ │
│  │ • CPU Details   │  │ • Critical     │  │ • Progress     │ │
│  │ • Memory        │  │   Ports Only   │  │ • Tables       │ │
│  │ • Disks         │  │ • Updates      │  │ • Menus        │ │
│  │ • GPU           │  │ • Software     │  │                │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  🗃️ DATABASE   │  │  📝 LOGGING    │  │  ⚡ ACTIVATION  │ │
│  │     MODULE      │  │     MODULE      │  │     MODULE     │ │
│  │                 │  │                 │  │                │ │
│  │ • MongoDB       │  │ • Rotation     │  │ • Windows      │ │
│  │ • Retry Logic   │  │ • Security     │  │ • Office       │ │
│  │ • Error Handle  │  │ • Operations   │  │ • Safety       │ │
│  │ • Optimization  │  │ • Debug        │  │   Checks       │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

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

<div align="center">

### 📋 Requisitos del Sistema

| Componente      | Requerimiento | Recomendado   | Estado                                                              |
| --------------- | ------------- | ------------- | ------------------------------------------------------------------- |
| 🐍 **Python**   | 3.7+          | 3.9+          | ![Python](https://img.shields.io/badge/python-required-red)         |
| 🪟 **Windows**  | 7/8/10/11     | 10/11 64-bit  | ![Windows](https://img.shields.io/badge/windows-compatible-green)   |
| 👑 **Permisos** | Usuario       | Administrador | ![Admin](https://img.shields.io/badge/admin-recommended-orange)     |
| 💾 **Espacio**  | 50 MB         | 200 MB        | ![Space](https://img.shields.io/badge/space-minimal-blue)           |
| 🌐 **Red**      | Opcional      | MongoDB Atlas | ![Network](https://img.shields.io/badge/network-optional-lightgrey) |

</div>

### 📦 Pasos de Instalación

<table>
<tr>
<td width="50%">

#### 🔽 **Paso 1: Obtener el Código**

```bash
# 🌟 Método recomendado - Git
git clone https://github.com/felipesanchez-dev/proyecto.git
cd proyecto

# 📁 Alternativo - Descargar ZIP
# Descomprimir en carpeta deseada
```

#### 🐍 **Paso 2: Dependencias Python**

```bash
# 🚀 Instalación automática
pip install -r requirements.txt

# 🔧 Manual (si es necesario)
pip install psutil==5.9.6
pip install pymongo==4.6.0
pip install rich==13.7.0
pip install wmi==1.5.1
```

</td>
<td width="50%">

#### 🗃️ **Paso 3: MongoDB (Opcional)**

```bash
# 🌐 Atlas Cloud (Recomendado)
set MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/

# 🏠 Local (Alternativo)
set MONGO_URI=mongodb://localhost:27017/

# ✅ Verificar conexión
python main.py --test-mongodb
```

#### ✅ **Paso 4: Verificación**

```bash
# 🧪 Ejecutar pruebas completas
python test_system.py

# 🎯 Prueba rápida
python main.py --help

# 🔍 Escaneo de prueba
python main.py --batch --scan-only
```

</td>
</tr>
</table>

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

| Variable    | Descripción               | Valor por Defecto            |
| ----------- | ------------------------- | ---------------------------- |
| `MONGO_URI` | URI de conexión a MongoDB | `mongodb://localhost:27017/` |

---

## 🎬 Demostración Visual

### 🖥️ Interfaz del Sistema

<table>
<tr>
<td width="50%">

#### 🎨 **Menú Principal**

```
╔══════════════════════════════════════════════════╗
║            SISTEMA SCANNER WINDOWS               ║
║         Mantenimiento Automatizado v1.1         ║
╚══════════════════════════════════════════════════╝

┌─────────── MENÚ PRINCIPAL ────────────────────────┐
│                                                   │
│  1. Escaneo Profundo del Sistema y Subida MongoDB │
│  2. Activación de Windows/Office        ⚠️       │
│  3. Salir del Sistema                            │
│                                                   │
│  Seleccione una opción (1-3):                    │
└───────────────────────────────────────────────────┘
```

#### 📊 **Progreso de Escaneo**

```
🔄 Escaneando hardware...          ████████████ 100%
🔒 Escaneando seguridad...         ████████████ 100%
💾 Guardando datos...              ████████████ 100%

✅ Escaneo completado - ID: 0d10a891
```

</td>
<td width="50%">

#### 📋 **Resultados del Escaneo**

```
┌────────── ✓ Escaneo Completado ──────────────────┐
│ ID de Escaneo: 0d10a891-91e2...                 │
│ PIN de Acceso: A7X9                             │
│ Timestamp:     2025-09-16T18:07:42              │
│ Hostname:      DESKTOP-ABC123                   │
└──────────────────────────────────────────────────┘

┌────────── Hardware Detectado ────────────────────┐
│ CPU    │ Intel Core i7 - 6 núcleos, 12 hilos   │
│        │ (HT habilitado) - Uso: 16.8%           │
│ RAM    │ 15.89 GB total - 45.2% usado           │
│ Discos │ 2 discos - 512.0 GB total              │
│ GPU    │ 1 GPU - Intel Iris Xe Graphics         │
└──────────────────────────────────────────────────┘

┌────────── Estado de Actualizaciones ─────────────┐
│ Sistema │ 1 pendientes (Auto habilitado)        │
│ Drivers │ 129 de 177 obsoletos (Revisar)       │
└──────────────────────────────────────────────────┘
```

</td>
</tr>
</table>

### 🚀 **Comandos de Ejemplo en Acción**

<details>
<summary><b>💻 Ver Ejemplos de Línea de Comandos</b></summary>

#### Escaneo Básico

```powershell
PS> python main.py --batch --no-sensitive --output scan.json
🔄 Ejecutando escaneo en modo batch...
   📊 Escaneando hardware...
   🔒 Escaneando seguridad...
   💾 Guardando escaneo localmente...
✅ Escaneo completado - ID: 0d10a891-91e2-4108-a6e4-7fe08e224fbd
```

#### Verificación MongoDB

```powershell
PS> python main.py --test-mongodb
🔗 Probando conexión a MongoDB...
✅ Conexión exitosa a proyectofinal.scans
📊 Documentos en colección: 15
✅ MongoDB está funcionando correctamente
```

#### Limpieza de Archivos

```powershell
PS> python main.py --cleanup-logs 30 --cleanup-scans 7
🧹 Limpiando logs antiguos (>30 días)...
   📁 Eliminados: 5 archivos de log
🧹 Limpiando escaneos antiguos (>7 días)...
   📁 Eliminados: 12 archivos JSON
✅ Limpieza completada
```

</details>

## 📊 Formato de Datos y Ejemplos

### 🏗️ Estructura del Escaneo JSON

<details>
<summary><b>📋 Ver Estructura Completa (Click para expandir)</b></summary>

```json
{
  "identifiers": {
    "scan_id": "0d10a891-91e2-4108-a6e4-7fe08e224fbd",
    "access_pin": "A7X9",
    "timestamp": "2025-09-16T18:07:42.188431"
  },
  "system_info": {
    "hardware": {
      "cpu": {
        "processor_name": "Intel64 Family 6 Model 141 Stepping 1, GenuineIntel",
        "physical_cores": 6,
        "logical_cores": 12,
        "threads_per_core": 2,
        "hyperthreading_enabled": true,
        "cpu_usage_percent": 16.8,
        "per_cpu_usage": [9.2, 10.9, 18.8, 10.9, 15.6, 4.7]
      },
      "memory": {
        "total_gb": 15.89,
        "used_percent": 45.2
      },
      "disks": [...],
      "gpu": [...]
    },
    "operating_system": {
      "system": "Windows",
      "release": "11",
      "hostname": "DESKTOP-ABC123"
    },
    "updates": {
      "system_updates": {
        "total_pending": 1,
        "reboot_required": false,
        "automatic_updates_enabled": true
      },
      "driver_updates": {
        "total_drivers": 177,
        "drivers_needing_update": 129
      }
    },
    "security": {
      "firewall": {
        "status": "fully_enabled"
      },
      "ports_summary": {
        "total_ports": 24,
        "critical_count": 5,
        "summary": "Se encontraron 24 puertos abiertos, 5 son críticos"
      }
    }
  },
  "scan_settings": {
    "include_sensitive": false,
    "scanner_version": "1.1.0"
  }
}
```

</details>

### 📈 Ejemplos de Salida Real

<table>
<tr>
<td width="50%">

#### 💻 **Información de CPU Detallada**

```json
{
  "physical_cores": 6,
  "logical_cores": 12,
  "threads_per_core": 2,
  "hyperthreading_enabled": true,
  "cpu_usage_percent": 16.8,
  "architecture": "AMD64",
  "max_frequency_mhz": 2688.0
}
```

#### 🔌 **Puertos Optimizados**

```json
{
  "total_ports": 24,
  "critical_count": 5,
  "critical_ports": [
    {
      "protocol": "TCP",
      "local_port": 445,
      "process_name": "System"
    }
  ],
  "summary": "24 puertos, 5 críticos"
}
```

</td>
<td width="50%">

#### 🔄 **Estado de Actualizaciones**

```json
{
  "system_updates": {
    "total_pending": 1,
    "reboot_required": false,
    "automatic_updates_enabled": true
  },
  "driver_updates": {
    "drivers_needing_update": 129,
    "total_drivers": 177
  }
}
```

#### 📊 **Resumen de Hardware**

```json
{
  "memory": {
    "total_gb": 15.89,
    "used_percent": 45.2
  },
  "disks": 2,
  "gpu_count": 1,
  "cpu_cores": "6/12"
}
```

</td>
</tr>
</table>

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

### 🚨 Errores Comunes y Soluciones

<table>
<tr>
<td width="50%">

#### ❌ **Errores de Dependencias**

```bash
ImportError: No module named 'psutil'
```

**🔧 Solución:**

```bash
pip install -r requirements.txt
# O individual:
pip install psutil pymongo rich wmi
```

#### ❌ **Errores de Conexión MongoDB**

```bash
pymongo.errors.ServerSelectionTimeoutError
```

**🔧 Solución:**

```bash
# 1️⃣ Verificar conexión
python main.py --test-mongodb

# 2️⃣ Configurar URI
set MONGO_URI=mongodb+srv://user:pass@cluster/

# 3️⃣ Verificar firewall/red
```

</td>
<td width="50%">

#### ❌ **Errores de Permisos**

```bash
Access Denied (wmic, netsh)
```

**🔧 Solución:**

```bash
# Ejecutar como Administrador
# Clic derecho → "Ejecutar como administrador"
```

#### ❌ **Timeouts del Sistema**

```bash
subprocess.TimeoutExpired
```

**🔧 Solución:**

```bash
# 1️⃣ Verificar antivirus no bloquee
# 2️⃣ Ejecutar con más privilegios
# 3️⃣ Revisar procesos colgados
```

#### ❌ **Error WMI**

```bash
wmi.x_wmi: <unknown>
```

**🔧 Solución:**

```bash
# Reparar WMI en Windows
winmgmt /verifyrepository
winmgmt /salvagerepository
```

</td>
</tr>
</table>

### 🔍 Diagnóstico Paso a Paso

<details>
<summary><b>🩺 Guía Completa de Diagnóstico</b></summary>

#### 1️⃣ **Verificación del Sistema**

```powershell
# Comprobar Python
python --version
# Debe mostrar: Python 3.7+

# Comprobar módulos
python -c "import psutil, pymongo, rich, wmi; print('✅ Módulos OK')"

# Ejecutar diagnóstico completo
python test_system.py
```

#### 2️⃣ **Verificación de Red y MongoDB**

```powershell
# Ping a MongoDB Atlas
ping cluster0.abc123.mongodb.net

# Test de conexión específico
python main.py --test-mongodb --log-level DEBUG

# Verificar variables de entorno
echo $env:MONGO_URI
```

#### 3️⃣ **Verificación de Permisos**

```powershell
# Verificar si es administrador
net session 2>$null
if ($?) { "✅ Administrador" } else { "❌ Usuario normal" }

# Test de comandos del sistema
wmic computersystem get name
netsh advfirewall show currentprofile state
```

#### 4️⃣ **Logs de Diagnóstico**

```powershell
# Ver logs recientes de errores
Get-Content logs\errors.log -Tail 20

# Ver logs de seguridad
Get-Content logs\security.log -Tail 10

# Log completo con debug
python main.py --log-level DEBUG --batch 2>&1 | Tee-Object debug.log
```

</details>

### Archivos de Log para Diagnóstico

| Archivo                    | Contenido                         |
| -------------------------- | --------------------------------- |
| `logs/sistema_scanner.log` | Log principal con rotación diaria |
| `logs/errors.log`          | Solo errores críticos             |
| `logs/security.log`        | Eventos de seguridad              |

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

<div align="center">

## 🎯 Estadísticas del Proyecto

![GitHub repo size](https://img.shields.io/github/repo-size/felipesanchez-dev/proyecto?style=for-the-badge)
![GitHub code size](https://img.shields.io/github/languages/code-size/felipesanchez-dev/proyecto?style=for-the-badge)
![Lines of code](https://img.shields.io/tokei/lines/github/felipesanchez-dev/proyecto?style=for-the-badge)

### 📊 Características Técnicas

| Métrica               | Valor            | Estado                                                              |
| --------------------- | ---------------- | ------------------------------------------------------------------- |
| 🐍 **Versión Python** | 3.7+             | ![Compatible](https://img.shields.io/badge/status-compatible-green) |
| 📦 **Módulos**        | 7 principales    | ![Modular](https://img.shields.io/badge/design-modular-blue)        |
| 🗃️ **Base de Datos**  | MongoDB Atlas    | ![Cloud](https://img.shields.io/badge/storage-cloud-orange)         |
| 🔒 **Seguridad**      | Logging completo | ![Secure](https://img.shields.io/badge/security-enhanced-red)       |
| 🎨 **Interfaz**       | Rich Console     | ![Modern](https://img.shields.io/badge/ui-modern-purple)            |

### 🚀 Próximas Mejoras (Roadmap)

- [ ] 🌐 **API REST** para integración remota
- [ ] 📱 **Interfaz web** con dashboard
- [ ] 🔄 **Escaneo automático** programado
- [ ] 📧 **Notificaciones** por email/Teams
- [ ] 🏢 **Modo empresarial** multi-equipo
- [ ] 🔐 **Autenticación** OAuth2/AD

### 🤝 Contribuir al Proyecto

```bash
# 1️⃣ Fork del repositorio
git fork https://github.com/felipesanchez-dev/proyecto

# 2️⃣ Crear rama de feature
git checkout -b feature/nueva-funcionalidad

# 3️⃣ Commit y push
git commit -m "✨ Agregar nueva funcionalidad"
git push origin feature/nueva-funcionalidad

# 4️⃣ Crear Pull Request
```

---

**© 2025 Sistema Scanner Windows v1.1.0**  
_🔍 Herramienta avanzada de escaneo y mantenimiento automatizado para Windows_

**Desarrollado por Felipe Sánchez**

[![GitHub](https://img.shields.io/badge/GitHub-felipesanchez--dev-black?style=for-the-badge&logo=github)](https://github.com/felipesanchez-dev)
[![License](https://img.shields.io/badge/License-Educational-orange?style=for-the-badge)](LICENSE)

</div>
