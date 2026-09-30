# Librerías/Funciones importadas:
import streamlit as st
import textwrap
from fisica import tamaño, temperatura, habitabilidad, planeta, color, calcular_dot_size, explicar_color
#------------------------------------------------------------------------------------

# configuración de la página (contenedor):
st.set_page_config(page_title="Crea tu Exoplaneta", layout="wide")

# fondo de la página:
def set_background(url_imagen_fondo):
    st.markdown(f"""
    <style>
    .stApp {{
        background-image:
            linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
            url("{url_imagen_fondo}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp, .stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3 {{
        color: white;
    }}
    h1, h2, h3 {{ color: #e8eeff !important; }}
    .stSlider label {{ color: #8899cc !important; }}
    .planet-container {{ 
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: rgba(62, 30, 200, 0.3);
        border: 0.5px solid rgba(100, 140, 255, 0.12);
        border-radius: 16px;
        padding: 30px;
        margin-top: 20px;
        position: relative; 
        overflow: hidden; 
        min-height: 220px;
    }}
    .orbit-ring {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        border: 0.5px solid rgba(100,140,255,0.1);
        border-radius: 50%;
    }} 
    </style>
    """, unsafe_allow_html=True)
     
set_background("https://cdn.esawebb.org/archives/images/screen/potm2603b.jpg")

# Título de la página (el simulador en sí):
st.markdown("<h1 style='text-align: center;'>Crea tu <span>Exoplaneta</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8899cc;'>Mueve los controles y descubre qué tipo de mundo estás construyendo y si es físicamente posible.</p>", unsafe_allow_html=True)
st.write("")

# las columnas en las que separarán los widgets que se colocarán:
col_simulador, col_2 = st.columns(2, gap="large")

# columna izquierda:
with col_simulador:
    with st.container(border=True):
        st.subheader("Simulador de exoplanetas")
        radio = st.slider(
            "Radio del planeta (R⊕)",
            min_value=0.3,
            max_value=22.0,
            value=0.3,
            step=0.1,
        ) 

        temp = st.slider(
            "Temperatura superficial (°C)",
            min_value=-200,
            max_value=3000,
            value=-200,
            step=5
        )
        st.write("DEBUG:", temp, temperatura(temp))
    # Aquí llamamos a las funciones que tenemos en fisica.py para los cálculos ajenos a la interfaz.
    r_nombre, r_color = tamaño(radio)
    temp_nombre = temperatura(temp)
    habitable = habitabilidad(radio, temp)
    v_type, v_title, v_why = planeta(radio, temp)

    # tamaño del planeta simulado:
    dot_size = calcular_dot_size(radio)
    planeta_color = color(radio, temp)
    glow_size = int(dot_size * 0.4)


    # En esta variable es realmente la que se encarga de dibujar el planeta simulado:
    planet_html = f"""
    <div class="planet-container">
    <div class="orbit-ring" style="width:160px;height:160px;"></div>
    <div class="orbit-ring" style="width:110px;height:110px;"></div>
    <div style="
    width: {dot_size}px;
    height: {dot_size}px;
    background: {planeta_color};
    border-radius: 50%;
    box-shadow: 0 0 {glow_size}px {planeta_color}88;
    transition: all 0.3s ease;
    z-index: 2;
    "></div>
    </div>
    
    """
    st.markdown(planet_html, unsafe_allow_html=True)
    
    if habitable:
        st.markdown(
            """<div style="
            text-align: center;
            margin-top: -15px;
            margin-bottom: 15px;
            background: rgba(62, 207, 142, 0.1);
            border: 0.5px solid #3ecf8e;
            color: #3ecf8e;
            font-size: 11px;
            font-weight: 500;
            padding: 3px 12px;
            border-radius: 20px;
            display: inline-block;
            ">Zona habitable</div>""",
            unsafe_allow_html=True
        )
            
    with st.container(border=True):
        st.markdown(
            f"""<div style="display:flex; align-items:center; gap:10px;">
            <div style="font-size:13px; color:{planeta_color};">{explicar_color(temp)}</div>
            </div>""",
            unsafe_allow_html=True)

