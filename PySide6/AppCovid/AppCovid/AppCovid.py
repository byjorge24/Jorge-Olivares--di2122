from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QComboBox, QLabel
from PySide6.QtWidgets import QHBoxLayout, QToolBar
from PySide6.QtWidgets import QPushButton, QStatusBar
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg
import os

carpeta = os.path.dirname(__file__)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("App Covid")

        self.widget = QWidget()

        self.layoutV = QVBoxLayout()

        self.layoutH = QHBoxLayout()

        self.layoutV.addLayout(self.layoutH)

        self.combo_box = QComboBox()
        self.combo_box2 = QComboBox()
        self.combo_box3 = QComboBox()

        self.combo_box.setFixedWidth(300)
        self.combo_box.setFixedWidth(300)

        self.combo_box2.setFixedWidth(300)
        self.combo_box2.setFixedWidth(300)

        self.combo_box3.setFixedWidth(300)
        self.combo_box3.setFixedWidth(300)

        self.layoutH.addWidget(self.combo_box)
        self.layoutH.addWidget(self.combo_box2)
        self.layoutH.addWidget(self.combo_box3)

        self.button = QPushButton("Buscar")

        self.button.setFixedWidth(100)
        self.button.setFixedHeight(25)

        self.icono = os.path.join(carpeta, "recursos/spain.png")
        self.combo_box.addItem(QIcon(self.icono), "Spain")

        self.icono2 = os.path.join(carpeta, "recursos/valencia.png")
        self.combo_box2.addItem(QIcon(self.icono2), "Comunidad Valenciana")

        self.setStatusBar(QStatusBar(self))

        self.boton_total = QAction("&Total", self)
        self.boton_total.setStatusTip("Ventana Total")

        self.boton_activos = QAction("&Activos", self)
        self.boton_activos.setStatusTip("Ventana Activos")

        self.boton_altas = QAction("&Altas", self)
        self.boton_altas.setStatusTip("Ventana Altas")

        self.boton_fallecidos = QAction("&Fallecidos", self)
        self.boton_fallecidos.setStatusTip("Ventana Fallecidos")

        self.boton_hospitalizaciones = QAction("&Hospitalizaciones", self)
        self.boton_hospitalizaciones.setStatusTip("Ventana Hospitalizaciones")

        self.boton_uci = QAction("&UCI", self)
        self.boton_uci.setStatusTip("Ventana UCI")

        self.toolbar = QToolBar("Toolbar Covid")
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.boton_total)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.boton_activos)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.boton_altas)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.boton_fallecidos)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.boton_hospitalizaciones)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.boton_uci)

        self.toolbar.setMovable(False)

        self.layoutH2 = QHBoxLayout()

        self.layoutV.addLayout(self.layoutH2)

        self.label = QLabel()

        self.label.setFixedHeight(350)
        self.label.setFixedWidth(350)

        self.font = self.label.font()
        self.font.setPointSize(14)
        self.font.setBold(True)
        self.label.setFont(self.font)

        self.label.setText(
            "Activos: " + "\n"
            + "Altas: " + "\n"
            + "Fallecidos: " + "\n"
            + "Hospitalizaciones: " + "\n"
            + "UCI: "
            )

        self.layoutH2.addWidget(self.label)

        self.graphWidget = pg.PlotWidget()

        self.layoutH2.addWidget(self.graphWidget)

        self.graphWidget.setBackground('w')

        self.graphWidget.setTitle("Total", color="black", size="20px")

        styles = {'color': 'black', 'font-size': '20px'}
        self.graphWidget.setLabel('left', 'Casos', **styles)
        self.graphWidget.setLabel('bottom', 'Dias', **styles)

        self.boton_total.triggered.connect(self.cambiarAtotal)
        self.boton_activos.triggered.connect(self.cambiarAactivos)
        self.boton_altas.triggered.connect(self.cambiarAaltas)
        self.boton_fallecidos.triggered.connect(self.cambiarAfallecidos)
        self.boton_hospitalizaciones.triggered.connect(
            self.cambiarAhospitalizaciones
            )
        self.boton_uci.triggered.connect(
            self.cambiarAuci
        )

        self.layoutH.addWidget(self.button)

        self.widget.setLayout(self.layoutV)

        self.setCentralWidget(self.widget)

    def cambiarAtotal(self):
        self.label.setText(
            "Activos: " + "\n"
            + "Altas: " + "\n"
            + "Fallecidos: " + "\n"
            + "Hospitalizaciones: " + "\n"
            + "UCI: "
            )
        self.graphWidget.setTitle("Total", color="black", size="15pt")

    def cambiarAactivos(self):
        self.label.setText("Activos: ")
        self.graphWidget.setTitle("Activos", color="black", size="15pt")

    def cambiarAaltas(self):
        self.label.setText("Altas: ")
        self.graphWidget.setTitle("Altas", color="black", size="15pt")

    def cambiarAfallecidos(self):
        self.label.setText("Fallecidos: ")
        self.graphWidget.setTitle("Fallecidos", color="black", size="15pt")

    def cambiarAhospitalizaciones(self):
        self.label.setText("Hospitalizaciones: ")
        self.graphWidget.setTitle(
            "Hospitalizaciones", color="black", size="15pt"
            )

    def cambiarAuci(self):
        self.label.setText("UCI: ")
        self.graphWidget.setTitle(
            "UCI", color="black", size="15pt"
            )


app = QApplication([])
main_window = MainWindow()
main_window.show()
app.exec()
