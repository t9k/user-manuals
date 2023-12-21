# WorkflowTemplate

WorkflowTemplate 用于在 Kubernetes 中有序、高效、方便地组织运行各类工作负载，例如机器学习流水线中的数据处理、模型训练、推理测试等具有依赖关系的多个步骤。WorkflowTemplate 是一个静态模板，指定了任务的详细规范，最终由 [WorkflowRun](./workflowrun.md) 实例化并真正开始运行。

## 创建 WorkflowTemplate

下面的 WorkflowTemplate 示例创建并运行一个 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/zh/docs/concepts/workloads/pods/">Kubernetes Pod</a>。

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: workflowtemplate-sample
spec:
  description: This WorkflowTemplate creates and runs a Pod.
  type: Pod
  pod:
    containers:
      - name: hello
        image: ubuntu:latest
        resources:
          limits:
            cpu: 100m
            memory: 100Mi
        command: ["echo"]
        args: ["Hello TensorStack!"]
```

在该例中：

* `description` 字段简要介绍了该 WorkflowTemplate 的用途，会在控制台中展示。
* WorkflowTemplate 的类型（由 `type` 字段指定）是 Pod，表示 WorkflowTemplate 会创建并运行一个 Pod。
* `pod` 字段定义所要创建的 Pod 的规约，指示 Pod 运行一个 `hello` 容器，该容器运行镜像 `ubuntu:latest` 并打印一个字符串 `Hello TensorStack!`。

## WorkflowTemplate 类型

WorkflowTemplate 的 `spec.type` 字段用于指定 WorkflowTemplate 的类型，可能的取值有：

* [`Pod`](#pod-workflowtemplate)
* [`SeqPod`](#seqpod-workflowtemplate)
* [`Resource`](#resource-workflowtemplate)
* [`DAG`](#dag-workflowtemplate)
* [`GenericJob`](#t9k-jobs-workflowtemplate)
* [`MPIJob`](#t9k-jobs-workflowtemplate)
* [`BeamJob`](#t9k-jobs-workflowtemplate)
* [`TensorFlowTrainingJob`](#t9k-jobs-workflowtemplate)
* [`PyTorchTrainingJob`](#t9k-jobs-workflowtemplate)
* [`XGBoostTrainingJob`](#t9k-jobs-workflowtemplate)

### Pod WorkflowTemplate

Pod WorkflowTemplate 用于创建一个原生的 Kubernetes Pod。

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: pod-workflowtemplate-sample
spec:
  type: Pod
  pod:
    containers:
      - name: hello
        image: ubuntu
        resources:
          limits:
            cpu: 100m
            memory: 100Mi
        command: ["sh", "-c"]
        args: ["echo Hello World!"]
```

`spec.pod` 中可以填写的字段与 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#podspec-v1-core">Kubernetes Pod</a> 相同。

### SeqPod WorkflowTemplate

SeqPod WorkflowTemplate 用于创建一个经过包装的 Pod，在 Pod 中按顺序执行一些步骤。

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: seqpod-workflowtemplate-sample
spec:
  type: SeqPod
  seqPod:
    steps:
      - name: hello
        image: ubuntu
        resources:
          limits:
            cpu: 100m
            memory: 100Mi
        command: ["sh", "-c"]
        args: ["echo Hello World!"]
      - name: working
        image: ubuntu
        resources:
          limits:
            cpu: 100m
            memory: 100Mi
        command: ["sh", "-c"]
        args: ["echo I am working!"]
      - name: bye
        image: ubuntu
        resources:
          limits:
            cpu: 100m
            memory: 100Mi
        command: ["sh", "-c"]
        args: ["echo Goodbye!"]
