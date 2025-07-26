from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db import Base  
from backend.main import app, get_db
from fastapi.testclient import TestClient

# Base de datos SQLite en memoria para testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Sobrescribir la dependencia de get_db para usar esta sesión de testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
