# BeamJob

BeamJob 用于在集群中通过 <a target="_blank" rel="noopener noreferrer" href="https://beam.apache.org/documentation/sdks/python/">Apache Beam Python SDK</a> 运行分布式计算任务，并提供多种底层计算引擎，目前支持 <a target="_blank" rel="noopener noreferrer" href="https://flink.apache.org/">Apache Flink</a>，未来会支持 <a target="_blank" rel="noopener noreferrer" href="https://spark.apache.org/">Apache Spark</a>。

## 创建 BeamJob

下面是一个基本的 BeamJob 配置示例，负责统计输入文件中的英文单词出现次数，并将结果存储在输出文件中：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: BeamJob
metadata:
  name: beamjob-example
spec:
  flinkClusterTemplate:
    spec:
      flinkVersion: 1.10.1
      image:
        name: t9kpublic/flink:1.10.1
      jobManager:
        accessScope: Cluster
        resources:
          limits:
            cpu: "100m"
            memory: "1Gi"
      taskManager:
        replicas: 2
        resources:
          limits:
            cpu: "100m"
            memory: "2Gi"
      flinkProperties:
        taskmanager.numberOfTaskSlots: "1"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - image: t9kpublic/apache_beam_python3.7_sdk:2.22.0
            name: submit-job
            command:
              - "python3"
            args:
              - "-m"
              - "apache_beam.examples.wordcount"
              - "--input"
              - "/mypvc/input.txt"
              - "--output"
              - "/mypvc/output.txt"
            volumeMounts:
              - mountPath: "/mypvc"
                name: mypvc
          volumes:
            - name: mypvc
              persistentVolumeClaim:
                claimName: mypvc
          restartPolicy: OnFailure
```

在该例中：

* 您需要准备好一个名为 `mypvc` 的 PVC，并将名为 `input.txt` 的输入文件存放在 PVC 的根路径下。
* `flinkClusterTemplate` 字段描述了所要创建的 Flink 集群，其中包含 1 个 <a target="_blank" rel="noopener noreferrer" href="https://nightlies.apache.org/flink/flink-docs-release-1.11/concepts/flink-architecture.html#jobmanager) 和 2 个 [Task Manager](https://nightlies.apache.org/flink/flink-docs-release-1.11/concepts/flink-architecture.html#taskmanagers">Job Manager</a>{target=_blank}，所使用的 Flink 版本为 1.10.1。
* `jobTemplate` 字段描述了用户如何将所要运行的任务提交给 Flink 集群，其中所使用的 Apache Beam Python SDK 版本为 2.22.0，所运行的程序为 Apache Beam Python SDK 自带的单词统计程序 `apache_beam.examples.wordcount`。

## BeamJob 状态

### BeamJob 的状态和阶段

`status.conditions` 字段用于描述当前 BeamJob 的状态，包括以下 2 种类型：

* `ClusterRunning`：Flink 集群正在运行
* `JobRunning`：用户提交的任务正在运行

`status.phase` 字段用于描述当前 BeamJob 所处的阶段，BeamJob 的整个生命周期主要有以下几个阶段：

1. `Initializing`：BeamJob 刚刚创建，等待 Flink 集群启动。
2. `Running`：Flink 集群已启动，用户提交的任务正在运行。
3. `Succeeded`：BeamJob 成功。
4. `Failed`：BeamJob 失败。
5. `Unknown`：控制器执行错误，导致未能获取 BeamJob 当前运行阶段。

`status.jobURL` 字段是 Flink 集群的 Web UI 中用户提交的此次任务对应的详细信息页面。

在下面的示例中，Flink 集群已启动，所以类型为 `ClusterRunning` 的 `condition` 被设置为 `True`；用户所提交的任务正在运行，所以类型为 `JobRunning` 的 `condition` 被设置为 `True`。当前 BeamJob 运行阶段为 `Running`，如需在 Flink 集群的 Web UI 中查看任务的详细信息，请跳转至 `jobURL`。

```yaml
...
status:
  conditions:
    - lastTransitionTime: "2021-01-18T02:36:09Z"
      status: "True"
      type: ClusterRunning
    - lastTransitionTime: "2021-01-18T02:36:31Z"
      status: "True"
      type: JobRunning
  phase: Running
  jobURL: /t9k/flink-cluster/beamjob-example-flinkcluster/namespace/t9k-example/#/job/c9f62e4d61d089f351ab1f8b29e1df32/overview/
