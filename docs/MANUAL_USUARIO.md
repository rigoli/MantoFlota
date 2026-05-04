# Manual de usuario — MantoFlota

MantoFlota es una aplicación web para registrar unidades de una flotilla interna, su kilometraje y el historial de mantenimientos, con un panel de inicio que sugiere próximos servicios preventivos.

## Requisitos

- Navegador actualizado (Chrome, Firefox, Edge o Safari).
- URL del sistema y credenciales que proporcione el administrador.

## 1. Acceder al sistema

1. Abra la página de inicio de MantoFlota.
2. Pulse **Entrar** (o vaya a la ruta de inicio de sesión).
3. Introduzca **correo** y **contraseña**.
4. Pulse **Entrar**. Si los datos son correctos, irá al **Inicio** (`/`), con el panel de resumen y enlaces a Unidades y Mantenimientos. Si entró desde una pantalla concreta (por ejemplo protección de ruta), tras iniciar sesión puede volver a esa pantalla según el enlace que usó.

Para salir, use **Salir** en la barra superior.

## 2. Panel de inicio (dashboard)

Tras iniciar sesión, la página principal muestra:

- Enlaces rápidos a **Unidades** y **Mantenimientos**.
- **Próximos mantenimientos sugeridos**: estimación orientativa según el último servicio registrado (intervalos fijos de 90 días y 10 000 km; si no hay historial, se usa la fecha de alta y el kilometraje actual).
- **Unidades en taller**: vehículos con estado “taller”.

Estas tablas son **sugerencias operativas**, no un sistema de alertas legales ni vencimientos certificados.

## 3. Unidades

### Listar

Menú **Unidades**. Verá una tabla con número económico, placas, marca/modelo, kilometraje, estado y acciones.

### Exportar respaldo (JSON y CSV)

En la misma pantalla puede usar **Exportar JSON** o **Exportar CSV**. Ambos incluyen todas las unidades registradas (respaldo o revisión en Excel / hojas de cálculo). El CSV usa codificación UTF-8 con BOM para abrir bien en Excel.

### Registrar unidad

1. Pulse **Nueva unidad**.
2. Complete todos los campos obligatorios (número económico, placas, marca, modelo, año, tipo de vehículo, kilometraje, estado).
3. Pulse **Guardar unidad**. Será redirigido a la ficha de la unidad.

### Ver y editar unidad

1. En el listado, pulse **Ver** sobre la unidad deseada.
2. Modifique los datos en **Editar datos** y pulse **Guardar cambios**.

### Actualizar solo el kilometraje

Use el botón **Actualizar kilometraje**, ingrese el nuevo valor y confirme.

### Eliminar unidad

Disponible en el listado o en la ficha (**Eliminar** / **Eliminar unidad**). Requiere rol de administrador en el sistema. Se eliminan también los mantenimientos asociados.

## 4. Mantenimientos

### Historial por unidad

En la ficha de la unidad, sección **Mantenimientos**, aparece la tabla del historial.

### Registrar mantenimiento

1. Pulse **Registrar mantenimiento**.
2. Complete tipo, fecha, kilometraje, costo, proveedor, responsable y observaciones (opcional).
3. Pulse **Guardar mantenimiento**.

### Editar mantenimiento

En la fila del servicio, pulse **Editar**, modifique los campos y **Guardar cambios**.

### Eliminar mantenimiento

Pulse **Eliminar** en la fila y confirme.

### Listado global

Menú **Mantenimientos**: muestra servicios recientes de toda la flota con enlace a la unidad. En esa pantalla también puede **Exportar JSON** o **Exportar CSV** del historial global (hasta 500 registros más recientes, mismo límite que el API).

## 5. Validaciones y mensajes

Si un dato no cumple las reglas (campos vacíos, números negativos, fechas inválidas), el sistema mostrará un mensaje de error. Corrija el campo indicado y vuelva a intentar.

## 6. Qué no incluye esta versión

No hay módulo de “alertas legales”, estados de mantenimiento tipo “vencido/crítico”, reportes de costos acumulados ni catálogo cerrado de tipos de servicio: el **tipo** es texto libre.

Para soporte técnico o altas de usuario, contacte al administrador del sistema.