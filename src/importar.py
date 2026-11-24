import json
import sqlite3
import hashlib
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
JSON_FILE = BASE / "resultados" / "resultados.json"
DB_FILE = BASE / "resultados" / "auditoria.db"

def calcular_sha256(ruta):
    sha = hashlib.sha256()
    with open(ruta, "rb") as archivo:
        for bloque in iter(lambda: archivo.read(65536), b""):
            sha.update(bloque)
    return sha.hexdigest()

def main():
    if not JSON_FILE.exists():
        raise FileNotFoundError(f"No existe {JSON_FILE}")

    with open(JSON_FILE, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    print("===== IMPORTADOR DE AUDITORÍAS =====")
    print("Proyecto:", datos["proyecto"])
    print("Versión:", datos["version"])
    print("Hallazgos:", len(datos["hallazgos"]))
    print("Evidencias:", len(datos["evidencias"]))

    # Verificar la integridad de los archivos antes de importarlos.
    for evidencia in datos["evidencias"]:
        ruta = BASE / evidencia["archivo"]

        if not ruta.is_file():
            raise FileNotFoundError(f"No se encuentra la evidencia: {ruta}")

        sha_real = calcular_sha256(ruta)

        if sha_real != evidencia["sha256"]:
            raise ValueError(
                f"El SHA-256 no coincide para {evidencia['archivo']}. "
                "No se importará la auditoría."
            )

        print(f"[OK] Integridad verificada: {evidencia['archivo']}")

    db = sqlite3.connect(DB_FILE)
    db.execute("PRAGMA foreign_keys = ON")

    try:
        with db:
            proyecto = db.execute(
                "SELECT id FROM projects WHERE name = ? AND target = ?",
                (
                    datos["proyecto"],
                    "https://www.educarex.es/pead/"
                )
            ).fetchone()

            if proyecto:
                project_id = proyecto[0]
            else:
                cursor = db.execute(
                    """
                    INSERT INTO projects (name, target, scope)
                    VALUES (?, ?, ?)
                    """,
                    (
                        datos["proyecto"],
                        "https://www.educarex.es/pead/",
                        "Análisis local de evidencias recopiladas. "
                        "Sin pruebas activas ni conexiones durante el análisis."
                    )
                )
                project_id = cursor.lastrowid
                print("[OK] Proyecto creado.")

            # Evitar importar dos veces la misma auditoría.
            auditoria = db.execute(
                """
                SELECT id FROM audits
                WHERE project_id = ? AND version = ? AND executed_at = ?
                """,
                (
                    project_id,
                    datos["version"],
                    datos["fecha_utc"]
                )
            ).fetchone()

            if auditoria:
                print("[INFO] Esta auditoría ya estaba importada.")
                print("ID de auditoría:", auditoria[0])
                return

            cursor = db.execute(
                """
                INSERT INTO audits
                    (project_id, version, mode, executed_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    project_id,
                    datos["version"],
                    datos["modo"],
                    datos["fecha_utc"]
                )
            )
            audit_id = cursor.lastrowid

            for hallazgo in datos["hallazgos"]:
                evidencia_json = json.dumps(
                    hallazgo.get("evidencia"),
                    ensure_ascii=False
                )

                db.execute(
                    """
                    INSERT INTO findings
                    (audit_id, code, title, status, severity,
                     description, evidence_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        audit_id,
                        hallazgo["id"],
                        hallazgo["titulo"],
                        hallazgo["estado"],
                        hallazgo["prioridad"],
                        hallazgo["descripcion"],
                        evidencia_json
                    )
                )
                print(f"[OK] Hallazgo importado: {hallazgo['id']}")

            for evidencia in datos["evidencias"]:
                db.execute(
                    """
                    INSERT INTO evidence
                    (audit_id, filename, sha256, size_bytes)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        audit_id,
                        evidencia["archivo"],
                        evidencia["sha256"],
                        evidencia["bytes"]
                    )
                )
                print(f"[OK] Evidencia registrada: {evidencia['archivo']}")

        print("\n[ÉXITO] Importación completada.")
        print("ID del proyecto:", project_id)
        print("ID de auditoría:", audit_id)

        # Aviso sobre el dato que requiere revisión.
        for hallazgo in datos["hallazgos"]:
            if hallazgo["id"] == "E-002":
                instancias = hallazgo.get("evidencia", {}).get("instancias")
                if instancias == 6:
                    print(
                        "\n[AVISO] E-002 conserva el dato original "
                        "(6 instancias), pendiente de revisar."
                    )

    finally:
        db.close()

if __name__ == "__main__":
    main()
