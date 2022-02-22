# App Covid

''' IMPORTS '''

import csv
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainter
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QComboBox, QLabel
from PySide6.QtWidgets import QHBoxLayout, QToolBar, QLineEdit
from PySide6.QtWidgets import QPushButton, QStatusBar
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
import os
import sqlite3
from sqlite3 import Error
from PySide6.QtCharts import (QBarSet, QChart, QChartView,
                              QStackedBarSeries, QBarCategoryAxis,
                              QLineSeries)
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

''' Carpeta donde alojaremos la ruta,
    para poder crear la base de datos,
    y muchas otras funciones,
    en la carpeta correcta.'''

carpeta = os.path.dirname(__file__)

''' Intentamos conectarnos a la base de datos,
    en caso de que no se pueda conectar,
    nos creara la base de datos. Controlamos la excepción,
    en caso de que no se pueda conectar.'''

try:
    sqliteConnection = sqlite3.connect(carpeta + '/usuarios.db')
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")
except Error as error:
    print("Failed to connect", error)


class WebWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Web Covid GVA')

        self.setFixedHeight(900)
        self.setFixedWidth(1600)

        self.toolBar = QToolBar()
        self.addToolBar(self.toolBar)

        self.iconoExit = os.path.join(carpeta, "recursos/exit.png")

        self.exit_button = QAction(QIcon(self.iconoExit), "&Close", self)
        self.exit_button.setStatusTip("This is your Exit Button")
        self.exit_button.triggered.connect(self.closeWeb)

        self.toolBar.addAction(self.exit_button)

        self.toolBar.setMovable(False)

        self.addressLineEdit = QLineEdit()
        self.addressLineEdit.returnPressed.connect(self.load)

        self.webEngineView = QWebEngineView()
        self.setCentralWidget(self.webEngineView)
        initialUrl = 'https://coronavirus.san.gva.es/es/estadisticas'
        self.addressLineEdit.setText(initialUrl)
        self.webEngineView.load(QUrl(initialUrl))
        self.webEngineView.page().titleChanged.connect(self.setWindowTitle)
        self.webEngineView.page().urlChanged.connect(self.urlChanged)

    def closeWeb(self):
        self.close()
        main_window.show()

    def load(self):
        url = QUrl.fromUserInput(self.addressLineEdit.text())
        if url.isValid():
            self.webEngineView.load(url)

    def back(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Back)

    def forward(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Forward)

    def urlChanged(self, url):
        self.addressLineEdit.setText(url.toString())


''' Definimos la ventana de Error,
    en caso de que no encuentre el usuario o contraseña,
    en la base de datos, nos aparecera esta ventana.'''


class ErrorWindow(QMainWindow):

    def __init__(self):
        super(ErrorWindow, self).__init__()

        ''' Fijamos el titulo de la aplicación para cuando se inicie '''
        self.setWindowTitle("Error")

        ''' Declaramos un widget '''
        self.widget = QWidget()

        ''' Definimos dos layouts, uno vertial
            y uno horizontal. '''
        self.layoutH = QHBoxLayout()
        self.layoutV = QVBoxLayout()

        ''' Fijamos el layout vertical a la ventana. '''
        self.setLayout(self.layoutV)

        ''' Definimos un label, que nos mostrara el texto,
            como que el usuario ha introducido datos incorrectos'''
        self.label = QLabel(
            "User or Password incorrect"
        )

        ''' Fijamos la fuente para que a la hora de modificar
            cualquier label tengan el mismo aspecto. '''
        font = self.label.font()
        font.setPointSize(12)
        font.setFamily("Times")
        font.setBold(False)
        self.label.setFont(font)

        ''' Alineamos el label al centro '''
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        ''' Añadimos el label al layout vertical
            y añadimos el layout horizontal al propio
            layout vertical. '''
        self.layoutV.addWidget(self.label)
        self.layoutV.addLayout(self.layoutH)

        ''' Definimos un boton que nos permitira Aceptar el error,
            y nos redirigira a la pagina de inicio de sesion. '''
        self.buttonConnect = QPushButton("Accept")
        self.buttonConnect.setStatusTip("Accept")
        self.buttonConnect.clicked.connect(self.closeApp)

        ''' Añadimos el boton al layout '''
        self.layoutH.addWidget(self.buttonConnect)

        ''' Fijamos el layout al Widget principal '''
        self.widget.setLayout(self.layoutV)

        self.setCentralWidget(self.widget)

    ''' Funcion para cerrar la ventana de login '''
    def closeApp(self):
        self.close()
        login_window.show()


