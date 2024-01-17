# PodGroup

## 概述

PodGroup 关联一组协同工作的 Pod，它们共同完成一项计算任务（例如分布式并行模型训练），因此需要作为一个整体来分配资源。通常情况下，用户可以通过创建 [T9k Job](../jobs/index.md) 类的工作负载来间接使用 PodGroup，而不需要直接创建 PodGroup。

PodGroup 是 T9k 支持 <a target="_blank" rel="noopener noreferrer" href="https://en.wikipedia.org/wiki/Coscheduling"> coscheduling </a> 机制的关键组成部分，可以为并行计算提供更好的支持，包括避免死锁场景和提高资源利用率。

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

* 最少运行数量是 3 个成员 Pod（由 `spec.minMember` 字段指定）。
* PodGroup 的优先级是 50（由 `spec.priority` 字段指定）。
* PodGroup 使用 `default` 队列（由 `spec.queue` 字段指定）申请资源。

### 队列

`spec.queue` 设置 PodGroup 欲使用的资源队列，默认值是 `default。`

### 优先级

`spec.priority` 字段设置 PodGroup 的优先级 ，值类型是 `int`，范围是 [0,100]，默认值是 0，数值越大表明优先级越高。在同一个队列中，优先级高的 PodGroup 会被优先分配资源。

### 最少成员限制

成员数量限制包括两部分，必须同时满足，调度器才会为 PodGroup 分配资源：
- 最少数量（minMember）；
- 角色最少数量（role minMember），但非必须字段。当未填写时，则自动满足。

#### 最少数量

`spec.minMember` 设置 PodGroup 的最小运行数量，表明 PodGroup 的 Pod 数量（不包括失败的 Pod）达到最小运行数量时，调度器才会为 PodGroup 分配资源。

本文开头的示例中设置的最小运行数量是 3，但未设置角色最少数量。

#### 角色最少数量

基于角色（role）的最小运行数量通过字段 `spec.roles` 的子字段设置。
- `spec.roles` 是一个记录角色名称和该角色的最小运行数量的数组；
- PodGroup 的 Pod 通过标签来指定自己的角色。

下面是一个示例：

```yaml
spec:
  roles:
  - name: master
    minMember: 1
  - name: worker
    minMember: 3
```

在该示例中，PodGroup 包含两类角色 `master` 和 `worker`。当可运行的 `master` Pod 数量达到 1，`worker` Pod 数量达到 3 时，调度器才会为 PodGroup 分配资源。

<aside class="note info">
<div class="title"> 指定 Pod 的 Role </div>

PodGroup 中 Pod 的角色（role）通过标签 `scheduler.tensorstack.dev/role` 指定。Job 控制器会自动为其创建的 Pod 设置 role。

例如：

* 贴有标签 `scheduler.tensorstack.dev/role: master` 的 Pod 的角色是 `master`
* 贴有标签 `scheduler.tensorstack.dev/role: worker` 的 Pod 的角色是 `worker`

</aside>

## 状态

PodGroup 的状态记录在 `status` 字段中。

<aside class="note">
<div class="title">注意</div>

PodGroup 只负责关联一组 Pod，其 `status` 记录信息有限。如果用户想知道 PodGroup 关联的工作负载整体的详细状态一般需要通过 PodGroup 的父资源，例如 T9k Job 的 `status` 获取；单独 Pod 的状态则须查看此 Pod 的 `status`。

</aside>

`status.conditions` 字段记录了当前 PodGroup 的状态，包括下列 2 种类型：
* `GroupScheduled`: PodGroup 是否已经被分配过资源
* `SufficientGroupMember`: PodGroup 的 Pod 数量是否满足最小运行需求

`status.allocated` 字段记录了当前 PodGroup 使用的资源量。

PodGroup 的 Pod 的数量：

* `status.pending`：处于 Pending phase 的 Pod 数量
* `status.running`：处于 Running phase 的 Pod 数量
* `status.succeeded`：处于 Succeeded phase 的 Pod 数量
* `status.failed`：处于 Failed phase 的 Pod 数量
* `status.unknown`：处于 Unknown phase 的 Pod 数量

### 示例

下面的 YAML 片段展示了一个正常运行中的 PodGroup 的 `status` 字段：

- `allocated`：podgroup 被分配的资源总和；
- `running`: 3 个 pod 处于 running 状态；
- condition `SufficientGroupMember` 为 `True`，表示 PodGroup 满足最小成员约束，可以被分配资源；
- condition `GroupScheduled` 为 `True`，表示整个 PodGroup 已经被分配资源；


```yaml
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

## 下一步

* 了解如何[使用 PodGroup](../../tasks/use-podgroup.md)
* PodGroup [API Reference](../../references/api-reference/scheduler.md#podgroup)
