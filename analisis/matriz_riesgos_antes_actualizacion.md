# Matriz de riesgos - Auditoría PEAD Educarex

## Criterios de valoración

- Alto: problema con impacto relevante y confirmado.
- Medio: deficiencia confirmada o indicio con impacto potencial.
- Bajo: observación de impacto limitado o pendiente de determinar.
- Informativo: observación técnica sin impacto de seguridad demostrado.

Las valoraciones son provisionales y no equivalen a puntuaciones CVSS.

## Matriz de hallazgos

| ID | Hallazgo | Estado | Prioridad provisional |
|---|---|---|---|
| E-001 | Divulgación de información interna mediante error SQL | Confirmado en evidencia | Media |
| E-002 | Ausencia de atributos de seguridad en cookies | Observado en 5 instancias | Baja |
| E-003 | Duplicación de cookies de sesión | Observado en 2 respuestas | Informativa |
| E-004 | Cabeceras HTTP de seguridad no observadas | Observado en capturas | Baja |
| E-005 | Cabecera Set-Cookie malformada | Observado en 1 respuesta | Informativa |
| E-006 | Diferencias entre cabeceras de respuestas HTTP 500 | Observado | Informativa |

## Justificación y medidas correctoras

### E-001 - Divulgación de información interna mediante error SQL

Prioridad: Media provisional.

La respuesta HTTP 500 revela código de error SQL, consulta ejecutada, nombre de tabla, columna, ruta del modelo y número de línea.

Medidas:
- Desactivar la visualización de errores detallados en producción.
- Mostrar mensajes genéricos al usuario.
- Mantener registros internos protegidos.
- Revisar la validación del campo login.

### E-002 - Ausencia de atributos de seguridad en cookies

Prioridad: Baja provisional.

Las cinco instancias válidas de gcprsess no presentan Secure, HttpOnly ni SameSite.

Medidas:
- Revisar la configuración de las cookies de sesión.
- Aplicar Secure cuando la aplicación funcione exclusivamente mediante HTTPS.
- Aplicar HttpOnly cuando no se requiera acceso desde JavaScript.
- Definir una política SameSite adecuada al funcionamiento de la aplicación.

### E-003 - Duplicación de cookies de sesión

Prioridad: Informativa.

Se observan dos cookies gcprsess en una respuesta HTTP 307 y en una de las respuestas HTTP 500. No se ha determinado su causa ni demostrado impacto sobre la seguridad de las sesiones.

Medidas:
- Revisar la inicialización y regeneración de sesiones.
- Comprobar que no se emitan cookies contradictorias.
- Revisar la eliminación y renovación de sesiones.

### E-004 - Cabeceras HTTP de seguridad no observadas

Prioridad: Baja provisional.

No se observan las siguientes cabeceras en las capturas analizadas:

- Strict-Transport-Security
- Content-Security-Policy
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy
- Permissions-Policy
- Cross-Origin-Opener-Policy
- Cross-Origin-Resource-Policy
- Cross-Origin-Embedder-Policy

Esto no demuestra que estén ausentes en todas las respuestas del servidor.

Medidas:
- Revisar las cabeceras emitidas por servidor y aplicación.
- Configurar HSTS cuando corresponda.
- Definir una política CSP compatible con la aplicación.
- Configurar protección contra MIME sniffing y framing.
- Establecer políticas de referencia y aislamiento adecuadas.

### E-005 - Cabecera Set-Cookie malformada

Prioridad: Informativa.

En una respuesta HTTP 500 se observa una cabecera Set-Cookie cuyo primer campo no presenta la estructura habitual nombre=valor.

No se ha identificado el componente que genera la cabecera ni su impacto en el navegador.

Medidas:
- Revisar la generación de cabeceras Set-Cookie.
- Comprobar la configuración del componente responsable.
- Evitar la emisión de cabeceras malformadas.

### E-006 - Diferencias entre cabeceras de respuestas HTTP 500

Prioridad: Informativa.

Las dos respuestas HTTP 500 conservadas presentan diferencias en sus cabeceras. Una incluye Content-Length: 1507 y la otra Cache-Control: max-age=0, no-cache, no-store, must-revalidate.

No se ha demostrado un impacto de seguridad.

Medidas:
- Revisar la uniformidad de las cabeceras de las respuestas de error.
- Aplicar políticas de caché coherentes cuando corresponda.

## Orden recomendado de actuación

1. Corregir la exposición de errores SQL en producción.
2. Revisar los atributos de seguridad de las cookies.
3. Investigar la duplicación de cookies.
4. Revisar las cabeceras HTTP de seguridad.
5. Corregir la generación de cabeceras Set-Cookie.
6. Unificar las políticas de respuesta de error.

## Limitaciones

- Análisis basado en evidencias previamente recopiladas.
- No se ha verificado la configuración global del servidor.
- No se ha demostrado explotación ni secuestro de sesión.
- No se ha comprobado el comportamiento de todas las rutas y respuestas.
- Las prioridades son provisionales y requieren validación del responsable técnico.
