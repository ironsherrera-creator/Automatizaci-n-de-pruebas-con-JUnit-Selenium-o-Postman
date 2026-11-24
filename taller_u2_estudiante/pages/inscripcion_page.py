
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class InscripcionPage:

    URL = "/inscripcion"

    FORMULARIO = (By.ID, "form-inscripcion")
    NOMBRE = (By.ID, "nombre")
    CORREO = (By.ID, "correo")
    PROGRAMA = (By.ID, "programa")
    SEMESTRE = (By.ID, "semestre")
    BOTON_INSCRIBIR = (By.ID, "btn-inscribir")
    MENSAJE_EXITO = (By.ID, "mensaje-exito")
    ENLACE_LISTADO = (By.ID, "ver-listado")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.espera = WebDriverWait(driver, 10)

    def abrir(self):
        self.driver.get(f"{self.base_url}{self.URL}")
        self.espera.until(
            EC.visibility_of_element_located(self.FORMULARIO)
        )
        return self

    def ingresar_nombre(self, nombre):
        campo = self.espera.until(
            EC.visibility_of_element_located(self.NOMBRE)
        )
        campo.clear()
        campo.send_keys(nombre)

    def ingresar_correo(self, correo):
        campo = self.driver.find_element(*self.CORREO)
        campo.clear()
        campo.send_keys(correo)

    def seleccionar_programa(self, programa):
        # Si viene vacío, se conserva la opción predeterminada del select.
        if programa:
            campo = self.driver.find_element(*self.PROGRAMA)
            Select(campo).select_by_visible_text(programa)

    def ingresar_semestre(self, semestre):
        campo = self.driver.find_element(*self.SEMESTRE)
        campo.clear()
        campo.send_keys(str(semestre))

    def inscribir(self):
        self.driver.find_element(*self.BOTON_INSCRIBIR).click()

    def registrar_estudiante(self, nombre, correo, programa, semestre):
        self.ingresar_nombre(nombre)
        self.ingresar_correo(correo)
        self.seleccionar_programa(programa)
        self.ingresar_semestre(semestre)
        self.inscribir()

    def obtener_mensaje_exito(self):
        elemento = self.espera.until(
            EC.visibility_of_element_located(self.MENSAJE_EXITO)
        )
        return elemento.text

    def obtener_error(self, campo):
        localizador = (By.ID, f"error-{campo}")
        elemento = self.espera.until(
            EC.visibility_of_element_located(localizador)
        )
        return elemento.text

    def obtener_valor(self, campo):
        localizadores = {
            "nombre": self.NOMBRE,
            "correo": self.CORREO,
            "semestre": self.SEMESTRE
        }
        elemento = self.driver.find_element(*localizadores[campo])
        return elemento.get_attribute("value")

    def abrir_listado(self):
        enlace = self.espera.until(
            EC.element_to_be_clickable(self.ENLACE_LISTADO)
        )
        enlace.click()


class ListadoPage:

    URL = "/estudiantes"
    TABLA = (By.ID, "tabla-estudiantes")
    FILAS = (
        By.CSS_SELECTOR,
        "#tabla-estudiantes tbody tr.fila-estudiante"
    )

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.espera = WebDriverWait(driver, 10)

    def abrir(self):
        self.driver.get(f"{self.base_url}{self.URL}")
        self.espera.until(
            EC.visibility_of_element_located(self.TABLA)
        )
        return self

    def correos(self):
        filas = self.espera.until(
            EC.presence_of_all_elements_located(self.FILAS)
        )

        correos = []
        for fila in filas:
            columnas = fila.find_elements(By.TAG_NAME, "td")
            if len(columnas) >= 3:
                correos.append(columnas[2].text.strip())

        return correos
