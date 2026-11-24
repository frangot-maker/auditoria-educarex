import sqlite3
import json
import hashlib
from pathlib import Path
from datetime import datetime

base = Path(".")
json_path = base / "resultados/resultados.json"
db_path = base / "resultados/auditoria.db"

data = json.loads(json_path.read_text(encoding="utf-8"))

if data.get("version") != "1.1":
    raise SystemExit("ERROR: el JSON no es versión 1.1")

if len(data.get("hallazgos", [])) != 6:
    raise SystemExit("ERROR: no hay seis hallazgos")

# Validar todas las evidencias antes de modificar SQLite.
for ev in data["evidencias"]:
    path = base / ev["archivo"]
    if not path.is_file():
        raise SystemExit(f"Falta evidencia: {ev['archivo']}")

    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != ev["sha256"]:
        raise SystemExit(f"Hash incorrecto: {ev['archivo']}")
    if len(raw) != ev["bytes"]:
        raise SystemExit(f"Tamaño incorrecto: {ev['archivo']}")

# Copia de seguridad de SQLite.
backup_path = base / "copias_seguridad" / (
    "auditoria_pre_sync_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".db"
)
backup_path.parent.mkdir(parents=True, exist_ok=True)

db = sqlite3.connect(db_path)
backup = sqlite3.connect(backup_path)
db.backup(backup)
backup.close()

try:
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("BEGIN")

    db.execute("""
        UPDATE audits
        SET version=?, mode=?, executed_at=?
        WHERE id=1
    """, (data["version"], data["modo"], data["fecha_utc"]))

    db.execute("""
        UPDATE projects
        SET scope=?
        WHERE id=1
    """, (
        "Auditoría PEAD en producción: pruebas HTTP no destructivas "
        "y análisis local de evidencias. No se realizaron pruebas DoS.",
    ))

    for h in data["hallazgos"]:
        rows = db.execute("""
            SELECT id FROM findings
            WHERE audit_id=1 AND code=?
            ORDER BY id
        """, (h["id"],)).fetchall()

        values = (
            h["titulo"], h["estado"], h["prioridad"],
            h["descripcion"],
            json.dumps(h["evidencia"], ensure_ascii=False)
        )

        if rows:
            db.execute("""
                UPDATE findings
                SET title=?, status=?, severity=?,
                    description=?, evidence_json=?
                WHERE id=?
            """, (*values, rows[0][0]))

            for duplicate in rows[1:]:
                db.execute(
                    "DELETE FROM findings WHERE id=?",
                    (duplicate[0],)
                )
        else:
            db.execute("""
                INSERT INTO findings
                (audit_id, code, title, status, severity,
                 description, evidence_json)
                VALUES (1, ?, ?, ?, ?, ?, ?)
            """, (h["id"], *values))

    db.execute("DELETE FROM evidence WHERE audit_id=1")

    for ev in data["evidencias"]:
        db.execute("""
            INSERT INTO evidence
            (audit_id, filename, sha256, size_bytes)
            VALUES (1, ?, ?, ?)
        """, (ev["archivo"], ev["sha256"], ev["bytes"]))

    db.commit()

except Exception:
    db.rollback()
    raise

finally:
    db.close()

print("Sincronización SQLite completada.")
print("Copia previa:", backup_path)
print("Versión:", data["version"])
print("Hallazgos:", len(data["hallazgos"]))
print("Evidencias:", len(data["evidencias"]))
