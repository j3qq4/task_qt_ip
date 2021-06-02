from PySide2 import QtCore, QtWidgets, QtWebEngineWidgets
from PySide2.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit
from PySide2.QtGui import QIcon, QFont
import sys
import os
import requests


class IPTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        central_widgets = QtWidgets.QWidget()
        self.setCentralWidget(central_widgets)

        # Top UI
        top_widgets = QtWidgets.QWidget()

        self.setWindowTitle('IP Tracker')

        self.input_ip = QLineEdit(top_widgets)
        self.input_ip.setGeometry(10, 10, 180, 30)
        self.input_ip.setFont(QFont("Times", 12))

        button = QPushButton("", top_widgets)
        button.setGeometry(188, 9, 32, 32)
        button.setIcon(QIcon("icon.png"))
        button.clicked.connect(self.ip_tracker)
        top_widgets.setMaximumHeight(40)

        # Bottom
        self.map = QtWebEngineWidgets.QWebEngineView(self)
        file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "map.html", )
        self.map.setUrl(QtCore.QUrl.fromLocalFile(file))
        self.map.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        bottom_widgets = QtWidgets.QWidget()
        bottom_layout = QtWidgets.QHBoxLayout()
        bottom_layout.addWidget(self.map)
        bottom_widgets.setLayout(bottom_layout)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)

        splitter.addWidget(top_widgets)
        splitter.addWidget(bottom_widgets)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(splitter)

        central_widgets.setLayout(main_layout)

        self.setMinimumSize(300, 300)
        self.statusBar().showMessage('Ready')

    @QtCore.Slot()
    def ip_tracker(self):
        text = self.input_ip.text()
        if text != "":
            res = requests.get("http://ipwhois.app/json/" + str(text)).json()
            if res.get("success") is False:
                self.statusBar().showMessage('Invalid IP')
            else:
                self.statusBar().showMessage(f'{res["country"]}, {res["city"]}, '
                                             f'latitude: {res["latitude"]}, longitude: {res["longitude"]}')
                self.map.page().runJavaScript(f"initMap({res['latitude']}, {res['longitude']});")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = IPTracker()
    main_window.show()
    sys.exit(app.exec_())
