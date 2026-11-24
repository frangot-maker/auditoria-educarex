# Metodología de auditoría - PEAD Educarex

## 1. Objetivo

Evaluar, desde una perspectiva de seguridad, la información observable de la aplicación PEAD de Educarex e identificar posibles deficiencias de configuración y exposición de información.

## 2. Alcance

Aplicación objeto de estudio:
- Nombre: Programas Educativos y Atención a la Diversidad (PEAD).
- URL de referencia: https://www.educarex.es/pead/
- Entorno: producción.

La evaluación realizada hasta el momento se limita al análisis de respuestas HTTP previamente recopiladas y de los documentos almacenados localmente.

## 3. Metodología

Se han realizado las siguientes actividades:

- Inspección de respuestas HTTP y códigos de estado.
- Análisis de cabeceras HTTP Set-Cookie.
- Revisión de atributos de seguridad de cookies.
- Revisión de la presencia de cabeceras de seguridad.
- Análisis de una respuesta HTML de error de base de datos.
- Identificación de información técnica expuesta en dicha respuesta.
- Registro y clasificación provisional de hallazgos.

## 4. Herramientas utilizadas

- Kali Linux.
- curl, para las peticiones HTTP previamente realizadas.
- Python 3, para el análisis local de cookies.
- grep, para localizar información técnica en las evidencias.
- cat, para consultar los archivos recopilados.

## 5. Limitaciones

- No se dispone del código fuente de la aplicación.
- No se dispone de cuentas de prueba.
- No se ha tenido acceso a la configuración interna del servidor.
- No se ha confirmado la versión del framework.
- No se han realizado pruebas de explotación.
- No se ha demostrado acceso no autorizado ni extracción de información.
- Los hallazgos relativos a cookies y cabeceras necesitan confirmación adicional.

## 6. Consideraciones

Los resultados reflejan exclusivamente las evidencias recopiladas.

Las observaciones pendientes de verificación no se consideran vulnerabilidades confirmadas.

Cualquier prueba activa adicional sobre producción deberá contar con autorización específica, alcance definido y condiciones de ejecución aprobadas por el responsable del sistema.
