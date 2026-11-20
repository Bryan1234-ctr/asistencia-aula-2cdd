from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum

SQLALCHEMY_DATABASE_URL = "sqlite:///./asistencia.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class GeneroEnum(str, enum.Enum):
    HOMBRE = "Hombre"
    MUJER = "Mujer"


class EstadoAsistenciaEnum(str, enum.Enum):
    A = "A"      # Asistencia
    FJ = "FJ"    # Falta Justificada
    FI = "FI"    # Falta Injustificada
    AT = "AT"    # Atraso


class EstadoLectivoEnum(str, enum.Enum):
    LECTIVO = "Lectivo"
    NO_LECTIVO = "No lectivo"
    FERIADO = "Feriado"
    SUSPENSION = "Suspensión"


class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    numero_lista = Column(Integer, unique=True, nullable=False)
    apellidos_nombres = Column(String(150), nullable=False)
    genero = Column(String(20), nullable=False)
    observaciones = Column(String(255), default="Ninguna")
    contacto_tutor = Column(String(150), default="Por registrar")
    activo = Column(Boolean, default=True)

    registros = relationship("RegistroAsistencia", back_populates="estudiante")


class SesionAsistencia(Base):
    __tablename__ = "sesiones_asistencia"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False, index=True)
    hora_inicio = Column(String(10), default="13:00")
    hora_cierre = Column(String(10), nullable=True)
    tiempo_total_segundos = Column(Integer, nullable=True)
    mecanismo = Column(String(50), default="Lista masiva")
    estado = Column(String(20), default="Activa")  # Activa | Cerrada
    total_esperados = Column(Integer, default=26)
    total_presentes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    registros = relationship("RegistroAsistencia", back_populates="sesion")


class RegistroAsistencia(Base):
    __tablename__ = "registros_asistencia"

    id = Column(Integer, primary_key=True, index=True)
    sesion_id = Column(Integer, ForeignKey("sesiones_asistencia.id"))
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"))
    estado = Column(String(5), default="A")  # A, FJ, FI, AT
    hora_llegada = Column(String(10), nullable=True)  # Solo para AT
    observacion = Column(String(255), nullable=True)
    marcado_por = Column(String(100), default="Docente")
    timestamp = Column(DateTime, default=datetime.utcnow)

    sesion = relationship("SesionAsistencia", back_populates="registros")
    estudiante = relationship("Estudiante", back_populates="registros")


class CalendarioDia(Base):
    __tablename__ = "calendario"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, unique=True, nullable=False)
    dia_semana = Column(String(15))
    materia = Column(String(100), default="Ciencia de Datos")
    horario = Column(String(20), default="13:00 – 15:40")
    estado_lectivo = Column(String(20), default="Lectivo")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
