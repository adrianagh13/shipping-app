import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def createPage(data):
    st.empty()
    st.title("Datos Estadísticos")
    st.write("")
    if data is not None:
        st.write("**Descripción Estadística del dataset:**")
        st.write(data.describe())
        st.write("")
         # Interactive exploration
        st.write("**Exploración Interactiva del dataset:**")
        explore_option = st.radio("Selecciona una opción:", ["Vista General", "Explorar Columnas", "Filtrar Datos"])

        if explore_option == "Vista General":
            # Shows complete df
            st.write(data)

        elif explore_option == "Explorar Columnas":
            # shows options to show specific columns
            selected_column = st.selectbox("Selecciona una columna:", list(data.columns))
            st.write(f"**Exploración de la Columna {selected_column}:**")
            st.write(f"**Cantidad de Valores Únicos:** {data[selected_column].nunique()}")
            st.write(f"**Top 10 Valores Más Comunes:**")
            st.write(data[selected_column].value_counts().head(10))

        elif explore_option == "Filtrar Datos":
            # allows user to filter a certain value
            filter_column = st.selectbox("Selecciona una columna para filtrar:", list(data.columns))
            filter_value = st.text_input("Ingresa el valor para filtrar:")
            filtered_df = data[data[filter_column] == filter_value]
            st.write(f"**DataFrame Filtrado por {filter_column} == {filter_value}:**")
            st.write(filtered_df)
        
        # Gráficas
        st.write("")
        st.header("**Gráficas**")
        
        # Countplot
        st.subheader("*Gráfico de Barras*")
        countplot_column = st.selectbox("Selecciona una columna para el grafico de barras:", list(data.columns), key="count_column")
        if countplot_column:
            # Countplot con los 10 valores que más se repiten
            st.write("Top 10 Valores Más Comunes")
            top_values = data[countplot_column].value_counts().head(10)
            countplot_top = sns.countplot(x=countplot_column, data=data[data[countplot_column].isin(top_values.index)])
            plt.xticks(rotation=45)
            st.pyplot(countplot_top.figure)

            # Countplot con los 10 valores que menos se repiten
            st.write("Top 10 Valores Menos Comunes")
            bottom_values = data[countplot_column].value_counts().tail(10)
            countplot_bottom = sns.countplot(x=countplot_column, data=data[data[countplot_column].isin(bottom_values.index)])
            plt.xticks(rotation=45)
            st.pyplot(countplot_bottom.figure)

         # Boxplot
        st.subheader("*Gráfico de Cajas*")
        st.write("Muestra la relación entre valores numéricos y valores categóricos")
        # Obtener listas de columnas numéricas y no numéricas
        numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
        non_numeric_columns = data.select_dtypes(exclude=['number']).columns.tolist()

        # Seleccionar una columna numérica y una no numérica
        numeric_column = st.selectbox("Selecciona una columna numérica:", numeric_columns)
        non_numeric_column = st.selectbox("Selecciona una columna no numérica:", non_numeric_columns)

        # Crear el gráfico de boxplot para los 10 valores más comunes
        top_values_numeric = data[numeric_column].value_counts().head(10).index
        top_values_non_numeric = data[non_numeric_column].value_counts().head(10).index
        if not top_values_numeric.empty and not top_values_non_numeric.empty:
            boxplot_top = sns.boxplot(x=non_numeric_column, y=numeric_column, data=data[data[non_numeric_column].isin(top_values_non_numeric) & data[numeric_column].isin(top_values_numeric)])
            st.pyplot(plt.gcf())
        else:
            st.warning("No hay suficientes valores únicos para el Boxplot de los 10 valores más comunes.")

    else:
        st.warning("No se han cargado datos todavía.")
    return True