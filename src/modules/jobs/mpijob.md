# MPIJob

<a target="_blank" rel="noopener noreferrer" href="https://www.open-mpi.org/">OpenMPI</a> 是一个开源的 MPI（Message Passing Interface）协议的实现项目。

MPIJob 是一种使用 OpenMPI 进行分布式计算的 T9k Job，此资源让您能够方便地在集群环境中使用 OpenMPI 进行训练。

## 创建 MPIJob

下面的 MPIJob 示例创建了 5 个执行副本，每个执行副本启动 3 个进程，运行随机游走程序：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: MPIJob
metadata:
  name: mpi-example
spec:
  worker:
    replicas: 5
    extraMPIArgs:
      - -N
      - "3"
      - --enable-recovery
      - --max-restarts
      - "100"
      - --allow-run-as-root
      - -bind-to
      - none
    cmd:
      - ./random_walk
      - "20"
      - "40"
      - "2"
    template:
      spec:
        containers:
          - name: mpi-worker
            image: t9kpublic/mpi-tutorial:2021022-2
            resources:
              limits:
                cpu: 100m
              requests:
                cpu: 50m
            workingDir: /usr/local/code
  mca:
    btl: ^openib
  runPolicy:
    cleanUpWorkers: true
  ssh:
    sshdPath: /usr/sbin/sshd
  mpiHome: /usr/local
```

在该例中：

* 创建 5 个执行副本（由 `spec.worker.replicas` 字段指定）。
* `spec.worker.template` 字段沿用 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/workloads/pods/#pod-templates">PodTemplate</a> 的规约，配置执行副本和启动副本的环境。每个执行副本包含一个名为 `mpi-worker` 的容器（为了确定用于执行 MPI 进程的容器，执行副本定义中必须有一个名为 `mpi-worker` 的容器）。`mpi-worker` 容器创建后执行 `sshd` 命令并等待启动副本连接，所以此容器会忽略 `PodTemplate` 定义中的 `command` 和 `args` 字段（因此该例中没有填写这两个字段）。
* 在执行副本准备完毕后，启动副本向执行副本发送启动命令，令执行副本创建 3 个 MPI 进程，这些进程分别执行 `./random_walk 20 40 2`（由 `spec.worker.cmd` 字段指定）命令。
* 在训练过程中不使用 Infiniband 进行通信（由 `spec.mca.btl` 字段指定）。
* 在训练结束后自动清除副本（由 `spec.runPolicy.cleanUpWorkers` 字段指定）来释放集群资源。
* sshd 的路径为 `/user/sbin/sshd`（由 `spec.ssh.sshdPath` 字段指定，使用该字段的原因是 sshd 程序必须使用绝对路径调用，所以需要其具体路径）。
* MPI 安装在 `/usr/local` 处（由 `spec.mpiHome` 字段指定，使用该字段的原因是 `mpirun` 的有些功能需要知道 MPI 的根目录地址才能正确运行）。

## 运行 Horovod 训练脚本

使用 <a target="_blank" rel="noopener noreferrer" href="https://horovod.ai/">Horovod</a> 框架的分布式训练脚本也可以使用 MPIJob 进行训练。

<aside class="note info">
<div class="title">信息</div>

Horovod 框架的分布式训练脚本一般使用 `horovodrun` 命令启动；而由于 Horovod 是基于 OpenMPI 实现的，所以也可以使用 `mpirun` 命令启动。两条命令的关系为：`horovodrun` 命令等同于 `mpirun -bind-to none -map-by slot -x NCCL_DEBUG=INFO -x LD_LIBRARY_PATH -x PATH -mca pml ob1 -mca btl ^openib`。具体信息请参阅 <a target="_blank" rel="noopener noreferrer" href="https://github.com/horovod/horovod/blob/master/docs/mpi.rst">Horovod With MPI</a>。

</aside>

在 MPIJob 中需要执行以下操作：

1. 在 `spec.worker.template.spec.containers[mpi-worker].env` 字段中添加 `NCCL_DEBUG`；
2. 在 `spec.mca` 字段中添加 `pml:ob1` 和 `btl:^openib`。

下面是使用 MPIJob 执行 Horovod 框架的分布式训练脚本的示例：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: MPIJob
metadata:
  name: mpi-example
spec:
  mca:
    btl: ^openib
    pml: ob1
  worker:
    template:
      spec:
        containers:
          - name: mpi-worker
            env: 
            - name: "NCCL_DEBUG"
              value: "INFO"
...
```

