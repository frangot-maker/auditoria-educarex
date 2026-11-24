# Registro de hallazgos — Auditoría PEAD Educarex
**Versión:** 1.1  
**Actualización:** 24-11-2026

## E-001 — Divulgación de información interna mediante error SQL

**Estado:** Confirmado en la evidencia conservada  
**Prioridad provisional:** Media provisional

**Descripción:** La respuesta HTTP 500 conservada expone el error SQL 1048, la columna login, la tabla pead_usuariosacceso0, una sentencia INSERT y la ruta y línea del modelo. También se observaron respuestas HTTP 500 ante HEAD y OPTIONS en el endpoint de login. En OPTIONS se observó una plantilla de error de base de datos, pero no se confirmó que contuviera exactamente el mismo error SQL.

**Evidencia estructurada:**

```json
{
  "archivo_principal": "evidencias/pead_500.html",
  "codigo_sql": "1048",
  "columna": "login",
  "tabla": "pead_usuariosacceso0",
  "archivo_fuente_expuesto": "modules/login/models/Login_model.php",
  "linea": 46,
  "head": "HTTP 500 observado; cuerpo no conservado",
  "options": "HTTP 500; plantilla de error DB observada parcialmente"
}
```

**Limitación:** no debe inferirse un impacto no demostrado a partir de la observación técnica.

---

## E-002 — Atributos de seguridad de cookies no observados

**Estado:** Observado en las respuestas recopiladas; inventario pendiente de consolidación  
**Prioridad provisional:** Baja provisional

**Descripción:** Las instancias gcprsess examinadas no muestran Secure, HttpOnly ni SameSite. El recuento inicial fue de cinco instancias válidas; se recopilaron respuestas adicionales posteriormente, por lo que el total definitivo debe recalcularse desde las cabeceras redactadas.

**Evidencia estructurada:**

```json
{
  "cookie": "gcprsess",
  "recuento_inicial": 5,
  "secure": "No observado",
  "httponly": "No observado",
  "samesite": "No declarado",
  "limitacion": "No se ha consolidado el total de todas las respuestas"
}
```

**Limitación:** no debe inferirse un impacto no demostrado a partir de la observación técnica.

---

## E-003 — Duplicación de cookies de sesión en una misma respuesta

**Estado:** Reproducido en múltiples respuestas anónimas; impacto no demostrado  
**Prioridad provisional:** Informativa

**Descripción:** Se observaron varias cabeceras Set-Cookie con nombre gcprsess en múltiples respuestas HTML de PEAD. Las cookies propias se probaron individualmente y en conjunto; las páginas públicas mantuvieron el mismo contenido y las rutas protegidas redirigieron al acceso. No se demostró bypass, fijación ni secuestro de sesión.

**Evidencia estructurada:**

```json
{
  "cookie": "gcprsess",
  "observacion": "Duplicación en respuestas HTML",
  "prueba_individual_y_conjunta": "Realizada con cookies anónimas propias",
  "resultado_acceso": "Redirección al login",
  "impacto": "No demostrado"
}
```

**Limitación:** no debe inferirse un impacto no demostrado a partir de la observación técnica.

---

## E-004 — Cabeceras de seguridad no observadas

**Estado:** No observadas en las capturas revisadas; alcance limitado  
**Prioridad provisional:** Baja provisional

**Descripción:** Las capturas revisadas no muestran determinadas cabeceras de seguridad. Esto no demuestra su ausencia en todas las rutas, respuestas o configuraciones del servidor.

**Evidencia estructurada:**

```json
[
  "Strict-Transport-Security",
  "Content-Security-Policy",
  "X-Frame-Options",
  "X-Content-Type-Options",
  "Referrer-Policy",
  "Permissions-Policy",
  "Cross-Origin-Opener-Policy",
  "Cross-Origin-Resource-Policy",
  "Cross-Origin-Embedder-Policy"
]
```

**Limitación:** no debe inferirse un impacto no demostrado a partir de la observación técnica.

---

## E-005 — Cabecera Set-Cookie con formato no válido

**Estado:** Observado en una captura  
**Prioridad provisional:** Informativa

**Descripción:** En una respuesta HTTP 500 se observó una cabecera Set-Cookie cuyo primer campo no presenta la estructura habitual nombre=valor. No se ha identificado su origen ni el efecto en los navegadores.

**Evidencia estructurada:**

```json
{
  "archivo": "analisis/cabeceras.txt",
  "observacion": "Campo inicial de Set-Cookie malformado",
  "limitacion": "Origen y efecto no determinados"
}
```

**Limitación:** no debe inferirse un impacto no demostrado a partir de la observación técnica.

---

## E-006 — Diferencias entre cabeceras de respuestas HTTP 500

**Estado:** Observado; impacto no demostrado  
**Prioridad provisional:** Informativa

**Descripción:** Las respuestas HTTP 500 conservadas presentan diferencias en cabeceras y huellas. Se registró Content-Length 1507 en determinadas respuestas y una política Cache-Control no-cache en otra. Un POST vacío tuvo 1507 bytes y un hash distinto, pero su cuerpo no se conservó.

**Evidencia estructurada:**

```json
{
  "content_length_observado": 1507,
  "cache_control_observado": "max-age=0, no-cache, no-store, must-revalidate",
  "post_vacio": "HTTP 500; cuerpo no conservado",
  "impacto": "No demostrado"
}
```

**Limitación:** no debe inferirse un impacto no demostrado a partir de la observación técnica.

---

## Hipótesis pendientes de confirmación

### H-001 — Posible DOM XSS en el login

El archivo `evidencias/nuevas/login.js` inserta `data.mensaje` mediante
`.html()`. El sumidero está identificado, pero no se ha demostrado que
una entrada anónima controle el mensaje ni que exista ejecución de código
en PEAD. No se clasifica como vulnerabilidad confirmada.

### H-002 — Validación del parámetro cursoacademico

El formulario no declara una regla JavaScript para este campo. La respuesta
del servidor a un curso ficticio fue el mismo rechazo genérico de credenciales.
El comportamiento no permite concluir si la validación del servidor es correcta.

## Pruebas negativas relevantes

- Credenciales ficticias rechazadas.
- Marcadores enviados no reflejados en las respuestas JSON examinadas.
- Cookies anónimas propias no permitieron acceder a rutas protegidas.
- Rutas administrativas probadas redirigieron al login.
- No se ha demostrado SQL injection, XSS, bypass ni secuestro de sesión.

## Limitaciones generales

- No se dispone de cuentas de prueba, código fuente ni configuración interna.
- No se ha confirmado la versión del framework.
- El recuento total de cookies debe consolidarse.
- Los resultados describen únicamente las respuestas y recursos efectivamente examinados.
