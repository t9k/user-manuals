# PVC 快照

如果 [PVC](./pvc.md) 存放了重要的数据，用户可适时制作快照（snapshot），以方便恢复。

## CRD 资源

存储系统中与快照相关的 CRD 资源，列表如下：

|              | 来源 | 说明                              |
| ------------ | --------------- | --------------------------------- |
| [PVC](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)          | Kubernetes              | 动态申请集群持久存储；用户可日常创建此 Resource 以申请存储资源    |
| [Volume Snapshot](https://kubernetes.io/docs/concepts/storage/volume-snapshots/)          | Kubernetes              | 针对某一个 PVC 进行快照；用户可日常创建此 Resource    |
| [Volume Snapshot Class](https://kubernetes.io/docs/concepts/storage/volume-snapshot-classes/) | Kubernetes              | 指明快照的类别，与 StorageClass 一一对应；管理员创建，用户创建 Volume Snapshot 时引用    |


## 创建快照

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

为了对该 PVC 进行快照，用户需要创建如下 VolumeSnapshot 资源：

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: pvc-demo-snapshot
spec:
  volumeSnapshotClassName: cephfs-hdd-snapshotclass
  source:
    persistentVolumeClaimName: pvc-demo
```

其中：

* `spec.volumeSnapshotClassName` 定义了所使用的快照类为 `cephfs-hdd-snapshotclass`，每个 StorageClass 都有对应的 VolumeSnapshotClass，由管理员负责创建；VolumeSnapshot 指定的 `spec.volumeSnapshotClassName` 应当与 PVC 的 `spec.storageClassName` 对应。
* `spec.source.persistentVolumeClaimName` 定义了所要快照的 PVC 名称为 `pvc-demo`。

创建完成后，用户可以对 PVC 中的数据进行继续修改；若需要放弃修改，则可方便地使用快照恢复到修改前的数据。

## 从快照中恢复

如果想将 PVC 中的数据恢复至快照创建时刻的状态，用户需要创建一个新的 PVC（之前的 PVC 仍然可以使用，两个 PVC 之间互不影响）：

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-demo-restore
spec:
  accessModes:
  - ReadWriteMany
  dataSource:
    name: pvc-demo-snapshot
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
  resources:
    requests:
      storage: 1Gi
  storageClassName: cephfs-hdd
```

其中：

* `spec.accessModes` 必须与原 PVC 一致。
* `spec.dataSource` 引用了所要恢复的名为 `pvc-demo-snapshot` 的快照，本 PVC 中的数据将与该快照中的数据完全一致。
* `spec.resources.requests.storage` 必须与原 PVC 一致。
* `spec.storageClassName` 必须与原 PVC 一致。

## 下一步

* 了解 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/storage/volume-snapshots/">VolumeSnapshot 的概念</a>
