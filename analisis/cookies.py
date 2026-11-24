from collections import defaultdict

cabeceras = [
    "Set-Cookie: gcprsess=[REDACTADO]; expires=Tue, 24-Nov-2026 18:28:41 GMT; Max-Age=7200; path=/",
    "Set-Cookie: gcprsess=[REDACTADO]; expires=Tue, 24-Nov-2026 18:28:41 GMT; Max-Age=7200; path=/"
]

cookies = defaultdict(list)

for cabecera in cabeceras:
    nombre, contenido = cabecera.split(":", 1)
    partes = contenido.strip().split(";")

    clave, valor = partes[0].split("=", 1)
    atributos = [x.strip().lower() for x in partes[1:]]

    cookies[clave].append({
        "valor": valor,
        "atributos": atributos
    })

print("===== ANALISIS DE COOKIES =====")

for nombre, instancias in cookies.items():
    print(f"\nCookie: {nombre}")
    print(f"Instancias: {len(instancias)}")

    for i, cookie in enumerate(instancias, 1):
        print(f"\n  Instancia {i}")
        print(f"  Secure: {'secure' in cookie['atributos']}")
        print(f"  HttpOnly: {'httponly' in cookie['atributos']}")
        print(f"  SameSite: ", end="")

        samesite = [
            x for x in cookie["atributos"]
            if x.startswith("samesite=")
        ]

        print(samesite[0] if samesite else "No declarado")
