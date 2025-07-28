import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from backend.db import Base
from backend.main import get_db
from backend.main import app
from fastapi.testclient import TestClient

# Motor en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Sesión de testing
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas solo una vez
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    # Inicia un SAVEPOINT para rollback entre tests
    session.begin_nested()

    # Escucha eventos para nuevos SAVEPOINTs si hay commits intermedios
    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
