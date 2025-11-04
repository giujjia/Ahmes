#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de execução AHMES
Automatiza a compilação e execução de programas AHMES
"""

import sys
import subprocess
import os

def main():
    if len(sys.argv) < 2:
        print("Uso: python ahmesexec.py <arquivo_entrada.TXT>")
        sys.exit(1)
    
    arquivo_entrada = sys.argv[1]
    
    # Compila o programa
    print(f"Compilando {arquivo_entrada}...")
    result = subprocess.run([sys.executable, "compAhmesTXT.py", arquivo_entrada])
    
    if result.returncode != 0:
        print("Erro na compilação!")
        sys.exit(1)
    
    # Executa o programa
    print("Executando programa...")
    result = subprocess.run([sys.executable, "exeprogAhmes.py"])
    
    if result.returncode != 0:
        print("Erro na execução!")
        sys.exit(1)

if __name__ == "__main__":
    main()
