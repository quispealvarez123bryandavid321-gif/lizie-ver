import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

# Configurar API Key desde los Secrets de Streamlit
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Falta configurar la GEMINI_API_KEY en los Secrets de Streamlit.")

# Configuración de la página
st.set_page_config(
    page_title='LIZIE VER - "El ojo artificial"',
    page_icon="🌱",
    layout="centered"
)

def buscar_logo(palabras_clave):
    archivos = os.listdir(".")
    extensiones_validas = ('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.jfif')
    for archivo in archivos:
        archivo_lower = archivo.lower()
        if any(clave.lower() in archivo_lower for clave in palabras_clave):
            if archivo_lower.endswith(extensiones_validas):
                try:
                    return Image.open(archivo)
                except Exception:
                    pass
    return None

# Encabezado con Logos y Títulos
col_logo1, col_texto, col_logo2 = st.columns([1, 3, 1])

logo_e = buscar_logo(["eureka"])
logo_c = buscar_logo(["colegio", "perez", "guereñu", "escudo"])

with col_logo1:
    if logo_e:
        st.image(logo_e, use_container_width=True)

with col_texto:
    st.markdown("<h4 style='text-align: center; color: #1b4332; margin:0;'>I.E. PADRE PÉREZ DE GUEREÑU</h4>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: #40916c; margin:0;'>FERIA ESCOLAR NACIONAL EUREKA</h6>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #2d6a4f; margin:0;'>🌱 LIZIE VER</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #52b788; font-style: italic; margin:0;'><b>'El ojo artificial que protege a las plantas'</b></p>", unsafe_allow_html=True)

with col_logo2:
    if logo_c:
        st.image(logo_c, use_container_width=True)

st.divider()

# Selector de origen de imagen (Cámara o Galería)
opcion = st.radio("Selecciona cómo ingresar la imagen:", ("📸 Usar Cámara del Celular", "📂 Subir de Galería"))

imagen_input = None

if opcion == "📸 Usar Cámara del Celular":
    imagen_input = st.camera_input("Toma una foto limpia de la hoja o planta")
else:
    imagen_input = st.file_uploader("Selecciona una foto", type=["jpg", "jpeg", "png", "webp"])

if imagen_input is not None:
    img = Image.open(imagen_input)
    st.image(img, caption="Fotografía seleccionada", use_container_width=True)
    
    if st.button("⚡ ANALIZAR PLANTA", type="primary", use_container_width=True):
        with st.spinner("⏳ Analizando planta con visión artificial..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                
                prompt = (
                    "Si la imagen NO es una planta o vegetal, responde ÚNICAMENTE: "
                    "'❌ No se detectó ninguna planta en la imagen. Por favor sube una foto de una planta o cultivo.'\n\n"
                    "Si SÍ es una planta, actúa como un experto agrónomo pero sé MUY BREVE, DIRECTO Y CONCISO. "
                    "No uses frases introductorias ni rellenos. Usa exactamente este formato corto:\n\n"
                    "🌿 Planta: [Nombre común]\n"
                    "🩺 Estado: [Sana / Con plaga / Enferma / Falta de agua o nutriente]\n"
                    "🔍 Problema: [Explicación en máximo 1 o 2 oraciones sencillas]\n"
                    "💡 Solución rápida: [Acción directa en máximo 1 o 2 oraciones]"
                )

                response = model.generate_content([prompt, img])

                st.success("Análisis completado")
                st.markdown("### 📋 Diagnóstico Agrónomo")
                st.info(response.text)

            except Exception as e:
                st.error(f"Error en la conexión: {e}")

st.divider()
st.caption("Proyecto LIZIE VER • I.E. Padre Pérez de Guereñu • Paz y Bien")
