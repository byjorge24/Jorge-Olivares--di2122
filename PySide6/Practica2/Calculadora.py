from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QGridLayout, QLineEdit)
from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget)
from PySide6.QtWidgets import (QPushButton)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Calculadora")

        self.widget = QWidget()

        self.layout = QVBoxLayout()
        self.layoutButtons = QGridLayout()

        self.guardar = ""
        self.comprobar = True

        self.display = QLineEdit()
        self.display.setText(self.guardar)

        self.display.setFixedHeight(50)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)

        self.layout.addWidget(self.display)

        self.layout.addLayout(self.layoutButtons)

        self.buttons = {'AC': (0, 0), '()': (0, 1), '%': (0, 2), '/': (0, 3),
                        '7': (1, 0), '8': (1, 1), '9': (1, 2), 'x': (1, 3),
                        '4': (2, 0), '5': (2, 1), '6': (2, 2), '+': (2, 3),
                        '1': (3, 0), '2': (3, 1), '3': (3, 2), '-': (3, 3),
                        '0': (4, 0), '.': (4, 1), '<-': (4, 2), '=': (4, 3),
                        }

        for buttonText, pos in self.buttons.items():
            self.buttons[buttonText] = QPushButton(buttonText)
            self.buttons[buttonText].setFixedSize(100, 50)
            self.layoutButtons.addWidget(
                                        self.buttons[buttonText],
                                        pos[0], pos[1]
                                        )
            self.buttons[buttonText].clicked.connect(self.op)

        self.layout.addLayout(self.layoutButtons)

        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def op(self):
        if (self.sender().text() == "="):
            self.setDisplayText(str(eval(self.guardar)))
        elif (self.sender().text() == "x"):
            self.guardar += "*"
            self.setDisplayText(self.guardar)
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

    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        return self.display.text()

    def clearDisplay(self):
        self.setDisplayText("")
        self.guardar = ""


app = QApplication([])
main_window = MainWindow()
main_window.show()
app.exec()
