"""
App de Asistencia en Aula - Curso 2 CDD "A"
Objetivo: Registrar los 26 estudiantes en menos de 60 segundos
Docente: Marcelo Fonseca
"""
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import List, Optional
import time

from .database import get_db, init_db, Estudiante, SesionAsistencia, RegistroAsistencia, CalendarioDia
from .seed import run_seed

app = FastAPI(
    title="Asistencia Aula 2 CDD A",
    description="Toma de asistencia en menos de 1 minuto - Curso 2 CDD \"A\"",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Inicializar DB al arrancar
@app.on_event("startup")
def startup():
    run_seed()


# ==================== PÁGINAS HTML ====================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    estudiantes = db.query(Estudiante).order_by(Estudiante.numero_lista).all()
    hoy = date.today()
    sesion_hoy = db.query(SesionAsistencia).filter(SesionAsistencia.fecha == hoy).first()
    
    registros_map = {}
    if sesion_hoy:
        for r in sesion_hoy.registros:
            registros_map[r.estudiante_id] = r

    return templates.TemplateResponse("index.html", {
        "request": request,
        "estudiantes": estudiantes,
        "sesion": sesion_hoy,
        "registros_map": registros_map,
        "hoy": hoy.strftime("%d/%m/%Y"),
        "total": len(estudiantes)
    })


@app.get("/reporte", response_class=HTMLResponse)
async def reporte(request: Request, db: Session = Depends(get_db)):
    sesiones = db.query(SesionAsistencia).order_by(SesionAsistencia.fecha.desc()).limit(30).all()
    return templates.TemplateResponse("reporte.html", {
        "request": request,
        "sesiones": sesiones
    })


# ==================== API ENDPOINTS ====================

@app.post("/api/iniciar-sesion")
async def iniciar_sesion(db: Session = Depends(get_db)):
    """Inicia una nueva sesión de asistencia para hoy (método lista masiva)"""
    hoy = date.today()
    
    existente = db.query(SesionAsistencia).filter(SesionAsistencia.fecha == hoy).first()
    if existente and existente.estado == "Cerrada":
        raise HTTPException(status_code=400, detail="Ya existe una sesión cerrada para hoy")
    
    if existente:
        return {"ok": True, "sesion_id": existente.id, "mensaje": "Sesión ya estaba abierta"}

    sesion = SesionAsistencia(
        fecha=hoy,
        hora_inicio=datetime.now().strftime("%H:%M"),
        mecanismo="Lista masiva",
        estado="Activa",
        total_esperados=26
    )
    db.add(sesion)
    db.commit()
    db.refresh(sesion)

    estudiantes = db.query(Estudiante).filter(Estudiante.activo == True).all()
    for est in estudiantes:
        reg = RegistroAsistencia(
            sesion_id=sesion.id,
            estudiante_id=est.id,
            estado="A",
            marcado_por="Sistema (lista masiva)"
        )
        db.add(reg)
    
    db.commit()
    return {
        "ok": True,
        "sesion_id": sesion.id,
        "mensaje": f"Sesión iniciada. {len(estudiantes)} estudiantes marcados como Presentes (A). Solo modifica los ausentes/atrasados.",
        "tiempo_inicio": time.time()
    }


@app.post("/api/marcar")
async def marcar_estudiante(
    estudiante_id: int = Form(...),
    estado: str = Form(...),
    hora_llegada: Optional[str] = Form(None),
    observacion: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Cambia el estado de un estudiante (A / FJ / FI / AT)"""
    if estado not in ["A", "FJ", "FI", "AT"]:
        raise HTTPException(status_code=400, detail="Estado inválido. Use: A, FJ, FI, AT")

    hoy = date.today()
    sesion = db.query(SesionAsistencia).filter(
        SesionAsistencia.fecha == hoy,
        SesionAsistencia.estado == "Activa"
    ).first()
    
    if not sesion:
        raise HTTPException(status_code=400, detail="No hay sesión activa. Inicie la sesión primero.")

    registro = db.query(RegistroAsistencia).filter(
        RegistroAsistencia.sesion_id == sesion.id,
        RegistroAsistencia.estudiante_id == estudiante_id
    ).first()

    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    if estado == "AT" and not hora_llegada:
        hora_llegada = datetime.now().strftime("%H:%M")

    registro.estado = estado
    registro.hora_llegada = hora_llegada if estado == "AT" else None
    registro.observacion = observacion
    registro.marcado_por = "Docente"
    registro.timestamp = datetime.utcnow()

    db.commit()
    return {"ok": True, "estudiante_id": estudiante_id, "nuevo_estado": estado}


@app.post("/api/cerrar-sesion")
async def cerrar_sesion(db: Session = Depends(get_db)):
    """Cierra la sesión del día y calcula el resumen (Módulo 5)"""
    hoy = date.today()
    sesion = db.query(SesionAsistencia).filter(
        SesionAsistencia.fecha == hoy,
        SesionAsistencia.estado == "Activa"
    ).first()

    if not sesion:
        raise HTTPException(status_code=400, detail="No hay sesión activa para cerrar")

    registros = db.query(RegistroAsistencia).filter(
        RegistroAsistencia.sesion_id == sesion.id
    ).all()

    if len(registros) != 26:
        raise HTTPException(
            status_code=400,
            detail=f"Faltan registros. Hay {len(registros)} de 26. Complete todos antes de cerrar."
        )

    conteo = {"A": 0, "FJ": 0, "FI": 0, "AT": 0}
    for r in registros:
        conteo[r.estado] = conteo.get(r.estado, 0) + 1

    sesion.estado = "Cerrada"
    sesion.hora_cierre = datetime.now().strftime("%H:%M")
    sesion.total_presentes = conteo["A"]
    
    try:
        h_ini = datetime.strptime(sesion.hora_inicio, "%H:%M")
        h_fin = datetime.strptime(sesion.hora_cierre, "%H:%M")
        delta = (h_fin - h_ini).total_seconds()
        sesion.tiempo_total_segundos = int(delta) if delta > 0 else None
    except:
        pass

    db.commit()

    return {
        "ok": True,
        "mensaje": "Sesión cerrada correctamente",
        "resumen": {
            "asistencias": conteo["A"],
            "faltas_justificadas": conteo["FJ"],
            "faltas_injustificadas": conteo["FI"],
            "atrasos": conteo["AT"],
            "total": sum(conteo.values()),
            "tiempo_segundos": sesion.tiempo_total_segundos
        }
    }


@app.get("/api/estudiantes")
async def listar_estudiantes(db: Session = Depends(get_db)):
    estudiantes = db.query(Estudiante).order_by(Estudiante.numero_lista).all()
    return [
        {
            "id": e.id,
            "numero_lista": e.numero_lista,
            "nombre": e.apellidos_nombres,
            "genero": e.genero
        }
        for e in estudiantes
    ]


@app.get("/api/sesion-hoy")
async def sesion_hoy(db: Session = Depends(get_db)):
    hoy = date.today()
    sesion = db.query(SesionAsistencia).filter(SesionAsistencia.fecha == hoy).first()
    if not sesion:
        return {"existe": False}

    registros = []
    for r in sesion.registros:
        registros.append({
            "estudiante_id": r.estudiante_id,
            "numero_lista": r.estudiante.numero_lista,
            "nombre": r.estudiante.apellidos_nombres,
            "genero": r.estudiante.genero,
            "estado": r.estado,
            "hora_llegada": r.hora_llegada,
            "observacion": r.observacion
        })

    return {
        "existe": True,
        "sesion_id": sesion.id,
        "estado": sesion.estado,
        "hora_inicio": sesion.hora_inicio,
        "hora_cierre": sesion.hora_cierre,
        "tiempo_total_segundos": sesion.tiempo_total_segundos,
        "registros": sorted(registros, key=lambda x: x["numero_lista"])
    }


@app.get("/api/resumen/{fecha}")
async def resumen_fecha(fecha: str, db: Session = Depends(get_db)):
    try:
        f = datetime.strptime(fecha, "%Y-%m-%d").date()
    except:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD")

    sesion = db.query(SesionAsistencia).filter(SesionAsistencia.fecha == f).first()
    if not sesion:
        raise HTTPException(status_code=404, detail="No hay sesión para esa fecha")

    conteo = {"A": 0, "FJ": 0, "FI": 0, "AT": 0}
    no_presentes = []
    for r in sesion.registros:
        conteo[r.estado] = conteo.get(r.estado, 0) + 1
        if r.estado != "A":
            no_presentes.append({
                "numero_lista": r.estudiante.numero_lista,
                "nombre": r.estudiante.apellidos_nombres,
                "genero": r.estudiante.genero,
                "estado": r.estado,
                "hora_llegada": r.hora_llegada
            })

    return {
        "fecha": fecha,
        "estado_sesion": sesion.estado,
        "conteo": conteo,
        "total": sum(conteo.values()),
        "no_presentes": no_presentes,
        "tiempo_segundos": sesion.tiempo_total_segundos
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
