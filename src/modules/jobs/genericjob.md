# GenericJob

GenericJob 是最基本的 T9k Job 资源，支持使用 T9k 高级调度策略。GenericJob 的使用十分灵活，一个熟练的使用者可以通过 GenericJob 实现 MPIJob、PyTorchTrainingJob 等特定功能的 T9k Job。

## 创建 GenericJob

下面是一个基本的 GenericJob 配置示例：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: GenericJob
metadata:
  name: generic-example
spec:
  successRules:
    - { "worker": [0] }
  failureRules:
    - { "worker": [0] }
    - { "worker": [1] }
  replicaSpecs:
    - type: worker
      replicas: 4
      template:
        spec:
          containers:
            - command:
                - sleep
                - '365'
              image: nginx:latest
              name: sleep
```

在该例中：

* 创建 4 个副本（由 `spec.replicaSpecs[0].replicas` 字段指定），这些副本的角色为 `worker`（由 `spec.replicaSpecs[0].type` 字段指定）。每个副本执行命令 `sleep 365`（由 `spec.replicaSpecs[0].template` 字段指定）。
* GenericJob 的成功条件为序号为 0 且角色为 `worker` 的副本执行完成（由 `spec.successRules` 字段指定）。
* GenericJob 的失败条件有两个，任意一个条件达成都会导致 GenericJob 失败（由 `spec.failureRules` 字段指定）：
    * 序号为 0 且角色为 `worker` 的副本执行失败。
    * 序号为 1 且角色为 `worker` 的副本执行失败。

## 成功和失败

GenericJob 的成功和失败条件是通过 `spec.successRules` 和 `spec.failureRules` 字段指定的，其规则如下：

* `spec.successRules` 数组包含 GenericJob 的所有成功条件，其中：
    * 任意一个条件达成则 GenericJob 成功。
    * 每个条件是一个由若干副本组成的集合，如果这些副本都执行完成，则该条件达成。
* `spec.failureRules` 数组包含 GenericJob 的所有失败条件，其中
    * 任意一个条件达成则 GenericJob 失败。
    * 每个条件是一个由若干副本组成的集合，如果这些副本都失败或者重启次数耗尽，则该条件达成。

在下面的示例中，记录了 3 种 GenericJob 成功的判定条件：

* 角色为 `master` 且序号为 0 的副本执行完成。
* 角色为 `worker` 且序号为 0、1、2 的三个副本全部执行完成。
* 角色为 `master` 且序号为 2 和角色为 `worker` 且序号为 0、1 的三个副本全部执行完成。

和 1 种 GenericJob 失败的判定：

* 角色为 `master` 且序号为 0 的副本执行失败。

```yaml
...
spec:
  successRules:
  - {"master": [0]}
  - {"worker": [0, 1, 2]}
  - {"master": [2], "worker": [0, 1]}
  failureRules:
  - {"master": [0]}
```

## 暴露副本的服务

在分布式计算中，有时需要不同的副本之间进行通信和数据交换。使用者可以通过设置 `spec.service` 字段来暴露副本的端口。

在下面的示例中，GenericJob 暴露出每一个副本的服务：端口为 `2222`，域名的格式为 `[job-name]-[type]-[rank]`，例如下例中角色为 `worker` 且序号为 0 的副本的域名为 `generic-example-worker-0`。

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: GenericJob
metadata:
  name: generic-example
spec:
  service:
    ports:
      - name: http
        port: 2222
  replicaSpecs:
    - type: worker
      replicas: 1
...
```

## 变量替换

在副本的配置信息中有时需要传入副本自身或其他副本的信息，包括序号、角色和副本的服务地址等。GenericJob 通过变量替换的方式提供这些信息，主要有以下 5 种变量：

