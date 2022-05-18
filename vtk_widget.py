import typing
import numpy as np
import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.util.vtkImageImportFromArray import vtkImageImportFromArray
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame


class VTKWidget(QWidget):
    def __init__(self, parent: typing.Optional["QWidget"]) -> None:
        super().__init__(parent)
        self.vlayer = QVBoxLayout(self)
        self.renderer = vtk.vtkRenderer()
        self.frame = QFrame(self)
        self.interactor = QVTKRenderWindowInteractor(self.frame)
        self.interactor.GetRenderWindow().AddRenderer(self.renderer)
        self.vlayer.addWidget(self.interactor)

    def showArray(self, data: np.ndarray, spacing: typing.Tuple) -> None:
        self.min = 1
        self.max = np.max(data)
        self.reader = vtkImageImportFromArray()
        self.reader.SetArray(data)
        self.reader.SetDataSpacing(spacing)
        self.reader.SetDataOrigin((0, 0, 0))
        self.reader.Update()
        self._changeShowMode()

    def _changeShowMode(self) -> None:
        scalars_off = vtk.vtkMaskFields()
        geometry = vtk.vtkGeometryFilter()
        tail = self.reader.GetOutputPort()
        # to mesh
        try:
            discrete_cubes = vtk.vtkDiscreteFlyingEdges3D()
        except AttributeError:
            discrete_cubes = vtk.vtkDiscreteMarchingCubes()
        discrete_cubes.SetInputConnection(tail)
        tail = discrete_cubes.GetOutputPort()
        discrete_cubes.GenerateValues(self.max - self.min + 1, self.min, self.max)
        discrete_cubes.Update()
        # simplify mesh
        decimate = vtk.vtkDecimatePro()
        decimate.SetInputConnection(tail)
        tail = decimate.GetOutputPort()
        decimate.SetTargetReduction(0.70)
        decimate.Update()
        # smooth the mesh
        smoother = vtk.vtkSmoothPolyDataFilter()
        smoother.SetInputConnection(decimate.GetOutputPort())
        tail = smoother.GetOutputPort()
        smoother.SetNumberOfIterations(20)
        smoother.SetBoundarySmoothing(0)
        smoother.SetFeatureEdgeSmoothing(0)
        smoother.SetFeatureAngle(120)
        smoother.Update()
        # strip the scalars from the output
        scalars_off.SetInputConnection(tail)
        tail = scalars_off.GetOutputPort()
        scalars_off.CopyAttributeOff(vtk.vtkMaskFields().POINT_DATA, vtk.vtkDataSetAttributes().SCALARS)
        scalars_off.CopyAttributeOff(vtk.vtkMaskFields().CELL_DATA, vtk.vtkDataSetAttributes().SCALARS)
        geometry.SetInputConnection(scalars_off.GetOutputPort())
        tail = geometry.GetOutputPort()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(tail)
        mapper.SetScalarRange(self.min, self.max)
        mapper.SetScalarModeToUseCellData()
        mapper.SetColorModeToMapScalars()
        colors = vtk.vtkNamedColors()
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(colors.GetColor3d("Green"))
        style = vtk.vtkInteractorStyleTrackballCamera()
        self.interactor.SetInteractorStyle(style)
        self.renderer.AddActor(actor)
        self.renderer.SetBackground(colors.GetColor3d("Black"))
        self.renderer.SetAutomaticLightCreation(1)
        self.renderer.SetLightFollowCamera(1)
        self.renderer.SetAmbient(1, 1, 1)
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(42.301174, 939.893457, -124.005030)
        camera.SetFocalPoint(224.697134, 221.301653, 146.823706)
        camera.SetViewUp(0.262286, -0.281321, -0.923073)
        camera.SetDistance(789.297581)
        camera.SetClippingRange(168.744328, 1509.660206)
        light = vtk.vtkLight()
        light.SetFocalPoint(actor.GetPosition())
        light.SetColor(colors.GetColor3d("White"))
        light.SetLightTypeToHeadlight()
        self.renderer.AddLight(light)
        self.interactor.Start()
        self.interactor.show()
