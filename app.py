import os
import random
import typing
import numpy as np
import SimpleITK as sitk
from seg import LITSSeg
from PyQt5 import QtWidgets
from ui import Ui_MainWindow


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super(App, self).__init__()
        self.setupUi(self)
        self.vtkWidget.init()
        self.openButton.clicked.connect(self._open_file)

    def _open_file(self) -> None:
        self.vtkWidget.init()
        filters = "医疗影像(*.nii)"
        nii_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "选择想显示的影像",
            os.getcwd(),
            filters,
            options=QtWidgets.QFileDialog.ReadOnly,
        )
        data, spcing = self._read_nii(nii_path)
        self.vtkWidget.show_array(
            data, 
            spcing, 
            self._get_color_map(len(np.unique(data)))
        )

    def _read_nii(self, path: str, use_seg: bool = False) -> typing.Tuple:
        ds = sitk.ReadImage(path)
        data = sitk.GetArrayFromImage(ds)
        if use_seg:
            data = LITSSeg("weight/model.pdparams").pridect(data)  # seg
        return data, ds.GetSpacing()


    def _get_color_map(self, number: int) -> typing.List:
        colors = []
        for _ in range(number):
            colors.append([
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            ])
        return colors
