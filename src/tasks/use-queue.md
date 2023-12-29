# 使用队列

## 概述

队列是 T9k 平台中资源管理的机制，用于补充 K8s 原生平台在 scheduling 方面的不足。管理员可以为队列设定使用权限，资源来源的集群节点，资源配额，最大运行时长等属性，以精细化管理集群。

用户在创建使用调度器 T9k Scheduler 的工作负载时，需为工作负载指定一个队列。

## 为工作负载指定队列

根据工作负载的种类，指定队列的方式如下。

### v1/Pod

创建 Pod 时，有两种指定所属队列的方式：
* 直接指定队列：此类 Pod 不属于任何 PodGroup。
* 通过 PodGroup 间接指定队列：此类 Pod 属于所指定的 PodGroup。

#### 直接指定队列

Pod 通过标签来表明他属于哪一个队列，标签的 key 是 `scheduler.tensorstack.dev/queue`。

<aside class="note">
<div class="title">注意</div>

Pod 一旦指定了所属的队列，就无法修改其所属的队列，如果想要修改 Pod 所属的队列，需要删除 Pod 再重新创建并指定新的队列。

</aside>

在下面的示例中，Pod 指定了队列 demo：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test1
  labels:
    scheduler.tensorstack.dev/queue: demo
spec:
  schedulerName: t9k-scheduler
  containers:
  - image: nginx:latest
    name: test
    resources:
      requests:
        cpu: 1
        memory: 200Mi
```

#### 通过 PodGroup 指定队列

如果 Pod 属于某个 PodGroup，那么 PodGroup 指定的队列就是这个 Pod 所属的队列。

Pod 如何指定 PodGroup 请参考 [使用 PodGroup](./use-podgroup.md)

### T9k Jobs

T9k Job 包括 TensorFlowTrainingJob、PyTorchTrainingJob、XGBoostTrainingJob、GenericJob、MPIJob、ColossalAIJob、DeepSpeedJob 和 BeamJob，这些 Job 中都有相同的 `spec.scheduler` 字段。

创建 T9k Job 时，用户可以通过设置 `spec.scheduler` 字段来表明使用 T9k scheduler，并指定 Job 使用哪个队列。

在下面的示例中：`spec.scheduler.t9kScheduler.queue` 字段表明 Job 使用的队列是 demo，GenericJob 控制器会自动创建使用队列 demo 的 PodGroup 和 Pod。

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: GenericJob
metadata:
 name: job-sample
spec:
 scheduler:
   t9kScheduler:
     queue: demo
     priority: 10
 replicaSpecs:
   - type: worker
     replicas: 4
     ...
   - type: ps
     replicas: 1
     ...
```


### T9k PodGroup

创建 PodGroup 时，通过 `spec.queue` 字段来表明 PodGroup 所使用的队列。

在下面的示例中，PodGroup 表明自己使用的队列是 demo：
```yaml
apiVersion: scheduler.tensorstack.dev/v1beta1
kind: PodGroup
metadata:
 name: test
spec:
 minMember: 2
 queue: demo
 priority: 50
```

### batch/v1/Job

与 [v1/Pod](#v1pod) 类似，创建 batch/v1 Job 使用队列时，需要通过设置 Pod 的标签来表明 Pod 所使用的队列。有两种设置 Pod 标签的方法：
* 直接指定队列：为 Pod 设置标签 `scheduler.tensorstack.dev/queue:<queue-name> ` 表明 Pod 所使用的队列。
* 通过 PodGroup 间接指定队列：为 Pod 设置标签 `scheduler.tensorstack.dev/group-name:<group-name>` 表明 Pod 所属的 PodGroup，PodGroup 使用的队列就是 Pod 使用的队列。

在下面的示例中，Job 通过为 Pod 设置标签 `scheduler.tensorstack.dev/queue:demo` 来表明使用队列 demo。

```yaml
apiVersion: batch/v1
kind: Job
metadata:
 name: test
spec:
 parallelism: 2
 template:
   metadata:
     labels:
       scheduler.tensorstack.dev/queue: demo
   spec:
     schedulerName: t9k-scheduler
     containers:
       - name: create
         image: nginx:latest
         command:
         - sleep
         - 10s
         resources:
           requests:
             cpu: 1
             memory: 100Mi
     restartPolicy: Never
```
