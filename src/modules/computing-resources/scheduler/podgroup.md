# PodGroup

PodGroup 是 T9k Scheduler 引入的另一项资源管理机制。PodGroup 关联一组协同工作的 Pod，这些 Pod 共同完成一项计算任务（例如模型分布式训练），因此应作为一个整体被分配资源。PodGroup 是平台支持 <a target="_blank" rel="noopener noreferrer" href="https://en.wikipedia.org/wiki/Coscheduling">coscheduling</a> 机制的关键组成部分，可以为并行计算提供更好的支持，包括避免死锁场景和提高资源利用率。

通常情况下，用户可以通过创建 [T9k Job](../jobs/index.md) 类型的工作负载来自动化地使用 PodGroup，但也可以手动创建 PodGroup。

## 规范

下面是一个基本的 PodGroup 示例：

```yaml
apiVersion: scheduler.tensorstack.dev/v1beta1
kind: PodGroup
metadata:
  name: chorus
  namespace: default
spec:
  minMember: 3
  priority: 50
  queue: default
```

在该例中：

* 最小 Pod 数量是 3（由 `spec.minMember` 字段指定）。
* PodGroup 的优先级是 50（由 `spec.priority` 字段指定）。
* PodGroup 通过 `default` 队列（由 `spec.queue` 字段指定）申请计算资源。

### 队列

`spec.queue` 字段定义 PodGroup 使用的队列，默认值是 `default`。

### 优先级

`spec.priority` 字段定义 PodGroup 的优先级，值类型是 `int`，范围是 [0,100]，默认值是 0，值越大表示优先级越高。在同一个队列中，优先级高的 PodGroup 会被优先分配资源。

### 运行需求

`spec.minMember` 字段定义 PodGroup 运行需要的最小 Pod 数量，可选的 `spec.roles` 字段定义 PodGroup 运行需要的角色以及相应角色的最小 Pod 数量。也就是说，只有以下条件同时被满足，调度器才会为 PodGroup 分配资源：

* PodGroup 中的 Pod 数量达到最小 Pod 数量。
* 如果设置了 `spec.roles` 字段，对于每一个角色，PodGroup 中扮演该角色的 Pod 数量都达到相应的最小 Pod 数量。

<aside class="note info">
<div class="title">Pod 的角色</div>

PodGroup 中 Pod 的角色（role）通过标签 `scheduler.tensorstack.dev/role` 指定。Job 控制器会自动为其创建的 Pod 设置 role。例如带有标签 `scheduler.tensorstack.dev/role: master` 的 Pod 的角色是 `master`，而带有标签 `scheduler.tensorstack.dev/role: worker` 的 Pod 的角色是 `worker`。

</aside>

在下面的示例中，PodGroup 的运行需求是：有 3 个 Pod，并且有 1 个角色为 master 的 Pod 和 1 个角色为 worker 的 Pod。

```yaml
...
spec:
  minMember: 3
  roles:
  - name: master
    minMember: 1
  - name: worker
    minMember: 1
```

## 状态

PodGroup 的状态记录在 `status` 字段中。

<aside class="note">
<div class="title">注意</div>

PodGroup 只负责关联一组 Pod，其 `status` 记录信息有限。如果用户想要知道 PodGroup 关联的工作负载整体的详细状态，一般需要通过 PodGroup 的父资源，例如 T9k Job 的 `status` 获取；特定 Pod 的状态则需要查看相应 Pod 的 `status`。

</aside>

`status.conditions` 字段记录了当前 PodGroup 的状态，包括以下两种类型：

* `GroupScheduled`：PodGroup 是否已经被分配过资源
* `SufficientGroupMember`：PodGroup 的 Pod 数量是否满足运行需求

`status.allocated` 字段记录了当前 PodGroup 被分配的资源量。

下列字段记录了当前 PodGroup 的处于不同阶段的 Pod 数量：

* `status.pending`：处于 Pending 阶段的 Pod 数量
* `status.running`：处于 Running 阶段的 Pod 数量
* `status.succeeded`：处于 Succeeded 阶段的 Pod 数量
* `status.failed`：处于 Failed 阶段的 Pod 数量
* `status.unknown`：处于 Unknown 阶段的 Pod 数量

下面是一个正常运行中的 PodGroup 的 `status` 字段的示例：

```yaml
...
status:
  allocated:
    cpu: 3
    memory: 600M
  conditions:
  - lastTransitionTime: "2023--17T13:54:02Z"
    reason: SufficientMemberPods
    status: "True"
    transitionID: 82ce5bf5-313d-4294-b44b-9b44ffd52213
    type: SufficientGroupMember
  - lastTransitionTime: "2023-12-17T13:48:16Z"
    message: Resources have been allocated to PodGroup
    reason: PodGroupScheduled
    status: "True"
    transitionID: c5a70cac-769c-44c4-a6ba-f4b1227cb135
    type: GroupScheduled
  running: 3
```

在该例中：

* condition `SufficientGroupMember` 为 `True`，表示 PodGroup 满足最小成员约束，可以被分配资源。
* condition `GroupScheduled` 为 `True`，表示整个 PodGroup 已经被分配资源。
* PodGroup 被分配了 3 个 CPU（核心）和 600MB 内存。
* 有 3 个 Pod 处于 running 状态。

## 下一步

* 学习如何[使用 PodGroup](../../../tasks/use-podgroup.md)
* PodGroup 的 [API Reference](../../../references/api-reference/scheduler.md#podgroup)
