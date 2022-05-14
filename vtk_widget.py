import typing
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QSlider
import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class VTK_Widget(QWidget):
    def __init__(self, parent: typing.Optional["QWidget"]) -> None:
        super().__init__(parent)
        self.vlayer = QVBoxLayout(self)
        self.frame = QFrame(self)
        self.interactor = QVTKRenderWindowInteractor(self.frame)
        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Horizontal)
        self.surface_extractor = vtk.vtkContourFilter()
        self.slider.valueChanged.connect(self._slot)
        self.vlayer.addWidget(self.interactor)
        self.vlayer.addWidget(self.slider)

    def openVTK(self, path):
        self.ren = vtk.vtkRenderer()
        try:
            self.interactor.GetRenderWindow().AddRenderer(self.ren)
        except:
            return
        self.iren = self.interactor.GetRenderWindow().GetInteractor()
        try:
            self.reader = vtk.vtkDICOMImageReader()
        except:
            return
        self.reader.SetDataByteOrderToLittleEndian()
        self.reader.SetDirectoryName(path)
        self.reader.Update()
        self._surfaceMode()

    def _surfaceMode(self):
        self.surface_extractor.SetInputConnection(self.reader.GetOutputPort())
        self.surface_extractor.SetValue(0, -500)
        surface_normals = vtk.vtkPolyDataNormals()
        surface_normals.SetInputConnection(self.surface_extractor.GetOutputPort())
        surface_normals.SetFeatureAngle(60.0)
        surface_mapper = vtk.vtkPolyDataMapper()
        surface_mapper.SetInputConnection(surface_normals.GetOutputPort())
        surface_mapper.ScalarVisibilityOff()
        surface = vtk.vtkActor()
        surface.SetMapper(surface_mapper)
        camera = vtk.vtkCamera()
        camera.SetViewUp(0, 0, -1)
        camera.SetPosition(0, 1, 0)
        camera.SetFocalPoint(0, 0, 0)
        camera.ComputeViewPlaneNormal()
        self.ren.AddActor(surface)
        self.ren.SetActiveCamera(camera)
        self.ren.ResetCamera()
        self.ren.SetBackground(0, 0, 0)
        self.ren.ResetCameraClippingRange()
        self.frame.setLayout(self.vlayer)
        self.interactor.Initialize()
        self.interactor.GetRenderWindow().Render()
        self.interactor.Start()
        self.interactor.show()

    def _slot(self, val):
        self.surface_extractor.SetValue(0, val)
        self.interactor.update()
