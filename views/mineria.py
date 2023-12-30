import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_curve, auc
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

def createPage(data):
    st.empty()
    st.title("Mineria de Datos: Entrenamiento del Modelo y Predicciones")
    
    if data is not None:
        # Obtener la lista de columnas del conjunto de datos
        columns_list = data.columns.tolist()

        # Widget para seleccionar la columna objetivo
        selected_column = st.selectbox("Selecciona la columna objetivo:", ['--'] + columns_list)

        if selected_column == '--':
            st.warning("Por favor, selecciona una columna objetivo para la predicción.")
            return True

        # Modificación de columnas
        data['DiscVessArrDt'] = pd.to_datetime(data['DiscVessArrDt'], format="%Y-%m-%d", errors='coerce')
        data['DestinationArrivalDt'] = pd.to_datetime(data['DestinationArrivalDt'], format="%Y-%m-%d", errors='coerce')
        data['OriginDepartureDt'] = pd.to_datetime(data['OriginDepartureDt'], format="%Y-%m-%d", errors='coerce')
        data['SailDt'] = pd.to_datetime(data['SailDt'], format="%Y-%m-%d", errors='coerce')
        data['BLDate'] = pd.to_datetime(data['BLDate'], format="%Y-%m-%d", errors='coerce')
        
        # Dividir el conjunto de datos en características (X) y la columna objetivo (y)
        X = data.drop(selected_column, axis=1)  # excluye la variable objetivo
        y = data[selected_column]

        # Fechas divididas
        for col in ['BLDate', 'SailDt', 'DiscVessArrDt', 'OriginDepartureDt', 'DestinationArrivalDt']:
            X[col + '_Year'] = X[col].dt.year
            X[col + '_Month'] = X[col].dt.month
            X[col + '_Day'] = X[col].dt.day

        X = X.drop(['BLDate', 'SailDt', 'DiscVessArrDt', 'OriginDepartureDt', 'DestinationArrivalDt'], axis=1)

        # Convertir variables categóricas a numéricas
        label_encoder = LabelEncoder() 
        for column in X.select_dtypes(include=['object']).columns:
            X[column] = label_encoder.fit_transform(X[column])

        # Dividir los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Entrenar el modelo (en este caso, un clasificador de bosque aleatorio)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Hacer predicciones en el conjunto de prueba
        y_pred = model.predict(X_test)

        # Calcular la precisión del modelo
        accuracy = accuracy_score(y_test, y_pred)
        # Mostrar la precisión
        st.write(f"La precisión del modelo para la columna '{selected_column}' es: {accuracy}")

        # Hacer predicciones para todas las filas
        y_pred_all = model.predict(X)

        # Asignar las predicciones al DataFrame
        data[f'Predicted_{selected_column}'] = y_pred_all

        # Mostrar el conjunto de datos con las predicciones
        st.subheader(f"Conjunto de Datos con Predicciones para la columna '{selected_column}'")
        st.write("En esta tabla se muestran 2 columnas: la primera, son los datos reales, y la segunda, muestra los resultados de la aplicación del modelo de machine learning, (entre mayor sea la precisión, mayor va a ser la similitud de los valores)")
        st.dataframe(data[[selected_column, f'Predicted_{selected_column}']])

        # Crear una muestra de 10 para el heatmap
        st.set_option('deprecation.showPyplotGlobalUse', False)
        sample_size = 10
        X_test_sample = X_test.head(sample_size)
        y_test_sample = y_test.head(sample_size)
        y_pred_sample = model.predict(X_test_sample)
        # Calcular la matriz de confusión para el subconjunto
        cm = confusion_matrix(y_test_sample, y_pred_sample)
        # Mostrar la matriz de confusión como un heatmap
        st.subheader(f"Matriz de Confusión (Muestra de 10) para la columna '{selected_column}'")
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, square=True)
        plt.xlabel("Predicciones")
        plt.ylabel("Valores Reales")
        st.pyplot()

        
    else:
        st.warning("No se han cargado datos todavía.")
    return True
