import streamlit as st
import paho.mqtt.publish as publish
import json

st.set_page_config(page_title="BMO interactivo", layout="centered")

# Sidebar de navegación
st.sidebar.title("Funciones Disponibles")
pagina = st.sidebar.radio("Ir a", ["Saludo", "Control de Baile", "Chatea con BMO"])

# Página: Inicio
if pagina == "Saludo":
    st.title("Saludo de BMO")
    st.write("Usa el menú lateral para controlar dispositivos y reproducir sonidos.")

# Página: Control de Baile
elif pagina == "Control de Baile":
    st.title("Control de Baile 🎵🕺")

    # Reproducir música
    audio_file = open("AudioBMO.mp3", "rb")
    audio_bytes = audio_file.read()

    if st.button("¡Que empiece el show!"):
        # Publicar mensaje MQTT
        audio_file = open("AudioBMO.mp3", "rb")
        audio_bytes = audio_file.read()
        
        msg = json.dumps({"bailar": True})
        publish.single("bailar/accion", msg, hostname="broker.mqttdashboard.com")

        # Reproducir audio
        st.audio(audio_bytes, format="audio/mp3")
        st.success("Motores activados y música sonando.")

# Página: Estado de Motores (ficticia para mostrar multipágina)
elif pagina == "Chatea con BMO":
    st.title("Preguntale a BMO")
    st.write("Aquí podrías mostrar datos en tiempo real del sistema.")
