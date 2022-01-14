#Imports -- Web Extracting
import requests

#Imports -- GUI
import sys
from PyQt5.QtGui import*
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from PyQt5 import QtCore

#Imports -- Etc.
import os
import re
import threading
import time
from string import Template
from pygame import mixer

#Audio
def music():
    path= os.path.dirname(__file__)
    start = str(path)
    start = start.replace("\\", "/")
    song = f"{start}/assets/rfmsmoothjazz.mp3"
    mixer.init()
    mixer.music.load(song)
    mixer.music.set_volume(.5)
    while True:
        mixer.music.play()
        time.sleep(228)
              
t=threading.Thread(target=music, daemon = True)
t.start()


#Template
class Update():
    
    #day_order that starts with "1,2,3" means night   
    day_order = (1,2,3,4,5,6,7,8)
    
    changed_text = "Weather"
    
    def __init__(self, text = None):
        self.text = text
        
    def get_text(self):
        return self.text
    
    def set_text(self, new_text):
       self.text = new_text
       
    def text_update(entered):
        pull = Update()
        pull.set_text(entered)
        result = pull.text
        template = Template("$text")
        text_string = template.safe_substitute(text = result)
        Update.changed_text = text_string
        
    def order_update(amchecker):
        if amchecker == True:
            order_count = ("3456789")
        else:
            order_count = ("23456789")
        pull = Update()
        pull.set_text(order_count)
        result = pull.text
        template = Template("$text")
        text_string = template.safe_substitute(text = result)
        if text_string[0] == "3":
            days = list(map(int, text_string))
            days.append(10)
            days = tuple(days)
        else:
            days = tuple(map(int, text_string)) 
        Update.day_order = days
    
        