## 调度器

目前 MPIJob 支持使用以下两种调度器：

1. Kubernetes 的<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/#kube-scheduler">默认调度器</a>
2. [T9k Scheduler](../scheduling/index.md)

调度策略通过 `spec.scheduler` 字段设置：

* 不设置 `spec.scheduler` 字段，则使用 Kubernetes 的默认调度器。
* 设置 `spec.scheduler.t9kScheduler` 字段，则使用 T9k Scheduler 调度器。

在下面的示例中，MPIJob 启用 T9k Scheduler 调度器，将执行副本插入 `default` 队列中等待调度，其优先级为 50。

```yaml
...
spec:
  scheduler:
    t9kScheduler:
      queue: default
      priority: 50
```

<aside class="note info">
<div class="title">信息</div>

队列和优先级都是 T9k Scheduler 的概念，具体含义请参阅 [T9k Scheduler](../scheduling/index.md)。

</aside>

## 调试模式

MPIJob 支持调试模式。在该模式下，训练环境会被部署好，但不会启动训练，用户可以连入副本测试环境或脚本。

该模式可以通过 `spec.runMode.debug` 字段来设置：

* `spec.runMode.debug.enabled` 表示是否启用调试模式。
* `spec.runMode.debug.replicaSpecs` 表示如何配置各个副本的调试模式：
    * `spec.runMode.debug.replicaSpecs.type` 表示作用于的副本类型。
    * `spec.runMode.debug.replicaSpecs.skipInitContainer` 表示让副本的 InitContainer 失效，默认为 `false`。
    * `spec.runMode.debug.replicaSpecs.command` 表示副本在等待调试的时候执行的命令，`launcher` 的默认命令为 `sleep inf`，`worker` 的默认命令为 `/usr/bin/sshd -D`。
    * 如果不填写 `spec.runMode.debug.replicaSpecs` 字段，则表示所有副本都使用默认设置。

在下面的示例中：

* 示例一：开启了调试模式，并配置 worker 跳过 InitContainer，并执行 `sleep inf`。
* 示例二：开启了调试模式，副本使用默认调试设置，即 worker 不跳过 InitContainer，并执行 `/usr/bin/sshd -D`。

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
          command: ["sleep", "inf"]

---
# 示例二
...
spec:
  runMode:
    debug:
      enabled: true
