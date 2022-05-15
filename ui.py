from PyQt5.QtCore import QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout
from vtk_widget import VTK_Widget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 500)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.vtkWidget = VTK_Widget(self.centralwidget)
        self.vtkWidget.setObjectName("vtkWidget")
        self.verticalLayout.addWidget(self.vtkWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
        self.vtkWidget.openVTK("data/Ankle")  # 加载图像

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
