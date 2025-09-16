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
    
    def __init__(self, include_sensitive: bool = True):
        self.include_sensitive = include_sensitive
        self.logger = logging.getLogger(__name__)
        self.wmi_connection = None
        
        try:
            self.wmi_connection = wmi.WMI()
        except Exception as e:
            self.logger.warning(f"No se pudo establecer conexión WMI: {e}")
    
    def generate_identifiers(self) -> Dict[str, str]:
        scan_id = str(uuid.uuid4())
        access_pin = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        
        return {
            "scan_id": scan_id,
            "access_pin": access_pin,
            "timestamp": datetime.now().isoformat()
        }
    
    def scan_disks(self) -> List[Dict[str, Any]]:
        disks_info = []
        
        try:
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
        cpu_info = {
            "processor_name": platform.processor(),
            "architecture": platform.machine(),
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "threads_per_core": psutil.cpu_count(logical=True) // psutil.cpu_count(logical=False) if psutil.cpu_count(logical=False) else 1,
            "max_frequency_mhz": psutil.cpu_freq().max if psutil.cpu_freq() else None,
            "current_frequency_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else None,
            "cpu_usage_percent": psutil.cpu_percent(interval=1),
            "per_cpu_usage": psutil.cpu_percent(interval=1, percpu=True)
        }
        
        try:
            if self.wmi_connection:
                for processor in self.wmi_connection.Win32_Processor():
                    cpu_info.update({
                        "manufacturer": processor.Manufacturer,
                        "name": processor.Name,
                        "description": processor.Description,
                        "family": processor.Family,
                        "model": processor.Model,
                        "stepping": processor.Stepping,
                        "revision": processor.Revision,
                        "l2_cache_size_kb": processor.L2CacheSize,
                        "l3_cache_size_kb": processor.L3CacheSize,
                        "socket_designation": processor.SocketDesignation,
                        "voltage": processor.CurrentVoltage,
                        "external_clock_mhz": processor.ExternalClock,
                        "data_width": processor.DataWidth,
                        "address_width": processor.AddressWidth,
                        "processor_id": processor.ProcessorId if self.include_sensitive else "***HIDDEN***",
                        "characteristics": processor.Characteristics,
                        "cpu_status": processor.CpuStatus,
                        "load_percentage": processor.LoadPercentage
                    })
                    
                    if processor.NumberOfCores and processor.NumberOfLogicalProcessors:
                        cpu_info["cores_per_socket"] = processor.NumberOfCores
                        cpu_info["logical_processors"] = processor.NumberOfLogicalProcessors
                        cpu_info["hyperthreading_enabled"] = processor.NumberOfLogicalProcessors > processor.NumberOfCores
                    
                    break
                    
        except Exception as e:
            self.logger.error(f"Error escaneando CPU: {e}")
        
        try:
            if self.wmi_connection:
                for temp_sensor in self.wmi_connection.Win32_TemperatureProbe():
                    if temp_sensor.CurrentReading:
                        cpu_info["temperature_celsius"] = (temp_sensor.CurrentReading - 2732) / 10
                        break
        except Exception as e:
            self.logger.debug(f"No se pudo obtener temperatura del CPU: {e}")
            
        return cpu_info
    
    def scan_operating_system(self) -> Dict[str, Any]:
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
                    
                for system_info in self.wmi_connection.Win32_ComputerSystem():
                    os_info.update({
                        "manufacturer": system_info.Manufacturer,
                        "model": system_info.Model,
                        "total_physical_memory_gb": round(int(system_info.TotalPhysicalMemory) / (1024**3), 2) if system_info.TotalPhysicalMemory else None
                    })
                    
                if self.include_sensitive:
                    try:
                        for os_product in self.wmi_connection.Win32_OperatingSystem():
                            os_info["serial_number"] = os_product.SerialNumber
                            
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
    
    def scan_system_updates(self) -> Dict[str, Any]:
        """Escanea actualizaciones pendientes del sistema"""
        updates_info = {
            "pending_updates": [],
            "total_pending": 0,
            "last_check": None,
            "automatic_updates_enabled": False,
            "reboot_required": False
        }
        
        try:
            result = subprocess.run([
                "powershell", "-Command", 
                "Get-ChildItem 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\WindowsUpdate\\Auto Update\\RebootRequired' -ErrorAction SilentlyContinue"
            ], capture_output=True, text=True, timeout=15)
            
            updates_info["reboot_required"] = result.returncode == 0 and result.stdout.strip()
            
            result = subprocess.run([
                "powershell", "-Command", 
                "(New-Object -ComObject Microsoft.Update.AutoUpdate).Settings.NotificationLevel"
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                level = result.stdout.strip()
                updates_info["automatic_updates_enabled"] = level not in ["1", "Disabled"]
            
            powershell_script = '''
            $Session = New-Object -ComObject Microsoft.Update.Session
            $Searcher = $Session.CreateUpdateSearcher()
            $Searcher.Online = $false
            try {
                $SearchResult = $Searcher.Search("IsInstalled=0")
                $Updates = $SearchResult.Updates
                foreach ($Update in $Updates) {
                    $UpdateInfo = @{
                        Title = $Update.Title
                        Description = $Update.Description
                        Size = $Update.MaxDownloadSize
                        IsDownloaded = $Update.IsDownloaded
                        Severity = $Update.MsrcSeverity
                    }
                    $UpdateInfo | ConvertTo-Json -Compress
                }
            } catch {
                Write-Output "Error: $($_.Exception.Message)"
            }
            '''
            
            result = subprocess.run([
                "powershell", "-Command", powershell_script
            ], capture_output=True, text=True, timeout=45)
            
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip() and not line.startswith("Error:"):
                        try:
                            update_data = json.loads(line)
                            updates_info["pending_updates"].append(update_data)
                        except json.JSONDecodeError:
                            continue
                            
            updates_info["total_pending"] = len(updates_info["pending_updates"])
            
        except Exception as e:
            self.logger.error(f"Error escaneando actualizaciones: {e}")
            updates_info["error"] = str(e)
            
        return updates_info
    
    def scan_driver_updates(self) -> Dict[str, Any]:
        driver_info = {
            "outdated_drivers": [],
            "total_drivers": 0,
            "drivers_needing_update": 0
        }
        
        try:
            if self.wmi_connection:
                for driver in self.wmi_connection.Win32_PnPSignedDriver():
                    if driver.DeviceName and driver.DriverVersion:
                        driver_data = {
                            "device_name": driver.DeviceName,
                            "driver_version": driver.DriverVersion,
                            "driver_date": driver.DriverDate,
                            "manufacturer": driver.Manufacturer,
                            "is_signed": driver.IsSigned,
                            "hardware_id": driver.HardwareID
                        }
                        
                        try:
                            if driver.DriverDate:
                                driver_year = int(driver.DriverDate[:4])
                                current_year = datetime.now().year
                                if current_year - driver_year > 2:
                                    driver_data["potentially_outdated"] = True
                                    driver_info["outdated_drivers"].append(driver_data)
                        except (ValueError, TypeError):
                            pass
                        
                        driver_info["total_drivers"] += 1
                        
            driver_info["drivers_needing_update"] = len(driver_info["outdated_drivers"])
            
            driver_info["outdated_drivers"] = driver_info["outdated_drivers"][:20]
            
        except Exception as e:
            self.logger.error(f"Error escaneando drivers: {e}")
            driver_info["error"] = str(e)
            
        return driver_info
    
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
                "operating_system": self.scan_operating_system(),
                "updates": {
                    "system_updates": self.scan_system_updates(),
                    "driver_updates": self.scan_driver_updates()
                }
            },
            "scan_settings": {
                "include_sensitive": self.include_sensitive,
                "scanner_version": "1.1.0"
            }
        }
        
        self.logger.info(f"Escaneo completo finalizado. ID: {scan_data['identifiers']['scan_id']}")
        return scan_data