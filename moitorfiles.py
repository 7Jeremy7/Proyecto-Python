import os
import hashlib
import json
from colorama import Fore, init

# Inicializa colorama
init()

# Calcula el hash SHA-256 de un archivo
def calcular_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Verifica la integridad de los archivos en un directorio
def verificar_integridad(directorio, hash_file):
    # Cargar hashes guardados
    if os.path.exists(hash_file):
        with open(hash_file, "r") as f:
            hashes_guardados = json.load(f)
    else:
        hashes_guardados = {}

    hashes_actuales = {}

    for root, _, files in os.walk(directorio):
        for file in files:
            file_path = os.path.join(root, file)
            hash_actual = calcular_hash(file_path)
            hashes_actuales[file_path] = hash_actual

            # Comparar hash actual con el guardado
            if file_path in hashes_guardados:
                if hash_actual != hashes_guardados[file_path]:
                    print(f"{Fore.RED}Archivo modificado: {file_path}{Fore.RESET}")
            else:
                print(f"{Fore.GREEN}Nuevo archivo detectado: {file_path}{Fore.RESET}")

    # Guardar hashes actuales
    with open(hash_file, "w") as f:
        json.dump(hashes_actuales, f, indent=4)

# Directorio a monitorear y archivo para guardar los hashes
directorio_a_monitorear = "/ruta/al/directorio"
archivo_hashes = "hashes.json"

# Ejecutar verificación de integridad
verificar_integridad(directorio_a_monitorear, archivo_hashes)
