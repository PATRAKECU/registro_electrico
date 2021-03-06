import streamlit as st 
import pandas as pd 
import lasio
import altair as alt
import matplotlib.pyplot as plt
from PIL import Image
from io import StringIO
#Nombre del proyecto
st.title("An谩lisis de Registro de Pozos")
# Men煤 de la aplicaci贸n
st.sidebar.title("Men煤 de opciones")
menu = st.sidebar.radio("Seleccione una de las siguientes opciones", ("馃彔 Inicio","馃搫 Informaci贸n","馃搳 An谩lisis de Datos","馃捁 Visualizaci贸n de Datos"))
# Algoritmo de las opciones
if menu == "馃彔 Inicio":
	with st.expander("Intrucciones de la aplicaci贸n"):
		st.write(""" 

			1- Cargar el archivo .las que contenga el registro de pozo.

			2- Ingresar los par谩metros necesarios para evaluar las formaciones.

			3- Visualizar e interpretar los datos.

			""")
	with st.expander("Descripci贸n de las secciones"):
		st.write("""
    	
    		
			Inicio: En la secci贸n Inicio encontramos instrucciones para el uso de la aplicaci贸n y datos del autor.
			Informaci贸n: En esta secci贸n se podr谩 cargar el archivo que contenga al registro y visualizar datos importantes del mismo.
			An谩lisis de Datos: Presenta una r谩pido an谩lisis estad铆stico de los datos disponibles y se definen las zonas de inter茅s del registro.
			Visualizaci贸n de Datos: Se visualizan las cruvas generadas por los registros analizados.


			""")
	with st.expander("Informaci贸n del autor"):
		st.info("Patricio Agurto, ingeniero de petr贸leos, pato777771@gmail.com, 0983438470")
archivo_las = st.sidebar.file_uploader("Cargar archivo LAS" , key=None)
		
if archivo_las is None:
	st.write("Suba un archivo con extenci贸n .las")

if archivo_las is not None:
	bytes_data = archivo_las.read()
	str_io = StringIO(bytes_data.decode('Windows-1252'))
	las_file = lasio.read(str_io)
	df = las_file.df()
	df['DEPTH'] = df.index
if menu == "馃搫 Informaci贸n":
	
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
			st.write("Pa铆s:",pais)
			st.write("Campo:",campo)
			st.write("Provincia:",provincia)
			st.write("Compa帽铆a:",compania)
			st.write("Este registro fue medido desde una profundidad de :", profundidad_min , "[ft]")
			st.write("Este registro fue medido hasta una profundidad de :", profundidad_max , "[ft]")
			st.write("n煤mero de columnas",n_columnas)
			st.write("n煤mero de filas",n_filas)
			try:
				df = pd.DataFrame(a)
			except:
				pass
				#st.write("no existe DataFrame")

if menu == "馃搳 An谩lisis de Datos":
	with st.expander("Estad铆sticas"):
		df_estadisticas = df.describe()
		st.write(df_estadisticas)
	with st.expander("Zonas de inter茅s"):
		columna1,columna2=st.columns(2)
		with columna1:
			limite_superior_z1=st.number_input("Ingrese el l铆mite superior zona 1",min_value=0.00,max_value=15000.00,value=10000.00)
			limite_inferior_z1=st.number_input("Ingrese el l铆mite inferior zona 1",min_value=0.00,max_value=15000.00,value=10500.00)
			df_zona_1 = df[limite_superior_z1:limite_inferior_z1]
			st.header("Zona 1")
			st.write(df_zona_1)
		with columna2:
			limite_superior_z2=st.number_input("Ingrese el l铆mite superior zona 2",min_value=0.00,max_value=15000.00,value=10000.00)
			limite_inferior_z2=st.number_input("Ingrese el l铆mite inferior zona 2",min_value=0.00,max_value=15000.00,value=10500.00)
			df_zona_2 = df[limite_superior_z2:limite_inferior_z2]
			st.header("Zona 2")
			st.write(df_zona_2)
if menu == "馃捁 Visualizaci贸n de Datos":
	lista_columnas = list(df.columns)
	seleccion_columnas = st.selectbox("Seleccione las columnas del registro",options=lista_columnas)
	grafico1= alt.Chart(df).mark_line().encode(x="DEPTH",y=seleccion_columnas)
	st.altair_chart(grafico1)