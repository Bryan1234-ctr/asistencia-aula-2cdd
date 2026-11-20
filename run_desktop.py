#!/usr/bin/env python3
"""
Lanzador de escritorio para Asistencia 2 CDD "A"
Abre el servidor local y el navegador automáticamente.
Compatible con Windows, Linux y macOS.
"""
import sys
import os
import time
import threading
import webbrowser
import socket
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.chdir(BASE_DIR)


def find_free_port(start=8000, end=8100):
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return 8000


def open_browser(url, delay=1.5):
    time.sleep(delay)
    webbrowser.open(url)


def main():
    port = find_free_port()
    url = f"http://127.0.0.1:{port}"

    print("=" * 50)
    print("  ASISTENCIA 2 CDD \"A\"")
    print("  Docente: Marcelo Fonseca")
    print("  Objetivo: < 60 segundos")
    print("=" * 50)
    print(f"\n  Servidor iniciando en: {url}")
    print("  Presiona Ctrl+C para cerrar.\n")

    threading.Thread(target=open_browser, args=(url,), daemon=True).start()

    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=port,
        log_level="info",
        access_log=False,
    )


if __name__ == "__main__":
    main()
