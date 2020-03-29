from PyQt5 import QtCore, QtWidgets, uic
import sys
import requests, json 

class Ui(QtWidgets.QMainWindow):
    
    data = resp = ""

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('/home/roy/Desktop/work/covid.ui', self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.show()
        self.resp = requests.get("https://api.covid19api.com/summary")
        self.data = json.loads(self.resp.text)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.country_selected)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(int(self.refresh.currentText()) * 60000)
        self.country.currentTextChanged.connect(self.country_selected)
        self.refresh.currentTextChanged.connect(self.update_timer)
        self.country_selected()

    def country_selected(self):

        for keys in self.data["Countries"]:
            if keys["Country"] == self.country.currentText():
                self.tot_deaths.display(int(keys["TotalDeaths"]))
                self.new_deaths.display(int(keys["NewDeaths"]))
                self.new_cases.display(int(keys["NewConfirmed"]))
                self.recovered.display(int(keys["TotalRecovered"]))
                self.all_cases.display(int(keys["TotalConfirmed"]))
    
    def update_timer(self):
        self.timer.setInterval(int(self.refresh.currentText())*60000)

    def update_data(self):
        self.resp = requests.get("https://api.covid19api.com/summary")
        self.data = json.loads(self.resp.text)

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()