import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLineEdit, QButtonGroup, QRadioButton, QCheckBox, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton)
from PyQt5.QtGui import QIcon, QFont, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple GUI")
        self.setGeometry(600, 300, 600, 500)
        self.setWindowIcon(QIcon("qt5.jpg"))
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
        self.button=QPushButton("Click Me", self)
        self.label=QLabel("Hello",self)
        self.label_checkbox=QLabel(self)
        self.checkbox=QCheckBox("Check me", self)
        self.radio1=QRadioButton("Visa", self)
        self.radio2=QRadioButton("MasterCard", self)
        self.radio3=QRadioButton("Gift Card", self)
        self.radio4=QRadioButton("In-Store", self)
        self.radio5=QRadioButton("Online", self)
        self.button_group1=QButtonGroup(self)
        self.button_group2=QButtonGroup(self)
        self.line_edit=QLineEdit(self)
        self.button_submit=QPushButton("Submit", self)
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

        self.setStyleSheet("background-color: #b8e3ca;")
        self.button_submit.setObjectName("button_submit")
        self.button.setObjectName("button")
        self.setup_buttons()
        self.setup_checkbox()
        self.setup_radio_buttons()
        self.line_edit_setup()
        
    #setup functions   
    def setup_buttons(self):
        self.button.setGeometry(240, 190, 120, 50)
        self.button.setStyleSheet("""
                QPushButton{
                    font-size:20px;
                    background-color:hsl(20, 62%, 85%);
                    font-weight:bold;
                    font-family:Comic Sans MS;
                    border-radius:10px;
                    padding:5px;
                    border:0.5px solid hsl(31, 17%, 32%);
                }
                QPushButton:hover{
                    background-color:hsl(31, 21%, 46%);
                    color:hsl(51, 36%, 86%);
                    border:0.5px solid hsl(31, 21%, 78%);
                }
                QPushButton:pressed{
                    background-color:hsl(20, 62%, 55%);
                    color:hsl(51, 36%, 46%);
                    border:0.5px solid hsl(31, 17%, 12%);
                }
                """)
        self.button.clicked.connect(self.on_click)
        self.label.setFont(QFont("Arial", 20))
        self.label.setGeometry(256, 260, 100, 30)
        
    def setup_checkbox(self):
        self.checkbox.setGeometry(10, 5, 150, 40)
        self.checkbox.setStyleSheet("font-size:20px;"
                                    "font-family:Comic Sans MS;")
        self.checkbox.stateChanged.connect(self.checkbox_changed)
        self.label_checkbox.setGeometry(20, 40, 170, 40)
        self.label_checkbox.setStyleSheet("font-size:20px;"
                                          "font-family:Comic Sans MS;")
        self.label_checkbox.setText("Unchecked")
        
    def line_edit_setup(self):
        self.line_edit.setGeometry(10, 440, 170, 50)
        self.line_edit.setStyleSheet("font-size:20px;"
                                     "font-family:Comic Sans MS;"
                                     "background-color:#d5e6c5;")
        self.button_submit.setGeometry(190, 440, 100, 50)
        self.button_submit.setStyleSheet("""
                QPushButton{
                    font-size:20px;
                    font-weight:bold;
                    font-family:Comic Sans MS;
                    background-color:hsl(175, 46%, 95%);
                    color:hsl(217, 37%, 26%);
                    border-radius:10px;
                    padding:5px;
                    border:0.5px solid hsl(175, 46%, 55%);
                }
                QPushButton:hover{
                    background-color:hsl(217, 44%, 23%);
                    color:hsl(175, 52%, 87%);
                    border:0.5px solid hsl(175, 46%, 95%);
                }
                QPushButton:pressed{
                    background-color:hsl(175, 46%, 55%);
                    color:hsl(217, 37%, 46%);
                    border:0.5px solid hsl(175, 46%, 55%);
                }
        """)
        self.line_edit.setPlaceholderText("Enter name here")
        self.button_submit.clicked.connect(self.submit_text)
        
    def submit_text(self):
        text=self.line_edit.text()
        print(f"Submitted text: {text}")
        
    def setup_radio_buttons(self):
        self.radio1.setGeometry(10, 90, 100, 30)
        self.radio2.setGeometry(10, 120, 110, 30)
        self.radio3.setGeometry(10, 150, 100, 30)
        self.radio4.setGeometry(10, 180, 100, 30)
        self.radio5.setGeometry(10, 210, 100, 30)
        self.button_group1.addButton(self.radio1)
        self.button_group1.addButton(self.radio2)
        self.button_group1.addButton(self.radio3)
        self.button_group2.addButton(self.radio4)
        self.button_group2.addButton(self.radio5)
        self.radio1.toggled.connect(self.radio_button_changed)
        self.radio2.toggled.connect(self.radio_button_changed)  
        self.radio3.toggled.connect(self.radio_button_changed)
        self.radio4.toggled.connect(self.radio_button_changed)
        self.radio5.toggled.connect(self.radio_button_changed)
    
    def radio_button_changed(self):
        radio_button=self.sender()
        if radio_button.isChecked():
            print(f"{radio_button.text()} is selected")
    
    def checkbox_changed(self, state):
        if state == Qt.Checked:
            print("Checkbox checked")
            self.label_checkbox.setText("Checked")
            self.label_checkbox.setGeometry(20, 40, 150, 40)
        else:
            print("Checkbox unchecked")
            self.label_checkbox.setText("Unchecked")
            self.label_checkbox.setGeometry(20, 40, 170, 40)

    def on_click(self):
        print("Button clicked!")
        self.button.setText("Clicked")
        self.label.setText("Goodbye!")
        self.label.setGeometry(216, 260, 170, 50)
        

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
        
if __name__ == "__main__":
    main()