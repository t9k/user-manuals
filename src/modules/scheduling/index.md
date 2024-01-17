# 计算资源

用户在向集群提交计算任务，使用计算资源时，需要遵循管理员设置的各种策略。

- [资源配额](#资源配额)：用户提交的工作负载需要满足集群的配额策略；
- [使用 t9k-scheduler](#t9k-scheduler)：可能需要通过特定的 scheduler 才能使用特定的资源。

## 资源配额

管理员可在 `Project` 和 `Queue` 分别设置资源（CPU、Memory、GPU、Storage 等）配额。

- 针对 `Project` 的配额限制单个 Project 里的各种计算资源使用上限；
- 设置在 `Queue` 上的配额则允许管理员设置特定容量的资源池供用户使用。

## t9k-scheduler

`t9k-scheduler` 调度器专为大规模分布式并行计算及异构资源集群设计，可以更加有效地管理 AI 集群的计算资源和计算任务。相比于 K8s 的默认调度器 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/#kube-scheduler">`kube-scheduler`</a>，`t9k-scheduler` 在对 AI 计算场景的支持方面进行了增强，并增加了额外的机制以对集群进行更加精细化管理。

### 适用场景

为并行计算性质的工作负载分配资源，当用户需要部署多个 Pod 协同工作以运行任务时，推荐使用 `t9k-scheduler`。

### Queue & PodGroup

`t9k-scheduler` 有两个重要的机制：

* [Queue](./queue.md)：`t9k-scheduler` 提供 queue 让用户工作负载申请集群资源，每一个使用 `t9k-scheduler` 的 Pod 都可指定一个 queue 为其分配资源。队列的创建/修改由集群管理员负责。
* [PodGroup](./podgroup.md)：PodGroup 是支持 <a target="_blank" rel="noopener noreferrer" href="https://en.wikipedia.org/wiki/Coscheduling"> coscheduling </a> 机制重要组成部分。它代表一组 Pod，并定义了这组 Pod 在资源方面的限制条件。当限制条件被满足时，PodGroup 中的 Pod 才会被分配计算资源。

### 使用

当用户创建 Pod 使用 t9k-scheduler 时，需要进行下列操作：

1. 将 Pod 使用的调度器名称设置为 t9k-scheduler；
2. 设置 Pod 所属的队列。

当用户创建一组 Pod 协同完成一项任务，并使用 t9k-scheduler，需要进行下列操作 （用户一般通过使用 T9k-Job 自动化地使用 PodGroup）：

1. 创建一个 PodGroup，并在 PodGroup 中设置所属的队列；
2. 将 Pod 使用的调度器名称设置为 t9k-scheduler；
3. 设置 Pod 属于步骤一创建的 PodGroup。

## 下一步

* 了解[资源配额](./quota.md)
* 了解[队列](./queue.md)
* 了解 [PodGroup](./podgroup.md)
* 了解动化的[资源回收](./reclaim.md)机制
* 学习[使用队列](../../tasks/use-queue.md)
* 学习[使用 PodGroup](../../tasks/use-podgroup.md)
