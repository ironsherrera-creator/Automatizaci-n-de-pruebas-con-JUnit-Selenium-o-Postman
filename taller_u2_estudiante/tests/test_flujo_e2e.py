import uuid

import pytest
import requests

from pages.inscripcion_page import InscripcionPage, ListadoPage


pytestmark = [pytest.mark.ui, pytest.mark.e2e]


def test_registro_web_se_verifica_en_api(driver, base_url, api_url):
    # Arrange
    correo = f"e2e_web_{uuid.uuid4().hex[:8]}@correo.com"

    pagina = InscripcionPage(driver, base_url)

    # Act: registrar mediante el formulario web
    pagina.abrir()
    pagina.registrar_estudiante(
        "Estudiante E2E Web",
        correo,
        "Ingenieria de Sistemas",
        3
    )

    mensaje = pagina.obtener_mensaje_exito()

    # Assert: verificar el registro mediante la API
    respuesta = requests.get(api_url)
    assert respuesta.status_code == 200

    estudiantes = respuesta.json()
    registro = next(
        (e for e in estudiantes if e["correo"] == correo),
        None
    )

    assert registro is not None
    assert registro["nombre"] == "Estudiante E2E Web"
    assert registro["semestre"] == 3
    assert "Inscripcion exitosa" in mensaje


def test_registro_api_aparece_en_listado_web(api_url, driver, base_url):
    # Arrange
    correo = f"e2e_api_{uuid.uuid4().hex[:8]}@correo.com"

    estudiante = {
        "nombre": "Estudiante E2E API",
        "correo": correo,
        "programa": "Tecnologia en Desarrollo de Software",
        "semestre": 4
    }

    # Act: registrar mediante la API
    respuesta = requests.post(api_url, json=estudiante)

    # Assert: comprobar creación
    assert respuesta.status_code == 201

    # Act: abrir el listado web
    listado = ListadoPage(driver, base_url).abrir()
    correos = listado.correos()

    # Assert: comprobar que el registro aparece en la interfaz
    assert correo in correos


def test_formulario_rechaza_correo_duplicado(driver, base_url):
    # Arrange
    correo = f"e2e_duplicado_{uuid.uuid4().hex[:8]}@correo.com"

    pagina = InscripcionPage(driver, base_url)

    # Act: realizar el primer registro
    pagina.abrir()
    pagina.registrar_estudiante(
        "Estudiante Duplicado",
        correo,
        "Ingenieria Industrial",
        5
    )

    mensaje = pagina.obtener_mensaje_exito()
    assert "Inscripcion exitosa" in mensaje

    # Act: intentar registrar nuevamente el mismo correo
    pagina.abrir()
    pagina.registrar_estudiante(
        "Estudiante Duplicado",
        correo,
        "Ingenieria Industrial",
        5
    )

    # Assert: el sistema debe mostrar el error de correo duplicado
    error = pagina.obtener_error("correo")

    assert "correo ya esta registrado" in error.lower()
