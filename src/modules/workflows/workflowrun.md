# WorkflowRun

WorkflowRun 是 WorkflowTemplate 的一次执行，为 WorkflowTemplate 提供运行时所需的一切资源，例如参数（[`params`](./workflowtemplate.md#指定参数)）、工作空间（[`workspaces`](./workflowtemplate.md#指定工作空间)）。

## 创建引用某个 WorkflowTemplate 的 WorkflowRun

下面的 WorkflowRun 示例为一个 WorkflowTemplate 创建一次运行。

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowRun
metadata:
  name: workflowrun-sample
spec:
  workflowTemplateRef: workflowtemplate-sample
```

在该例中，`workflowTemplateRef` 字段标明所要运行的 WorkflowTemplate 的名称，该 WorkflowTemplate 必须是一个已经创建好的、与该 WorkflowRun 在同一个命名空间的 WorkflowTemplate。

## 创建内嵌 WorkflowTemplate 规约的 WorkflowRun

下面的 WorkflowRun 示例也是为一个 WorkflowTemplate 创建一次运行，但是该 WorkflowTemplate 的规约直接在 WorkflowRun 的规约中填写。

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowRun
metadata:
  name: embedded-workflowrun-sample
spec:
  workflowTemplateSpec:
    type: Pod
    pod:
      containers:
        - name: hello
          image: ubuntu:latest
          command: ["echo"]
          args: ["Hello TensorStack!"]
```

在该例中，`workflowTemplateSpec` 字段用于填写所要运行的 WorkflowTemplate 的规约，WorkflowTemplate 规约的写法详见 [WorkflowTemplateSpec](../../../reference/tensorstack-resources/workflow-api/workflowtemplate.md#workflowTemplateSpec)（坏链）。

## WorkflowRun 状态

在下面的示例中，首先创建一个类型为 DAG 的 WorkflowTemplate，然后创建一个 WorkflowRun 引用该 WorkflowTemplate。

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
      - dependencies:
          - a
        name: b1
        workflowTemplateRef: pod-workflowtemplate-sample
      - dependencies:
          - a
        name: b2
        workflowTemplateRef: pod-workflowtemplate-sample
      - dependencies:
          - b1
          - b2
        name: c
        workflowTemplateRef: pod-workflowtemplate-sample
---
apiVersion: batch.tensorstack.dev/v1beta1
kind: WorkflowRun
metadata:
  labels:
    batch.tensorstack.dev/workflowTemplate: dag-workflowtemplate-sample
  name: dag-workflowtemplate-sample-run
spec:
  serviceAccountName: ''
  workflowTemplateRef: dag-workflowtemplate-sample
status:
  completionTime: '2021-04-16T07:39:05Z'
  conditions:
    - lastTransitionTime: '2021-04-16T07:39:05Z'
      status: 'False'
      type: Running
    - lastTransitionTime: '2021-04-16T07:39:05Z'
      status: 'True'
      type: Completed
  message: All nodes in DAG have succeeded
  nodes:
    a:
      phase: Succeeded
      workflowRunName: dag-workflowtemplate-sample-run-a-pmb2m
    b1:
      phase: Succeeded
      workflowRunName: dag-workflowtemplate-sample-run-b1-mssn6
    b2:
      phase: Succeeded
      workflowRunName: dag-workflowtemplate-sample-run-b2-5db66
    c:
      phase: Succeeded
      workflowRunName: dag-workflowtemplate-sample-run-c-sjpb2
  phase: Succeeded
  startTime: '2021-04-16T07:38:10Z'
  workflowTemplateSpec:
    dag:
      templates:
        - name: a
          workflowTemplateRef: pod-workflowtemplate-sample
        - dependencies:
            - a
          name: b1
          workflowTemplateRef: pod-workflowtemplate-sample
        - dependencies:
            - a
          name: b2
          workflowTemplateRef: pod-workflowtemplate-sample
        - dependencies:
            - b1
            - b2
          name: c
          workflowTemplateRef: pod-workflowtemplate-sample
    type: DAG
```

WorkflowTemplate `dag-workflowtemplate-sample` 有四个节点，分别是：

* `a`
* `b1`
* `b2`
* `c`

WorkflowRun `dag-workflowtemplate-sample-run` 被创建后，WorkflowRun 控制器会为这四个节点创建四个 WorkflowRun，分别是

* `dag-workflowtemplate-sample-run-a-pmb2m`
* `dag-workflowtemplate-sample-run-b1-mssn6`
* `dag-workflowtemplate-sample-run-b2-5db66`
* `dag-workflowtemplate-sample-run-c-sjpb2`

如果这四个 WorkflowRun 均运行成功，WorkflowRun `dag-workflowtemplate-sample-run` 即运行成功。

WorkflowRun `dag-workflowtemplate-sample-run` 的 `status` 字段显示，该 WorkflowRun 处于 `Succeeded` 状态（见 `status.phase` 字段），原因是 “All nodes in DAG have succeeded”（见 `status.message` 字段）。`status.nodes` 字段记录了该 WorkflowRun 中每个 DAG 节点的名称以及对应的 WorkflowRun 名称和状态。

## 下一步

* 学习如何[建立自动化工作流](../../tasks/build-automation-workflow.md)
