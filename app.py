import streamlit as st
import paho.mqtt.client as paho
import time
import json

# Configuración MQTT
broker = "broker.mqttdashboard.com"  # También puedes usar broker.mqttdashboard.com
port = 1883
topic = "BMO_wokwi"  # Asegúrate que este topic lo escuche tu ESP32 en Wokwi

client = paho.Client("BMO_streamlit")
client.connect(broker, port)
client.loop_start()

def publicar_baile():
    payload = json.dumps({"bailar": True})
    resultado = client.publish(topic, payload)
    return resultado

st.set_page_config(page_title="BMO interactivo", layout="centered")

# Sidebar de navegación
st.sidebar.title("Funciones Disponibles")
pagina = st.sidebar.radio("Ir a", ["Saludo", "Control de Baile", "Chatea con BMO"])

# Página: Saludo
if pagina == "Saludo":
    st.title("Saludo de BMO")
    st.write("Presiona el boton para que BMO te salude.")
    #APARTIR DE AQUI EMPIEZA A PROGRAMAR EL SALUDO

# Página: Control de Baile
elif pagina == "Control de Baile":
    st.title("🕺 Activar Motores de Baile")

audio_file = open("AudioBMO.mp3", "rb")
audio_bytes = audio_file.read()

if st.button("¡Reproducir Baile!"):
        resultado = publicar_baile()
        st.audio(audio_bytes, format="audio/mp3")
        if resultado.rc == 0:
            st.success("✅ Motores activados en Wokwi (mensaje MQTT enviado).")
        else:
            st.error("❌ Fallo al enviar el mensaje MQTT.")
            st.audio(audio_bytes, format="audio/mp3")
            st.success("Motores activados y música sonando.")

# Página: Chatea con BMO
elif pagina == "Chatea con BMO":
    st.title("Preguntale a BMO")
    st.write("Aquí podrías mostrar datos en tiempo real del sistema.")
    #APARTIR DE AQUI EMPIEZA A PROGRAMAR EL SALUDO
