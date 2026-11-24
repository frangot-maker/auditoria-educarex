# Metodología de auditoría — PEAD Educarex

## 1. Objetivo y alcance

Aplicación: Programas Educativos y Atención a la Diversidad (PEAD).  
URL: https://www.educarex.es/pead/  
Entorno: producción.

La evaluación combina reconocimiento y peticiones HTTP activas de baja
intensidad con análisis local de respuestas, HTML, JavaScript, CSS y evidencias.

## 2. Actividades realizadas

- Inspección de respuestas HTTP y códigos de estado.
- Peticiones GET, HEAD y OPTIONS sobre recursos de la aplicación.
- Pruebas POST de autenticación con datos ficticios.
- Análisis de cabeceras HTTP y cookies `gcprsess`.
- Comprobación de cookies anónimas propias en páginas públicas y rutas protegidas.
- Análisis de HTML, formulario de login y JavaScript asociado.
- Revisión de fuentes y sumideros DOM.
- Inspección de versiones declaradas o identificables en recursos públicos.
- Análisis de respuestas de error y hashes de evidencias.
- Registro de resultados positivos, negativos y limitaciones.

## 3. Herramientas

Kali Linux, curl, Python 3, SQLite, grep, sha256sum y herramientas
estándar de inspección de archivos.

## 4. Pruebas y resultados negativos

Las credenciales ficticias fueron rechazadas. Los marcadores examinados
no aparecieron en las respuestas JSON conservadas. Las cookies anónimas
propias no permitieron acceder a las rutas protegidas probadas.

La presencia de `.html()` en el código JavaScript identifica un sumidero
HTML potencial, pero no demuestra por sí sola XSS. No se ha demostrado
SQL injection, bypass de autenticación ni secuestro de sesión.

## 5. Restricciones y limitaciones observadas

No se dispone de cuentas de prueba, código fuente ni configuración interna.
No se ha confirmado la versión del framework. No se han realizado pruebas
DoS. No se ha demostrado modificación de datos ni extracción de información.
El recuento global de cookies aún requiere consolidación.

## 6. Gestión de evidencias

Las evidencias conservadas se identifican mediante SHA-256 y tamaño.
Los valores de cookies, tokens y otros identificadores de sesión deben
mantenerse redactados en informes compartidos. Las evidencias originales
no deben modificarse.

## 7. Interpretación

Los hallazgos confirmados describen únicamente lo que prueban las evidencias.
Las hipótesis pendientes se mantienen separadas y no se presentan como
vulnerabilidades confirmadas.
