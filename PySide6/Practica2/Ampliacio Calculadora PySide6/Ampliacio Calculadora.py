import math
import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QApplication, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QStatusBar, QVBoxLayout, QWidget,
    QPushButton)

carpeta = os.path.dirname(__file__)


class AnotherWindow(QWidget):

    def __init__(self):
        super().__init__()
        layoutV = QVBoxLayout()
        self.setWindowTitle("Help")
        self.label = QLabel(
            "-----  How to use the Simple Calculator  -----"
            + "\n" +
            "--------------------------------------------"
            +
            "--------------------"
            + "\n" +
            "c -> Delete everything"
            + "\n" +
            "Backspace -> Delete one value"
            + "\n" +
            "Shift+0 -> ="
            + "\n" +
            "Shift+5 -> %"
            + "\n" +
            "Shift+7 -> /"
            + "\n" +
            "Shift+8 -> ()"
            + "\n" +
            "Shift++ -> x"
        )
        layoutV.addWidget(self.label)
        self.setLayout(layoutV)
        layoutV2 = QVBoxLayout()
        layoutV.addLayout(layoutV2)
        self.label2 = QLabel(
            "----- How to use the Advanced Calculator -----"
            + "\n" +
            "--------------------------------------------"
            +
            "-----------------------"
            + "\n" +
            "c -> Delete everything"
            + "\n" +
            "Backspace -> Delete one value"
            + "\n" +
            "Shift+1 -> !"
            + "\n" +
            "Shift+4 -> √"
            + "\n" +
            "Shift+5 -> %"
            + "\n" +
            "Shift+6 -> π"
            + "\n" +
            "Shift+7 -> /"
            + "\n" +
            "Shift+8 -> ()"
            + "\n" +
            "Shift+9 -> ^"
            + "\n" +
            "Shift++ -> *"
        )
        layoutV2.addWidget(self.label2)


