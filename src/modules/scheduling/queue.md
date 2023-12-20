# 队列

## 概述

使用 T9k Scheduler 进行作业调度的任务都必须有一个所属的队列（Queue），监控管理员可以通过队列配置来管控队列中任务的作业调度，例如将不同类型的任务放到不同的队列中，设置队列可以使用的资源权限，设置可以使用队列的用户权限等。

## 创建队列

下面是一个基本的队列示例：

```yaml
apiVersion: scheduler.tensorstack.dev/v1beta1
kind: Queue
metadata:
  name: default
  namespace: t9k-system
spec:
  closed: false
  priority: 1
  requests:
    cpu: 4
    memory: 200Gi
  preemptible: true
```

在该示例中：

* 队列所位于的命名空间是 `t9k-system`。
* 队列处于开启状态，队列中的任务可以被分配资源。
* 队列的优先级是 `1`。
* 队列的资源配额是 `{cpu: 4, memory: 200Gi}`，队列中任务占据的资源总量不可以超过资源配额。
* 队列处于可以抢占状态，队列中运行的任务可以被高优先级的队列抢占资源。

## 命名空间

队列的命名空间必须和**部署 T9k Scheduler 的命名空间**一致。在上述基本示例中，T9k Scheduler 部署在 `t9k-system` 中，所以队列的命名空间也必须设置为 `t9k-system`。

## 队列开关

队列的开关是通过字段 `spec.closed` 来设置的：

* `true`：队列处于关闭状态，调度器停止向队列分配资源，但是队列中已经存在的 PodGroup 可以被分配新资源。
* `false`：队列处于开启状态。

## 优先级

队列的优先级是通过字段 `spec.priority` 来指定的，调度器会优先为高优先级队列分配资源。当两个队列的 `spec.priority` 相同时，调度器会通过[公平排序机制](../policy/fair-share.md)判断任务调度的顺序。

当集群中包含生产级别任务和测试任务时，不应该把两种类型任务放在同一队列中，并且生产级别任务的队列优先级应该高于测试任务的队列。

## 资源配额

资源配额用于限制队列可以占据的资源上限，通过字段 `spec.requests` 设置。

## 资源抢占

当集群资源不足时，优先级高的队列可以抢占优先级低的队列的资源，但是被设置不能被抢占资源的队列不会被抢占资源。通过 `spec.preemptible` 可以设置队列的抢占开关：

* `true`：队列可以被抢占资源，队列中运行的任务可以被高优先级的队列抢占资源。
* `false`：队列不可以被抢占资源。

## 资源限制

资源限制通过集群节点的标签筛选来限制队列可以使用的节点，由字段 `spec.nodeSelector`（字段详解请参考 [LabelSelector:octicons-link-external-16:](https://v1-22.docs.kubernetes.io/docs/reference/kubernetes-api/common-definitions/label-selector/){target=_blank}）设置，未设置时队列可以使用集群中所有节点的资源。

下面是一个设置资源限制的示例：

```yaml
spec:
  nodeSelector:
    matchLabels:
      kubernetes.io/arch: amd64
    matchExpressions:
    - key: kubernetes.io/hostname
      operator: In
      values:
      - host1
      - host2
```

在该示例中，队列可以使用的节点必须具有以下标签：

* `kubernetes.io/arch: amd64`
* `kubernetes.io/hostname: host1` 或 `kubernetes.io/hostname: host2`

## 访问权限

访问权限通过命名空间的标签筛选来限制可以使用该队列的命名空间，由字段 `spec.namespaceSelector`（字段详解请参考 [LabelSelector:octicons-link-external-16:](https://v1-22.docs.kubernetes.io/docs/reference/kubernetes-api/common-definitions/label-selector/){target=_blank}）设置，未设置时任何命名空间都可以使用该队列。

下面是一个设置访问权限的示例：

```yaml
spec:
  namespaceSelector:
    matchLabels:
      tensorstack.dev/role: master
```

在该示例中，可以使用该队列的命名空间必须具有标签 `tensorstack.dev/role: master`。

## 队列状态

队列状态记录在字段 `status` 中，下面的队列状态示例包含了所有的状态字段：

```yaml
status:
  allocated:
    cpu: "2"
    memory: "419430400"
  closedTimeStamp: "2022-03-07T05:27:58Z"
  unknown: 0
  pending: 0
  running: 1
  finished: 0
```

在该示例中，状态字段包括：

* 队列占据的资源数量：`status.allocated` 记录队列已经使用的资源数量，示例中队列使用了 2 个 CPU 和 419,430,400 字节（419 MB）的内存。
* 队列的关闭时间：当队列处于关闭状态时，`status.closedTimeStamp` 记录队列被关闭的时刻。
* 队列中的 PodGroup 状态数量：`status.unknown`、`status.pending`、`status.running`、`status.finished` 分别记录队列中处于 **unknown**、**pending**、**running**、**finished** 状态的 PodGroup 的数量。

## 调度策略

与队列相关的调度策略如下：

* [资源抢占](../policy/preemption-of-queue-resource.md)
* [公平排序](../policy/fair-share.md)
