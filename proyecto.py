import streamlit as st 
import pandas as pd 
import lasio
import altair as alt
import matplotlib.pyplot as plt
from PIL import Image
from io import StringIO
#Nombre del proyecto
st.title("Análisis de Registro de Pozos")
# Menú de la aplicación
st.sidebar.title("Menú de opciones")
menu = st.sidebar.radio("Seleccione una de las siguientes opciones", ("🏠 Inicio","📄 Información","📊 Análisis de Datos","💹 Visualización de Datos"))
# Algoritmo de las opciones
if menu == "🏠 Inicio":
	with st.expander("Intrucciones de la aplicación"):
		st.write(""" 

			1- Cargar el archivo .las que contenga el registro de pozo.

			2- Ingresar los parámetros necesarios para evaluar las formaciones.

			3- Visualizar e interpretar los datos.

			""")
	with st.expander("Descripción de las secciones"):
		st.write("""
    	
    		
			Inicio: En la sección Inicio encontramos instrucciones para el uso de la aplicación y datos del autor.
			Información: En esta sección se podrá cargar el archivo que contenga al registro y visualizar datos importantes del mismo.
			Análisis de Datos: Presenta una rápido análisis estadístico de los datos disponibles y se definen las zonas de interés del registro.
			Visualización de Datos: Se visualizan las cruvas generadas por los registros analizados.


			""")
	with st.expander("Información del autor"):
		st.info("Patricio Agurto, ingeniero de petróleos, pato777771@gmail.com, 0983438470")
archivo_las = st.sidebar.file_uploader("Cargar archivo LAS" , key=None)
		
if archivo_las is None:
	st.write("Suba un archivo con extención .las")

if archivo_las is not None:
	bytes_data = archivo_las.read()
	str_io = StringIO(bytes_data.decode('Windows-1252'))
	las_file = lasio.read(str_io)
	df = las_file.df()
	df['DEPTH'] = df.index
if menu == "📄 Información":
	
		with st.expander("Data Frame"):
			st.write(df)
			st.header("Lectura del registro")
			lista_columnas = list(df.columns)
			seleccion_columna = st.multiselect("Seleccione columnas del registro", options= lista_columnas)
			df_filtrado = df[seleccion_columna]
			st.write(df_filtrado)
		with st.expander("Datos del registro"):
			pais = las_file.header['Well'].COUNT.value
			campo = las_file.header['Well'].FLD.value
			provincia = las_file.header['Well'].PROV.value
			compania = las_file.header['Well'].COMP.value
			n_columnas = df.shape[1]
			n_filas = df.shape[0]
			profundidad_min = df.index.values[0]
			profundidad_max = df.index.values[-1]
			st.write("País:",pais)
			st.write("Campo:",campo)
			st.write("Provincia:",provincia)
			st.write("Compañía:",compania)
			st.write("Este registro fue medido desde una profundidad de :", profundidad_min , "[ft]")
			st.write("Este registro fue medido hasta una profundidad de :", profundidad_max , "[ft]")
			st.write("número de columnas",n_columnas)
			st.write("número de filas",n_filas)
			try:
				df = pd.DataFrame(a)
			except:
				pass
				#st.write("no existe DataFrame")

if menu == "📊 Análisis de Datos":
	with st.expander("Estadísticas"):
		df_estadisticas = df.describe()
		st.write(df_estadisticas)
	with st.expander("Zonas de interés"):
		columna1,columna2=st.columns(2)
		with columna1:
			limite_superior_z1=st.number_input("Ingrese el límite superior zona 1",min_value=0.00,max_value=15000.00,value=10000.00)
			limite_inferior_z1=st.number_input("Ingrese el límite inferior zona 1",min_value=0.00,max_value=15000.00,value=10500.00)
			df_zona_1 = df[limite_superior_z1:limite_inferior_z1]
			st.header("Zona 1")
			st.write(df_zona_1)
		with columna2:
			limite_superior_z2=st.number_input("Ingrese el límite superior zona 2",min_value=0.00,max_value=15000.00,value=10000.00)
			limite_inferior_z2=st.number_input("Ingrese el límite inferior zona 2",min_value=0.00,max_value=15000.00,value=10500.00)
			df_zona_2 = df[limite_superior_z2:limite_inferior_z2]
			st.header("Zona 2")
			st.write(df_zona_2)
if menu == "💹 Visualización de Datos":
	lista_columnas = list(df.columns)
	seleccion_columnas = st.selectbox("Seleccione las columnas del registro",options=lista_columnas)
	grafico1= alt.Chart(df).mark_line().encode(x="DEPTH",y=seleccion_columnas)
	st.altair_chart(grafico1)