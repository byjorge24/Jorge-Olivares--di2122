import os
from PySide6.QtWidgets import (
    QApplication, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QVBoxLayout, QWidget,
    QPushButton)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon

carpeta = os.path.dirname(__file__)


class AdminWindow(QMainWindow):

    def __init__(self):
        super(AdminWindow, self).__init__()

        # Fijamos el titulo de la aplicación para cuando se inicie
        self.setWindowTitle("Administrator")

        self.setFixedSize(QSize(1200, 800))

        # Declaramos un widget
        self.widget = QWidget()

        self.layoutH = QHBoxLayout()
        self.layoutV = QVBoxLayout()
        self.setLayout(self.layoutV)
        self.label = QLabel(
            "Logged in as administrator"
        )

        self.menu = self.menuBar()

        self.file_menu = self.menu.addMenu("&Menu")

        self.icono4 = os.path.join(carpeta, "recursos/salir.png")

        self.exit_button = QAction(QIcon(self.icono4), "&Exit", self)
        self.exit_button.setStatusTip("This is your Exit Button")
        self.exit_button.triggered.connect(self.closeApp)

        self.file_menu.addAction(self.exit_button)

        font = self.label.font()
        font.setPointSize(20)
        font.setFamily("Times")
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.layoutV.addWidget(self.label)
        self.layoutV.addLayout(self.layoutH)

        self.widget.setStatusTip("Administrator")

        self.widget.setLayout(self.layoutV)

        self.setCentralWidget(self.widget)

    def closeApp(self):
        self.close()
        main_window.show()


class UserWindow(QMainWindow):

    def __init__(self):
        super(UserWindow, self).__init__()

        # Fijamos el titulo de la aplicación para cuando se inicie
        self.setWindowTitle("User")

        self.setFixedSize(QSize(1200, 800))

        # Declaramos un widget
        self.widget = QWidget()

        self.layoutH = QHBoxLayout()
        self.layoutV = QVBoxLayout()
        self.setLayout(self.layoutV)
        self.label = QLabel(
            "Logged in as user"
        )

        self.menu = self.menuBar()

        self.file_menu = self.menu.addMenu("&Menu")

        self.icono4 = os.path.join(carpeta, "recursos/salir.png")

        self.exit_button = QAction(QIcon(self.icono4), "&Exit", self)
        self.exit_button.setStatusTip("This is your Exit Button")
        self.exit_button.triggered.connect(self.closeApp)

        self.file_menu.addAction(self.exit_button)

        font = self.label.font()
        font.setPointSize(20)
        font.setFamily("Times")
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.layoutV.addWidget(self.label)
        self.layoutV.addLayout(self.layoutH)

        self.widget.setLayout(self.layoutV)

        self.widget.setStatusTip("Standard User")

        self.setCentralWidget(self.widget)

    def closeApp(self):
        self.close()
        main_window.show()


class ErrorWindow(QMainWindow):

    def __init__(self):
        super(ErrorWindow, self).__init__()

        # Fijamos el titulo de la aplicación para cuando se inicie
        self.setWindowTitle("Error")

        # Declaramos un widget
        self.widget = QWidget()

        self.layoutH = QHBoxLayout()
        self.layoutV = QVBoxLayout()
        self.setLayout(self.layoutV)
        self.label = QLabel(
            "User or Password incorrect"
        )

        font = self.label.font()
        font.setPointSize(20)
        font.setFamily("Times")
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.layoutV.addWidget(self.label)
        self.layoutV.addLayout(self.layoutH)

        self.buttonConnect = QPushButton("Accept")
        self.buttonConnect.setStatusTip("Accept")
        self.buttonConnect.clicked.connect(self.closeApp)

        self.layoutH.addWidget(self.buttonConnect)

        self.widget.setLayout(self.layoutV)

        self.widget.setStatusTip("Standard User")

        self.setCentralWidget(self.widget)

    def closeApp(self):
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Fijamos el titulo de la aplicación para cuando se inicie
        self.setWindowTitle("App Login")

        # Declaramos un widget
        self.widget = QWidget()

        # Declaramos un layout vertical
        self.layout = QVBoxLayout()

        self.user = QLineEdit()
        self.user.setPlaceholderText("user")
        self.userLabel = QLabel("User")
        self.password = QLineEdit()
        self.password.setPlaceholderText("password")
        self.passwordLabel = QLabel("Password")

        self.buttonConnect = QPushButton("Connect")
        self.buttonConnect.setStatusTip("Connect")
        self.buttonConnect.clicked.connect(self.closeApp2)

        self.buttonCancel = QPushButton("Cancel")
        self.buttonCancel.setStatusTip("Cancel")
        self.buttonCancel.clicked.connect(self.closeApp3)

        self.layout.addWidget(self.userLabel)
        self.layout.addWidget(self.user)
        self.layout.addWidget(self.passwordLabel)
        self.layout.addWidget(self.password)

        self.layoutH = QHBoxLayout()
        self.layout.addLayout(self.layoutH)

        self.layoutH.addWidget(self.buttonConnect)
        self.layoutH.addWidget(self.buttonCancel)

        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

        self.window1 = AdminWindow()
        self.window2 = UserWindow()

        self.window3 = ErrorWindow()

    def closeApp2(self):
        self.close()
        if (self.user.text() == "admin" and self.password.text() == "1234"):
            self.window1.show()
        elif (self.user.text() == "user" and self.password.text() == "1234"):
            self.window2.show()
        else:
            main_window.show()
            self.window3.show()

    def closeApp3(self):
        self.close()


app = QApplication([])
main_window = MainWindow()
main_window.show()
app.exec()
