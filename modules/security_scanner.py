"""
Extensión del módulo de escaneo para software y configuraciones de seguridad
"""
import subprocess
import json
import logging
import socket
from typing import Dict, List, Any, Optional

class SecurityScanner:
    """Escáner de seguridad y software del sistema"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def scan_firewall_status(self) -> Dict[str, Any]:
        """Escanea el estado del firewall de Windows"""
        firewall_info = {
            "profiles": {},
            "status": "unknown",
            "rules_count": 0
        }
        
        try:
            # Obtener estado del firewall por perfil
            profiles = ["domain", "public", "private"]
            
            for profile in profiles:
                try:
                    result = subprocess.run([
                        "netsh", "advfirewall", "show", profile, "state"
                    ], capture_output=True, text=True, timeout=15)
                    
                    if result.returncode == 0:
                        output = result.stdout
                        if "ON" in output or "Activado" in output:
                            firewall_info["profiles"][profile] = "enabled"
                        elif "OFF" in output or "Desactivado" in output:
                            firewall_info["profiles"][profile] = "disabled"
                        else:
                            firewall_info["profiles"][profile] = "unknown"
                    
                except subprocess.TimeoutExpired:
                    self.logger.warning(f"Timeout al verificar firewall {profile}")
                    firewall_info["profiles"][profile] = "timeout"
                except Exception as e:
                    self.logger.warning(f"Error verificando firewall {profile}: {e}")
                    firewall_info["profiles"][profile] = "error"
            
            # Determinar estado general
            enabled_count = sum(1 for status in firewall_info["profiles"].values() if status == "enabled")
            if enabled_count == len(profiles):
                firewall_info["status"] = "fully_enabled"
            elif enabled_count > 0:
                firewall_info["status"] = "partially_enabled"
            else:
                firewall_info["status"] = "disabled"
            
            # Contar reglas del firewall (aproximado)
            try:
                result = subprocess.run([
                    "netsh", "advfirewall", "firewall", "show", "rule", "name=all"
                ], capture_output=True, text=True, timeout=20)
                
                if result.returncode == 0:
                    # Contar ocurrencias de "Rule Name" o "Nombre de regla"
                    firewall_info["rules_count"] = result.stdout.count("Rule Name:") + result.stdout.count("Nombre de regla:")
                    
            except Exception as e:
                self.logger.warning(f"Error contando reglas de firewall: {e}")
                
        except Exception as e:
            self.logger.error(f"Error escaneando firewall: {e}")
            
        return firewall_info
    
    def scan_open_ports(self) -> List[Dict[str, Any]]:
        """Escanea puertos abiertos y conexiones de escucha"""
        connections = []
        
        try:
            # Usar psutil para obtener conexiones
            import psutil
            
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == psutil.CONN_LISTEN:
                    connection_info = {
                        "protocol": "TCP" if conn.type == socket.SOCK_STREAM else "UDP",
                        "local_address": conn.laddr.ip if conn.laddr else None,
                        "local_port": conn.laddr.port if conn.laddr else None,
                        "status": conn.status,
                        "pid": conn.pid
                    }
                    
                    # Intentar obtener nombre del proceso
                    if conn.pid:
                        try:
                            process = psutil.Process(conn.pid)
                            connection_info["process_name"] = process.name()
                            connection_info["process_exe"] = process.exe()
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            connection_info["process_name"] = "unknown"
                    
                    connections.append(connection_info)
                    
        except Exception as e:
            self.logger.error(f"Error escaneando puertos: {e}")
            
            # Fallback usando netstat
            try:
                result = subprocess.run([
                    "netstat", "-an"
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    lines = result.stdout.split('\\n')
                    for line in lines:
                        if "LISTENING" in line or "ESCUCHANDO" in line:
                            parts = line.split()
                            if len(parts) >= 4:
                                protocol = parts[0]
                                local_addr = parts[1]
                                
                                if ':' in local_addr:
                                    ip, port = local_addr.rsplit(':', 1)
                                    connections.append({
                                        "protocol": protocol,
                                        "local_address": ip,
                                        "local_port": port,
                                        "status": "LISTENING",
                                        "source": "netstat"
                                    })
                                    
            except Exception as e2:
                self.logger.error(f"Error con netstat fallback: {e2}")
                
        return connections
    
    def scan_hotfixes(self) -> List[Dict[str, Any]]:
        """Escanea actualizaciones y hotfixes instalados"""
        hotfixes = []
        
        try:
            # Usar wmic qfe para obtener hotfixes
            result = subprocess.run([
                "wmic", "qfe", "get", "HotFixID,InstalledOn,Description", "/format:csv"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\\n')
                headers = None
                
                for line in lines:
                    if not line.strip():
                        continue
                        
                    parts = [part.strip() for part in line.split(',')]
                    
                    if headers is None:
                        headers = parts
                        continue
                    
                    if len(parts) >= 3 and parts[1]:  # Asegurar que hay datos válidos
                        hotfix_info = {}
                        for i, header in enumerate(headers):
                            if i < len(parts):
                                hotfix_info[header.lower().replace(' ', '_')] = parts[i]
                        
                        if hotfix_info.get('hotfixid'):
                            hotfixes.append(hotfix_info)
                            
        except subprocess.TimeoutExpired:
            self.logger.warning("Timeout al obtener hotfixes")
        except Exception as e:
            self.logger.error(f"Error escaneando hotfixes: {e}")
            
        return hotfixes
    
    def scan_installed_software(self) -> List[Dict[str, Any]]:
        """Escanea software instalado (resumen)"""
        software = []
        
        try:
            # Obtener software instalado desde el registro usando wmic
            result = subprocess.run([
                "wmic", "product", "get", "Name,Version,Vendor", "/format:csv"
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\\n')
                headers = None
                
                for line in lines:
                    if not line.strip():
                        continue
                        
                    parts = [part.strip() for part in line.split(',')]
                    
                    if headers is None:
                        headers = parts
                        continue
                    
                    if len(parts) >= 3 and parts[1]:  # Asegurar que hay datos válidos
                        software_info = {}
                        for i, header in enumerate(headers):
                            if i < len(parts):
                                software_info[header.lower().replace(' ', '_')] = parts[i]
                        
                        if software_info.get('name'):
                            software.append(software_info)
                            
        except subprocess.TimeoutExpired:
            self.logger.warning("Timeout al obtener software instalado")
        except Exception as e:
            self.logger.error(f"Error escaneando software: {e}")
            
        return software[:50]  # Limitar a 50 elementos para evitar sobrecarga
    
    def scan_drivers_status(self) -> List[Dict[str, Any]]:
        """Escanea estado de drivers del sistema"""
        drivers = []
        
        try:
            # Obtener información de drivers usando wmic
            result = subprocess.run([
                "wmic", "systemdriver", "get", "Name,State,Status,PathName", "/format:csv"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\\n')
                headers = None
                
                for line in lines:
                    if not line.strip():
                        continue
                        
                    parts = [part.strip() for part in line.split(',')]
                    
                    if headers is None:
                        headers = parts
                        continue
                    
                    if len(parts) >= 3 and parts[1]:
                        driver_info = {}
                        for i, header in enumerate(headers):
                            if i < len(parts):
                                driver_info[header.lower().replace(' ', '_')] = parts[i]
                        
                        # Solo incluir drivers con estado problemático
                        if driver_info.get('state') != 'Running' or driver_info.get('status') != 'OK':
                            drivers.append(driver_info)
                            
        except subprocess.TimeoutExpired:
            self.logger.warning("Timeout al obtener drivers")
        except Exception as e:
            self.logger.error(f"Error escaneando drivers: {e}")
            
        return drivers
    
    def perform_security_scan(self) -> Dict[str, Any]:
        """Realiza un escaneo completo de seguridad y software"""
        self.logger.info("Iniciando escaneo de seguridad...")
        
        security_data = {
            "firewall": self.scan_firewall_status(),
            "open_ports": self.scan_open_ports(),
            "hotfixes": self.scan_hotfixes(),
            "installed_software_summary": {
                "total_count": 0,
                "sample": []
            },
            "problematic_drivers": self.scan_drivers_status()
        }
        
        # Obtener software instalado
        software_list = self.scan_installed_software()
        security_data["installed_software_summary"]["total_count"] = len(software_list)
        security_data["installed_software_summary"]["sample"] = software_list[:10]  # Muestra solo 10
        
        self.logger.info("Escaneo de seguridad completado")
        return security_data