# 创建和使用 PodGroup

本教程演示如何创建和使用 [PodGroup](../modules/computing-resources/scheduler/podgroup.md)。

## 手动创建 PodGroup

用户可以手动创建 PodGroup 以关联一组进行协同工作的 Pod，步骤如下：

1. （使用 YAML 配置文件）创建一个 PodGroup。
2. 创建若干个 Pod，设置 `scheduler.tensorstack.dev/group-name` 标签为步骤 1 中创建的 PodGroup 的名称。
3. Pod 的数量（和角色）达到 PodGroup 的运行需求后，T9k Scheduler 开始调度 PodGroup。

<aside class="note">
<div class="title">注意</div>

Pod 所属的 PodGroup 无法被修改，只能删除 Pod 再重新创建并为其指定新的 PodGroup。

</aside>

### 示例：基本场景

首先创建一个 PodGroup，设置其最小数量、队列和优先级：

```yaml
apiVersion: scheduler.tensorstack.dev/v1beta1
kind: PodGroup
metadata:
  name: podgroup-test
spec:
  minMember: 2
  queue: default
  priority: 50
```

然后创建两个 Pod 并指定所属的 PodGroup，`scheduler.tensorstack.dev/group-name: podgroup-test` 标签表示它们属于 PodGroup `podgroup-test`：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx1
  labels:
    scheduler.tensorstack.dev/group-name: podgroup-test
spec:
  schedulerName: t9k-scheduler
  containers:
  - image: nginx
    name: nginx
    resources:
      requests:
        cpu: 1
        memory: 200Mi
--
apiVersion: v1
kind: Pod
metadata:
  name: nginx2
  labels:
    scheduler.tensorstack.dev/group-name: podgroup-test
spec:
  schedulerName: t9k-scheduler
  containers:
  - image: nginx
    name: nginx
    resources:
      requests:
        cpu: 1
        memory: 200Mi
```

此时 PodGroup 的运行需求得到满足，从而开始被调度。

### 示例：设置角色最小数量

本示例创建有两种角色的 PodGroup。

首先创建一个 PodGroup：

```yaml
apiVersion: scheduler.tensorstack.dev/v1beta1
kind: PodGroup
metadata:
  name: role-test
spec:
  roles:
  - name: master
    minMember: 1
  - name: worker
    minMember: 1
  minMember: 3
  queue: default
  priority: 50
```

该 PodGroup 的运行需求如下：

* 有 3 个 Pod。
* 有 1 个角色名称是 master 的 Pod。
* 有 1 个角色名称是 worker 的 Pod。

然后创建 3 个 Pod 并指定所属的 PodGroup，`scheduler.tensorstack.dev/role: <role-name>` 标签表示它们自己的角色名称：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: master
  labels:
    scheduler.tensorstack.dev/group-name: role-test
    scheduler.tensorstack.dev/role: master
spec:
  schedulerName: t9k-scheduler
  containers:
  - name: nginx
    image: nginx

--

apiVersion: v1
kind: Pod
metadata:
  name: worker
  labels:
    scheduler.tensorstack.dev/group-name: role-test
    scheduler.tensorstack.dev/role: worker
spec:
  schedulerName: t9k-scheduler
  containers:
  - name: nginx
    image: nginx

--

apiVersion: v1
kind: Pod
metadata:
  name: worker1
  labels:
    scheduler.tensorstack.dev/group-name: role-test
    scheduler.tensorstack.dev/role: worker
spec:
  schedulerName: t9k-scheduler
  containers:
  - name: nginx
    image: nginx
```

此时 PodGroup 的运行需求得到满足，从而开始被调度。

## T9k Job 自动创建 PodGroup

T9k Job 包括 TensorFlowTrainingJob、PyTorchTrainingJob、XGBoostTrainingJob、GenericJob、MPIJob、ColossalAIJob、DeepSpeedJob 和 BeamJob，这些 Job 中都有相同的 `spec.scheduler` 字段。

创建这些 Job 时，用户可以设置 `spec.scheduler.t9kScheduler` 字段以使用 T9k Scheduler 并指定队列。在这种情况下，Job 会自动创建一个 PodGroup 以及若干属于该 PodGroup 的 Pod 来执行计算任务，PodGroup 会继承 Job 的队列和优先级。

### 示例：基本场景

创建一个使用 T9k Scheduler 的 GenericJob，设置其队列和优先级：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: GenericJob
metadata:
 name: job-test
spec:
 scheduler:
   t9kScheduler:
     queue: default
     priority: 10
 replicaSpecs:
   - type: ps
     replicas: 1
     ...
   - type: worker
     replicas: 4
     ...
```

Job 会自动创建一个 PodGroup，其 `spec.priority` 和 `spec.queue` 字段的值继承自 Job 的 `spec.scheduler.t9kScheduler` 字段，`spec.minMember` 字段的值则为 Job 的总副本（replica）数：

```yaml
apiVersion: scheduler.tensorstack.dev/v1beta1
kind: PodGroup
metadata:
  name: job-test
  ownerReferences: [...]
spec:
  minMember: 5
  priority: 10
  queue: default
```

随后，Job 会自动创建 5 个副本的 Pod，并为它们设置 `scheduler.tensorstack.dev/group-name: job-test` 标签以指定它们属于这个 PodGroup：

```yaml
# worker-2 的 Pod
apiVersion: v1
kind: Pod
metadata:
  labels:
    genericjob: job-test
    genericjob-replica: job-test-worker-2
    scheduler.tensorstack.dev/group-name: job-test
    scheduler.tensorstack.dev/queue: default
    tensorstack.dev/component: genericjob
    tensorstack.dev/component-type: user
  name: job-test-worker-0
  namespace: demo
  ownerReferences: [...]
```

### 示例：启用弹性训练

弹性训练要求训练规模可以动态调整，所以对 PodGroup 的设置也有所不同。

T9k Job 中，PyTorchTrainingJob 和 DeepSpeedJob 支持弹性训练，它们具有相同的 `spec.elastic` 字段，以此启动弹性训练。

创建一个使用 T9k Scheduler 并启用弹性训练的 GenericJob：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: PyTorchTrainingJob
metadata:
  name: elastic-test
spec:
  scheduler:
    t9kScheduler:
      queue: default
      priority: 10
  elastic:
    enabled: true
    minReplicas: 4
    maxReplicas: 10
    expectedReplicas: 7
  ...
```

其中：

* `spec.elastic.enabled` 字段设为 `true` 表示启用弹性训练。
* 训练规模（即副本数量）的伸缩范围为 [4,10]，期望值为 7。

PyTorchTrainingJob 会自动创建一个 PodGroup，其 `spec.minMember` 字段的值继承自 PyTorchTrainingJob 的 `spec.elastic.minReplicas` 字段，即为弹性训练的最小副本数。

```yaml
apiVersion: scheduler.tensorstack.dev/v1beta1
kind: PodGroup
metadata:
  name: elastic-test
  ownerReferences: [...]
spec:
  minMember: 4
  priority: 10
  queue: default
```
