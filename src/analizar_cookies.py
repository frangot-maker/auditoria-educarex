import re
import json
from collections import defaultdict, Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

ARCHIVOS = {
    "PEAD": BASE / "analisis" / "cabeceras.txt",
    "PORTADA": BASE / "evidencias" / "procesadas" / "cabeceras_portada.txt",
}

PATRON_NOMBRE = re.compile(r"[!#$%&'*+\-.^_`|~0-9A-Za-z]+")


def separar_respuestas(contenido):
    """
    Separa las respuestas HTTP.
    Si el archivo es un fragmento procesado sin líneas HTTP,
    lo trata como una única unidad de análisis.
    """
    bloques = re.split(
        r"(?=^HTTP/\S+\s+\d+)",
        contenido,
        flags=re.MULTILINE
    )

    bloques = [b for b in bloques if b.strip()]

    return bloques or [contenido]


def analizar_cookie(linea):
    """
    Extrae únicamente nombre y atributos.
    Nunca conserva el valor de la cookie.
    """
    contenido = linea.split(":", 1)[1].strip()
    partes = [p.strip() for p in contenido.split(";")]

    if not partes or "=" not in partes[0]:
        return None

    nombre, _ = partes[0].split("=", 1)
    nombre = nombre.strip()

    if not PATRON_NOMBRE.fullmatch(nombre):
        return None

    atributos = {}

    for parte in partes[1:]:
        if not parte:
            continue

        if "=" in parte:
            clave, valor = parte.split("=", 1)
            atributos[clave.strip().lower()] = valor.strip()
        else:
            atributos[parte.strip().lower()] = True

    return {
        "nombre": nombre,
        "secure": "secure" in atributos,
        "httponly": "httponly" in atributos,
        "samesite": atributos.get("samesite", "No declarado"),
        "path": atributos.get("path", "No declarado"),
        "max_age": atributos.get("max-age", "No declarado"),
    }


def analizar_archivo(componente, ruta):
    resultado = {
        "componente": componente,
        "archivo": str(ruta.relative_to(BASE)),
        "respuestas_analizadas": 0,
        "cookies": {},
        "respuestas": [],
        "cabeceras_malformadas": 0,
        "total_validas": 0,
    }

    if not ruta.exists():
        resultado["error"] = "Archivo no encontrado"
        return resultado

    contenido = ruta.read_text(
        encoding="utf-8",
        errors="replace"
    )

    bloques = separar_respuestas(contenido)
    agregados = defaultdict(lambda: {
        "instancias": 0,
        "secure": 0,
        "httponly": 0,
        "samesite": [],
        "path": [],
        "max_age": [],
        "respuestas": [],
        "duplicada_en_alguna_respuesta": False,
    })

    for numero, bloque in enumerate(bloques, 1):
        estado = re.search(
            r"^HTTP/\S+\s+(\d+)",
            bloque,
            re.MULTILINE
        )

        codigo = estado.group(1) if estado else "No identificado"

        cookies_respuesta = []
        conteo_nombres = Counter()

        for linea in bloque.splitlines():
            if not linea.lower().startswith("set-cookie:"):
                continue

            cookie = analizar_cookie(linea)

            if cookie is None:
                resultado["cabeceras_malformadas"] += 1
                continue

            cookies_respuesta.append(cookie)
            conteo_nombres[cookie["nombre"]] += 1
            resultado["total_validas"] += 1

            datos = agregados[cookie["nombre"]]
            datos["instancias"] += 1
            datos["secure"] += int(cookie["secure"])
            datos["httponly"] += int(cookie["httponly"])
            datos["samesite"].append(cookie["samesite"])
            datos["path"].append(cookie["path"])
            datos["max_age"].append(cookie["max_age"])

            if numero not in datos["respuestas"]:
                datos["respuestas"].append(numero)

        # Detectar duplicados únicamente dentro de esta respuesta.
        duplicadas = {
            nombre: cantidad
            for nombre, cantidad in conteo_nombres.items()
            if cantidad > 1
        }

        for nombre in duplicadas:
            agregados[nombre]["duplicada_en_alguna_respuesta"] = True

        resultado["respuestas"].append({
            "numero": numero,
            "estado_http": codigo,
            "total_cookies_validas": len(cookies_respuesta),
            "cabeceras_malformadas": (
                sum(
                    1 for linea in bloque.splitlines()
                    if linea.lower().startswith("set-cookie:")
                ) - len(cookies_respuesta)
            ),
            "duplicadas": duplicadas,
            "cookies": cookies_respuesta,
        })

    resultado["respuestas_analizadas"] = len(resultado["respuestas"])

    for nombre, datos in agregados.items():
        resultado["cookies"][nombre] = {
            **datos,
            "secure_ausente_en_todas": datos["secure"] == 0,
            "httponly_ausente_en_todas": datos["httponly"] == 0,
            "samesite_ausente_en_todas": all(
                str(v).lower() == "no declarado"
                for v in datos["samesite"]
            ),
        }

    return resultado


def main():
    print("=" * 60)
    print(" ANALIZADOR LOCAL DE COOKIES - VERSION 2")
    print("=" * 60)

    resultados = []

    for componente, ruta in ARCHIVOS.items():
        datos = analizar_archivo(componente, ruta)
        resultados.append(datos)

        print(f"\n===== {componente} =====")

        if "error" in datos:
            print("[ERROR]", datos["error"])
            continue

        print("Respuestas analizadas:", datos["respuestas_analizadas"])
        print("Cookies válidas:", datos["total_validas"])
        print("Cabeceras malformadas:", datos["cabeceras_malformadas"])

        for respuesta in datos["respuestas"]:
            print(
                f"\nHTTP {respuesta['estado_http']} "
                f"| Respuesta {respuesta['numero']}"
            )
            print("Cookies válidas:", respuesta["total_cookies_validas"])
            print("Cabeceras malformadas:", respuesta["cabeceras_malformadas"])

            if respuesta["duplicadas"]:
                print("Duplicados dentro de esta respuesta:",
                      respuesta["duplicadas"])
            else:
                print("Duplicados dentro de esta respuesta: Ninguno")

            for cookie in respuesta["cookies"]:
                print("  Nombre:", cookie["nombre"])
                print("    Secure:", cookie["secure"])
                print("    HttpOnly:", cookie["httponly"])
                print("    SameSite:", cookie["samesite"])
                print("    Path:", cookie["path"])
                print("    Max-Age:", cookie["max_age"])

        print("\nResumen por nombre de cookie:")

        for nombre, cookie in datos["cookies"].items():
            print(f"\n  {nombre}")
            print("    Instancias:", cookie["instancias"])
            print("    Secure:", cookie["secure"], "/", cookie["instancias"])
            print("    HttpOnly:", cookie["httponly"], "/", cookie["instancias"])
            print("    SameSite:", cookie["samesite"])
            print("    Path:", cookie["path"])
            print("    Max-Age:", cookie["max_age"])
            print(
                "    Duplicada en alguna respuesta:",
                cookie["duplicada_en_alguna_respuesta"]
            )

    salida = BASE / "resultados" / "analisis_cookies.json"
    salida.parent.mkdir(exist_ok=True)

    salida.write_text(
        json.dumps(resultados, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print("\n[OK] Resultado guardado en:",
          salida.relative_to(BASE))
    print("[OK] No se han almacenado valores de cookies.")


if __name__ == "__main__":
    main()
