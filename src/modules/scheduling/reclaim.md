# 资源回收

Notebook、TensorBoard 和 Explorer 一旦创建完毕，就一直占据所申请的 CPU、Mem、GPU 等计算资源，但是大部分时间用户并没有在真正使用这些资源。

TensorStack AI 平台为保证集群资源的充分利用，采取资源回收机制，自动检测并暂停空闲服务，回收其占用的资源。

## 原理

以 Notebook 为例，介绍资源回收的原理（TensorBoard 和 Explorer 同理）。

![structure](../../assets/modules/scheduling/reclaim.structure.drawio.svg)

如上图所示：

* 集群管理员提交“资源回收配置”给 Resource Keeper；
* Resource Keeper 根据配置判断一个项目是否需要启用资源回收机制，并监听启用该机制的项目中的 Notebook；
* 当 Notebook 空闲时间达到配置中规定的空闲时间上限，则 Resource Keeper 会暂停该资源。

### 空闲状态的检测

TensorStack AI 平台为所有服务添加一层 PEP Proxy，用来处理身份验证和授权。在资源回收过程中，也可以作为检查服务是否空闲的信息来源。

![pepproxy](../../assets/modules/scheduling/pepproxy.drawio.svg)

对 TensorBoard 和 Explorer，对应控制器会向 PEP Proxy 发送请求，检查其上一次请求的时间，如果给定时间内（比如 1 小时，由集群管理员配置）没有再次请求，则控制器判定其为空闲状态。

对 Jupyter Notebook 和自定义 Notebook，Notebook 控制器会先尝试向 Notebook 发送请求检查 Jupyter 内核状态，如果内核处于空闲或请求失败（可能 Notebook 使用的不是 Jupyter 内核，主要发生在自定义 Notebook 上），则继续向 PEP Proxy 发送请求，如果给定时间内（比如 1 小时，由集群管理员配置）没有请求，则控制器判定其为空闲状态。

对 RStudio Notebook，目前没有空闲状态的判定，控制器将其视为永远处于活跃状态。

## Jupyter Notebook 保持活跃状态

目前，Notebook 服务的空闲状态检测存在不完善的地方：在 Notebook 中只运行训练而没有其他操作时，无论 Jupyter Kernel 还是 PEP Proxy 都无法检测到这个活跃状态，导致错误地将其判断为空闲。

该情形下，您可以在 Notebook 中创建 `active.ipynb` 文件并执行以下代码块：
  
```python
import time

while True:
    time.sleep(60)
```

如果您的任务运行完成，您可以手动停止该代码块的执行，以恢复空闲资源回收的功能。
