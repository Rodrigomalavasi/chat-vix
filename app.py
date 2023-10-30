import streamlit as st
import paho.mqtt.client as mqtt

def receber_mensagens(mensagem):
    mensagem_recebida = mensagem.payload.decode("utf-8")
    st.session_state.mensagens_pedro.append(f"Pedro: {mensagem_recebida}")

cliente = mqtt.Client()
cliente.on_message = receber_mensagens

try:
    cliente.connect('localhost', 1883)
    cliente.subscribe('PedroToRodrigo')
    st.write("Conectado e inscrito no tópico com sucesso!")
except Exception as e:
    st.write(f"Erro na conexão: {e}")

st.title('Chatvix')
st.subheader('Conversa com Pedro')

if 'mensagens_pedro' not in st.session_state:
    st.session_state.mensagens_pedro = []

prompt = st.chat_input("Digite aqui")
if prompt:
    st.session_state.mensagens_pedro.append(f"Rodrigo: {prompt}")
    cliente.publish('PedroToRodrigo', prompt)

cliente.loop_start()

for mensagem in st.session_state.mensagens_pedro:
    st.write(mensagem)
    
while True:
    cliente.loop()