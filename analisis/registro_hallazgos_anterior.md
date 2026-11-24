# Auditoría de seguridad - PEAD Educarex

## E-001 - Divulgación de información interna mediante error SQL

**Estado:** Confirmado.

**Evidencia:**
- Respuesta HTTP 500.
- Código de error SQL 1048.
- Columna: login.
- Tabla: pead_usuariosacceso0.
- Modelo: modules/login/models/Login_model.php.
- Línea: 46.
- La respuesta revela una consulta SQL y detalles internos de la aplicación.

**Impacto potencial:**
Divulgación de información técnica que facilita el reconocimiento de la arquitectura interna.

**Recomendación:**
Desactivar la visualización de errores SQL en producción y registrar los detalles exclusivamente en logs internos.

## E-002 - Atributos de seguridad de cookies no observados

**Estado:** Pendiente de verificación.

**Evidencia:**
En las cabeceras recopiladas no aparecen los atributos Secure, HttpOnly ni SameSite para gcprsess.

**Impacto potencial:**
Mayor exposición de la cookie ante determinados escenarios de ataque.

**Recomendación:**
Revisar la configuración de cookies de sesión y establecer Secure, HttpOnly y una política SameSite adecuada.

## E-003 - Posible duplicidad de cookies de sesión

**Estado:** Observado, causa desconocida.

**Evidencia:**
Se registraron varias cabeceras Set-Cookie con el nombre gcprsess en distintas respuestas.

**Impacto potencial:**
Posibles ambigüedades en la gestión de sesiones.

**Recomendación:**
Revisar la inicialización, regeneración y eliminación de sesiones en la aplicación.

## E-004 - Cabeceras de seguridad no observadas

**Estado:** Pendiente de verificación.

**Evidencia:**
No aparecen en las respuestas recopiladas:
- Strict-Transport-Security.
- Content-Security-Policy.
- X-Frame-Options.
- X-Content-Type-Options.
- Referrer-Policy.

**Impacto potencial:**
Menor protección frente a determinados ataques del navegador.

**Recomendación:**
Revisar las políticas de seguridad HTTP y configurar las cabeceras adecuadas según la aplicación.

## Limitaciones generales

- Análisis basado en respuestas HTTP previamente recopiladas.
- No se ha verificado la configuración global del servidor.
- No se ha demostrado SQL injection, secuestro de sesión ni acceso no autorizado.
- Los hallazgos pendientes requieren confirmación por el responsable técnico o en un entorno de pruebas autorizado.

## Ampliación de evidencias de E-001

### Información técnica adicional

La respuesta HTML conservada presenta:
- Título: Error en Base de Datos.
- Mensaje: A Database Error Occurred.
- Código SQL: 1048.
- Operación: INSERT.
- Tabla: pead_usuariosacceso0.
- Columna no nula: login.
- Modelo: modules/login/models/Login_model.php.
- Línea: 46.
- Recurso gráfico: /pead/pub/imgs/error-ico.png.

### Observaciones

La plantilla presenta elementos visuales compatibles con páginas de error de CodeIgniter. No se ha determinado la versión del framework.

La aplicación expone una consulta SQL y detalles de implementación en una respuesta HTTP visible para el cliente.

No hay evidencia suficiente para afirmar que exista una vulnerabilidad de inyección SQL.

### Recomendaciones adicionales

- Desactivar los errores detallados de base de datos en producción.
- Mostrar al usuario un mensaje genérico y un identificador de incidencia.
- Guardar la excepción completa en logs protegidos.
- Revisar el flujo que permite intentar registrar un acceso con login NULL.
- Comprobar que los campos obligatorios se validan antes de ejecutar operaciones SQL.

---

## E-003 — Duplicación de cookies de sesión en una misma respuesta

**Estado:** Observado, causa desconocida.

**Componente:** PEAD.

**Evidencia recopilada:**
- Respuesta HTTP 307: dos cabeceras Set-Cookie con nombre gcprsess.
- Primera respuesta HTTP 500: una cabecera gcprsess válida.
- Segunda respuesta HTTP 500: dos cabeceras Set-Cookie con nombre gcprsess.
- Las instancias observadas utilizan Path=/.

**Interpretación:**
Se observa la emisión de varias cookies con el mismo nombre dentro de una misma respuesta HTTP. Es necesario determinar si se trata de una regeneración legítima de sesión o de un comportamiento incorrecto de la aplicación.

**Limitaciones:**
No se ha demostrado fijación de sesión, secuestro de sesión ni acceso no autorizado.

**Recomendación:**
Revisar la generación y renovación de identificadores de sesión y evitar emitir cookies redundantes o contradictorias.

---

## E-005 — Cabecera Set-Cookie con formato no válido

**Estado:** Observado en una captura.

**Componente:** PEAD.

**Evidencia recopilada:**
En una respuesta HTTP 500 aparece una cabecera Set-Cookie cuyo primer campo no contiene el formato nombre=valor.

**Interpretación:**
La cabecera no presenta la estructura habitual de una cookie HTTP.

**Limitaciones:**
No se ha determinado qué componente genera la cabecera ni cómo la interpreta el navegador.

**Recomendación:**
Revisar la generación de cabeceras Set-Cookie y los registros del servidor para identificar el origen.
