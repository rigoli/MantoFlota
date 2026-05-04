# Evidencia — Etapa 3 (MantoFlota)

## Capturas sugeridas (manuales)

Tomar desde el navegador con datos de prueba coherentes (MAMP + API + frontend en marcha):

1. **Login** — `/login` con sesión iniciada o formulario listo.
2. **Dashboard** — `/` autenticado: tablas de próximos mantenimientos y en taller.
3. **Listado de unidades** — `/unidades` con tabla y botones **Exportar JSON** / **Exportar CSV**.
4. **Alta unidad** — `/unidades/nueva` o confirmación tras guardar.
5. **Edición unidad** — ficha `/unidades/{id}` sección “Editar datos”.
6. **Alta mantenimiento** — diálogo “Registrar mantenimiento”.
7. **Edición mantenimiento** — diálogo “Editar mantenimiento” en una fila del historial.
8. **Historial** — misma ficha, tabla de mantenimientos.
9. **Exportación unidades** — descarga JSON y CSV de unidades.
10. **Exportación mantenimientos** — en `/mantenimientos`, descarga JSON y CSV del historial global.

Guardar imágenes en la carpeta que exija la entrega institucional (zip, PDF, etc.).

## Pruebas automáticas (comandos)

Desde la raíz del repositorio:

```bash
make test-backend
```

```bash
cd frontend && pnpm test && pnpm lint && pnpm typecheck
```

Opcional E2E (requiere Chromium instalado):

```bash
cd frontend && pnpm e2e:install   # una vez
make e2e
```

## Resultado de una corrida local

Ver `RUN_RESULTS.md` en esta carpeta (actualizar tras cada corrida antes de entregar).
