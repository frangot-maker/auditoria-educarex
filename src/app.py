import sqlite3
from pathlib import Path
from flask import Flask, render_template_string, abort

BASE = Path(__file__).resolve().parent.parent
DB = BASE / "resultados" / "auditoria.db"

app = Flask(__name__)

def consultar(sql, parametros=()):
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    try:
        return db.execute(sql, parametros).fetchall()
    finally:
        db.close()

PLANTILLA = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ titulo }} - Audit Framework</title>
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    background: #101827;
    color: #e5e7eb;
    font-family: Arial, sans-serif;
}
header {
    background: #172338;
    padding: 22px 5%;
    border-bottom: 1px solid #34445c;
}
header h1 { margin: 0; font-size: 23px; }
header p { color: #9ca3af; margin-bottom: 0; }
nav {
    background: #1c2a40;
    padding: 14px 5%;
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}
nav a { color: #93c5fd; text-decoration: none; }
nav a:hover { color: white; }
main { padding: 30px 5%; max-width: 1250px; margin: auto; }
h2 { margin-top: 0; }
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin: 22px 0;
}
.card {
    background: #1c2a40;
    border: 1px solid #34445c;
    border-radius: 10px;
    padding: 20px;
}
.numero { font-size: 32px; font-weight: bold; margin-top: 8px; }
.muted { color: #9ca3af; font-size: 13px; }
table {
    width: 100%;
    border-collapse: collapse;
    background: #1c2a40;
    border-radius: 9px;
    overflow: hidden;
}
th, td {
    text-align: left;
    padding: 13px;
    border-bottom: 1px solid #34445c;
    overflow-wrap: anywhere;
}
th { background: #263750; }
.badge {
    display: inline-block;
    background: #34445c;
    padding: 5px 9px;
    border-radius: 6px;
    font-size: 12px;
}
section { margin-top: 30px; }
code { overflow-wrap: anywhere; }
@media(max-width: 650px) {
    main { padding: 20px 12px; }
    table { font-size: 13px; }
    th, td { padding: 9px 6px; }
}
</style>
</head>
<body>
<header>
    <h1>🛡️ AUDIT FRAMEWORK</h1>
    <p>Panel local de gestión y análisis de auditorías</p>
</header>
<nav>
    <a href="/">Inicio</a>
    <a href="/proyectos">Proyectos</a>
    <a href="/hallazgos">Hallazgos</a>
    <a href="/evidencias">Evidencias</a>
</nav>
<main>
    {{ contenido|safe }}
</main>
</body>
</html>
"""

@app.route("/")
def inicio():
    proyectos = consultar("SELECT COUNT(*) AS n FROM projects")[0]["n"]
    auditorias = consultar("SELECT COUNT(*) AS n FROM audits")[0]["n"]
    hallazgos = consultar("SELECT COUNT(*) AS n FROM findings")[0]["n"]
    evidencias = consultar("SELECT COUNT(*) AS n FROM evidence")[0]["n"]

    recientes = consultar("""
        SELECT a.id, p.name, a.version, a.mode, a.executed_at
        FROM audits a
        JOIN projects p ON p.id = a.project_id
        ORDER BY a.id DESC
    """)

    contenido = """
    <h2>Resumen general</h2>
    <div class="grid">
        <div class="card"><div class="muted">Proyectos</div>
            <div class="numero">{{ proyectos }}</div></div>
        <div class="card"><div class="muted">Auditorías</div>
            <div class="numero">{{ auditorias }}</div></div>
        <div class="card"><div class="muted">Hallazgos</div>
            <div class="numero">{{ hallazgos }}</div></div>
        <div class="card"><div class="muted">Evidencias</div>
            <div class="numero">{{ evidencias }}</div></div>
    </div>
    <section>
    <h2>Auditorías registradas</h2>
    <table>
    <tr><th>ID</th><th>Proyecto</th><th>Versión</th>
        <th>Modo</th><th>Fecha</th></tr>
    {% for a in recientes %}
    <tr><td>{{ a.id }}</td><td>{{ a.name }}</td>
        <td>{{ a.version }}</td><td>{{ a.mode }}</td>
        <td>{{ a.executed_at }}</td></tr>
    {% else %}
    <tr><td colspan="5">Todavía no hay auditorías.</td></tr>
    {% endfor %}
    </table>
    </section>
    """
    html = render_template_string(
        contenido, proyectos=proyectos, auditorias=auditorias,
        hallazgos=hallazgos, evidencias=evidencias, recientes=recientes
    )
    return render_template_string(PLANTILLA, titulo="Inicio", contenido=html)

@app.route("/proyectos")
def proyectos():
    filas = consultar("""
        SELECT p.*, COUNT(a.id) AS auditorias
        FROM projects p
        LEFT JOIN audits a ON a.project_id = p.id
        GROUP BY p.id
        ORDER BY p.id DESC
    """)
    contenido = """
    <h2>Proyectos</h2>
    <table>
    <tr><th>Nombre</th><th>Objetivo</th><th>Alcance</th>
        <th>Auditorías</th></tr>
    {% for p in filas %}
    <tr><td>{{ p.name }}</td><td>{{ p.target or '-' }}</td>
        <td>{{ p.scope or '-' }}</td><td>{{ p.auditorias }}</td></tr>
    {% else %}
    <tr><td colspan="4">No hay proyectos registrados.</td></tr>
    {% endfor %}
    </table>
    """
    html = render_template_string(contenido, filas=filas)
    return render_template_string(PLANTILLA, titulo="Proyectos", contenido=html)

@app.route("/hallazgos")
def hallazgos():
    filas = consultar("""
        SELECT f.*, a.version, p.name AS proyecto
        FROM findings f
        JOIN audits a ON a.id = f.audit_id
        JOIN projects p ON p.id = a.project_id
        ORDER BY f.id DESC
    """)
    contenido = """
    <h2>Hallazgos</h2>
    <table>
    <tr><th>Código</th><th>Título</th><th>Prioridad</th>
        <th>Estado</th><th>Proyecto</th></tr>
    {% for f in filas %}
    <tr><td>{{ f.code }}</td><td>{{ f.title }}</td>
        <td><span class="badge">{{ f.severity or 'Sin clasificar' }}</span></td>
        <td>{{ f.status or '-' }}</td><td>{{ f.proyecto }}</td></tr>
    {% else %}
    <tr><td colspan="5">No hay hallazgos registrados.</td></tr>
    {% endfor %}
    </table>
    """
    html = render_template_string(contenido, filas=filas)
    return render_template_string(PLANTILLA, titulo="Hallazgos", contenido=html)

@app.route("/evidencias")
def evidencias():
    filas = consultar("""
        SELECT e.*, a.version, p.name AS proyecto
        FROM evidence e
        JOIN audits a ON a.id = e.audit_id
        JOIN projects p ON p.id = a.project_id
        ORDER BY e.id DESC
    """)
    contenido = """
    <h2>Evidencias registradas</h2>
    <table>
    <tr><th>Archivo</th><th>SHA-256</th>
        <th>Tamaño</th><th>Proyecto</th></tr>
    {% for e in filas %}
    <tr><td>{{ e.filename }}</td><td><code>{{ e.sha256 }}</code></td>
        <td>{{ e.size_bytes }} bytes</td><td>{{ e.proyecto }}</td></tr>
    {% else %}
    <tr><td colspan="4">No hay evidencias registradas.</td></tr>
    {% endfor %}
    </table>
    """
    html = render_template_string(contenido, filas=filas)
    return render_template_string(PLANTILLA, titulo="Evidencias", contenido=html)

if __name__ == "__main__":
    if not DB.exists():
        raise FileNotFoundError(f"No existe la base de datos: {DB}")

    print("====================================")
    print(" AUDIT FRAMEWORK - PANEL LOCAL")
    print("====================================")
    print("Base de datos:", DB)
    print("Dirección: http://127.0.0.1:5000")
    print("Solo accesible desde este equipo.")
    app.run(host="127.0.0.1", port=5000, debug=False)
