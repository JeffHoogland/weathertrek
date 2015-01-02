import sys
import os
import platform
import datetime
import cPickle as pickle

#Google Maps module
# https://github.com/swistakm/python-gmaps
import gmaps
from gmaps import Directions
from gmaps import Geocoding

#Weather module
# https://code.google.com/p/python-weather-api/
import pywapi

from PySide.QtGui import *
from PySide.QtCore import *

from ui_weathertrek import Ui_MainWindow
from ui_locationFrame import Ui_LocationFrame

class LocationFrame(QFrame, Ui_LocationFrame):
    def __init__(self, parent):
        super(LocationFrame, self).__init__(parent)
        self.setupUi(self)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        
        #holds directions generated by gmaps.Directions
        self.directions = None
        
        #holds the lat, lng of all the end points in our directions
        self.positions = []

        #holds the zipcodes of all the end points in our directions
        self.zipcodes = []
        
        #holds weather reports generated by pywapi
        self.full_weather_y = []
        self.full_weather_wc = []
        
        #holds label objects with weather reports
        self.dataLabels = { "today":[],
                            "tomorrow":[],
                            "two":[],
                            "three":[],
                            "four":[]}
                            
        self.pmIcons = {    "Partly Cloudy":"icons/pm-cloudy.jpg",
                            "Ice Late":"icons/ice.jpg",
                            "Rain / Ice Late":"icons/rain-to-snow.jpg",
                            "Ice to Rain":"icons/rain-to-snow.jpg",
                            "Rain to Snow":"icons/rain-to-snow.jpg",
                            "Rain":"icons/rain.jpg",
                            "Snow":"icons/snow.jpg",
                            "Rain / Freezing Rain":"icons/rain-to-snow.jpg",
                            "Clear":"icons/pm-clear.jpg",
                            "Partly Cloudy / Wind":"icons/pm-cloudy.jpg",
                            "Clouds Early / Clearing Late":"icons/pm-cloudy.jpg",
                            "Snow Showers Late":"icons/snow.jpg",
                            "Mostly Cloudy":"icons/pm-cloudy.jpg",
                            "Flurries":"icons/snow.jpg",
                            "NA":"icons/na.jpg",
                            "Freezing Rain":"icons/rain-to-snow.jpg",
                            "Rain / Snow":"icons/rain-to-snow.jpg",
                            "Light Rain":"icons/light-rain.jpg",
                            "Mostly Clear":"icons/pm-clear.jpg",
                            "Showers / Wind":"icons/rain.jpg",
                            "PM Showers / Wind":"icons/rain.jpg",
                            "Cloudy":"icons/pm-cloudy.jpg",
                            "Scattered Flurries":"icons/snow.jpg",
                            "Snow Shower":"icons/snow.jpg"}
        
        self.amIcons = {    "Partly Cloudy":"icons/am-cloudy.jpg",
                            "AM Clouds / PM Sun":"icons/am-cloudy.jpg",
                            "Ice to Rain":"icons/hail.jpg",
                            "Rain to Snow":"icons/rain-to-snow.jpg",
                            "Rain":"icons/rain.jpg",
                            "Snow":"icons/snow.jpg",
                            "Rain / Freezing Rain":"icons/rain-to-snow.jpg",
                            "Clear":"icons/am-clear.jpg",
                            "Partly Cloudy / Wind":"icons/am-cloudy.jpg",
                            "PM Snow Showers / Wind":"icons/rain.jpg",
                            "Few Showers / Wind":"icons/rain.jpg",
                            "Sunny":"icons/am-clear.jpg",
                            "Mostly Cloudy":"icons/am-cloudy.jpg",
                            "Flurries":"icons/snow.jpg",
                            "NA":"icons/na.jpg",
                            "Mostly Sunny":"icons/am-clear.jpg",
                            "AM Snow Showers":"icons/snow.jpg",
                            "Freezing Rain":"icons/rain-to-snow.jpg",
                            "Rain / Snow":"icons/rain-to-snow.jpg",
                            "Light Rain":"icons/light-rain.jpg",
                            "Mostly Clear":"icons/pm-clear.jpg",
                            "Showers / Wind":"icons/rain.jpg",
                            "PM Showers / Wind":"icons/rain.jpg",
                            "Cloudy":"icons/pm-cloudy.jpg",
                            "Scattered Flurries":"icons/snow.jpg",
                            "Snow Shower":"icons/snow.jpg"}
        
        self.assignWidgets()
    
    def workingMessage( self ):
        self.statusbar.showMessage("Working...")
    
    def getWeather( self ):
        startLocation = self.startText.text()
        endLocation = self.endText.text()
        
        if startLocation and endLocation:
            self.directions = Directions().directions(startLocation, endLocation)
            self.directions = self.directions[0]
            
            self.positions = []
            self.zipcodes = []
            
            #Snag lat, lng of points into an easy to access list
            for i in range(len(self.directions["legs"][0]["steps"])):
                self.positions.append(self.directions["legs"][0]["steps"][i]["end_location"])
            
            #Get zip codes of all of these points
            for pos in self.positions:
                results = Geocoding(sensor=False).reverse(lat=pos["lat"], lon=pos["lng"])
                for i in range(len(results[0]['address_components'])):
                    if results[0]['address_components'][i]["types"][0] == "postal_code":
                        if results[0]['address_components'][i]["short_name"] not in self.zipcodes:
                            self.zipcodes.append(results[0]['address_components'][i]["short_name"])
            
            self.statusbar.showMessage("Getting weather...")
            for zippy in self.zipcodes:
                #self.full_weather_y.append(pywapi.get_weather_from_yahoo(zippy))
                self.full_weather_wc.append(pywapi.get_weather_from_weather_com(zippy))
            
            self.todayDate.setText('<p align=\"center\"><strong>%s, %s</strong></p>'%(self.full_weather_wc[0]["forecasts"][0]["day_of_week"], self.full_weather_wc[0]["forecasts"][0]["date"]))
            self.tomorrowDate.setText('<p align=\"center\"><strong>%s, %s</strong></p>'%(self.full_weather_wc[0]["forecasts"][1]["day_of_week"], self.full_weather_wc[0]["forecasts"][1]["date"]))
            self.twoDate.setText('<p align=\"center\"><strong>%s, %s</strong></p>'%(self.full_weather_wc[0]["forecasts"][2]["day_of_week"], self.full_weather_wc[0]["forecasts"][2]["date"]))
            self.threeDate.setText('<p align=\"center\"><strong>%s, %s</strong></p>'%(self.full_weather_wc[0]["forecasts"][3]["day_of_week"], self.full_weather_wc[0]["forecasts"][3]["date"]))
            self.fourDate.setText('<p align=\"center\"><strong>%s, %s</strong></p>'%(self.full_weather_wc[0]["forecasts"][4]["day_of_week"], self.full_weather_wc[0]["forecasts"][4]["date"]))
            
            curLbl = 0
            
            for cast in self.full_weather_wc:
                if "location" in cast:
                    self.dataLabels["today"].append(LocationFrame(self))
                    self.setLabels(self.dataLabels["today"][curLbl], 0, cast, self.zipcodes[curLbl])
                    self.todayLayout.addWidget(self.dataLabels["today"][curLbl])
                    
                    self.dataLabels["tomorrow"].append(LocationFrame(self))
                    self.setLabels(self.dataLabels["tomorrow"][curLbl], 1, cast, self.zipcodes[curLbl])
                    self.tomorrowLayout.addWidget(self.dataLabels["tomorrow"][curLbl])
                    
                    self.dataLabels["two"].append(LocationFrame(self))
                    self.setLabels(self.dataLabels["two"][curLbl], 2, cast, self.zipcodes[curLbl])
                    self.twoLayout.addWidget(self.dataLabels["two"][curLbl])
                    
                    self.dataLabels["three"].append(LocationFrame(self))
                    self.setLabels(self.dataLabels["three"][curLbl], 3, cast, self.zipcodes[curLbl])
                    self.threeLayout.addWidget(self.dataLabels["three"][curLbl])
                    
                    self.dataLabels["four"].append(LocationFrame(self))
                    self.setLabels(self.dataLabels["four"][curLbl], 4, cast, self.zipcodes[curLbl])
                    self.fourLayout.addWidget(self.dataLabels["four"][curLbl])
                else:
                    for x in self.dataLabels:
                        self.dataLabels[x].append(None)
                
                curLbl += 1
            
            self.statusbar.showMessage("Done.")
            self.reportTab.setEnabled(True)
        else:
            self.statusbar.showMessage("Please enter start and end locations.")
            self.messageBox("Please enter start and end locations.")
            
    def setLabels( self, ourObject, dayNum, cast, zipcode ):
        ourObject.locationLabel.setText('<p align=\"center\"><span style=\" font-weight:600;\"><a href="http://www.weather.com/weather/5day/l/%s:4:US">%s</a></span></p>'%(zipcode, cast["location"]["name"]))
        
        #Set AM Icon
        ourObject.amDes.setText('<p align=\"center\">%s</p>'%cast["forecasts"][dayNum]["day"]["text"])
        if cast["forecasts"][dayNum]["day"]["text"] in self.amIcons:
            amPath = self.amIcons[cast["forecasts"][dayNum]["day"]["text"]]
        else:
            amPath = self.amIcons["NA"]
            
        amIcon = QPixmap(amPath)
        ourObject.amLabel.setPixmap(amIcon)
        
        #Set PM Icon
        ourObject.pmDes.setText('<p align=\"center\">%s</p>'%cast["forecasts"][dayNum]["night"]["text"])
        if cast["forecasts"][dayNum]["night"]["text"] in self.pmIcons:
            pmPath = self.pmIcons[cast["forecasts"][dayNum]["night"]["text"]]
        else:
            pmPath = self.pmIcons["NA"]
        
        pmIcon = QPixmap(pmPath)
        ourObject.pmLabel.setPixmap(pmIcon)
        
        ourObject.tempHigh.setText('<p align=\"center\"><span style=\" font-weight:600;\">High:</span></p> <p align=\"center\">%s</p>'%(int(cast["forecasts"][dayNum]["high"])*1.8+32))
        ourObject.tempLow.setText('<p align=\"center\"><span style=\" font-weight:600;\">Low:</span></p> <p align=\"center\">%s</p>'%(int(cast["forecasts"][dayNum]["low"])*1.8+32))
        ourObject.amPercChance.setText('<p align=\"center\"><span style=\" font-weight:600;\">Chance of Percip:</span></p> <p align=\"center\">%s</p>'%(cast["forecasts"][dayNum]["day"]["chance_precip"]))
        ourObject.pmPercChance.setText('<p align=\"center\"><span style=\" font-weight:600;\">Chance of Percip:</span></p> <p align=\"center\">%s</p>'%(cast["forecasts"][dayNum]["night"]["chance_precip"]))
        
    
    def messageBox( self, ourMessage, ourTitle="Trek Message" ):
		msgBox = QMessageBox()
                msgBox.setWindowTitle(ourTitle)
		msgBox.setText(ourMessage)
		msgBox.exec_()
    
    def assignWidgets( self ):
        self.startButton.clicked.connect(self.workingMessage)
        self.startButton.clicked.connect(self.getWeather)

#Custom object to allow sorting by number and alpha
class TreeWidgetItem( QTreeWidgetItem ):
    def __init__(self, parent=None):
        QTreeWidgetItem.__init__(self, parent)

    def __lt__(self, otherItem):
        column = self.treeWidget().sortColumn()
        try:
            return float( self.text(column) ) > float( otherItem.text(column) )
        except ValueError:
            return self.text(column) > otherItem.text(column)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    ret = app.exec_()
