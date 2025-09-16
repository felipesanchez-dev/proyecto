import subprocess
import platform
import logging
from typing import Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.text import Text
from modules.logging_setup import SecurityLogger
from config.settings import ACTIVATION_COMMANDS

class ActivationModule:
    
    def __init__(self, console: Console = None):
        self.console = console or Console()
        self.logger = logging.getLogger('sistema_scanner.activation')
        self.security_logger = SecurityLogger()
        
        self.windows_version = self.detect_windows_version()
        
    def detect_windows_version(self) -> str:
       
        try:
            version = platform.version()
            release = platform.release()
            
            if "6.1" in version or release == "7":
                return "windows_7_legacy"
            
            elif any(x in release for x in ["8", "10", "11"]) or "10.0" in version:
                return "windows_8_10_11"
            
            else:
                return "windows_8_10_11"
                
        except Exception as e:
            self.logger.warning(f"Error detectando versión de Windows: {e}")
            return "windows_8_10_11"
    
    def show_activation_menu(self):
        """Muestra el menú de activación con advertencias"""
        
        warning_text = Text()
        warning_text.append("⚠️  ADVERTENCIA CRÍTICA  ⚠️\n\n", style="bold red")
        warning_text.append("Esta función ejecutará comandos de activación de terceros.\n", style="yellow")
        warning_text.append("• No nos hacemos responsables de ningún daño al sistema\n", style="white")
        warning_text.append("• Use bajo su propio riesgo\n", style="white")
        warning_text.append("• Asegúrese de tener respaldos del sistema\n", style="white")
        warning_text.append("• Solo para fines educativos y de prueba\n", style="white")
        
        self.console.print(Panel.fit(
            warning_text,
            title="[bold red]⚠️ RIESGO DE SEGURIDAD ⚠️[/bold red]",
            border_style="red"
        ))
        
        system_info = Panel.fit(
            f"[bold white]Sistema Detectado:[/bold white]\n"
            f"• Windows: {platform.release()} ({platform.version()})\n"
            f"• Arquitectura: {platform.architecture()[0]}\n"
            f"• Comando recomendado: {self.windows_version}\n",
            title="[bold blue]Información del Sistema[/bold blue]",
            border_style="blue"
        )
        
        self.console.print(system_info)
        
        menu_text = Text()
        menu_text.append("OPCIONES DISPONIBLES:\n\n", style="bold white")
        menu_text.append("1. ", style="bright_green")
        menu_text.append("Activación Windows (Automática)\n", style="white")
        menu_text.append("2. ", style="bright_yellow")
        menu_text.append("Activación Windows (Manual - Ver comandos)\n", style="white")
        menu_text.append("3. ", style="bright_blue")
        menu_text.append("Información de licencias actuales\n", style="white")
        menu_text.append("4. ", style="bright_red")
        menu_text.append("Volver al menú principal\n", style="white")
        
        menu_panel = Panel.fit(
            menu_text,
            title="[bold cyan]Menú de Activación[/bold cyan]",
            border_style="cyan"
        )
        
        self.console.print(menu_panel)
        
        while True:
            choice = Prompt.ask(
                "[bright_white]Seleccione una opción",
                choices=["1", "2", "3", "4"],
                default="4"
            )
            
            if choice == "1":
                self.perform_automatic_activation()
                break
            elif choice == "2":
                self.show_manual_activation()
                break
            elif choice == "3":
                self.show_license_info()
                break
            elif choice == "4":
                self.console.print("[green]Volviendo al menú principal...[/green]")
                break
    
    def perform_automatic_activation(self):
        """Ejecuta la activación automática con confirmaciones múltiples"""
        
        self.console.print(Panel.fit(
            "[bold red]CONFIRMACIÓN DE RIESGO[/bold red]\n\n"
            "Está a punto de ejecutar un script de activación que:\n"
            "• Descargará código desde Internet\n"
            "• Modificará configuraciones del sistema\n"
            "• Podría afectar la estabilidad del Windows\n"
            "• Podría ser detectado por antivirus\n\n"
            "[yellow]¿Comprende completamente los riesgos?[/yellow]",
            border_style="red"
        ))
        
        risk_understood = Confirm.ask(
            "[red]¿Acepta TODOS los riesgos mencionados?[/red]",
            default=False
        )
        
        if not risk_understood:
            self.console.print("[green]✓ Operación cancelada por seguridad[/green]")
            self.security_logger.log_activation_attempt("Windows", False)
            return
        
        command = ACTIVATION_COMMANDS[self.windows_version]
        
        command_panel = Panel.fit(
            f"[bold white]COMANDO A EJECUTAR:[/bold white]\n\n"
            f"[cyan]{command}[/cyan]\n\n"
            f"[yellow]Este comando se ejecutará en PowerShell como administrador[/yellow]",
            title="[bold blue]Confirmación de Comando[/bold blue]",
            border_style="blue"
        )
        
        self.console.print(command_panel)
        
        execute_command = Confirm.ask(
            "[yellow]¿Proceder con la ejecución del comando?[/yellow]",
            default=False
        )
        
        if not execute_command:
            self.console.print("[green]✓ Ejecución cancelada[/green]")
            self.security_logger.log_activation_attempt("Windows", False)
            return
        
        final_confirm = Confirm.ask(
            "[bold red]ÚLTIMA CONFIRMACIÓN: ¿Ejecutar script de activación AHORA?[/bold red]",
            default=False
        )
        
        if not final_confirm:
            self.console.print("[green]✓ Operación cancelada en confirmación final[/green]")
            self.security_logger.log_activation_attempt("Windows", False)
            return
        
        self.security_logger.log_activation_attempt("Windows", True)
        self.security_logger.log_external_command(command, True)
        
        try:
            self.console.print("[bold yellow]🔄 Ejecutando comando de activación...[/bold yellow]")
            
            powershell_cmd = [
                "powershell", 
                "-ExecutionPolicy", "Bypass",
                "-WindowStyle", "Normal",
                "-Command", command
            ]
            
            self.logger.info(f"Ejecutando comando de activación: {self.windows_version}")
            
            process = subprocess.Popen(
                powershell_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE if platform.system() == "Windows" else 0
            )
            
            self.console.print("[cyan]📝 Comando enviado a PowerShell. Verifique la ventana de PowerShell...[/cyan]")
            
            stdout, stderr = process.communicate(timeout=300)
            
            if process.returncode == 0:
                self.console.print("[bold green]✅ Comando ejecutado exitosamente[/bold green]")
                self.logger.info("Activación completada exitosamente")
                
                if stdout:
                    self.console.print(Panel.fit(
                        stdout,
                        title="[green]Salida del Comando[/green]",
                        border_style="green"
                    ))
            else:
                self.console.print(f"[bold red]❌ Error en la ejecución (código: {process.returncode})[/bold red]")
                self.logger.error(f"Error en activación: {stderr}")
                
                if stderr:
                    self.console.print(Panel.fit(
                        stderr,
                        title="[red]Errores del Comando[/red]",
                        border_style="red"
                    ))
        
        except subprocess.TimeoutExpired:
            self.console.print("[red]⏱️ Timeout: El comando tardó demasiado en ejecutarse[/red]")
            self.logger.error("Timeout en comando de activación")
            process.kill()
            
        except Exception as e:
            self.console.print(f"[bold red]❌ Error ejecutando comando: {e}[/bold red]")
            self.logger.error(f"Error en activación: {e}")
            self.security_logger.log_external_command(command, False)
        
        self.console.input("\n[dim]Presione Enter para continuar...[/dim]")
    
    def show_manual_activation(self):
        """Muestra los comandos para activación manual"""
        
        commands_text = Text()
        commands_text.append("COMANDOS DE ACTIVACIÓN MANUAL\n\n", style="bold white")
        
        commands_text.append("Para Windows 8, 10, 11:\n", style="bold green")
        commands_text.append(f"{ACTIVATION_COMMANDS['windows_8_10_11']}\n\n", style="cyan")
        
        commands_text.append("Para Windows 7 y anteriores:\n", style="bold yellow")
        commands_text.append(f"{ACTIVATION_COMMANDS['windows_7_legacy']}\n\n", style="cyan")
        
        commands_text.append("INSTRUCCIONES:\n", style="bold blue")
        commands_text.append("1. Abra PowerShell como Administrador\n", style="white")
        commands_text.append("2. Copie y pegue el comando correspondiente\n", style="white")
        commands_text.append("3. Presione Enter para ejecutar\n", style="white")
        commands_text.append("4. Siga las instrucciones en pantalla\n", style="white")
        
        self.console.print(Panel.fit(
            commands_text,
            title="[bold cyan]Comandos Manuales de Activación[/bold cyan]",
            border_style="cyan"
        ))
        
        self.security_logger.log_activation_attempt("Windows_Manual", True)
        self.console.input("\n[dim]Presione Enter para continuar...[/dim]")
    
    def show_license_info(self):
        """Muestra información de las licencias actuales del sistema"""
        
        self.console.print("[cyan]🔍 Obteniendo información de licencias...[/cyan]")
        
        try:
            windows_info = self.get_windows_activation_info()
            
            office_info = self.get_office_activation_info()
            
            if windows_info:
                self.console.print(Panel.fit(
                    windows_info,
                    title="[bold blue]Estado de Windows[/bold blue]",
                    border_style="blue"
                ))
            
            if office_info:
                self.console.print(Panel.fit(
                    office_info,
                    title="[bold green]Estado de Office[/bold green]",
                    border_style="green"
                ))
        
        except Exception as e:
            self.console.print(f"[red]Error obteniendo información de licencias: {e}[/red]")
            self.logger.error(f"Error en información de licencias: {e}")
        
        self.console.input("\n[dim]Presione Enter para continuar...[/dim]")
    
    def get_windows_activation_info(self) -> Optional[str]:
        """Obtiene información de activación de Windows"""
        try:
            result = subprocess.run([
                "slmgr", "/xpr"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return f"Estado de Activación:\n{result.stdout}"
            else:
                return "No se pudo obtener información de activación de Windows"
                
        except Exception as e:
            self.logger.warning(f"Error obteniendo info Windows: {e}")
            return None
    
    def get_office_activation_info(self) -> Optional[str]:
        """Obtiene información de activación de Office"""
        try:
            office_paths = [
                "C:\\\\Program Files\\\\Microsoft Office\\\\Office16\\\\ospp.vbs",
                "C:\\\\Program Files (x86)\\\\Microsoft Office\\\\Office16\\\\ospp.vbs",
                "C:\\\\Program Files\\\\Microsoft Office\\\\Office15\\\\ospp.vbs",
                "C:\\\\Program Files (x86)\\\\Microsoft Office\\\\Office15\\\\ospp.vbs"
            ]
            
            for path in office_paths:
                try:
                    result = subprocess.run([
                        "cscript", path, "/dstatus"
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0 and "LICENSE STATUS" in result.stdout:
                        return f"Estado de Office:\n{result.stdout[:500]}..."  # Limitar output
                        
                except:
                    continue
            
            return "Office no detectado o no disponible"
            
        except Exception as e:
            self.logger.warning(f"Error obteniendo info Office: {e}")
            return None
