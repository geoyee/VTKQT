import sys
import typing
from PyQt5.QtWidgets import QMainWindow, QApplication
from ui import Ui_MainWindow
import SimpleITK as sitk


def readNII(path: str) -> typing.Dict:
    ds = sitk.ReadImage(path)
    data = sitk.GetArrayFromImage(ds)
    # == TODO: segmentation ==
    # data = segmentation(data)
    # ======
    spcing = ds.GetSpacing()
    return data, spcing


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # load image
    nii_path = "data/volume-0.nii"
    data, spcing = readNII(nii_path)
    ui.vtkWidget.showArray(data, spcing)
    sys.exit(app.exec_())
