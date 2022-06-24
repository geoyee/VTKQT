import sys
import typing
from PyQt5.QtWidgets import QMainWindow, QApplication
from ui import Ui_MainWindow
import SimpleITK as sitk
from seg import LITSSeg
import numpy as np
import random


def read_nii(path: str) -> typing.Tuple:
    ds = sitk.ReadImage(path)
    data = sitk.GetArrayFromImage(ds)
    # data = LITSSeg("weight/model.pdparams").pridect(data)  # seg
    return data, ds.GetSpacing()


def get_color_map(number: int) -> typing.List:
    colors = []
    for _ in range(number):
        colors.append([
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        ])
    return colors


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # load image
    # nii_path = "data/volume-21.nii"
    nii_path = "data/segmentation-21.nii"
    data, spcing = read_nii(nii_path)
    ui.vtkWidget.show_array(
        data, 
        spcing, 
        get_color_map(len(np.unique(data)))
    )
    sys.exit(app.exec_())
