# VTKQT

基于VTK的自定义QWidget，可以方便插入PyQt的Layout中，可以将C×H×W的np.ndarray（分割结果）进行可视化显示。

![~E6_HXST08`` CWQEWKOK_S](https://user-images.githubusercontent.com/71769312/175547709-57d27bc2-35dd-4e63-bda4-3a51c9e759db.png)

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

1. [VTK_Medical_Visualization_PyQt5](https://github.com/its-kamel/VTK_Medical_Visualization_PyQt5)
2. [python 使用vtk库生成三维模型_TWINKLING?的博客-CSDN博客_python快速生成3d模型](https://blog.csdn.net/weixin_46579211/article/details/118279231)
