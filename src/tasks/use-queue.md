# 为工作负载指定队列

本教程演示如何为不同类型的工作负载指定[队列](../modules/computing-resources/scheduler/queue.md)。

## Pod

对于 Pod 有两种指定队列的方法：直接指定队列和通过 PodGroup 间接指定队列。

### 直接指定队列

Pod 的 `scheduler.tensorstack.dev/queue` 标签标识其属于哪一个队列。创建 Pod 时，用户可以设置 `spec.schedulerName` 字段为 `t9k-scheduler`，并设置该标签以直接指定队列。

<aside class="note">
<div class="title">注意</div>

Pod 所属的队列无法被修改，只能删除 Pod 再重新创建并为其指定新的队列。

</aside>

在下面的示例中，Pod 被指定了队列 `default`：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-test
  labels:
    scheduler.tensorstack.dev/queue: default
spec:
  schedulerName: t9k-scheduler
  containers:
  - name: nginx
    image: nginx
```

### 通过 PodGroup 间接指定队列

Pod 的 `scheduler.tensorstack.dev/group-name` 标签标识其属于哪一个 PodGroup。创建 Pod 时，用户可以设置该标签以指定所属的 PodGroup，这样 Pod 会使用该 PodGroup 的队列。

## PodGroup

[手动创建 PodGroup](./use-podgroup.md#手动创建-podgroup) 时，需要设置 `spec.queue` 字段以指定队列。属于 PodGroup 的所有 Pod 都会使用该队列。

在下面的示例中，PodGroup 被指定了队列 `default`：

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

## T9k Job

T9k Job 包括 TensorFlowTrainingJob、PyTorchTrainingJob、XGBoostTrainingJob、GenericJob、MPIJob、ColossalAIJob、DeepSpeedJob 和 BeamJob，这些 T9k Job 中都有相同的 `spec.scheduler` 字段。

创建这些 T9k Job 时，用户可以设置 `spec.scheduler.t9kScheduler` 字段以使用 T9k Scheduler 并指定队列。T9k Job 创建的所有 Pod 都会使用该队列。

在下面的示例中，GenericJob 被指定了队列 `default`：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: GenericJob
metadata:
 name: t9k-job-test
spec:
 scheduler:
   t9kScheduler:
     queue: default
     priority: 10
 replicaSpecs:
   - type: worker
     replicas: 4
     ...
   - type: ps
     replicas: 1
     ...
```

## batch/v1 Job

创建 batch/v1 Job 时，用户可以参照 [Pod](#pod) 设置 Pod 模板（`spec.template` 字段），从而为 batch/v1 Job 的所有 Pod 指定队列。

在下面的示例中，batch/v1 Job 的 Pod 被指定了队列 `default`：

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: batch-v1-job-test
spec:
  parallelism: 2
  template:
    metadata:
      labels:
        scheduler.tensorstack.dev/queue: default
    spec:
      schedulerName: t9k-scheduler
      containers:
        - name: nginx
          image: nginx
          command: ["sleep", "10"]
```
