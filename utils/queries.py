import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import mysql.connector

LOGGER = get_logger(__name__)

def mysql_connection():
  mysql_config = st.secrets["mysql"]
  # Cria a conexão com MySQL
  conn = mysql.connector.connect(
    host=mysql_config['host'],
    port=mysql_config['port'],
    database=mysql_config['database'],
    user=mysql_config['username'],
    password=mysql_config['password']
  )    
  return conn

def execute_query(query):
  conn = mysql_connection()
  cursor = conn.cursor()
  cursor.execute(query)

  # Obter nomes das colunas
  column_names = [col[0] for col in cursor.description]
  
  # Obter resultados
  result = cursor.fetchall()
  
  cursor.close()
  return result, column_names


def dataframe_query(query):
  resultado, nomeColunas = execute_query(query)
  dataframe = pd.DataFrame(resultado, columns=nomeColunas)
  return dataframe


########### Permissions #############

@st.cache_data
def GET_USERNAME(email):
  emailStr = f"'{email}'"
  return dataframe_query(f'''
  SELECT 
	  au.FULL_NAME AS 'Nome'
  FROM
  	ADMIN_USERS au 
  WHERE au.LOGIN = {emailStr}
  ''')

############ get lojas ############

@st.cache_data
def GET_LOJAS():
  return dataframe_query(f'''
  SELECT 
    te.ID,
	  te.NOME_FANTASIA AS 'Loja'
  FROM
	  T_EMPRESAS te 
  WHERE te.ID NOT IN (100, 101, 102, 106, 107, 108, 109, 111, 113, 119, 120, 121, 123, 124, 125, 126, 127, 129, 130, 133, 134, 135, 138, 141, 142, 143, 144, 145, 146, 147, 148, 155, 157, 158, 159)
  ORDER BY te.NOME_FANTASIA
    ''')


def GET_INSUMOS():
  return dataframe_query(f'''
  SELECT 
	  tin.ID AS 'ID Insumo',
  	tin.DESCRICAO AS 'Nome Insumo'
  FROM T_INSUMOS_NIVEL_5 tin
  WHERE tin.VM_ACTIVE = 1
  ORDER BY tin.DESCRICAO 
''')