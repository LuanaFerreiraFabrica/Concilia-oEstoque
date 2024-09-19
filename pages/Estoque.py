import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.queries import *
from utils.functions.dados_gerais import *
from st_aggrid import AgGrid, GridOptionsBuilder



st.set_page_config(
  layout = 'wide',
  page_title = 'Estoque',
  page_icon=':ballot_box_with_ballot:',
  initial_sidebar_state="collapsed"
)

if 'loggedIn' not in st.session_state or not st.session_state['loggedIn']:
  st.switch_page('Inicio.py')


config_sidebar()

st.title("estoque")

df_lojas = GET_LOJAS()
lojas = df_lojas['Loja'].tolist()

df_insumos = GET_INSUMOS()


col1, col2 = st.columns([2, 1])
with col1:
  lojas_selecionadas = st.multiselect(label='Loja:', options=lojas, key='lojas_multiselect')
with col2:
  data_contagem = st.date_input('Data da Contagem:', value=datetime.today(), key='data_input', format="DD/MM/YYYY")


df_insumos['Quantidade'] = 0

row_height = 35
header_height = 40 
total_height = (len(df_insumos) * row_height) + header_height

# Configurar o AgGrid para permitir edição apenas na coluna 'Quantidade'
gb = GridOptionsBuilder.from_dataframe(df_insumos)
gb.configure_column('Quantidade', editable=True)  # Apenas a coluna 'Quantidade' é editável
gb.configure_column('ID Insumo', editable=False)
gb.configure_column('Nome Insumo', editable=False)
grid_options = gb.build()

grid_response = AgGrid(
    df_insumos,
    gridOptions=grid_options,
    update_mode='value_changed',
    fit_columns_on_grid_load=True,
    height=total_height,  # Defina a altura total
    domLayout='normal'  # Tente mudar para 'normal' se 'autoHeight' não funcionar
)

# Obter o DataFrame editado
df_editado = grid_response['data']
