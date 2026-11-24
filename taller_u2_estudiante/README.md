# Inscripciones CETO — Diagnóstico técnico y guía para AA1

## 1. Descripción general

Inscripciones CETO es una aplicación pequeña construida con Flask para registrar estudiantes. Incluye una API REST, un formulario web y una página con el listado. El repositorio sirve como proyecto base para la evidencia AA1 de automatización de pruebas.

Este README documenta la estructura y el comportamiento observados en el código. La inspección fue estática: no se inició el servidor ni se ejecutaron pruebas. Por eso, se describe lo implementado sin afirmar resultados de ejecución.

## 2. Estructura del proyecto

```text
taller_u2_estudiante/
├── app/
│   ├── __init__.py                 # Vacío
│   ├── servidor.py                 # Aplicación Flask, API y rutas web
│   └── templates/
│       ├── inscripcion.html        # Formulario de inscripción
│       └── estudiantes.html        # Tabla de estudiantes inscritos
├── data/
│   └── .gitkeep                    # Sin archivos de datos todavía
├── evidencias/
│   └── .gitkeep                    # Sin capturas guardadas todavía
├── pages/
│   └── __init__.py                 # Vacío; no hay Page Objects todavía
├── tests/
│   └── conftest.py                 # Fixtures y configuración compartida
├── pytest.ini                      # Configuración de pytest y marcadores
├── requirements.txt               # Dependencias declaradas
└── README.md                       # Este documento
```

No se encontraron archivos CSS ni JavaScript separados, pruebas `test_*.py`, archivos CSV ni carpeta `reportes/`. Los estilos del formulario están escritos dentro de `app/templates/inscripcion.html`.

## 3. Tecnologías y dependencias

| Tecnología | Uso previsto en este proyecto | Estado observado |
|---|---|---|
| Python | Backend y código de pruebas | Código Python en `app/` y `tests/` |
| Flask | API, rutas web y plantillas | Aplicación definida en `app/servidor.py` |
| pytest | Organización y ejecución de pruebas | `pytest.ini` y fixtures en `tests/conftest.py`; faltan casos de prueba |
| requests | Llamadas HTTP desde pruebas de API | Declarada, aún no usada por pruebas del repositorio |
| Selenium WebDriver | Automatización del formulario en navegador | Fixture `driver` preparada en `conftest.py` |
| pytest-html | Generación de un reporte HTML | Dependencia y comando documentados; no hay reporte creado |
| CSV | Datos externos para pruebas | Pendiente; `data/` solo contiene `.gitkeep` |
| Page Object Model | Separación entre interacción UI y pruebas | Pendiente; `pages/__init__.py` está vacío |

`requirements.txt` declara `flask>=3.0`, `requests>=2.31`, `pytest>=8.0`, `pytest-html>=4.0` y `selenium>=4.11`. Esto confirma las dependencias declaradas, no cuáles están instaladas en el entorno.

## 4. Instalación e inicio manual

El README original del proyecto propone crear y activar un entorno virtual e instalar las dependencias:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

Para iniciar el servidor manualmente:

```bash
python -m app.servidor
```

El código inicia Flask en el puerto `5000` con `debug=False`. Las rutas para explorar la aplicación son:

- Formulario: `http://127.0.0.1:5000/inscripcion`
- Listado: `http://127.0.0.1:5000/estudiantes`
- API: `http://127.0.0.1:5000/api/estudiantes`

Los registros se guardan en memoria y se pierden al reiniciar el servidor.

## 5. Backend y API REST

`app/servidor.py` define `crear_app()`, que construye la aplicación Flask. Los estudiantes se guardan en un diccionario local y los IDs se asignan con un contador. La función interna `validar(datos)` centraliza las validaciones del formulario y de la API.

| Método | Endpoint | Función | Datos de entrada | Respuesta definida en el código |
|---|---|---|---|---|
| GET | `/api/estudiantes` | Lista estudiantes; permite filtro exacto por programa | Query opcional `programa` | `200` y lista JSON |
| POST | `/api/estudiantes` | Valida y crea estudiante | Objeto JSON con `nombre`, `correo`, `programa`, `semestre` | `201` y estudiante JSON; `400` cuerpo no JSON/objeto; `422` datos inválidos; `409` correo duplicado cuando es el único error |
| GET | `/api/estudiantes/<id>` | Consulta por ID entero | ID de ruta | `200` y estudiante JSON; `404` si no existe |
| DELETE | `/api/estudiantes/<id>` | Elimina por ID entero | ID de ruta | `204` cuerpo vacío; `404` si no existe |

