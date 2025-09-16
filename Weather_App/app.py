import sys
import requests
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    if hasattr(sys, '_MEIPASS'):  # PyInstaller creates this temp folder
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label=QLabel("Enter city name: ", self)
        self.city_input=QLineEdit(self)
        self.get_weather_button=QPushButton("Get Weather", self)
        self.temperature_label=QLabel("", self)
        self.temperature_feels_label=QLabel("", self)
        self.emoji_label=QLabel("", self)
        self.description_label=QLabel("", self)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setGeometry(600, 350, 600, 500)
        self.setWindowIcon(QIcon(resource_path("weather.ico")))
        vbox=QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.setStyleSheet("""
                QLabel, QPushButton{
                    font-family:"Comic Sans MS";
                }           
                QLabel#city_label{
                    font-size:28px;
                    font-style:italic;
                    font-family: "Comic Sans MS";
                }
                QLineEdit#city_input{
                    font-size:38px;
                }
                QPushButton#get_weather_button{
                    font-size:30px;
                    background-color:#a1e6d9;
                    color:#051411;
                    border-radius:10px;
                    padding:10px;
                    border:0.5px solid #051411;
                }
                QLabel#temperature_label{
                    font-size:38px;
                }
                QLabel#description_label{
                    font-size:38px;
                    font-family: "Comic Sans MS";
                }
                QPushButton#get_weather_button:hover{
                    background-color:#84d6c9;
                }
                QPushButton#get_weather_button:pressed{
                    background-color:#63c5b9;
                }
                """)
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key="f475eac319d01459343f35150d4f6edd"
        city=self.city_input.text()
        url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()
            if data["cod"]==200:
                self.display_weather(data)
            else:
                self.display_error(data["message"])
        except requests.exceptions.HTTPError:
            match response.status_code:
                case 404:
                    self.display_error("Error:\nCity not found")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 400:
                    self.display_error("Bad request")
                case 500:
                    self.display_error("Internal server error:\nPlease try again later")
                case 403:
                    self.display_error("Forbidden:\nAccess denied")
                case 502:
                    self.display_error("Bad Gateway:\nCheck the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error("HTTP error")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error:\n{req_error}") 
    
    def display_error(self, message):
        self.temperature_label.clear()
        self.description_label.clear()
        self.emoji_label.setStyleSheet("""
                font-size: 32px;
                color: hsl(12, 60%, 19%);    
                font-family: "Comic Sans MS";
                    """)
        self.emoji_label.setText(message)
    
    def display_weather(self, data):
        temperature=data["main"]["temp"]
        self.temperature_label.setText(f"{temperature-273.15:.2f}°C")
        description=data["weather"][0]["description"].capitalize()
        self.description_label.setText(description)
        weather_id=data["weather"][0]["id"]
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.emoji_label.setStyleSheet("""
                font-size: 90px;
                font-family: Segoe UI emoji;
                    """)
        
    @staticmethod
    def get_weather_emoji(weather_id):
        if weather_id in range(210, 222):
            return "🌩️"
        elif weather_id in range(200, 232):
            return "⛈️"
        elif weather_id==300:
            return "🌦️"
        elif weather_id in range(301, 321):
            return "🌧️"
        elif weather_id in range(500, 532):
            return "🌧️"
        elif weather_id in range(600, 602):
            return "❄️"
        elif weather_id in range(611, 623):
            return "❄️🌨️"
        elif weather_id in range(700, 762):
            return "🌫️"
        elif weather_id==781:
            return "🌪️"
        elif weather_id==771:
            return "💨"
        elif weather_id==762:
            return "🌋"
        elif weather_id==800:
            return "☀️"
        elif weather_id==801:
            return "🌥️"
        elif weather_id in range(802, 805):
            return "☁️"
        else:
            return "☀️"

if __name__=="__main__":
    import ctypes
    myappid = 'mycompany.weatherapp.1.0'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app=QApplication(sys.argv)
    app.setWindowIcon(QIcon("weather.ico"))
    weather_app=WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
    