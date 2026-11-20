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

```bash
# 1. Clonar
git clone https://github.com/Bryan1234-ctr/asistencia-aula-2cdd.git
cd asistencia-aula-2cdd

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Abre en el navegador: **http://localhost:8000**

---

## 📱 Flujo de uso (para cumplir < 60 s)

1. Presiona **▶ Iniciar sesión (lista masiva)**  
   → Todos los 26 estudiantes quedan marcados como **A**.
2. Solo cambia a **FI / FJ / AT** a los que faltan o llegaron tarde.
3. Presiona **✓ Cerrar y guardar**.
4. Revisa el resumen y el tiempo total.

---

## 🏗️ Estructura del proyecto

```
asistencia-aula-2cdd/
├── app/
│   ├── main.py          # API + rutas FastAPI
│   ├── database.py      # Modelos SQLAlchemy
│   └── seed.py          # Datos iniciales (26 estudiantes + calendario)
├── templates/
│   ├── index.html       # Pantalla principal de toma de asistencia
│   └── reporte.html     # Historial de sesiones
├── static/              # (archivos estáticos si se necesitan)
├── requirements.txt
└── README.md
```

---

## 📡 API Endpoints

| Método | Ruta                    | Descripción                          |
|--------|-------------------------|--------------------------------------|
| GET    | `/`                     | Pantalla de toma de asistencia       |
| GET    | `/reporte`              | Historial de sesiones                |
| POST   | `/api/iniciar-sesion`   | Inicia sesión del día (lista masiva) |
| POST   | `/api/marcar`           | Cambia estado de un estudiante       |
| POST   | `/api/cerrar-sesion`    | Cierra y valida el registro del día  |
| GET    | `/api/estudiantes`      | Lista de los 26 estudiantes          |
| GET    | `/api/sesion-hoy`       | Estado de la sesión actual           |
| GET    | `/api/resumen/{fecha}`  | Resumen de una fecha (YYYY-MM-DD)   |

---

## 📋 Datos precargados

- **26 estudiantes** del Curso 2 CDD "A"
- Calendario del **1er trimestre** (01/09/2026 – 01/12/2026)
- Feriados de Ecuador marcados
- Tolerancia de atraso: **15 minutos**

---

## 🛠️ Stack

- **Backend:** FastAPI + SQLAlchemy + SQLite
- **Frontend:** HTML + CSS + JavaScript (vanilla)
- **Base de datos:** SQLite (archivo `asistencia.db`)

---

## 📄 Licencia

Proyecto educativo — Curso 2 CDD "A" | Docente Marcelo Fonseca  
2026-2027