Ejemplo de objeto devuelto al crear un estudiante:

```json
{
  "id": 1,
  "nombre": "Ana Pérez",
  "correo": "ana@example.com",
  "programa": "Ingenieria de Sistemas",
  "semestre": 1
}
```

Los errores de validación usan la estructura `{"errores": {"campo": "mensaje"}}`. Los errores de consulta o eliminación usan `{"error": "Estudiante no encontrado"}`.

## 6. Frontend e identificadores para Selenium

El formulario usa POST tradicional a `/inscripcion`; no se encontró comunicación AJAX. Los errores se muestran al volver a renderizar la página con los datos enviados. El backend devuelve estado HTTP `200` para ese renderizado con errores.

| Elemento | ID HTML | Tipo | Función |
|---|---|---|---|
| Formulario | `form-inscripcion` | `form` | Envía campos por POST a `/inscripcion` |
| Nombre | `nombre` | `input` | Nombre completo |
| Error de nombre | `error-nombre` | `div` condicional | Mensaje de validación |
| Correo | `correo` | `input` | Correo electrónico |
| Error de correo | `error-correo` | `div` condicional | Correo inválido o duplicado |
| Programa | `programa` | `select` | Selección del programa |
| Error de programa | `error-programa` | `div` condicional | Programa no válido |
| Semestre | `semestre` | `input type="number"` | Semestre de 1 a 10 según backend |
| Error de semestre | `error-semestre` | `div` condicional | Mensaje de validación |
| Botón Inscribir | `btn-inscribir` | `button` | Envía el formulario |
| Mensaje de éxito | `mensaje-exito` | `p` condicional, `role="status"` | Informa el código `EST-####` asignado |
| Enlace al listado | `ver-listado` | `a` | Navega a `/estudiantes` |
| Tabla del listado | `tabla-estudiantes` | `table` | Muestra estudiantes inscritos |
| Fila del estudiante | `fila-estudiante` | Clase CSS | Identifica cada fila de datos |
| Total | `total` | `p` | Muestra el número de registros |

No hay validaciones JavaScript encontradas. El campo de correo no declara `type="email"`; los controles no incluyen `required`; el campo numérico no tiene atributos `min` o `max`. Las reglas efectivas se aplican en el servidor.

## 7. Reglas de negocio verificadas en el código

| Regla | Comportamiento implementado |
|---|---|
| Nombre | Se recortan espacios de los extremos y se requieren al menos 3 caracteres |
| Correo | Se recortan espacios, se pasa a minúsculas y se valida con `^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$` |
| Unicidad del correo | Se compara el correo normalizado contra registros existentes; la comparación no distingue mayúsculas |
| Programa | Debe ser exactamente uno de: `Ingenieria de Sistemas`, `Tecnologia en Desarrollo de Software`, `Ingenieria Industrial` |
| Semestre | Se convierte a entero y debe estar entre 1 y 10, inclusive |
| Cuerpo de POST API | Si `request.get_json(silent=True)` no produce un objeto, devuelve `400` |
| Datos inválidos API | Devuelve `422`, salvo duplicado como único error (`409`) |
| Datos inválidos en formulario | Re-renderiza el formulario con errores y valores; respuesta `200` |
| ID inexistente | GET y DELETE devuelven `404` |
| Filtro por programa | Coincidencia exacta; al omitirlo o enviarlo vacío lista todo |

El patrón de correo es sencillo y no pretende validar todos los casos permitidos por la especificación completa del correo electrónico.

## 8. Configuración actual de pruebas

`pytest.ini` define `testpaths = tests`, registra los marcadores `api`, `ui`, `e2e` y añade `-ra`.

`tests/conftest.py` contiene estas fixtures:

