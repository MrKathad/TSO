import subprocess
from concurrent.futures import ThreadPoolExecutor
import os
import time
#Calcular los objetivos del txt
lineas = [linea.strip() for linea in open('objetivos.txt') if linea.strip()]

# Opciones de Nmap y directorios de salida
nmap_options = {
    "ports": "-sV -O",
    "services_ports": "-sV -A -O",
    "vuln": "-A -O -sVC --script auth,brute,default,exploit,fuzzer,intrusive,vuln"
}

# Crear un directorio para los resultados
base_output_dir = 'result'
os.makedirs(base_output_dir, exist_ok=True)

# Función para realizar el escaneo Nmap
def run_nmap_scan(target, option):
    output_dir = os.path.join(base_output_dir, f'{option}')
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, f"nmapScan_{target}.txt")
    command = f"nmap -Pn {nmap_options[option]} {target} -oN {output_filename} 2>/dev/null"
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"\tEl escaneo nmap de {target} con opción '{option}' ha culminado.")

# Leer los objetivos desde un archivo de texto
with open('objetivos.txt', 'r') as file:
    targets = [line.strip() for line in file if line.strip()]

# Usar ThreadPoolExecutor para ejecutar escaneos en paralelo por cada opción
for option in nmap_options.keys():
    print(f"Iniciando escaneo con la opción: {option}")
    with ThreadPoolExecutor(max_workers=len(lineas)) as executor:
        executor.map(lambda target: run_nmap_scan(target, option), targets)
