# TensorFlowTrainingJob

TensorFlowTrainingJob 是服务于 <a target="_blank" rel="noopener noreferrer" href="https://www.tensorflow.org/guide/distributed_training">TensorFlow</a> 分布式训练框架的 T9k Job。  

您可以较为方便地使用 TensorFlowTrainingJob 为 TensorFlow 训练脚本提供训练环境，并监控训练进程。

## 创建 TensorFlowTrainingJob

下面是一个基本的 TensorFlowTrainingJob 配置示例：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: TensorFlowTrainingJob
metadata:
  name: tensorflow-example
spec:
  replicaSpecs:
  - replicas: 4
    restartPolicy: OnFailure
    template:
      spec:
        containers:
        - command:
          - python
          - dist_mnist.py
          image: tensorflow/tensorflow:2.11.0
          name: tensorflow
          resources:
            limits:
              cpu: 1
              memory: 2Gi
            requests:
              cpu: 500m
              memory: 1Gi
    type: worker
```

在该例中：

* 创建 4 个副本（由 `spec.replicaSpecs[*].replicas` 字段指定），副本的角色为 `worker`（由 `spec.replicaSpecs[*].type` 字段指定）。
* 每个副本使用 `tensorflow/tensorflow:2.11.0` 镜像，执行命令 `python dist_mnist.py`（由 `spec.replicaSpecs<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/workloads/pods/#pod-templates">*].template` 字段指定，此处的填写方式参考 [PodTemplate</a>）。
* 当副本失败后，会自动重启（由 `spec.replicaSpecs[*].restartPolicy` 字段指定）。

<aside class="note">
<h1>注意</h1>

TensorFlowTrainingJob 的 `spec.replicaSpecs[*].template` 字段一定要包含 `name` 为 `tensorflow` 的容器，以便控制器识别训练使用的主容器。

TensorFlowTrainingJob 中执行的脚本应使用 TensorFlow 分布式训练框架，否则可能达不到训练效果。

</aside>

## 副本的角色

在 TensorFlow 分布式训练框架中，副本有 4 种类型：Chief、Worker、PS 和 Evaluator。

在 TensorFlowTrainingJob 中，副本的类型由 `spec.replicaSpecs[*].type` 字段指定，分别是 `chief`、`worker`、`ps` 和 `evaluator`。

## 成功和失败

在 TensorFlow 分布式训练框架中，Chief 是主节点。如果没有指定 Chief，则会选择第一个 Worker 作为主节点。当分布式训练的主节点执行完成时，TensorFlow 分布式训练成功；反之，当分布式训练的主节点执行失败时，TensorFlow 分布式训练失败。

