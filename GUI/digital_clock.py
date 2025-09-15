import sys
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QFont, QFontDatabase

class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        self.time_label=QLabel(self)
        self.timer=QTimer(self)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Digital Clock")
        self.setGeometry(600, 400, 300, 100)
        vbox=QVBoxLayout()
        vbox.addWidget(self.time_label)
        self.setLayout(vbox)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size:150px;"
                                      "color:hsl(161, 56%, 8%);")
        self.setStyleSheet("background-color:hsl(145, 43%, 81%);")
        font_id=QFontDatabase.addApplicationFont("D:/OneDrive/Documents/Python/GUI/DS-DIGIT.TTF")
        if font_id == -1:
            print("Failed to load font!")
        else:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                my_font = QFont(families[0], 150)
                self.time_label.setFont(my_font)
            else:
                print("No font families found in the file.")
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()
        
    def update_time(self):
        current_time=QTime.currentTime().toString("hh:mm:ss AP")
        self.time_label.setText(current_time)
    
if __name__ == "__main__":
    app=QApplication(sys.argv)
    clock=DigitalClock()
    clock.show()
    sys.exit(app.exec_())
    