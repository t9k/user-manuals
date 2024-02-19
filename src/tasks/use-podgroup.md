# 使用 PodGroup

## 概念

PodGroup 是 namespaced-scoped 资源对象，代表一组协同工作的 Pod。PodGroup spec 中定义了 coscheduling 和其他相关的配置信息，调度器 T9k Scheduler 会根据这些信息为 Pod 分配资源。

## 使用 PodGroup


根据工作负载的种类，创建并使用 PodGroup 的方式如下。

### Pod

一般仅需要通过 Job 控制器自动化地实现对 PodGroup 的使用。工作负载控制器的编程者，或者需手工设定 pod 的 PodGroup，可参考本节内容。

用户创建一组使用调度器 T9k Scheduler 进行协同工作的 Pod 时，需要：
1. 先在相同的 namespace 中创建一个 PodGroup
2. 为 Pod 添加标签 `scheduler.tensorstack.dev/group-name: <PodGroup-name>` 来表明 Pod 属于步骤一创建的 PodGroup

<aside class="note">
<div class="title">注意</div>

Pod 一旦指定了所属的 PodGroup，就无法修改其所属的 PodGroup，如果想要修改 Pod 所属的 PodGroup，需要删除 Pod 再重新创建并指定新的 PodGroup。

</aside>

#### 示例1 - 基本场景

首先需要创建一个 PodGroup：
```yaml
apiVersion: scheduler.tensorstack.dev/v1beta1
kind: PodGroup
metadata:
  name: dance
spec:
  minMember: 2
  queue: default
  priority: 50
```

然后创建 2 个 Pod 并指定 PodGroup，Pod 通过标签 `scheduler.tensorstack.dev/group-name: dance` 表明他们属于 PodGroup dance。
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test1
  labels:
    scheduler.tensorstack.dev/group-name: dance
spec:
  schedulerName: t9k-scheduler
  containers:
  - image: nginx:latest
    name: test
    resources:
      requests:
        cpu: 1
        memory: 200Mi
--
apiVersion: v1
kind: Pod
metadata:
  name: test2
  labels:
    scheduler.tensorstack.dev/group-name: dance
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

#### 示例2 - 使用 role

本示例展示有 2 个 role 并设置了 role minMember 的 PodGroup 使用场景。

创建 PodGroup

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
说明：上面这个 PodGroup 的最小运行需求如下，这些需求都被满足了，调度器才会为 PodGroup 中的 Pod 分配资源：
* PodGroup 的 Pod 数量需要达到 3
* 角色名称是 master 的 Pod 数量需要达到 1
* 角色名称是 worker 的 Pod 数量需要达到 1

创建 Pod：

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
  - image: nginx:latest
    name: test
    resources:
      requests:
        cpu: 100m
        memory: 200Mi
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
  - image: nginx:latest
    name: test
    resources:
      requests:
        cpu: 100m
        memory: 200Mi
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
  - image: nginx:latest
    name: test
    resources:
      requests:
        cpu: 100m
        memory: 200Mi
```

Pod 通过标签 `scheduler.tensorstack.dev/role: <role-name>` 来表明自己的角色名称。 

### T9k Jobs

T9k Job 包括 TensorFlowTrainingJob、PyTorchTrainingJob、XGBoostTrainingJob、GenericJob、MPIJob、ColossalAIJob、DeepSpeedJob 和 BeamJob，这些 Job 中都有相同的 `spec.scheduler` 字段。

创建 T9k Job 时，用户可以通过设置 `spec.scheduler` 字段来表明使用 T9k scheduler，并指定 Job 使用哪个队列，然后控制器会自动地创建 PodGroup、并创建 Pod 使用这个 PodGroup。

#### 基本示例

本示例适用于未启用弹性训练的 Job。

以下面这个 GenericJob 为例：
```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: GenericJob
metadata:
 name: job-sample
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

控制器在监测到上述 CRD 后，会创建一个 PodGroup:

```yaml
apiVersion: scheduler.tensorstack.dev/v1beta1
kind: PodGroup
metadata:
  name: job-sample
  ownerReferences: [...]
spec:
  minMember: 5
  priority: 10
  queue: default
```

其中，priority 和 queue 字段参考 job 的 `spec.scheduler.t9kScheduler` 中的信息设置，minMember 即为 job 所有副本的总数。

随后，控制器会在创建副本的 Pod 时，为 Pod 设置标签 `scheduler.tensorstack.dev/group-name: job-sample` 来使用上述 PodGroup。

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    genericjob: job-sample
    genericjob-replica: job-sample-worker-2
    scheduler.tensorstack.dev/group-name: job-sample
    scheduler.tensorstack.dev/queue: default
    tensorstack.dev/component: genericjob
    tensorstack.dev/component-type: user
  name: job-sample-worker-0
  namespace: dev-wangdi
  ownerReferences: [...]
```

#### 弹性训练

弹性训练要求训练规模可以动态调整，所以对 PodGroup 的设置也有所不同。

T9k Job 中，PyTorchTrainingJob 和 DeepSpeedJob 支持弹性训练，他们具有相同的 `spec.elastic` 字段，以此启动弹性训练。

以下面的 PyTorchTrainingJob 为例：
* `spec.elastic.enabled` 是 true 表明启用弹性训练
* PyTorchTrainingJob 支持最少 3 个副本、最多 10 个副本的训练规模
```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: PyTorchTrainingJob
metadata:
 name: torch-mnist-trainingjob
spec:
 scheduler:
   t9kScheduler:
     queue: default
     priority: 10
 elastic:
   enabled: true
   minReplicas: 3
   maxReplicas: 10
   expectedReplicas: 7
 ...
```

控制器在监测到上述 CRD 后，会创建下列 PodGroup，使用 `spec.elastic.minReplicas` 作为 PodGroup 的 `spec.minMember`：
```yaml
apiVersion: scheduler.tensorstack.dev/v1beta1
kind: PodGroup
metadata:
  name: torch-mnist-trainingjob
  ownerReferences: [...]
spec:
  minMember: 3
  priority: 10
  queue: default
```

