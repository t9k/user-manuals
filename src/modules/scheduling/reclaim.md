# 资源回收

[Notebook](../building/notebook.md)、[TensorBoard](../building/tensorboard.md) 和 [Explorer](../storage/explorer.md) 一旦创建完毕，就一直占据所申请的 CPU、内存、GPU 等计算资源，但是大部分时间用户并没有在真正使用这些资源。

TensorStack AI 平台为保证集群资源的充分利用，采取资源回收机制，自动检测并暂停空闲的 Notebook、TensorBoard 和 Explorer 服务，回收其占用的资源。

## 原理

以 Notebook 为例，介绍资源回收的原理（TensorBoard、 Explorer 或者其他工作负载同理）。

![structure](../../assets/modules/scheduling/reclaim.structure.drawio.svg)

如上图所示：

* 集群管理员设置 “资源回收配置” 策略；
* 根据配置，Resource Keeper 监听启用回收功能的项目（Project 2）中的 Notebook 状态；
* 当 Notebook 空闲时间达到配置中规定的阈值，则 Resource Keeper 对该资源实施暂停操作，以释放资源。

### 状态检测

很多在 TensorStack AI 平台上运行的服务，使用 PEP Proxy 来处理身份验证和授权。由于其 proxy 所有客户端请求，这个 PEP Proxy 也可以作为检查服务是否空闲的信息来源。

![pepproxy](../../assets/modules/scheduling/pepproxy.drawio.svg)

对于 TensorBoard 和 Explorer，对应控制器会向 PEP Proxy 发送请求，检查其上一次请求的时间，如果给定时间内（比如 1 小时，由集群管理员配置）没有再次请求，则控制器判定其为空闲状态。

Jupyter Notebook 本身的 server 就提供了状态查询功能。因此，对于 Notebook 类型的工作负载，Notebook 的控制器会先尝试向 Notebook server 发送请求检查空闲状态。如果处于空闲或请求失败（可能 Notebook 使用的不是 Jupyter 内核，主要发生在自定义 Notebook 上），则继续向 PEP Proxy 发送请求，查询 PEP Proxy 观测到的服务使用情况：例如，如果 1 小时内（由管理员配置）没有请求，则控制器判定其为空闲状态。

对于 RStudio Notebook，目前没有空闲状态的判定，控制器将其视为永远处于活跃状态。

## Jupyter Notebook 保持活跃状态

如果由于某种特定原因，用户需要使特定的 Notebook 不被此回收机制影响，用户可以在 Notebook 中创建 `active.ipynb` 文件并执行以下代码块：
  
```python
import time

while True:
    time.sleep(60)
```

此代码使得 Notebook 保持活跃状态，而又不实际耗费额外计算资源。

如果需要恢复空闲资源回收的功能，用户可手动停止该代码块的执行。

## 下一步

- [创建 Notebook](../../tasks/create-notebook.md)
- [使用 Notebook](../../tasks/use-notebook.md)
