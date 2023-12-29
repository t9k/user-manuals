# Notebook

<a target="_blank" rel="noopener noreferrer" href="https://jupyterlab.readthedocs.io/en/latest/">JupyterLab</a> 是一款非常流行的机器学习开发工具，它通过友好易用的 Web 界面提供交互式计算环境，支持多种编程语言和执行环境，在机器学习、AI、数据处理、数值模拟、统计建模、数据可视化等领域被广泛使用。

您可以使用 Notebook 在集群中一键部署 JupyterLab 服务，同时本产品还提供 GPU 支持、SSH 访问支持等补充功能。

## 创建 Notebook

下面是一个基本的 Notebook 配置示例：

```yaml
# notebook-example.yaml
apiVersion: tensorstack.dev/v1beta1
kind: Notebook
metadata:
  name: notebook-sample
spec:
  runMode: running
  template:
    spec:
      containers:
      - image: t9kpublic/tensorflow-2.14.0-notebook-cpu:latest
        name: tensorflow
  type: jupyter
```

在该例中，`template` 字段定义所要创建的 Pod 的规约，指示 Pod 运行一个 `tensorflow` 容器，该容器运行的镜像是 `t9kpublic/tensorflow-2.14.0-notebook-cpu:latest`，这是一个[预先编译好的镜像](#预先编译好的镜像)。

## 预先编译好的镜像

模型构建模块提供了一些预先编译好的镜像，与 JupyterLab 原生镜像相比内置了更丰富的工具包，请参阅 [Notebook 标准镜像列表](../../references/standard-images.md#notebook-标准镜像列表)。

在这些镜像中：

* 默认启动一个 JupyterLab 服务。
* 预装了 Python3 以及 `tensorflow`、`pytorch`、`keras`、`pandas`、`scikit-learn` 等常用 Python 包。
* 身份是一个名为 `t9kuser` 的非 `root` 用户（用户 ID 为 1000，组 ID 为 1000），`$HOME` 目录为 `/t9k/mnt`。
* 预装了 `tensorboard` 插件，您可以在网页中创建 <a target="_blank" rel="noopener noreferrer" href="https://www.tensorflow.org/tensorboard">TensorBoard</a> 以可视化数据。
* 预装了 `notebook2workflow` 插件，您可以在网页中创建 [WorkflowTemplate](../workflows/workflowtemplate.md) 用于在[工作流模块](../workflows/index.md)中运行一个 `.ipynb` 文件。

## 使用 GPU

Notebook 支持通过 [T9k Scheduler](../scheduling/index.md) 进行调度并申请使用一定量的 GPU 资源，例如：

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: Notebook
metadata:
  name: notebook-gpu-sample
spec:
  scheduler:
    t9kScheduler:
      queue: default
  template:
    spec:
      containers:
      - image: t9kpublic/tensorflow-2.11.0-notebook-gpu:latest
        name: gpu
        resources:
          requests:
            cpu: "0.5"
            memory: 1.0Gi
            tensorstack.dev/nvidia-gpu-percent: 30
```

在该例中：

* 所创建的 Pod 使用 T9k Scheduler 作为调度器（通过 `scheduler` 字段指定），并放在名为 default 的[队列](../scheduling/queue.md)中。
* 所创建的 Pod 申请使用 0.5 个 CPU、1Gi 内存以及一个 GPU 的 30% 显存，T9k Scheduler 会将 Pod 调度到某个能提供这些资源的节点上。

## SSH 访问

Notebook 提供运行 SSH Server 的支持。下面的 Notebook 示例运行一个支持 SSH 连接的 JupyterLab 镜像：

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: Notebook
metadata:
  name: notebook-sample
spec:
  ssh:
    authorized_keys:
    - my-public-key
    enabled: true
    serviceType: NodePort
  template:
    spec:
      containers:
      - image: t9kpublic/tensorflow-2.11.0-notebook-cpu:latest
        name: tensorflow
```

在该例中，Notebook 控制器检测到 `spec.ssh.enabled` 字段的值为 `true`，然后创建一个处理 SSH 请求的 Service，其名称前缀为 `managed-notebook-ssh`。Service 的 `targetPort` 为固定的 `2222`，Service 类型通过 `spec.ssh.serviceType` 字段指定为 `NodePort`。

<aside class="note">
<div class="title">注意</div>

Notebook 控制器会为所有 Notebook 创建名称前缀为 `managed-notebook-http` 的 Service，帮助您访问 Juypter Notebook 的服务。而前缀为 `managed-notebook-ssh` 的 Service 只会为 `spec.ssh.enabled` 字段的值为 `true` 的 Notebook 创建。

</aside>

<aside class="note info">
<div class="title">信息</div>

SSH 访问支持允许您直接在本地连接到 Notebook 环境，从而可以使用惯用的本地 IDE 进行开发工作。

</aside>

## 资源回收

Notebook 提供空闲资源回收的支持，在检测到 Notebook 处于空闲状态并超过一定时长时，删除工作负载以释放计算资源。目前，资源回收仅针对 Jupyter 类型的 Notebook，其他类型（例如 RStudio）的 Notebook 不会被回收。

默认情况下（管理员可修改配置）：

* Notebook 没有活跃运行超过 1h 后，标记该 Notebook 为 `Idle`。
* Notebook 进入 `Idle` 状态超过 24h 后，删除该 Notebook 底层工作负载。

如果需要再次使用该 Notebook，您可以在模型构建控制台中手动点击**恢复**按钮。

<aside class="note info">
<div class="title">判定 Notebook 是否活跃</div>

满足以下任一条件即为活跃：

* <a target="_blank" rel="noopener noreferrer" href="https://github.com/jupyter/jupyter/wiki/Jupyter-kernels">Jupyter ipykernel</a> 存在任务运行（即 .ipynb 文件中有代码块在运行）。
* 前端网页存在活动。
* Notebook SSH 存在连接。

</aside>

<aside class="note info">
<div class="title">在不满足上述条件的情况下，保持 Notebook 活跃</div>

* 参考[使用 Jupyter Notebook](../../tasks/develop-and-test-model/use-notebook.md#使用-jupyter-notebook) 创建 `active.ipynb` 文件并执行以下代码块：
  
  ```
  import time

  while True:
      time.sleep(60)
  ```

如果您的任务运行完成，您可以手动停止该代码块的执行，以恢复空闲资源回收的功能。

</aside>