在 TensorFlowTrainingJob 中，如果没有 Chief 副本，则选取序号为 0 的 Worker 节点作为主节点。主节点的失败有时可能是因为环境因素导致的，比如集群网络断连、集群节点崩溃等等，此类原因导致的失败应该被允许自动恢复。针对这一情况，TensorFlowTrainingJob 允许副本重启（请参阅[重启机制](#重启机制)），并设定了重启次数限制（由 `spec.runPolicy.backoffLimit` 字段指定），当副本重启次数达到上限后，如果主节点再次失败，则 TensorFlowTrainingJob 失败。此外，TensorFlowTrainingJob 可以设置最长执行时间（由 `spec.runPolicy.activeDeadlineSeconds` 字段指定），当超过这个执行时间后，TensorFlowTrainingJob 失败。

如果 TensorFlowTrainingJob 在没有超过重启次数和没有超过最长执行时间的情况下成功完成了主节点的运行，则 TensorFlowTrainingJob 成功。

## 重启机制

TensorFlowTrainingJob 的 `spec.replicaSpec[*].template` 字段使用 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/workloads/pods/#pod-templates">PodTemplate</a> 的规范填写，但是 Pod 的重启策略并不能完全满足 TensorFlowTrainingJob 的需求，所以 TensorFlowTrainingJob 使用 `spec.replicaSpec[*].restartPolicy` 字段覆盖 `spec.replicaSpec[*].template` 中指定的重启策略。

可选的重启策略有以下四种：

* `Never`：不重启
* `OnFailure`：失败后重启
* `Always`：总是重启
* `ExitCode`：特殊退出码重启

使用 `Never` 重启策略时，Job 的副本失败后不会重启。如果需要调试代码错误，可以选择此策略，便于从副本中读取训练日志。

`ExitCode` 是一种比较特殊的重启策略，它将失败进程的返回值分为两类：一类是由于系统环境原因或用户操作导致的错误，此类错误可以通过重启解决；另一类是代码错误或者其他不可自动恢复的错误。可重启的退出码包括：

* 130（128+2）：使用 `Control+C` 终止容器运行。
* 137（128+9）：容器接收到 `SIGKILL` 信号。
* 143（128+15）：容器接收到 `SIGTERM` 信号。
* 138：用户可以自定义这个返回值的含义。如果用户希望程序在某处退出并重启，可以在代码中写入这个返回值。

### 重启次数限制

如果因为某种原因（例如代码错误或者环境错误并且长时间没有修复），TensorFlowTrainingJob 不断地失败重启却无法解决问题，这会导致集群资源的浪费。用户可以通过设置 `spec.runPolicy.backoffLimit` 字段来设置副本的最大重启次数。重启次数为所有副本共享，即所有副本重启次数累计达到此数值后，副本将不能再次重启。

## 清除策略

在训练结束后，可能有些副本仍处于运行状态，比如 TensorFlow 训练框架中的 PS 经常在训练完成后仍然保持运行。这些运行的副本仍然会占用集群资源，TensorFlowTrainingJob 提供清除策略，在训练结束后删除这些副本。

TensorFlowTrainingJob 提供以下三种策略：

* `None`：不删除副本。
* `All`：删除所有副本。
* `Unfinished`：只删除未结束的副本。

<aside class="note tip">
<h1>提示</h1>

已结束的副本不会继续消耗集群资源，因此在一定程度上，`Unfinished` 策略比 `All` 策略更优。但这并不总是适用，由于一个项目的资源配额的计算不考虑 Pod 是否已经结束，对于资源紧张的项目，如果确定不需要通过日志来调试 Job，则可以使用 `All` 策略。

</aside>
    
    `None` 策略主要用于训练脚本调试阶段。如果需要从副本中读取训练日志，则可以选用此策略。但由于这些副本可能占用资源并影响后续训练，建议您在调试完毕后手动删除这些副本或删除整个 TensorFlowTrainingJob。

## 调度器

目前 TensorFlowTrainingJob 支持使用以下两种调度器：

1. Kubernetes 的<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/#kube-scheduler">默认调度器</a>
2. [T9k Scheduler 调度器](../scheduling/index.md)

调度器通过 `spec.scheduler` 字段设置：

* 不设置 `spec.scheduler` 字段，则默认使用 Kubernetes 的默认调度器。
* 设置 `spec.scheduler.t9kScheduler` 字段，则使用 T9k Scheduler 调度器。

在下面的示例中，TensorFlowTrainingJob 启用 T9k Scheduler 调度器，将副本插入 `default` 队列中等待调度，其优先级为 50。

```yaml
...
spec:
  scheduler:
    t9kScheduler:
      queue: default
      priority: 50
```

<aside class="note info">
<h1>信息</h1>

队列和优先级都是 T9k Scheduler 的概念，具体含义请参阅 [T9k Scheduler](../scheduling/index.md)。

</aside>

## TensorBoard 的使用

TensorFlowTrainingJob 支持使用 TensorBoard 对训练过程和结果进行实时可视化（由 `spec.tensorboardSpec` 字段设置）。

在下面的示例中，TensorFlowTrainingJob 使用 `t9kpublic/tensorboard:2.11.0` 镜像创建一个 TensorBoard，可视化名为 `tensorflow-tensorboard-pvc` 的 PVC 中 `/log` 路径下的模型数据。

```yaml
...
spec:
  tensorboardSpec:
    image: t9kpublic/tensorboard:2.11.0
    trainingLogFilesets:
    - t9k://pvc/tensorflow-tensorboard-pvc/log
...
```

<aside class="note info">
<h1>信息</h1>

TensorBoard 的详细介绍请参阅 [TensorBoard]((../building/tensorboard.md))。

</aside>

## 调试模式

TensorFlowTrainingJob 支持调试模式。在该模式下，训练环境会被部署好，但不会启动训练，用户可以连入副本测试环境或脚本。

该模式可以通过 `spec.runMode.debug` 字段来设置：

* `spec.runMode.debug.enabled` 表示是否启用调试模式。
* `spec.runMode.debug.replicaSpecs` 表示如何配置各个副本的调试模式：
    * `spec.runMode.debug.replicaSpecs.type` 表示作用于的副本类型。
    * `spec.runMode.debug.replicaSpecs.skipInitContainer` 表示让副本的 InitContainer 失效，默认为 `false`。
    * `spec.runMode.debug.replicaSpecs.command` 表示副本在等待调试的时候执行的命令，默认为 `sleep inf`。
    * 如果不填写 `spec.runMode.debug.replicaSpecs` 字段，则表示所有副本都使用默认设置。

在下面的示例中：

* 示例一：开启了调试模式，并配置 worker 跳过 InitContainer，并执行 `/usr/bin/sshd`。
* 示例二：开启了调试模式，副本使用默认调试设置，即不跳过 InitContainer，并执行 `sleep inf`。

```yaml
# 示例一
...
spec:
  runMode:
    debug:
      enabled: true
      replicaSpecs:
        - type: worker
          skipInitContainer: true
          command: ["/usr/bin/sshd"]

---
# 示例二
...
spec:
  runMode:
    debug:
      enabled: true
```

## 暂停模式

TensorFlowTrainingJob 支持暂停模式。在该模式下，删除（或不创建）副本，停止训练。

该模式可以通过 `spec.runMode.pause` 字段来设置：

* `spec.runMode.pause.enabled` 表示是否启用暂停模式。
* `spec.runMode.pause.resumeSpecs` 表示结束暂停后，如何恢复各个副本：
    * `spec.runMode.pause.resumeSpecs.type` 表示作用于的副本类型。
    * `spec.runMode.pause.resumeSpecs.skipInitContainer` 表示让副本的 InitContainer 失效，默认为 `false`。
    * `spec.runMode.pause.resumeSpecs.command` 和 `spec.runMode.pause.resumeSpecs.args` 表示副本在恢复运行时候执行的命令，默认使用 `spec.replicaSpecs[0].template` 中的命令。
    * 如果不填写 `spec.runMode.pause.resumeSpecs` 字段，则表示所有副本都使用默认设置。

用户可以随时修改 `spec.runMode.pause.enabled` 来控制任务暂停，但是不可以更改 `spec.runMode.pause.resumeSpecs`，所以如果有暂停 TensorFlowTrainingJob 的需求，请提前设置好恢复设置。

在下面的示例中：

* 示例一：开启了暂停模式，并配置 worker 跳过 InitContainer，并执行 `/usr/bin/sshd`。
* 示例二：开启了暂停模式，副本使用默认恢复设置，即不跳过 InitContainer，并执行 `spec.replicaSpecs[0].template` 中设置的命令。

```yaml
# 示例一
...
spec:
  runMode:
    pause:
      enabled: true
      resumeSpecs:
        - type: worker
          skipInitContainer: true
          command: ["/usr/bin/sshd"]

---
# 示例二
...
spec:
  runMode:
    pause:
      enabled: true
```

## TensorFlowTrainingJob 状态

### TensorFlowTrainingJob 的状态和阶段

`status.conditions` 字段用于描述当前 TensorFlowTrainingJob 的状态，包括以下 6 种类型：

1. `Initialized`：TensorFlowTrainingJob 已经成功创建各子资源，完成初始化。
2. `Running`：开始执行任务。
3. `ReplicaFailure`：有一个或多个副本出现错误。
4. `Completed`：TensorFlowTrainingJob 成功。
5. `Failed`：TensorFlowTrainingJob 失败。
6. `Paused`：TensorFlowTrainingJob 进入暂停模式，所有副本都已删除或正在删除。

`status.phase` 字段用于描述当前 TensorFlowTrainingJob 所处的阶段，TensorFlowTrainingJob 的整个生命周期主要有以下7个阶段：

1. `Pending`：TensorFlowTrainingJob 刚刚创建，等待副本启动。
2. `Running`：副本创建成功，开始执行任务。
3. `Paused`：TensorFlowTrainingJob 进入暂停模式。
4. `Resuming`：TensorFlowTrainingJob 正从暂停模式中恢复运行。恢复运行后，切换为 `Running` 阶段。
5. `Succeeded`：TensorFlowTrainingJob 成功。
6. `Failed`：TensorFlowTrainingJob 失败。
7. `Unknown`：控制器无法获得 TensorFlowTrainingJob 的阶段。

在下面的示例中，TensorFlowTrainingJob 所有子资源创建成功，所以类型为 `Initalized` 的 `condition` 被设为 `True`；TensorFlowTrainingJob 运行结束，所以类型为 `Completed` 的 `condition` 被设置为 `True`；TensorFlowTrainingJob 的训练成功结束，所以类型为 `Completed` 的 `condition` 被设置为 `True`（原因是 `The job has finished successfully.`）。当前 TensorFlowTrainingJob 运行阶段为 `Succeeded`。


```yaml
...
status:
  conditions:
    - lastTransitionTime: "2023-12-19T02:40:25Z"
      message: The job has been initialized successfully.
      reason: '-'
      status: "True"
      type: Initialized
    - lastTransitionTime: "2023-12-19T02:53:14Z"
      message: The job has finished successfully.
      reason: Succeeded
      status: "False"
      type: Running
    - lastTransitionTime: "2023-12-19T02:53:14Z"
      message: The job has finished successfully.
      reason: Succeeded
      status: "False"
      type: Failed
    - lastTransitionTime: "2023-12-19T02:53:14Z"
      message: The job has finished successfully.
      reason: Succeeded
      status: "True"
      type: Completed
    - lastTransitionTime: "2023-12-19T02:40:25Z"
      message: All pods are running normally.
      reason: '-'
      status: "False"
      type: ReplicaFailure
  phase: Succeeded
```

### 副本的状态

`status.tasks` 字段用来记录副本的状态，记录的内容主要包括：

* 副本的重启次数（同一种角色的副本的重启次数之和）；
* 副本当前的运行阶段，此处的“运行阶段”在 K8s Pod 的 5 个阶段的基础上，添加了 `Creating` 和 `Deleted` 分别表示正在创建和已删除；
* 副本在集群中对应的 Pod 的索引信息。

在下面的示例中，TensorFlowTrainingJob 创建了 1 个角色为 `worker` 的副本，当前均处于 `Succeeded` 阶段，运行在 `mnist-trainingjob-5b373-worker-0` 这个 Pod 上。

```yaml
...
status:
  tasks:
  - replicas:
    - containers:
      - exitCode: 0
        name: pytorch
        state: Terminated
      name: mnist-trainingjob-5b373-worker-0
      phase: Succeeded
      uid: d39f91d6-9c48-4c57-bb71-4131226395b6
    type: worker
```

### 副本状态统计

`status.aggregate` 字段统计了各个阶段的副本数量。

在下面示例中，TensorFlowTrainingJob 创建了 3 个副本，其中 1 个处于 `Pending` 阶段，另外两个处于 `Running` 阶段。

```yaml
...
status:
  aggregate:
    creating: 0
    deleted: 0
    failed: 0
    pending: 1
    running: 2
    succeeded: 0
    unknown: 0
...
```

### TensorBoard 状态

`status.tensorboard` 字段用来记录 TensorBoard 的状态。

在下面的示例中，TensorFlowTrainingJob 创建了名为 `mnist-trainingjob-5b373` 的 TensorBoard，TensorBoard 目前运行正常。

```yaml
status:
  tensorboard:
    action: NOP
    dependent:
      apiVersion: tensorstack.dev/v1beta1
      kind: TensorBoard
      name: mnist-trainingjob-5b373
      namespace: demo
      uid: b09378f3-2164-4f14-a425-a1340fa32d7d
    note: TensorBoard [mnist-trainingjob-5b373] is ready
    ready: true
    reason: DependentReady
    type: Normal
```

## 下一步

* 了解如何[使用 TensorFlowTrainingJob 进行数据并行训练](../../tasks/tensorflow-training-parallel.md)
* 了解如何[使用 TensorFlowTrainingJob 进行参数服务器训练](../../tasks/tensorflow-training-ps.md)
