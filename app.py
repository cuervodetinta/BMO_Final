import streamlit as st
import paho.mqtt.client as paho
import time
import json

# Configuración MQTT
broker = "broker.mqttdashboard.com"
port = 1883
topic = "BMO_wokwi"

client = paho.Client("BMO_streamlit")
client.connect(broker, port)
client.loop_start()

# Función para publicar mensaje de baile
def publicar_baile():
    mensaje = {"accion": "baile", "duracion": 6}
    resultado = client.publish(topic, json.dumps(mensaje))
    return resultado

# Página: Saludo
def pagina_saludo():
    st.title("Saludo de BMO")
    st.write("Presiona el botón para que BMO te salude.")
    if st.button("¡Saluda, BMO!"):
        resultado = client.publish(topic, json.dumps({"accion": "saludo"}))
        if resultado.rc == 0:
            st.success("✅ BMO envió su saludo.")
        else:
            st.error("❌ Fallo al enviar el saludo.")

# Página: Control de Baile
def pagina_baile():
    st.title("🕺 Activar Motores de Baile")
    st.write("Presiona el botón para que BMO baile y suene la canción.")
    
    try:
        audio_file = open("AudioBMO.mp3", "rb")
        audio_bytes = audio_file.read()
        audio_file.close()
    except FileNotFoundError:
        st.error("❌ Archivo de audio no encontrado.")
        return

    if st.button("¡Reproducir Baile!"):
        resultado = publicar_baile()
        st.audio(audio_bytes, format="audio/mp3")
        if resultado.rc == 0:
            st.success("✅ Motores activados en Wokwi (mensaje MQTT enviado).")
        else:
            st.error("❌ Fallo al enviar el mensaje MQTT.")

# Página: Chatea con BMO
def pagina_chat():
    st.title("Chatea con BMO")
    st.write("Aquí podras chatear con BMO En tiempo real")
    pregunta = st.text_input("¿Qué quieres preguntarle a BMO?")
    if st.button("Enviar pregunta"):
        if pregunta.strip():
            client.publish(topic, json.dumps({"accion": "pregunta", "texto": pregunta}))
            st.success("✅ Pregunta enviada a BMO.")
        else:
            st.warning("Por favor escribe algo antes de enviar.")

# Diccionario de páginas
paginas = {
    "Saludo": pagina_saludo,
    "Control de Baile": pagina_baile,
    "Chatea con BMO": pagina_chat,
}

# Sidebar de navegación
st.sidebar.title("Funciones Disponibles")
seleccion = st.sidebar.radio("Ir a", list(paginas.keys()))
paginas[seleccion]()
