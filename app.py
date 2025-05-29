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
    mensaje = {"bailar": True}
    resultado = client.publish(topic, json.dumps(mensaje))
    return resultado

# Página: Saludo
def pagina_saludo():
    st.title("👋 Saludo de BMO")
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
    st.title("💬 Chatea con BMO")
    st.write("Aquí podras chatear con BMO En tiempo real")
    pregunta = st.text_input("¿Qué quieres preguntarle a BMO?")
    if st.button("Enviar pregunta"):
        if pregunta.strip():
            client.publish(topic, json.dumps({"accion": "pregunta", "texto": pregunta}))
            st.success("✅ Pregunta enviada a BMO.")
        else:
            st.warning("Por favor escribe algo antes de enviar.")

#LO QUE ISIS ME ACABA DE PASAR
# Configura tu API key de ElevenLabs
ELEVENLABS_API_KEY = "sk_628f20d8f86797b404799056f0443d2a4920cadc7cbbbfd1" # Reemplaza con tu API Key real
#VOICE_ID = "1Z7qQDyqapTm8qBfJx6e" #INGLES
VOICE_ID = "tTdCI0IDTgFa2iLQiWu4"  # español

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.content  # Devuelve el audio en bytes
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

# Interfaz en Streamlit
st.title("Texto a Voz con ElevenLabs")

user_text = st.text_area("Escribe el texto que quieres convertir a voz:")

if st.button("Convertir a voz"):
    if user_text.strip():
        audio_data = text_to_speech(user_text)
        if audio_data:
            st.audio(audio_data, format="audio/mp3")
    else:
        st.warning("Por favor, escribe algo de texto.")

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
