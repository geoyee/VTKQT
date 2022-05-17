import typing
import numpy as np
# from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame  # , QSlider
import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.util.vtkImageImportFromArray import vtkImageImportFromArray

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkDataSetAttributes
from vtkmodules.vtkFiltersCore import vtkMaskFields, vtkSmoothPolyDataFilter
from vtkmodules.vtkFiltersGeneral import vtkDiscreteFlyingEdges3D
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkFiltersCore import vtkDecimatePro


class VTK_Widget(QWidget):
    def __init__(self, parent: typing.Optional["QWidget"]) -> None:
        super().__init__(parent)
        self.vlayer = QVBoxLayout(self)
        self.frame = QFrame(self)
        self.interactor = QVTKRenderWindowInteractor(self.frame)
        # self.slider = QSlider(self)
        # self.slider.setOrientation(Qt.Horizontal)
        self.surface_extractor = vtk.vtkContourFilter()
        # self.slider.valueChanged.connect(self._slot)
        self.vlayer.addWidget(self.interactor)
        # self.vlayer.addWidget(self.slider)

    def showArray(self, data: np.ndarray, spacing: typing.Tuple) -> None:
        self.ren = vtk.vtkRenderer()
        try:
            self.interactor.GetRenderWindow().AddRenderer(self.ren)
        except:
            return
        self.iren = self.interactor.GetRenderWindow().GetInteractor()
        try:
            self.reader = vtkImageImportFromArray()
        except:
            return
        self.min = np.min(data)  # self.slider.setMaximum(np.min(data))
        self.max = np.max(data)  # self.slider.setMaximum(np.max(data))
        self.reader.SetArray(data)
        self.reader.SetDataSpacing(spacing)
        self.reader.SetDataOrigin((0, 0, 0))
        self.reader.Update()
        self._surfaceMode()

    def _surfaceMode(self) -> None:
        scalars_off = vtkMaskFields()
        geometry = vtkGeometryFilter()
        tail = self.reader.GetOutputPort()
        discrete_cubes = vtkDiscreteFlyingEdges3D()
        discrete_cubes.SetInputConnection(tail)
        tail = discrete_cubes.GetOutputPort()
        # discrete_cubes.GenerateValues(
        #     self.slider.maximum() - self.slider.minimum() + 1, self.slider.minimum(), self.slider.maximum())
        discrete_cubes.GenerateValues(self.max - self.min + 1, self.min, self.max)
        discrete_cubes.Update()
        decimate = vtkDecimatePro()
        decimate.SetInputConnection(tail)
        tail = decimate.GetOutputPort()
        decimate.SetTargetReduction(0.70)
        decimate.Update()
        smoother = vtkSmoothPolyDataFilter()
        smoother.SetInputConnection(decimate.GetOutputPort())
        tail = smoother.GetOutputPort()
        smoother.SetNumberOfIterations(20)
        smoother.SetBoundarySmoothing(0)
        smoother.SetFeatureEdgeSmoothing(0)
        smoother.SetFeatureAngle(120)
        smoother.Update()
        scalars_off.SetInputConnection(tail)
        tail = scalars_off.GetOutputPort()
        scalars_off.CopyAttributeOff(vtkMaskFields().POINT_DATA, vtkDataSetAttributes().SCALARS)
        scalars_off.CopyAttributeOff(vtkMaskFields().CELL_DATA, vtkDataSetAttributes().SCALARS)
        geometry.SetInputConnection(scalars_off.GetOutputPort())
        tail = geometry.GetOutputPort()
        self.surface_extractor.SetInputConnection(self.reader.GetOutputPort())
        self.surface_extractor.SetValue(0, 1)
        # self.slider.setValue(1)
        colors = vtkNamedColors()
        surface_normals = vtk.vtkPolyDataNormals()
        surface_normals.SetInputConnection(self.surface_extractor.GetOutputPort())
        surface_normals.SetFeatureAngle(60.0)
        surface_mapper = vtk.vtkPolyDataMapper()
        surface_mapper.SetInputConnection(tail)
        surface_mapper.ScalarVisibilityOff()
        # surface_mapper.SetScalarRange(self.slider.minimum(), self.slider.maximum())
        surface_mapper.SetScalarRange(self.min, self.max)
        surface = vtk.vtkActor()
        surface.SetMapper(surface_mapper)
        surface.GetProperty().SetColor(colors.GetColor3d("Green"))
        camera = vtk.vtkCamera()
        camera.SetPosition(42.301174, 939.893457, -124.005030)
        camera.SetFocalPoint(224.697134, 221.301653, 146.823706)
        camera.SetViewUp(0.262286, -0.281321, -0.923073)
        camera.SetDistance(789.297581)
        camera.SetClippingRange(168.744328, 1509.660206)
        camera.ComputeViewPlaneNormal()
        light = vtk.vtkLight()
        light.SetFocalPoint(surface.GetPosition())
        light.SetColor(colors.GetColor3d("White"))
        light.SetLightTypeToHeadlight()
        self.ren.AddActor(surface)
        self.ren.SetActiveCamera(camera)
        self.ren.AddLight(light)
        self.ren.ResetCamera()
        self.ren.SetBackground(colors.GetColor3d("Black"))
        self.ren.SetAutomaticLightCreation(1)
        self.ren.SetLightFollowCamera(1)
        self.ren.SetAmbient(1, 1, 1)
        self.ren.ResetCameraClippingRange()
        self.interactor.Initialize()
        self.interactor.GetRenderWindow().Render()
        self.interactor.Start()
        self.interactor.show()

    # def _slot(self, val: int) -> None:
    #     self.surface_extractor.SetValue(0, val)
    #     self.interactor.update()
