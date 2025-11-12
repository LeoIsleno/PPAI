from sqlalchemy import create_engine, event
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker, declarative_base

import os
from pathlib import Path

# --- Configuración de la Base de Datos ---

# Si DATABASE_URL está definida en el entorno, la usamos; sino usamos
# el archivo local bdd/sismografos.db dentro del paquete BDD.
env_url = os.getenv("DATABASE_URL")
if env_url:
    DATABASE_URL = env_url
else:
    repo_folder = Path(__file__).resolve().parent
    db_path = repo_folder / "sismografos.db"
    DATABASE_URL = f"sqlite:///{db_path.as_posix()}"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False, "timeout": 30},
    poolclass=NullPool,
)

@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA busy_timeout = 30000;")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    """Importa `BDD.orm_models` (que utiliza `Base`) y crea las tablas.

    Hacemos el import de forma perezosa para evitar ciclos en el tiempo de
    importación: `BDD.orm_models` hace `from .database import Base`, por lo
    que `Base` debe existir antes de importar los modelos.
    """
    import BDD.orm_models  # noqa: F401

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    print(f"Initializing DB at: {DATABASE_URL}")
    init_db()
    print("Database initialized (tables created).")
