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

在该例中：

* 最小运行数量是 2 个 Pod（由 `spec.minMember` 字段指定）。
* PodGroup 的优先级是 50（由 `spec.priority` 字段指定）。
* PodGroup 属于 `default` 队列（由 `spec.queue` 字段指定）。

## 所属队列

PodGroup 所属的队列通过字段 `spec.queue` 设置，默认值是 default。

## 优先级

PodGroup 的优先级通过 `spec.priority` 字段设置，值类型是 int，范围是 [0,100]，默认值是 0，数值越大表明优先级越高。在同一个队列中，优先级高的 PodGroup 会被优先分配资源（优先级相同时，先创建的先分配）。

## 最低运行需求

PodGroup 是一组协调工作以完成某项具体任务的 Pod 的集合，如果某个 Pod 未被创建会导致该项任务无法运行，那么其他 Pod 即使被分配资源也无法完成工作，反而导致计算资源的浪费。为了避免这种浪费资源的情况，PodGroup 需要配置最低运行需求，只有 Pod 数量满足了最低运行需求，调度器才会为 PodGroup 分配资源。

最低运行需求包括两部分——**最小运行数量**和**基于角色的最小运行数量**，两部分必须同时满足，调度器才会为 PodGroup 分配资源。

### 最小运行数量

最小运行数量通过字段 `spec.minMember` 设置，表明 PodGroup 的 Pod 数量（不包括失败的 Pod）达到最小运行数量时，调度器才会为 PodGroup 分配资源。

以 [创建 PodGroup](#创建-podgroup) 为例，示例中设置的最小运行数量是 2。

### 基于角色的最小运行数量

基于角色的最小运行数量通过字段 `spec.roles` 设置，`spec.roles` 是一个记录角色名称和该角色的最小运行数量的数组，PodGroup 的 Pod 通过标签来指定自己的角色。

下面是一个示例：

```yaml
spec:
  roles:
  - name: master
    minMember: 1
  - name: worker
    minMember: 3
```

在该示例中，PodGroup 包含两类角色 `master` 和 `worker`。当可运行的 `master` Pod 数量达到 1，`worker` Pod 数量达到 3 时，调度器才会为 PodGroup 分配资源，其中：

* 含有标签 `scheduler.tensorstack.dev/role: master` 的 Pod 的角色是 `master`
* 含有标签 `scheduler.tensorstack.dev/role: worker` 的 Pod 的角色是 `worker`

## 状态

PodGroup 的状态记录在 `status` 字段中。

`status.conditions` 字段记录了当前 PodGroup 的状态，包括下列 2 种类型：
* GroupScheduled: PodGroup 是否已经被分配过资源
* SufficientGroupMember: PodGroup 的 Pod 数量是否满足最小运行需求

`status.allocated` 字段记录了当前 PodGroup 使用的资源量。

PodGroup 的 Pod 的数量：

* `status.pending`：处于 Pending phase 的 Pod 数量
* `status.running`：处于 Running phase 的 Pod 数量
* `status.succeeded`：处于 Succeeded phase 的 Pod 数量
* `status.failed`：处于 Failed phase 的 Pod 数量
* `status.unknown`：处于 Unknown phase 的 Pod 数量

在下面的示例中：PodGroup 已经被分配过资源，PodGroup 的 Pod 数量为 0。有以下可能：

* PodGroup 的任务已经完成，完成后处于 Succeeded Phase 的 Pod 都被删除
* PodGroup 的任务未完成，Pod 在运行过程中未成功运行结束就被删除

<aside class="note">
<div class="title">注意</div>

PodGroup 只负责 coscheduling，并不记录任务的完成状态，想知道任务是否完成需要查看 T9k Job 或查看训练产出结果。

</aside>

```yaml
status:
  conditions:
  - lastTransitionTime: "2023-12-28T06:33:32Z"
    message: Insufficient members in PodGroup, waiting for more
    reason: InsufficientMemberPod
    status: "True"
    transitionID: 076fab41-181f-43fe-aa1c-b8b5c5832d2e
    type: SufficientGroupMember
  - lastTransitionTime: "2023-03-13T06:42:03Z"
    message: Resources have been allocated to PodGroup
    reason: PodGroupScheduled
    status: "True"
    transitionID: 67a49da4-eb59-4471-aeaf-ec69b7d49f75
    type: GroupScheduled
```

## 下一步

* 了解如何[使用 PodGroup](../../tasks/use-podgroup.md)
* PodGroup [API Reference](../../references/api-reference/scheduler.md#podgroup)
