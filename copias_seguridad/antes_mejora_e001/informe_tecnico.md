# Informe técnico — Auditoría PEAD Educarex

**Versión 1.1 — 24-11-2026**

## Resumen

Se han documentado seis observaciones (E-001 a E-006), con distinto grado de confirmación e impacto. E-001 acredita exposición de detalles internos de base de datos. Las observaciones de cookies y cabeceras requieren evaluación adicional. No se ha demostrado SQLi, XSS, bypass ni secuestro de sesión.

## Hallazgos

### E-001 — Divulgación de información interna mediante error SQL

**Estado:** Confirmado en la evidencia conservada  
**Prioridad:** Media provisional

La respuesta HTTP 500 conservada expone el error SQL 1048, la columna login, la tabla pead_usuariosacceso0, una sentencia INSERT y la ruta y línea del modelo. También se observaron respuestas HTTP 500 ante HEAD y OPTIONS en el endpoint de login. En OPTIONS se observó una plantilla de error de base de datos, pero no se confirmó que contuviera exactamente el mismo error SQL.

### E-002 — Atributos de seguridad de cookies no observados

**Estado:** Observado en las respuestas recopiladas; inventario pendiente de consolidación  
**Prioridad:** Baja provisional

Las instancias gcprsess examinadas no muestran Secure, HttpOnly ni SameSite. El recuento inicial fue de cinco instancias válidas; se recopilaron respuestas adicionales posteriormente, por lo que el total definitivo debe recalcularse desde las cabeceras redactadas.

### E-003 — Duplicación de cookies de sesión en una misma respuesta

**Estado:** Reproducido en múltiples respuestas anónimas; impacto no demostrado  
**Prioridad:** Informativa

Se observaron varias cabeceras Set-Cookie con nombre gcprsess en múltiples respuestas HTML de PEAD. Las cookies propias se probaron individualmente y en conjunto; las páginas públicas mantuvieron el mismo contenido y las rutas protegidas redirigieron al acceso. No se demostró bypass, fijación ni secuestro de sesión.

### E-004 — Cabeceras de seguridad no observadas

**Estado:** No observadas en las capturas revisadas; alcance limitado  
**Prioridad:** Baja provisional

Las capturas revisadas no muestran determinadas cabeceras de seguridad. Esto no demuestra su ausencia en todas las rutas, respuestas o configuraciones del servidor.

### E-005 — Cabecera Set-Cookie con formato no válido

**Estado:** Observado en una captura  
**Prioridad:** Informativa

En una respuesta HTTP 500 se observó una cabecera Set-Cookie cuyo primer campo no presenta la estructura habitual nombre=valor. No se ha identificado su origen ni el efecto en los navegadores.

### E-006 — Diferencias entre cabeceras de respuestas HTTP 500

**Estado:** Observado; impacto no demostrado  
**Prioridad:** Informativa

Las respuestas HTTP 500 conservadas presentan diferencias en cabeceras y huellas. Se registró Content-Length 1507 en determinadas respuestas y una política Cache-Control no-cache en otra. Un POST vacío tuvo 1507 bytes y un hash distinto, pero su cuerpo no se conservó.

## Hipótesis pendientes

H-001: el login inserta `data.mensaje` mediante `.html()`, pero no se ha demostrado que el usuario controle ese mensaje ni que exista XSS.

H-002: el campo `cursoacademico` no tiene regla JavaScript declarada; la respuesta del servidor no permite determinar la validación backend.

## Limitaciones

Sin cuentas de prueba, código fuente ni configuración interna. No se han realizado pruebas DoS ni se ha demostrado modificación de datos.
