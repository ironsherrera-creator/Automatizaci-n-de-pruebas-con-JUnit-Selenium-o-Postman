
import uuid

import pytest
import requests


@pytest.mark.api
def test_registrar_estudiante_correctamente(api_url):
    # Arrange
    estudiante = {
        "nombre": "Carlos Ramirez",
        "correo": f"carlos_{uuid.uuid4().hex[:8]}@correo.com",
        "programa": "Ingenieria de Sistemas",
        "semestre": 3
    }

    # Act
    respuesta = requests.post(api_url, json=estudiante)

    # Assert
    assert respuesta.status_code == 201

    datos = respuesta.json()
    assert datos["nombre"] == estudiante["nombre"]
    assert datos["correo"] == estudiante["correo"]
    assert datos["programa"] == estudiante["programa"]
    assert datos["semestre"] == estudiante["semestre"]
    assert "id" in datos


@pytest.mark.api
def test_listar_estudiantes(api_url):
    # Arrange
    estudiante = {
        "nombre": "Laura Martinez",
        "correo": f"laura_{uuid.uuid4().hex[:8]}@correo.com",
        "programa": "Ingenieria Industrial",
        "semestre": 5
    }
    requests.post(api_url, json=estudiante)

    # Act
    respuesta = requests.get(api_url)

    # Assert
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)
    assert any(
        e["correo"] == estudiante["correo"]
        for e in respuesta.json()
    )


@pytest.mark.api
def test_filtrar_estudiantes_por_programa(api_url):
    # Arrange
    programa = "Tecnologia en Desarrollo de Software"
    estudiante = {
        "nombre": "Andres Gomez",
        "correo": f"andres_{uuid.uuid4().hex[:8]}@correo.com",
        "programa": programa,
        "semestre": 4
    }
    requests.post(api_url, json=estudiante)

    # Act
    respuesta = requests.get(
        api_url,
        params={"programa": programa}
    )

    # Assert
    assert respuesta.status_code == 200
    assert all(e["programa"] == programa for e in respuesta.json())
    assert any(
        e["correo"] == estudiante["correo"]
        for e in respuesta.json()
    )


@pytest.mark.api
def test_consultar_estudiante_por_id(api_url):
    # Arrange
    estudiante = {
        "nombre": "Pedro Sanchez",
        "correo": f"pedro_{uuid.uuid4().hex[:8]}@correo.com",
        "programa": "Ingenieria de Sistemas",
        "semestre": 2
    }
    registro = requests.post(api_url, json=estudiante).json()
    estudiante_id = registro["id"]

    # Act
    respuesta = requests.get(f"{api_url}/{estudiante_id}")

    # Assert
    assert respuesta.status_code == 200
    assert respuesta.json()["id"] == estudiante_id
    assert respuesta.json()["correo"] == estudiante["correo"]


@pytest.mark.api
def test_eliminar_estudiante(api_url):
    # Arrange
    estudiante = {
        "nombre": "Maria Lopez",
        "correo": f"maria_{uuid.uuid4().hex[:8]}@correo.com",
        "programa": "Ingenieria Industrial",
        "semestre": 6
    }
    registro = requests.post(api_url, json=estudiante).json()
    estudiante_id = registro["id"]

    # Act
    respuesta = requests.delete(f"{api_url}/{estudiante_id}")

    # Assert
    assert respuesta.status_code == 204
    assert respuesta.text == ""

    consulta = requests.get(f"{api_url}/{estudiante_id}")
    assert consulta.status_code == 404


@pytest.mark.api
@pytest.mark.parametrize(
    "campo,valor",
    [
        ("nombre", "Al"),
        ("correo", "correo-invalido"),
        ("programa", "Programa inexistente"),
        ("semestre", 0),
        ("semestre", 11),
        ("semestre", "abc"),
    ]
)
def test_rechazar_datos_invalidos(api_url, campo, valor):
    # Arrange
    estudiante = {
        "nombre": "Estudiante Valido",
        "correo": f"valido_{uuid.uuid4().hex[:8]}@correo.com",
        "programa": "Ingenieria de Sistemas",
        "semestre": 3
    }
    estudiante[campo] = valor

    # Act
    respuesta = requests.post(api_url, json=estudiante)

    # Assert
    assert respuesta.status_code == 422
    assert campo in respuesta.json()["errores"]


@pytest.mark.api
def test_rechazar_correo_duplicado(api_url):
    # Arrange
    estudiante = {
        "nombre": "Daniel Torres",
        "correo": f"duplicado_{uuid.uuid4().hex[:8]}@correo.com",
        "programa": "Ingenieria Industrial",
        "semestre": 4
    }

    primera_respuesta = requests.post(api_url, json=estudiante)
    segunda_respuesta = requests.post(api_url, json=estudiante)

    # Act
    # La segunda solicitud intenta registrar el mismo correo.

    # Assert
    assert primera_respuesta.status_code == 201
    assert segunda_respuesta.status_code == 409
    assert "correo" in segunda_respuesta.json()["errores"]


@pytest.mark.api
def test_rechazar_cuerpo_que_no_es_json(api_url):
    # Arrange
    contenido = "Esto no es un objeto JSON"

    # Act
    respuesta = requests.post(
        api_url,
        data=contenido,
        headers={"Content-Type": "text/plain"}
    )

    # Assert
    assert respuesta.status_code == 400
    assert respuesta.json()["error"] == "El cuerpo debe ser JSON"


@pytest.mark.api
def test_consultar_estudiante_inexistente(api_url):
    # Arrange
    estudiante_id = 999999

    # Act
    respuesta = requests.get(f"{api_url}/{estudiante_id}")

    # Assert
    assert respuesta.status_code == 404
    assert respuesta.json()["error"] == "Estudiante no encontrado"


@pytest.mark.api
def test_eliminar_estudiante_inexistente(api_url):
    # Arrange
    estudiante_id = 999999

    # Act
    respuesta = requests.delete(f"{api_url}/{estudiante_id}")

    # Assert
    assert respuesta.status_code == 404
    assert respuesta.json()["error"] == "Estudiante no encontrado"