# Como dato, se puede llamar la misma columna las veces que quieras, no se hace de nuevo un st.columns o se reinicia todo.


with col_2:
    with st.container(border=True):
            st.subheader("Datos del exoplaneta creado")
            
            st.markdown(
                f"**Tipo por tamaño:** <span style='color:{r_color}'>{r_nombre}</span>",
                unsafe_allow_html=True,
                )
            
            st.markdown(f"**Tipo por temperatura:** {temp_nombre}")
            
            st.write("¿Es físicamente posible?")
            
            if v_type == "ok":
                st.success(f"**{v_title}**\n\n{v_why}")
            elif v_type == "warn":
                st.warning(f"**{v_title}**\n\n{v_why}")
            else:
                st.error(f"**{v_title}**\n\n{v_why}")
                
# Todos los casos explicados:

st.markdown("<br><hr style='border: 0.5px solid rgba(255,255,255,0.1);'><br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: left;'>Todos los casos explicados</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #8899cc; margin-bottom: 25px;'>Por qué cada combinación de tamaño y temperatura existe, es rara, o es imposible en la naturaleza.</p>", unsafe_allow_html=True)

casos = [
    {
        "icon": "https://assets.science.nasa.gov/dynamicimage/assets/science/cds/general/images/2024/03/pia04304-mars.jpg?w=1536&h=1456&fit=crop&crop=faces%2Cfocalpoint",
        "title": "Terrestre frío",
        "subtitle": "< 1.25 R⊕ · ≤ -70 °C",
        "badge_text": "Posible",
        "badge_type": "green",
        "description": "Un planeta pequeño y rocoso en los bordes fríos de su sistema. <b>El agua existe solo como hielo</b>, la atmósfera es tenue o inexistente, y el suelo es sólido pero árido.",
        "box_text": "La gravedad de un planeta rocoso puede retener gases pesados incluso en el frío. La superficie sólida soporta temperaturas extremas sin fundirse. Funciona físicamente.",
        "example": "Ej. real: Marte (-60 °C promedio)"
    },
    {
        "icon": "https://science.nasa.gov/wp-content/uploads/2023/05/earth-1-jpg.webp?resize=768,432",
        "title": "Terrestre templado",
        "subtitle": "< 1.25 R⊕ · -70 a 40 °C",
        "badge_text": "Posible — el más buscado",
        "badge_type": "green",
        "description": "El tipo más codiciado: superficie sólida + temperatura donde el <b>agua puede ser líquida</b>. Condiciones ideales para la vida tal como la conocemos.",
        "box_text": "La física lo permite perfectamente: gravedad suficiente para atmósfera, temperatura suficiente para agua líquida, corteza sólida para sostener vida. Es la Tierra.",
        "example": "Ej. real: Tierra, TRAPPIST-1e, LHS 1140b"
    },
    {
        "icon": "🌋",
        "title": "Terrestre ultra caliente",
        "subtitle": "< 1.25 R⊕ · > 800 °C",
        "badge_text": "Extremo pero posible",
        "badge_type": "orange",
        "description": "Un mundo donde la superficie está <b>completamente fundida</b>. No hay corteza sólida, sino un océano global de roca derretida llamado océano de magma.",
        "box_text": "No es imposible, pero la atmósfera desaparece rápidamente: los gases son expulsados por la intensa radiación estelar. El planeta \"pierde\" material continuamente. Un mundo en agonía.",
        "example": "Ej. real: 55 Cancri e (~2400 °C)"
    },
    {
        "icon": "💧",
        "title": "Supertierra / mini-neptuno templado",
        "subtitle": "1.25 - 4 R⊕ · -20 a 50 °C",
        "badge_text": "Posible",
        "badge_type": "green",
        "description": "Podría ser un <b>mundo oceánico</b>: un planeta con tanta agua que no tiene fondo sólido accesible. O un mundo rocoso con atmósfera gruesa de nitrógeno.",
        "box_text": "El tamaño permite retener atmósferas densas y grandes cantidades de agua. La temperatura mantiene el agua líquida. LHS 1140b es el mejor ejemplo actual.",
        "example": "Ej. real: LHS 1140b, Kepler-442b"
    },
    {
        "icon": "🥶",
        "title": "Gigante gaseoso frío",
        "subtitle": "4 - 15 R⊕ · ≤ -70 °C",
        "badge_text": "Posible — pero en órbita lejana",
        "badge_type": "orange",
        "description": "Un gigante gaseoso <b>solo puede ser frío si está muy lejos de su estrella</b>. La combinación tiene sentido: Urano y Neptuno son exactamente esto.",
        "box_text": "La física lo permite, pero implica una distancia orbital enorme. Un gigante gaseoso frío cerca de su estrella es imposible: la radiación lo calentaría inevitablemente.",
        "example": "Ej. real: Urano (-197 °C), Neptuno (-201 °C)"
    },
    {
        "icon": "🔥",
        "title": "Júpiter caliente",
        "subtitle": "4 - 15 R⊕ · 200 - 1200 °C",
        "badge_text": "Posible — muy común",
        "badge_type": "green",
        "description": "El tipo de exoplaneta <b>más fácil de detectar</b>. Son gigantes gaseosos que orbitan muy cerca de su estrella, completando una órbita en pocos días.",
        "box_text": "Físicamente consistente: la masa enorme retiene la atmósfera incluso bajo radiación intensa. El gas es comprimido y calentado. Fue el primer tipo de exoplaneta confirmado.",
        "example": "Ej. real: 51 Pegasi b, primer exoplaneta descubierto"
    },
    {
        "icon": "💥",
        "title": "Júpiter ultra caliente",
        "subtitle": "4 - 15 R⊕ · > 2000 °C",
        "badge_text": "Extremo pero posible",
        "badge_type": "orange",
        "description": "Más caliente que muchas estrellas pequeñas. <b>Los metales se evaporan</b> en la atmósfera: llueve hierro líquido en el lado nocturno. Un mundo completamente caótico.",
        "box_text": "Posible gracias a la enorme masa que retiene incluso una atmósfera de metal vaporizado. Pero el planeta pierde masa constantemente. A largo plazo, puede ser destruido.",
        "example": "Ej. real: WASP-76b (llueve hierro)"
    },
    {
        "icon": "⚡",
        "title": "Súper-Júpiter frío",
        "subtitle": "> 15 R⊕ · ≤ -70 °C",
        "badge_text": "Posible — muy escaso",
        "badge_type": "orange",
        "description": "Un monstruo gaseoso en los confines de su sistema. <b>Recién fotografiado por el James Webb</b> en 2024 con el planeta Epsilon Indi Ab.",
        "box_text": "Físicamente válido: la masa enorme genera su propio calor interno, pero en órbitas muy lejanas la temperatura cae. Son raros porque los gigantes tienden a migrar hacia adentro.",
        "example": "Ej. real: Epsilon Indi Ab (~0 °C, 12 años luz)"
    },
    {
        "icon": "🚫",
        "title": "Planeta micro-rocoso ultra caliente",
        "subtitle": "< 0.5 R⊕ · > 2000 °C",
        "badge_text": "Físicamente inestable",
        "badge_type": "red",
        "description": "Demasiado pequeño para sobrevivir. A esa temperatura y tamaño, <b>la atmósfera se evapora completamente</b> y la roca misma se vaporiza y escapa al espacio.",
        "box_text": "Sin masa suficiente, la gravedad no puede competir con la presión de radiación estelar. El planeta sería literalmente \"comido\" por su estrella en millones de años.",
        "example": "No existen ejemplos confirmados en este rango exacto."
    },
    {
        "icon": "🪨",
        "title": "El \"asteroide grande\"",
        "subtitle": "< 0.5 R⊕ · cualquier temperatura",
        "badge_text": "No es un planeta",
        "badge_type": "red",
        "description": "Por debajo de ~0.5 R⊕ la gravedad no es suficiente para que el objeto <b>adopte forma esférica</b>. Es un asteroide, una luna pequeña o un cuerpo irregular, no un planeta.",
        "box_text": "La definición misma de planeta requiere suficiente masa para que la gravedad \"redondee\" el cuerpo. Sin eso, tenemos un planetesimal o cuerpo menor del sistema.",
        "example": "Ej. de no-planeta: Ceres (0.073 R⊕)"
    },
    {
        "icon": "🌱",
        "title": "Zona habitable perfecta",
        "subtitle": "0.8 - 2.5 R⊕  |  -20 a 50 °C",
        "badge_text": "El candidato ideal",
        "badge_type": "green",
        "description": "El \"Santo Grial\" de la búsqueda de exoplanetas. Tamaño rocoso o sub-neptuniano + temperatura donde el <b>agua puede ser líquida en la superficie</b>.",
        "box_text": "Todo encaja: gravedad suficiente para atmósfera, temperatura para agua líquida, posible corteza sólida. Es el único rango donde buscamos activamente señales de vida.",
        "example": "Ej. real: Tierra, Proxima b, TOI-715b"
    }
]