#GUI        
class MainWindow(QWidget):
    
    #Scaling
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    
    def __init__ (self):
        super().__init__()
        self.title = "Weather"
        self.left = 200
        self.top = 300
        self.width = 550
        self.height = 550
        self.mw_attributes()
        self.button_1()
        self.button_2()
        self.button_3()
        self.button_4()
        self.button_5()
        self.present_button()
        self.mute_button()
        self.sound_cut = False
        self.day_1()
        self.day_2()
        self.day_3()
        self.day_4()
        self.day_5()
        self.zip_code_input()
        self.show()
    
    def mw_attributes(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top,self.width, self.height)
        self.setFixedSize(self.size())
        self.label = QLabel(self)
        path= os.path.dirname(__file__)
        start = str(path)
        self.start = start.replace("\\", "/")
        self.pixmap = QPixmap(f"{start}/assets/defaultbg.png")
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.width(),self.pixmap.height())
        info_text = "Please enter a zipcode above to get started."
        self.detail_screen = QLabel(info_text,self)
        self.detail_screen.setGeometry(302, 93, 227, 130)
        self.detail_screen.setStyleSheet("color: white")
        self.detail_screen.setFont(QFont('Arial',10))
        self.detail_screen.setWordWrap(True)
        
        
    def zip_code_input(self):
        self.line = QLineEdit(self)
        self.line.setPlaceholderText("Zip Code...")
        self.line.resize(64,32)
        self.line.move(402,30)

    def button_1(self):
        self.button = QtWidgets.QPushButton(self)
        self.button.clicked.connect(self.button_1_click)
        self.button.setEnabled(True)
        self.button.setText("")
        self.button.setStyleSheet("QPushButton"
                               "{"
                               "background:green;"f"background-image : url({self.start}/assets/magnifyingglass.png);"
                               "}"
                               "QPushButton:pressed"
                               "{"
                               "background:green;"f"background-image : url({self.start}/assets/magnifyingglasspressed.png);"
                               "}"
                               )
                               
        self.button.resize (48,48)
        self.button.move(470,22)
        
        
    def button_1_click(self):
        Meat.extract(self)
        self.button2.setEnabled(True)
        self.button3.setEnabled(True)
        self.button4.setEnabled(True)
        self.button5.setEnabled(True)
        self.buttonp.setEnabled(True)

    def button_2(self):
        self.button2 = QtWidgets.QPushButton(self)
        self.button2.clicked.connect(self.button_2_click)
        self.button2.setEnabled(False)
        self.button2.setText("+")
        self.button2.resize (78,35)
        self.button2.move(26,480)
        
    def button_2_click(self):
        Meat.transform(self.day_2_detail)
        Meat.paste_info(self, self.detail_screen.setText)
        
    
    def button_3(self):
        self.button3 = QtWidgets.QPushButton(self)
        self.button3.clicked.connect(self.button_3_click)
        self.button3.setEnabled(False)
        self.button3.setText("+")
        self.button3.resize (78,35)
        self.button3.move(161,480)
        
    def button_3_click(self):
        Meat.transform(self.day_3_detail)
        Meat.paste_info(self, self.detail_screen.setText)
        
    def button_4(self):
        self.button4 = QtWidgets.QPushButton(self)
        self.button4.clicked.connect(self.button_4_click)
        self.button4.setEnabled(False)
        self.button4.setText("+")
        self.button4.resize (78,35)
        self.button4.move(304,480)
        
    def button_4_click(self):
        Meat.transform(self.day_4_detail)
        Meat.paste_info(self, self.detail_screen.setText)
        
    def button_5(self):
        self.button5 = QtWidgets.QPushButton(self)
        self.button5.clicked.connect(self.button_5_click)
        self.button5.setEnabled(False)
        self.button5.setText("+")
        self.button5.resize (78,35)
        self.button5.move(444,480)
        
    def button_5_click(self):
        Meat.transform(self.day_5_detail)
        Meat.paste_info(self, self.detail_screen.setText)
        
    def present_button(self):
        self.buttonp = QtWidgets.QPushButton(self)
        self.buttonp.clicked.connect(self.present_button_click)
        self.buttonp.setEnabled(False)
        self.buttonp.setText("+")
        self.buttonp.resize (35,25)
        self.buttonp.move(30,195)
        
    def present_button_click(self):
        Meat.transform(self.day_1_detail)
        Meat.paste_info(self, self.detail_screen.setText)
        
    def mute_button(self):
        self.buttonm = QtWidgets.QPushButton(self)
        self.buttonm.clicked.connect(self.mute_button_click)
        self.buttonm.setEnabled(True)
        self.buttonm.setStyleSheet("QPushButton"
                               "{"
                               "background:transparent;"f"background-image : url({self.start}/assets/volumeon.png);"   
                               "}")  
        self.buttonm.resize (23,31)
        self.buttonm.move(355,5)
        
    def mute_button_click(self):
        if self.sound_cut == True:
            mixer.music.set_volume(.5)
            self.sound_cut = False
            self.buttonm.setStyleSheet("QPushButton"
                               "{"
                               "background:transparent;"f"background-image : url({self.start}/assets/volumeon.png);"   
                               "}")  
        else:
            mixer.music.set_volume(0)
            self.sound_cut = True
            self.buttonm.setStyleSheet("QPushButton"
                               "{"
                               "background:transparent;"f"background-image : url({self.start}/assets/volumeoff.png);"   
                               "}")  
            
        
    
    def day_1(self):
        location_text = "---"
        date_text = "--"
        day_text = "Today"
        text = "Present: \n      High: \n      Low:"
        text_2 =  "-°"
        text_3 = "-°"
        text_4 = "-°"
        self.day_1_screen = QLabel (text, self)
        self.day_1_screen.setGeometry(55, 110, 80, 100)
        self.day_1_screen.setStyleSheet("color: white")
        self.day_1_screen.setFont(QFont('Arial',14))
        self.day_1_t_screen = QLabel (text_2, self)
        self.day_1_t_screen.setGeometry(131, 87, 300, 100)
        self.day_1_t_screen.setStyleSheet("color: white")
        self.day_1_t_screen.setFont(QFont('Arial',14))
        self.day_1_ht_screen = QLabel (text_3, self)
        self.day_1_ht_screen.setGeometry(131, 108, 300, 100)
        self.day_1_ht_screen.setStyleSheet("color: white")
        self.day_1_ht_screen.setFont(QFont('Arial',14))
        self.day_1_lt_screen = QLabel (text_4, self)
        self.day_1_lt_screen.setGeometry(131, 132, 300, 100)
        self.day_1_lt_screen.setStyleSheet("color: white")
        self.day_1_lt_screen.setFont(QFont('Arial',14))
        self.day_1_location_screen = QLabel (location_text, self)
        self.day_1_location_screen.setGeometry(85, 55, 171, 100)
        self.day_1_location_screen.setStyleSheet("color: white")
        self.day_1_location_screen.setFont(QFont('Arial',16))
        self.day_1_location_screen.setWordWrap(True)
        self.day_1_day_screen = QLabel (day_text, self)
        self.day_1_day_screen.setGeometry(95, 20, 300, 100)
        self.day_1_day_screen.setStyleSheet("color: white")
        self.day_1_day_screen.setFont(QFont('Arial',18))
        self.day_1_date_screen = QLabel (date_text, self)
        self.day_1_date_screen.setGeometry(48, 10, 300, 100)
        self.day_1_date_screen.setStyleSheet("color: white")
        self.day_1_date_screen.setFont(QFont('Arial',8))
        self.day_1_image_screen = QLabel(self)
        self.day_1_image_screen.setStyleSheet("background-image :")
        self.day_1_image_screen.setGeometry(170, 141, 52, 50)
        
    def day_2(self):
        date_text = "--"
        day_text = "---"
        text = "High: \nLow:"
        text_2 = "-°"
        text_3 = "-°"
        self.day_2_screen = QLabel (text, self)
        self.day_2_screen.setGeometry(26, 290, 300, 100)
        self.day_2_screen.setStyleSheet("color: white")
        self.day_2_screen.setFont(QFont('Arial',14))
        self.day_2_ht_screen = QLabel (text_2, self)
        self.day_2_ht_screen.setGeometry(74, 278, 300, 100)
        self.day_2_ht_screen.setStyleSheet("color: white")
        self.day_2_ht_screen.setFont(QFont('Arial',14))
        self.day_2_lt_screen = QLabel (text_3, self)
        self.day_2_lt_screen.setGeometry(74, 302, 300, 100)
        self.day_2_lt_screen.setStyleSheet("color: white")
        self.day_2_lt_screen.setFont(QFont('Arial',14))
        self.day_2_day_screen = QLabel (day_text, self)
        self.day_2_day_screen.setGeometry(24, 240, 110, 108)
        self.day_2_day_screen.setStyleSheet("color: white")
        self.day_2_day_screen.setFont(QFont('Arial',14))
        self.day_2_day_screen.setWordWrap(True)
        self.day_2_date_screen = QLabel (date_text, self)
        self.day_2_date_screen.setGeometry(8, 216, 300, 100)
        self.day_2_date_screen.setStyleSheet("color: white")
        self.day_2_date_screen.setFont(QFont('Arial',8))
        self.day_2_image_screen = QLabel(self)
        self.day_2_image_screen.setStyleSheet("background-image :")
        self.day_2_image_screen.setGeometry(46, 380, 52, 50)
        
    def day_3(self):
        date_text = "--"
        day_text = "---"
        text = "High: \nLow:"
        text_2 = "-°"
        text_3 = "-°"
        self.day_3_screen = QLabel (text, self)
        self.day_3_screen.setGeometry(165, 290, 300, 100)
        self.day_3_screen.setStyleSheet("color: white")
        self.day_3_screen.setFont(QFont('Arial',14))
        self.day_3_ht_screen = QLabel (text_2, self)
        self.day_3_ht_screen.setGeometry(212, 278, 300, 100)
        self.day_3_ht_screen.setStyleSheet("color: white")
        self.day_3_ht_screen.setFont(QFont('Arial',14))
        self.day_3_lt_screen = QLabel (text_3, self)
        self.day_3_lt_screen.setGeometry(212, 302, 300, 100)
        self.day_3_lt_screen.setStyleSheet("color: white")
        self.day_3_lt_screen.setFont(QFont('Arial',14))
        self.day_3_day_screen = QLabel (day_text, self)
        self.day_3_day_screen.setGeometry(160, 240, 110, 108)
        self.day_3_day_screen.setStyleSheet("color: white")
        self.day_3_day_screen.setFont(QFont('Arial',14))
        self.day_3_day_screen.setWordWrap(True)
        self.day_3_date_screen = QLabel (date_text, self)
        self.day_3_date_screen.setGeometry(142, 216, 300, 100)
        self.day_3_date_screen.setStyleSheet("color: white")
        self.day_3_date_screen.setFont(QFont('Arial',8))
        self.day_3_image_screen = QLabel(self)
        self.day_3_image_screen.setStyleSheet("background-image :")
        self.day_3_image_screen.setGeometry(170, 380, 52, 50)
        
    def day_4(self):
        date_text = "--"
        day_text = "---"
        text = "High: \nLow:"
        text_2 = "-°"
        text_3 = "-°"
        self.day_4_screen = QLabel (text, self)
        self.day_4_screen.setGeometry(302, 290, 300, 100)
        self.day_4_screen.setStyleSheet("color: white")
        self.day_4_screen.setFont(QFont('Arial',14))
        self.day_4_ht_screen = QLabel (text_2, self)
        self.day_4_ht_screen.setGeometry(350, 278, 300, 100)
        self.day_4_ht_screen.setStyleSheet("color: white")
        self.day_4_ht_screen.setFont(QFont('Arial',14))
        self.day_4_lt_screen = QLabel (text_3, self)
        self.day_4_lt_screen.setGeometry(350, 302, 300, 100)
        self.day_4_lt_screen.setStyleSheet("color: white")
        self.day_4_lt_screen.setFont(QFont('Arial',14))
        self.day_4_day_screen = QLabel (day_text, self)
        self.day_4_day_screen.setGeometry(293, 240, 110, 108)
        self.day_4_day_screen.setStyleSheet("color: white")
        self.day_4_day_screen.setFont(QFont('Arial',14))
        self.day_4_day_screen.setWordWrap(True)
        self.day_4_date_screen = QLabel (date_text, self)
        self.day_4_date_screen.setGeometry(282, 216, 300, 100)
        self.day_4_date_screen.setStyleSheet("color: white")
        self.day_4_date_screen.setFont(QFont('Arial',8))
        self.day_4_date_screen.setFont(QFont('Arial',8))
        self.day_4_image_screen = QLabel(self)
        self.day_4_image_screen.setStyleSheet("background-image :")
        self.day_4_image_screen.setGeometry(310, 380, 52, 50)
        
    def day_5(self):
        date_text = "--"
        day_text = "---"
        text = "High: \nLow:"
        text_2 = "-°"
        text_3 = "-°"
        self.day_5_screen = QLabel (text, self)
        self.day_5_screen.setGeometry(438, 290, 300, 100)
        self.day_5_screen.setStyleSheet("color: white")
        self.day_5_screen.setFont(QFont('Arial',14))
        self.day_5_ht_screen = QLabel (text_2, self)
        self.day_5_ht_screen.setGeometry(486, 278, 300, 100)
        self.day_5_ht_screen.setStyleSheet("color: white")
        self.day_5_ht_screen.setFont(QFont('Arial',14))
        self.day_5_lt_screen = QLabel (text_3, self)
        self.day_5_lt_screen.setGeometry(486, 302, 300, 100)
        self.day_5_lt_screen.setStyleSheet("color: white")
        self.day_5_lt_screen.setFont(QFont('Arial',14))
        self.day_5_day_screen = QLabel (day_text, self)
        self.day_5_day_screen.setGeometry(434, 240, 110, 108)
        self.day_5_day_screen.setStyleSheet("color: white")
        self.day_5_day_screen.setFont(QFont('Arial',14))
        self.day_5_day_screen.setWordWrap(True)
        self.day_5_date_screen = QLabel (date_text, self)
        self.day_5_date_screen.setGeometry(422, 216, 300, 100)
        self.day_5_date_screen.setStyleSheet("color: white")
        self.day_5_date_screen.setFont(QFont('Arial',8))
        self.day_5_image_screen = QLabel(self)
        self.day_5_image_screen.setStyleSheet("background-image :")
        self.day_5_image_screen.setGeometry(450, 380, 52, 50)

