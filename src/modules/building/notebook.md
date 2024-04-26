# Notebook

<a target="_blank" rel="noopener noreferrer" href="https://jupyterlab.readthedocs.io/en/latest/">JupyterLab</a> 是一款非常流行的机器学习开发工具，它通过友好易用的 Web 界面提供交互式计算环境，支持多种编程语言和执行环境，在机器学习、AI、数据处理、数值模拟、统计建模、数据可视化等领域被广泛使用。

用户可以使用 Notebook CRD 在集群中快速部署一个 JupyterLab 服务，同时本产品还提供 GPU 支持、SSH 访问支持等功能。

<aside class="note info">
<div class="title">信息</div>

除了 Jupyter 系列的 Notebook，用户也可创建其他类型（`spec.type` 指定）的 Notebook，例如 RStudio。

</aside>

## 创建 Notebook

下面是一个基本的 Notebook 配置示例：

```yaml
# notebook-tutorial.yaml
apiVersion: tensorstack.dev/v1beta1
kind: Notebook
metadata:
  name: tutorial
spec:
  type: jupyter
  template:
    spec:
      containers:
        - name: notebook
          image: t9kpublic/torch-2.1.0-notebook:1.77.1
          volumeMounts:
            - name: workingdir
              mountPath: /t9k/mnt
          resources:
            requests:
              cpu: '8'
              memory: 16Gi
              nvidia.com/gpu: 1
            limits:
              cpu: '16'
              memory: 32Gi
              nvidia.com/gpu: 1
      volumes:
        - name: workingdir
          persistentVolumeClaim:
            claimName: tutorial
```

在该例中，`spec.template.spec` 字段定义所要创建的 Pod 的规约：

