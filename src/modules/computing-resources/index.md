# 计算资源

运行集群中的工作负载需要使用计算资源。TensorStack AI 平台提供了完善的计算资源分配和管理机制，支持使用 GPU、高速网卡等扩展设备资源，并提供资源使用监控、统计功能帮助用户随时获得工作负载的资源使用情况。

## 资源请求和限制

资源请求（requests）和限制（limits）是一种管理资源的重要机制，用于确保集群中的工作负载可以按照预期方式使用计算资源。资源请求（`spec.containers[].resources.requests` 字段）定义了工作负载的一个容器所需的最小资源量，资源限制（`spec.containers[].resources.limits` 字段）则定义了该容器所允许使用的最大资源量。集群的[调度器](./scheduler/index.md)根据这些参数进行资源分配，确保各个容器在共享主机资源时不会相互干扰或过度使用资源。

容器会被分配请求（requests）的资源量；如果容器所在的节点有足够的可用资源，容器可以使用超出请求（requests）的资源量，但不可使用超出限制（limits）的资源量。例如，当容器中的进程尝试使用超出限制的内存（memory）资源量时，系统会将尝试申请内存的进程终止，并触发内存不足（OOM）错误。

## 资源类型

资源类型包括 CPU、内存（memory）和扩展资源（extended resources）：

* CPU 的请求和限制以 Kubernetes CPU 为单位，1 个 Kubernetes CPU 等于 1 个物理 CPU 核心或 1 个虚拟核心，取决于节点是一台物理主机还是运行在某物理主机上的虚拟机。可以指定小数，例如 `0.1` 或 `100m`（`1m = 1/1000`），来使用核心的部分处理能力。
* 内存的请求和限制以字节为单位。可以使用科学计数法、定点后缀（k、M、G、T、P 和 E）和 2 的幂后缀（Ki、Mi、Gi、Ti、Pi 和 Ei），例如以下表达式代表大致相同的值：

    ```128974848 129e6 129M 128974848000m 123Mi```

* 除了 CPU 和内存之外，Kubernetes 还支持扩展资源。扩展资源由管理员颁布（advertise），然后用户可以像使用 CPU 和内存一样使用扩展资源。GPU 是最重要的扩展资源类型之一，请参阅 [GPU 使用](./gpu-usage.md)。

## 资源配额

资源配额是对于资源使用量的限制，旨在确保集群中有限的计算资源被公平、有效地分配和利用，以提高集群的整体效率。平台引入了以下两种资源配额：

1. 项目配额：一个项目中的工作负载可以使用的资源总量。
2. 队列配额：一个队列中的工作负载可以使用的资源总量。

当用户创建工作负载（如 Notebook、T9k Job 等）时，系统会检查项目和队列的资源使用量是否将超过各自的资源配额。如果超过配额，系统将拒绝该工作负载的创建。

请参阅[项目资源配额](../security/project.md#资源配额与配额模版)和[队列资源配额](./scheduler/queue.md#资源配额)。

## 调度

调度（scheduling）是指将 Pod 分配给集群中的节点的过程。当用户创建一个工作负载时，由[调度器](./scheduler/index.md)决定将工作负载的 Pod 放置在哪些节点上运行。调度器会根据一系列的策略和条件来选择最合适的节点，并确保集群中的工作负载被有效地分配和管理。

节点上的每种资源类型都有特定的容量，调度器会确保对于每种资源类型，所有调度到某个节点上的 Pod 的资源请求量之和都小于该节点的可用容量。只有当所有资源请求（包括 CPU、内存和任何扩展资源）都被某个节点满足时，Pod 才能被调度到这个节点上。当资源请求无法被任何节点满足时，Pod 将保持 PENDING 状态。

除了资源需求，调度器还会根据自身的[调度策略](./scheduler/scheduling-policy.md)，以及节点的约束、亲和性、健康状态等来选择节点。

关于调度的更多细节，请参阅[调度器](./scheduler/index.md)。

## 参考

* <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/zh-cn/docs/concepts/configuration/manage-resources-containers/">为 Pod 和容器管理资源</a>
* <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/zh-cn/docs/concepts/policy/resource-quotas/">资源配额</a>

## 下一步

* 进一步了解[调度器](./scheduler/index.md)
* 了解如何[使用 GPU](./gpu-usage.md)
* 了解自动化的[资源回收](./reclaim.md)机制
* 了解如何[监控工作负载的资源使用情况](./resources-monitoring.md)
