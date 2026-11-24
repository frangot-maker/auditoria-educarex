import sqlite3
import hashlib
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DB = BASE / "resultados" / "auditoria.db"
ARCHIVO = BASE / "evidencias" / "procesadas" / "cabeceras_portada.txt"

if not ARCHIVO.is_file():
    raise SystemExit(
        "[ERROR] No existe evidencias/procesadas/cabeceras_portada.txt"
    )

sha = hashlib.sha256(ARCHIVO.read_bytes()).hexdigest()
tamano = ARCHIVO.stat().st_size

db = sqlite3.connect(DB)
db.execute("PRAGMA foreign_keys = ON")

try:
    auditoria = db.execute(
        "SELECT id FROM audits WHERE project_id = 1 ORDER BY id DESC LIMIT 1"
    ).fetchone()

    if not auditoria:
        raise SystemExit("[ERROR] No existe una auditoría para el proyecto 1.")

    audit_id = auditoria[0]

    existente = db.execute(
        """
        SELECT id FROM evidence
        WHERE audit_id = ? AND filename = ?
        """,
        (audit_id, "evidencias/procesadas/cabeceras_portada.txt")
    ).fetchone()

    if existente:
        print("[INFO] Esta evidencia ya estaba registrada.")
        print("ID:", existente[0])
    else:
        cursor = db.execute(
            """
            INSERT INTO evidence
            (audit_id, filename, sha256, size_bytes)
            VALUES (?, ?, ?, ?)
            """,
            (
                audit_id,
                "evidencias/procesadas/cabeceras_portada.txt",
                sha,
                tamano
            )
        )
        db.commit()
        print("[OK] Evidencia registrada. ID:", cursor.lastrowid)

    print("SHA-256:", sha)
    print("Tamaño:", tamano, "bytes")

finally:
    db.close()