```

## 暂停模式

MPIJob 支持暂停模式。在该模式下，删除（或不创建）副本，停止训练。

该模式可以通过 `spec.runMode.pause` 字段来设置：

* `spec.runMode.pause.enabled` 表示是否启用暂停模式。
* `spec.runMode.pause.resumeSpecs` 表示结束暂停后，如何恢复各个副本：
    * `spec.runMode.pause.resumeSpecs.type` 表示作用于的副本类型。
    * `spec.runMode.pause.resumeSpecs.skipInitContainer` 表示让副本的 InitContainer 失效，默认为 `false`。
    * `spec.runMode.pause.resumeSpecs.command` 和 `spec.runMode.pause.resumeSpecs.args` 表示副本在恢复运行时候执行的命令，默认使用 `spec.replicaSpecs[0].template` 中的命令。
    * 如果不填写 `spec.runMode.pause.resumeSpecs` 字段，则表示所有副本都使用默认设置。

用户可以随时修改 `spec.runMode.pause.enabled` 来控制任务暂停，但是不可以更改 `spec.runMode.pause.resumeSpecs`，所以如果有暂停 MPIJob 的需求，请提前设置好恢复设置。

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

## MPIJob 状态

### MPIJob 的状态和阶段

`status.conditions` 字段用于描述当前 MPIJob 的状态，包括以下 5 种类型：

1. `Initialized`：MPIJob 已经成功创建各子资源，完成初始化。
2. `Running`：开始执行任务。
3. `ReplicaFailure`：有一个或多个副本出现错误。
4. `Completed`：MPIJob **结束**。
5. `Failed`：MPIJob 失败。
6. `Paused`：MPIJob 进入暂停模式，所有副本都已删除或正在删除。

`status.phase` 字段用于描述当前 MPIJob 所处的阶段，MPIJob 的整个生命周期主要有以下几个阶段：

1. `Pending`：MPIJob 刚刚创建，等待副本启动。
2. `Running`：副本创建成功，开始执行任务。
3. `Paused`：MPIJob 进入暂停模式。
4. `Resuming`：MPIJob 正从暂停模式中恢复运行。恢复运行后，切换为 `Running` 阶段。
5. `Succeeded`：MPIJob **结束**。
6. `Failed`：MPIJob 失败。
7. `Unknown`：控制器无法获得 MPIJob 的阶段。

在下面的示例中，MPIJob 所有子资源创建成功，所以类型为 `Initalized` 的 `condition` 被设为 `True`；MPIJob 运行结束，所以类型为 `Completed` 的 `condition` 被设置为 `True`；但是 MPIJob 的训练结果是失败的，所以类型为 `Failed` 的 `condition` 被设置为 `True`。当前 MPIJob 运行阶段为 `Failed`。

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

<aside class="note">
<div class="title">注意</div>

上述 `conditions` 中的 `Completed` 和 `phase` 中的 `Succeeded` 并不表示 MPIJob 成功，仅仅表示 MPIJob 结束。

MPIJob 使用 `mpirun` 实现 MPI 计算，并将其移植到 Kubernetes 上，`mpirun` 的工作原理是：在本地运行 `mpirun`，向其他主机发送计算命令，并监听这些主机上所启动的进程运行状况，打印这些进程的日志，在所有进程结束（无论是成功还是失败）后退出，返回值为 0。在将 `mpirun` 移植到 Kubernetes 上之后，MPIJob 的控制器仅能看到 `mpirun` 是以什么方式结束的（返回值是零或非零），无法更准确地知道任务具体是成功还是失败，所以 MPIJob 以 `Completed` 记录任务结束的状态（而非 `Succeeded`）。

同理，`conditions` 和 `phase` 中的 `Failed` 表示的也不是 MPIJob 任务运行失败，而是启动副本、执行副本因为某些原因（集群故障、网络错误等）无法正确工作。

因此在 MPIJob 结束后，您需要通过查看启动副本的日志来确定任务的具体执行情况。

</aside>

### 副本的状态

`status.tasks` 字段用来记录副本的状态，记录的内容主要包括：

* 副本的重启次数（同一种角色的副本的重启次数之和）
* 副本当前的运行阶段
* 副本在集群中对应的 Pod 的索引信息

在下面的示例中，MPIJob 创建了 1 个启动副本和 2 个执行副本。当前均处于 `Running` 阶段，分别运行在 `mpi-example-worker-0` 和 `mpi-example-worker-1` 这 2 个 Pod 上；启动副本当前处于 `Running` 阶段，运行在 `mpi-example-launcher` Pod 上。

```yaml
...
status:
  tasks:
  - type: launcher
    restartCount: 0
    status:
    - phase: Running
      name: mpi-example-launcher
      uid: 66634db2-35e7-4641-a4dc-adbd5479734e
      containers: []
  - type: worker
    restartCount: 0
    status:
    - phase: Running
      name: mpi-example-worker-0
      uid: e3ec2ee3-6645-4e21-993f-1e472b94e0ae
      containers: []
    - phase: Running
      name: mpi-example-worker-1
      uid: 908a93f0-7b8b-491e-85d5-3da0abcb4ca4
      containers: []
```

### 副本状态统计

`status.aggregate` 字段统计了各个阶段的副本数量。

在下面示例中，MPIJob 创建了 3 个副本，其中 1 个处于 `Pending` 阶段，另外两个处于 `Running` 阶段。

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
## 下一步

* 了解如何[使用 Horovod 进行 Keras 模型的数据并行训练](../../tasks/horovod-keras-parallel.md)
* 了解如何[使用 Horovod 进行 PyTorch 模型的数据并行训练](../../tasks/horovod-pytorch-parallel.md)
