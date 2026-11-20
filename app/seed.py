"""
Seed inicial con los 26 estudiantes del Curso 2 CDD "A"
y el calendario del 1er trimestre 2026-2027
"""
from datetime import date, timedelta
from .database import SessionLocal, Estudiante, CalendarioDia, init_db

ESTUDIANTES = [
    (1, "Almeida, Steven Jose", "Hombre"),
    (2, "Amoroso Sandoval, Angela Mishel", "Mujer"),
    (3, "Benavides Valencia, Jonathan David", "Hombre"),
    (4, "Bombon Chimpatiza, Joseph Fernando", "Hombre"),
    (5, "Chicaiza Jimenez, Paola Cristina", "Mujer"),
    (6, "Chico Ashqui, Justin Guillermo", "Hombre"),
    (7, "Culqui Quilcapi, Joel Dario", "Hombre"),
    (8, "Escobar Rivera, Julian David", "Hombre"),
    (9, "Espin Reinoso, Mathias Alberto", "Hombre"),
    (10, "Guerrero Agudelo, Alanis Nicole", "Mujer"),
    (11, "Hurtado Hurtado, Erick Leandro", "Hombre"),
    (12, "Laica Caisa, Anderson Smith", "Hombre"),
    (13, "Largo Arboleda, Antony Jharin", "Hombre"),
    (14, "Mallatasig Murillo, Leon Pierre", "Hombre"),
    (15, "Masabanda Chiriapa, Leslie Nicole", "Mujer"),
    (16, "Moran Escobar, Mateo Alexander", "Hombre"),
    (17, "Moreno Caisaguano, Maykel Josue", "Hombre"),
    (18, "Ocaña Vega, Maykel Joshua", "Hombre"),
    (19, "Palango Guaraca, Andres Paolo", "Hombre"),
    (20, "Poaquiza Punina, Genesis Lizeth", "Mujer"),
    (21, "Ramirez Lagos, Jonathan Alexander", "Hombre"),
    (22, "Rosero Oloyache, Maria Jose", "Mujer"),
    (23, "Sanchez Castro, Joselyn Teresa", "Mujer"),
    (24, "Timpiza Urbina, Johan Paul", "Hombre"),
    (25, "Tusa Loumatasig, Bryan Stalin", "Hombre"),
    (26, "Zuniga Tumiña, Christopher Santiago", "Hombre"),
]

FERIADOS = {
    date(2026, 10, 9): "Feriado",   # Independencia de Guayaquil
    date(2026, 11, 2): "Feriado",   # Día de los Difuntos
    date(2026, 11, 3): "Feriado",   # Independencia de Cuenca
}

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def seed_estudiantes(db):
    if db.query(Estudiante).count() > 0:
        return
    for num, nombre, genero in ESTUDIANTES:
        est = Estudiante(
            numero_lista=num,
            apellidos_nombres=nombre,
            genero=genero,
            observaciones="Ninguna",
            contacto_tutor="Por registrar"
        )
        db.add(est)
    db.commit()
    print(f"✓ {len(ESTUDIANTES)} estudiantes cargados")


def seed_calendario(db):
    if db.query(CalendarioDia).count() > 0:
        return

    start = date(2026, 9, 1)
    end = date(2026, 12, 1)
    current = start
    count = 0

    while current <= end:
        if current.weekday() < 5:  # Lunes a Viernes
            estado = FERIADOS.get(current, "Lectivo")
            materia = "—" if estado == "Feriado" else "Ciencia de Datos"
            horario = "—" if estado == "Feriado" else "13:00 – 15:40"

            dia = CalendarioDia(
                fecha=current,
                dia_semana=DIAS_SEMANA[current.weekday()],
                materia=materia,
                horario=horario,
                estado_lectivo=estado
            )
            db.add(dia)
            if estado == "Lectivo":
                count += 1
        current += timedelta(days=1)

    db.commit()
    print(f"✓ Calendario cargado ({count} días lectivos)")


def run_seed():
    init_db()
    db = SessionLocal()
    try:
        seed_estudiantes(db)
        seed_calendario(db)
        print("✓ Base de datos inicializada correctamente")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
