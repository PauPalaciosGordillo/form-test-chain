from backend.tests.test_db import client

def test_crear_usuario():
    response = client.post("/usuarios/", json={
        "nombre_completo": "Test User",
        "email": "testuser@example.com",
        "telefono": "123456789",
        "edad": 30,
        "pais": "España",
        "comentarios": "Este es un test"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nombre_completo"] == "Test User"
    assert data["email"] == "testuser@example.com"
    assert "id" in data

def test_crear_usuario_faltan_campos():
    response = client.post("/usuarios/", json={
        "email": "incompleto@example.com",
        "telefono": "123456789",
        "edad": 25,
        "pais": "España"
    })
    assert response.status_code == 422

def test_crear_usuario_email_invalido():
    response = client.post("/usuarios/", json={
        "nombre_completo": "Email Inválido",
        "email": "noesuncorreo",
        "telefono": "123456789",
        "edad": 30,
        "pais": "España",
        "comentarios": "Correo no válido"
    })
    assert response.status_code == 422

def test_crear_usuario_edad_negativa():
    response = client.post("/usuarios/", json={
        "nombre_completo": "Edad Negativa",
        "email": "edad@negativa.com",
        "telefono": "123456789",
        "edad": -5,
        "pais": "España",
        "comentarios": "Edad inválida"
    })
    assert response.status_code == 422

def test_crear_usuario_telefono_invalido():
    response = client.post("/usuarios/", json={
        "nombre_completo": "Teléfono Inválido",
        "email": "telefono@invalido.com",
        "telefono": "123ABC456",
        "edad": 30,
        "pais": "España",
        "comentarios": "Teléfono con letras"
    })
    assert response.status_code == 422

    response = client.post("/usuarios/", json={
        "nombre_completo": "Teléfono Corto",
        "email": "telefono@corto.com",
        "telefono": "12345",
        "edad": 30,
        "pais": "España",
        "comentarios": "Teléfono demasiado corto"
    })
    assert response.status_code == 422

    response = client.post("/usuarios/", json={
        "nombre_completo": "Teléfono Largo",
        "email": "telefono@largo.com",
        "telefono": "1234567890",
        "edad": 30,
        "pais": "España",
        "comentarios": "Teléfono demasiado largo"
    })
    assert response.status_code == 422