1. 指示 Pod 运行一个 `notebook` 容器（`spec.template.containers`），该容器运行的镜像是 `t9kpublic/torch-2.1.0-notebook:1.77.1`，这是一个 [Notebook 镜像](#notebook镜像)；
2. 通过 `spec.template.spec.volumes`，`spec.template.containers[].volumeMounts` 指示挂载网络文件系统 PVC `tutorial` 到 `/t9k/mnt`；
3. 通过 `spec.template.spec.containers[].resources` 指定使用的 CPU、memory、GPU 资源 。


## 使用 GPU

Notebook 支持通过申请使用 GPU 资源，例如：

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: Notebook
metadata:
  name: tutorial
spec:
  type: jupyter
  template:
    spec:
      containers:
        - name: notebook
          image: t9kpublic/torch-2.1.0-notebook:1.77.1
          volumeMounts:
            - name: workingdir
              mountPath: /t9k/mnt
          resources:
            limits:
              cpu: '16'
              memory: 32Gi
              nvidia.com/gpu: 1
          command: []
      volumes:
        - name: workingdir
          persistentVolumeClaim:
            claimName: tutorial
```

在该例中：

* 申请使用 16 个 CPU、32Gi 内存以及一个 NVIDIA GPU；系统会自动将 Notebook 调度到集群中某个能提供这些资源的节点上。

## SSH 访问

Notebook 提供运行 SSH Server 的支持。下面的 Notebook 示例运行一个支持 SSH 连接的 JupyterLab 镜像：

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: Notebook
metadata:
  name: tutorial
spec:
  type: jupyter
  template:
    spec:
      containers:
        - name: notebook
          image: t9kpublic/torch-2.1.0-notebook:1.77.1
          volumeMounts:
            - name: workingdir
              mountPath: /t9k/mnt
          resources:
            limits:
              cpu: '16'
              memory: 32Gi
              nvidia.com/gpu: 1
      volumes:
        - name: workingdir
          persistentVolumeClaim:
            claimName: tutorial
  ssh:
    authorized_keys:
      - example-user
    enabled: true
    serviceType: ClusterIP
```

在该例中，用户：

1. 设置 `spec.ssh.enabled` 字段的值为 `true`，T9k 系统将会自动创建一个处理 SSH 请求的 `Service`；
2. 通过 `spec.ssh.serviceType` 字段指定服务类型为 `ClusterIP`；
3. 设置自动挂载存放在 `Secret/example-user` 中的用户 SSH key；

使用此 SSH 服务需要通过 [t9k-pf](../../tools/cli-t9k-pf/index.md) 工具进行端口转发。

<aside class="note">
<div class="title">注意</div>

1. Notebook 控制器会为所有 Notebook 创建名称前缀为 `managed-notebook-http` 的 Service，以支持用户通过 Web 访问 Juypter Notebook 的服务；
2. 而前缀为 `managed-notebook-ssh` 的 Service 只会为 `spec.ssh.enabled` 字段的值为 `true` 的 Notebook 创建。

</aside>

<aside class="note info">
<div class="title">信息</div>

SSH 访问支持允许用户直接在本地连接到 Notebook 环境，从而可以使用惯用的本地 IDE 进行开发工作。

</aside>

## 资源回收

T9k 系统提供空闲 Notebook 资源回收的支持。系统在检测到 Notebook 处于空闲状态并超过一定时长时，就会自动删除工作负载以释放计算资源。目前，资源回收仅针对 Jupyter 类型的 Notebook，其他类型（例如 RStudio）的 Notebook 不会被回收。

管理员可设置回收策略，使得：

* Notebook 没有活跃运行超过 1h（管理员可修改此时长）后，标记该 Notebook 为 `Idle`。
* Notebook 进入 `Idle` 状态超过 24h（管理员可修改此时长）后，删除该 Notebook 底层工作负载。

如果需要再次使用该 Notebook，你可以在模型构建控制台中手动点击**恢复**按钮。

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
  
  ```python
  import time

  while True:
      time.sleep(60)
  ```

如果你的任务运行完成，你可以手动停止该代码块的执行，以恢复空闲资源回收的功能。

</aside>

## Notebook 镜像

T9k 提供了一些预先构建的镜像，与 JupyterLab 原生镜像相比内置了更丰富的工具包，请参阅 [Notebook 标准镜像列表](../../references/standard-images.md#notebook-标准镜像列表)。

在这些镜像中：

* 默认启动一个 JupyterLab 服务。
* 预装了 Python3 以及 `tensorflow`、`pytorch`、`keras`、`pandas`、`scikit-learn` 等常用 Python 包。
* 身份是一个名为 `t9kuser` 的非 `root` 用户（用户 ID 为 1000，组 ID 为 1000），`$HOME` 目录为 `/t9k/mnt`。
* 预装了 `tensorboard` 插件，你可以在网页中创建 <a target="_blank" rel="noopener noreferrer" href="https://www.tensorflow.org/tensorboard">TensorBoard</a> 以可视化数据。

用户也可以自行构建镜像，并上载到镜像 registry 中供使用。


## 常见高级配置

Notebook 底层启动了一个 Pod 来运行 JupyterLab，因此 Pod 相关的配置均可填写到 Notebook 中，详见 [PodSpec](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#PodSpec)。

下面介绍如何填写一些常见的高级配置。

### 环境变量

下面的 Notebook 示例设置了一些环境变量：

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: Notebook
metadata:
  name: tutorial
spec:
  type: jupyter
  template:
    spec:
      containers:
        - name: notebook
          image: t9kpublic/torch-2.1.0-notebook:1.77.1
          env:
            - name: HTTP_PROXY
              value: <host>:<port>
            - name: HTTPS_PROXY
              value: <host>:<port>
            - name: LOCALE
              value: zh-cn
          volumeMounts:
            - name: workingdir
              mountPath: /t9k/mnt
          resources:
            requests:
              cpu: '8'
              memory: 16Gi
              nvidia.com/gpu: 1
            limits:
              cpu: '16'
              memory: 32Gi
              nvidia.com/gpu: 1
      volumes:
        - name: workingdir
          persistentVolumeClaim:
            claimName: tutorial
```

在该例中，`spec.template.spec.containers[*].env` 定义了 Pod 中对应容器的环境变量。环境变量常被用于：

1. 设置网络代理：`HTTP_PROXY` 和 `HTTPS_PROXY`；
2. 设置额外的 Python 包和模块路径：`PYTHONPATH`；
3. 设置 C 语言静态库和共享库路径：`LIBRARY_PATH` 和 `LD_LIBRARY_PATH`；
4. ...

用户可直接在 Notebook 的终端中使用这些环境变量，例如：

```bash
# 自动使用，curl 可以自动使用 HTTPS_PROXY 等环境变量
curl https://ifconfig.io

# 通过命令行参数指定 --proxy 指定环境变量的值
curl --proxy $HTTPS_PROXY https://ifconfig.io
```

用户也可以在 Python 程序中读取并使用这些环境变量，例如：

```python
import os
os.getenv('LOCALE')
```

</aside>

<aside class="note tip">
<div class="title">提示</div>

更多环境变量相关配置，请参考 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/tasks/inject-data-application/">Inject Data Into Applications
</a>。

</aside>


### 共享内存

一些程序的运行可能要求使用共享内存，下面的 Notebook 示例展示了如何设置共享内存：

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: Notebook
metadata:
  name: tutorial
spec:
  type: jupyter
  template:
    spec:
      containers:
        - name: notebook
          image: t9kpublic/torch-2.1.0-notebook:1.77.1
          volumeMounts:
            - name: workingdir
              mountPath: /t9k/mnt
            - name: dshm
              mountPath: /dev/shm
          resources:
            requests:
              cpu: '8'
              memory: 16Gi
              nvidia.com/gpu: 1
            limits:
              cpu: '16'
              memory: 32Gi
              nvidia.com/gpu: 1
      volumes:
        - name: workingdir
          persistentVolumeClaim:
            claimName: tutorial
        - name: dshm
          emptyDir:
            medium: Memory
            sizeLimit: "1Gi"
```

在该例中：

* 在 `spec.template.spec.volumes` 中增加一项，名称为 `dshm`，其中限制共享内存最大为 `1Gi`；
* 在 `spec.template.spec.containers[*].volumeMounts` 中增加一项，将上述 `dshm` 绑定到 `/dev/shm` 路径。


## 设置网络代理

在 Notebook（或者 Job 等其它工作负载）中运行程序时，例如下载训练数据，如果用户需要设置网络代理，可采用如下方式：

### 全局设置

请按照[环境变量](#环境变量)一节为 Notebook（或者 Job 等其它工作负载）设置 `HTTP_PROXY` 和 `HTTPS_PROXY` 两个环境变量（或者其它更多相关变量）。

<aside class="note tip">
<div class="title">提示</div>

设置代理的环境变量并没有严格的统一标准，用户可查看对应命令的手册获得更加准确信息。常见的环境变量如下：

```
# 大写版本
HTTPS_PROXY, HTTP_PROXY, NO_PROXY, ALL_PROXY

# 小写版本
https_proxy, http_proxy, no_proxy, all_proxy
```

</aside>


无论是通过终端运行 curl、wget 等命令或通过 Python 代码来下载训练数据，下载程序一般都会尊重环境变量 `HTTP_PROXY` 和 `HTTPS_PROXY` 的设置，使用这两个环境的值作为网络代理。

### 临时设置

如果仅在运行特定程序时需要使用代理，可通过临时设置环境变量。例如，curl 支持如下方式设置网络代理：

1. 命令行参数

```bash
curl --proxy <proxy-address> https://ifconfig.io
```

2. 环境变量

```bash
# 为单个命令设置环境变量
HTTPS_PROXY=<proxy-address> curl  https://ifconfig.io

# 或者，为当前 shell 及子进程设置
export HTTPS_PROXY=<proxy-address>
curl  https://ifconfig.io
```

### 在程序里设置

很多网络通讯库支持在调用时设置额外的参数，例如 Python 的 request 库，支持如下使用方法：

```python
import requests 

proxies = {
    'http': 'http://1.2.3.4:8080',
    'https': 'https://1.2.3.4:3128'
}

response = requests.get(url, proxies=proxies)
```

## 下一步

用户可尝试如下功能：

* [创建 Notebook](../../tasks/create-notebook.md)
* [使用 Notebook](../../tasks/use-notebook.md)
* [通过 SSH 远程使用 Notebook](../../tasks/ssh-notebook.md)

## 参考

* T9k 提供的 [Notebook 标准镜像列表](../../references/standard-images.md#notebook-标准镜像列表)
* <a target="_blank" rel="noopener noreferrer" href="https://jupyterlab.readthedocs.io/en/stable/">JupyterLab 文档</a>
