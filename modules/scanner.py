"""
Módulo de escaneo del sistema Windows
Escanea hardware, software y configuraciones de seguridad
"""
import psutil
import platform
import subprocess
import json
import os
import uuid
import random
import string
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import wmi

class SystemScanner:
    """Escáner completo del sistema Windows"""
    
    def __init__(self, include_sensitive: bool = True):
        self.include_sensitive = include_sensitive
        self.logger = logging.getLogger(__name__)
        self.wmi_connection = None
        
        try:
            self.wmi_connection = wmi.WMI()
        except Exception as e:
            self.logger.warning(f"No se pudo establecer conexión WMI: {e}")
    
    def generate_identifiers(self) -> Dict[str, str]:
        """Genera identificadores únicos para el escaneo"""
        scan_id = str(uuid.uuid4())
        access_pin = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        
        return {
            "scan_id": scan_id,
            "access_pin": access_pin,
            "timestamp": datetime.now().isoformat()
        }
    
    def scan_disks(self) -> List[Dict[str, Any]]:
        """Escanea información de discos y particiones"""
        disks_info = []
        
        try:
            # Obtener particiones
            partitions = psutil.disk_partitions()
            
            for partition in partitions:
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    
                    disk_info = {
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total_gb": round(partition_usage.total / (1024**3), 2),
                        "used_gb": round(partition_usage.used / (1024**3), 2),
                        "free_gb": round(partition_usage.free / (1024**3), 2),
                        "percent_used": round((partition_usage.used / partition_usage.total) * 100, 2)
                    }
                    
                    # Intentar obtener información del disco físico via WMI
                    if self.wmi_connection:
                        try:
                            for disk in self.wmi_connection.Win32_DiskDrive():
                                if partition.device.replace('\\', '').replace(':', '') in disk.DeviceID.replace('\\', ''):
                                    disk_info.update({
                                        "model": disk.Model,
                                        "size_bytes": disk.Size,
                                        "interface_type": disk.InterfaceType,
                                        "media_type": "SSD" if "SSD" in disk.Model else "HDD"
                                    })
                                    break
                        except Exception as e:
                            self.logger.warning(f"Error obteniendo info WMI del disco: {e}")
                    
                    disks_info.append(disk_info)
                    
                except PermissionError:
                    self.logger.warning(f"Sin permisos para acceder a {partition.mountpoint}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error escaneando discos: {e}")
            
        return disks_info
    
    def scan_gpu(self) -> List[Dict[str, Any]]:
        """Escanea información de tarjetas gráficas"""
        gpu_info = []
        
        try:
            if self.wmi_connection:
                for gpu in self.wmi_connection.Win32_VideoController():
                    if gpu.Name:
                        gpu_data = {
                            "name": gpu.Name,
                            "adapter_ram_mb": gpu.AdapterRAM // (1024*1024) if gpu.AdapterRAM else None,
                            "driver_version": gpu.DriverVersion,
                            "driver_date": gpu.DriverDate,
                            "video_processor": gpu.VideoProcessor,
                            "status": gpu.Status
                        }
                        gpu_info.append(gpu_data)
        except Exception as e:
            self.logger.error(f"Error escaneando GPU: {e}")
            
        return gpu_info
    
    def scan_memory(self) -> Dict[str, Any]:
        """Escanea información de memoria RAM"""
        memory_info = {
            "total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
            "used_percent": psutil.virtual_memory().percent,
            "modules": []
        }
        
        try:
            if self.wmi_connection:
                for memory_module in self.wmi_connection.Win32_PhysicalMemory():
                    module_info = {
                        "capacity_gb": int(memory_module.Capacity) // (1024**3) if memory_module.Capacity else None,
                        "speed_mhz": memory_module.Speed,
                        "manufacturer": memory_module.Manufacturer,
                        "part_number": memory_module.PartNumber,
                        "serial_number": memory_module.SerialNumber if self.include_sensitive else "***HIDDEN***"
                    }
                    memory_info["modules"].append(module_info)
        except Exception as e:
            self.logger.error(f"Error escaneando memoria: {e}")
            
        return memory_info
    
    def scan_cpu(self) -> Dict[str, Any]:
        """Escanea información del procesador"""
        cpu_info = {
            "processor_name": platform.processor(),
            "architecture": platform.machine(),
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "max_frequency_mhz": psutil.cpu_freq().max if psutil.cpu_freq() else None,
            "current_frequency_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else None
        }
        
        try:
            if self.wmi_connection:
                for processor in self.wmi_connection.Win32_Processor():
                    cpu_info.update({
                        "manufacturer": processor.Manufacturer,
                        "family": processor.Family,
                        "model": processor.Model,
                        "stepping": processor.Stepping,
                        "l2_cache_size_kb": processor.L2CacheSize,
                        "l3_cache_size_kb": processor.L3CacheSize
                    })
                    break  # Tomar solo el primer procesador
        except Exception as e:
            self.logger.error(f"Error escaneando CPU: {e}")
            
        return cpu_info
    
    def scan_operating_system(self) -> Dict[str, Any]:
        """Escanea información del sistema operativo"""
        os_info = {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "architecture": platform.architecture()[0],
            "hostname": platform.node(),
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
        }
        
        try:
            if self.wmi_connection:
                for os_data in self.wmi_connection.Win32_OperatingSystem():
                    os_info.update({
                        "name": os_data.Name.split('|')[0] if os_data.Name else None,
                        "version_number": os_data.Version,
                        "build_number": os_data.BuildNumber,
                        "install_date": os_data.InstallDate,
                        "last_boot_up_time": os_data.LastBootUpTime,
                        "total_virtual_memory_gb": round(int(os_data.TotalVirtualMemorySize) / (1024*1024), 2) if os_data.TotalVirtualMemorySize else None
                    })
                    
                # Obtener información del sistema
                for system_info in self.wmi_connection.Win32_ComputerSystem():
                    os_info.update({
                        "manufacturer": system_info.Manufacturer,
                        "model": system_info.Model,
                        "total_physical_memory_gb": round(int(system_info.TotalPhysicalMemory) / (1024**3), 2) if system_info.TotalPhysicalMemory else None
                    })
                    
                # Obtener product ID y clave de producto
                if self.include_sensitive:
                    try:
                        for os_product in self.wmi_connection.Win32_OperatingSystem():
                            os_info["serial_number"] = os_product.SerialNumber
                            
                        # Intentar obtener la clave de producto
                        result = subprocess.run([
                            "powershell", "-Command", 
                            "(Get-WmiObject -query 'select * from SoftwareLicensingService').OA3xOriginalProductKey"
                        ], capture_output=True, text=True, timeout=10)
                        
                        if result.returncode == 0 and result.stdout.strip():
                            os_info["product_key"] = result.stdout.strip()
                        else:
                            os_info["product_key"] = "No disponible"
                            
                    except Exception as e:
                        self.logger.warning(f"No se pudo obtener clave de producto: {e}")
                        os_info["product_key"] = "Error al obtener"
                else:
                    os_info["serial_number"] = "***HIDDEN***"
                    os_info["product_key"] = "***HIDDEN***"
                    
        except Exception as e:
            self.logger.error(f"Error escaneando sistema operativo: {e}")
            
        return os_info
    
    def perform_full_scan(self) -> Dict[str, Any]:
        """Realiza un escaneo completo del sistema"""
        self.logger.info("Iniciando escaneo completo del sistema...")
        
        scan_data = {
            "identifiers": self.generate_identifiers(),
            "system_info": {
                "hardware": {
                    "disks": self.scan_disks(),
                    "gpu": self.scan_gpu(),
                    "memory": self.scan_memory(),
                    "cpu": self.scan_cpu()
                },
                "operating_system": self.scan_operating_system()
            },
            "scan_settings": {
                "include_sensitive": self.include_sensitive,
                "scanner_version": "1.0.0"
            }
        }
        
        self.logger.info(f"Escaneo completo finalizado. ID: {scan_data['identifiers']['scan_id']}")
        return scan_data