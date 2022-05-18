import sys
import typing
from PyQt5.QtWidgets import QMainWindow, QApplication
from ui import Ui_MainWindow
import SimpleITK as sitk
from seg import LITSSeg


def readNII(path: str) -> typing.Tuple:
    ds = sitk.ReadImage(path)
    data = sitk.GetArrayFromImage(ds)
    # data = LITSSeg("weight/model.pdparams").pridect(data)  # seg
    return data, ds.GetSpacing()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # load image
    # nii_path = "data/volume-21.nii"
    nii_path = "data/segmentation-21.nii"
    data, spcing = readNII(nii_path)
    ui.vtkWidget.showArray(data, spcing)
    sys.exit(app.exec_())
