from PyQt5.QtCore import QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from vtk_widget import VTKWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QMainWindow) -> None:
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 500)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.openButton = QPushButton(self.centralwidget)
        self.openButton.setObjectName("openButton")
        self.openButton.setText("打开文件")
        self.verticalLayout.addWidget(self.openButton)
        self.vtkWidget = VTKWidget(self.centralwidget)
        self.vtkWidget.setObjectName("vtkWidget")
        self.verticalLayout.addWidget(self.vtkWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow: QMainWindow) -> None:
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
