# PodGroup

## 概述

PodGroup 是一组 Pod 的集合，这一组 Pod 协调工作完成一项具体任务。通常情况下，您不会直接创建 PodGroup，而是通过创建 [T9k Job](../jobs/index.md) 来间接使用 PodGroup。

## 创建 PodGroup

下面是一个基本的 PodGroup 示例：

```yaml
apiVersion: scheduler.tensorstack.dev/v1beta1
kind: PodGroup
metadata:
  name: test
  namespace: default
spec:
  minMember: 2
  priority: 50
  queue: default
```

在该示例中：

* 最小运行需求是至少有 2 个 Pod 可以成功运行。
* PodGroup 的优先级是 50。
* 所属队列是 `default`。

## 所属队列

通过字段 `spec.queue` 设置 PodGroup 所属的队列，如果没有设置，则默认为 `default` 队列。

## 成员 Pod

Pod 通过标签指定所属的 PodGroup，例如标签 `scheduler.tensorstack.dev/group-name: test` 表明 Pod 所属的 PodGroup 是 `test`。

## 优先级

PodGroup 的优先级是通过 `spec.priority` 指定的，在一个队列内，调度器会根据 PodGroup 的优先级依次分配资源（优先级相同时，先创建的先分配）。

## 最低运行需求

PodGroup 是一组协调工作以完成某项具体任务的 Pod 的集合，如果某个 Pod 无法运行会导致该项任务无法完成，那么其他 Pod 即使被分配资源也无法完成工作，反而导致计算资源的浪费。所以为了避免这种浪费资源的情况，PodGroup 需要配置最低运行需求。

最低运行需求包括两部分——**最小运行数量**和**基于角色的最小运行数量**，两部分必须同时满足，调度器才会为 PodGroup 分配资源。

### 最小运行数量

最小运行数量通过字段 `spec.minMember` 设置，表明 PodGroup 中可以运行的 Pod （或成功运行结束的 Pod）达到该数量时，调度器才会为 PodGroup 分配资源。在示例[创建 PodGroup](#创建-podgroup) 中，设置的最小运行数量是 2。

### 基于角色的最小运行数量

基于角色的最小运行数量通过字段 `spec.roles` 设置，`spec.roles` 是一个记录角色名称和该角色的最小运行数量的数组，PodGroup 中的 Pod 通过标签来指定自己的角色。下面是一个示例：

```yaml
spec:
  roles:
  - name: master
    minMember: 1
  - name: worker
    minMember: 3
```

在该示例中，PodGroup 包含两类角色 `master` 和 `worker` 的 Pod。当可运行的 `master` Pod 数量达到 1，`worker` Pod 数量达到 3 时，调度器才会为 PodGroup 分配资源，其中：

* 含有标签 `scheduler.tensorstack.dev/role: master` 的 Pod 的角色是 `master`。
* 含有标签 `scheduler.tensorstack.dev/role: worker` 的 Pod 的角色是 `worker`。

## 任务结束

PodGroup 代表的任务被完成后，应该将字段 `spec.finished` 设置为 `true` 表明任务结束，然后调度器会停止为该 PodGroup 分配资源。如果使用 [T9k Job](../jobs/index.md) 来部署任务，无需手动修改 PodGroup 的任务结束字段，T9k Job 会在任务完成后自动将 PodGroup 标记为任务结束。

下面是一个任务结束的 PodGroup 的示例：

```yaml
spec:
  finished: true
```

## 状态

PodGroup 状态记录在字段 `status` 中，下面是一个包括了所有状态字段的示例：

```yaml
status:
  phase: Running
  conditions:
  - lastTransitionTime: "2022-03-07T10:11:34Z"
    message: pods are ready to be scheduled
    reason: ready
    status: "True"
    transitionID: 910f8e62-3e69-4f1b-a39e-c1b84739e573
    type: Scheduled
  running: 2
  succeeded: 1
  failed: 0
```

### 运行状态

`status.phase` 记录 PodGroup 的运行状态。PodGroup 具有以下几种运行状态：

* `Pending`：PodGroup 处于等待状态，例如集群资源不足，PodGroup 未满足最小运行需求等。
* `Running`：PodGroup 处于运行状态。
* `Unknown`：PodGroup 处于未知状态，例如 PodGroup 中有运行的 Pod，但是 PodGroup 未满足最小运行需求（可能是误删 Pod 导致的）。
* `Finished`：PodGroup 处于结束状态，任务成功完成。

### 状态详情

`status.conditions` 记录 PodGroup 的状态详情。

### Pod 状态数量

状态字段 `status.running`、`status.succeeded`、`status.failed` 分别记录 PodGroup 中处于 **running**、**succeeded**、**failed** 状态的 Pod 的数量。

## 下一步

* 查看 [PodGroup API 详情](../../../../reference/tensorstack-resources/scheduling-api/podgroup.md)（坏链）