class AnotherWindow2(QWidget):

    def __init__(self):
        super().__init__()
        self.layoutH = QHBoxLayout()
        self.layoutV = QVBoxLayout()
        self.setWindowTitle("Help")
        self.setLayout(self.layoutV)
        self.label = QLabel(
            "Are you sure you want to exit?"
        )
        self.buttonSi = QPushButton("Yes")
        self.buttonSi.setStatusTip("Yes")
        self.buttonSi.clicked.connect(self.closeApp2)

        self.buttonNo = QPushButton("No")
        self.buttonNo.setStatusTip("No")
        self.buttonNo.clicked.connect(self.closeApp3)

        self.layoutV.addWidget(self.label)
        self.layoutV.addLayout(self.layoutH)
        self.layoutH.addWidget(self.buttonSi)
        self.layoutH.addWidget(self.buttonNo)

    def closeApp2(self):
        app.closeAllWindows()

    def closeApp3(self):
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Fijamos el titulo de la aplicación para cuando se inicie
        self.setWindowTitle("Simple Calculator")

        # Declaramos un widget
        self.widget = QWidget()

        # Declaramos un layout vertical y un grid layout
        self.layout = QVBoxLayout()
        self.layoutButtons = QGridLayout()

        # Definimos variables de comprobación
        self.guardar = ""
        self.comprobar = True
        self.advancedCalculatorCheck = False

        # Declaramos un line edit, que nos permitira mostrar las operaciones
        self.display = QLineEdit()
        self.display.setText(self.guardar)

        """
            Definimos algunas propiedades del line edit, como altura fija
            ,alineación del texto y modo solo lectura
        """
        self.display.setFixedHeight(50)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)

        # Añadimos el line edit a nuestro layout vertical
        self.layout.addWidget(self.display)

        """
            Añadimos el grid layout que contendra los botones
            a nuestro layout vertical
        """
        self.layout.addLayout(self.layoutButtons)

        # Definimos una lista con los botones de la calculadora simple
        self.buttons = {'AC': (0, 0), '()': (0, 1), '%': (0, 2), '/': (0, 3),
                        '7': (1, 0), '8': (1, 1), '9': (1, 2), 'x': (1, 3),
                        '4': (2, 0), '5': (2, 1), '6': (2, 2), '+': (2, 3),
                        '1': (3, 0), '2': (3, 1), '3': (3, 2), '-': (3, 3),
                        '0': (4, 0), '.': (4, 1), '<-': (4, 2), '=': (4, 3),
                        }

        # Definimos una lista con los botones de la calculadora avanzada
        self.buttons2 = {'π': (0, 0), '^': (0, 1), '!': (0, 2), '√': (0, 3),
                         'AC': (1, 0), '()': (1, 1), '%': (1, 2), '/': (1, 3),
                         '7': (2, 0), '8': (2, 1), '9': (2, 2), 'x': (2, 3),
                         '4': (3, 0), '5': (3, 1), '6': (3, 2), '+': (3, 3),
                         '1': (4, 0), '2': (4, 1), '3': (4, 2), '-': (4, 3),
                         '0': (5, 0), '.': (5, 1), '<-': (5, 2), '=': (5, 3),
                         }

        self.layout.addLayout(self.layoutButtons)

        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

        self.icono = os.path.join(carpeta, "recursos/calculadora.png")

        """
            Creamos un boton que nos llevara hasta la calculadora simple
        """
        self.button_action = QAction(QIcon(self.icono), "&Simple", self)
        self.button_action.setStatusTip("This is your Simple Calculator")
        self.button_action.triggered.connect(self.simpleCalculator)

        self.icono2 = os.path.join(carpeta, "recursos/calculadoraAdvanced.png")

        """
            Creamos un boton que nos llevara hasta la calculadora avanzada
        """
        self.button_action2 = QAction(QIcon(self.icono2), "&Advanced", self)
        self.button_action2.setStatusTip("This is your Advanced Calculator")
        self.button_action2.triggered.connect(self.advancedCalculator)

        self.icono3 = os.path.join(carpeta, "recursos/guardar.png")

        """
            Creamos un boton que sera una casilla
            podremos activarla o desactivarla mediante un click
            Esta nos permitira guardar las operaciónes en un fichero de texto
        """
        self.check_box = QAction(QIcon(self.icono3), "&Save data", self)
        self.check_box.setStatusTip("Save Button")
        self.check_box.setCheckable(True)

        self.setStatusBar(QStatusBar(self))

        self.menu = self.menuBar()

        self.icono4 = os.path.join(carpeta, "recursos/salir.png")

        """
            Creamos el boton de Salida, le añadimos un Status
            para cuando pasemos el ratón por encima y
            le indicamos que si se pulsa el boton, se lanzara
            la función 'closeApp' que cierra la aplicación
        """
        self.exit_button = QAction(QIcon(self.icono4), "&Exit", self)
        self.exit_button.setStatusTip("This is your Exit Button")
        self.exit_button.triggered.connect(self.closeApp)

        self.icono5 = os.path.join(carpeta, "recursos/help.png")

        """
            Creamos el boton de Ayuda, le añadimos un Status
            para cuando pasemos el ratón por encima y
            le indicamos que si se pulsa el boton, se lanzara
            la función 'help' que nos muestra ayuda sobre la aplicación
        """
        self.help_button = QAction(QIcon(self.icono5), "&Help", self)
        self.help_button.setStatusTip("This is your Help Button")
        self.help_button.triggered.connect(self.help)

        """
            Añadimos al menú principal, los menús que vamos a utilizar
        """
        self.file_menu = self.menu.addMenu("&Menu")
        self.file_menu2 = self.file_menu.addMenu("&Calculators")

        """
            Añadimos atajos de teclado para elegir el tipo de calculadora
        """
        self.button_action.setShortcut(QKeySequence("Ctrl+p"))
        self.button_action2.setShortcut(QKeySequence("Ctrl+l"))

        """
            Añadimos al menú los botones, y entre ellos unos separadores
        """
        self.file_menu2.addAction(self.button_action)
        self.file_menu.addSeparator()
        self.file_menu2.addAction(self.button_action2)
        self.file_menu.addSeparator()
        self.menu.addAction(self.help_button)
        self.file_menu.addAction(self.check_box)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_button)

        """
            Iniciamos la calculadora simple
            Nuestro usuario primero dispondra de la calculadora simple,
            en caso de que quiera utilizar la avanzada, lo podra hacer
            desde el menú
        """
        self.simpleCalculator()

        self.window1 = AnotherWindow()
        self.window2 = AnotherWindow2()

    # Funcion que realiza las operaciones y nos las muestra por pantalla.
    def op(self):
        if (self.sender().text() == "="):
            self.setDisplayText(str(eval(self.guardar)))
            self.resultado = str(eval(self.guardar))
            self.guardar += "="
            self.guardar += self.resultado
            self.saveText()
            self.guardar = ""
        elif (self.sender().text() == "x"):
            self.guardar += "*"
            self.setDisplayText(self.guardar)
        elif (self.sender().text() == "π"):
            self.guardar += str(math.pi)
            self.setDisplayText(self.guardar)
        elif (self.sender().text() == "%"):
            self.guardar += "/100"
            self.setDisplayText(self.guardar)
        elif (self.sender().text() == "^"):
            self.guardar += "**"
            self.setDisplayText(self.guardar)
        elif (self.sender().text() == "!"):
            self.numero = 0
            self.numero += math.factorial(int(self.guardar))
            self.resultado = ""
            self.guardarfichero = "!"
            self.guardarfichero += self.guardar
            self.guardarfichero += "="
            self.guardarfichero += str(self.numero)
            self.resultado = str(self.numero)
            self.setDisplayText(self.resultado)
            self.guardar = self.guardarfichero
            self.saveText()
        elif (self.sender().text() == "√"):
            self.numero2 = 0
            self.numero2 += math.sqrt(int(self.guardar))
            self.resultado = ""
            self.guardarfichero2 = "√"
            self.guardarfichero2 += self.guardar
            self.guardarfichero2 += "="
            self.guardarfichero2 += str(self.numero2)
            self.resultado2 = str(self.numero2)
            self.setDisplayText(self.resultado2)
            self.guardar = self.guardarfichero2
            self.saveText()
        elif (self.sender().text() == "<-"):
            self.setDisplayText(self.guardar[:-1])
            self.guardar = self.guardar[:-1]
        elif (self.sender().text() == "()"):
            if (self.comprobar):
                self.guardar += "("
                self.comprobar = False
            elif (not self.comprobar):
                self.guardar += ")"
                self.comprobar = True
            self.setDisplayText(self.guardar)
        elif (self.sender().text() == "AC"):
            self.clearDisplay()
        else:
            self.guardar += self.sender().text()
            self.setDisplayText(self.guardar)

    # Funcion que introduce el texto en nuestro QLineEdit
    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    # Funcion que nos devuelve el texto de nuestro QLineEdit
    def displayText(self):
        return self.display.text()

    """
        Funcion que limipia la pantalla
        y la variable donde guardamos las operaciones la deja en blanco
    """
    def clearDisplay(self):
        self.setDisplayText("")
        self.guardar = ""

    # Funcion que borra los widgets de nuestro layout de botones
    def clearLayout(self):
        for i in reversed(range(self.layoutButtons.count())):
            widget = self.layoutButtons.itemAt(i).widget()
            self.layoutButtons.removeWidget(widget)
            widget.setParent(None)

    """
        Funcion para comprobar en que calculadora estamos
        Hará que los botones del menu estén activados o desactivados
    """
    def check(self):
        if (self.simple == 1):
            self.button_action.setDisabled(True)
            self.button_action2.setEnabled(True)
        elif (self.simple == 0):
            self.button_action.setEnabled(True)
            self.button_action2.setDisabled(True)
        else:
            self.button_action.setEnabled(True)
            self.button_action2.setEnabled(True)

    def help(self):

        self.window1.show()

    # Funcion de la calculadora simple
    def simpleCalculator(self):

        # Fijamos el titulo de la aplicación
        self.setWindowTitle('Simple Calculator')

        # Variable de comprobación
        self.simple = 1

        """
            Llamamos a nuestra función
            para comprobar en que calculadora nos encontramos
        """
        self.check()

        """
            En caso de que sea la calculadora avanzada
            limpiara el layout con la función creada anteriormente
        """
        if self.advancedCalculatorCheck:
            self.clearLayout()

        for buttonText1, pos in self.buttons.items():
            self.button = QPushButton(buttonText1)
            self.button.setFixedSize(100, 50)
            self.layoutButtons.addWidget(
                                        self.button,
                                        pos[0], pos[1]
                                        )
            self.button.clicked.connect(self.op)
            self.button.setStatusTip(buttonText1)

            """
                Asignamos el status de los atajos de teclado
                para que el usuario sepa en todo momento,
                cuales son los atajos a utilizar
            """
            if(buttonText1 == 'AC'):
                self.button.setStatusTip(
                    ('c'))
            elif(buttonText1 == '<-'):
                self.button.setStatusTip(
                    ('Backspace'))
            elif(buttonText1 == "%"):
                self.button.setStatusTip(
                    ('Shift+5'))
            elif(buttonText1 == "/"):
                self.button.setStatusTip(
                    ('Shift+7'))
            elif(buttonText1 == "x"):
                self.button.setStatusTip(
                    ('Shift++'))
            elif(buttonText1 == "()"):
                self.button.setStatusTip(
                    ('Shift+8'))

            """
                Asignamos los atajos de teclado para poder utilizar el teclado
                Podremos utilizar los atajos o el ratón
            """
            if(buttonText1 == 'AC'):
                self.button.setShortcut(
                    QKeySequence('c'))
            elif(buttonText1 == '<-'):
                self.button.setShortcut(
                    QKeySequence('Backspace'))
            elif(buttonText1 == "%"):
                self.button.setShortcut(
                    QKeySequence('Shift+5'))
            elif(buttonText1 == "/"):
                self.button.setShortcut(
                    QKeySequence('Shift+7'))
            elif(buttonText1 == "x"):
                self.button.setShortcut(
                    QKeySequence('Shift++'))
            elif(buttonText1 == "()"):
                self.button.setShortcut(
                    QKeySequence('Shift+8'))
            else:
                self.button.setShortcut(
                    QKeySequence(buttonText1))

        self.advancedCalculatorCheck = False

    # Funcion de la calculadora avanzada
    def advancedCalculator(self):

        # Fijamos el titulo de la aplicación
        self.setWindowTitle('Advanced Calculator')

        # Variable de comprobación
        self.simple = 0

        """
            Llamamos a nuestra función
            para comprobar en que calculadora nos encontramos
        """
        self.check()

        """
            En caso de que no sea la calculadora avanzada
            limpiara el layout con la función creada anteriormente
        """
        if not (self.advancedCalculatorCheck):
            self.clearLayout()

        for buttonText2, pos2 in self.buttons2.items():
            self.button2 = QPushButton(buttonText2)
            self.button2.setFixedSize(100, 50)
            self.layoutButtons.addWidget(
                                        self.button2,
                                        pos2[0], pos2[1]
                                        )
            self.button2.clicked.connect(self.op)
            self.button2.setStatusTip(buttonText2)

            if(buttonText2 == 'AC'):
                self.button2.setStatusTip(
                    ('c'))
            elif(buttonText2 == '<-'):
                self.button2.setStatusTip(
                    ('Backspace'))
            elif(buttonText2 == "%"):
                self.button2.setStatusTip(
                    ('Shift+5'))
            elif(buttonText2 == "/"):
                self.button2.setStatusTip(
                    ('Shift+7'))
            elif(buttonText2 == "x"):
                self.button2.setStatusTip(
                    ('Shift++'))
            elif(buttonText2 == "()"):
                self.button2.setStatusTip(
                    ('Shift+8'))
            elif(buttonText2 == "^"):
                self.button2.setStatusTip(
                    ('Shift+9'))
            elif(buttonText2 == "√"):
                self.button2.setStatusTip(
                    ('Shift+4'))
            elif(buttonText2 == "π"):
                self.button2.setStatusTip(
                    ('Shift+6'))

            """
                Asignamos los atajos de teclado para poder utilizar el teclado
                Podremos utilizar los atajos o el ratón
            """
            if(buttonText2 == 'AC'):
                self.button2.setShortcut(
                    QKeySequence('c'))
            elif(buttonText2 == '<-'):
                self.button2.setShortcut(
                    QKeySequence('Backspace'))
            elif(buttonText2 == "%"):
                self.button2.setShortcut(
                    QKeySequence('Shift+5'))
            elif(buttonText2 == "/"):
                self.button2.setShortcut(
                    QKeySequence('Shift+7'))
            elif(buttonText2 == "x"):
                self.button2.setShortcut(
                    QKeySequence('Shift++'))
            elif(buttonText2 == "()"):
                self.button2.setShortcut(
                    QKeySequence('Shift+8'))
            elif(buttonText2 == "^"):
                self.button2.setShortcut(
                    QKeySequence('Shift+9'))
            elif(buttonText2 == "√"):
                self.button2.setShortcut(
                    QKeySequence('Shift+4'))
            elif(buttonText2 == "π"):
                self.button2.setShortcut(
                    QKeySequence('Shift+6'))
            else:
                self.button2.setShortcut(
                    QKeySequence(buttonText2))

        self.advancedCalculatorCheck = True

    # Funcion que nos permite guardar las operaciones en un fichero de texto
    def saveText(self):
        if (self.check_box.isChecked()):
            with open(
                os.path.join(os.path.dirname(__file__), "Operaciones.txt"),
                    "a+"
            ) as f:
                f.write(self.guardar + "\n")

    """
        Función que cierra todas las ventanas
        La utilizamos cuando pulsamos el boton del menú "Exit"
    """
    def closeApp(self):
        self.window2.show()


app = QApplication([])
main_window = MainWindow()
main_window.show()
app.exec()
