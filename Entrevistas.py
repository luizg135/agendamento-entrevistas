import streamlit as st
import pandas as pd

# Definir datas e horários disponíveis
datas = ['13/11/2024', '14/11/2024']
horarios = ['13h30', '14h00', '14h30', '15h00', '15h30', '16h00', '16h30', '17h00']

# Carregar dados já agendados (se houver)
try:
    agendamentos = pd.read_csv('agendamentos.csv')
except FileNotFoundError:
    agendamentos = pd.DataFrame(columns=['Data', 'Horário', 'Nome'])

# Função para verificar se o horário já foi agendado
def horario_disponivel(data, horario):
    return not agendamentos[(agendamentos['Data'] == data) & (agendamentos['Horário'] == horario)].empty

# Função para agendar entrevista
def agendar_entrevista(data, horario, nome):
    agendamentos.loc[len(agendamentos)] = [data, horario, nome]
    agendamentos.to_csv('agendamentos.csv', index=False)

# Interface Streamlit
st.title('Agendamento de Entrevistas | ATeG')

# Formulário de agendamento
nome = st.text_input('Digite seu nome:')
data = st.selectbox('Escolha a data:', datas)
horario = st.selectbox('Escolha o horário:', horarios)

# Verificar se a data e o horário estão disponíveis
if horario_disponivel(data, horario):
    st.error(f'O horário {horario} no dia {data} já está agendado!')
else:
    if st.button('Confirmar Agendamento'):
        agendar_entrevista(data, horario, nome)
        st.success(f'Entrevista agendada com sucesso para {nome} no dia {data} às {horario}!')

# Mostrar agendamentos atuais
st.subheader('Agendamentos Confirmados:')
st.dataframe(agendamentos)
