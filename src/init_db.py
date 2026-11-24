
#!/usr/bin/env python3

import json
import sys

from database import (
    initialize_database,
    get_connection,
    get_statistics
)

from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
JSON_FILE = BASE / "resultados" / "resultados.json"

PROJECT_NAME = "Auditoria PEAD Educarex"
PROJECT_TARGET = "https://www.educarex.es/pead/"


def import_results():

    if not JSON_FILE.exists():
        print("[ERROR] No existe resultados/resultados.json")
        sys.exit(1)

    data = json.loads(JSON_FILE.read_text(encoding="utf-8"))

    initialize_database()

    with get_connection() as db:

        project = db.execute(
            "SELECT id FROM projects WHERE name = ?",
            (PROJECT_NAME,)
        ).fetchone()

        if project:
            project_id = project["id"]
        else:
            cursor = db.execute(
                """
                INSERT INTO projects (name, target, scope)
                VALUES (?, ?, ?)
                """,
                (
                    PROJECT_NAME,
                    PROJECT_TARGET,
                    "Análisis local de evidencias recopiladas"
                )
            )
            project_id = cursor.lastrowid

        audit_cursor = db.execute(
            """
            INSERT INTO audits (project_id, version, mode)
            VALUES (?, ?, ?)
            """,
            (
                project_id,
                data.get("version", "1.0"),
                data.get("modo", "analisis_local")
            )
        )

        audit_id = audit_cursor.lastrowid

        for item in data.get("hallazgos", []):

            db.execute(
                """
                INSERT INTO findings (
                    audit_id, code, title, status,
                    severity, description, evidence_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    audit_id,
                    item.get("id"),
                    item.get("titulo"),
                    item.get("estado"),
                    item.get("prioridad"),
                    item.get("descripcion"),
                    json.dumps(
                        item.get("evidencia", {}),
                        ensure_ascii=False
                    )
                )
            )

        for item in data.get("evidencias", []):

            db.execute(
                """
                INSERT INTO evidence (
                    audit_id, filename, sha256, size_bytes
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    audit_id,
                    item.get("archivo"),
                    item.get("sha256"),
                    item.get("bytes")
                )
            )

    print(f"\n[OK] Auditoría importada. ID: {audit_id}")
    print("[OK] Hallazgos y evidencias almacenados.")
    print("\n===== ESTADÍSTICAS =====")

    for key, value in get_statistics().items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    import_results()
