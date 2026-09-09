import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Copiloto de Respuestas Meta", page_icon="💬")
st.title("💬 Copiloto con Google Gemini")

comentario = st.text_area("1. Pega el comentario recibido:", height=100)
intencion = st.selectbox(
    "2. Selecciona la intención:",
    ["Consulta de Ventas/Precio", "Soporte/Dudas", "Queja/Reclamo", "Elogio/Agradecimiento", "Requisitos de Cuentas"]
)

api_key = st.sidebar.text_input("Google Gemini API Key", type="password")

if st.button("Generar Sugerencias", type="primary"):
    if not comentario or not api_key:
        st.warning("Por favor ingresa el comentario y tu API Key de Gemini.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-3.6-flash')
            
            # --- AQUÍ INYECTAMOS EL CEREBRO DE LAFISE ---
            prompt = f"""
            Eres un asistente de atención al cliente para redes sociales de Banco Lafise.
            
            INFORMACIÓN OFICIAL DEL BANCO (Usa estrictamente esta información para responder si el cliente pregunta por estos temas):
            - Requisitos para cuenta de ahorro: 
               Gracias por comunicarse con Banco LAFISE. ¡Muy fácil! Solo necesita abrir su Cuenta de Ahorro Digital desde LAFISE Digital, nuestra app móvil.
               También puede hacerlo desde nuestro sitio web o en cualquiera de nuestras sucursales. Una vez que realice el primer depósito desde C$50 o USD $1, usted podrá solicitar una Tarjeta de Débito VISA Internacional gratis sin costo. Si requiere más información, puede ingresar acá: https://digital.lafise.com. O escribirnos a nuestro WhatsApp (8989-8484), indicando hablar con Asesor
            
            - Horarios de atención en sucursales: Lunes a Viernes de 8:00 am a 4:30 pm y los dias sábados de 8:00 am a 12:00 md
            - Lafise Digital: Si tienen problemas con la app, indicarles que pueden restablecer su contraseña en www.lafise.com o escribir al WhatsApp oficial.
            
            - Tono de voz: Amable, profesional, empático y siempre dispuesto a ayudar. Nunca pidas datos sensibles (como contraseñas o pines) por redes sociales.
            
            Comentario recibido: "{comentario}"
            Intención del cliente: {intencion}
            
            Genera exactamente 2 opciones de respuesta. No agregues introducciones, ni viñetas, ni negritas (**), ni símbolos (>).
            
            OPCION 1: [Escribe aquí únicamente el texto de la respuesta corta y directa]
            ---
            OPCION 2: [Escribe aquí únicamente el texto de la respuesta comercial y empática]
            """
            
            with st.spinner("Generando respuestas con Gemini..."):
                response = model.generate_content(prompt)
                texto = response.text
                
                if "---" in texto:
                    partes = texto.split("---")
                    opcion1 = partes[0].replace("OPCION 1:", "").strip()
                    opcion2 = partes[1].replace("OPCION 2:", "").strip()
                    
                    st.subheader("📌 Opción 1: Corta y directa")
                    st.code(opcion1, language=None)
                    
                    st.subheader("📌 Opción 2: Comercial y empática")
                    st.code(opcion2, language=None)
                else:
                    st.write("### Respuestas sugeridas:")
                    st.code(texto, language=None)
                    
        except Exception as e:
            st.error(f"Error al conectar con Gemini: {e}")
