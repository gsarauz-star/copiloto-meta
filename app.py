import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Copiloto de Respuestas Meta", page_icon="💬", layout="centered")
st.title("💬 Copiloto LAFISE: Evaluación de Riesgo e Información Oficial")

api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Google Gemini API Key", type="password")

comentario = st.text_area("1. Pega el comentario recibido:", height=120)
intencion = st.selectbox(
    "2. Selecciona la intención:",
    ["Soporte/Dudas", "Queja/Reclamo", "Ataque/Hostilidad Extrema", "Requisitos de Cuentas/Tarjetas", "Consulta de Ventas/Precio", "Elogio/Agradecimiento"]
)

if st.button("Analizar y Generar Sugerencias", type="primary"):
    if not comentario or not api_key:
        st.warning("Por favor ingresa el comentario y verifica tu API Key de Gemini.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-3.6-flash')
            
            prompt = f"""
            Eres un especialista Senior en Reputación Digital y Atención al Cliente de Banco LAFISE.
            
            INFORMACIÓN OFICIAL DEL BANCO (Usa estrictamente esta base de conocimientos para responder):
            - Requisitos Cuenta de Ahorro: Cédula de identidad original y vigente, y depósito inicial mínimo de $50 (o equivalente local).
            - Requisitos Tarjeta de Crédito: Cédula vigente, constancia de ingresos (mínimo $500) y 1 año de antigüedad laboral.
            - Lafise Digital: Para problemas de acceso o claves, dirigir a www.lafise.com o al WhatsApp oficial verificado.
            - Horario de Sucursales: Lunes a Viernes de 8:00 am a 4:30 pm.
            - Política de Seguridad: NUNCA solicitar contraseñas, PINs o datos sensibles por redes sociales.

            REGLAS DE EVALUACIÓN DE CONVENIENCIA:
            - 🔴 NO RESPONDER / ESCALAR A CRISIS: Si hay insultos graves, hostilidad pura sin solicitud de ayuda real, acusaciones de delitos (robo/hackeo), o si responder con un bot/plantilla generará más burlas (como clientes quejándose explícitamente de respuestas automatizadas).
            - 🟡 RESPONDER CON PRECAUCIÓN: Quejas con molestia justificada sobre un servicio o producto donde se pueda ofrecer una solución real por mensaje privado.
            - 🟢 RESPONDER NORMALMENTE: Dudas de productos, precios, requisitos o elogios.

            Comentario recibido: "{comentario}"
            Intención seleccionada: {intencion}

            Escribe tu análisis respetando ESTRICTAMENTE este formato separado por triples guiones (---):

            EVALUACION: [Escribe únicamente: "🔴 NO RESPONDER (Riesgo Reputacional)", "🟡 RESPONDER CON PRECAUCIÓN" o "🟢 RESPONDER NORMALMENTE"]
            ---
            JUSTIFICACION: [Explicación breve de 1 o 2 oraciones de por qué es conveniente o no responder]
            ---
            OPCION 1: [Escribe la respuesta recomendada usando la INFORMACIÓN OFICIAL. Si evaluaste 🔴 NO RESPONDER, escribe: "Se sugiere NO publicar respuesta pública. Derivar caso a Gestión de Crisis / Legal."]
            ---
            OPCION 2: [Segunda opción de respuesta o alternativa de abordaje comercial/empática]
            """
            
            with st.spinner("Analizando riesgo y consultando información oficial..."):
                response = model.generate_content(prompt)
                partes = response.text.split("---")
                
                if len(partes) >= 4:
                    evaluacion = partes[0].replace("EVALUACION:", "").strip()
                    justificacion = partes[1].replace("JUSTIFICACION:", "").strip()
                    opcion1 = partes[2].replace("OPCION 1:", "").strip()
                    opcion2 = partes[3].replace("OPCION 2:", "").strip()
                    
                    st.markdown("### 📊 Evaluación de Conveniencia")
                    if "🔴" in evaluacion:
                        st.error(f"**Recomendación:** {evaluacion}")
                    elif "🟡" in evaluacion:
                        st.warning(f"**Recomendación:** {evaluacion}")
                    else:
                        st.success(f"**Recomendación:** {evaluacion}")
                        
                    st.info(f"**Análisis de Riesgo:** {justificacion}")
                    
                    st.markdown("---")
                    st.subheader("📌 Respuesta Sugerida 1 (Directa / Basada en Datos)")
                    st.code(opcion1, language=None)
                    
                    st.subheader("📌 Respuesta Sugerida 2 (Empática / Comercial)")
                    st.code(opcion2, language=None)
                else:
                    st.write("### Resultado del Análisis:")
                    st.code(response.text, language=None)
                    
        except Exception as e:
            st.error(f"Error al conectar con Gemini: {e}")