* `$(type)`：当前副本的角色。
* `$(rank)`：当前副本在同类副本中的序号。
* `$(replicas[_type_])`：扮演此角色的副本的数量。
* `$(service._type_[_rank_].host)`：各个副本的域名（当且仅当[副本的服务被暴露出来](#暴露副本端口)，此变量可用）。
* `$(service.port[_port-name_])`：`spec.service.ports` 字段中定义的服务端口号（当且仅当[副本的服务被暴露出来](#暴露副本端口)，此变量可用）。

上述变量中 `_type_`、`_rank_` 和 `_port-name_` 需填入具体的**角色**、**序号**和**端口名称**（由 `spec.service.ports[*].name` 字段指定）。

变量替换可以被使用在下列字段中：

* `spec.replicaSpecs[*].template.command`
* `spec.replicaSpecs[*].template.args`
* `spec.replicaSpecs[*].template.env`

以下是用 GenericJob 实现的 TensorFlow 分布式框架使用示例，其中 `TF_CONFIG` 环境变量需要填写所有副本的地址和当前副本的序号等信息，我们使用变量替换的方式添加：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: GenericJob
metadata:
  name: generic-example
spec:
  replicaSpecs:
    - type: worker
      replicas: 4
      template:
        spec:
          containers:
            - command:
                - python
                - /mnt/training.py
              image: tensorflow/tensorflow:2.11.0
              name: tensorflow
              env:
                - name: TF_CONFIG
                  value: '{"task":{"type":"$(type)","index":$(rank)},"cluster":{"worker":["$(service.worker[0].host):$(service.port[http])","$(service.worker[1].host):$(service.port[http])","$(service.worker[2].host):$(service.port[http])","$(service.worker[3].host):$(service.port[http])"]}}'
```

## 重启机制

GenericJob 为副本提供以下重启机制：

1. `Never`：不重启
2. `OnFailure`：错误即重启
3. `Always`：总是重启（谨慎使用此策略，此策略可能导致 GenericJob 无法停止）

GenericJob 重启机制通过 `spec.replicaSpecs[*].restartPolicy` 字段指定:

* `spec.replicaSpecs[*].restartPolicy.policy` 表示当前副本所使用的重启策略，可以设置为 `Never`、`OnFailure` 或 `Always`。
* `spec.replicaSpecs[*].restartPolicy.limit` 表示当前副本的最大重启次数。

不同的角色可以使用不同的重启策略，比如 `master` 使用 `Always`，`worker` 使用 `OnFailure`。

## 清除策略

在 GenericJob 成功或失败后，控制器清理所创建的 Kubernetes 资源，使 GenericJob 不再浪费集群资源（内存、CPU 等）。GenericJob 提供三种策略，通过 `spec.cleanUpPolicy` 字段指定：

* `All`：清除全部副本
* `None`：不清除副本
* `Unfinished`：清除未结束（处于 `Pending`、`Running` 或 `Unknown` 阶段）的副本

!!! tip "提示"
    已结束的副本不会继续消耗集群资源，因此在一定程度上，`Unfinished` 策略比 `All` 策略更优。但这并不总是适用，由于一个项目的资源配额的计算不考虑 Pod 是否已经结束，对于资源紧张的项目，如果确定不需要通过日志来调试 Job，则可以使用 `All` 策略。
    
    `None` 策略主要用于训练脚本调试阶段。如果需要从副本中读取训练日志，则可以选用此策略。但由于这些副本可能占用资源并影响后续训练，建议您在调试完毕后手动删除这些副本或删除整个 GenericJob。

## 调度器

目前 GenericJob 支持两种调度器：

1. Kubernetes 的<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/#kube-scheduler">默认调度器</a>
2. [T9k Scheduler 调度器](../../cluster/scheduling/index.md)

调度器通过 `spec.scheduler` 字段设置：

* 不设置 `spec.scheduler` 字段，则默认使用 Kubernetes 的默认调度器。
* 设置 `spec.scheduler.t9kScheduler` 字段，则使用 T9k Scheduler 调度器。

在下面的示例中，GenericJob 启用 T9k Scheduler 调度器，将副本插入 `default` 队列中等待调度，其优先级为 50。

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

## 调试模式

GenericJob 支持调试模式。在该模式下，训练环境会被部署好，但不会启动训练，用户可以连入副本测试环境或脚本。

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

GenericJob 支持暂停模式。在该模式下，删除（或不创建）副本，停止训练。

该模式可以通过 `spec.runMode.pause` 字段来设置：

* `spec.runMode.pause.enabled` 表示是否启用暂停模式。
* `spec.runMode.pause.resumeSpecs` 表示结束暂停后，如何恢复各个副本：
    * `spec.runMode.pause.resumeSpecs.type` 表示作用于的副本类型。
    * `spec.runMode.pause.resumeSpecs.skipInitContainer` 表示让副本的 InitContainer 失效，默认为 `false`。
    * `spec.runMode.pause.resumeSpecs.command` 和 `spec.runMode.pause.resumeSpecs.args` 表示副本在恢复运行时候执行的命令，默认使用 `spec.replicaSpecs[0].template` 中的命令。
    * 如果不填写 `spec.runMode.pause.resumeSpecs` 字段，则表示所有副本都使用默认设置。

用户可以随时修改 `spec.runMode.pause.enabled` 来控制任务暂停，但是不可以更改 `spec.runMode.pause.resumeSpecs`，所以如果有暂停 GenericJob 的需求，请提前设置好恢复设置。

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

## GenericJob 状态

### GenericJob 的状态和阶段

`status.conditions` 字段用于描述当前 GenericJob 的状态，包括以下 6 种类型：

1. `Initialized`：GenericJob 已经成功创建各子资源，完成初始化。
2. `Running`：开始执行任务。
3. `ReplicaFailure`：有一个或多个副本出现错误。
4. `Completed`：GenericJob 成功。
5. `Failed`：GenericJob 失败。
6. `Paused`：GenericJob 进入暂停模式，所有副本都已删除或正在删除。

`status.phase` 字段用于描述当前 GenericJob 所处的阶段，GenericJob 的整个生命周期主要有以下7个阶段：

1. `Pending`：GenericJob 刚刚创建，等待副本启动。
2. `Running`：副本创建成功，开始执行任务。
3. `Paused`：GenericJob 进入暂停模式。
4. `Resuming`：GenericJob 正从暂停模式中恢复运行。恢复运行后，切换为 `Running` 阶段。
5. `Succeeded`：GenericJob 成功。
6. `Failed`：GenericJob 失败。
7. `Unknown`：控制器无法获得 GenericJob 的阶段。

在下面的示例中，GenericJob 所有子资源创建成功，所以类型为 `Initalized` 的 `condition` 被设为 `True`；GenericJob 运行结束，所以类型为 `Completed` 的 `condition` 被设置为 `True`；但是 GenericJob 的训练结果是失败的，所以类型为 `Failed` 的 `condition` 被设置为 `True`（原因是 `The job is failed with rule: { "worker": [0] }`）。当前 GenericJob 运行阶段为 `Failed`。


```yaml
...
status:
  conditions:
    - lastTransitionTime: "2021-01-18T02:36:09Z"
      status: "True"
      message: "The job has been initialized successfully."
      reason: "-"
      type: Initializing
    - lastTransitionTime: "2021-01-18T02:36:09Z"
      status: "True"
      message: "All pods are running normally."
      reason: "-"
      type: Running
    - lastTransitionTime: "2021-01-18T02:36:09Z"
      status: "False"
      message: "All pods are running normally."
      reason: "-"
      type: ReplicaFailure
    - lastTransitionTime: "2021-01-18T02:36:31Z"
      status: "False"
      message: 'The job is failed with rule: { "worker": [0] }'
      reason: "Failed"
      type: Completed
    - lastTransitionTime: "2021-01-18T02:36:31Z"
      status: "True"
      message: 'The job is failed with rule: { "worker": [0] }'
      reason: "Failed"
      type: Failed
  phase: Failed
```

### 副本的状态

`status.tasks` 字段用来记录副本的状态，记录的内容主要包括：

* 副本的重启次数（同一种角色的副本的重启次数之和）；
* 副本当前的运行阶段，此处的“运行阶段”在 K8s Pod 的 5 个阶段的基础上，添加了 `Creating` 和 `Deleted` 分别表示正在创建和已删除；
* 副本在集群中对应的 Pod 的索引信息。

在下面的示例中，GenericJob 创建了 2 个角色为 `worker` 的副本，这 2 个副本的重启次数之和为 3，当前均处于 `Running` 阶段，分别运行在 `generic-example-worker-0` 和 `generic-example-worker-1` 这 2 个 Pod 上。

```yaml
...
status:
  tasks:
  - type: worker
    restartCount: 3
    status:
    - phase: Running
      name: generic-example-worker-0
      uid: e3ec2ee3-6645-4e21-993f-1e472b94e0ae
      containers: []
    - phase: Running
      name: generic-example-worker-1
      uid: 908a93f0-7b8b-491e-85d5-3da0abcb4ca4
      containers: []
```

### 副本状态统计

`status.aggregate` 字段统计了各个阶段的副本数量。

在下面示例中，GenericJob 创建了 3 个副本，其中 1 个处于 `Pending` 阶段，另外两个处于 `Running` 阶段。

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