```

SeqPod 中的每个步骤（step）对应 Kubernetes Pod 中的一个容器，但 SeqPod 会按照顺序依次执行每个步骤，直到所有的步骤成功运行完毕，或者其中某个步骤失败（后续的步骤不会再运行）。


!!! tip "提示"
    在 `pod.containers[*].command`、`pod.containers[*].args`、`seqPod.steps[*].command`、`seqPod.steps[*].args` 等字段中，您有时候可能需要填写带有引号的字符串，有以下几种合法的方式：

    ```
    command: ["echo"]
    args: ["this is a 'quote'"]
    ```

    ```
    command: ['echo']
    args: ['this is a "quote"']
    ```
    
    ```
    command:
      - echo
    args:
      - this is a "quote"
    ```

    ```
    command:
      - echo
    args:
      - this is a 'quote'
    ```

#### 指定 script

SeqPod 的每个步骤可以指定 `script` 字段，即一段脚本语言（例如 Bash、Python）编写的代码，用于代替 `command` 字段。`script` 脚本会在容器开始运行时代替 `command` 被调用，而 `args` 会被当做参数传递给 `script` 脚本。

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: seqpod-workflowtemplate-sample-script
spec:
  type: SeqPod
  seqPod:
    steps:
      - name: hello
        image: python
        resources:
          limits:
            cpu: 100m
            memory: 100Mi
        script: |
          #!/usr/bin/env python3
          print("Hello from Python!")
```

如果 `script` 脚本的开头不包含以 `#!` 开头的字符串（<a target="_blank" rel="noopener noreferrer" href="https://en.wikipedia.org/wiki/Shebang_(Unix)">shebang</a>），以下字符串会被自动添加到 `script` 脚本的开头：

```bash
#!/bin/bash
set -e # Immediately exit if any command exited with non-zero status. 
```

#### 保留目录

为了 SeqPod WorkflowTemplate 的正常工作，最终生成的 Pod 有一些特殊的保留目录：

