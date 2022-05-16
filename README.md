# VTKQT
基于VTK的自定义QWidget，可以方便插入PyQt的Layout中，可以将C×H×W的np.ndarray（分割结果）进行可视化显示。

![G$L)5TE8AB6X{ MH}U$49UF](https://user-images.githubusercontent.com/71769312/168525961-24bf02c5-01a7-4a47-a06c-c01612577a60.png)

在[这里](https://next.a-boat.cn:2021/s/n4j6eSN6zgWJSCb)下载测试模型和数据。

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

