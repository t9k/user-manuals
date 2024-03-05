# 小技巧

本教程汇总了一些实用的小技巧，可以帮助你更好地使用平台。

## 让 Notebook 不被资源回收

如果想要让 Notebook 不被[资源回收](../modules/scheduling/reclaim.md)，可以在该 Notebook 中[创建一个 Jupyter Notebook](./use-notebook.md#使用-jupyter-notebook)，并运行以下代码：

```python
# To keep the kernel active
import time

while True:
    time.sleep(60)
```

上述代码使 Notebook 保持活跃状态，而又不占用额外的计算资源。如要恢复对该 Notebook 的资源回收，只需停止上述代码的运行即可。
