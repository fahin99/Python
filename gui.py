import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton)
from PyQt5.QtGui import QIcon, QFont, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple GUI")
        self.setGeometry(600, 300, 500, 400)
        # self.setWindowIcon(QIcon("qt5.jpg"))
        # self.setStyleSheet("background-color:#e6dcc8;")
        # label = QLabel("Hello",self)
        # label.setFont(QFont("Comic Sans MS", 20))
        # label.setGeometry(0, 0, 500, 100)
        # label.setStyleSheet("color: #1d2f38;"
        #                     "font-weight:bold;"
        #                     "font-style:italic;")
        # label.setAlignment(Qt.AlignCenter)
        # label2 = QLabel(self)
        # label2.setGeometry(100, 100, 200, 100)
        # pixmap=QPixmap("images.jpeg")
        # label2.setPixmap(pixmap)
        # label2.setScaledContents(True)
        # label2.setGeometry((self.width()-label2.width())//2,
        #                    (self.height()-label2.height())//2,
        #                    label2.width(),
        #                    label2.height())
        self.initUI()
        
    def initUI(self):
        # central_widget=QWidget()
        # self.setCentralWidget(central_widget)
        # label1=QLabel("Label 1", self)
        # label2=QLabel("Label 2", self)
        # label3=QLabel("Label 3", self)
        # label4=QLabel("Label 4", self)
        # label1.setStyleSheet("background-color: lightblue;")
        # label2.setStyleSheet("background-color: lightgreen;")
        # label3.setStyleSheet("background-color: lightcoral;") 
        # label4.setStyleSheet("background-color: lightgoldenrodyellow;")
        # label5=QLabel("Label 5", self)
        # label6=QLabel("Label 6", self)  
        # label7=QLabel("Label 7", self)
        # label8=QLabel("Label 8", self)
        # label5.setStyleSheet("background-color: lightpink;")
        # label6.setStyleSheet("background-color: lightgray;")
        # label7.setStyleSheet("background-color: lightyellow;")
        # label8.setStyleSheet("background-color: lightblue;")
        # grid=QGridLayout()
        # grid.addWidget(label1, 0, 0)
        # grid.addWidget(label2, 0, 1)
        # grid.addWidget(label3, 1, 0)
        # grid.addWidget(label4, 1, 1)
        # grid.addWidget(label5, 2, 0)
        # grid.addWidget(label6, 2, 1)
        # grid.addWidget(label7, 3, 0)
        # grid.addWidget(label8, 3, 1)
        # central_widget.setLayout(grid)
        self.button=QPushButton("Click Me", self)
        self.button.setGeometry(190, 150, 120, 50)
        self.button.setStyleSheet("background-color: lightblue;"
                             "font-size:24px;"
                             "font-weight:bold;")
        self.button.clicked.connect(self.on_click)

    def on_click(self):
        print("Button clicked!")
        self.button.setText("Clicked")
        self.button.setEnabled(False)
        

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
        
if __name__ == "__main__":
    main()