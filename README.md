# VTKQT
基于VTK的自定义QWidget，可以方便插入PyQt的Layout中，可以将C×H×W的np.ndarray（分割结果）进行可视化显示。

## 使用

```python
from vtk_widget import VTK_Widget

...
self.vtkWidget = VTK_Widget(self.centralwidget)
self.vtkWidget.setObjectName("vtkWidget")
self.verticalLayout.addWidget(self.vtkWidget)
...
```

## 参考

1.  [VTK_Medical_Visualization_PyQt5](https://github.com/its-kamel/VTK_Medical_Visualization_PyQt5)

