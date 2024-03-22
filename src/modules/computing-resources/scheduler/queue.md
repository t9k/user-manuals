# 队列

队列（Queue）是 T9k Scheduler 引入的一项资源管理机制。如果用户在创建工作负载时使用 T9k Scheduler 调度，就需要通过一个队列申请计算资源。

## 队列设置

队列由管理员进行创建和设置，但作为用户也需要了解下面的这些设置。

### 使用权限

队列的使用权限用于控制哪些用户、组和项目可以使用这个队列。队列的使用权限通过两种方式进行设置：

1. 管理员直接设置拥有队列使用权限的用户和组。
2. 管理员设置队列的 `spec.namespaceSelector`（类型是 <a target="_blank" rel="noopener noreferrer" href="https://github.com/kubernetes/apimachinery/blob/v0.29.0/pkg/apis/meta/v1/types.go#L1213">labelSelector</a>）字段。

当满足下列任一条件时，用户有权限在特定项目下使用特定队列创建工作负载：

* 用户拥有该队列的使用权限。
* 该队列设置了 `spec.namespaceSelector` 字段，并且该项目对应的 namespace 的标签匹配这个 `namespaceSelector`。

### 节点限制

队列的节点限制用于指定队列可用的集群工作节点（worker node），T9k Scheduler 只会将队列内的工作负载分配到这些特定的节点上。

`spec.nodeSelector`（类型是 <a target="_blank" rel="noopener noreferrer" href="https://github.com/kubernetes/apimachinery/blob/v0.29.0/pkg/apis/meta/v1/types.go#L1213">labelSelector</a>）字段用于设置队列的节点限制：

* 字段未被设置时，队列可以使用集群内所有的节点。
* 字段被设置时，队列可以使用节点标签匹配 nodeSelector 的节点。

在下面的示例中，队列可以使用节点标签包含 `topology.kubernetes.io/zone: peking` 或 `topology.kubernetes.io/zone: tianjin` 的节点。

```yaml
...
spec:
  nodeSelector:
    matchExpressions:
    - key: topology.kubernetes.io/zone
      operator: In
      values:
      - peking
      - tianjin
```

### 资源配额

队列的[资源配额](../index.md#资源配额)用于限制队列可以分配的资源量。如果用户创建的工作负载（例如 Notebook、T9k Job 等）会导致队列的资源使用量超出资源配额，那么系统会拒绝该工作负载的创建。

`spec.quota` 字段定义队列的资源配额，`status.allocated` 字段表示队列已经分配的资源量。

在下面的示例中，队列的 CPU 资源配额为 40，即队列中所有工作负载的 CPU 请求量（`requests`）之和不能超过 40，而当前已经分配了 38。如果此时用户使用该队列创建一个请求 `{cpu: 4}` 资源的 Notebook，则该 Notebook 会被拒绝创建。

```yaml
...
spec:
  quota:
    requests:
      cpu: 40
status:
  allocated:
    cpu: "38"
```

### 优先级

`spec.priority` 字段定义队列的优先级，值类型是 int，范围是 [0,100]，数值越大代表队列的优先级越高。队列的优先级会影响下列事件：

* 优先级较高的队列会被优先分配资源。
* 如果 T9k Scheduler 开启了资源抢占，则优先级较高的队列可以抢占低优先级队列使用的资源。

### 是否可被抢占资源

`spec.preemptible` 字段定义队列是否可以被其他队列抢占资源，字段值类型是 `bool`：

* `true`：队列可以被抢占资源。
* `false`：队列不能被抢占资源。

### 开启/关闭

`spec.closed` 字段定义队列是否处于关闭状态。如果队列处于关闭状态，用户就不能创建使用该队列的工作负载。字段值类型是 `bool`：

* 字段未被设置或被设置为 `false` 时，队列处于开启状态。
* 字段被设置为 `true` 时，队列处于关闭状态。

### 最大运行时长

最大运行时长会限制队列中的 Pod 的运行时长，如果 Pod 的存在时长（存在时长=当前时间 - 创建时间）超过最大运行时长，Pod 会被删除。

`spec.maxDuration` 字段定义队列的最大运行时长：

* 值类型是 string，并且需要匹配正则表达式 `^(0|(([0-9]+)y)?(([0-9]+)w)?(([0-9]+)d)?(([0-9]+)h)?(([0-9]+)m)?(([0-9]+)s)?(([0-9]+)ms)?)$`。
* 支持的时间单位：y, w（周）, d, h, m, s, ms。
* 示例："3w"，"2h45m"。
* 未设置时，队列中的 Pod 不受最大运行时长约束。

### 资源尺寸

资源尺寸（resource shape）会限制队列中的工作负载的资源请求量。当用户创建资源请求量超过资源尺寸的工作负载时，系统会拒绝该工作负载的创建。

`spec.resourceShapeProfile` 字段定义队列使用的资源尺寸模板，模板对应的资源尺寸详情存储在 ConfigMap `t9k-system/resource-shapes` 中。用户可以通过集群管理控制台查看队列的资源尺寸设置。

## 下一步

* 学习如何[使用队列](../../../tasks/use-queue.md)
* 队列的 [API Reference](../../../references/api-reference/scheduler.md#queue)
