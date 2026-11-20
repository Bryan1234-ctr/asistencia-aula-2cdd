# 📋 Asistencia Aula — Curso 2 CDD "A"

App de **toma de asistencia en menos de 1 minuto** para el curso **2 CDD "A"**  
**Docente:** Marcelo Fonseca  
**Materia:** Ciencia de Datos / Fundamentos de datos  
**Periodo:** 1er Trimestre 2026-2027  

Basada en la **Matriz de Operacionalización** de requerimientos y lógica de asistencia.

---

## 🎯 Objetivo principal

Registrar la asistencia de los **26 estudiantes** en **menos de 60 segundos** usando el método de **Lista masiva** (todos empiezan como Presentes → solo se cambian los ausentes/atrasados).

### Estados de asistencia
| Código | Significado              |
|--------|--------------------------|
| **A**  | Asistencia               |
| **FJ** | Falta Justificada        |
| **FI** | Falta Injustificada      |
| **AT** | Atraso (≥ 15 minutos)    |

---

## 🚀 Cómo ejecutar

### Opción A — Servidor web (desarrollo)

```bash
git clone https://github.com/Bryan1234-ctr/asistencia-aula-2cdd.git
cd asistencia-aula-2cdd
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Abre: **http://localhost:8000**

### Opción B — Escritorio (un clic)

```bash
python run_desktop.py
```

Se inicia el servidor y se abre el navegador automáticamente.

### Opción C — Instalables (EXE / Linux / Mac / Android)

Ver la guía completa en **[build_packages.md](build_packages.md)**:

| Plataforma | Formato | Método |
|-----------|---------|--------|
| Windows | `.exe` | PyInstaller |
| Linux | binario | PyInstaller |
| macOS | `.app` | PyInstaller |
| Android | PWA (instalar desde Chrome) o APK con Capacitor | PWA ya incluida |

---

## 📱 Flujo de uso (para cumplir < 60 s)

1. Presiona **▶ Iniciar sesión (lista masiva)** → Todos quedan en **A**.
2. Solo cambia a **FI / FJ / AT** a los que faltan o llegaron tarde.
3. Presiona **✓ Cerrar y guardar**.
4. Revisa el resumen y el tiempo total.

---

## 🏗️ Estructura del proyecto

```
asistencia-aula-2cdd/
├── app/
│   ├── main.py
│   ├── database.py
│   └── seed.py
├── templates/
├── static/           # PWA (manifest, icons, service worker)
├── run_desktop.py    # Lanzador de escritorio
├── build_packages.md # Guía EXE / APK / Linux / Mac
├── requirements.txt
└── README.md
```

---

## 📡 API Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Pantalla de toma de asistencia |
| GET | `/reporte` | Historial de sesiones |
| POST | `/api/iniciar-sesion` | Inicia sesión (lista masiva) |
| POST | `/api/marcar` | Cambia estado de un estudiante |
| POST | `/api/cerrar-sesion` | Cierra y valida el día |
| GET | `/api/estudiantes` | Lista de los 26 estudiantes |
| GET | `/api/sesion-hoy` | Estado de la sesión actual |
| GET | `/api/resumen/{fecha}` | Resumen por fecha |

---

## 📋 Datos precargados

- 26 estudiantes del Curso 2 CDD "A"
- Calendario 1er trimestre (01/09/2026 – 01/12/2026)
- Feriados de Ecuador
- Tolerancia de atraso: 15 minutos

---

## 🛠️ Stack

- Backend: FastAPI + SQLAlchemy + SQLite
- Frontend: HTML + CSS + JS (PWA)
- Escritorio: `run_desktop.py` + PyInstaller

---

## 📄 Licencia

Proyecto educativo — Curso 2 CDD "A" | Docente Marcelo Fonseca  
2026-2027
