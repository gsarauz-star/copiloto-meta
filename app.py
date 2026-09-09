import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Copiloto de Respuestas Meta", page_icon="💬")
st.title("💬 Copiloto de Respuestas Meta")

comentario = st.text_area("1. Pega el comentario recibido:", height=100)
intencion = st.selectbox(
    "2. Selecciona la intención:",
    ["Consulta de Ventas/Precio", "Soporte/Dudas", "Queja/Reclamo", "Elogio/Agradecimiento"]
)

api_key = st.sidebar.text_input("OpenAI API Key", type="password")

if st.button("Generar Sugerencias", type="primary"):
    if not comentario or not api_key:
        st.warning("Por favor ingresa el comentario y tu API Key de OpenAI.")
    else:
        client = OpenAI(api_key=api_key)
        
        prompt = f"""
        Eres un asistente de atención al cliente para redes sociales.
        Comentario recibido: "{comentario}"
        Intención del cliente: {intencion}
        
        Genera 2 opciones de respuesta (una corta/directa y otra más comercial/empática).
        Asegúrate de cerrar invitando al usuario a escribir por mensaje privado (DM).
        """
        
        with st.spinner("Generando respuestas..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            
            sugerencia = response.choices[0].message.content
            
            st.write("### Respuestas sugeridas:")
            st.code(sugerencia, language=None)
