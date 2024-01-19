# PVC（持久卷）

PVC 是一种 Kubernetes 原生资源，是对存储的需求声明，它抽象了底层存储细节，允许用户请求特定大小和访问模式的存储，而不必关心存储的具体实现。


## 创建 PVC

下面是一个基本的 PVC 配置示例：

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-demo
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
  storageClassName: cephfs-hdd
```

在该例中：

* `spec.resources.requests.storage` 字段定义了所申请的存储空间容量大小为 `1Gi`。
* `spec.accessModes` 字段定义了访问模式为 `ReadWriteMany`，表示该 PVC 能够同时被多个节点上的 Pod 使用。
* `spec.storageClassName` 字段定义了所使用的存储类名称为 `cephfs-hdd`，集群中可用的存储类由管理员提供。

## 使用 PVC

下面是在 Pod 中使用 PVC 的示例：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-demo
spec:
  containers:
  - name: myfrontend
    image: nginx
    volumeMounts:
    - mountPath: "/var/www/html"
      name: data
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: pvc-demo
```

在该例中，`pod-demo` 将 `pvc-demo` 作为一个数据卷（volume）来使用，其中容器 `myfrontend` 将该数据卷挂载到 `/var/www/html` 目录下。

在 TensorStack AI 平台中，PVC 是通用的持久化存储资源，您在 [Notebook](../building/notebook.md)、[Job](../jobs/index.md)、[MLService](../deployment/index.md)、[Workflow](../workflows/index.md) 等 TensorStack 资源中都可以使用 PVC。以 Notebook 为例：

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: Notebook
metadata:
  name: notebook-demo
spec:
  type: jupyter
  template:
    spec:
      containers:
      - image: t9kpublic/torch-2.0.0-notebook:1.72.0
        name: notebook
        resources:
          limits:
            cpu: "4"
            memory: 4Gi
          requests:
            cpu: "0.5"
            memory: 500Mi
        volumeMounts:
        - name: workingdir
          mountPath: /t9k/mnt
      volumes:
      - name: workingdir
        persistentVolumeClaim:
          claimName: pvc-demo
```

在该例中，`notebook-demo` 将 `pvc-demo` 作为一个数据卷（volume）来使用，其中容器 `notebook` 将该数据卷挂载到 `/t9k/mnt` 目录下。


## 生命周期

PVC 有以下几种状态：

* `Pending`：PVC 正在由对应的存储类处理。
* `Bound`：PVC 创建成功，可以被使用。
* `Unknown`：无法获取 PVC 状态。

### PVC 与 Pod

PVC 的生命周期独立于 Pod。一个 PVC 可以被多个 Pod 使用。当 PVC 正在被 Pod 使用时，它无法被删除。

### PVC 与 StorageShim

在 TensorStack AI 平台中，您可以：

1. 创建一个独立的 PVC，申请全新的存储空间。
2. 创建一个 [StorageShim](./storageshim.md)，将已有存储系统的某个子目录挂载为一个 PVC。此时 StorageShim 控制器将为所创建的 StorageShim 创建一个同名的 PVC，此 PVC 的生命周期由 StorageShim 管理。

## 容量请求

创建 PVC 时，`spec.resources.requests.storage` 字段用于指定 PVC 的容量，您无法在 PVC 中存储超过此容量限制的文件。

<aside class="note">
<div class="title">注意</div>

当 PVC 由 StorageShim 管理时，由于具体容量限制由底层存储系统决定，`spec.resources.requests.storage` 字段可能没有意义。

</aside>

## 访问模式

创建 PVC 时，`spec.accessModes` 字段用于指定 PVC 的访问模式，可选择以下几种访问模式：

* `ReadWriteMany`：PVC 能被多个节点上的 Pod 读写。
* `ReadWriteOnce`：PVC 只能被一个节点上的 Pod 读写。
* `ReadOnlyMany`：PVC 只能被多个节点上的 Pod 读。

一般选择 `ReadWriteMany` 即可。

## 存储类

创建 PVC 时，`spec.storageClassName` 字段用于指定 PVC 的存储类，集群中可用的存储类由管理员提供。

例如，一个集群可能提供两个存储类，名为 `cephfs-hdd` 和 `cephfs-ssd`，分别提供基于 HDD 机械硬盘和 SSD 固态硬盘的存储空间，用于不同的数据存储目的。

## 下一步

* 了解 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/storage/persistent-volumes/">PVC 的概念</a>
* 了解 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/kubernetes-api/config-and-storage-resources/persistent-volume-claim-v1/">PVC 的定义</a>
* 如何[上传和下载文件](../../tasks/pvc-importing-and-exporting-files.md)到 PVC