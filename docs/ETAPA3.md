# Proyecto integrador etapa 3

**Universidad del Valle de México**  
**Asignatura:** Lógica y Programación Estructurada  
**Proyecto:** MantoFlota  
**Alumno:** Rigoberto Gonzalez Lomeli  
**Docente:** José Antonio Urquidez Ramírez  
**Ciudad y fecha:** Cancún, Quintana Roo — [coloca la fecha final]  

---

## Introducción

En la tercera etapa del proyecto integrador se presenta la consolidación del sistema **MantoFlota**, una aplicación orientada al control básico de mantenimiento preventivo para una flotilla interna de empresa. Durante las etapas anteriores se definió el problema, se establecieron los requerimientos principales, se diseñó el flujo del sistema y se desarrolló una versión funcional inicial con operaciones básicas sobre unidades y mantenimientos.

En esta etapa final, el proyecto se enfoca en fortalecer la solución mediante la **persistencia de datos**, la **validación avanzada de entradas**, las **pruebas finales del sistema**, la **optimización del código** y la **documentación completa** del funcionamiento técnico y operativo. El propósito de esta fase es entregar una versión más robusta, clara y presentable, demostrando que el sistema no solo funciona, sino que también puede mantenerse, entenderse y utilizarse correctamente.

---

# III. Funcionalidades avanzadas, documentación y presentación final

## 3.1 Manejo de archivos y persistencia de datos

Uno de los aspectos más importantes en la etapa final del proyecto fue asegurar la permanencia de la información del sistema. En versiones básicas de consola, los datos pueden perderse al cerrar el programa si solo se almacenan en memoria. Por ello, en esta etapa se integró un mecanismo de persistencia para conservar la información registrada de las unidades y sus mantenimientos.

En el caso de **MantoFlota**, la persistencia principal se plantea mediante una base de datos, lo que permite mantener la información disponible entre sesiones y gestionar los registros de forma más organizada. Adicionalmente, puede incorporarse un mecanismo de exportación o respaldo en archivo, por ejemplo en formato **JSON** o **CSV**, con el fin de facilitar consultas externas, migración de datos o generación de evidencia documental.

### Objetivo de la persistencia

- Conservar los registros aun después de cerrar el sistema.
- Recuperar información previamente almacenada.
- Evitar pérdida de datos por reinicio o cierre de la aplicación.
- Facilitar respaldo y consulta externa de la información.

### Datos que deben persistirse

- Unidades registradas.
- Historial de mantenimientos.
- Kilometraje actual.
- Datos del proveedor o responsable.
- Costos asociados a cada servicio.

### Ejemplo de respaldo estructurado

```json
{
  "unidad": {
    "numero_economico": "U-001",
    "placas": "ABC-123-A",
    "marca": "Nissan",
    "modelo": "NP300",
    "anio": 2022,
    "tipo_vehiculo": "Camioneta",
    "kilometraje_actual": 45200,
    "estado": "Activa"
  },
  "mantenimiento": {
    "tipo": "Cambio de aceite",
    "fecha": "12/04/2026",
    "kilometraje": 45000,
    "costo": 1850.0,
    "proveedor": "Taller Central",
    "responsable": "Carlos Lopez"
  }
}
```

### Importancia técnica

La persistencia convierte al sistema en una solución útil en escenarios reales, ya que la información no depende únicamente de la ejecución actual del programa. Esto representa una mejora importante respecto a la etapa 2, donde el enfoque principal fue demostrar el flujo de las funciones básicas.

---

## 3.2 Manipulación avanzada de cadenas y validación de entradas

Otro objetivo de esta etapa fue fortalecer la calidad de la información ingresada por el usuario. Para ello, se incorporaron validaciones orientadas al manejo de cadenas, formatos y reglas básicas de captura.

En un sistema como **MantoFlota**, no basta con almacenar datos; también es necesario asegurar que los datos sean consistentes, legibles y correctos. Por esta razón, se validan campos como placas, fechas, nombres, tipos de mantenimiento y estados de unidad.

### Validaciones implementadas o propuestas

- Verificar que los campos obligatorios no estén vacíos.
- Validar que el kilometraje y el costo no sean negativos.
- Confirmar que la fecha tenga formato correcto.
- Restringir ciertos campos a letras, números o combinaciones válidas.
- Evitar caracteres no deseados en nombres o identificadores.

### Ejemplos de validación

#### Validación de fecha

```python
from datetime import datetime

def validar_fecha(fecha_texto):
    try:
        datetime.strptime(fecha_texto, "%d/%m/%Y")
        return True
    except ValueError:
        return False
```

#### Validación de nombre del responsable

```python
import re

def validar_responsable(nombre):
    patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$"
    return bool(re.match(patron, nombre))
```

#### Validación de placas

```python
import re

def validar_placas(placas):
    patron = r"^[A-Z0-9-]{5,10}$"
    return bool(re.match(patron, placas))
```

### Beneficios de estas validaciones

- Reduce errores de captura.
- Mejora la calidad de los registros.
- Facilita búsquedas y reportes futuros.
- Evita inconsistencias en la base de datos o archivos.
- Hace que el sistema sea más confiable.

---

## 3.3 Pruebas finales y optimización del sistema

En esta fase se llevaron a cabo pruebas finales para revisar tanto las funciones individuales como la interacción entre módulos. El propósito fue verificar que el sistema opere de forma coherente y que los datos fluyan correctamente entre el registro de unidades, el historial de mantenimientos y la persistencia de la información.

### Objetivos de las pruebas finales

