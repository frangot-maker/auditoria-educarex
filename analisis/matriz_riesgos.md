# Matriz de riesgos — Auditoría PEAD Educarex

**Versión:** 1.1 — 24-11-2026

Las prioridades son provisionales y no constituyen una puntuación CVSS.
Se valora por separado la existencia de una observación y la demostración
de impacto explotable.

| ID | Hallazgo | Estado | Prioridad |
|---|---|---|---|
| E-001 | Divulgación de información interna mediante error SQL | Confirmado en la evidencia conservada | Media provisional |
| E-002 | Atributos de seguridad de cookies no observados | Observado en las respuestas recopiladas; inventario pendiente de consolidación | Baja provisional |
| E-003 | Duplicación de cookies de sesión en una misma respuesta | Reproducido en múltiples respuestas anónimas; impacto no demostrado | Informativa |
| E-004 | Cabeceras de seguridad no observadas | No observadas en las capturas revisadas; alcance limitado | Baja provisional |
| E-005 | Cabecera Set-Cookie con formato no válido | Observado en una captura | Informativa |
| E-006 | Diferencias entre cabeceras de respuestas HTTP 500 | Observado; impacto no demostrado | Informativa |

## Interpretación

- **E-001:** divulgación técnica confirmada en una respuesta conservada.
  No demuestra SQL injection ni acceso a datos.
- **E-002:** atributos no observados en las cookies examinadas; falta
  consolidar todas las respuestas y evaluar el uso real de la cookie.
- **E-003:** duplicación reproducida; no se ha demostrado impacto sobre
  sesiones autenticadas.
- **E-004:** ausencia limitada a las capturas revisadas.
- **E-005:** anomalía de formato observada una vez; impacto desconocido.
- **E-006:** diferencias entre respuestas de error; sin impacto demostrado.

## Hipótesis fuera de la matriz de vulnerabilidades confirmadas

- H-001: posible DOM XSS en el mensaje del login. Sumidero `.html()`
  identificado, pero fuente controlable no demostrada.
- H-002: validación servidor del parámetro `cursoacademico` no concluyente.

## Orden de revisión recomendado

1. Corregir la exposición de errores internos en producción.
2. Revisar la configuración de cookies de sesión.
3. Investigar la causa de la duplicación de cookies.
4. Revisar las políticas de cabeceras HTTP.
5. Identificar el origen de la cabecera Set-Cookie malformada.
6. Revisar la uniformidad de respuestas de error.

## Limitaciones

No se ha demostrado SQL injection, XSS, bypass de autenticación,
secuestro de sesión ni acceso no autorizado. Las prioridades son provisionales.
