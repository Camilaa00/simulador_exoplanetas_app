def tamaño(r):
    if r < 0.5:
        return "No es un planeta", "#444466"
    if r < 1.25:
        return "Terrestre/rocoso", "#3ecf8e"
    if r < 2.0:
        return "Supertierra", "#22d3ee"
    if r < 4.0:
        return "Mini-neptuno", "#a78bfa"
    if r < 6.0:
        return "Gigante gaseoso pequeño", "#818cf8"
    if r < 15.0:
        return "Gigante gaseoso grande", "#f59e0b"
    return "Super-Júpiter", "#fb923c"

def habitabilidad(r, t):
    return 0.8 <= r < 2.5 and -20 <= t <= 50 

def planeta(r, t):
    if r < 0.5: 
        return (
            "bad",
            "Demasiado pequeño para ser un planeta",
            "Sin suficiente masa, la gravedad no puede redondear el cuerpo ni retener una atmósfera.",
        )
    if r < 1.25 and t > 1800:
        return (
            "bad",
            "Mundo rocoso imposible a esta temperatura",
            "La roca se vaporiza sobre los ~1700 °C y el planeta pierde masa.",
        )
    if habitabilidad(r, t):
        return (
            "ok",
            "Zona habitable: candidato a vida",
            "Rango ideal para que exista agua líquida en la superficie.",
        )
    return (
        "ok",
        "Físicamente posible",
        "Esta combinación de tamaño y temperatura es consistente con la física planetaria."
    )
    


def calcular_dot_size(r, min_dot=20, max_dot=120):
    """Traduce el radio del planeta a un tamaño de punto en píxeles."""
    dot_size = int(min_dot + (r / 22.0) * (max_dot - min_dot))
    return max(min_dot, min(max_dot, dot_size))

# fisica.py
RANGOS_TEMP = [
    # (límite superior °C, etiqueta, color)
    (-70,  "Frío / helado", "#c0392b"),
    (40,   "Templado",      "#f39c12"),
    (200,  "Caliente",      "#e8b84b"),
    (1200, "Muy caliente",  "#fff1d0"),
    (float("inf"), "Ultra caliente", "#4f8fff"),
]

def _rango(t):
    for limite, nombre, col in RANGOS_TEMP:
        if t <= limite:
            return nombre, col

def temperatura(t):
    return _rango(t)[0]

def color(r, t):
    if r < 0.5:
        return "#444466"
    return _rango(t)[1]

EXPLICACIONES_COLOR = {
    "Frío / helado": "A temperaturas muy bajas casi no hay radiación térmica visible: el planeta se ve de un rojo oscuro y apagado, como una brasa casi extinta.",
    "Templado": "A temperaturas moderadas, el planeta emitiría en tonos naranjo-amarillos, como un metal recién calentado.",
    "Caliente": "A temperaturas moderadas, el planeta emitiría en tonos naranjo-amarillos, como un metal recién calentado.",
    "Muy caliente": "A temperaturas altas, la emisión se acerca al blanco, como el filamento incandescente de una ampolleta o un metal al rojo vivo.",
    "Ultra caliente": "A temperaturas extremas, el pico de emisión se corre hacia el azul: así como la llama más caliente de un mechero es azul y no roja, un planeta a esta temperatura brillaría en tonos azulados, no rojos.",
}

def explicar_color(t):
    return EXPLICACIONES_COLOR[temperatura(t)]
