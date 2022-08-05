from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

class PopupInfo(qtw.QWidget):

    submitted = qtc.pyqtSignal([str], [int, str])

    def __init__(self,msg):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())

        self.info_label = qtw.QLabel()
        self.info_label.setText(msg)
        self.submit = qtw.QPushButton('Ok', clicked=self.onSubmit)

        self.layout().addWidget(self.info_label)
        self.layout().addWidget(self.submit)

    def onSubmit(self):
        self.close()