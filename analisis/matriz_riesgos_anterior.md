# Matriz de riesgos - Auditoría PEAD Educarex

## Criterios de valoración

- Alto: evidencia de un problema con impacto relevante y confirmado.
- Medio: deficiencia confirmada o indicio con impacto potencial que requiere más comprobaciones.
- Bajo: observación de impacto limitado o pendiente de determinar.
- Informativo: observación técnica sin impacto de seguridad demostrado.

Las valoraciones son provisionales y no equivalen a puntuaciones CVSS.

## Matriz de hallazgos

| ID | Hallazgo | Estado | Prioridad provisional |
|---|---|---|---|
| E-001 | Divulgación de información interna mediante error SQL | Confirmado | Media |
| E-002 | Atributos de seguridad de cookies no observados | Pendiente de verificación | Baja |
| E-003 | Posible duplicidad de cookies de sesión | Observado | Informativa |
| E-004 | Cabeceras de seguridad no observadas | Pendiente de verificación | Baja |

## Justificación y medidas correctoras

### E-001 - Divulgación de información interna

Prioridad: Media.

Justificación:
La respuesta HTTP 500 revela información de base de datos, estructura interna, nombre de tabla, columna, modelo y línea de código.

Medidas:
- Desactivar la visualización de errores detallados en producción.
- Mostrar mensajes genéricos al usuario.
- Mantener logs internos protegidos.
- Revisar la validación del campo login.

### E-002 - Atributos de seguridad de cookies

Prioridad: Baja, pendiente de verificación.

Justificación:
En las cabeceras recopiladas no aparecen Secure, HttpOnly ni SameSite.

Medidas:
- Revisar la configuración de las cookies de sesión.
- Aplicar Secure en conexiones HTTPS.
- Aplicar HttpOnly.
- Definir una política SameSite adecuada.

### E-003 - Posible duplicidad de cookies

Prioridad: Informativa.

Justificación:
Se han observado varias cabeceras Set-Cookie con el nombre gcprsess. No se ha determinado si responden a una regeneración legítima de sesión o a un error de configuración.

Medidas:
- Revisar la inicialización y regeneración de sesiones.
- Comprobar que no se emitan cookies contradictorias.
- Revisar la eliminación y renovación de sesiones.

### E-004 - Cabeceras de seguridad

Prioridad: Baja, pendiente de verificación.

Justificación:
Las cabeceras Strict-Transport-Security, Content-Security-Policy, X-Frame-Options, X-Content-Type-Options y Referrer-Policy no aparecen en los fragmentos recopilados.

Medidas:
- Revisar las cabeceras emitidas por servidor y aplicación.
- Configurar HSTS cuando corresponda.
- Definir una política CSP compatible con la aplicación.
- Configurar protección contra MIME sniffing y framing.
- Establecer una política de referencia adecuada.

## Orden recomendado de actuación

1. Corregir la exposición de errores SQL en producción.
2. Revisar la configuración de cookies de sesión.
3. Investigar la duplicidad de cookies.
4. Verificar y completar las cabeceras de seguridad.

## Limitaciones

La matriz se basa en evidencias parciales. Las prioridades deberán revisarse cuando el responsable técnico confirme la configuración real y el impacto de cada observación.
