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
  # Preserve os dados de login
  dados_login = session.get('loggedIn', {})
  # Limpar todos os dados da sessão
  session.clear()
  # Reatribuir os dados de login
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
df_insumos = st.session_state['df_insumos']

col1, col2 = st.columns([2, 1])
with col1:
  lojas_selecionadas = st.selectbox(label='Loja:', options=lojas, key='lojas_multiselect')
with col2:
  data_contagem = st.date_input('Data da Contagem:', value=datetime.today(), key='data_input', format="DD/MM/YYYY")

row_height = 34.2
total_height = int(len(df_insumos) * (row_height + 1))
col1, col2, col3 = st.columns([1, 7, 1])
with col2:
  df_editado = st.data_editor(df_insumos, disabled=("ID Insumo", "Nome Insumo"), width=1000, height=total_height, key="data_editor", hide_index=True)

# Botão para registrar a contagem
if st.button("Registrar Contagem", key="registrar"):
  # Filtrar o DataFrame para incluir apenas as quantidades diferentes de 0
  df_filtrado = df_editado[(df_editado['Quantidade'] != 0) & (df_editado['Quantidade'].notna())]
  id_loja_selecionada = loja_ids[lojas_selecionadas]

  # Armazenar os dados no estado da sessão para confirmação
  st.session_state['confirmar_contagem'] = True
  st.session_state['df_filtrado'] = df_filtrado
  st.session_state['id_loja_selecionada'] = id_loja_selecionada
  st.session_state['data_contagem'] = data_contagem.strftime("%d-%m-%Y")

# Verificar se o estado de confirmação está ativo
if 'confirmar_contagem' in st.session_state and st.session_state['confirmar_contagem']:
  st.subheader('Tem certeza? Confirme as informações:')
  st.write("Loja selecionada:", lojas_selecionadas)
  st.write("Data selecionada:", st.session_state['data_contagem'])
  st.dataframe(st.session_state['df_filtrado'])

  # Botão para confirmar e inserir no banco de dados
  if st.button("Confirmar", key="confirmar"):
    # Inserir os dados no banco
    for _, row in st.session_state['df_filtrado'].iterrows():
      fk_insumo = row['ID Insumo']
      quantidade_insumo = row['Quantidade']
      insert_into_contagem_insumos(st.session_state['id_loja_selecionada'], fk_insumo, quantidade_insumo, st.session_state['data_contagem'])

    st.success("Contagens registradas com sucesso!")
    st.session_state['df_insumos'] = reset_quantidades(df_editado)
    limpar_sessao(st.session_state)

    # Rerun para atualizar a página
    st.rerun()

