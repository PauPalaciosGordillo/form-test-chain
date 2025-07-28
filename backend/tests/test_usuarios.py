import uuid
from backend.tests.test_db import client

def test_crear_usuario():
    email_unico = f"test_{uuid.uuid4()}@example.com"
    response = client.post("/usuarios/", json={
        "nombre_completo": "Test User",
        "email": email_unico,
        "telefono": "123456789",
        "edad": 30,
        "pais": "España",
        "comentarios": "Este es un test"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email_unico

def test_campos_obligatorios():
    response = client.post("/usuarios/", json={})
    assert response.status_code == 422

def test_edad_negativa():
    email_unico = f"edad_negativa_{uuid.uuid4()}@example.com"
    response = client.post("/usuarios/", json={
        "nombre_completo": "Negativo",
        "email": email_unico,
        "telefono": "000000000",
        "edad": -10,
        "pais": "España",
        "comentarios": ""
    })
    assert response.status_code == 422

def test_email_invalido():
    response = client.post("/usuarios/", json={
        "nombre_completo": "Correo Inválido",
        "email": "correo-no-valido",
        "telefono": "000000000",
        "edad": 25,
        "pais": "España",
        "comentarios": ""
    })
    assert response.status_code == 422

def test_listar_usuarios():
    response = client.get("/usuarios/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