```

### Flink 集群的状态

`status.flinkClusterStatus` 字段用来记录 Flink 集群的状态，包括所有 Job Manager 和 Task Manager 的运行阶段以及对应的 Pod 索引。

在下面的示例中，BeamJob 创建的 Flink 集群包括 1 个 Job Manager 和 2 个 Task Manager，均处于 `Running` 阶段（记录在 `phase` 字段中），对应的 Pod 的索引信息记录在 `reference` 字段中（包括 Pod 的名称和 UID）。

```yaml
...
status:
  flinkClusterStatus:
    jobManagerStatus:
    - phase: Running
      reference:
        name: beamjob-example-flinkcluster-jobmanager-0
        uid: 21c67b2d-88d4-4b0a-9044-2311edee5e83
    taskManagerStatus:
    - phase: Running
      reference:
        name: beamjob-example-flinkcluster-taskmanager-0
        uid: c120c704-0730-49c8-8995-5fb719840af7
    - phase: Running
      reference:
        name: beamjob-example-flinkcluster-taskmanager-1
        uid: f1326d53-c5b6-4869-b5e9-8c35b7a7637d
```

### 用户提交任务的状态

`status.jobStatus` 字段用来记录用户所提交的任务的状态，包括运行阶段以及对应的 Pod 索引。

在下面的示例中，BeamJob 创建的用户任务仅包含 1 个 Pod，处于 `Succeeded` 阶段（记录在 `phase` 字段中），对应的 Pod 的索引信息记录在 `reference` 字段中（包括 Pod 的名称和 UID）。用户所提交的任务运行可能出现错误并多次重试，因此 `status.jobStatus` 字段可能包含多个 Pod。

```yaml
...
status:
  jobStatus:
  - phase: Succeeded
    reference:
      name: beamjob-example-batchjob-szsn8
      uid: 9aed0159-fe2a-4096-99a7-1c89af5a6f0e
```

## 清除策略

在 BeamJob 成功或失败后，所创建的 Flink 集群仍然在运行，占据较多的计算资源。在下面的示例中，您可以在 `spec.runPolicy` 字段中将 `cleanUpCluster` 设置为 `true`，在 BeamJob 运行完毕（无论成功还是失败）之后删除 Flink 集群。

```yaml
...
spec:
  runPolicy:
    cleanUpCluster: true
...
```

<aside class="note">
<div class="title">注意</div>

删除 Flink 集群会丢失任务运行相关的所有信息，且无法恢复。

</aside>

## 调度器

目前 BeamJob 支持两种调度器：

1. Kubernetes 的<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/#kube-scheduler">默认调度器</a>
2. [T9k Scheduler 调度器](../scheduling/index.md)

调度器通过 `spec.scheduler` 字段设置：

* 不设置 `spec.scheduler` 字段，则默认使用 Kubernetes 的默认调度器。
* 设置 `spec.scheduler.t9kScheduler` 字段，则使用 T9k Scheduler 调度器。

在下面的示例中，BeamJob 启用 T9k Scheduler 调度器，将副本插入 `default` 队列中等待调度，其优先级为 50。

```yaml
...
spec:
  scheduler:
    t9kScheduler:
      queue: default
      priority: 50
...
```

<aside class="note info">
<div class="title">信息</div>

队列和优先级都是 T9k Scheduler 的概念，具体含义请参阅 [T9k Scheduler](../scheduling/index.md)。

</aside>
