import streamlit as st
import pandas as pd
from datetime import datetime
from utils.queries import *
from utils.functions.dados_gerais import *

st.set_page_config(
  layout='wide',
  page_title='Estoque',
  page_icon=':ballot_box_with_ballot:',
  initial_sidebar_state="collapsed"
)

if 'loggedIn' not in st.session_state or not st.session_state['loggedIn']:
  st.switch_page('Inicio.py')

# config_sidebar()

def limpar_sessao(session):
  dados_login = session.get('loggedIn', {})
  session.clear()
  session['loggedIn'] = dados_login


def reset_quantidades(df):
  df['Quantidade'] = 0.0
  return df


st.title("Contagem de Estoque")

# Obter as lojas e insumos
df_lojas = GET_LOJAS()
lojas = df_lojas['Loja'].tolist()
loja_ids = dict(zip(df_lojas['Loja'], df_lojas['ID Loja']))
         

# Se o DataFrame de insumos não está no estado de sessão, reseta as quantidades
if 'df_insumos' not in st.session_state:
  st.session_state['df_insumos'] = reset_quantidades(GET_INSUMOS())
df_insumos = reset_quantidades(st.session_state['df_insumos'])

# Criação da chave do data_editor, que deve ser fixa a menos que um novo registro seja feito
if 'data_editor_key' not in st.session_state:
  st.session_state['data_editor_key'] = datetime.now().strftime("%Y%m%d%H%M%S%f") 


if 'hora_contagem' not in st.session_state:
  st.session_state['hora_contagem'] = datetime.now().time()



col1, col2, col3 = st.columns([2, 1, 1])
with col1:
  lojas_selecionadas = st.selectbox(label='Loja:', options=lojas, key='lojas_multiselect')
with col2:
  data_contagem = st.date_input('Data da Contagem:', value=datetime.today(), key='data_input', format="DD/MM/YYYY")
with col3:
  # Inicializar o time_input com o valor armazenado na sessão
  st.session_state['hora_contagem'] = st.time_input('Horário da Contagem:', value=st.session_state['hora_contagem'])


# Combinar data e hora
datetime_contagem = datetime.combine(data_contagem, st.session_state['hora_contagem'])
datetime_formatado = datetime_contagem.strftime("%d-%m-%Y %H:%M")  # Formato para exibição
datetime_banco = datetime_contagem.strftime("%Y-%m-%d %H:%M:%S")  # Formato para inserção no banco


col1, col2, col3 = st.columns([1, 7, 1])
with col2:
  df_editado = st.data_editor(df_insumos, disabled=("ID Insumo", "Nome Insumo", "Unidade de Medida"), width=1000, height=10000, key=st.session_state['data_editor_key'], hide_index=True)


# Botão para registrar a contagem
if st.button("Registrar Contagem", key="registrar"):
  # Filtrar o DataFrame para incluir apenas as quantidades diferentes de 0
  df_filtrado = df_editado[(df_editado['Quantidade'] != 0) & (df_editado['Quantidade'].notna())]
  id_loja_selecionada = loja_ids[lojas_selecionadas]

  # Armazenar os dados no estado da sessão para confirmação
  st.session_state['confirmar_contagem'] = True
  st.session_state['df_filtrado'] = df_filtrado
  st.session_state['id_loja_selecionada'] = id_loja_selecionada
  # st.session_state['data_contagem'] = data_contagem.strftime("%d-%m-%Y")
  st.session_state['data_contagem_banco'] = datetime_banco
  st.session_state['data_contagem_formatado'] = datetime_formatado

# Verificar se o estado de confirmação está ativo
if 'confirmar_contagem' in st.session_state and st.session_state['confirmar_contagem']:
  st.subheader('Tem certeza? Confirme as informações:')
  st.write("Loja selecionada:", lojas_selecionadas)
  st.write("Data e hora selecionadas:", st.session_state['data_contagem_formatado'])
  st.dataframe(st.session_state['df_filtrado'])

  # Botão para confirmar e inserir no banco de dados
  if st.button("Confirmar", key="confirmar"):
    # Inserir os dados no banco
    for _, row in st.session_state['df_filtrado'].iterrows():
      fk_insumo = row['ID Insumo']
      quantidade_insumo = row['Quantidade']
      insert_into_contagem_insumos(st.session_state['id_loja_selecionada'], fk_insumo, quantidade_insumo, st.session_state['data_contagem_banco'])

    st.success("Contagens registradas com sucesso!")
    st.session_state['df_insumos'] = reset_quantidades(df_editado)
    limpar_sessao(st.session_state)

    # Rerun para atualizar a página
    st.rerun()
