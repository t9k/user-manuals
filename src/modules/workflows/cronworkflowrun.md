# CronWorkflowRun

CronWorkflowRun 用于方便地定时执行 [WorkflowRun](./workflowrun.md)，对于创建周期性的、反复重复的任务很有用。

!!! info "什么是 cron"

    <a target="_blank" rel="noopener noreferrer" href="https://en.wikipedia.org/wiki/Cron">cron</a> 是一种书写定时计划的格式，用一个字符串指定何时触发任务的执行，通常由以空格分隔的 5 个部分组成：

    ```bash
    # ┌───────────── minute (0 - 59)
    # │ ┌───────────── hour (0 - 23)
    # │ │ ┌───────────── day of the month (1 - 31)
    # │ │ │ ┌───────────── month (1 - 12)
    # │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
    # │ │ │ │ │                                   7 is also Sunday on some systems)
    # │ │ │ │ │
    # │ │ │ │ │
    # * * * * *
    ```

    例如：

    * `1 0 * * *` 表示在每天的 00:01 执行。
    * `45 23 * * 6` 表示在每个星期六的 23:45 执行。
    * `*/5 1,2,3 * * *` 表示在每天的第 1、2、3 个小时每隔 5 分钟执行一次（即 01:00，01:05，01:10，...，03:55）。

    注意 `*/n` 表示每隔 n 个时间单位执行一次，在某个时间单位多次执行可以用逗号连接（例如 `1,2,3`）。

    为了更方便地创建 cron 表达式，可以使用第三方网页工具，例如 <a target="_blank" rel="noopener noreferrer" href="https://crontab.guru">crontab.guru</a>。


## 创建 CronWorkflowRun

下面的 CronWorkflowRun 示例会每分钟创建一个 WorkflowRun。

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: CronWorkflowRun
metadata:
  name: cronworkflowrun-sample
spec:
  schedule: "*/1 * * * *"
  workflowRun:
    spec:
      workflowTemplateRef: workflowtemplate-sample
```

在该例中：

* `schedule` 字段是一个 cron 格式的字符串，表示每分钟触发一次 WorkflowRun 的运行。
* 所要运行的 WorkflowRun 由 `workflowRun` 字段定义，是一个引用 `workflowtemplate-sample` 的 WorkflowRun。

## 详细配置 CronWorkflowRun

下面是一个经过详细配置的 CronWorkflowRun 示例，与上一节类似，也会每分钟创建一个 WorkflowRun。

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: CronWorkflowRun
metadata:
  name: cronworkflowrun-sample
spec:
  schedule: "*/1 * * * *"
  startingDeadlineSeconds: 30
  concurrencyPolicy: "Allow"
  suspend: true
  successfulRunsHistoryLimit: 10
  failedRunsHistoryLimit: 10
  workflowRun:
    spec:
      workflowTemplateRef: workflowtemplate-sample
```

在该例中：

* 如果某个 WorkflowRun 由于任何原因未能准时在预设的时间点开始执行，它在 30 秒钟的期限内必须开始执行（由 `startingDeadlineSeconds` 字段指定），否则将被认为该次执行已失败。
* 如果到了某个 WorkflowRun 应该开始执行的时间点，但是上一个 WorkflowRun 仍未运行完成，允许这两个 WorkflowRun 同时运行（由 `concurrencyPolicy` 字段指定）。
* `suspend` 字段为 `true` 表示暂时停止创建新的 WorkflowRun，该字段可以随时变化。
* 由该 CronWorkflowRun 创建的所有 WorkflowRun 中，最多保留 10 个运行成功的 WorkflowRun 和 10 个运行失败的 WorkflowRun（分别由 `successfulRunsHistoryLimit` 和 `failedRunsHistoryLimit` 字段指定），多余的运行时间较早的 WorkflowRun 会被删除。

## CronWorkflowRun 状态

下面是 CronWorkflowRun 的状态示例：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: CronWorkflowRun
metadata:
  name: cronworkflowrun-sample
spec:
  schedule: "*/1 * * * *"
  startingDeadlineSeconds: 30
  concurrencyPolicy: "Allow"
  suspend: true
  successfulRunsHistoryLimit: 10
  failedRunsHistoryLimit: 10
  workflowRun:
    spec:
      workflowTemplateRef: workflowtemplate-sample
status:
  active:
  - apiVersion: batch.tensorstack.dev/v1beta1
    kind: WorkflowRun
    name: cronworkflowrun-sample-1631093400
    namespace: t9k-example
    resourceVersion: "220623640"
    uid: 39634803-d8cf-41d4-8a8e-649e0133b11b
  lastScheduleTime: "2021-09-08T09:30:00Z"
  conditions:
  - lastTransitionTime: "2021-09-08T09:23:00Z"
    message: At least one WorkflowRun has started
    status: "True"
    type: HasStarted
  - lastTransitionTime: "2021-09-08T09:30:00Z"
    message: There are running WorkflowRuns
    status: "True"
    type: IsRunning
  - lastTransitionTime: "2021-09-08T09:23:35Z"
    message: There are successful WorkflowRuns
    status: "True"
    type: HasSuccessfulRun
  - lastTransitionTime: "2021-09-08T09:22:08Z"
    message: No failed WorkflowRuns yet
    status: "False"
    type: HasFailedRun
```

该 CronWorkflowRun 的 `status` 字段显示：

* 正在执行中的 WorkflowRun 有一个，其基本信息记录在 `status.active` 字段中。
* 最新的 WorkflowRun 的创建时间是 2021-09-08T09:30:00Z（由 `status.lastScheduleTime` 字段描述）。
* 在由该 CronWorkflowRun 创建的 WorkflowRun 中，已开始过至少一次 WorkflowRun（可能已结束或未结束），有正在运行中的 WorkflowRun，有已成功的 WorkflowRun，没有失败的 WorkflowRun（由 `status.conditions` 字段描述）。
