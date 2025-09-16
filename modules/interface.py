"""
Interfaz de consola avanzada usando Rich
Menú principal con colores y confirmaciones
"""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt, Confirm
from rich.layout import Layout
from rich.live import Live
import time
import logging
from typing import Optional, Dict, Any
from modules.scanner import SystemScanner
from modules.security_scanner import SecurityScanner
from modules.database import MongoDBClient
from modules.utils import DataManager
from modules.logging_setup import OperationLogger, SecurityLogger
from config.settings import SENSITIVE_DATA_WARNING

class ConsoleInterface:
    """Interfaz de consola principal con Rich"""
    
    def __init__(self):
        self.console = Console()
        self.logger = logging.getLogger('sistema_scanner.interface')
        self.security_logger = SecurityLogger()
        
    def show_banner(self):
        """Muestra el banner principal del sistema"""
        banner_text = Text()
        banner_text.append("╔══════════════════════════════════════════════════════════════════════╗\n", style="bright_cyan")
        banner_text.append("║                    SISTEMA SCANNER WINDOWS                          ║\n", style="bright_cyan")
        banner_text.append("║                 Mantenimiento Automatizado v1.0                    ║\n", style="bright_cyan")
        banner_text.append("║              Escaneo de Hardware y Software del Sistema            ║\n", style="bright_cyan")
        banner_text.append("╚══════════════════════════════════════════════════════════════════════╝", style="bright_cyan")
        
        self.console.print(banner_text)
        self.console.print()
    
    def show_main_menu(self) -> str:
        """
        Muestra el menú principal y captura la selección del usuario
        Returns:
            Opción seleccionada por el usuario
        """
        menu_panel = Panel.fit(
            "[bold bright_white]MENÚ PRINCIPAL[/bold bright_white]\n\n"
            "[bright_green]1.[/bright_green] [white]Escaneo Profundo del Sistema y Subida a MongoDB[/white]\n"
            "[bright_yellow]2.[/bright_yellow] [white]Activación de Windows/Office[/white] [red]⚠️[/red]\n"
            "[bright_red]3.[/bright_red] [white]Salir del Sistema[/white]\n\n"
            "[dim]Seleccione una opción (1-3):[/dim]",
            title="[bold blue]Sistema Scanner[/bold blue]",
            border_style="bright_blue"
        )
        
        self.console.print(menu_panel)
        
        while True:
            choice = Prompt.ask("[bright_white]Opción", choices=["1", "2", "3"], default="1")
            return choice
    
    def show_scan_options(self) -> Dict[str, bool]:
        """
        Muestra opciones de escaneo y captura configuración
        Returns:
            Diccionario con opciones de escaneo
        """
        self.console.print(Panel.fit(
            "[bold yellow]CONFIGURACIÓN DEL ESCANEO[/bold yellow]\n\n"
            "El sistema escaneará automáticamente:\n"
            "• Hardware (CPU, RAM, discos, GPU)\n"
            "• Sistema operativo y configuración\n"
            "• Estado de seguridad y firewall\n"
            "• Puertos abiertos y conexiones\n"
            "• Software instalado y actualizaciones\n",
            title="[bold green]Configuración[/bold green]",
            border_style="green"
        ))
        
        # Advertencia sobre datos sensibles
        self.console.print(Panel.fit(
            f"[red]{SENSITIVE_DATA_WARNING}[/red]\n\n"
            "Los datos sensibles incluyen:\n"
            "• Clave de producto de Windows\n"
            "• Números de serie del hardware\n"
            "• Información detallada de red\n",
            title="[bold red]⚠️ Advertencia de Seguridad[/bold red]",
            border_style="red"
        ))
        
        include_sensitive = Confirm.ask("[yellow]¿Incluir datos sensibles en el escaneo?[/yellow]", default=False)
        
        if include_sensitive:
            self.security_logger.log_sensitive_data_access("system_scan", True)
            self.console.print("[yellow]⚠️ Se incluirán datos sensibles en el escaneo[/yellow]\n")
        else:
            self.security_logger.log_sensitive_data_access("system_scan", False)
            self.console.print("[green]✓ Los datos sensibles serán excluidos[/green]\n")
        
        return {
            "include_sensitive": include_sensitive,
            "save_local": True,  # Siempre guardar localmente
            "upload_mongodb": Confirm.ask("[cyan]¿Subir resultado a MongoDB?[/cyan]", default=True)
        }
    
    def perform_system_scan(self, options: Dict[str, bool]) -> Optional[Dict[str, Any]]:
        """
        Realiza el escaneo completo del sistema con interfaz visual
        Args:
            options: Opciones de escaneo
        Returns:
            Datos del escaneo o None si falla
        """
        operation_logger = OperationLogger("system_scan")
        operation_id = operation_logger.start_operation()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console
        ) as progress:
            
            # Inicializar escáneres
            operation_logger.log_step("Inicializando escáneres")
            scanner = SystemScanner(include_sensitive=options["include_sensitive"])
            security_scanner = SecurityScanner()
            data_manager = DataManager()
            
            # Definir tareas de progreso
            hardware_task = progress.add_task("[green]Escaneando hardware...", total=100)
            security_task = progress.add_task("[yellow]Escaneando seguridad...", total=100)
            saving_task = progress.add_task("[blue]Guardando datos...", total=100)
            
            try:
                # Escaneo de hardware
                operation_logger.log_progress("Iniciando escaneo de hardware", 10)
                progress.update(hardware_task, advance=20)
                
                # Escanear componentes individuales
                progress.update(hardware_task, description="[green]Discos y particiones...")
                disks = scanner.scan_disks()
                progress.update(hardware_task, advance=15)
                
                progress.update(hardware_task, description="[green]Tarjetas gráficas...")
                gpu = scanner.scan_gpu()
                progress.update(hardware_task, advance=15)
                
                progress.update(hardware_task, description="[green]Memoria RAM...")
                memory = scanner.scan_memory()
                progress.update(hardware_task, advance=15)
                
                progress.update(hardware_task, description="[green]Procesador...")
                cpu = scanner.scan_cpu()
                progress.update(hardware_task, advance=15)
                
                progress.update(hardware_task, description="[green]Sistema operativo...")
                os_info = scanner.scan_operating_system()
                progress.update(hardware_task, advance=10)
                
                progress.update(hardware_task, description="[green]Actualizaciones del sistema...")
                system_updates = scanner.scan_system_updates()
                progress.update(hardware_task, advance=5)
                
                progress.update(hardware_task, description="[green]Drivers del sistema...")
                driver_updates = scanner.scan_driver_updates()
                progress.update(hardware_task, advance=5)
                
                # Escaneo de seguridad
                operation_logger.log_progress("Iniciando escaneo de seguridad", 50)
                progress.update(security_task, advance=20)
                
                progress.update(security_task, description="[yellow]Estado del firewall...")
                firewall = security_scanner.scan_firewall_status()
                progress.update(security_task, advance=20)
                
                progress.update(security_task, description="[yellow]Puertos críticos...")
                ports = security_scanner.scan_open_ports()  # Ahora solo devuelve resumen y críticos
                progress.update(security_task, advance=20)
                
                progress.update(security_task, description="[yellow]Hotfixes instalados...")
                hotfixes = security_scanner.scan_hotfixes()
                progress.update(security_task, advance=20)
                
                progress.update(security_task, description="[yellow]Software instalado...")
                software = security_scanner.scan_installed_software()
                progress.update(security_task, advance=20)
                
                # Compilar datos
                operation_logger.log_progress("Compilando datos del escaneo", 80)
                identifiers = data_manager.generate_scan_identifiers()
                
                scan_data = {
                    "identifiers": identifiers,
                    "system_info": {
                        "hardware": {
                            "disks": disks,
                            "gpu": gpu,
                            "memory": memory,
                            "cpu": cpu  # Ahora incluye núcleos, hilos, hyperthreading
                        },
                        "operating_system": os_info,
                        "updates": {
                            "system_updates": system_updates,
                            "driver_updates": driver_updates
                        },
                        "security": {
                            "firewall": firewall,
                            "ports_summary": ports,  # Ahora es un diccionario con resumen
                            "hotfixes": hotfixes,
                            "installed_software_summary": {
                                "total_count": len(software),
                                "sample": software[:10]
                            }
                        }
                    },
                    "scan_settings": {
                        "include_sensitive": options["include_sensitive"],
                        "scanner_version": "1.1.0",  # Actualizada por mejoras en hardware y puertos
                        "operation_id": operation_id
                    }
                }
                
                # Guardar localmente
                progress.update(saving_task, advance=50, description="[blue]Guardando localmente...")
                local_file = data_manager.save_scan_locally(scan_data)
                operation_logger.log_step("Guardado local", local_file)
                
                # Subir a MongoDB si está habilitado
                if options["upload_mongodb"]:
                    progress.update(saving_task, description="[blue]Subiendo a MongoDB...")
                    try:
                        with MongoDBClient() as db_client:
                            document_id = db_client.insert_scan_data(scan_data)
                            if document_id:
                                operation_logger.log_step("Subida MongoDB", f"ID: {document_id}")
                                self.security_logger.log_database_operation("INSERT", True, document_id)
                            else:
                                operation_logger.log_error("Fallo subida a MongoDB")
                                self.security_logger.log_database_operation("INSERT", False, "Error desconocido")
                    except Exception as e:
                        operation_logger.log_error("Error MongoDB", e)
                        self.security_logger.log_database_operation("INSERT", False, str(e))
                
                progress.update(saving_task, advance=50)
                
                operation_logger.end_operation(True, f"Escaneo completado - ID: {identifiers['scan_id']}")
                return scan_data
                
            except Exception as e:
                operation_logger.log_error("Error durante escaneo", e)
                operation_logger.end_operation(False, f"Error: {e}")
                return None
    
    def show_scan_results(self, scan_data: Dict[str, Any]):
        """
        Muestra los resultados del escaneo de forma visual
        Args:
            scan_data: Datos del escaneo a mostrar
        """
        if not scan_data:
            self.console.print("[red]❌ No hay datos de escaneo para mostrar[/red]")
            return
        
        identifiers = scan_data.get("identifiers", {})
        system_info = scan_data.get("system_info", {})
        hardware = system_info.get("hardware", {})
        os_info = system_info.get("operating_system", {})
        
        # Panel principal con información del escaneo
        info_table = Table(show_header=False, box=None)
        info_table.add_column("Campo", style="bright_cyan", width=20)
        info_table.add_column("Valor", style="white")
        
        info_table.add_row("ID de Escaneo:", identifiers.get("scan_id", "N/A")[:16] + "...")
        info_table.add_row("PIN de Acceso:", identifiers.get("access_pin", "N/A"))
        info_table.add_row("Timestamp:", identifiers.get("timestamp", "N/A"))
        info_table.add_row("Hostname:", os_info.get("hostname", "N/A"))
        
        self.console.print(Panel.fit(
            info_table,
            title="[bold green]✓ Escaneo Completado[/bold green]",
            border_style="green"
        ))
        
        # Tabla de hardware
        hw_table = Table(show_header=True, header_style="bold bright_white")
        hw_table.add_column("Componente", style="cyan", width=15)
        hw_table.add_column("Información", style="white")
        
        # CPU - Información detallada
        cpu_info = hardware.get("cpu", {})
        cpu_cores = cpu_info.get('physical_cores', 'N/A')
        cpu_threads = cpu_info.get('logical_cores', 'N/A')
        cpu_hyperthreading = cpu_info.get('hyperthreading_enabled', False)
        cpu_usage = cpu_info.get('cpu_usage_percent', 'N/A')
        
        cpu_text = f"{cpu_info.get('name', cpu_info.get('processor_name', 'N/A'))}"
        cpu_text += f"\n{cpu_cores} núcleos, {cpu_threads} hilos"
        if cpu_hyperthreading:
            cpu_text += " (HT habilitado)"
        cpu_text += f"\nUso actual: {cpu_usage}%"
        
        hw_table.add_row("CPU", cpu_text)
        
        # RAM
        memory_info = hardware.get("memory", {})
        ram_text = f"{memory_info.get('total_gb', 'N/A')} GB total - {memory_info.get('used_percent', 'N/A')}% usado"
        hw_table.add_row("RAM", ram_text)
        
        # Discos
        disks = hardware.get("disks", [])
        disk_text = f"{len(disks)} discos detectados"
        if disks:
            total_gb = sum(disk.get('total_gb', 0) for disk in disks)
            disk_text += f" - {total_gb:.1f} GB total"
        hw_table.add_row("Discos", disk_text)
        
        # GPU
        gpus = hardware.get("gpu", [])
        gpu_text = f"{len(gpus)} GPU(s) detectadas"
        if gpus:
            gpu_text += f" - {gpus[0].get('name', 'N/A')}"
        hw_table.add_row("GPU", gpu_text)
        
        self.console.print(Panel.fit(
            hw_table,
            title="[bold blue]Hardware Detectado[/bold blue]",
            border_style="blue"
        ))
        
        # Mostrar información de seguridad si está disponible
        security_info = system_info.get("security", {})
        if security_info:
            sec_table = Table(show_header=True, header_style="bold bright_white")
            sec_table.add_column("Aspecto", style="yellow", width=20)
            sec_table.add_column("Estado", style="white")
            
            firewall = security_info.get("firewall", {})
            fw_status = firewall.get("status", "unknown")
            fw_color = "green" if fw_status == "fully_enabled" else "red"
            sec_table.add_row("Firewall", f"[{fw_color}]{fw_status}[/{fw_color}]")
            
            ports_summary = security_info.get("ports_summary", {})
            if isinstance(ports_summary, dict):
                total_ports = ports_summary.get("total_ports", 0)
                critical_ports = ports_summary.get("critical_count", 0)
                sec_table.add_row("Puertos", f"{total_ports} total, {critical_ports} críticos")
            else:
                sec_table.add_row("Puertos", f"{len(ports_summary)} conexiones")
            
            hotfixes = security_info.get("hotfixes", [])
            sec_table.add_row("Actualizaciones", f"{len(hotfixes)} hotfixes instalados")
            
            software_summary = security_info.get("installed_software_summary", {})
            sw_count = software_summary.get("total_count", 0)
            sec_table.add_row("Software Instalado", f"{sw_count} programas detectados")
            
            self.console.print(Panel.fit(
                sec_table,
                title="[bold yellow]Estado de Seguridad[/bold yellow]",
                border_style="yellow"
            ))
        
        # Mostrar información de actualizaciones si está disponible
        updates_info = system_info.get("updates", {})
        if updates_info:
            upd_table = Table(show_header=True, header_style="bold bright_white")
            upd_table.add_column("Tipo", style="cyan", width=20)
            upd_table.add_column("Estado", style="white")
            
            system_updates = updates_info.get("system_updates", {})
            pending_updates = system_updates.get("total_pending", 0)
            reboot_required = system_updates.get("reboot_required", False)
            auto_updates = system_updates.get("automatic_updates_enabled", False)
            
            update_status = f"{pending_updates} pendientes"
            if reboot_required:
                update_status += " [red](Reinicio requerido)[/red]"
            if auto_updates:
                update_status += " [green](Auto habilitado)[/green]"
            upd_table.add_row("Sistema", update_status)
            
            driver_updates = updates_info.get("driver_updates", {})
            outdated_drivers = driver_updates.get("drivers_needing_update", 0)
            total_drivers = driver_updates.get("total_drivers", 0)
            
            driver_status = f"{outdated_drivers} de {total_drivers} obsoletos"
            if outdated_drivers > 0:
                driver_status += " [yellow](Revisar)[/yellow]"
            else:
                driver_status += " [green](OK)[/green]"
            upd_table.add_row("Drivers", driver_status)
            
            self.console.print(Panel.fit(
                upd_table,
                title="[bold magenta]Estado de Actualizaciones[/bold magenta]",
                border_style="magenta"
            ))
        
        # Panel de resumen final
        self.console.print(Panel.fit(
            f"[green]✓ Escaneo completado exitosamente[/green]\n"
            f"[white]Los datos han sido guardados localmente y enviados a MongoDB[/white]\n"
            f"[cyan]Use el PIN [bold]{identifiers.get('access_pin', 'N/A')}[/bold] para acceso rápido[/cyan]",
            title="[bold bright_green]Resumen Final[/bold bright_green]",
            border_style="bright_green"
        ))
    
    def run_main_loop(self):
        """Ejecuta el bucle principal de la interfaz"""
        try:
            self.show_banner()
            
            while True:
                choice = self.show_main_menu()
                
                if choice == "1":
                    # Escaneo del sistema
                    self.console.print("[bright_green]Iniciando escaneo del sistema...[/bright_green]\n")
                    
                    options = self.show_scan_options()
                    scan_data = self.perform_system_scan(options)
                    
                    if scan_data:
                        self.show_scan_results(scan_data)
                        
                        # Preguntar si quiere ver detalles
                        if Confirm.ask("\n[cyan]¿Ver resumen detallado del escaneo?[/cyan]"):
                            data_manager = DataManager()
                            summary = data_manager.format_scan_summary(scan_data)
                            self.console.print(Panel.fit(
                                summary,
                                title="[bold green]Resumen Detallado[/bold green]",
                                border_style="green"
                            ))
                    else:
                        self.console.print("[red]❌ El escaneo falló. Revise los logs para más detalles.[/red]")
                    
                    self.console.input("\n[dim]Presione Enter para continuar...[/dim]")
                
                elif choice == "2":
                    # Activación de Windows/Office
                    from modules.activation import ActivationModule
                    activation = ActivationModule(self.console)
                    activation.show_activation_menu()
                
                elif choice == "3":
                    # Salir
                    self.console.print("[bright_yellow]¡Gracias por usar Sistema Scanner![/bright_yellow]")
                    break
                
                self.console.clear()
                
        except KeyboardInterrupt:
            self.console.print("\n[bright_red]Operación cancelada por el usuario[/bright_red]")
        except Exception as e:
            self.logger.error(f"Error en interfaz principal: {e}")
            self.console.print(f"[red]Error inesperado: {e}[/red]")
        
        self.console.print("[dim]Cerrando sistema...[/dim]")