# 计算资源

您在 TensorStack AI 平台创建工作负载时，需要设置工作负载所需的计算资源数量，最常见的可设定资源是 CPU 和内存大小，此外还有其他类型的资源。当工作负载被设置了计算资源数量之后，调度器根据该信息决定将 Pod 调度到哪个节点上运行。

## 请求和限制

[TODO] 说明设置 resources 的 requests 和 limits 的意义

## 资源类型

[TODO] 说明内置资源类型 cpu、memory，和扩展资源。更多见 [GPU 使用](./use-gpu.md)

## 调度器

[TODO] 说明调度器基本工作原理，简介 T9k Scheduler 和 Kube Scheduler。更多见 [T9k Scheduler](./t9k-scheduler.md)

## [资源配额](./quota.md)

[TODO] 简介资源配额

## [资源回收](./reclaim.md)

[TODO] 简介资源回收

## [资源使用监控](./monitoring.md)

[TODO] 简介资源使用监控

