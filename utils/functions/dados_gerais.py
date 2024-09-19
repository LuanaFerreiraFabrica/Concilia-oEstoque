import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.queries import *


def config_sidebar():
  st.sidebar.header("Bem-vindo(a)!")
  if st.session_state['loggedIn']:
    st.sidebar.title("Menu")
    st.sidebar.page_link("pages/Estoque.py", label="Inserção de Estoque")
  else:
    st.sidebar.write("Por favor, faça login para acessar o menu.")






