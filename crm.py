import streamlit as st
import pandas as pd
import pymssql

# Estilos personalizados
st.markdown(
    """
    <style>
    .main {
        background-color: #f9f9f9;
        font-family: 'Arial', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #e6e6e6;
        font-family: 'Arial', sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #333333;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 15px;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .dataframe-container {
        max-width: 90%;
        margin: auto;
    }
    .small-text {
        font-size: 14px;
        text-align: center;
        color: #555555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Encabezado de bienvenida
st.markdown(
    """
    <h1 style='text-align: center; color: #333333;'>
        Sistema de Gestión de Clientes
    </h1>
    """,
    unsafe_allow_html=True
)

# Diccionario de usuarios con nombres formateados
usuarios = {
    "12345": {"gestor": "Anahí Cabrales Araujo", "password": "12345"},
    "123": {"gestor": "Ana Laura Rivera Inzunza", "password": "123"},
    "983243": {"gestor": "Jessica Maribel Vargas Villagrana", "password": "34567"},
    "983242": {"gestor": "Cinthia Guadalupe Checa Robles", "password": "34562"},
    "983241": {"gestor": "Julissa Iveth Gamez Ramirez", "password": "34565"},
    "983247": {"gestor": "Marcos Eduardo Robles Vázquez", "password": "34568"},
    "983248": {"gestor": "Reyna Berenice Salazar Cabrera", "password": "34569"},
    "983244": {"gestor": "José Alfredo Alvarado Hernandez", "password": "34561"},
    "1": {"gestor": "Sergio Millán", "password": "1"}
}

# Función de inicio de sesión
def login():
    st.title("Iniciar Sesión")
    codigo_acceso = st.text_input("Código de Acceso")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar Sesión"):
        if codigo_acceso in usuarios and usuarios[codigo_acceso]["password"] == password:
            gestor = usuarios[codigo_acceso]["gestor"]
            st.success(f"Bienvenido {gestor}")
            st.session_state["authenticated"] = True
            st.session_state["gestor"] = gestor
        else:
            st.error("Código de acceso o contraseña incorrectos")

# Botón para cerrar sesión
def cerrar_sesion():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# Verificar si el usuario está autenticado
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
else:
    # Configurar la conexión a SQL Server
    server = '52.167.231.145'
    port = 51433
    database = 'CreditoYCobranza'
    username = 'credito'
    password = 'Cr3d$.23xme'

    # Crear la conexión con manejo de errores
    try:
        conn = pymssql.connect(
            server=server,
            port=port,
            user=username,
            password=password,
            database=database
        )
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        st.stop()

    # Cargar datos desde SQL Server
    gestor_autenticado = st.session_state["gestor"].strip()
    query = "SELECT * FROM Base_Nueva_CRM WHERE GESTOR = %s"  # Cambio a %s para parametrizar

    try:
        data = pd.read_sql(query, conn, params=[gestor_autenticado])
    except Exception as e:
        st.error(f"Error al ejecutar la consulta: {e}")
        st.stop()

    # Sidebar para navegación y botón de cerrar sesión
    st.sidebar.title(f"Gestor: {gestor_autenticado}")
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Ir a", ["Información de Cliente", "Base Completa", "Estadísticas", "Comisiones"])
    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar Sesión"):
        cerrar_sesion()

    # Resto del código para las páginas (sin cambios)
