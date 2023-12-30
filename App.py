import pickle
from pathlib import Path
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import numpy as np
from streamlit_option_menu import option_menu

from views import estadistica, mineria, inicio

st.set_page_config(page_title = "Sistema de Control", page_icon=":bar_chart:", layout="wide")

# User auth
names = ["Adriana Gómez", "Jose Luis Rios"]
usernames = ["agomez13", "joseluishdez01"]

#Load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, 
    "shipping_dashboard", "abcdef", cookie_expiry_days = 30)

name, authentication_status, username = authenticator.login("Iniciar Sesión", "main")

if authentication_status == False:
    st.error("Su Usuario/contraseña es incorrecto")

if authentication_status == None:
    st.warning("Por favor ingrese su usuario y contraseña")

if authentication_status:
    #menu
    v_menu=["Inicio", "Mineria de Datos", "Datos Estadisticos"]

    with st.sidebar:

        st.header("OPCIONES DE NAVEGACIÓN")

        selected = option_menu(
            menu_title=None,  # required
            options=v_menu,  # required
            icons=None,  # optional
            menu_icon="menu-down",  # optional
            default_index=0,  # optional
        )

    if selected == "Inicio":
        st.title(f"Bienvenido/a {name}")

        if "data" not in st.session_state:
            st.session_state.data = None

        uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])

        if uploaded_file:
            # Reads csv and keeps data in streamlit session
            df = pd.read_csv(uploaded_file)
            st.session_state.data = df
            st.success("Archivo CSV cargado exitosamente!")

            # CSV details
            st.write(df)
            st.write(f"**Cantidad de Filas y Columnas:** {df.shape}")
            st.write(f"**Nombre de las Columnas:** {list(df.columns)}")

            st.header("Modificar Columnas")
            selected_columns = st.multiselect("Selecciona columna(s) a modificar:", list(st.session_state.data.columns))
            if selected_columns:
                def modify_column_data(data, selected_columns, modification_option):
                    modified_data = data.copy()
                    for column in selected_columns:
                        if modification_option == "Llenar con 0":
                            if np.issubdtype(data[column].dtype, np.number):
                                modified_data[column] = 0
                            else:
                                modified_data[column] = "0"
                        elif modification_option == "Llenar con valor promedio":
                            if np.issubdtype(data[column].dtype, np.number):
                                mean_value = data[column].mean()
                                modified_data[column] = mean_value
                            else:
                                # Llenar con el valor que menos se repite para columnas de texto
                                mode_value = data[column].mode().iloc[0]
                                modified_data[column] = mode_value
                        elif modification_option == "Llenar con valor máximo":
                            if np.issubdtype(data[column].dtype, np.number):
                                max_value = data[column].max()
                                modified_data[column] = max_value
                            else:
                                # Llenar con el texto que más se repite para columnas de texto
                                mode_value = data[column].mode().iloc[0]
                                modified_data[column] = mode_value

                    return modified_data
                options = ["Llenar con 0", "Llenar con valor promedio", "Llenar con valor máximo"]
                modification_option = st.selectbox("Selecciona una opción de modificación:", options)
                if st.button("Guardar Cambios"):
                    st.session_state.data = modify_column_data(st.session_state.data, selected_columns, modification_option)
                    st.write(st.session_state.data)
                    st.success("Cambios guardados exitosamente.")
                    
    if selected=="Mineria de Datos":
        mineria.createPage(st.session_state.data)

    if selected=="Datos Estadisticos":
        estadistica.createPage(st.session_state.data)
    
    #Logout button
    authenticator.logout("Cerrar Sesión", "sidebar")
    