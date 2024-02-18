# Pod

Pod 是可以在 Kubernetes 中创建和管理的、最小的可部署的计算单元。

Pod 是一组（一个或多个）容器；这些容器共享存储、网络、以及怎样运行这些容器的声明。Pod 中的内容总是并置的并且一同调度，在共享的上下文中运行。Pod 模拟一个特定应用的“逻辑主机”，其中包含一个或多个应用容器，这些容器相对紧密地耦合在一起。在非云环境中，在相同的物理机或虚拟机上运行的应用类似于在同一逻辑主机上运行的云应用。

除了应用容器，Pod 还可以包含在 Pod 启动期间运行的 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/workloads/pods/init-containers/">Init 容器</a>。你也可以在集群支持临时性容器的情况下，为调试的目的注入<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/workloads/pods/ephemeral-containers/">临时性容器</a>。

通常你不需要直接创建 Pod，甚至单实例 Pod。你会使用诸如 Deployment 或 Job 这类工作负载资源来创建 Pod。如果 Pod 需要跟踪状态，可以考虑 StatefulSet 资源。

Kubernetes 集群中的 Pod 主要有两种用法：

* 运行单个容器的 Pod：最常见的 Kubernetes 用例； 在这种情况下，可以将 Pod 看作单个容器的包装器，并且 Kubernetes 直接管理 Pod，而不是容器。
* 运行多个协同工作的容器的 Pod：Pod 可能封装由多个紧密耦合且需要共享资源的共处容器组成的应用程序。这些位于同一位置的容器可能形成单个内聚的服务单元 —— 一个容器将文件从共享卷提供给公众，而另一个单独的 sidecar 容器则刷新或更新这些文件。Pod 将这些容器和存储资源打包为一个可管理的实体。

每个 Pod 都旨在运行给定应用程序的单个实例。如果希望横向扩展应用程序（例如，运行多个实例以提供更多的资源），则应该每个实例使用一个 Pod。在 Kubernetes 中，这通常被称为副本。通常使用一种工作负载资源及其控制器来创建和管理一组 Pod 副本。

## Pod 示例

以下是一个 Pod 的 YAML 示例：

```
apiVersion: v1
kind: Pod
metadata:
  name: test-sdk
spec:
  containers:
    - name: sdk
      image: t9kpublic/t9k-sdk:0.6.0-torch-2.0.1
      command:
        - sleep
        - inf
      resources:
        limits:
          cpu: 500m
          memory: 200Mi
```

在上述示例中：

* Pod 使用 `t9kpublic/t9k-sdk:0.6.0-torch-2.0.1`（由 `spec.containers[0].image` 字段指定）镜像启动容器 `sdk`（由 `spec.containers[0].name` 字段指定）。
* 容器中执行 `sleep inf`（由 `spec.containers[0].command` 字段指定）命令。
* `sdk` 容器最多可使用 `0.5` 个 CPU 和 `200Mi` 内存（由 `spec.containers[0].resources.limits` 字段指定）。

## 应用场景

在 TensorStack AI 平台，你可以使用 Pod 实现以下操作：

* 测试镜像：在你使用 ImageBuilder 构建镜像后，可通过创建 Pod 并进入 Pod 终端来验证镜像是否符合预期。
* 存储卷预处理：在训练前，需提前下载好数据，此时可以通过创建 Pod 绑定对应 PVC，在 Pod 终端向其中下载数据。
* 测试代码：你在 Notebook 中开发后的脚本在训练镜像中并不一定能正常运行，可以用训练镜像创建一个 Pod，来测试训练脚本在新镜像中是否可用。

## 下一步

* 了解 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/workloads/pods/">Pod 的概念</a>。
* 了解 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/">Pod 的定义</a>。
