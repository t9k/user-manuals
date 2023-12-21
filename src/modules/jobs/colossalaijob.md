# ColossalAIJob

ColossalAIJob 是服务于 <a target="_blank" rel="noopener noreferrer" href="https://colossalai.org/">ColossalAI</a> 分布式训练框架的 T9k Job。

您可以较为方便地使用 ColossalAIJob 为 ColossalAI 训练脚本提供训练环境，并监控训练进程。

## 创建 ColossalAIJob

下面是一个基本的 ColossalAIJob 配置示例：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: ColossalAIJob
metadata:
  name: colossalai-example
spec:
  ssh:
    authMountPath: /root/.ssh
    sshdPath: /usr/sbin/sshd
  launcher:
    image: hpcaitech/colossalai:0.3.0
    workingDir: /workspace
    env: []
    resources: 
      limits:
        cpu: 1
        memory: 2Gi
      requests:
        cpu: 500m
        memory: 1Gi
  worker:
    replicas: 2
    procPerWorker: 1
    command:
      - train.py
      - arg1
    torchArgs: []
    template:
      spec:
        restartPolicy: OnFailure
        containers:
          - image: hpcaitech/colossalai:0.3.0
            imagePullPolicy: IfNotPresent
            name: worker
            resources:
              limits:
                cpu: 2
                memory: 8Gi
                nvidia.com/gpu: 1
              requests:
                cpu: 1
                memory: 4Gi
                nvidia.com/gpu: 1
            volumeMounts:
              - mountPath: /workspace
                name: code
        volumes:
          - name: code
            persistentVolumeClaim:
              claimName: colossalai
```

在该例中：

* 创建 1 个启动副本，该启动副本是 ColossalAI 在训练中所必须的，启动副本的配置参考 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-template-v1/#PodTemplateSpec">PodTemplate</a>，这里不再赘述（启动副本的配置由 `spec.launcher` 字段指定）。
* 创建 2 个执行副本（由 `spec.worker.replicas` 字段指定），每个执行副本上启动 1 个训练进程（由 `spec.worker.procPerWorker` 字段指定），训练脚本和参数为 `train.py arg1`（由 `spec.worker.command` 字段指定），执行副本的其他配置参考 PodTemplate，这里不再赘述（这些配置由 `spec.worker.template` 字段指定）。
* 执行副本需要执行 sshd 程序，等待启动副本发来训练指令。sshd 的路径为 `/user/sbin/sshd`（由 `spec.ssh.sshdPath` 字段指定，使用该字段的原因是 sshd 程序必须使用绝对路径调用，所以需要其具体路径）。

!!! note "注意"
    另外，ColossalAIJob 的执行副本定义中必须包含一个 `name` 是 `worker` 的容器，用来作为训练容器。

    由于执行副本实际执行的命令是启动 `sshd`，所以执行副本的训练容器的 `command` 字段不再生效。

## ColossalAIJob 状态

### ColossalAIJob 的状态和阶段

`status.conditions` 字段用于描述当前 ColossalAIJob 的状态，包括以下 5 种类型：

1. `Initialized`：ColossalAIJob 已经成功创建各子资源，完成初始化。
2. `Running`：开始执行任务。
3. `ReplicaFailure`：有一个或多个副本出现错误。
4. `Completed`：ColossalAIJob 成功。
5. `Failed`：ColossalAIJob 失败。

`status.phase` 字段用于描述当前 ColossalAIJob 所处的阶段，ColossalAIJob 的整个生命周期主要有以下几个阶段：

1. `Pending`：ColossalAIJob 刚刚创建，等待副本启动。
2. `Running`：副本创建成功，开始执行任务。
3. `Succeeded`：ColossalAIJob 成功。
4. `Failed`：ColossalAIJob 失败。
5. `Unknown`：控制器无法获得 ColossalAIJob 的阶段。

在下面的示例中，ColossalAIJob 所有子资源创建成功，所以类型为 `Initalized` 的 `condition` 被设为 `True`；ColossalAIJob 运行结束，所以类型为 `Completed` 的 `condition` 被设置为 `True`；但是 ColossalAIJob 的训练结果是失败的，所以类型为 `Failed` 的 `condition` 被设置为 `True`。当前 ColossalAIJob 运行阶段为 `Failed`。

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
      message: "The job exited with an error code."
      reason: "Failed"
      type: Completed
    - lastTransitionTime: "2021-01-18T02:36:31Z"
      status: "True"
      message: "The job exited with an error code."
      reason: "Failed"
      type: Failed
  phase: Failed
```

