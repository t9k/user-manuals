# 存储

TensorStack 平台支持提供易于配置和管理的高性能网络存储服务，可方便的给各种类型的工作负载，例如 Notebook，T9k Jobs，推理服务等提供持久化存储卷 （Persistent Volumes）服务。

- 支持在集群中使用不同性能等级的存储服务。例如，管理员可设置集群同时提供高性能的 SSD 和海量的 HDD 2 种等级的存储服务；
- 所有 SSD 和 HDD 等级均可创建为 Block Volumes（块存储卷）或 Shared Filesystem Volumes （共享文件系统存储卷）；
- 可随时调整 Volume 大小以增加容量；
- 存储与计算分开管理，并且可以在不同实例和硬件类型之间移动；
- 可通过 UI 或 `kubectl` 轻松管理；
- 支持快照、备份及恢复。

## 存储类型

### Block Storage Volumes（块存储卷）

Block Storage Volumes （块存储卷）可作为高性能虚拟存储盘挂载到各种类型的工作负载上。这些卷被呈现为通用 Block Device (块设备)，操作系统将其视为物理连接存储设备，并且独占使用。

如果集群部署了高性能的 NVMe 的存储节点，并使用了足够快的网络，这种类型的存储卷的性能将会超过本地 SATA 接口的 SSD，并且可以扩展到 PB 级别容量。

### Filesystem Volumes (文件系统卷)

遵守 POSIX 标准的 Filesystem Volumes（文件系统卷）可以挂载到各种工作负载上，以提供原生共享文件系统。

同时，这些卷可以同时附加到多个工作负载实例上，非常适合作在 Notebook、大规模并行计算 Job、推理服务等场景的存储卷。


## 使用

TensorStack 的存储系统支持建立在 Kubernetes 的 Storage API 基础之上，主要通过 API [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) ， [Storage Class](https://kubernetes.io/docs/concepts/storage/storage-classes/) 提供用户接口。

同时，为了支持一些特定场景的使用，TensorStack 提供 CRD [StorageShim](storageshim.md)，[Explorer](explorer.md) 增加了额外的支持。

例 1：获得集群中的存储类型：

```bash
$ kubectl get sc
```

例 2：创建存储请求：

```yaml
# 使用 StorageClass `generic-hdd` 的 Filesystem Volumes (文件系统卷)
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-example
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 100Gi
  storageClassName: generic-hdd
  volumeMode: Filesystem
```

## CRD 资源

存储系统中普通用户相关的 CRD 资源，列表如下：

|              | 来源 | 说明                              |
| ------------ | --------------- | --------------------------------- |
| [PVC](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)          | Kubernetes              | 动态申请集群持久存储；用户可日常创建此 Resource 以申请存储资源    |
| [Storage Class](https://kubernetes.io/docs/concepts/storage/storage-classes/) | Kubernetes              | 指明存储的类别；管理员创建，用户创建 PVC 时引用    |
| [StorageShim](../../references/api-reference/storageshim.md)  | TensorStack             | 对各种存储系统的便捷支持，为用户自动创建 PVC；用户可日常创建此 Resource |
| [Explorer](../../references/api-reference/explorer.md)     | TensorStack             | 文件浏览器，查看和管理 PVC 中的文件       |


## 参考

- API reference [Explorer](../../references/api-reference/explorer.md)
- API reference [StorageShim](../../references/api-reference/storageshim.md)