#Code        
class Meat():
    
    images = {"rain": '/assets/rain.gif',"rain-snow": '/assets/rain-snow.gif', "snow": '/assets/snow.gif', "sunny": '/assets/sunny.gif', "clear": '/assets/clear.gif', "storm": '/assets/storm.gif',
              "cloudy": '/assets/cloudy.gif',"fog": '/assets/fog.gif', "warning": '/assets/warning.gif'}
    
    skin = {"rain": '/assets/rainbg.png', "snow": '/assets/snowbg.png', "sunny": '/assets/sunnybg.png', "clear": '/assets/clearbg.png', "moonclear": '/assets/moonclearbg.png', "storm": '/assets/stormbg.png',
              "cloudy": '/assets/cloudybg.png', "mooncloudy": '/assets/mooncloudybg.png',"fog": '/assets/fogbg.png', "warning": '/assets/warningbg.png'}
          
    def transform (entered):
        Update.text_update(entered)
        template = Template("$t_score")
        transformed_score = template.safe_substitute(t_score = Update.changed_text)
        
    def order_transform (self):
        if self.earlyam == True:
            Update.order_update(True)
        else:
            Update.order_update(False)
        template = Template("$t_score")
        transformed_score = template.safe_substitute(t_score = Update.day_order)
        
    def find_forecast(self, section, day):
        precipitation = ('rain', 'showers', 'storm', 'snow', 'flurries')
        sky_forecasts = ('rain', 'showers', 'storm', 'thunder', 'snow', 'flurries', 'fog', 'mist', 'sunny', 'clear')
        all_rain = sky_forecasts[:2]
        all_snow = sky_forecasts[4:6]
        all_storm = sky_forecasts[2:4]
        all_fog = sky_forecasts[6:8]
        all_clear = sky_forecasts[8:]
        all_clouds = ("cloudy", "overcast")
        all_warning = ("blizzard", "tornado", "earthquake", "hurricane", "flood", "hail", "fire", "landslide", "mudslide", "avalanche", "volcano", "eruption", "lava")
        
        Meat.run_api(self,section)
        detailed = self.data["properties"]["periods"][day]["detailedForecast"]
        short = self.data["properties"]["periods"][day]["shortForecast"]
        short_forecast = str(short.lower())
        self.weather_of_day = None
        self.short_weather = short
        self.detailed_weather = detailed
        detailed_checker = str(detailed.lower())
        self.bg = None

        
        if any (selection in short_forecast for selection in precipitation):
            day_measured = str(detailed)
            pattern =  r'precipitation is \d+%'
            matches = re.findall(pattern, day_measured)
            m = str(matches)
            numbers = re.findall('[0-9]+', m)
            
            try:
                number = int(numbers[0])
                if number > 30:
                    if any (selection in short_forecast for selection in all_warning):
                        self.weather_of_day = "warning"
                        self.bg = "warning"

                    elif any (selection in short_forecast for selection in all_storm):
                        self.weather_of_day = "storm"
                        self.bg = "storm"
                    else:
                        #Rain
                        if any (selection in short_forecast for selection in all_rain):                               
                            if any (selection in short_forecast for selection in all_snow):
                                self.weather_of_day = "rain-snow"
                                self.bg = "snow"

                            else:
                                self.weather_of_day = "rain"
                                self.bg = "rain"

                        #Snow
                        elif any (selection in short_forecast for selection in all_snow):
                            self.weather_of_day = "snow"
                            self.bg ="snow"

                        #Hazard    
                        else:
                            self.weather_of_day = "warning"
                            self.bg = "warning"

                else:
                    #This is what happens if preciptation is below 30%
                    if any (selection in short_forecast for selection in all_warning):
                        self.weather_of_day = "warning"
                        self.bg = "warning"

                    
                                           
                    elif any (selection in short_forecast for selection in all_clouds):
                        self.weather_of_day = "cloudy"
                        self.bg ="cloudy"

                    
                    elif any (selection in short_forecast for selection in all_clear):
                        #if night:
                        if self.night ==True:
                            self.weather_of_day = "clear"
                            self.bg = "clear"

                        else:
                            self.weather_of_day = "sunny"
                            self.bg = "sunny"
                            
                    elif any (selection in detailed_checker for selection in all_clear):
                        #if night:
                        if self.night ==True:
                            self.weather_of_day = "clear"
                            self.bg ="clear"

                        else:
                            self.weather_of_day = "sunny"
                            self.bg ="sunny"
                            
                    elif any (selection in detailed_checker for selection in all_clouds):
                        self.weather_of_day = "cloudy"
                        self.bg = "cloudy"
                        
                    else:    
                        self.weather_of_day = "warning"
                        self.bg = "warning"
 
            except IndexError:
                if any (selection in short_forecast for selection in all_warning):
                    self.weather_of_day = "warning"
                    self.bg = "warning"

                elif any (selection in short_forecast for selection in all_storm):
                        self.weather_of_day = "storm"
                        self.bg = "storm"

                else:
                    #Rain
                    if any (selection in short_forecast for selection in all_rain):      
                        if any (selection in short_forecast for selection in all_snow):
                            self.weather_of_day = "rain-snow"
                            self.bg = "snow"

                        else:
                            self.weather_of_day = "rain"
                            self.bg = "rain"
                    #Snow
                    elif any (selection in short_forecast for selection in all_snow):
                        self.weather_of_day = "snow"
                        self.bg = "snow"

                    #Hazard    
                    else:
                        self.weather_of_day = "warning"
                        self.bg = "warning"
            
        else:
            #This is what happens if there is no preciptation at all 
            if any (selection in short_forecast for selection in all_warning):
                self.weather_of_day = "warning"
                self.bg = "warning"

            elif any (selection in short_forecast for selection in all_fog) and self.night ==True:
                self.weather_of_day = "fog"
                self.bg = "fog"
                    
            elif any (selection in short_forecast for selection in all_clouds):
                #if night:
                if self.night ==True:
                    self.weather_of_day = "cloudy"
                    self.bg = "mooncloudy"
                #else day:
                else:
                    self.weather_of_day = "cloudy"
                    self.bg = "cloudy"

            
            elif any (selection in short_forecast for selection in all_clear):
                #if night:
                if self.night ==True:
                    self.weather_of_day = "clear"
                    self.bg = "moonclear"
                #else day:
                else:
                    self.weather_of_day = "sunny"
                    self.bg =  "sunny"
                    
            elif any (selection in short_forecast for selection in all_fog):
                self.weather_of_day = "fog"
                self.bg = "fog"
            else:    
                self.weather_of_day = "warning"
                self.bg = "warning"
 
        
    
    def create_image_link(self, dir):
        self.link = self.start + dir
        self.gif = QMovie(f'{self.link}')



    def run_api(self, specify):
        contact = {'User-Agent': '(portfolio: https://github.com/gunraidan, contact: kiticanax@gmail.com)'}
        response = requests.get (f'https://api.weather.gov/points/{self.geolocation}', headers = contact)
        self.data = response.json()
        forecast = self.data["properties"][specify]
        response = requests.get(forecast)
        self.data = response.json()
        
        
    def run_zip(self,zip):        
        headers = { 
        "apikey": "30ad1fa0-4b34-11ec-9573-4dfc542bc923"}

        params = (
        ("codes",zip),("country", "US")
        );

        response = requests.get('https://app.zipcodebase.com/api/v1/search', headers=headers, params=params);
        data = response.json()
        self.longitude = data["results"][zip][0]["longitude"]
        self.latitude = data["results"][zip][0]["latitude"]
        self.geolocation = f"{self.latitude},{self.longitude}"

        
    def extract(self):
        #Geolocating
        Meat.transform(self.line.text())
        template = Template("$text")
        self.zipcode = template.safe_substitute(text = Update.changed_text)
        self.error_box = None
        try:
            Meat.run_zip(self, self.zipcode)
            self.error_box = False
        except TypeError:
            error_message = "Can't locate zip code. Please be sure to use numbers only."
            Meat.transform(error_message)
            Meat.paste_info(self, self.detail_screen.setText)
            self.error_box = True
        #Weather Data    
        try:        
            #Day 1
            Meat.run_api(self, "forecastHourly")    
            day_1_temp = self.data["properties"]["periods"][0]["temperature"]
            Meat.transform(day_1_temp)
            Meat.paste_temp(self, self.day_1_t_screen.setText)
            response = requests.get (f'https://api.weather.gov/points/{self.geolocation}')
            data = response.json()
            city = data["properties"]["relativeLocation"]["properties"]["city"]
            state = data["properties"]["relativeLocation"]["properties"]["state"]
            location = f"{city}, {state}"
            Meat.transform(location)
            Meat.paste_info(self, self.day_1_location_screen.setText)
            Meat.current_date(self)
            Meat.order_check(self)
            Meat.find_forecast(self,"forecastHourly",0)
            self.night = False
            Meat.create_image_link(self,Meat.images[self.weather_of_day])
            self.day_1_image_screen.setMovie(self.gif)
            self.gif.start()
            skin_present = Meat.skin[self.bg]
            self.skin_select = f"{self.start}{skin_present}"
            self.pixmap.load(self.skin_select)
            self.label.setPixmap(self.pixmap)
            Meat.find_forecast(self,"forecast", 0)
            self.day_1_detail = "CURRENT DATE: " + self.detailed_weather
            if self.error_box == True:
                error_message = "Can't locate zip code. Please be sure to use numbers only."
                Meat.transform(error_message)
                Meat.paste_info(self, self.detail_screen.setText)
            else:
                Meat.transform(self.day_1_detail)
                Meat.paste_info(self, self.detail_screen.setText)
  
  
  
  
            #Day 2
            day_2_hi_temp = self.data["properties"]["periods"][Update.day_order[0]]["temperature"]
            Meat.transform(day_2_hi_temp)
            Meat.paste_temp(self, self.day_2_ht_screen.setText)
            day_2_lo_temp = self.data["properties"]["periods"][Update.day_order[1]]["temperature"]
            Meat.transform(day_2_lo_temp)
            Meat.paste_temp(self, self.day_2_lt_screen.setText)
            day_2_day = self.data["properties"]["periods"][Update.day_order[0]]["name"]
            Meat.transform(day_2_day)
            Meat.paste_info(self, self.day_2_day_screen.setText)
            day_2_date = self.data["properties"]["periods"][Update.day_order[0]]["startTime"][:10]
            day_2_date_cut = day_2_date[5:]
            Meat.transform(day_2_date_cut)
            Meat.paste_info(self, self.day_2_date_screen.setText)
            Meat.find_forecast(self,"forecast",Update.day_order[0])
            self.day_2_detail = day_2_day.upper() + ": " + self.detailed_weather
            Meat.create_image_link(self,Meat.images[self.weather_of_day])
            self.day_2_image_screen.setMovie(self.gif)
            self.gif.start()
            
            
            #Day 3
            day_3_hi_temp = self.data["properties"]["periods"][Update.day_order[2]]["temperature"]
            Meat.transform(day_3_hi_temp)
            Meat.paste_temp(self, self.day_3_ht_screen.setText)
            day_3_lo_temp = self.data["properties"]["periods"][Update.day_order[3]]["temperature"]
            Meat.transform(day_3_lo_temp)
            Meat.paste_temp(self, self.day_3_lt_screen.setText)
            day_3_day = self.data["properties"]["periods"][Update.day_order[2]]["name"]
            Meat.transform(day_3_day)
            Meat.paste_info(self, self.day_3_day_screen.setText)
            day_3_date = self.data["properties"]["periods"][Update.day_order[2]]["startTime"][:10]
            day_3_date_cut = day_3_date[5:]
            Meat.transform(day_3_date_cut)
            Meat.paste_info(self, self.day_3_date_screen.setText)
            Meat.find_forecast(self,"forecast",Update.day_order[2])
            self.day_3_detail = day_3_day.upper() + ": " + self.detailed_weather
            Meat.create_image_link(self,Meat.images[self.weather_of_day])
            self.day_3_image_screen.setMovie(self.gif)
            self.gif.start()
            
            #Day 4
            day_4_hi_temp = self.data["properties"]["periods"][Update.day_order[4]]["temperature"]
            Meat.transform(day_4_hi_temp)
            Meat.paste_temp(self, self.day_4_ht_screen.setText)
            day_4_lo_temp = self.data["properties"]["periods"][Update.day_order[5]]["temperature"]
            Meat.transform(day_4_lo_temp)
            Meat.paste_temp(self, self.day_4_lt_screen.setText)
            day_4_day  = self.data["properties"]["periods"][Update.day_order[4]]["name"]
            Meat.transform(day_4_day)
            Meat.paste_info(self, self.day_4_day_screen.setText)
            day_4_date = self.data["properties"]["periods"][Update.day_order[4]]["startTime"][:10]
            day_4_date_cut = day_4_date[5:]
            Meat.transform(day_4_date_cut)
            Meat.paste_info(self, self.day_4_date_screen.setText)
            Meat.find_forecast(self,"forecast",Update.day_order[4])
            self.day_4_detail = day_4_day.upper() + ": " + self.detailed_weather
            Meat.create_image_link(self,Meat.images[self.weather_of_day])
            self.day_4_image_screen.setMovie(self.gif)
            self.gif.start()
            
            #Day 5
            day_5_hi_temp = self.data["properties"]["periods"][Update.day_order[6]]["temperature"]
            Meat.transform(day_5_hi_temp)
            Meat.paste_temp(self, self.day_5_ht_screen.setText)
            day_5_lo_temp = self.data["properties"]["periods"][Update.day_order[7]]["temperature"]
            Meat.transform(day_5_lo_temp)
            Meat.paste_temp(self, self.day_5_lt_screen.setText)
            day_5_day = self.data["properties"]["periods"][Update.day_order[6]]["name"]
            Meat.transform(day_5_day)
            Meat.paste_info(self, self.day_5_day_screen.setText)
            day_5_date = self.data["properties"]["periods"][Update.day_order[6]]["startTime"][:10]
            day_5_date_cut = day_5_date[5:]
            Meat.transform(day_5_date_cut)
            Meat.paste_info(self, self.day_5_date_screen.setText)
            Meat.find_forecast(self,"forecast",Update.day_order[6])
            self.day_5_detail = day_5_day.upper() + ": " + self.detailed_weather
            Meat.create_image_link(self,Meat.images[self.weather_of_day])
            self.day_5_image_screen.setMovie(self.gif)
            self.gif.start()
            
        
        except:
            if self.error_box == True:
                error_message = "Can't locate zip code. Please be sure to use numbers only."
                Meat.transform(error_message)
                Meat.paste_info(self, self.detail_screen.setText)
            else:
                alert = "There seems to be connection issues with weather.gov. Please try again shortly."
                Meat.transform(alert)
                Meat.paste_info(self, self.detail_screen.setText)

    
    def paste_temp(self,text_variable):
        template = Template("$text")
        label_string = template.safe_substitute(text = Update.changed_text)
        text_variable(f"{label_string}°")
        
    def paste_info(self,text_variable):
        template2 = Template("$text")
        label_string = template2.safe_substitute(text = Update.changed_text)
        text_variable(label_string)
        
    def order_check(self):
        self.night = False
        self.earlyam = False
        Meat.run_api(self, "forecast")
        day_name = self.data["properties"]["periods"][2]["name"]
        is_it_day_check = self.data["properties"]["periods"][0]["isDaytime"]
        
        if is_it_day_check == False:
            lt_number = self.data["properties"]["periods"][0]["temperature"]
            Meat.transform(lt_number)
            Meat.paste_temp(self, self.day_1_lt_screen.setText) 
            Meat.transform("Tonight")
            Meat.paste_info(self, self.day_1_day_screen.setText)
            self.night = True   
            if self.late_night ==True:
                self.earlyam = True
                Meat.transform("Early AM")
                Meat.paste_info(self, self.day_1_day_screen.setText)
                Meat.order_transform(self)
                template = Template("$text")
                label_string = template.safe_substitute(text = Update.day_order)
                ht_number = self.data["properties"]["periods"][0]["temperature"]
                lt_number = self.data["properties"]["periods"][1]["temperature"]
                Meat.transform(ht_number)
                Meat.paste_temp(self, self.day_1_ht_screen.setText)
                Meat.transform(lt_number)
                Meat.paste_temp(self, self.day_1_lt_screen.setText)
        else:
            Meat.order_transform(self)
            template = Template("$text")
            label_string = template.safe_substitute(text = Update.day_order)
            ht_number = self.data["properties"]["periods"][0]["temperature"]
            lt_number = self.data["properties"]["periods"][1]["temperature"]
            Meat.transform(ht_number)
            Meat.paste_temp(self, self.day_1_ht_screen.setText)
            Meat.transform(lt_number)
            Meat.paste_temp(self, self.day_1_lt_screen.setText)
            
    def current_date(self):
        self.adder = 0
        months = ("01", "02", "04", "06", "08", "09", "11")
        Meat.run_api(self, "forecast")
        rough_date = self.data["properties"]["periods"][2]["startTime"][:10]
        year = int(rough_date[:4])
        rough_date_cut = rough_date[5:]
        stringed = str(rough_date_cut)
        splitting = stringed.split("-")
        month = int(splitting[0])
        day = int(splitting[1])
        day = day - 1
        complete_date = str(month + day)
        Meat.hour_check(self)
        Meat.run_api(self, "forecast")
        day = str(day + self.adder)
        month = str(month)
        if len(month)==1:
            month = "0"+ month
        if len(day)==1:
            day = "0"+ day
  
        if day == "01":
            if month in months:
                day = "31"
                month = str(int(month) - 1)
                current_date = month + "-" + day
                Meat.transform(current_date)
                Meat.paste_info(self, self.day_1_date_screen.setText)
                
            elif month == "03":
                if year % 4 == 0:
                    current_date = "02-29"
                    Meat.transform(current_date)
                    Meat.paste_info(self, self.day_1_date_screen.setText)
                
                else:
                    current_date = "02-28"
                    Meat.transform(current_date)
                    Meat.paste_info(self, self.day_1_date_screen.setText)
                
            else:
                day = "30"
                month = str(int(month) - 1)
                current_date = month + "-" + day
                Meat.transform(current_date)
                Meat.paste_info(self, self.day_1_date_screen.setText)        
        else:
            current_date = month + "-" + day
            Meat.transform(current_date)
            Meat.paste_info(self, self.day_1_date_screen.setText)

    def hour_check(self):
        self.late_night = False
        hours = ('01:00', '02:00', '03:00', '04:00', '05:00', '06:00')     
        Meat.run_api(self, "forecastHourly")
        time = self.data["properties"]["periods"][1]["startTime"][11:]
        time_cut = str(time[:5])
        if time_cut in hours:
            self.adder = 1
            self.late_night = True
        else:
            self.adder = 0
    

        


app = QApplication(sys.argv) 
ex = MainWindow()
code = app.exec()
sys.exit(code)
