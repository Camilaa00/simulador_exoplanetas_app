#llamamos a la libreria
import streamlit as st

#nombre de la pagina
st.set_page_config(
    page_title="Crea tu Exoplaneta", layout="centered"
)

# diseño
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0a0e1a;
        color: #e8eeff;
    }
    h1, h2, h3 {
        color: #e8eeff !important; 
    }
    .stSlider label {
        color: #8899cc !important;
    }
    .planet-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: #1a2340;
        border: 0.5px solid rgba(100,140,255,0.12);
        border-radius: 16px;
        padding: 30px;
        margin-top: 20px;
        position: relative;
        overflow: hidden;
        min-height: 220px;
    }
    .orbit-ring {
        position: absolute;
        border: 0.5px solid rgba(100,140,255,0.1);
        border-radius: 50%;
    } 
    </style>
""",
    unsafe_allow_html=True,
)

# Título de la aplicación
st.markdown(
    "<h1 style='text-align: center;'>Crea tu <span>Exoplaneta</span></h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #8899cc;'>Mueve los controles y descubre qué tipo de mundo estás construyendo y si es físicamente posible.</p>",
    unsafe_allow_html=True,
)

#columnaspara los controles
col_1, col_2 = st.columns(2)

with col_1:
    radio = st.slider(
        "Radio del planeta (R⊕)",
        min_value=0.3,
        max_value=22.0,
        value=1.0,
        step=0.1,
    ) 

with col_2:
    temp = st.slider(
        "Temperatura superficial (°C)",
        min_value=-200,
        max_value=3000,
        value=15,
        step=5
    )

#clasisifacion segun temperatura y tamaño  
def tamaño(r):
    if r < 0.5:
        return "No es un planeta", "#f87171"
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

def temperatura(t):
    if t <= -70:
        return "Frío / helado"
    if t <= 40:
        return "Templado"
    if t <= 200:
        return "Caliente"
    if t <= 1200:
        return "Muy caliente"
    return "Ultra caliente"

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

def color(r, t):
    if r < 0.5:
        return "#444466"
    if t > 2000:
        return "#c0392b"
    if t > 200:
        return "#f39c12"
    if t > 40:
        return "#e8b84b"
    if t > -70:
        return "#3ecf8e"
    return "#4f8fff"

# llamamos a la funcion
r_nombre, r_color = tamaño(radio)
temp_nombre = temperatura(temp)
habitable = habitabilidad(radio, temp)
v_type, v_title, v_why = planeta(radio, temp)

# tamaño del punto
min_dot, max_dot = 20, 120
dot_size = int(min_dot + (radio / 22.0) * (max_dot - min_dot))
dot_size = max(min_dot, min(max_dot, dot_size))
planet_color = color(radio, temp)
glow_size = int(dot_size * 0.4)


habitable_html = f"""
<div style="
margin-top: 8px;
background: rgba(62,207,142,0.1);
border: 0.5px solid #3ecf8e;
color: #3ecf8e;
font-size: 11px;
font-weight: 500;
padding: 3px 12px;
border-radius: 20px;
z-index: 2;
">Zona habitable</div>
""" if habitable else ""

# dibujar el planeta 
planet_html = f"""
<div class="planet-container">
<div class="orbit-ring" style="width:160px;height:160px;"></div>
<div class="orbit-ring" style="width:110px;height:110px;"></div>

<div style="
width: {dot_size}px;
height: {dot_size}px;
background: {planet_color};
border-radius: 50%;
box-shadow: 0 0 {glow_size}px {planet_color}88;
transition: all 0.3s ease;
z-index: 2;
"></div>

<div style="margin-top: 14px; font-size: 13px; font-weight: 500; color: #8899cc; z-index: 2;">
{r_nombre} · {temp_nombre.lower()}
</div>
{habitable_html}
</div>
"""

st.markdown(planet_html, unsafe_allow_html=True)

st.write("---")
col_res1, col_res2 = st.columns(2)
with col_res1:
    st.markdown(
        f"**Tipo por tamaño:** <span style='color:{r_color}'>{r_nombre}</span>",
        unsafe_allow_html=True,
    )
with col_res2:
    st.markdown(f"**Tipo por temperatura:** {temp_nombre}")

st.write("")

if v_type == "ok":
    st.success(f"**{v_title}**\n\n{v_why}")
elif v_type == "warn":
    st.warning(f"**{v_title}**\n\n{v_why}")
else:
    st.error(f"**{v_title}**\n\n{v_why}")