- `base_url` (sesión): usa `BASE_URL` si está definida; en otro caso crea una instancia de la app y la sirve en un puerto libre durante la sesión.
- `api_url` (sesión): construye la URL base `/api/estudiantes`.
- `driver` (por prueba): inicia Chrome y lo cierra al terminar. Headless está activo por defecto (`HEADLESS=1`). Admite `CHROME_BIN` y `CHROMEDRIVER` para configurar los ejecutables.
- `evidencia`: permite guardar capturas PNG en `evidencias/`.
- Hook de pytest: si falla una prueba que usó `driver`, guarda una captura `FALLO__...png`.

La aplicación creada por `base_url` mantiene los datos durante la sesión de pruebas. No hay una fixture de limpieza de estudiantes. La carpeta `evidencias/` se crea si hace falta al guardar capturas. El README original documentaba generar un HTML con:

```bash
python -m pytest -v --html=reportes/reporte.html --self-contained-html
```

La carpeta `reportes/` no existe aún en el árbol inspeccionado. El comando regular documentado es `python -m pytest -v`.

## 9. Estado de los componentes

**Implementado**

- Aplicación Flask, API REST, formulario y listado.
- Reglas de validación y respuestas descritas arriba.
- Almacenamiento en memoria.
- Fixtures para servidor, URL de API, Selenium y capturas.
- Marcadores de pytest y dependencias declaradas.

**Parcialmente implementado**

- pytest está configurado, pero no existen pruebas.
- Selenium/Chrome está preparado en una fixture, pero no hay flujos UI automatizados.
- Captura de evidencia está preparada, pero `evidencias/` solo contiene `.gitkeep`.
- pytest-html está declarado y su uso documentado, pero no hay reporte generado ni carpeta `reportes/`.

**Pendiente**

- Pruebas de API y de interfaz.
- Page Objects dentro de `pages/`.
- Datos de prueba CSV y su carga desde las pruebas.
- Matriz de casos de prueba, evidencias de ejecución y reporte final.

## 10. Plan técnico para completar AA1

1. Crear módulos `test_*.py` bajo `tests/`, marcando los grupos `api` y `ui`.
2. Implementar pruebas API con `requests` y `api_url` para camino feliz, consulta, listado y filtro, eliminación, datos inválidos, límites, duplicado, cuerpo no JSON e ID inexistente.
3. Mantener independencia de datos; usar correos únicos y considerar el estado compartido durante la sesión.
4. Aplicar Arrange, Act, Assert y parametrizar casos repetidos de validación.
5. Añadir los datos externos CSV dentro de `data/` y cargar los casos desde las pruebas.
6. Crear Page Objects en `pages/` para encapsular los localizadores y acciones del formulario.
7. Automatizar inscripción exitosa, nombre corto, correo inválido, programa sin seleccionar, semestre inválido y conservación de los datos tras error.
8. Usar esperas explícitas de Selenium para mensajes y cambios de página, especialmente porque el POST web simula medio segundo de latencia.
9. Guardar capturas necesarias con `evidencia` y generar el reporte HTML en `reportes/`.
10. Documentar resultados reales solo después de ejecutar la suite.

## 11. Posibles dificultades y recomendaciones

- **Estado compartido:** registros creados por una prueba pueden afectar las siguientes durante la misma sesión. Evitar depender del orden y usar correos únicos.
- **Diferencia de status entre API y web:** la API responde `422`/`409` ante validación, mientras el formulario vuelve a renderizar con `200`.
- **Correo duplicado con errores múltiples:** el código devuelve `409` solamente si el duplicado es el único error; con otros errores devuelve `422`.
- **Selenium y latencia:** usar esperas explícitas, no pausas fijas. El servidor espera 0,5 segundos en cada POST web.
- **Chrome y driver:** la fixture necesita Chrome y un driver compatible disponibles o las variables de entorno configuradas.
- **Filtro exacto:** el parámetro `programa` requiere coincidencia exacta.
- **Reporte HTML:** crear `reportes/` antes de usar la ruta documentada si la herramienta no la crea automáticamente.

## 12. Conclusión

El proyecto ya incluye una aplicación Flask con API y formulario, reglas de negocio implementadas y una base inicial para pytest, Selenium headless y capturas. La evidencia AA1 requiere completar las pruebas, los Page Objects, los datos CSV, la matriz de casos, las capturas y el reporte. La infraestructura existente permite empezar ese desarrollo reutilizando `base_url`, `api_url`, `driver` y `evidencia`.
