# GPU 模式

目前 T9k Scheduler 提供的 GPU 支持情况如下：

* NVIDIA GPU：T9k Scheduler 原生支持，使用方式详见 [NVIDIA GPU](#nvidia-gpu)。
* AMD GPU：第三方支持，详见 <a target="_blank" rel="noopener noreferrer" href="https://github.com/RadeonOpenCompute/k8s-device-plugin">AMD Device Plugin</a>。
* Huawei NPU：第三方支持，详见 <a target="_blank" rel="noopener noreferrer" href="https://github.com/apulis/ascend-device-plugin">Ascend Device Plugin</a>。

## 背景知识

Kubernetes 默认只支持 CPU 和 内存的资源调度分配，不支持 GPU。不过 Kubernetes 提供了一种<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/">扩展机制</a>，通过该机制可以将 GPU 注册为 Kubernetes 扩展资源，然后可供集群进行资源调度分配。

## 节点配置（管理员）

在使用 GPU 之前，管理员需要为装有 GPU 的节点进行一些配置。

### 安装有 NVIDIA GPU 的节点

如果节点安装有 NVIDIA GPU，首先管理员需要在节点上添加标签（label）`sched.tensorstack.dev/accelerator: nvidia-gpu`，然后再为其添加下述的某个标签，表明在该节点上 NVIDIA GPU 的使用模式： 

1. `sched.tensorstack.dev/node-alloc-mode: xgn`：拥有此标签的节点会被 T9k Scheduler 添加 taint `sched.tensorstack.dev/xgn-mode=true:NoSchedule`，防止其他不使用 GPU 的 Pod 被部署在该类型节点上。节点支持如下两种 GPU 使用模式：
    * GPU 独占模式：单个 GPU 被一个容器独自占据，不可以和其他容器共享。
    * 节点独占模式：节点的所有资源（包括 GPU）被一个 Pod 的所有容器占据。
2. `sched.tensorstack.dev/node-alloc-mode: sgn`：拥有此标签的节点支持 GPU 共享模式，单个 GPU 可以被多个容器共享。

<aside class="note info">
<div class="title">什么是 taint</div>

taint（污点）是节点的属性，它使节点能够排斥一类特定的 Pod，详见 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/zh/docs/concepts/scheduling-eviction/taint-and-toleration/">Kubernetes 文档</a>。

</aside>

<aside class="note info">
<div class="title">信息</div>

`xgn` 表示 `exclusive gpu node`，`sgn` 表示 `shared gpu node`。

</aside>

### 安装有 AMD GPU 的节点

如果节点安装有 AMD GPU，推荐管理员在节点上添加标签 `sched.tensorstack.dev/accelerator: amd-gpu`，在部署 <a target="_blank" rel="noopener noreferrer" href="https://github.com/RadeonOpenCompute/k8s-device-plugin">AMD Device Plugin</a> 时，将 nodeSelector 设置为 `sched.tensorstack.dev/accelerator: amd-gpu`。

### 安装有 Huawei NPU 的节点

如果节点安装有 Huawei NPU，推荐管理员在节点上添加标签 `sched.tensorstack.dev/accelerator: huawei-npu`，在部署 <a target="_blank" rel="noopener noreferrer" href="https://github.com/apulis/ascend-device-plugin">Ascend Device Plugin</a> 时，将 nodeSelector 设置为 `sched.tensorstack.dev/accelerator: huawei-npu`。

## NVIDIA GPU

T9k Scheduler 支持三种使用 NVIDIA GPU 的模式，每个模式对应一种扩展资源，扩展资源如下：

  * `tensorstack.dev/nvidia-gpu`：表示单个 GPU 资源，用于 GPU 独占模式。
  * `tensorstack.dev/nvidia-gpu-percent`：表示 GPU 显存百分比，用于 GPU 共享模式。
  * `tensorstack.dev/nvidia-gpu-node`：表示占据节点所有资源（包括 GPU 资源），用于节点独占模式。

### GPU 独占

GPU 独占模式适用于对 GPU 资源需求较多的计算密集型任务，例如小规模的机器学习模型训练。

使用示例如下：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: exclusive-gpu
  labels:
    scheduler.tensorstack.dev/group-name: gpu-usage
spec:
  schedulerName: t9k-scheduler
  containers:
  - image: example.io/example-image:latest
    name: exclusive
    resources:
      limits:
        tensorstack.dev/nvidia-gpu: 2
```

在该 Pod 中，名为 `exclusive` 的容器声明资源请求 `tensorstack.dev/nvidia-gpu: 2`，表明要使用 2 个 NVIDIA GPU。

T9k Scheduler 会将该容器所属的 Pod 调度到 GPU 独占模式的节点上，同时会为该容器设置如下环境变量：

   * `NVIDIA_VISIBLE_DEVICES=id0,id1`：表明该节点上的 GPU `id0`、`id1` 被分配给该容器使用，<a target="_blank" rel="noopener noreferrer" href="https://github.com/NVIDIA/nvidia-docker">nvidia-docker-runtime</a> 负责限制该容器只能使用 GPU `id0`、`id1`。

<aside class="note">
<div class="title">注意</div>

创建 Pod 时无需指定 `spec.tolerations`，T9k Scheduler 会根据资源需求自动添加。

</aside>

### GPU 共享

GPU 共享模式适用于对 GPU 资源需求较少的任务，例如负载较低的模型推理服务、交互式计算任务。

使用示例如下：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: shared-gpu
  labels:
    scheduler.tensorstack.dev/group-name: gpu-usage
spec:
  schedulerName: t9k-scheduler
  containers:
  - image: example.io/example-image:latest
    name: shared
    resources:
      limits:
        tensorstack.dev/nvidia-gpu-percent: 30
      requests:
        cpu: 500m
        memory: 200Mi
```

在该 Pod 中，名为 `shared` 的容器声明资源请求 `tensorstack.dev/nvidia-gpu-percent: 30`，表示需要使用某个 NVIDIA GPU 的 30% 显存。

T9k Scheduler 会将该容器所属的 Pod 调度到 GPU 共享模式的节点上，同时会为该容器设置如下环境变量：

   * `NVIDIA_VISIBLE_DEVICES=i`：表示该节点上的 GPU i 被分配给该容器，<a target="_blank" rel="noopener noreferrer" href="https://github.com/NVIDIA/nvidia-docker">nvidia-docker-runtime</a> 负责限制该容器只能使用 GPU i。
   * `T9K_GPU_PERCENT=x`：表示该容器可用的 GPU 显存占比为 x%（此规则需要用户自己遵守，目前没有硬性限制）。
   * `T9K_GPU_MEMORY=m`：表示该容器可用的 GPU 显存大小为 m MB（此规则需要用户自己遵守，目前没有硬性限制）。

### 节点独占

节点独占模式适用于需要更多资源的大型工作负载，例如大规模数据处理，大规模并行分布式机器学习训练等。节点的所有资源（包括 CPU、内存、GPU）均分配给工作负载使用；同时，工作负载可以进行针对性的优化，充分利用一个物理节点内部的多个 GPU 设备及其拓扑结构。

使用示例如下：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: exlusive-node
  labels:
    scheduler.tensorstack.dev/group-name: gpu-usage
spec:
  schedulerName: t9k-scheduler
  containers:
  - image: nginx
    name: exlusive
    resources:
      limits:
        tensorstack.dev/nvidia-gpu-node: 1
```

在该 Pod 中，名为 `exclusive` 的容器声明资源请求 `tensorstack.dev/nvidia-gpu-node: 1`，表明要独占某个拥有 NVIDIA GPU 的节点的所有资源。

T9k Scheduler 会将该容器所属的 Pod 调度到 GPU 独占模式的节点上，同时会为该容器设置如下环境变量：

   * `NVIDIA_VISIBLE_DEVICES=all`：表明该节点上的所有 GPU 都被分配给该容器使用，<a target="_blank" rel="noopener noreferrer" href="https://github.com/NVIDIA/nvidia-docker">nvidia-docker-runtime</a> 为该容器提供所有的 GPU 资源。 

<aside class="note">
<div class="title">注意</div>

如果使用节点独占模式，一个 Pod 中只能有一个容器声明资源请求 `tensorstack.dev/nvidia-gpu-node: 1`，因为一个 Pod 不可能被分配到多个节点上。

</aside>