### 副本的状态

`status.tasks` 字段用来记录副本的状态，记录的内容主要包括：

* 副本的重启次数（同一种角色的副本的重启次数之和）
* 副本当前的运行阶段
* 副本在集群中对应的 Pod 的索引信息

在下面的示例中，ColossalAIJob 创建了 1 个启动副本和 2 个执行副本。执行副本当前均处于 `Running` 阶段，分别运行在 `colossalai-example-worker-0` 和 `colossalai-example-worker-1` 这 2 个 Pod 上；启动副本当前处于 `Running` 阶段，运行在 `colossalai-example-launcher` Pod 上。

```yaml
...
status:
  tasks:
  - type: launcher
    restartCount: 0
    status:
    - phase: Running
      name: colossalai-example-launcher
      uid: 66634db2-35e7-4641-a4dc-adbd5479734e
      containers: []
  - type: worker
    restartCount: 0
    status:
    - phase: Running
      name: colossalai-example-worker-0
      uid: e3ec2ee3-6645-4e21-993f-1e472b94e0ae
      containers: []
    - phase: Running
      name: colossalai-example-worker-1
      uid: 908a93f0-7b8b-491e-85d5-3da0abcb4ca4
      containers: []
```

## 成功和失败

在 ColossalAIJob 分布式训练框架中：

* 如果启动副本执行失败，ColossalAIJob 训练失败。
* 如果启动副本执行成功，ColossalAIJob 并不一定成功：启动副本的作用是启动训练和监测，无论是训练成功还是失败，启动副本都会正常结束，而不是报错。因此，如果要确定 ColossalAIJob 是否成功结束，需要检查启动副本的日志。

## 重启机制

与其他 TrainingJob 不同，ColossalAIJob 使用 `colossalairun` 作为启动命令，在这种情况下，Pod 失败重启后不会再加入到训练中。所以 ColossalAIJob 无法像其他 TrainingJob 那样支持 Pod 失败重启。

## 清除策略

在 ColossalAIJob 训练结束后，ColossalAIJob 控制器可以清理所创建的 Kubernetes 资源，使 ColossalAIJob 不再浪费集群资源（内存、CPU 等）。一般来说，您需要查看启动副本的日志来确定训练结果，所以启动副本不在清理范围之内，ColossalAIJob 控制器只清理执行副本（通过 `spec.runPolicy.cleanUpWorkers` 字段设置）。

在下面的示例中，ColossalAIJob 在训练结束后会自动删除所有执行副本：

```yaml
...
spec:
  runPolicy:
    cleanUpWorkers: true
```

## 调度器

目前 ColossalAIJob 支持两种调度器：

1. Kubernetes 的<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/#kube-scheduler">默认调度器</a>
2. [T9k Scheduler 调度器](../../cluster/scheduling/index.md)

调度器通过 `spec.scheduler` 字段设置：

* 不设置 `spec.scheduler` 字段，则默认使用 Kubernetes 的默认调度器。
* 设置 `spec.scheduler.t9kScheduler` 字段，则使用 T9k Scheduler 调度器。

在下面的示例中，ColossalAIJob 启用 T9k Scheduler 调度器，将执行副本插入 `default` 队列中等待调度，其优先级为 50。

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

## Debug 模式

ColossalAIJob 支持 Debug 模式，在该模式下，训练环境会被部署好，但不会启动训练，用户可以连入副本测试环境或脚本。

该模式可以通过 `spec.runMode.debug` 字段来设置：

* `spec.runMode.debug.enable` 表示是否启用 Debug 模式。
* `spec.runMode.debug.replicaSpecs` 表示如何配置各个副本的 Debug 模式：
    * `spec.runMode.debug.replicaSpecs.type` 表示作用于的副本类型。
    * `spec.runMode.debug.replicaSpecs.skipInitContainer` 表示让副本的 InitContainer 失效，默认为 `false`。
    * `spec.runMode.debug.replicaSpecs.command` 表示副本在等待调试的时候执行的命令，默认为 `sleep inf`。
    * 如果不填写 `spec.runMode.debug.replicaSpecs` 字段，则表示副本使用上述默认设置。

在下面的示例中：

* 示例一：开启了 Debug 模式，并配置 worker 跳过 InitContainer，并执行 `/usr/bin/sshd`。
* 示例二：开启了 Debug 模式，副本使用默认 Debug 设置，即不跳过 InitContainer，并执行 `sleep inf`。

```yaml
# 示例一
...
spec:
  runMode:
    debug:
      enable: true
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
      enable: true
```
