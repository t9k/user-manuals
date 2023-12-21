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

!!! note "注意"
    TensorFlowTrainingJob 的 `spec.replicaSpecs[*].template` 字段一定要包含 `name` 为 `tensorflow` 的容器，以便控制器识别训练使用的主容器。

    TensorFlowTrainingJob 中执行的脚本应使用 TensorFlow 分布式训练框架，否则可能达不到训练效果。

## 副本的角色

在 TensorFlow 分布式训练框架中，副本有 4 种类型：Chief、Worker、PS 和 Evaluator。

在 TensorFlowTrainingJob 中，副本的类型由 `spec.replicaSpecs[*].type` 字段指定，分别是 `chief`、`worker`、`ps` 和 `evaluator`。

## 成功和失败

在 TensorFlow 分布式训练框架中，Chief 是主节点。如果没有指定 Chief，则会选择第一个 Worker 作为主节点。当分布式训练的主节点执行完成时，TensorFlow 分布式训练成功；反之，当分布式训练的主节点执行失败时，TensorFlow 分布式训练失败。

在 TensorFlowTrainingJob 中，如果没有 Chief 副本，则选取序号为 0 的 Worker 节点作为主节点。主节点的失败有时可能是因为环境因素导致的，比如集群网络断连、集群节点崩溃等等，此类原因导致的失败应该被允许自动恢复。针对这一情况，TensorFlowTrainingJob 允许副本重启（请参阅[重启机制](#重启机制)），并设定了重启次数限制（由 `spec.runPolicy.backoffLimit` 字段指定），当副本重启次数达到上限后，如果主节点再次失败，则 TensorFlowTrainingJob 失败。此外，TensorFlowTrainingJob 可以设置最长执行时间（由 `spec.runPolicy.activeDeadlineSeconds` 字段指定），当超过这个执行时间后，TensorFlowTrainingJob 失败。

如果 TensorFlowTrainingJob 在没有超过重启次数和没有超过最长执行时间的情况下成功完成了主节点的运行，则 TensorFlowTrainingJob 成功。

## 重启机制

TensorFlowTrainingJob 的 `spec.replicaSpec<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/workloads/pods/#pod-templates">*].template` 字段使用 [PodTemplate</a> 的规范填写，但是 Pod 的重启策略并不能完全满足 TensorFlowTrainingJob 的需求，所以 TensorFlowTrainingJob 使用 `spec.replicaSpec[*].restartPolicy` 字段覆盖 `spec.replicaSpec[*].template` 中指定的重启策略。

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

!!! tip "提示"
    已结束的副本不会继续消耗集群资源，因此在一定程度上，`Unfinished` 策略比 `All` 策略更优。但这并不总是适用，由于一个项目的资源配额的计算不考虑 Pod 是否已经结束，对于资源紧张的项目，如果确定不需要通过日志来调试 Job，则可以使用 `All` 策略。
    
    `None` 策略主要用于训练脚本调试阶段。如果需要从副本中读取训练日志，则可以选用此策略。但由于这些副本可能占用资源并影响后续训练，建议您在调试完毕后手动删除这些副本或删除整个 TensorFlowTrainingJob。

## 调度器

目前 TensorFlowTrainingJob 支持使用以下两种调度器：

1. Kubernetes 的<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/#kube-scheduler">默认调度器</a>
2. [T9k Scheduler 调度器](../../cluster/scheduling/index.md)

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

!!! info "信息"
    队列和优先级都是 T9k Scheduler 的概念，具体含义请参阅 [T9k Scheduler](../../cluster/scheduling/index.md)。

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

!!! info "信息"
    TensorBoard 的详细介绍请参阅 [TensorBoard](../../building/tensorboard.md)。

## 下一步

* 了解如何[使用 TensorFlowTrainingJob 进行 TensorFlow 分布式训练](../../../guide/run-distributed-training/tensorflow/index.md)
