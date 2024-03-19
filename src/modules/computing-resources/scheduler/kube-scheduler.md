# kube-scheduler

kube-scheduler 是 Kubernetes 集群的默认调度器，也是平台的默认调度器。在不涉及大规模并行计算的场景下，kube-scheduler 是合适的选择。

下面将介绍 kube-scheduler 的一些常见的特性，这些特性对于 T9k Scheduler 也是适用的。如果想要更全面地了解 kube-scheduler，请参阅官方文档<a target="_blank" rel="noopener noreferrer" href="https://en.wikipedia.org/wiki/Coscheduling">调度、抢占和驱逐</a>。

## 节点选择的约束

在某些情况下，用户可能需要进一步控制 Pod 被放置在哪个节点上运行，例如在训练 LLM 时需要将 Pod 放置在安装有 NVIDIA A100-80GB 的节点上。下面几种方法可以限制 Pod 只能在特定节点上运行，或让 Pod 优先在特定节点上运行。

### nodeSelector

每个节点都有自己的一些标签，例如标签 `kubernetes.io/hostname: kube-01` 标识节点的名称为 kube-01，`nvidia.com/gpu.product: NVIDIA-A100-PCIE-40GB` 标识节点安装了 NVIDIA A100-40GB 型号的 GPU。`nodeSelector` 是 Pod 规约（spec）中的一个字段，用于根据节点标签筛选节点。

下面是一个使用 `nodeSelector` 字段的 Pod 配置示例：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pytorch
spec:
  containers:
  - name: pytorch
    image: pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime
  nodeSelector:
    nvidia.com/gpu.product: NVIDIA-A100-PCIE-40GB
```

在该例中，Pod 只能被调度到安装了 NVIDIA A100-40GB 的节点上。

<aside class="note tip">
<div class="title">提示</div>

对于特定的 API 资源，在 YAML 配置中的哪个位置设置 `nodeSelector` 字段需要参考其 [API 文档]((../../../references/api-reference/index.md))。从中寻找 PodSpec 类型的字段，它拥有 `nodeSelector` 子字段；或从中寻找 PodTemplateSpec 类型的字段，它的 `spec` 子字段拥有 `nodeSelector` 子字段。

</aside>

### nodeName

`nodeName` 也是 Pod 规约中的一个字段，用于直接指定节点的名称，相当于设置 `nodeSelector` 字段为标签 `kubernetes.io/hostname: <NODE_NAME>`。

下面是一个使用 `nodeName` 字段的 Pod 配置示例：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx
  nodeName: kube-01
```

在该例中，Pod 只能被调度到节点 `kube-01` 上。

### 污点

污点（taint）是节点的一种属性，它使得某些类型的 Pod 不能被调度到该节点上。当节点存在出现软硬件故障、网络不可用、磁盘空间不足等问题时，系统会自动为该节点添加一个污点。此外，当管理员发现节点存在问题或正在测试节点时，也可能为该节点添加污点。

当用户的工作负载不能被调度到某个资源充足的节点上时，可能就是因为这个节点被添加了污点。

更多细节请进一步参阅官方文档<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/zh-cn/docs/concepts/scheduling-eviction/taint-and-toleration/">污点和容忍度</a>。

## 优先级和抢占

kube-scheduler 和 T9k Scheduler 都有各自的优先级和抢占机制，我们更推荐通过 T9k Scheduler 来使用这一机制，请参阅 T9k Scheduler 的[优先级和抢占](./t9k-scheduler.md)。

## 参考

* <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/zh-cn/docs/concepts/scheduling-eviction/kube-scheduler/">Kubernetes 调度器</a>
