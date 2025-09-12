import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QIcon, QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple GUI")
        self.setGeometry(600, 300, 500, 400)
        self.setWindowIcon(QIcon("qt5.jpg"))
        self.setStyleSheet("background-color:#e6dcc8;")
        label = QLabel("Hello",self)
        label.setFont(QFont("Comic Sans MS", 20))
        label.setGeometry(0, 0, 500, 100)
        label.setStyleSheet("color: #1d2f38;"
                            "font-weight:bold;"
                            "font-style:italic;")
        label.setAlignment(Qt.AlignCenter)
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
        
if __name__ == "__main__":
    main()