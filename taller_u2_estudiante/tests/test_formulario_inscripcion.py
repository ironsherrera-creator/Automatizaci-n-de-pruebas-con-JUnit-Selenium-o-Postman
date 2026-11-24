
import csv
import uuid
from pathlib import Path

import pytest

from pages.inscripcion_page import InscripcionPage, ListadoPage


pytestmark = pytest.mark.ui

DATOS = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "casos_formulario.csv"
)


def cargar_casos_invalidos():
    with open(DATOS, encoding="utf-8", newline="") as archivo:
        return [
            pytest.param(fila, id=fila["caso"])
            for fila in csv.DictReader(archivo)
        ]


def test_cargar_formulario(driver, base_url):
    pagina = InscripcionPage(driver, base_url).abrir()

    assert driver.title == "Inscripciones CETO"
    assert driver.find_element(*pagina.FORMULARIO).is_displayed()


def test_inscripcion_exitosa_aparece_en_listado(
    driver, base_url, evidencia
):
    correo = f"ceto_{uuid.uuid4().hex[:8]}@ceto.edu.co"

    pagina = InscripcionPage(driver, base_url).abrir()
    evidencia("01_formulario_vacio")

    pagina.registrar_estudiante(
        nombre="Carlos Gomez",
        correo=correo,
        programa="Ingenieria de Sistemas",
        semestre=5
    )

    evidencia("02_resultado_inscripcion")

    mensaje = pagina.obtener_mensaje_exito()

    assert mensaje.startswith("Inscripcion exitosa. Codigo: EST-")

    listado = ListadoPage(driver, base_url).abrir()
    evidencia("03_listado_estudiantes")

    assert correo in listado.correos()


@pytest.mark.parametrize("caso", cargar_casos_invalidos())
def test_formulario_muestra_error_por_campo(
    driver, base_url, caso, evidencia
):
    pagina = InscripcionPage(driver, base_url).abrir()

    pagina.registrar_estudiante(
        nombre=caso["nombre"],
        correo=caso["correo"],
        programa=caso["programa"],
        semestre=caso["semestre"]
    )

    error = pagina.obtener_error(caso["campo_error"])

    assert error == caso["mensaje_esperado"]

    evidencia(f"error_{caso['caso']}")


def test_conserva_nombre_despues_de_un_error(
    driver, base_url
):
    pagina = InscripcionPage(driver, base_url).abrir()

    nombre = "Luis Fernandez"

    pagina.registrar_estudiante(
        nombre=nombre,
        correo="correo-invalido",
        programa="Ingenieria de Sistemas",
        semestre=3
    )

    assert pagina.obtener_error("correo") == "Correo invalido"
    assert pagina.obtener_valor("nombre") == nombre


def test_navegar_al_listado(driver, base_url):
    pagina = InscripcionPage(driver, base_url).abrir()

    pagina.abrir_listado()

    assert driver.current_url.endswith("/estudiantes")
    assert driver.find_element(
        *ListadoPage.TABLA
    ).is_displayed()