class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()

        ''' Fijamos el titulo de la aplicación para cuando se inicie '''
        self.setWindowTitle("App Login")

        ''' Declaramos un widget '''
        self.widget = QWidget()

        ''' Declaramos un layout vertical '''
        self.layout = QVBoxLayout()

        ''' Creamos dos LineEdit, uno de ellos para el usuario,
            y otro para la contraseña '''
        self.user = QLineEdit()
        self.user.setPlaceholderText("user")
        self.userLabel = QLabel("User")
        self.password = QLineEdit()
        self.password.setPlaceholderText("password")
        self.passwordLabel = QLabel("Password")
        self.password.setEchoMode(QLineEdit.Password)

        ''' Creamos un boton, que servira para conectarnos '''
        self.buttonConnect = QPushButton("Connect")
        self.buttonConnect.setStatusTip("Connect")
        self.buttonConnect.clicked.connect(self.closeApp2)

        ''' Creamos un boton, que servira para salir de la aplicacion '''
        self.buttonCancel = QPushButton("Cancel")
        self.buttonCancel.setStatusTip("Cancel")
        self.buttonCancel.clicked.connect(self.closeApp3)

        ''' Añadimos los campos al layout para que puedan ser visibles '''
        self.layout.addWidget(self.userLabel)
        self.layout.addWidget(self.user)
        self.layout.addWidget(self.passwordLabel)
        self.layout.addWidget(self.password)

        ''' Creamos un layout horizontal y lo añadimos al layout principal '''
        self.layoutH = QHBoxLayout()
        self.layout.addLayout(self.layoutH)

        ''' Añadimos al layout horizontal los dos botones,
            el de Conectar y Cancelar '''
        self.layoutH.addWidget(self.buttonConnect)
        self.layoutH.addWidget(self.buttonCancel)

        ''' Al widget principal le fijamos el layout principal '''
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

        self.window3 = ErrorWindow()

    ''' Funcion que comprueba que el usuario y la contraseña,
        estan en la base de datos. En caso de que esten, nos mostrara
        la ventana principal de la app. En caso contrario, nos aparecera
        la ventana de error '''
    def closeApp2(self):
        self.close()

        (cursor.execute("""SELECT usuario
                            ,contraseña
                            FROM usuarios
                            WHERE usuario=?
                            AND contraseña=?""",
                        (self.user.text(), self.password.text())))

        result = cursor.fetchone()
        if result:
            print("User and Password correct - Logged In")
            main_window.show()
        else:
            print("User or Password incorrect")
            self.window3.show()

    ''' Funcion para cerrar la propia ventana '''
    def closeApp3(self):
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        ''' Fijamos el titulo de la ventana '''
        self.setWindowTitle("App Covid")

        ''' Creamos un Widget, un layout Vertical y
            un layout Horizontal '''
        self.widget = QWidget()
        self.layoutV = QVBoxLayout()
        self.layoutH = QHBoxLayout()

        ''' Añadimos al layout vertical, el layout horizontal '''
        self.layoutV.addLayout(self.layoutH)

        ''' Creamos cuatro combobox, que nos permitiran mostrar,
            los Paises, las Comunidades, las Ciudades, y el
            periodo de dias '''
        self.combo_box = QComboBox()
        self.combo_box2 = QComboBox()
        self.combo_box3 = QComboBox()
        self.combo_box4 = QComboBox()

        ''' Fijamos unas medidas concretas para los cuatro combobox '''
        self.combo_box.setFixedWidth(300)
        self.combo_box.setFixedWidth(300)
        self.combo_box2.setFixedWidth(300)
        self.combo_box2.setFixedWidth(300)
        self.combo_box3.setFixedWidth(300)
        self.combo_box3.setFixedWidth(300)
        self.combo_box4.setFixedWidth(70)
        self.combo_box4.setFixedWidth(70)

        ''' Mediante el CSV rellenamos el combobox, con items.
            Que cada item sera un pais, provincia o ciudad '''
        with open(
            carpeta + '/recursos/data/es/countries.csv', 'r'
                ) as csv_file:
            csv_reader = csv.reader(csv_file)

            for line in csv_reader:
                self.combo_box.addItem(line[0])

        with open(
            carpeta + '/recursos/data/es/provinces.csv', 'r'
                ) as csv_file:
            csv_reader = csv.reader(csv_file)

            for line in csv_reader:
                self.combo_box2.addItem(line[0])

        with open(
            carpeta + '/recursos/data/covid/03a30/' +
            '03.csv', 'r'
                ) as csv_file:
            csv_reader = csv.reader(csv_file,  delimiter=";")

            i = 0

            for line in csv_reader:
                if (i == 0):
                    print()
                    i += 1
                else:
                    self.combo_box3.addItem(line[1])

        ''' Añadimos al combobox dos items, un periodo de 7 Dias,
            y un periodo de 30 Dias, para mostrar la información '''
        self.combo_box4.addItem("7 Dias")
        self.combo_box4.addItem("30 Dias")

        ''' Añadimos al layout horizontal los combobox '''
        self.layoutH.addWidget(self.combo_box)
        self.layoutH.addWidget(self.combo_box2)
        self.layoutH.addWidget(self.combo_box3)
        self.layoutH.addWidget(self.combo_box4)

        ''' Fijamos el item de 30 Dias para que cuando se inicie la app,
            este ese item seleccionado por defecto '''
        self.combo_box4.setCurrentText("30 Dias")

        ''' Establecemos los combobox como editables,
            para poder agregar el metodo de MaxVisibleItems,
            esto hara que se muestren un maximo de 5 items,
            si no, se muestrar muchos y ocupa mucho en pantalla '''
        self.combo_box.setEditable(True)
        self.combo_box.setMaxVisibleItems(5)
        self.combo_box2.setEditable(True)
        self.combo_box2.setMaxVisibleItems(5)
        self.combo_box3.setEditable(True)
        self.combo_box3.setMaxVisibleItems(5)
        self.combo_box4.setEditable(False)
        self.combo_box4.setVisible(False)

        ''' Fijamos por defecto los items España y Valencia,
            de sus respectivos combobox, al iniciar la app '''
        self.combo_box.setCurrentText("España")
        self.combo_box2.setCurrentText("Valéncia")

        self.setStatusBar(QStatusBar(self))

        ''' BOTON PCR'''

        self.buttonPcr = QPushButton("Buscar")

        self.buttonPcr.setFixedWidth(100)
        self.buttonPcr.setFixedHeight(25)

        self.layoutH.addWidget(self.buttonPcr)
        self.buttonPcr.setVisible(False)

        ''' BOTON PCR ACUMULADA'''

        self.buttonPcrAcumulada = QPushButton("Buscar")

        self.buttonPcrAcumulada.setFixedWidth(100)
        self.buttonPcrAcumulada.setFixedHeight(25)

        self.layoutH.addWidget(self.buttonPcrAcumulada)
        self.buttonPcrAcumulada.setVisible(False)

        ''' BOTON ACTIVOS '''

        self.buttonActivos = QPushButton("Buscar")

        self.buttonActivos.setFixedWidth(100)
        self.buttonActivos.setFixedHeight(25)

        self.layoutH.addWidget(self.buttonActivos)
        self.buttonActivos.setVisible(False)

        ''' BOTON ACTIVOS ACUMULADOS '''

        self.buttonActivosAcumulados = QPushButton("Buscar")

        self.buttonActivosAcumulados.setFixedWidth(100)
        self.buttonActivosAcumulados.setFixedHeight(25)

        self.layoutH.addWidget(self.buttonActivosAcumulados)
        self.buttonActivosAcumulados.setVisible(False)

        ''' BOTON FALLECIDOS '''

        self.buttonFallecidos = QPushButton("Buscar")

        self.buttonFallecidos.setFixedWidth(100)
        self.buttonFallecidos.setFixedHeight(25)

        self.layoutH.addWidget(self.buttonFallecidos)
        self.buttonFallecidos.setVisible(False)

        ''' Accion Total que añadiremos al Toolbar '''
        self.boton_total = QAction("&Total", self)
        self.boton_total.setStatusTip("Ventana Total")

        ''' Accion PCR+ que añadiremos al Toolbar '''
        self.boton_pcr = QAction("&Casos PCR+", self)
        self.boton_pcr.setStatusTip("Ventana Casos PCR+")

        ''' Accion PCR+ Acumulada que añadiremos al Toolbar '''
        self.boton_pcr_acumulada = QAction("&PCR+ Acumulada", self)
        self.boton_pcr_acumulada.setStatusTip("Ventana PCR+ Acumulada")

        ''' Accion Activos que añadiremos al Toolbar '''
        self.boton_activos = QAction("&Activos", self)
        self.boton_activos.setStatusTip("Ventana Activos")

        ''' Accion Activos Acumulados que añadiremos al Toolbar '''
        self.boton_activos_acumulados = QAction("&Activos Acumulados", self)
        self.boton_activos_acumulados.setStatusTip(
            "Ventana Activos Acumulados")

        ''' Accion Fallecidos que añadiremos al Toolbar '''
        self.boton_fallecidos = QAction("&Fallecidos", self)
        self.boton_fallecidos.setStatusTip("Ventana Fallecidos")

        ''' Creamos un toolbar, que añadiremos a nuestra app '''
        self.toolbar = QToolBar("Toolbar Covid")
        self.addToolBar(self.toolbar)

        ''' Aqui añadimos todas las acciones creadas anteriormente '''
        self.toolbar.addAction(self.boton_total)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.boton_pcr)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.boton_pcr_acumulada)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.boton_activos)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.boton_activos_acumulados)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.boton_fallecidos)

        ''' Fijamos el toolbar para que no se pueda mover '''
        self.toolbar.setMovable(False)

        ''' Creamos un segundo layout horizontal '''
        self.layoutH2 = QHBoxLayout()

        ''' Añadimos al layout vertical el segundo layout horizontal '''
        self.layoutV.addLayout(self.layoutH2)

        ''' Creamos un label y fijamos un tamaño concreto '''
        self.label = QLabel()

        self.label.setFixedHeight(350)
        self.label.setFixedWidth(350)

        ''' Especificamos la fuente y parametros de fuente,
            que tendra nuestro label '''
        self.font = self.label.font()
        self.font.setPointSize(14)
        self.font.setBold(True)
        self.label.setFont(self.font)

        ''' Rellenamos el label con los datos del CSV '''
        with open(
            carpeta + '/recursos/data/covid/total_gva_covid19.csv', 'r'
                ) as csv_file:
            csv_reader = csv.reader(csv_file)

            i = 0

            for line in csv_reader:
                if i == 0:
                    pcr = line[0]
                elif i == 1:
                    pcracumulado = line[0]
                elif i == 2:
                    hospitalizaciones = line[0]
                elif i == 3:
                    uci = line[0]
                elif i == 4:
                    alta = line[0]
                elif i == 5:
                    fallecidos = line[0]
                i += 1

            self.label.setText(
                                "Casos Confirmados: " + pcr + "\n"
                                + "PCR+ Acumulado: " + pcracumulado + "\n"
                                + "Hospitalizaciones: " + hospitalizaciones
                                + "\n"
                                + "UCI: " + uci + "\n"
                                + "Alta: " + alta + "\n"
                                + "Fallecidos: " + fallecidos
                            )

        ''' Creamos un segundo label y especificamos su fuente y parametros '''
        self.label2 = QLabel()

        self.font = self.label2.font()
        self.font.setPointSize(14)
        self.font.setBold(True)
        self.label2.setFont(self.font)

        ''' Establecemos un StyleSheet que dara color a nuestra letra,
            de ambos label, tanto el primero como el segundo '''
        self.label2.setStyleSheet('''
                                    QLabel {
                                        color: rgb(0, 0, 0);
                                    }
                                  ''')

        self.label.setStyleSheet('''
                                    QLabel {
                                        color: rgb(0, 0, 0);
                                    }
                                  ''')

        ''' Fijamos un texto al segundo label y un tamaño fijo '''
        self.label2.setText("Bienvenido a AppCovid")

        self.label2.setFixedHeight(400)
        self.label2.setFixedWidth(600)

        ''' Alineamos el segundo label al centro '''
        self.label2.setAlignment(Qt.AlignCenter)

        ''' Creamos un ChartView, que nos servira para hacer los graficos '''
        self.graphWidget = QChartView()

        ''' Fijamos un tamaño al grafico '''
        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)

        ''' Añadimos el segundo label al segundo layout horizontal '''
        self.layoutH2.addWidget(self.label2)

        ''' Establecemos las acciones, para cuando pulsemos los botones '''
        self.boton_total.triggered.connect(self.cambiarAtotal)
        self.boton_pcr.triggered.connect(self.cambiarApcr)
        self.boton_pcr_acumulada.triggered.connect(self.cambiarApcracumulada)
        self.boton_activos.triggered.connect(self.cambiarAactivos)
        self.boton_activos_acumulados.triggered.connect(
            self.cambiarAactivosacumulados
        )
        self.boton_fallecidos.triggered.connect(
            self.cambiarAfallecidos
            )

        ''' Creamos una barra de menu '''
        self.menu = self.menuBar()

        ''' Añadimos un menu a la barra del Menu '''
        self.file_menu = self.menu.addMenu("&Menu")

        ''' Establecemos los logos y botones del menu,
            despues añadimos las acciones al menu '''
        self.iconoLogout = os.path.join(carpeta, "recursos/logout.png")

        self.logout_button = QAction(QIcon(self.iconoLogout), "&Log Out", self)
        self.logout_button.setStatusTip("This is your LogOut Button")
        self.logout_button.triggered.connect(self.closeWindow)

        self.file_menu.addAction(self.logout_button)

        self.iconoExit = os.path.join(carpeta, "recursos/exit.png")

        self.exit_button = QAction(QIcon(self.iconoExit), "&Close", self)
        self.exit_button.setStatusTip("This is your Exit Button")
        self.exit_button.triggered.connect(self.closeAll)

        self.file_menu.addAction(self.logout_button)
        self.file_menu.addAction(self.exit_button)

        self.file_menu2 = self.menu.addMenu("&Web")

        self.webIcon = os.path.join(carpeta, "recursos/web.png")

        self.web_button = QAction(QIcon(self.webIcon), "&Web", self)
        self.web_button.setStatusTip("This is your Web Button")
        self.web_button.triggered.connect(self.webShow)

        self.file_menu2.addAction(self.web_button)

        ''' Fijamos el layout vertical al widget principal'''
        self.widget.setLayout(self.layoutV)

        ''' Fijamos a la ventana el widget principal '''
        self.setCentralWidget(self.widget)

    def webShow(self):
        self.close()
        webWindow.show()

    ''' Funcion que cambia los datos del grafico y del label,
        cuando pulsamos el boton '''
    def buscarPcr(self):

        self.graphWidget.close()

        with open(
            carpeta + '/recursos/data/covid/03a30/' +
            '31.csv', 'r'
                ) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                if line[1] == self.combo_box3.currentText():
                    pcr = line[2]

            self.label.setText(
                                "Información Actual" + "\n"
                                + "PCR+: " + pcr
                                )

        self.layoutH2.removeWidget(self.label2)

        self.layoutH2.removeWidget(self.graphWidget)

        self.graphWidget = QChartView(self.create_line_chart_pcr())

        self.graphWidget.setRenderHint(QPainter.Antialiasing)

        self.layoutH2.addWidget(self.graphWidget)

        self.layoutH2.addWidget(self.label)

        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)
        self.label2.setFixedHeight(400)
        self.label2.setFixedWidth(600)

    ''' Funcion que cambia los datos del grafico y del label,
        cuando pulsamos el boton '''
    def buscarPcrAcumulada(self):

        self.graphWidget.close()

        with open(
            carpeta + '/recursos/data/covid/03a30/' +
            '31.csv', 'r'
                ) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                if line[1] == self.combo_box3.currentText():
                    pcrmas = line[3]

            self.label.setText(
                                "Información Actual" + "\n"
                                + "PCR+ Acumulada: " + pcrmas
                                )

        self.layoutH2.removeWidget(self.label2)

        self.layoutH2.removeWidget(self.graphWidget)

        self.graphWidget = QChartView(self.create_line_chart_pcr_acumulada())

        self.graphWidget.setRenderHint(QPainter.Antialiasing)

        self.layoutH2.addWidget(self.graphWidget)

        self.layoutH2.addWidget(self.label)

        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)
        self.label2.setFixedHeight(400)
        self.label2.setFixedWidth(600)

    ''' Funcion que cambia los datos del grafico y del label,
        cuando pulsamos el boton '''
    def buscarActivos(self):

        self.graphWidget.close()

        with open(
            carpeta + '/recursos/data/covid/03a30/' +
            '31.csv', 'r'
                ) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                if line[1] == self.combo_box3.currentText():
                    activos = line[4]

            self.label.setText(
                                "Información Actual" + "\n"
                                + "Activos: " + activos
                                )

        self.layoutH2.removeWidget(self.label2)

        self.layoutH2.removeWidget(self.graphWidget)

        self.graphWidget = QChartView(self.create_line_chart_activos())

        self.graphWidget.setRenderHint(QPainter.Antialiasing)

        self.layoutH2.addWidget(self.graphWidget)

        self.layoutH2.addWidget(self.label)

        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)
        self.label2.setFixedHeight(400)
        self.label2.setFixedWidth(600)

    ''' Funcion que cambia los datos del grafico y del label,
        cuando pulsamos el boton '''
    def buscarActivosAcumulados(self):

        self.graphWidget.close()

        with open(
            carpeta + '/recursos/data/covid/03a30/' +
            '31.csv', 'r'
                ) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                if line[1] == self.combo_box3.currentText():
                    activosAcumulados = line[5]

            self.label.setText(
                                "Información Actual" + "\n"
                                + "Activos Acumulados: " + activosAcumulados
                                )

        self.layoutH2.removeWidget(self.label2)

        self.layoutH2.removeWidget(self.graphWidget)

        self.graphWidget = QChartView(
            self.create_line_chart_activos_acumulados())

        self.graphWidget.setRenderHint(QPainter.Antialiasing)

        self.layoutH2.addWidget(self.graphWidget)

        self.layoutH2.addWidget(self.label)

        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)
        self.label2.setFixedHeight(400)
        self.label2.setFixedWidth(600)

    ''' Funcion que cambia los datos del grafico y del label,
        cuando pulsamos el boton '''
    def buscarFallecidos(self):

        self.graphWidget.close()

        with open(
            carpeta + '/recursos/data/covid/03a30/' +
            '31.csv', 'r'
                ) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                if line[1] == self.combo_box3.currentText():
                    fallecidos = line[6]

        self.label.setText(
                            "Información Actual" + "\n"
                            + "Fallecidos: " + fallecidos
                            )

        self.layoutH2.removeWidget(self.label2)

        self.layoutH2.removeWidget(self.graphWidget)

        self.graphWidget = QChartView(self.create_line_chart_fallecidos())

        self.graphWidget.setRenderHint(QPainter.Antialiasing)

        self.layoutH2.addWidget(self.graphWidget)

        self.layoutH2.addWidget(self.label)

        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)
        self.label2.setFixedHeight(400)
        self.label2.setFixedWidth(600)

    ''' Creamos grafico de barras y lo rellenamos con los datos del CSV '''
    def create_bar_chart(self):

        self.set0 = QBarSet("Casos Confirmados")
        self.set1 = QBarSet("PCR+ Acumulado")
        self.set2 = QBarSet("Hospitalizaciones")
        self.set3 = QBarSet("UCI")
        self.set4 = QBarSet("Alta")
        self.set5 = QBarSet("Fallecidos")

        with open(
            carpeta + '/recursos/data/covid/total_gva_covid19.csv', 'r'
                ) as csv_file:
            csv_reader = csv.reader(csv_file)

            for i, data in enumerate(csv_reader):
                if (i == 0):
                    self.set0.append([int(data[0]), 0, 0, 0, 0, 0])
                if (i == 1):
                    self.set1.append([0, int(data[0]), 0, 0, 0, 0])
                if (i == 2):
                    self.set2.append([0, 0, int(data[0]), 0, 0, 0])
                if (i == 3):
                    self.set3.append([0, 0, 0, int(data[0]), 0, 0])
                if (i == 4):
                    self.set4.append([0, 0, 0, 0, int(data[0]), 0])
                if (i == 5):
                    self.set5.append([0, 0, 0, 0, 0, int(data[0])])

        self._bar_series = QStackedBarSeries()
        self._bar_series.append(self.set0)
        self._bar_series.append(self.set1)
        self._bar_series.append(self.set2)
        self._bar_series.append(self.set3)
        self._bar_series.append(self.set4)
        self._bar_series.append(self.set5)

        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)
        self.chart.setTheme(QChart.ChartThemeDark)
        self.chart.addSeries(self._bar_series)
        self.chart.setTitle("Total")

        self.categories = ["Casos Confirmados", "PCR+ Acumulado",
                           "Hospitalizaciones", "UCI", "Alta", "Fallecidos"]

        self.chart.createDefaultAxes()

        self.chart.removeAxis(self.chart.axisX())

        axisX = QBarCategoryAxis()
        axisX.append(self.categories)

        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)
        self.label2.setFixedHeight(400)
        self.label2.setFixedWidth(600)

        return self.chart

    ''' Creamos un grafico de lineas, y lo rellenamos con los datos del CSV '''
    def create_line_chart_pcr(self):

        ''' Comprobamos el periodo de dias elegido por el usuario '''
        if (self.combo_box4.currentText() == "30 Dias"):
            self.series = QLineSeries()

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '03.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        pcr = line[2]

                self.series.append(QPointF(0.0, float(pcr)))
                self.series.append(QPointF(3.0, float(pcr)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '05.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        pcr = line[2]

                self.series.append(QPointF(5.0, float(pcr)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '10.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        pcr = line[2]

                self.series.append(QPointF(10.0, float(pcr)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '13.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        pcr = line[2]

                self.series.append(QPointF(13.0, float(pcr)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '17.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        pcr = line[2]

                self.series.append(QPointF(17.0, float(pcr)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '20.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        pcr = line[2]

                self.series.append(QPointF(20.0, float(pcr)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '24.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        pcr = line[2]

                self.series.append(QPointF(24.0, float(pcr)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '27.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        pcr = line[2]

                self.series.append(QPointF(27.0, float(pcr)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '31.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        pcr = line[2]

                self.series.append(QPointF(31.0, float(pcr)))

            self.chart = QChart()
            self.chart.setAnimationOptions(QChart.AllAnimations)
            self.chart.setTheme(QChart.ChartThemeBlueNcs)
            self.chart.legend().hide()
            self.chart.addSeries(self.series)
            self.chart.createDefaultAxes()
            self.chart.setTitle("PCR+")

        ''' Comprobamos el periodo de dias elegido por el usuario '''
        if (self.combo_box4.currentText() == "7 Dias"):

            self.series = QLineSeries()

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '24.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        pcr = line[2]

                self.series.append(QPointF(24.0, float(pcr)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '27.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        pcr = line[2]

                self.series.append(QPointF(27.0, float(pcr)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '31.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        pcr = line[2]

                self.series.append(QPointF(31.0, float(pcr)))

            self.chart = QChart()
            self.chart.setAnimationOptions(QChart.AllAnimations)
            self.chart.setTheme(QChart.ChartThemeBlueNcs)
            self.chart.legend().hide()
            self.chart.addSeries(self.series)
            self.chart.createDefaultAxes()
            self.chart.setTitle("PCR+")

        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)
        self.label2.setFixedHeight(400)
        self.label2.setFixedWidth(600)

        return self.chart

    ''' Creamos un grafico de lineas, y lo rellenamos con los datos del CSV '''
    def create_line_chart_pcr_acumulada(self):

        ''' Comprobamos el periodo de dias elegido por el usuario '''
        if (self.combo_box4.currentText() == "30 Dias"):

            self.series = QLineSeries()

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '03.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        pcrAcumulada = line[1]

                self.series.append(QPointF(0.0, float(pcrAcumulada)))
                self.series.append(QPointF(3.0, float(pcrAcumulada)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '05.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        pcrAcumulada = line[1]

                self.series.append(QPointF(5.0, float(pcrAcumulada)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '10.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        pcrAcumulada = line[1]

                self.series.append(QPointF(10.0, float(pcrAcumulada)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '13.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        pcrAcumulada = line[1]

                self.series.append(QPointF(13.0, float(pcrAcumulada)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '17.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        pcrAcumulada = line[1]

                self.series.append(QPointF(17.0, float(pcrAcumulada)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '20.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        pcrAcumulada = line[1]

                self.series.append(QPointF(20.0, float(pcrAcumulada)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '24.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        pcrAcumulada = line[1]

                self.series.append(QPointF(24.0, float(pcrAcumulada)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '27.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        pcrAcumulada = line[1]

                self.series.append(QPointF(27.0, float(pcrAcumulada)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '31.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        pcrAcumulada = line[1]

                self.series.append(QPointF(31.0, float(pcrAcumulada)))

            self.chart = QChart()
            self.chart.setAnimationOptions(QChart.AllAnimations)
            self.chart.setTheme(QChart.ChartThemeBlueCerulean)
            self.chart.legend().hide()
            self.chart.addSeries(self.series)
            self.chart.createDefaultAxes()
            self.chart.setTitle("PCR+ Acumuladas")

        ''' Comprobamos el periodo de dias elegido por el usuario '''
        if (self.combo_box4.currentText() == "7 Dias"):

            self.series = QLineSeries()

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '24.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        pcrAcumulada = line[1]

                self.series.append(QPointF(24.0, float(pcrAcumulada)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '27.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        pcrAcumulada = line[1]

                self.series.append(QPointF(27.0, float(pcrAcumulada)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '31.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        pcrAcumulada = line[1]

                self.series.append(QPointF(31.0, float(pcrAcumulada)))

            self.chart = QChart()
            self.chart.setAnimationOptions(QChart.AllAnimations)
            self.chart.setTheme(QChart.ChartThemeBlueCerulean)
            self.chart.legend().hide()
            self.chart.addSeries(self.series)
            self.chart.createDefaultAxes()
            self.chart.setTitle("PCR+ Acumuladas")

        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)
        self.label2.setFixedHeight(400)
        self.label2.setFixedWidth(600)

        return self.chart

    ''' Creamos un grafico de lineas, y lo rellenamos con los datos del CSV '''
    def create_line_chart_activos(self):

        ''' Comprobamos el periodo de dias elegido por el usuario '''
        if (self.combo_box4.currentText() == "30 Dias"):

            self.series = QLineSeries()

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '03.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        activos = line[4]

                self.series.append(QPointF(0.0, float(activos)))
                self.series.append(QPointF(3.0, float(activos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '05.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        activos = line[4]

                self.series.append(QPointF(5.0, float(activos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '10.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        activos = line[4]

                self.series.append(QPointF(10.0, float(activos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '13.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        activos = line[4]

                self.series.append(QPointF(13.0, float(activos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '17.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        activos = line[4]

                self.series.append(QPointF(17.0, float(activos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '20.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        activos = line[4]

                self.series.append(QPointF(20.0, float(activos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '24.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        activos = line[4]

                self.series.append(QPointF(24.0, float(activos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '27.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        activos = line[4]

                self.series.append(QPointF(27.0, float(activos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '31.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        activos = line[4]

                self.series.append(QPointF(31.0, float(activos)))

            self.chart = QChart()
            self.chart.setAnimationOptions(QChart.AllAnimations)
            self.chart.setTheme(QChart.ChartThemeBrownSand)
            self.chart.legend().hide()
            self.chart.addSeries(self.series)
            self.chart.createDefaultAxes()
            self.chart.setTitle("Activos")

        ''' Comprobamos el periodo de dias elegido por el usuario '''
        if (self.combo_box4.currentText() == "7 Dias"):

            self.series = QLineSeries()

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '24.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        activos = line[4]

                self.series.append(QPointF(24.0, float(activos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '27.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        activos = line[4]

                self.series.append(QPointF(27.0, float(activos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '31.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        activos = line[4]

                self.series.append(QPointF(31.0, float(activos)))

            self.chart = QChart()
            self.chart.setAnimationOptions(QChart.AllAnimations)
            self.chart.setTheme(QChart.ChartThemeBrownSand)
            self.chart.legend().hide()
            self.chart.addSeries(self.series)
            self.chart.createDefaultAxes()
            self.chart.setTitle("Activos")

        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)
        self.label2.setFixedHeight(400)
        self.label2.setFixedWidth(600)

        return self.chart

    ''' Creamos un grafico de lineas, y lo rellenamos con los datos del CSV '''
    def create_line_chart_activos_acumulados(self):

        ''' Comprobamos el periodo de dias elegido por el usuario '''
        if (self.combo_box4.currentText() == "30 Dias"):

            self.series = QLineSeries()

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '03.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        activosAcumulados = line[2]

                self.series.append(QPointF(0.0, float(activosAcumulados)))
                self.series.append(QPointF(3.0, float(activosAcumulados)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '05.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        activosAcumulados = line[2]

                self.series.append(QPointF(5.0, float(activosAcumulados)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '10.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        activosAcumulados = line[2]

                self.series.append(QPointF(10.0, float(activosAcumulados)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '13.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        activosAcumulados = line[2]

                self.series.append(QPointF(13.0, float(activosAcumulados)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '17.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        activosAcumulados = line[2]

                self.series.append(QPointF(17.0, float(activosAcumulados)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '20.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        activosAcumulados = line[2]

                self.series.append(QPointF(20.0, float(activosAcumulados)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '24.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        activosAcumulados = line[2]

                self.series.append(QPointF(24.0, float(activosAcumulados)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '27.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        activosAcumulados = line[2]

                self.series.append(QPointF(27.0, float(activosAcumulados)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '31.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        activosAcumulados = line[2]

                self.series.append(QPointF(31.0, float(activosAcumulados)))

            self.chart = QChart()
            self.chart.setAnimationOptions(QChart.AllAnimations)
            self.chart.setTheme(QChart.ChartThemeHighContrast)
            self.chart.legend().hide()
            self.chart.addSeries(self.series)
            self.chart.createDefaultAxes()
            self.chart.setTitle("Activos Acumulados")

        ''' Comprobamos el periodo de dias elegido por el usuario '''
        if (self.combo_box4.currentText() == "7 Dias"):

            self.series = QLineSeries()

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '24.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        activosAcumulados = line[2]

                self.series.append(QPointF(24.0, float(activosAcumulados)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '27.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        activosAcumulados = line[2]

                self.series.append(QPointF(27.0, float(activosAcumulados)))

            with open(
                carpeta + '/recursos/data/covid/prueba/' +
                '31.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")

                for line in csv_reader:
                    if line[0] == self.combo_box3.currentText():
                        activosAcumulados = line[2]

                self.series.append(QPointF(31.0, float(activosAcumulados)))

            self.chart = QChart()
            self.chart.setAnimationOptions(QChart.AllAnimations)
            self.chart.setTheme(QChart.ChartThemeHighContrast)
            self.chart.legend().hide()
            self.chart.addSeries(self.series)
            self.chart.createDefaultAxes()
            self.chart.setTitle("Activos Acumulados")

        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)
        self.label2.setFixedHeight(400)
        self.label2.setFixedWidth(600)

        return self.chart

    ''' Creamos un grafico de lineas, y lo rellenamos con los datos del CSV '''
    def create_line_chart_fallecidos(self):

        ''' Comprobamos el periodo de dias elegido por el usuario '''
        if (self.combo_box4.currentText() == "30 Dias"):

            self.series = QLineSeries()

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '03.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        fallecidos = line[6]

                self.series.append(QPointF(0.0, float(fallecidos)))
                self.series.append(QPointF(3.0, float(fallecidos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '05.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        fallecidos = line[6]

                self.series.append(QPointF(5.0, float(fallecidos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '10.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        fallecidos = line[6]

                self.series.append(QPointF(10.0, float(fallecidos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '13.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        fallecidos = line[6]

                self.series.append(QPointF(13.0, float(fallecidos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '17.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        fallecidos = line[6]

                self.series.append(QPointF(17.0, float(fallecidos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '20.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        fallecidos = line[6]

                self.series.append(QPointF(20.0, float(fallecidos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '24.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        fallecidos = line[6]

                self.series.append(QPointF(24.0, float(fallecidos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '27.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        fallecidos = line[6]

                self.series.append(QPointF(27.0, float(fallecidos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '31.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        fallecidos = line[6]

                self.series.append(QPointF(31.0, float(fallecidos)))

            self.chart = QChart()
            self.chart.setAnimationOptions(QChart.AllAnimations)
            self.chart.setTheme(QChart.ChartThemeDark)
            self.chart.legend().hide()
            self.chart.addSeries(self.series)
            self.chart.createDefaultAxes()
            self.chart.setTitle("Fallecidos")

        ''' Comprobamos el periodo de dias elegido por el usuario '''
        if (self.combo_box4.currentText() == "7 Dias"):

            self.series = QLineSeries()

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '24.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        fallecidos = line[6]

                self.series.append(QPointF(24.0, float(fallecidos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '27.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        fallecidos = line[6]

                self.series.append(QPointF(27.0, float(fallecidos)))

            with open(
                carpeta + '/recursos/data/covid/03a30/' +
                '31.csv', 'r'
                    ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")

                for line in csv_reader:
                    if line[1] == self.combo_box3.currentText():
                        fallecidos = line[6]

                self.series.append(QPointF(31.0, float(fallecidos)))

            self.chart = QChart()
            self.chart.setAnimationOptions(QChart.AllAnimations)
            self.chart.setTheme(QChart.ChartThemeDark)
            self.chart.legend().hide()
            self.chart.addSeries(self.series)
            self.chart.createDefaultAxes()
            self.chart.setTitle("Fallecidos")

        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)
        self.label2.setFixedHeight(400)
        self.label2.setFixedWidth(600)

        return self.chart

    ''' Funcion para cerrar la ventana, cuando pulsamos el boton de log out,
        y nos mostrara la ventana del login otra vez '''
    def closeWindow(self):
        self.close()
        print("Logged Out")
        login_window.user.setText("")
        login_window.password.setText("")
        login_window.show()

    ''' Funcion para cerrar todas las ventanas,
        cuando pulsamos el boton de salir del menu '''
    def closeAll(self):
        app.closeAllWindows()

    ''' Funcion que cambia los datos, cuando pulsamos el boton del toolbar '''
    def cambiarAtotal(self):
        self.combo_box4.setVisible(False)

        self.combo_box.setCurrentText("España")

        self.combo_box2.setCurrentText("Valéncia")

        self.combo_box3.setEnabled(False)

        self.combo_box3.setVisible(False)

        with open(
            carpeta + '/recursos/data/covid/total_gva_covid19.csv', 'r'
                ) as csv_file:
            csv_reader = csv.reader(csv_file)

            i = 0

            for line in csv_reader:
                if i == 0:
                    pcr = line[0]
                elif i == 1:
                    pcracumulado = line[0]
                elif i == 2:
                    hospitalizaciones = line[0]
                elif i == 3:
                    uci = line[0]
                elif i == 4:
                    alta = line[0]
                elif i == 5:
                    fallecidos = line[0]
                i += 1

            self.label.setText(
                                "Información Actual 2020-2022" + "\n"
                                + "Casos Confirmados: " + pcr + "\n"
                                + "PCR+ Acumulado: " + pcracumulado + "\n"
                                + "Hospitalizaciones: " + hospitalizaciones
                                + "\n"
                                + "UCI: " + uci + "\n"
                                + "Alta: " + alta + "\n"
                                + "Fallecidos: " + fallecidos
                            )

        self.label2.setText("")

        self.layoutH2.removeWidget(self.label2)

        self.layoutH2.removeWidget(self.graphWidget)

        self.graphWidget = QChartView(self.create_bar_chart())

        self.layoutH2.addWidget(self.graphWidget)

        self.layoutH2.addWidget(self.label)

        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)
        self.label2.setFixedHeight(400)
        self.label2.setFixedWidth(600)

    ''' Funcion que cambia los datos, cuando pulsamos el boton del toolbar '''
    def cambiarApcr(self):

        self.buttonPcr.setVisible(True)

        self.buttonPcrAcumulada.setVisible(False)

        self.buttonActivos.setVisible(False)

        self.buttonActivosAcumulados.setVisible(False)

        self.buttonFallecidos.setVisible(False)

        self.combo_box3.setVisible(True)

        self.combo_box3.setEnabled(True)

        self.combo_box4.setVisible(True)

        with open(
            carpeta + '/recursos/data/covid/03a30/' +
            '31.csv', 'r'
                ) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                if line[1] == self.combo_box3.currentText():
                    pcr = line[2]

        self.label.setText(
                            "Información Actual" + "\n"
                            + "PCR+: " + pcr
                            )

        self.layoutH2.removeWidget(self.label2)

        self.layoutH2.removeWidget(self.graphWidget)

        self.graphWidget = QChartView(self.create_line_chart_pcr())

        self.graphWidget.setRenderHint(QPainter.Antialiasing)

        self.layoutH2.addWidget(self.graphWidget)

        self.layoutH2.addWidget(self.label)

        self.buttonPcr.clicked.connect(self.buscarPcr)

        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)
        self.label2.setFixedHeight(400)
        self.label2.setFixedWidth(600)

    ''' Funcion que cambia los datos, cuando pulsamos el boton del toolbar '''
    def cambiarApcracumulada(self):

        self.buttonPcr.setVisible(False)

        self.buttonPcrAcumulada.setVisible(True)

        self.buttonActivos.setVisible(False)

        self.buttonActivosAcumulados.setVisible(False)

        self.buttonFallecidos.setVisible(False)

        self.combo_box3.setVisible(True)

        self.combo_box3.setEnabled(True)

        self.combo_box4.setVisible(True)

        with open(
            carpeta + '/recursos/data/covid/03a30/' +
            '31.csv', 'r'
                ) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                if line[1] == self.combo_box3.currentText():
                    pcrmas = line[3]

            self.label.setText(
                                "Información Actual" + "\n"
                                + "PCR+ Acumulada: " + pcrmas
                                )

        self.layoutH2.removeWidget(self.label2)

        self.layoutH2.removeWidget(self.graphWidget)

        self.graphWidget = QChartView(self.create_line_chart_pcr_acumulada())

        self.graphWidget.setRenderHint(QPainter.Antialiasing)

        self.layoutH2.addWidget(self.graphWidget)

        self.layoutH2.addWidget(self.label)

        self.buttonPcrAcumulada.clicked.connect(self.buscarPcrAcumulada)

        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)
        self.label2.setFixedHeight(400)
        self.label2.setFixedWidth(600)

    ''' Funcion que cambia los datos, cuando pulsamos el boton del toolbar '''
    def cambiarAactivos(self):

        self.buttonPcr.setVisible(False)

        self.buttonPcrAcumulada.setVisible(False)

        self.buttonActivos.setVisible(True)

        self.buttonActivosAcumulados.setVisible(False)

        self.buttonFallecidos.setVisible(False)

        self.combo_box4.setVisible(True)

        self.combo_box3.setEnabled(True)

        with open(
            carpeta + '/recursos/data/covid/03a30/' +
            '31.csv', 'r'
                ) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                if line[1] == self.combo_box3.currentText():
                    activos = line[4]

            self.label.setText(
                                "Información Actual" + "\n"
                                + "Activos: " + activos
                                )

        self.layoutH2.removeWidget(self.label2)

        self.layoutH2.removeWidget(self.graphWidget)

        self.graphWidget = QChartView(self.create_line_chart_activos())

        self.graphWidget.setRenderHint(QPainter.Antialiasing)

        self.layoutH2.addWidget(self.graphWidget)

        self.layoutH2.addWidget(self.label)

        self.buttonActivos.clicked.connect(self.buscarActivos)

        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)
        self.label2.setFixedHeight(400)
        self.label2.setFixedWidth(600)

    ''' Funcion que cambia los datos, cuando pulsamos el boton del toolbar '''
    def cambiarAactivosacumulados(self):

        self.buttonPcr.setVisible(False)

        self.buttonPcrAcumulada.setVisible(False)

        self.buttonActivos.setVisible(False)

        self.buttonActivosAcumulados.setVisible(True)

        self.buttonFallecidos.setVisible(False)

        self.combo_box4.setVisible(True)

        self.combo_box3.setEnabled(True)

        with open(
            carpeta + '/recursos/data/covid/03a30/' +
            '31.csv', 'r'
                ) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                if line[1] == self.combo_box3.currentText():
                    activosAcumulados = line[5]

            self.label.setText(
                                "Información Actual" + "\n"
                                + "Activos Acumulados: " + activosAcumulados
                                )

        self.layoutH2.removeWidget(self.label2)

        self.layoutH2.removeWidget(self.graphWidget)

        self.graphWidget = QChartView(
            self.create_line_chart_activos_acumulados()
            )

        self.graphWidget.setRenderHint(QPainter.Antialiasing)

        self.layoutH2.addWidget(self.graphWidget)

        self.layoutH2.addWidget(self.label)

        self.buttonActivosAcumulados.clicked.connect(
            self.buscarActivosAcumulados)

        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)
        self.label2.setFixedHeight(400)
        self.label2.setFixedWidth(600)

    ''' Funcion que cambia los datos, cuando pulsamos el boton del toolbar '''
    def cambiarAfallecidos(self):

        self.buttonPcr.setVisible(False)

        self.buttonPcrAcumulada.setVisible(False)

        self.buttonActivos.setVisible(False)

        self.buttonActivosAcumulados.setVisible(False)

        self.buttonFallecidos.setVisible(True)

        self.combo_box4.setVisible(True)

        self.combo_box3.setEnabled(True)

        with open(
            carpeta + '/recursos/data/covid/03a30/' +
            '31.csv', 'r'
                ) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                if line[1] == self.combo_box3.currentText():
                    fallecidos = line[6]

        self.label.setText(
                            "Información Actual" + "\n"
                            + "Fallecidos: " + fallecidos
                            )

        self.layoutH2.removeWidget(self.label2)

        self.layoutH2.removeWidget(self.graphWidget)

        self.graphWidget = QChartView(self.create_line_chart_fallecidos())

        self.graphWidget.setRenderHint(QPainter.Antialiasing)

        self.layoutH2.addWidget(self.graphWidget)

        self.layoutH2.addWidget(self.label)

        self.buttonFallecidos.clicked.connect(self.buscarFallecidos)

        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)
        self.label2.setFixedHeight(400)
        self.label2.setFixedWidth(600)


app = QApplication([])
login_window = LoginWindow()
webWindow = WebWindow()
main_window = MainWindow()
login_window.show()
app.exec()

''' Comprobamos que estamos todavia conectados,
    y cerramos la conexion '''
if sqliteConnection:
    sqliteConnection.close()
    print("The SQLite connection is closed")
