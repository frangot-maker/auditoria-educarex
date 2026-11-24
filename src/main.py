
#!/usr/bin/env python3
# Framework de auditoría web - versión 1.0
# Analiza exclusivamente evidencias locales. No realiza conexiones de red.

import csv
import json
import hashlib
import re
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent.parent
HEADERS_FILE = BASE / "analisis" / "cabeceras.txt"
HTML_FILE = BASE / "evidencias" / "pead_500.html"
OUTPUT = BASE / "resultados"

OUTPUT.mkdir(parents=True, exist_ok=True)

findings = []
evidence_hashes = []


def sha256_file(path):
    """Calcula el SHA-256 de un archivo local."""
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            digest.update(chunk)

    return digest.hexdigest()


def register_evidence(path):
    """Registra la integridad de una evidencia existente."""
    if not path.exists():
        print(f"[!] No encontrada: {path}")
        return None

    digest = sha256_file(path)

    evidence_hashes.append({
        "archivo": str(path.relative_to(BASE)),
        "sha256": digest,
        "bytes": path.stat().st_size
    })

    return path.read_text(encoding="utf-8", errors="replace")


def add_finding(code, title, status, severity, description, evidence):
    findings.append({
        "id": code,
        "titulo": title,
        "estado": status,
        "prioridad": severity,
        "descripcion": description,
        "evidencia": evidence
    })


def analyze_headers(content):
    """Analiza cabeceras ya recopiladas, sin realizar peticiones."""

    if not content:
        return

    blocks = re.split(r"(?=^HTTP/)", content, flags=re.MULTILINE)
    security_headers = [
        "strict-transport-security",
        "content-security-policy",
        "x-frame-options",
        "x-content-type-options",
        "referrer-policy"
    ]

    observed = set()
    cookie_names = {}
    malformed_cookies = 0
    cookie_instances = 0

    for block_number, block in enumerate(blocks, start=1):
        if not block.strip():
            continue

        response_headers = {}

        for line in block.splitlines():
            if ":" not in line:
                continue

            name, value = line.split(":", 1)
            name = name.strip().lower()
            value = value.strip()

            response_headers.setdefault(name, []).append(value)

            if name in security_headers:
                observed.add(name)

            if name == "set-cookie":
                cookie_instances += 1

                # Solo se conserva el nombre de la cookie.
                # Nunca se exportan sus valores.
                first_part = value.split(";", 1)[0]

                if "=" not in first_part:
                    malformed_cookies += 1
                    continue

                cookie_name = first_part.split("=", 1)[0].strip()

                if not cookie_name:
                    malformed_cookies += 1
                    continue

                cookie_names.setdefault(cookie_name, 0)
                cookie_names[cookie_name] += 1

                attributes = {
                    part.strip().split("=", 1)[0].lower()
                    for part in value.split(";")[1:]
                    if part.strip()
                }

                print(
                    f"  Cookie {cookie_name}: "
                    f"Secure={'secure' in attributes}, "
                    f"HttpOnly={'httponly' in attributes}, "
                    f"SameSite={'samesite' in attributes}"
                )

    missing = sorted(set(security_headers) - observed)

    if missing:
        add_finding(
            "E-004",
            "Cabeceras de seguridad no observadas",
            "Pendiente de verificación",
            "Baja provisional",
            "Las siguientes cabeceras no aparecen en el archivo "
            "de cabeceras recopiladas. No implica que falten "
            "en todas las respuestas del servidor.",
            missing
        )

    if cookie_names:
        add_finding(
            "E-002",
            "Atributos de seguridad de cookies",
            "Pendiente de verificación",
            "Baja provisional",
            "Se han registrado cookies. Debe revisarse la presencia "
            "de Secure, HttpOnly y SameSite en respuestas completas.",
            {
                "nombres": sorted(cookie_names.keys()),
                "instancias": cookie_instances
            }
        )

    duplicates = [
        name for name, count in cookie_names.items()
        if count > 1
    ]

    if duplicates:
        add_finding(
            "E-003",
            "Posible duplicidad de cookies",
            "Observado, causa desconocida",
            "Informativa",
            "Se repiten nombres de cookies en el conjunto de "
            "respuestas. Es necesario distinguir regeneraciones "
            "legítimas de posibles errores de configuración.",
            duplicates
        )

    if malformed_cookies:
        print(
            f"[!] Cabeceras Set-Cookie incompletas o mal formadas: "
            f"{malformed_cookies}"
        )


def analyze_html(content):
    """Busca errores internos en el HTML local."""

    if not content:
        return

    patterns = {
        "codigo_sql": r"Error Number:\s*(\d+)",
        "columna": r"Column ['\"]([^'\"]+)['\"] cannot be null",
        "tabla": r"INSERT INTO [`\"]?([a-zA-Z0-9_]+)",
        "archivo": r"Filename:\s*([^<]+)",
        "linea": r"Line Number:\s*(\d+)"
    }

    evidence = {}

    for key, pattern in patterns.items():
        match = re.search(pattern, content, re.IGNORECASE)

        if match:
            evidence[key] = match.group(1).strip()

    if evidence:
        add_finding(
            "E-001",
            "Divulgación de información interna mediante error SQL",
            "Confirmado en la evidencia recopilada",
            "Media provisional",
            "La página de error muestra información interna "
            "de la base de datos y de la implementación.",
            evidence
        )


def export_results():
    """Genera JSON, CSV y hashes de las evidencias."""

    report = {
        "proyecto": "Auditoria PEAD Educarex",
        "version": "1.0",
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
        "modo": "analisis_local_sin_conexiones",
        "hallazgos": findings,
        "evidencias": evidence_hashes
    }

    json_path = OUTPUT / "resultados.json"

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    csv_path = OUTPUT / "resultados.csv"

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "id", "titulo", "estado",
                "prioridad", "descripcion", "evidencia"
            ]
        )

        writer.writeheader()

        for finding in findings:
            row = finding.copy()
            row["evidencia"] = json.dumps(
                row["evidencia"], ensure_ascii=False
            )
            writer.writerow(row)

    hash_path = OUTPUT / "hashes.sha256"

    with hash_path.open("w", encoding="utf-8") as file:
        for item in evidence_hashes:
            file.write(
                f'{item["sha256"]}  {item["archivo"]}\n'
            )

    print("\n===== RESULTADOS GENERADOS =====")
    print(f"Hallazgos: {len(findings)}")
    print(f"JSON: {json_path.relative_to(BASE)}")
    print(f"CSV: {csv_path.relative_to(BASE)}")
    print(f"Hashes: {hash_path.relative_to(BASE)}")


def main():
    print("=" * 55)
    print(" FRAMEWORK DE AUDITORIA WEB - PEAD")
    print(" Analisis local de evidencias - Version 1.0")
    print("=" * 55)

    print("\n[1] Registrando evidencias...")

    headers = register_evidence(HEADERS_FILE)
    html = register_evidence(HTML_FILE)

    print("\n[2] Analizando cabeceras y cookies...")
    analyze_headers(headers)

    print("\n[3] Analizando errores HTML...")
    analyze_html(html)

    print("\n[4] Exportando resultados...")
    export_results()

    print("\n===== RESUMEN =====")

    for finding in findings:
        print(
            f'{finding["id"]} | {finding["prioridad"]} | '
            f'{finding["titulo"]}'
        )

    print("\nAnálisis finalizado.")


if __name__ == "__main__":
    main()
