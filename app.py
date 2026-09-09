import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Copiloto de Respuestas Meta", page_icon="💬")
st.title("💬 Copiloto con Google Gemini")

comentario = st.text_area("1. Pega el comentario recibido:", height=100)
intencion = st.selectbox(
    "2. Selecciona la intención:",
    ["Consulta de Ventas/Precio", "Soporte/Dudas", "Queja/Reclamo", "Elogio/Agradecimiento"]
)

# Ahora pedimos la clave de Gemini en lugar de OpenAI
api_key = st.sidebar.text_input("Google Gemini API Key", type="password")

if st.button("Generar Sugerencias", type="primary"):
    if not comentario or not api_key:
        st.warning("Por favor ingresa el comentario y tu API Key de Gemini.")
    else:
        try:
            # Configuramos la conexión con Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Eres un asistente de atención al cliente para redes sociales.
            Comentario recibido: "{comentario}"
            Intención del cliente: {intencion}
            
            Genera 2 opciones de respuesta (una corta/directa y otra más comercial/empática).
            Asegúrate de cerrar invitando al usuario a escribir por mensaje privado (DM).
            """
            
            with st.spinner("Generando respuestas con Gemini..."):
                response = model.generate_content(prompt)
                sugerencia = response.text
                
                st.write("### Respuestas sugeridas:")
                st.code(sugerencia, language=None)
        except Exception as e:
            st.error(f"Error al conectar con Gemini: {e}")
