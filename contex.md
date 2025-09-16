Eres un ingeniero de software senior especializado en mantenimiento automatizado de sistemas Windows.
Tu tarea es crear un módulo de consola en Python que escanee profundamente el hardware y estado del sistema y lo publique en una base de datos MongoDB.

El módulo debe:

Escaneo de sistema (hardware/software):

Discos: modelo/marca, tipo (SSD/HDD), particiones, espacio total/uso/libre.

Tarjeta gráfica: nombre, VRAM, driver.

RAM instalada y velocidad (si es detectable).

Procesador: fabricante, modelo, núcleos físicos/lógicos, velocidad.

Versión y edición de Windows (ej. Windows 10 Pro 22H2).

Arquitectura (32/64 bits).

Nombre del dispositivo (hostname), ID del dispositivo y ProductId.

Clave de producto de Windows (solo si no se usa --no-sensitive).

Estado del Firewall (activo/inactivo, perfiles, reglas resumidas).

Puertos abiertos / conexiones de escucha (netstat).

Hotfixes y actualizaciones instaladas (wmic qfe).

Drivers sin actualizar (si se puede detectar).

Software instalado (resumen).

Gestión de seguridad y flags:

Flag --no-sensitive → excluye clave de producto y datos sensibles.

Generación de identificadores:

scan_id como UUID v4.

Código aleatorio alfanumérico de 4 caracteres (PIN de acceso).

Guardar el JSON en archivo local organizado.

Publicación de resultados:

Enviar el documento a MongoDB →

Base de datos: proyectofinal

Colección: scans

La URI debe leerse desde variable de entorno (MONGO_URI).

Si no está definida, usar la URI provista como fallback (con advertencia).

Logs:

Registrar en consola y en archivo .log.

Manejar reintentos al enviar a MongoDB.

Interfaz de consola (menú principal con colores usando rich):

Opción 1 → Escaneo profundo del sistema y subida a MongoDB.

Opción 2 → Activación de Windows/Office (placeholder configurable).

Mostrar advertencia ⚠️.

Ejecutar un comando externo definido por el usuario (ej. Massgrave con PowerShell).

Preguntar confirmación antes de lanzar el comando.

Opción 3 → Salir.

Dependencias:

psutil (hardware info).

pymongo (conexión a MongoDB).

rich (interfaz de consola).

uuid, random, subprocess, platform, argparse.


para la activacion si el suario llega a solicitarlo los comandos que se deben cuando se le clik son los siguientes
How to Activate Windows / Office / Extended Updates (ESU)?
Method 1 - PowerShell ❤️
Open PowerShell
Click the Start Menu, type PowerShell, then open it.

Copy and paste the code below, then press enter.

For Windows 8, 10, 11: 📌
irm https://get.activated.win | iex
For Windows 7 and later:
iex ((New-Object Net.WebClient).DownloadString('https://get.activated.win'))

estos comandos estaras si o si en el codigo y serviran 