- Confirmar el funcionamiento correcto de cada módulo.
- Verificar la interacción entre frontend, backend y almacenamiento.
- Identificar errores residuales.
- Realizar ajustes para mejorar claridad y estabilidad.
- Documentar evidencia del comportamiento del sistema.

### Casos de prueba sugeridos

| ID | Módulo | Caso evaluado | Resultado esperado |
|---|---|---|---|
| PF1 | Registro de unidad | Alta de unidad con datos válidos | La unidad se guarda correctamente |
| PF2 | Registro de unidad | Intento con campo obligatorio vacío | El sistema muestra error de validación |
| PF3 | Kilometraje | Captura de valor negativo | El sistema rechaza el dato |
| PF4 | Mantenimiento | Alta de mantenimiento para unidad existente | El registro queda asociado correctamente |
| PF5 | Historial | Consulta del historial por unidad | Se muestran mantenimientos relacionados |
| PF6 | Edición | Modificación de datos de unidad | Los cambios se guardan correctamente |
| PF7 | Eliminación | Baja de unidad con mantenimientos asociados | Se elimina la unidad y se conserva coherencia del sistema |
| PF8 | Persistencia | Reinicio de aplicación con datos previos | Los datos siguen disponibles |
| PF9 | Validación de fecha | Ingreso de formato incorrecto | El sistema rechaza la fecha |
| PF10 | Exportación o respaldo | Generación de archivo JSON o CSV | El archivo se crea correctamente |

### Optimización realizada o recomendada

- Organización modular del código.
- Separación entre lógica de negocio, validaciones y persistencia.
- Uso de nombres de función claros.
- Mejora en los mensajes mostrados al usuario.
- Reducción de repeticiones en validaciones.
- Preparación del sistema para despliegue en frontend y backend por separado.

### Comentario de mejora estructural

Como parte del crecimiento del proyecto, se plantea separar la solución en dos componentes:

- **Frontend:** interfaz de usuario, preparado para despliegue en **Vercel**.
- **Backend:** lógica de negocio, API y persistencia, preparado para despliegue en **Railway**.

Esta separación permite una mejor organización del sistema, facilita el mantenimiento y acerca el proyecto a una arquitectura más realista de desarrollo web.

---

## 3.4 Documentación, manuales y presentación final

La etapa 3 no solo implica entregar una versión más sólida del sistema, sino también presentar documentación clara para distintos tipos de usuario.

### Manual de usuario

El manual de usuario debe explicar, de forma sencilla:

- qué es MantoFlota,
- cómo acceder al sistema,
- cómo registrar una unidad,
- cómo editar o eliminar registros,
- cómo registrar mantenimientos,
- cómo consultar historial,
- cómo interpretar mensajes o validaciones,
- y, en su caso, cómo exportar información.

### Manual técnico

El manual técnico debe describir:

- arquitectura general del sistema,
- estructura del frontend y backend,
- tecnologías utilizadas,
- organización de carpetas,
- endpoints principales,
- modelo de datos,
- validaciones,
- persistencia,
- pruebas realizadas,
- e instrucciones básicas de instalación y ejecución.

### Presentación final

La presentación final debe resumir el desarrollo del proyecto, mostrando:

1. problema identificado,
2. solución propuesta,
3. arquitectura del sistema,
4. funcionalidades principales,
5. persistencia de datos,
6. validaciones,
7. pruebas finales,
8. resultado visual o demostración,
9. conclusiones.

La documentación complementa el valor del sistema, ya que permite entenderlo, usarlo y mantenerlo con mayor facilidad.

---

## Conclusión

La etapa 3 permitió consolidar **MantoFlota** como una solución más completa y estructurada. A diferencia de las fases anteriores, en esta entrega no solo se consideró la implementación funcional, sino también la permanencia de los datos, la calidad de las entradas, la validación del sistema mediante pruebas finales y la preparación de documentación técnica y de usuario.

Con ello, el proyecto alcanza un nivel más sólido tanto a nivel académico como práctico, al presentar una propuesta funcional, organizada y escalable. Además, la planeación para separar frontend y backend representa una mejora importante en la evolución del sistema y en su futura publicación en servicios como Vercel y Railway.

---

## Referencias

Moreno, D., y Carrillo, J. (2019). *Normas APA 7.a edición: Guía de citación y referenciación*. Universidad Central.

Universidad del Valle de México. (s. f.). *Actividad. Proyecto integrador, etapa 1* [Documento institucional].

Universidad del Valle de México. (s. f.). *Actividad. Proyecto integrador, etapa 2* [Documento institucional].

Universidad del Valle de México. (s. f.). *Actividad. Proyecto integrador, etapa 3* [Documento institucional].

Universidad del Valle de México. (s. f.). *Blackboard: La guía del estudiante exitoso* [Guía institucional].

Universidad del Valle de México. (s. f.). *La guía Lince de la integridad académica* [Guía institucional].

Velasco Ponce, A. (2021). *Manual para elaborar citas y referencias en formato APA: basado en la 7.a edición de las normas APA*. Ecoe Ediciones; UVM Editorial.

---

## Nota de trabajo

Este archivo está pensado como **base editable** para tu entrega de la etapa 3. Conviene ajustar el contenido final según:

- el estado real actual del repo,
- las funcionalidades que ya estén implementadas,
- las capturas o evidencias de pruebas,
- y el formato exacto que vayas a entregar en PDF.

Material de apoyo en esta carpeta `docs/`: [MANUAL_USUARIO.md](MANUAL_USUARIO.md), [MANUAL_TECNICO.md](MANUAL_TECNICO.md), [E3_ESTRUCTURA_PDF.md](E3_ESTRUCTURA_PDF.md), [PRESENTACION_E3.md](PRESENTACION_E3.md) y [evidencia/](evidencia/).
