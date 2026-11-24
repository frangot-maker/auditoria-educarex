
#!/usr/bin/env python3

import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DB_PATH = BASE / "resultados" / "auditoria.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    with get_connection() as db:

        db.executescript("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            target TEXT,
            scope TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS audits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            version TEXT,
            mode TEXT,
            executed_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(project_id) REFERENCES projects(id)
        );

        CREATE TABLE IF NOT EXISTS findings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_id INTEGER NOT NULL,
            code TEXT NOT NULL,
            title TEXT NOT NULL,
            status TEXT,
            severity TEXT,
            description TEXT,
            evidence_json TEXT,
            FOREIGN KEY(audit_id) REFERENCES audits(id)
        );

        CREATE TABLE IF NOT EXISTS evidence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            size_bytes INTEGER,
            FOREIGN KEY(audit_id) REFERENCES audits(id)
        );

        CREATE INDEX IF NOT EXISTS idx_findings_audit
        ON findings(audit_id);

        CREATE INDEX IF NOT EXISTS idx_evidence_audit
        ON evidence(audit_id);

        CREATE INDEX IF NOT EXISTS idx_audits_project
        ON audits(project_id);
        """)

    print(f"[OK] Base de datos preparada: {DB_PATH}")


def get_statistics():
    with get_connection() as db:
        return {
            "projects": db.execute(
                "SELECT COUNT(*) FROM projects"
            ).fetchone()[0],
            "audits": db.execute(
                "SELECT COUNT(*) FROM audits"
            ).fetchone()[0],
            "findings": db.execute(
                "SELECT COUNT(*) FROM findings"
            ).fetchone()[0],
            "evidence": db.execute(
                "SELECT COUNT(*) FROM evidence"
            ).fetchone()[0]
        }


if __name__ == "__main__":
    initialize_database()
    print(get_statistics())
