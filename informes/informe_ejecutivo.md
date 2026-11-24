# Informe ejecutivo — Auditoría PEAD Educarex

**Versión 1.1 — 24-11-2026**

## Resultado general

La auditoría ha identificado una exposición confirmada de información
interna en una respuesta de error SQL y varias observaciones de configuración
y comportamiento que requieren revisión técnica.

## Aspectos prioritarios

1. La aplicación expone detalles de una operación SQL, nombres internos
   de tabla y columna, y ruta y línea del modelo.
2. Las cookies de sesión examinadas no muestran determinados atributos
   de protección.
3. Se observó duplicación de cookies, sin demostrar impacto sobre sesiones.
4. Las cabeceras de seguridad indicadas no aparecen en las capturas revisadas.

## Lo que no se ha demostrado

No se ha demostrado SQL injection, XSS, bypass de autenticación,
secuestro de sesión ni acceso no autorizado a información.

## Recomendaciones

- Desactivar la exposición de errores técnicos en producción.
- Revisar la configuración y ciclo de vida de las cookies.
- Revisar la política de cabeceras HTTP.
- Investigar el origen de respuestas HTTP 500 y cabeceras Set-Cookie anómalas.
- Validar las hipótesis pendientes en un entorno y procedimiento controlados.

Las prioridades son provisionales y requieren validación del responsable técnico.