* `/t9k/workspaces`：用于挂载 [workspaces](#指定工作空间)，您可以通过 `$(workspaces.<workspaceName>.path)` 来使用该路径。
* `/t9k/results`：用于存储 [results](#输出结果)，您可以通过 `$(results.<resultName>.path)` 来使用该路径。
* `/t9k/tools`：用于保证 SeqPod 中 `steps` 顺序执行的辅助工具，与用户无关。
* `/t9k/termination`：用于写入 Pod 的 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/tasks/debug-application-cluster/determine-reason-pod-failure/#writing-and-reading-a-termination-message">termination message</a>，与用户无关。

### Resource WorkflowTemplate

Resource WorkflowTemplate 用于创建另一个 Kubernetes 资源，并监测该资源的运行状态。

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: resource-workflowtemplate-sample
spec:
  type: Resource
  resource:
    manifest: |
      apiVersion: batch/v1
      kind: Job
      metadata:
        generateName: pi-job-
      spec:
        template:
          metadata:
            name: pi
          spec:
            containers:
            - name: pi
              image: perl
              command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
            restartPolicy: Never
        backoffLimit: 4
    successRules:
      fieldSelector: status.succeeded > 0
    failureRules:
      fieldSelector: status.failed > 3
```

`spec.resource` 的各个字段含义如下：

* `manifest`：所要创建的 Kubernetes 资源的详细配置。
* `successRules`：如果所创建的资源满足该条件，本 WorkflowTemplate 视为成功。
* `failureRules`：如果所创建的资源满足该条件，本 WorkflowTemplate 视为失败。

`fieldSelector` 的写法与 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/">Kubernetes 标签选择器</a>的语法相同但更强大，除了标签之外还能应用到资源的任意字段，支持的运算符有 `>`、`<`、`==`、`!=`、`in`、`notin` 等，多个需要同时满足的条件可以用逗号连接。例如，以下都是合法的 `fieldSelector`：

* `status.succeeded>0`
* `status.succeeded > 0`
* `status.succeeded > 0,status.failed == 0`
* `status.phase in (Succeeded, Failed),status.workflowTemplateSpec.type == DAG`

另外，`successRules` 和 `failureRules` 还支持设置 `conditionSelector`。如果所创建的资源的 `status.conditions` 字段包含一个 `condition`，其 `type` 和 `status` 都与 `conditionSelector` 相同，就认为该资源满足条件。

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: resource-workflowtemplate-sample-condition
spec:
  type: Resource
  resource:
    manifest: |
      apiVersion: batch.tensorstack.dev
      kind: TensorFlowTrainingJob
      metadata:
        generateName: t9k-training-job-
      spec:
        ...
    successRules:
      conditionSelector:
        type: Succeeded
        status: "True"
    failureRules:
      conditionSelector:
        type: Failed
        status: "True"
```

如果所创建的资源类型是下列 [T9k Jobs](../job/index.md) 之一，系统将自动帮助填写 `successRules` 和 `failureRules`，以减轻您的负担：

* GenericJob
* MPIJob
* BeamJob
* TensorFlowTrainingJob
* PyTorchTrainingJob
* XGBoostTrainingJob

!!! note "注意"

    创建 Resource WorkflowTemplate 对应的 WorkflowRun 时需要提供一个 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/kubernetes-api/authentication-resources/service-account-v1/">Service Account</a>，使得 WorkflowRun 具有在 Kubernetes 中创建该 Resource 的权限。例如：

    ```yaml
    apiVersion: batch.tensorstack.dev/v1beta1
    kind: WorkflowRun
    metadata:
      name: resource-workflowtemplate-sample-run
    spec:
      workflowTemplateRef: resource-workflowtemplate-sample
      serviceAccountName: managed-project-sa
    ```

    在网页中创建 WorkflowRun 时，系统将自动为您配置名为 `managed-project-sa` 的 Service Account，您不用关心这一项的填写。

### T9k Jobs WorkflowTemplate

T9k Workflow 系统对 [T9k Jobs](../job/index.md) 提供更进一步的原生支持，添加以下 WorkflowTemplate 类型：

* GenericJob
* MPIJob
* BeamJob
* TensorFlowTrainingJob
* PyTorchTrainingJob
* XGBoostTrainingJob

并在 WorkflowTemplate 的 `spec` 中添加了相应字段用于填写 T9k Job 的 `spec`：

* `spec.genericJob`
* `spec.mpiJob`
* `spec.beamJob`
* `spec.tensorflowTrainingJob`
* `spec.pytorchTrainingJob`
* `spec.xgboostTrainingJob`

相比于在 Resource 类型中将资源的 `spec` 视作一个很长的字符串，添加原生类型支持的好处是在创建 WorkflowTemplate 时 T9k Job 的 `spec` 就会得到语法检查，能更早地发现错误，加深了 T9k Workflow 系统和 T9k Job 系统的集成配合。

例如，创建一个 MPIJob 可以使用如下格式（其中 MPIJob 示例来自 [MPIJob 文档](../../workflow/job/mpijob#创建-mpijob)）：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: mpijob-workflowtemplate-sample
spec:
  type: MPIJob
  mpiJob:
    spec:
      worker:
        replicas: 5
        processesPerWorker: 3
        processRecovery:
          enable: true
          limit: 100
        cmd:
          - ./random_walk
          - "20"
          - "40"
          - "2"
        template:
          spec:
            containers:
              - name: mpi-worker
                image: registry.tensorstack.cn/t9k/mpi-tutorial:1.41.0
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

!!! note "注意"

    与 Resource WorkflowTemplate 相同，T9k Jobs WorkflowTemplate 对应的 WorkflowRun 也需要一个 Service Account。同样，在网页中创建 WorkflowRun 时，系统将自动为您配置名为 `managed-project-sa` 的 Service Account，您不用关心这一项的填写。


### DAG WorkflowTemplate

DAG WorkflowTemplate 用于创建一个由其他 WorkflowTemplate 组成的有向无环图（DAG，Directed Acyclic Graph），按照有向无环图中的依赖关系按顺序执行这些 WorkflowTemplate。

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: dag-workflowtemplate-sample
spec:
  type: DAG
  dag:
    templates:
      - name: a
        workflowTemplateRef: pod-workflowtemplate-sample
        dependencies: []
      - name: b1
        workflowTemplateRef: pod-workflowtemplate-sample
        dependencies: ["a"]
      - name: b2
        workflowTemplateRef: pod-workflowtemplate-sample
        dependencies: ["a"]
      - name: c
        workflowTemplateRef: pod-workflowtemplate-sample
        dependencies: ["b1", "b2"]
```

在上面的示例中，首先运行 WorkflowTemplate a，等待 WorkflowTemplate a 运行完毕之后再同时运行 WorkflowTemplate b1 和 b2。WorkflowTemplate c 会在 b1 和 b2 都结束后运行。这些 WorkflowTemplates 组成一个从上往下顺序执行的有向无环图：

```yaml
   a
 /   \
b1   b2
 \   /
   c
```

## 指定参数

您可以为 WorkflowTemplate 指定一些参数，并在 `spec` 中用 `$(params.<paramName>)` 来引用参数。[WorkflowRun](./workflowrun.md) 会在运行时为这些参数提供实际值。支持 `params` 的 WorkflowTemplate 类型有 Pod、SeqPod、DAG，详见[支持变量替换的 WorkflowTemplate 字段](../../../reference/tensorstack-resources/workflow-api/variable-substitution-rules.md#支持变量替换的-workflowtemplate-字段)。

Pod WorkflowTemplate 示例：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: pod-workflowtemplate-sample-params
spec:
  params:
    - name: message
      default: "hi"
  type: Pod
  pod:
    containers:
      - name: hello
        image: ubuntu
        resources:
          limits:
            cpu: 100m
            memory: 100Mi
        command: ["sh", "-c"]
        args: ["echo $(params.message)"]
```

SeqPod WorkflowTemplate 示例：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: seqpod-workflowtemplate-sample-params
spec:
  params:
    - name: message
      default: hi
  type: SeqPod
  seqPod:
    steps:
      - name: hello
        image: ubuntu
        resources:
          limits:
            cpu: 100m
            memory: 100Mi
        script: |
          #!/bin/sh
          echo $(params.message)
```

DAG WorkflowTemplate 在引用其他的 WorkflowTemplate 作为节点时，必须提供该节点需要的 `params`，可以是静态的字符串，也可以引用 DAG WorkflowTemplate 自身的 `params` 变量或[其他变量](../../../reference/tensorstack-resources/workflow-api/variable-substitution-rules.md)。示例：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: dag-workflowtemplate-sample-params
spec:
  params:
    - name: dag-param
  type: DAG
  dag:
    templates:
      - name: step0
        workflowTemplateRef: pod-workflowtemplate-sample-params
        dependencies: []
        params:
          - name: message
            value: Hello World!
      - name: step1
        workflowTemplateRef: seqpod-workflowtemplate-sample-params
        dependencies: ["step0"]
        params:
          - name: message
            value: "$(params.dag-param)"
      - name: step2
        workflowTemplateRef: seqpod-workflowtemplate-sample-params
        dependencies: ["step1"]
        params:
          - name: message
            value: "DAG WorkflowTemplate provides param $(params.dag-param) for you"
```

## 指定工作空间

您可以为 WorkflowTemplate 指定可用的存储空间，并在 `spec` 中用 `$(workspaces.<workspaceName>.path)` 来引用存储空间的路径。[WorkflowRun](./workflowrun.md) 会在运行时指定具体挂载何种存储空间，例如 PVC、Secret、ConfigMap 等。支持 `workspaces` 的 WorkflowTemplate 类型有 Pod、SeqPod、DAG。

Pod WorkflowTemplate 示例：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: pod-workflowtemplate-sample-workspace
spec:
  workspaces:
    - name: pod-workspace
  type: Pod
  pod:
    containers:
      - name: hello
        image: ubuntu
        resources:
          limits:
            cpu: 100m
            memory: 100Mi
        command: ["sh", "-c"]
        args: ["echo Hello World! > $(workspaces.pod-workspace.path)/output.txt"]
```

SeqPod WorkflowTemplate 示例：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: seqpod-workflowtemplate-sample-workspaces
spec:
  workspaces:
    - name: seqpod-workspace
  type: SeqPod
  seqPod:
    steps:
      - name: hello
        image: ubuntu
        resources:
          limits:
            cpu: 100m
            memory: 100Mi
        script: |
          #!/bin/sh
          echo Hello World! > $(workspaces.seqpod-workspace.path)/output.txt
```

DAG WorkflowTemplate 在引用其他的 WorkflowTemplate 作为节点时，必须提供该节点需要的 `workspaces`，一般通过 DAG WorkflowTemplate 自身的 `workspaces` 继承而来。示例：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: dag-workflowtemplate-sample-workspaces
spec:
  workspaces:
    - name: dag-workspace
  type: DAG
  dag:
    templates:
      - name: step0
        workflowTemplateRef: pod-workflowtemplate-sample-workspace
        dependencies: []
        workspaces:
          - name: pod-workspace
            workspace: dag-workspace
      - name: step1
        workflowTemplateRef: seqpod-workflowtemplate-sample-workspace
        dependencies: ["step0"]
        workspaces:
          - name: seqpod-workspace
            workspace: dag-workspace
      - name: step2
        workflowTemplateRef: seqpod-workflowtemplate-sample-workspace
        dependencies: ["step1"]
        workspaces:
          - name: seqpod-workspace
            workspace: dag-workspace
```

## 输出结果

WorkflowTemplate 可以在运行过程中输出一些字符串，并最终展示在 WorkflowRun 的 `status` 中。支持 `results` 的 WorkflowTemplate 类型有 SeqPod、DAG。

每个 `result` 本质上是一个文件，如下例所示，您可以向 `$(results.<resultName>.path)` 这个路径写入想要输出的内容。注意写入内容的总和不能超过 4096 字节。

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: seqpod-workflowtemplate-sample-result
spec:
  results:
    - name: my-status
      description: "My status"
  type: SeqPod
  seqPod:
    steps:
      - name: echo
        image: ubuntu
        resources:
          limits:
            cpu: 100m
            memory: 100Mi
        script: |
          echo I am OK > $(results.my-status.path)
```

`results` 更重要的用途是在 DAG WorkflowTemplate 的节点之间传递信息。DAG 的各个节点可以通过 `$(templates.<workflowtemplateName>.results.<resultName>)` 来引用这些 `results`，一般有两种用途：

* DAG 的下层节点可以在 [`params`](#指定参数) 或 [`when`](#条件分支) 字段引用上层节点的 `results`。
* DAG WorkflowTemplate 可以组合节点的 `results` 来输出自身的 `results`。

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: add-workflowtemplate
spec:
  params:
    - name: first
      description: the first operand
    - name: second
      description: the second operand
  results:
    - name: sum
      description: the sum of the first and second operand
  type: SeqPod
  seqPod:
    steps:
      - name: add
        image: ubuntu
        resources:
          limits:
            cpu: 100m
            memory: 100Mi
        env:
          - name: OP1
            value: $(params.first)
          - name: OP2
            value: $(params.second)
        command: ["/bin/sh", "-c"]
        args:
          - echo -n $((${OP1}+${OP2})) | tee $(results.sum.path);
---
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: sum-three-workflowtemplate
spec:
  params:
    - name: first
      description: the first operand
    - name: second
      description: the second operand
    - name: third
      description: the third operand
  type: DAG
  dag:
    templates:
      - name: first-add
        workflowTemplateRef: add-workflowtemplate
        params:
          - name: first
            value: $(params.first)
          - name: second
            value: $(params.second)
      - name: second-add
        workflowTemplateRef: add-workflowtemplate
        params:
          - name: first
            value: $(templates.first-add.results.sum)
          - name: second
            value: $(params.third)
  results:
    - name: total-sum
      description: the sum of all three operands
      value: $(templates.second-add.results.sum)
    - name: partial-sum
      description: the sum of first two operands
      value: $(templates.first-add.results.sum)
```

## 条件分支

在 DAG WorkflowTemplate 中，如果需要在某个条件满足时才执行某个节点，可以设置 `when` 字段。

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: flip-coin
spec:
  results:
    - name: coin
      description: Which side? Heads or tails?
  type: SeqPod
  seqPod:
    steps:
      - name: flip-coin
        image: python
        resources:
          limits:
            cpu: 100m
            memory: 100Mi
        script: |
          #!/usr/bin/env python3
          import random
          f = open("$(results.coin.path)", "w")
          if random.random() > 0.5:
            f.write("heads")
          else:
            f.write("tails")
          f.close()
---
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: dag-workflowtemplate-sample-when
spec:
  type: DAG
  dag:
    templates:
      - name: flip-coin
        workflowTemplateRef: flip-coin
      - name: execute-only-if-heads
        workflowTemplateRef: pod-workflowtemplate-sample
        dependencies: ["flip-coin"]
        when:
          - input: "$(templates.flip-coin.results.coin)"
            operator: in
            values: ["heads"]
```

`when` 字段包含一些表达式：

* `input`：表达式的输入，可以是静态字符串或 [`params`](#指定参数)、[`results`](#输出结果) 等变量。如果未填写，默认为一个空的字符串。
* `operator`：表示 `input` 和 `values` 的关系，可以是 `in` 或者 `notin`。
* `values`：字符串数组，可以是静态字符串或 [`params`](#指定参数)、[`results`](#输出结果) 等变量。

只有当 `when` 字段包含的所有表达式结果都为真时，该节点才会被运行，否则会跳过该节点继续运行其他节点。

如果一个节点的 `when` 表达式中引用了其他节点的 `results` 变量，相当于引入了前者对后者的依赖关系，前者会在后者运行结束后才开始运行。

## 失败处理

对于 Pod/SeqPod/Resource WorkflowTemplate，一个 WorkflowRun 只对应一次运行，即使失败也不会重启。也就是说，一个 WorkflowRun 对应产生的 Pod 的 `spec` 中 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/zh/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy">`restartPolicy`</a> 永远是 `Never`。

对于 DAG WorkflowTemplate，DAG 的每个节点都有可能会失败，我们使用 `retries` 字段来控制节点的重启。

* `retries = 0`（默认选项）表示不重启失败的节点。
* `retries > 0` 表示会重启失败的节点，并用一个正整数来限制最多可重启的次数。

如果 DAG 的某个节点失败并超过了最大可重启次数，该节点将被视为永久失败，并由 `spec.dag.failureStrategy` 决定接下来的行为：

* `failureStrategy = StopAllWorkflowTemplates`（默认选项）表示停止创建任何新的节点。
* `failureStrategy = StopDependentWorkflowTemplates` 表示只停止创建依赖于失败节点的节点，其他分支上的节点正常创建。

注意无论是哪种策略，已开始运行的节点都会等待其运行结束。

在下面的 DAG WorkflowTemplate 示例中，共有两个节点 `a` 和 `b`。

* 如果 `a` 节点运行失败，它最多可以重试 5 次。
* 如果 `b` 节点运行失败，它不能进行重试，直接被认定为失败。
* 如果任意一个节点被认定为失败，整个 DAG WorkflowTemplate 也会被认定为失败，并且由于 `spec.dag.failureStrategy` 字段的值为 `StopAllWorkflowTemplates`，所有未开始运行的节点都不再运行。

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowTemplate
metadata:
  name: dag-workflowtemplate-sample-retries
spec:
  type: DAG
  dag:
    failureStrategy: StopAllWorkflowTemplates
    templates:
      - name: a
        workflowTemplateRef: pod-workflowtemplate-sample
        dependencies: []
        retries: 5
      - name: b
        workflowTemplateRef: pod-workflowtemplate-sample
        dependencies: ["a"]
        retries: 0
```

## 下一步

* 了解 [WorkflowRun](./workflowrun.md)
