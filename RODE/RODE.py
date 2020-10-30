import sys
import time
from os import *
import sqlite3
import requests
from requests import exceptions
import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets

from source_rc import *
from style import *


class main(QDialog):
	def __init__(self, parent = None):
		super(main, self).__init__()
		#self.setObjectName("Dialog")
		self.setWindowTitle("Regristo de deudores")
		self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
		self.setWindowIcon(QIcon(":/Icono/img/calendar.png"))
		self.setFixedSize(654, 490)  
		self.setStyleSheet("QDialog{\n"
		"background-color: #fff}")
		self.initUi()
		self.mostrar_datos()
		self._timer = QTimer()
		self._timer.singleShot(5000, self.valor_dolar)
		#self.valor_dolar

	def initUi(self):
		self.shadow  = QGraphicsDropShadowEffect()        
		self.shadow.setBlurRadius(15)

		#Frame title
		self.frame_title = QFrame(self)
		self.frame_title.setGeometry(QRect(0,0,653,71))
		self.frame_title.setStyleSheet(style_frame_title)

		self.label_title = QLabel(self.frame_title)
		self.label_title.setGeometry(QRect(0,0,491,71))
		self.label_title.setAlignment(Qt.AlignCenter)
		self.label_title.setText("Registro de deudores")
		self.label_title.setStyleSheet(style_label_title)
		##########

		#Label de precios

		self.label_copias = QLabel(self.frame_title)
		self.label_copias.setGeometry(QRect(460,5,161,21))
		self.label_copias.setAlignment(Qt.AlignCenter)
		self.label_copias.setText("")

		self.label_impresiones = QLabel(self.frame_title)
		self.label_impresiones.setGeometry(QRect(458,25,191,21))
		self.label_impresiones.setAlignment(Qt.AlignCenter)
		self.label_impresiones.setText("")

		self.label_internet = QLabel(self.frame_title)
		self.label_internet.setGeometry(QRect(460,45,191,21))
		self.label_internet.setAlignment(Qt.AlignCenter)
		self.label_internet.setText("")

		#################

		#Frame menu
		self.frame_menu = QFrame(self)
		self.frame_menu.setGeometry(QRect(0,70,91,421))
		self.frame_menu.setStyleSheet(style_frame_menu)

		self.button_actualizar = QPushButton(self.frame_menu)
		self.button_actualizar.setGeometry(QRect(20,11,24,24))
		self.button_actualizar.setStyleSheet(style_actualizar)
		self.button_actualizar.setToolTip("Click para actualizar tabla")
		self.button_actualizar.setIcon(QIcon(":/Recargar/img/Recargar.png"))
		self.button_actualizar.setIconSize(QSize(26,26))

		self.button_actualizar_dolar = QPushButton(self.frame_menu)
		self.button_actualizar_dolar.setGeometry(QRect(50,10,24,24))
		self.button_actualizar_dolar.setStyleSheet(style_actualizar)
		self.button_actualizar_dolar.setToolTip("Actualizar tasa de intercambio del dolar")
		self.button_actualizar_dolar.setIcon(QIcon(":/Dolar_recarga/img/Recargar_dolar.png"))
		self.button_actualizar_dolar.setIconSize(QSize(20,20))



		self.button_agregar = QPushButton(self.frame_menu)
		self.button_agregar.setGeometry(QRect(5,160,81,25))
		self.button_agregar.setStyleSheet(style_eliminar_agregar)
		self.button_agregar.setIcon(QIcon(":/Agregar/img/Lapiz_negro.png"))
		self.button_agregar.setText("Agregar")
		self.button_agregar.setIconSize(QSize(16,16))

		self.button_eliminar = QPushButton(self.frame_menu)
		self.button_eliminar.setGeometry(QRect(5,200,81,25))
		self.button_eliminar.setStyleSheet(style_eliminar_agregar)
		self.button_eliminar.setIcon(QIcon(":/Eliminar/img/Papelera_negro.png"))
		self.button_eliminar.setText("Eliminar")
		self.button_eliminar.setIconSize(QSize(19,19))
		##########


		#Frame menu_dos
		self.frame_menu_dos = QFrame(self)
		self.frame_menu_dos.setGeometry(QRect(91,70,564,41))
		self.frame_menu_dos.setStyleSheet(style_menu_dos)

		self.line_edit_buscar = QLineEdit(self.frame_menu_dos)
		self.line_edit_buscar.setGeometry(QRect(20,7,151,25))
		self.line_edit_buscar.setObjectName("Enter")
		self.line_edit_buscar.setPlaceholderText("Ingresa nombre")
		self.line_edit_buscar.setStyleSheet(style_line_edit)

		self.button_buscar = QPushButton(self.frame_menu_dos)
		self.button_buscar.setGeometry(QRect(150,7,21,25))
		self.button_buscar.setStyleSheet(style_eliminar_agregar)
		self.button_buscar.setObjectName("Buscar")
		self.button_buscar.setIcon(QIcon(":/Buscar/img/Lupa_negra.png"))
		self.button_buscar.setText("")
		self.button_buscar.setIconSize(QSize(16,16))

		#self.menu_buscar = QMenu()
		self.button_buscar_por = QPushButton(self.frame_menu_dos)
		self.button_buscar_por.setGeometry(QRect(200,7,81,25))
		self.button_buscar_por.setStyleSheet(style_eliminar_agregar)
		self.button_buscar_por.setText("Buscar por: ")
		#self.menu_buscar.setStyleSheet(Style_button_menu)
		#self.buscar_por = self.menu_buscar.addAction("Buscar por fecha", self.mostrar_agregar)
		#self.button_buscar_por.setMenu(self.menu_buscar)
		self.button_buscar_por.clicked.connect(self.aun_no)

		#resp = requests.get('https://s3.amazonaws.com/dolartoday/data.json')
		#a = json.loads(resp.text)
		#usd = a['USD']
		#dolar = usd['transferencia']


		self.label_ultimo_registro = QLabel(self.frame_menu_dos)
		self.label_ultimo_registro.setGeometry(QRect(310,10,231,20))
		self.label_ultimo_registro.setText("")
		self.label_ultimo_registro.setAlignment(Qt.AlignCenter)
		self.label_ultimo_registro.setStyleSheet(style_ultimo_registro)
		###############

		#Tabla de registro

		nombreColumnas = ("ID", "Nombre", "Descripción de deuda",
		 "Monto de deuda", "Fecha", "Hora")
		self.Tabla_registro = QTableWidget(self)
		self.Tabla_registro.setToolTip("Click para ver usuario")
		self.Tabla_registro.setGeometry(QRect(97,120,552,361))
		self.Tabla_registro.setStyleSheet(style_qtable_contenido)
		self.Tabla_registro.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.Tabla_registro.setDragDropOverwriteMode(False)
		self.Tabla_registro.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.Tabla_registro.setSelectionMode(QAbstractItemView.SingleSelection)
		self.Tabla_registro.setTextElideMode(Qt.ElideRight)
		self.Tabla_registro.setWordWrap(False)
		self.Tabla_registro.setSortingEnabled(False)
		self.Tabla_registro.setColumnCount(6)
		self.Tabla_registro.setRowCount(0)
		self.Tabla_registro.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter|Qt.AlignVCenter|
														  Qt.AlignCenter)
		self.Tabla_registro.horizontalHeader().setHighlightSections(False)
		self.Tabla_registro.horizontalHeader().setStretchLastSection(True)
		self.Tabla_registro.verticalHeader().setVisible(False)
		self.Tabla_registro.setAlternatingRowColors(False)
		self.Tabla_registro.verticalHeader().setDefaultSectionSize(20)
		self.Tabla_registro.setHorizontalHeaderLabels(nombreColumnas)
		self.Tabla_registro.itemDoubleClicked.connect(self.Item_click)

		for indice, ancho in enumerate((50, 100, 300, 100,100,80), start=0):
			self.Tabla_registro.setColumnWidth(indice, ancho)

		##################

		#Registrar un nuevo deudor
		self.frame_registro_nuevo = QFrame(self)
		self.frame_registro_nuevo.setGeometry(QRect(-1000,160,151,312))
		self.frame_registro_nuevo.setStyleSheet(style_menu_dos)

		self.frame_registro_nuevo.setGraphicsEffect(self.shadow)

		self.label_nombre_apellido = QLabel(self.frame_registro_nuevo)
		self.label_nombre_apellido.setGeometry(QRect(10,10,131,20))
		self.label_nombre_apellido.setText("Nombre y Apellido")
		self.label_nombre_apellido.setAlignment(Qt.AlignCenter)
		self.label_nombre_apellido.setStyleSheet(style_ultimo_registro)

		self.line_edit_nombre_apellido = QLineEdit(self.frame_registro_nuevo)
		self.line_edit_nombre_apellido.setGeometry(QRect(10,35,131,20))
		self.line_edit_nombre_apellido.setStyleSheet(style_line_edit)
		self.line_edit_nombre_apellido.setPlaceholderText("Ingresa aquí")
		self.line_edit_nombre_apellido.setToolTip("Ingresa el nombre y apellido de\nla persona deudora")


		self.label_descripcion_deuda = QLabel(self.frame_registro_nuevo)
		self.label_descripcion_deuda.setGeometry(QRect(10,70,131,20))
		self.label_descripcion_deuda.setText("Descripción de deuda")
		self.label_descripcion_deuda.setAlignment(Qt.AlignCenter)
		self.label_descripcion_deuda.setStyleSheet(style_ultimo_registro)

		self.text_edit_descripcion = QTextEdit(self.frame_registro_nuevo)
		self.text_edit_descripcion.setGeometry(QRect(10,95,131,111))
		self.text_edit_descripcion.setPlaceholderText("Ingrese la descrición aquí")
		self.text_edit_descripcion.setToolTip("Describa de forma breve y detallada\nla deuda de la persona")
		self.text_edit_descripcion.setStyleSheet(style_text_edit)

		self.label_monto_deuda = QLabel(self.frame_registro_nuevo)
		self.label_monto_deuda.setGeometry(QRect(10,220,131,20))
		self.label_monto_deuda.setText("Monto de deuda")
		self.label_monto_deuda.setAlignment(Qt.AlignCenter)
		self.label_monto_deuda.setStyleSheet(style_ultimo_registro)

		self.line_edit_monto = QLineEdit(self.frame_registro_nuevo)
		self.line_edit_monto.setGeometry(QRect(10,245,131,20))
		self.line_edit_monto.setStyleSheet(style_line_edit)
		self.line_edit_monto.setText("$")
		self.line_edit_monto.setPlaceholderText("Ingresa aquí")
		self.line_edit_monto.setToolTip("Ingresa el monto de\nla deuda")

		#self.line_edit_monto.setValidator(QRegExpValidator(QRegExp("[0-9]+[,-.]"),self.line_edit_monto))

		self.button_cancelar = QPushButton(self.frame_registro_nuevo)
		self.button_cancelar.setGeometry(QRect(50,280,22,22))
		self.button_cancelar.setStyleSheet(style_button_guardar)
		self.button_cancelar.setIcon(QIcon(":/Cancelar/img/Cancelar_rojo.png"))

		self.button_guardar = QPushButton(self.frame_registro_nuevo)
		self.button_guardar.setGeometry(QRect(80,280,22,22))
		self.button_guardar.setStyleSheet(style_button_guardar)
		self.button_guardar.setIcon(QIcon(":/Check/img/Check_azul.png"))
		##########################

		#Visualizar deudor
		self.frame_visualizar = QFrame(self)
		self.frame_visualizar.setGeometry(QRect(290,140,0,0))
		self.frame_visualizar.setStyleSheet(style_menu_dos)
		self.frame_visualizar.setGraphicsEffect(self.shadow)

		self.label_nombre_apellido_vz = QLabel(self.frame_visualizar)
		self.label_nombre_apellido_vz.setGeometry(QRect(10,10,131,20))
		self.label_nombre_apellido_vz.setText("Nombre y Apellido")
		self.label_nombre_apellido_vz.setAlignment(Qt.AlignCenter)
		self.label_nombre_apellido_vz.setStyleSheet(style_ultimo_registro)

		self.line_edit_nombre_apellido_vz = QLineEdit(self.frame_visualizar)
		self.line_edit_nombre_apellido_vz.setGeometry(QRect(10,35,131,20))
		self.line_edit_nombre_apellido_vz.setStyleSheet(style_line_edit)
		self.line_edit_nombre_apellido_vz.setPlaceholderText("Ingresa aquí")
		self.line_edit_nombre_apellido_vz.setToolTip("Ingresa el nombre y apellido de\nla persona deudora")


		self.label_descripcion_deuda_vz = QLabel(self.frame_visualizar)
		self.label_descripcion_deuda_vz.setGeometry(QRect(10,70,131,20))
		self.label_descripcion_deuda_vz.setText("Descripción de deuda")
		self.label_descripcion_deuda_vz.setAlignment(Qt.AlignCenter)
		self.label_descripcion_deuda_vz.setStyleSheet(style_ultimo_registro)

		self.text_edit_descripcion_vz = QTextEdit(self.frame_visualizar)
		self.text_edit_descripcion_vz.setGeometry(QRect(10,95,131,111))
		self.text_edit_descripcion_vz.setPlaceholderText("Ingrese la descrición aquí")
		self.text_edit_descripcion_vz.setToolTip("Describa de forma breve y detallada\nla deuda de la persona")
		self.text_edit_descripcion_vz.setStyleSheet(style_text_edit)

		self.label_monto_deuda_vz = QLabel(self.frame_visualizar)
		self.label_monto_deuda_vz.setGeometry(QRect(10,220,131,20))
		self.label_monto_deuda_vz.setText("Monto de deuda")
		self.label_monto_deuda_vz.setAlignment(Qt.AlignCenter)
		self.label_monto_deuda_vz.setStyleSheet(style_ultimo_registro)

		self.line_edit_monto_vz = QLineEdit(self.frame_visualizar)
		self.line_edit_monto_vz.setGeometry(QRect(10,245,131,20))
		self.line_edit_monto_vz.setStyleSheet(style_line_edit)
		self.line_edit_monto_vz.setPlaceholderText("Ingresa aquí")
		self.line_edit_monto_vz.setToolTip("Ingresa el monto de\nla deuda")
		#self.line_edit_monto_vz.setValidator(QRegExpValidator(QRegExp("[0-9]+"),self.line_edit_monto))

		self.button_cancelar_vz = QPushButton(self.frame_visualizar)
		self.button_cancelar_vz.setGeometry(QRect(50,280,22,22))
		self.button_cancelar_vz.setStyleSheet(style_button_guardar)
		self.button_cancelar_vz.setIcon(QIcon(":/Cancelar/img/Cancelar_rojo.png"))

		self.button_guardar_vz = QPushButton(self.frame_visualizar)
		self.button_guardar_vz.setGeometry(QRect(80,280,22,22))
		self.button_guardar_vz.setStyleSheet(style_button_guardar)
		self.button_guardar_vz.setIcon(QIcon(":/Check/img/Check_azul.png"))		

		##################

		##############################################################
		#Eventos click
		self.line_edit_buscar.returnPressed.connect(self.buscar_datos)
		self.button_buscar.clicked.connect(self.buscar_datos)

		self.button_agregar.clicked.connect(self.mostrar_agregar)
		self.button_eliminar.clicked.connect(self.eliminar_datos)

		self.button_cancelar.clicked.connect(self.funtion_cancelar)

		self.button_guardar.clicked.connect(self.Creater_base_datos)
		self.button_guardar.clicked.connect(self.insert_datos_db)

		self.button_actualizar.clicked.connect(self.mostrar_datos)

		self.button_actualizar_dolar.clicked.connect(self.valor_dolar)
		self.button_actualizar_dolar.clicked.connect(self.Precio_productos)		

		self.button_cancelar_vz.clicked.connect(self.funtion_cancelar_vz)
		self.button_guardar_vz.clicked.connect(self.Update_datos)
		##############
	def aun_no(self):
		QMessageBox.critical(self, "Upps!", "Aun no se ha agregado ninguna funcionalidad a este boton!.",
							QMessageBox.Ok)

	def valor_dolar(self):
		try:
			resp = requests.get('https://s3.amazonaws.com/dolartoday/data.json',timeout = 3)
			print("Connected")
			a = json.loads(resp.text)
			usd = a['USD']
			dolar = usd['transferencia']
			self.label_ultimo_registro.setText("Valor del dolar actual: 1$ = "+str(dolar)+"Bs")
			self.Precio_productos(dolar)
			print(dolar)
		except exceptions.ConnectionError:
			QMessageBox.critical(self, "Error de conexión", "Erro al conectar con DolarToday vuelva a cargar o \nComprueba tu conexión a internet.",
											 QMessageBox.Ok)

			self.label_copias.setText('Precio de las copias: No conecto ')
			self.label_impresiones.setText('Precio de las impresiones: No conecto ')
			self.label_internet.setText('Precio del uso de internet: No conecto')
			self.label_ultimo_registro.setText("Valor del dolar actual: 1$ = No conecto")
			print("Not connected")


	def Precio_productos(self,dolar):
		if dolar:
			#print("AAAA",dolar)
			copias = 0.17
			impresiones = 0.18
			internet = 0.16

			precio_copias = round(dolar*copias,2)
			precio_impresiones = round(dolar*impresiones,2)
			precio_internet = round(dolar*internet,2)

			#r_1 = round(precio_copias,2)
			#print("El r",precio_copias)
			#r_2 = precio_impresiones
			#r_3 = precio_internet
			self.label_copias.setText('Precio de las copias: '+str(precio_copias)+"Bs")
			self.label_impresiones.setText('Precio de las impresiones: '+str(precio_impresiones)+"Bs")
			self.label_internet.setText('Precio del uso de internet: '+str(precio_internet)+"Bs")



	def Creater_base_datos(self):
		
			if not QFile.exists("Base de datos"):
				makedirs("Base de datos")

			if QFile.exists("Base de datos"):
				if QFile.exists('Base de datos/DB_DEUDORES.db'):
					None
				else:
					try:
						with sqlite3.connect('Base de datos/DB_DEUDORES.db') as db:
							cursor = db.cursor()


						cursor.execute("CREATE TABLE IF NOT EXISTS USUARIOS_DEUDORES (ID INTEGER PRIMARY KEY, NOMBRE_APELLIDO TEXT,"
										"DESCRIPCION_DEUDA TEXT, MONTO TEXT, FECHA TEXT, HORA TEXT)")

						db.commit()     
						cursor.close()
						db.close()

					except Exception as e:
						print(e)
						QMessageBox.critical(self, "Nuevo registro", "Error desconocido.",
											 QMessageBox.Ok)
			else:
				None

	def insert_datos_db(self):

		nombre_apellido = self.line_edit_nombre_apellido.text()
		descripcion_deuda = self.text_edit_descripcion.toPlainText()
		monto_deudor = self.line_edit_monto.text()

		if not nombre_apellido: 
			self.line_edit_nombre_apellido.setFocus()
		elif not descripcion_deuda:
			self.text_edit_descripcion.setFocus()
		elif not monto_deudor:
			self.line_edit_monto.setFocus()

		else:
			if QFile.exists("Base de datos/DB_DEUDORES.db"):
							conexion = sqlite3.connect('Base de datos/DB_DEUDORES.db')
							cursor = conexion.cursor()

							try:
								# Variables de tiempo insertadas en base de datos
								hora = time.strftime("%I:%M:%S %p")
								fecha_actual = time.strftime("%d/%m/%y")

								datos_insertar = [nombre_apellido, descripcion_deuda,monto_deudor,
												fecha_actual, hora]

								cursor.execute("INSERT INTO USUARIOS_DEUDORES (NOMBRE_APELLIDO,"
												"DESCRIPCION_DEUDA, MONTO, FECHA, HORA)"
												"VALUES(?,?,?,?,?)",datos_insertar)


								conexion.commit()       
								cursor.close()
								conexion.close()
								QMessageBox.information(self, "Nuevo deudor", "Deudor registrado.",QMessageBox.Ok)

								self.line_edit_nombre_apellido.clear()
								self.text_edit_descripcion.clear()
								self.line_edit_monto.clear()
								self.ocultar_agregar()

							
							except Exception as e:
								print(e)
								QMessageBox.critical(self, "Nuevo deudor", "Error desconocido.",
											QMessageBox.Ok)

								

			else:
				None



	def Update_datos(self):

		nombre_apellido_vz = self.line_edit_nombre_apellido_vz.text()
		descripcion_deuda_vz = self.text_edit_descripcion_vz.toPlainText()
		monto_deudor_vz = self.line_edit_monto_vz.text()

		if QFile.exists("Base de datos/DB_DEUDORES.db"):
			conexion = sqlite3.connect('Base de datos/DB_DEUDORES.db')
			cursor = conexion.cursor()
			try:
				hora_vz = time.strftime("%I:%M:%S %p")
				fecha_actual_vz = time.strftime("%d/%m/%y")

				datos_insertar = [nombre_apellido_vz, descripcion_deuda_vz, monto_deudor_vz,
								fecha_actual_vz, hora_vz, self.datos[0]]
 
				print("Estos son los datos:",datos_insertar)


				cursor.execute("UPDATE USUARIOS_DEUDORES SET NOMBRE_APELLIDO = ?, DESCRIPCION_DEUDA = ?,"
											"MONTO = ?, FECHA = ?, HORA = ? WHERE ID = ?", datos_insertar)
				conexion.commit()       
				cursor.close()
				conexion.close()
				QMessageBox.information(self, "Actualización de deudor", "Deudor actualizado.",QMessageBox.Ok)


			except Exception as e:
					print(e)
					QMessageBox.critical(self, "Actualización de deudor", "Error desconocido.",
											QMessageBox.Ok)
		self.line_edit_nombre_apellido_vz.clear()
		self.text_edit_descripcion_vz.clear()
		self.line_edit_monto_vz.clear()
		self.ocultar_visualizar()


	def buscar_datos(self):

		try:
			widget = self.sender().objectName()

			if widget in ("Enter", "Buscar"):
				cliente = " ".join(self.line_edit_buscar.text().split()).lower()

				if len(cliente)== 0:
					QMessageBox.critical(self, "Error", "No se ha escrito nada",
												 QMessageBox.Ok)
				if cliente:
					sql = "SELECT ID, NOMBRE_APELLIDO,DESCRIPCION_DEUDA, MONTO, FECHA, HORA FROM USUARIOS_DEUDORES WHERE NOMBRE_APELLIDO LIKE ?", ("%"+cliente+"%",)
				else:
					self.line_edit_buscar.setFocus()
					return
			else:
				self.line_edit_buscar.clear()
				sql = "SELECT * FROM USUARIOS_DEUDORES"

			if QFile.exists('Base de datos/DB_DEUDORES.db'):
				conexion = sqlite3.connect('Base de datos/DB_DEUDORES.db')
				cursor = conexion.cursor()
				print("Si")
					
				try:
					if widget in ("Enter", "Buscar"):
						cursor.execute(sql[0], sql[1])
						
					else:
						cursor.execute(sql)
						
					datosDevueltos = cursor.fetchall()
					conexion.close()

					self.Tabla_registro.clearContents()
					self.Tabla_registro.setRowCount(0)

					if datosDevueltos:
						fila = 0
						for datos in datosDevueltos:
							self.Tabla_registro.setRowCount(fila + 1)
				
							idDato = QTableWidgetItem(str(datos[0]))
							idDato.setTextAlignment(Qt.AlignCenter)
							
							self.Tabla_registro.setItem(fila, 0, idDato)
							self.Tabla_registro.setItem(fila, 1, QTableWidgetItem(datos[1]))
							self.Tabla_registro.setItem(fila, 2, QTableWidgetItem(datos[2]))
							self.Tabla_registro.setItem(fila, 3, QTableWidgetItem(datos[3]))
							self.Tabla_registro.setItem(fila, 4, QTableWidgetItem(datos[4]))
							self.Tabla_registro.setItem(fila, 5, QTableWidgetItem(datos[5]))

							fila += 1

					else:   
						QMessageBox.information(self, "Buscar deudor", "No se encontró ", QMessageBox.Ok)
				except Exception as e:
					print(e)
					conexion.close()
					QMessageBox.critical(self, "Buscar deudor", "Error desconocido.",
										 QMessageBox.Ok)
			else:
				QMessageBox.critical(self, "Buscar deudor", "No se encontró la base de datos.",
									 QMessageBox.Ok)

			self.line_edit_busqueda.setFocus()
		except AttributeError:
			pass


	def eliminar_datos(self):

		if QFile.exists("Base de datos/DB_DEUDORES.db"):

			msg = QMessageBox()
			#msg.setWindowIcon(QIcon('Imagenes-iconos/Icono_window.png'))
			msg.setText("¿Está seguro de querer eliminar este deudor?")
			msg.setIcon(QMessageBox.Question)
			msg.setWindowTitle("Eliminar Usuario")
			msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

			button_si = msg.button(QMessageBox.Yes)
			button_si.setText("Si")
			button_si.setIcon(QIcon("I:/Check/img/Check_azul.png"))
			button_si.setIconSize(QSize(13,13))
			button_si.setStyleSheet("QPushButton:hover{background:rgb(0, 170, 255);}\n"
			"QPushButton{background:#343a40;\n"
			"}")

			button_no = msg.button(QMessageBox.No)
			button_no.setIcon(QIcon(":/Cancelar/img/Cancelar_rojo.png"))
			button_no.setIconSize(QSize(13,13))
			button_no.setStyleSheet("QPushButton:hover{background:rgb(0, 170, 255);}\n"
			"QPushButton{background:#343a40;}")

			msg.setStyleSheet("\n"
				"color:#ffffff;\n"
				"font-size:12px;\n"
				"background-color:#12191D;")

			if (msg.exec_() == QMessageBox.Yes):

				try:

					self.con = sqlite3.connect("Base de datos/DB_DEUDORES.db")

					self.cursor = self.con.cursor()
		

					self.Tabla_registro.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
					ID = self.Tabla_registro.selectedIndexes()[0].data()
					print("has clickeado en", ID)
					
					# Primera Instancia
					query = 'DELETE  FROM USUARIOS_DEUDORES WHERE ID =?'
					self.cursor.execute(query, (ID,))
					self.con.commit()

					# Seleccionar fila
					self.Seleccion = self.Tabla_registro.selectedItems()
					# Borrar seleccionado
					self.Tabla_registro.removeRow(self.Tabla_registro.currentRow())

				except Exception as e:
					print(e)
					QMessageBox.critical(self, "Error", "No existen deudores para eliminar",
											 QMessageBox.Ok)

			else:
				pass    

		else:
			QMessageBox.critical(self, "Eliminar", "No se encontró la base de datos.   ",
											QMessageBox.Ok)







	def mostrar_datos(self):

		if QFile.exists("Base de datos/DB_DEUDORES.db"):

			try: 
				self.con = sqlite3.connect("Base de datos/DB_DEUDORES.db")
				self.cursor = self.con.cursor()

				self.cursor.execute("SELECT ID, NOMBRE_APELLIDO, DESCRIPCION_DEUDA, MONTO, FECHA,HORA FROM USUARIOS_DEUDORES ORDER BY ID")

				datos_Devueltos = self.cursor.fetchall()
				self.Tabla_registro.clearContents()
				self.Tabla_registro.setRowCount(0)
				print(datos_Devueltos)

				if datos_Devueltos:
					row = 0

					for datos in datos_Devueltos:
						self.Tabla_registro.setRowCount(row + 1)
						
						idDato = QTableWidgetItem(str(datos[0]))
						idDato.setTextAlignment(Qt.AlignCenter)

						self.Tabla_registro.setItem(row, 0, idDato)
						self.Tabla_registro.setItem(row, 1, QTableWidgetItem(datos[1]))
						self.Tabla_registro.setItem(row, 2, QTableWidgetItem(datos[2]))
						self.Tabla_registro.setItem(row, 3, QTableWidgetItem(datos[3]))
						self.Tabla_registro.setItem(row, 4, QTableWidgetItem(datos[4]))
						self.Tabla_registro.setItem(row, 5, QTableWidgetItem(datos[5]))
						row +=1

				else:   
					QMessageBox.information(self, "Buscar deudor", "No se encontraron deudores", QMessageBox.Ok)

			except Exception as e:
				print(e)
				QMessageBox.critical(self, "Error", "No se ha podido conectar a la base de datos o no existe la base de datos",
											 QMessageBox.Ok)
		else:
			QMessageBox.critical(self, "Buscar deudores", "No se encontro la base de datos.",
								 QMessageBox.Ok)





	def Item_click(self,celda):
		celda = self.Tabla_registro.selectedItems()

		if celda:
			indice = celda[0].row()
			dato = [self.Tabla_registro.item(indice,i).text()for i in range(5)]

			dato_buscar = dato[0]

			if dato_buscar:
				sql = "SELECT * FROM USUARIOS_DEUDORES WHERE ID LIKE ?", (dato_buscar,)
				print("Si")
			else:
				print("NO")

			if QFile.exists("Base de datos/DB_DEUDORES.db"):
				conexion = sqlite3.connect("Base de datos/DB_DEUDORES.db")
				cursor = conexion.cursor()

				try:
					cursor.execute(sql[0],sql[1])
					datosdevueltos = cursor.fetchall()
					for dato in datosdevueltos:
						indice = dato[0]

					self.mostrar_visualizar(dato)
					self.datos = dato

					conexion.close()
				except Exception as e:
					print("A1:",e)
		else:
			print("Error")





	def visualizar_dudor(self):

		self.animacionMostar = QPropertyAnimation(self.frame_registro_nuevo,b"geometry")
		self.animacionMostar.finished.connect(lambda: (self.frame_registro_nuevo))

		self.animacionMostar.setDuration(500)
		self.animacionMostar.setStartValue(QRect(-1500, 160, 151,312))
		self.animacionMostar.setEndValue(QRect(90, 160, 151, 312))
		self.animacionMostar.start(QAbstractAnimation.DeleteWhenStopped)


	#funcion de la ventana agregar nuevo deudor
	def funtion_cancelar(self):
		msg = QMessageBox()
		msg.setText("¿Estás seguro de que desea cancelar?")
		msg.setIcon(QMessageBox.Question)
		msg.setWindowTitle("Cancelar registro")
		msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

		button_si = msg.button(QMessageBox.Yes)
		button_si.setText("Si")
		button_si.setIcon(QIcon(":/Check/img/Check_azul.png"))
		button_si.setIconSize(QSize(13,13))
		button_si.setStyleSheet("QPushButton:hover{background:rgb(0, 170, 255);}\n"
		"QPushButton{background:#343a40;\n"
		"}")


		button_no = msg.button(QMessageBox.No)
		button_no.setIcon(QIcon(":/Cancelar/img/Cancelar_rojo.png"))
		button_no.setIconSize(QSize(13,13))
		button_no.setStyleSheet("QPushButton:hover{background:rgb(0, 170, 255);}\n"
		"QPushButton{background:#343a40;}")

		msg.setStyleSheet("\n"
			"color:#ffffff;\n"
			"font-size:12px;\n"
			"background-color:#12191D;")

		if (msg.exec_() == QMessageBox.Yes):
			self.ocultar_agregar()
		else:
			pass

	def mostrar_agregar(self):
		self.animacionMostar = QPropertyAnimation(self.frame_registro_nuevo,b"geometry")
		self.animacionMostar.finished.connect(lambda: (self.frame_registro_nuevo))

		self.animacionMostar.setDuration(500)
		self.animacionMostar.setStartValue(QRect(-1500, 160, 151,312))
		self.animacionMostar.setEndValue(QRect(90, 160, 151, 312))
		self.animacionMostar.start(QAbstractAnimation.DeleteWhenStopped)

	def ocultar_agregar(self):

		self.animacionMostar = QPropertyAnimation(self.frame_registro_nuevo,b"geometry")
		self.animacionMostar.finished.connect(lambda: (self.frame_registro_nuevo))

		self.animacionMostar.setDuration(500)
		self.animacionMostar.setStartValue(QRect(90, 160, 151, 312))
		self.animacionMostar.setEndValue(QRect(-1500, 160, 151, 312))
		self.animacionMostar.start(QAbstractAnimation.DeleteWhenStopped)








	def funtion_cancelar_vz(self):
		msg = QMessageBox()
		msg.setText("¿Estás seguro de que desea cancelar?")
		msg.setIcon(QMessageBox.Question)
		msg.setWindowTitle("Cancelar registro")
		msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

		button_si = msg.button(QMessageBox.Yes)
		button_si.setText("Si")
		button_si.setIcon(QIcon(":/Check/img/Check_azul.png"))
		button_si.setIconSize(QSize(13,13))
		button_si.setStyleSheet("QPushButton:hover{background:rgb(0, 170, 255);}\n"
		"QPushButton{background:#343a40;\n"
		"}")


		button_no = msg.button(QMessageBox.No)
		button_no.setIcon(QIcon(":/Cancelar/img/Cancelar_rojo.png"))
		button_no.setIconSize(QSize(13,13))
		button_no.setStyleSheet("QPushButton:hover{background:rgb(0, 170, 255);}\n"
		"QPushButton{background:#343a40;}")

		msg.setStyleSheet("\n"
			"color:#ffffff;\n"
			"font-size:12px;\n"
			"background-color:#12191D;")

		if (msg.exec_() == QMessageBox.Yes):
			self.ocultar_visualizar()
		else:
			pass


	def mostrar_visualizar(self,dato):

		datos = dato
		self.line_edit_nombre_apellido_vz.setText(str(datos[1]))
		self.text_edit_descripcion_vz.setText(str(datos[2]))
		self.line_edit_monto_vz.setText(str(datos[3]))

		self.animacionMostar = QPropertyAnimation(self.frame_visualizar,b"geometry")
		self.animacionMostar.finished.connect(lambda: (self.frame_visualizar))

		self.animacionMostar.setDuration(200)
		self.animacionMostar.setStartValue(QRect(340, 250, 0,0))
		self.animacionMostar.setEndValue(QRect(290, 140, 151, 312))
		self.animacionMostar.start(QAbstractAnimation.DeleteWhenStopped)

	def ocultar_visualizar(self):

		self.animacionMostar = QPropertyAnimation(self.frame_visualizar,b"geometry")
		self.animacionMostar.finished.connect(lambda: (self.frame_visualizar))

		self.animacionMostar.setDuration(200)
		self.animacionMostar.setStartValue(QRect(290, 140, 151, 312))
		self.animacionMostar.setEndValue(QRect(340, 250, 0, 0))
		self.animacionMostar.start(QAbstractAnimation.DeleteWhenStopped)



if __name__ == '__main__':
	app = QApplication(sys.argv)
	Window = main()
	Window.show()
	app.exec_()

