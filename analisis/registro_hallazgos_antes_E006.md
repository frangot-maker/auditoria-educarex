# Registro de hallazgos — Auditoría PEAD Educarex

## E-001 — Divulgación de información interna mediante error SQL

**Estado:** Confirmado en la evidencia recopilada.

**Severidad:** Media provisional.

**Evidencia:**
La respuesta HTTP 500 conservada en `evidencias/pead_500.html` muestra:

- Error Number: 1048.
- Mensaje: Column 'login' cannot be null.
- Operación SQL: INSERT.
- Tabla: pead_usuariosacceso0.
- Columna: login.
- Modelo: modules/login/models/Login_model.php.
- Línea: 46.

**Interpretación:**
La aplicación devuelve al cliente información interna sobre una operación SQL y detalles de implementación.

**Impacto potencial:**
Divulgación de información técnica que puede facilitar el reconocimiento de la arquitectura interna.

**Limitaciones:**
No se ha demostrado SQL injection ni acceso no autorizado a la base de datos. La plantilla es compatible visualmente con CodeIgniter, pero no se ha identificado su versión.

**Recomendaciones:**
- Desactivar los errores detallados de base de datos en producción.
- Mostrar mensajes genéricos al usuario.
- Guardar los detalles técnicos en registros protegidos.
- Revisar la validación del campo login antes de ejecutar la operación SQL.

---

## E-002 — Atributos de seguridad de cookies no observados

**Estado:** Observado, pendiente de evaluación de impacto.

**Severidad:** Baja provisional.

**Componente:** PEAD.

**Evidencia:**
En las cinco instancias válidas de la cookie gcprsess recopiladas:

- Secure: no observado (0/5).
- HttpOnly: no observado (0/5).
- SameSite: no declarado.
- Path: /.

**Interpretación:**
Las cabeceras recopiladas no muestran atributos de protección Secure, HttpOnly ni SameSite para gcprsess.

**Impacto potencial:**
Mayor exposición de la cookie ante determinados escenarios de ataque, dependiendo de su función y del contexto de uso.

**Limitaciones:**
No se ha demostrado secuestro de sesión, acceso no autorizado ni explotación. El análisis se limita a las cabeceras conservadas.

**Recomendaciones:**
- Revisar la configuración de las cookies de sesión.
- Establecer Secure cuando la aplicación funcione exclusivamente mediante HTTPS.
- Establecer HttpOnly cuando no sea necesario acceder a la cookie desde JavaScript.
- Configurar una política SameSite adecuada al funcionamiento de la aplicación.

---

## E-003 — Duplicación de cookies de sesión en una misma respuesta

**Estado:** Observado, causa desconocida.

**Componente:** PEAD.

**Evidencia:**
En las respuestas recopiladas se observa:

- HTTP 307: dos cabeceras Set-Cookie con nombre gcprsess.
- Primera respuesta HTTP 500: una cabecera gcprsess válida.
- Segunda respuesta HTTP 500: dos cabeceras Set-Cookie con nombre gcprsess.
- Las instancias observadas utilizan Path=/.

**Interpretación:**
Se observa la emisión de varias cookies con el mismo nombre dentro de una misma respuesta HTTP en dos de las tres respuestas analizadas.

**Impacto potencial:**
Posibles ambigüedades en la gestión de sesiones, dependiendo de cómo se procesen las cookies emitidas.

**Limitaciones:**
No se ha demostrado fijación de sesión, secuestro de sesión ni acceso no autorizado. Se desconoce si la duplicación responde a una regeneración legítima.

**Recomendaciones:**
- Revisar la inicialización y regeneración de sesiones.
- Comprobar la coherencia de las cabeceras Set-Cookie.
- Evitar emitir cookies redundantes o contradictorias.

---

## E-004 — Cabeceras de seguridad no observadas

**Estado:** Pendiente de verificación.

**Severidad:** Baja provisional.

**Componente:** Respuestas HTTP recopiladas.

**Evidencia:**
No aparecen en las respuestas revisadas:

- Strict-Transport-Security.
- Content-Security-Policy.
- X-Frame-Options.
- X-Content-Type-Options.
- Referrer-Policy.

**Interpretación:**
Las cabeceras indicadas no aparecen en el conjunto de respuestas analizado.

**Impacto potencial:**
Menor protección frente a determinados ataques que pueden mitigarse mediante políticas de seguridad del navegador.

**Limitaciones:**
No se ha verificado la configuración global del servidor ni todas las rutas y respuestas de la aplicación.

**Recomendaciones:**
- Revisar las políticas de seguridad HTTP.
- Evaluar qué cabeceras son adecuadas para la aplicación.
- Configurarlas de forma coherente en el servidor o en la aplicación.

---

## E-005 — Cabecera Set-Cookie con formato no válido

**Estado:** Observado en una captura.

**Componente:** PEAD.

**Evidencia:**
En una respuesta HTTP 500 aparece una cabecera Set-Cookie cuyo primer campo no presenta el formato habitual nombre=valor.

**Interpretación:**
La cabecera recopilada presenta una estructura no habitual para una cookie HTTP.

**Impacto potencial:**
Posibles problemas de interpretación o gestión de cookies por parte del cliente.

**Limitaciones:**
No se ha determinado qué componente genera la cabecera ni cómo la interpreta el navegador.

**Recomendaciones:**
- Revisar la generación de cabeceras Set-Cookie.
- Identificar el origen de la cabecera mediante los registros del servidor.
- Comprobar que todas las cookies emitidas cumplen el formato esperado.

---

## Limitaciones generales

- Análisis basado en respuestas HTTP previamente recopiladas.
- No se ha verificado la configuración global del servidor.
- No se ha demostrado SQL injection, secuestro de sesión ni acceso no autorizado.
- No se han realizado pruebas intrusivas sobre el servicio de producción.
- Los hallazgos pendientes requieren confirmación por el responsable técnico o en un entorno de pruebas autorizado.
- Las severidades indicadas son provisionales y deberán revisarse durante la validación técnica.
