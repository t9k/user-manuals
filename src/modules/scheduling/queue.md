# 队列

## 概述

T9k Scheduler 通过队列来管理集群资源，使用 T9k Scheduler 进行作业调度的任务都必须有一个所属的队列。集群管理员负责创建队列、设置队列属性，队列有下列属性。

## 使用权限

队列的使用权限用于控制哪些项目可以使用这个队列，您可以在 T9k 产品前端查看到您所在的项目有权使用哪些队列。

更详细地，队列的使用权限通过两种方式进行设置：
* 管理员直接设置有权使用队列的用户/用户组
* 管理员设置队列的 `spec.namespaceSelector`（类型是 [labelSelector](https://github.com/kubernetes/apimachinery/blob/v0.29.0/pkg/apis/meta/v1/types.go#L1213)） 字段

当项目满足下列任一条件时，用户有权在项目下创建使用某个队列的工作负载：
* 队列设置了 `spec.namespaceSelector`，并且项目对应的 namespace 的标签符合这个 namespaceSelector
* 项目的用户有权使用这个队列

## 节点权限

队列的节点权限用于限制队列有权限使用哪些集群节点，T9k Scheduler 只会将队列内的工作负载分配到有权使用的节点上。

队列的 `spec.nodeSelector` （类型是 [labelSelector](https://github.com/kubernetes/apimachinery/blob/v0.29.0/pkg/apis/meta/v1/types.go#L1213)）字段用于设置队列的节点权限：
* 字段未设置时，队列可以使用集群内所有的节点
* 字段设置后，队列可以使用节点标签满足 nodeSelector 的节点。

在下面的节点权限示例中：说明队列可以使用节点标签包含 `topology.kubernetes.io/zone: peking` 或 `topology.kubernetes.io/zone: tianjin` 的节点。
```yaml
spec:
  nodeSelector:
    matchExpressions:
    - key: topology.kubernetes.io/zone
      operator: In
      values:
      - peking
      - tianjin
```

## 资源配额

队列的资源配额用于限制队列可以使用的资源上限，如果您创建的工作负载会导致队列超出资源配额限制，那么系统会拒绝您的创建行为。

队列的 `spec.quota` 字段定义队列的资源配额，队列的 `status.allocated` 字段表明队列已经使用的资源量。

在下面的示例中：如果想创建使用该队列的工作负载，工作负载声明的 cpu 资源量不能超过 2。
```yaml
spec:
  quota:
    requests:
      cpu: 40
status:
  allocated:
    cpu: "38"
```


## 优先级

队列的 `spec.priority` 字段定义队列的优先级，值类型是 int，范围是 [0,100]，数值越大代表队列的优先级越高。队列的优先级会影响下列事情：
* 优先级较高的队列会被优先分配资源
* 如果 T9k Scheduler 开启了资源抢占行为，优先级较高的队列有权抢占低优先级队列使用的资源。

## 是否可被抢占资源

队列的 `spec.preemptible` 字段定义队列是否可以被其他队列抢占资源，字段值类型是 bool：
* 字段被设置为 false 时，队列无法被抢占资源
* 字段未设置或设置为 true 时，队列可以被抢占资源

## 开启/关闭

队列的 `spec.closed` 字段定义队列是否处于关闭状态，当队列被关闭了，用户无法创建使用该队列的工作负载。字段值类型是 bool：
* 字段未设置或被设置为 false 时，队列处于开启状态
* 字段被设置为 true 时，队列处于关闭状态

## 最大运行时长

最大运行时长会限制队列中 Pod 的运行时长，如果 Pod 的存在时长（存在时长=当前时间 - Pod 创建时间）超过最大运行时长，Pods 会被删除。

队列的 `spec.maxDuration` 字段设置了队列的最大运行时长：
* 值类型是 string，并且需要满足正则表达式 `^(0|(([0-9]+)y)?(([0-9]+)w)?(([0-9]+)d)?(([0-9]+)h)?(([0-9]+)m)?(([0-9]+)s)?(([0-9]+)ms)?)$`
* 支持的时间单位：y, w（周）, d, h, m, s, ms
* 示例："3w",  "2h45m"。
* 未设置时，队列不受最大运行时长约束。

## 资源尺寸

资源尺寸会限制队列中工作负载声明的资源量上限，当您创建超过资源尺寸的工作负载时，创建行为会被系统拒绝。

队列的 `spec.resourceShapeProfile` 字段设置了队列使用的资源尺寸模版，模型对应的资源尺寸详情存储在 ConfigMap t9k-system/resource-shapes 中。您可以通过 T9k 产品前端查看队列的资源尺寸。

## 下一步

* 了解如何[使用队列](../../tasks/use-queue.md)
* 队列 [API Reference](../../references/api-reference/scheduler.md#queue)
