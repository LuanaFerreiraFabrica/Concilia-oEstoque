import streamlit as st
import pandas as pd

st.set_page_config(
  layout = 'wide',
  page_title = 'Estoque',
  page_icon=':ballot_box_with_ballot:',
  initial_sidebar_state="collapsed"
)

if 'loggedIn' not in st.session_state or not st.session_state['loggedIn']:
  st.switch_page('Inicio.py')


def main():
  config_sidebar()
  col, colx = st.columns([5, 1])
  with col:
    st.title('DESPESAS')
  with colx:
    if st.button("Logout"):
      logout()
  st.divider()