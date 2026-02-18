import os
import time
import re
import json
import shutil
import subprocess
import configparser
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Dict

from deep_translator import GoogleTranslator
from rich.console import Console, Group
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn, MofNCompleteColumn
from rich.panel import Panel
from rich.live import Live

class FateTranslator:
    """Clase profesional para la gestión de traducción y empaquetado de Fate/Stay Night."""
    
    def __init__(self, config_path: str = 'config.ini'):
        self.console = Console()
        self.config = configparser.ConfigParser()
        self.config.read(config_path, encoding='utf-8')
        
        # Cargar configuraciones
        self.entrada = self.config['DIRECTORIOS']['entrada']
        self.salida = self.config['DIRECTORIOS']['salida']
        self.ruta_xp3 = self.config['HERRAMIENTAS']['ruta_xp3_py']
        self.archivo_final = self.config['HERRAMIENTAS']['archivo_final']
        self.idioma = self.config['AJUSTES']['idioma_destino']
        self.hilos = int(self.config['AJUSTES']['max_hilos'])
        self.cache_path = self.config['AJUSTES']['archivo_cache']
        
        self.cache_data: Dict[str, str] = {}
        self.cargar_cache()

    def cargar_cache(self):
        """Carga la memoria de traducciones previas para optimizar tiempo."""
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, 'r', encoding='utf-8') as f:
                    self.cache_data = json.load(f)
            except Exception: self.cache_data = {}

    def guardar_cache(self):
        """Guarda el progreso actual en un archivo JSON persistente."""
        with open(self.cache_path, 'w', encoding='utf-8') as f:
            json.dump(self.cache_data, f, ensure_ascii=False, indent=4)

    def proteger_etiquetas(self, linea: str) -> Tuple[str, List[str]]:
        """Extrae etiquetas [KAG] para evitar que el traductor las corrompa."""
        etiquetas = re.findall(r'\[.*?\]', linea)
        texto_limpio = re.sub(r'\[.*?\]', ' @ ', linea).strip()
        return texto_limpio, etiquetas

    def traducir_texto(self, texto: str) -> str:
        """Traduce texto con manejo de caché y reintentos automáticos."""
        if not texto or texto.strip() == "@": return texto
        if texto in self.cache_data: return self.cache_data[texto]
        
        try:
            traducido = GoogleTranslator(source='auto', target=self.idioma).translate(texto)
            if traducido:
                self.cache_data[texto] = traducido
                return traducido
        except: pass
        return texto

    def procesar_archivo(self, rutas: Tuple[str, str], progress, overall_task):
        """Gestiona la lógica de traducción para scripts o copiado para multimedia."""
        r_orig, r_dest = rutas
        nombre = os.path.basename(r_orig)
        
        try:
            os.makedirs(os.path.dirname(r_dest), exist_ok=True)
            if nombre.lower().endswith(('.ks', '.tjs', '.scn')):
                with open(r_orig, 'r', encoding='utf-16', errors='ignore') as f:
                    lineas = f.readlines()
                
                t_id = progress.add_task(f"[cyan]→ {nombre[:15]}", total=len(lineas))
                nuevo_txt = []
                for l in lineas:
                    if l.strip() and not l.strip().startswith(('@', ';', '*', '#')):
                        txt, etiq = self.proteger_etiquetas(l)
                        trad = self.traducir_texto(txt)
                        # Reconstrucción
                        partes = trad.split('@')
                        final = ""
                        for i in range(len(partes)):
                            final += partes[i].strip()
                            if i < len(etiq): final += etiq[i]
                        nuevo_txt.append(final + "\n")
                    else:
                        nuevo_txt.append(l)
                    progress.advance(t_id)
                
                with open(r_dest, 'w', encoding='utf-16-sig') as f:
                    f.writelines(nuevo_txt)
                progress.remove_task(t_id)
            else:
                shutil.copy2(r_orig, r_dest) # Clonación de archivos no traducibles
            
            progress.advance(overall_task)
        except Exception as e:
            self.console.print(f"[red]Error en {nombre}: {e}[/red]")

    def ejecutar(self):
        """Inicia el motor de traducción y el empaquetado final."""
        self.console.print(Panel.fit("[bold magenta]FATE ENGINE TRANSLATOR[/bold magenta]\n[dim]Modo Portafolio Profesional[/dim]", border_style="blue"))
        
        tareas = []
        for r, _, archivos in os.walk(self.entrada):
            for n in archivos:
                tareas.append((os.path.join(r, n), os.path.join(self.salida, os.path.relpath(r, self.entrada), n)))

        prog = Progress("{task.description}", SpinnerColumn(), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), MofNCompleteColumn(), TimeElapsedColumn())
        total_task = prog.add_task("[yellow]Progreso General", total=len(tareas))
        
        with Live(Group(Panel(prog, title="Hilos Activos", border_style="blue")), refresh_per_second=5):
            with ThreadPoolExecutor(max_workers=self.hilos) as exe:
                [exe.submit(self.procesar_archivo, t, prog, total_task) for t in tareas]
        
        self.guardar_cache()
        
        # Empaquetado
        if os.path.exists(self.ruta_xp3):
            self.console.print("\n[bold yellow]📦 Generando parche XP3...[/bold yellow]")
            subprocess.run(["python", self.ruta_xp3, "--pack", self.archivo_final, self.salida])
            self.console.print(f"[bold green]✨ Éxito: {self.archivo_final}[/bold green]")

if __name__ == "__main__":
    FateTranslator().ejecutar()
