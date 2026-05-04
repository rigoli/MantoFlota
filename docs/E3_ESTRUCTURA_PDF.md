# Estructura sugerida del PDF — Etapa 3 (MantoFlota)

Use este orden al exportar o compilar el documento final (Word/LaTeX/Google Docs → PDF). Puede fusionar contenido con [`ETAPA3.md`](ETAPA3.md) ya existente.

---

## 1. Portada

- Nombre del proyecto: **MantoFlota**
- Asignatura, institución, alumno, docente, ciudad y fecha de entrega.

---

## 2. Introducción

- Contexto del problema (mantenimiento preventivo de flotilla interna).
- Objetivos de la etapa 3: persistencia, validación, pruebas, documentación, exportación de respaldo.

### Párrafo de alcance (listo para pegar)

> La versión final de MantoFlota integra autenticación de usuarios, panel visual de inicio, gestión de unidades, registro e historial de mantenimientos, persistencia de datos mediante base de datos relacional, validación de entradas y mecanismos de prueba y documentación. Como complemento, el sistema incorpora la exportación de información a archivo JSON para respaldo y consulta externa.

---

## 3. Alcance explícito: qué **no** incluye la entrega

Incluya una lista corta para evitar sobreexpectativas:

- Centro de alertas legales o notificaciones push.
- Estados de mantenimiento tipo “al día / vencido / crítico”.
- Motor de vencimiento por “lo que ocurra primero” entre fecha y kilometraje.
- Reportes analíticos (costos acumulados por unidad o por tipo, etc.).
- Catálogo fijo de tipos de mantenimiento (el tipo es texto libre).

---

## 4. Arquitectura

- Diagrama o lista: navegador → Next.js → FastAPI → MySQL.
- Mención de despliegue futuro (Vercel / Railway) si aplica al curso.

---

## 5. Funcionalidades demostrables

Lista alineada con el manual de usuario: login, cierre de sesión, dashboard, CRUD unidades, kilometraje, CRUD mantenimientos (incluida edición en interfaz), listado global, exportación JSON.

---

## 6. Persistencia

- MySQL como almacenamiento principal entre sesiones.
- Descripción de los endpoints `GET /api/v1/export/unidades`, `/export/unidades/csv`, `/export/mantenimientos`, `/export/mantenimientos/csv` y de los botones **Exportar JSON** / **Exportar CSV** en **Unidades** y **Mantenimientos**.

---

## 7. Validación

- Texto genérico: validación en API con Pydantic y funciones auxiliares (`validators.py`).
- Tabla breve: fechas aceptadas (ISO / dd/mm/aaaa), enteros no negativos, campos obligatorios, longitudes máximas.

---

## 8. Dashboard y lógica preventiva

- Explicar heurística **90 días** y **10 000 km** desde el último servicio (o desde alta sin historial).
- Aclarar que son **sugerencias**, no certificación de cumplimiento normativo.

---

## 9. Pruebas finales

### Tabla de casos (ejemplo PF10 actualizado)

| ID | Módulo | Caso | Resultado esperado |
|----|--------|------|-------------------|
| PF10 | Exportación | Usuario autenticado pulsa Exportar JSON | Se descarga archivo `.json` con el listado de unidades |

Complete PF1–PF9 según [`ETAPA3.md`](ETAPA3.md) y marque **Pasa / No aplica** con breve nota.

- Anexe capturas (ver `docs/evidencia/README.md`).
- Anexe o resuma salida de `make test-backend` y pruebas del frontend (ver `docs/evidencia/RUN_RESULTS.md`).

---

## 10. Conclusión y referencias

- Conclusión en 1–2 párrafos.
- Referencias en formato APA 7 (ver skill o guía institucional).

---

## Anexos (opcional)

- Manual de usuario resumido o enlace al archivo [`MANUAL_USUARIO.md`](MANUAL_USUARIO.md).
- Manual técnico resumido o enlace a [`MANUAL_TECNICO.md`](MANUAL_TECNICO.md).