# Estilos de etiquetas de estado (badges)
badge_styles = {
    "green": "; color: #3ecf8e; border: 1px solid #3ecf8e;",
    "orange": "color: #f59e0b; border: 1px solid #f59e0b;",
    "red": "color: #f87171; border: 1px solid #f87171;"
}

accent_colors = {
    "green": "#3ecf8e",
    "orange": "#f59e0b",
    "red": "#f87171"
}

# Renderizar las tarjetas en una cuadrícula de 3 columnas
for i in range(0, len(casos), 3):
    cols = st.columns(3, gap="medium")
    chunk = casos[i:i+3]
    for idx, card in enumerate(chunk):
        with cols[idx]:
            b_style = badge_styles[card["badge_type"]]
            accent = accent_colors[card["badge_type"]]

            # El ícono puede ser una URL de imagen (empieza con "http") o un emoji.
            # Un emoji no se puede usar como src de una imagen, así que lo tratamos distinto.
            if card["icon"].startswith("http"):
                icono_html = f'<img src="{card["icon"]}" style="border-radius: 50%; width: 50px; height: 50px; object-fit: cover;">'
            else:
                icono_html = f'<div style="font-size: 34px; line-height: 50px; width: 50px; height: 50px; text-align: center;">{card["icon"]}</div>'

            card_html = textwrap.dedent(f"""
            <div style="background: rgba(62, 30, 200, 0.3); border: 1px solid rgba(100, 140, 255, 0.15); border-radius: 17px; padding: 20px; margin-bottom: 20px; min-height: 380px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
            <div>
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
            {icono_html}
            <div>
            <h4 style="margin: 0; font-size: 16px; font-weight: 600; color: #ffffff;">{card['title']}</h4>
            <p style="margin: 0; font-size: 12px; color: #8899cc;">{card['subtitle']}</p>
            </div>
            </div>
            <span style="display: inline-block; font-size: 11px; font-weight: 500; padding: 3px 10px; border-radius: 20px; margin-bottom: 10px; {b_style}">{card['badge_text']}</span>
            <p style="font-size: 13px; color: #dbe4ff; line-height: 1.5;">{card['description']}</p>
            <div style="border-left: 3px solid {accent}; background: rgba(255,255,255,0.03); padding: 8px 10px; font-size: 12px; color: #a8b4d9; line-height: 1.4; border-radius: 4px;">{card['box_text']}</div>
            </div>
            <p style="font-size: 11px; color: #6b7aa8; margin-top: 12px; margin-bottom: 0;">{card['example']}</p>
            </div>
            """)
            st.markdown(card_html, unsafe_allow_html=True)
            

