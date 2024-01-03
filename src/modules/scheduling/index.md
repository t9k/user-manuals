# 调度

T9k Scheduler 是 K8s 调度器，负责将 Pod 调度到一个合适的节点上来运行。相比于 K8s 的默认调度器 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/#kube-scheduler">kube-scheduler</a>，T9k Scheduler 增强了对 AI 计算场景的支持，并增加了额外的机制方便对集群进行更加精细化管理等。

## 适用场景

T9k Scheduler 适用于为批处理任务分配资源。当您需要部署多个 Pod 协同工作以运行任务时，推荐使用 T9k Scheduler。

## 队列 & PodGroup

T9k Scheduler 有两个重要的概念：
* [队列](./queue.md)：T9k Scheduler 通过队列来管理集群资源，队列的创建/修改由集群管理员负责。每一个使用 T9k Scheduler 的 Pod 都需要指定一个队列，通过队列来为其分配资源。
* [PodGroup](./podgroup.md)：PodGroup 代表了一组 Pod，定义了这组 Pod 可以被分配资源的限制条件。只有限制条件被满足了，PodGroup 中的 Pod 才会被分配集群资源进行工作。

## 使用 T9k Scheduler

当您创建一个 Pod 使用 T9k Scheduler 时，需要进行下列操作：

1. 将 Pod 使用的调度器名称设置为 t9k-scheduler；
2. 设置 Pod 所属的队列。

当您创建一组 Pod 协同完成一项任务，并使用 T9k Scheduler，需要进行下列操作：

1. 创建一个 PodGroup，并在 PodGroup 中设置所属的队列；
2. 将 Pod 使用的调度器名称设置为 t9k-scheduler；
3. 设置 Pod 属于步骤一创建的 PodGroup。

## 下一步

* 了解[队列](./queue.md)
* 了解 [PodGroup](./podgroup.md)
* 了解如何[使用队列](../../tasks/use-queue.md)
* 了解如何[使用 PodGroup](../../tasks/use-podgroup.md)
