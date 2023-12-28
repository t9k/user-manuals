# StorageShim

StorageShim 用于将已有的存储系统以 PVC 的形式提供给用户使用，例如 S3 bucket 的某个子路径可以作为一个 PVC，分布式文件系统的某个子目录可以作为一个 PVC。通过 StorageShim，用户能够方便地访问已经上传到各类存储系统中的数据，而无需进行复制。目前支持的存储系统包括 <a target="_blank" rel="noopener noreferrer" href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html">S3</a> 和 <a target="_blank" rel="noopener noreferrer" href="https://docs.ceph.com/en/quincy/cephfs/">CephFS</a>，未来可能支持更多的存储系统类型。

## 创建 StorageShim

### S3 类型

下面是一个 S3 类型的 StorageShim 配置示例：

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: StorageShim
metadata:
  name: storageshim-s3-demo
spec:
  type: s3
  s3:
    uri: "s3://bucket/path/subpath"
    readOnly: false
    secretRef:
      name: s3-secret-demo
```

其中所引用的 Secret `s3-secret-demo` 配置如下：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: s3-secret-demo
  labels:
    tensorstack.dev/resource: s3-cfg
stringData:
  .s3cfg: <s3cfg>
```

在该例中，StorageShim `storageshim-s3-demo` 被创建后，StorageShim 控制器将创建一个同名的 PVC `storageshim-s3-demo`，该 PVC 的根目录对应 S3 路径 `s3://bucket/path/subpath`，访问该 S3 路径的登录凭证存储在 Secret `s3-secret-demo` 中，该 Secret 必须为 [S3-cfg 类型](./secret.md#secret-用途)。


### CephFS 类型

下面是一个 CephFS 类型的 StorageShim 配置示例：

```yaml
apiVersion: tensorstack.dev/v1beta2
kind: StorageShim
metadata:
  name: storageshim-cephfs-demo
spec:
  type: cephfs
  cephfs:
    path: /cephfs/data/user/mydata
    client:
      secretRef:
        name: ceph-client-key-demo
    server:
      configMapRef:
        name: ceph-cluster-config-demo
```

其中所引用的 Secret `ceph-client-key-demo` 配置示例如下：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ceph-client-key-demo
  labels:
    tensorstack.dev/resource: ceph-client
stringData:
  userID: <user-id>
  userKey: <user-key>
```

其中所引用的 ConfigMap `ceph-cluster-config-demo` 配置示例如下：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ceph-cluster-config-demo
  labels:
    tensorstack.dev/resource: ceph-cluster
data:
  driver: <driver-name>
  clusterID: <cluster-id>
  fsName: <fs-name>
```

在该例中，StorageShim `storageshim-cephfs-demo` 被创建后，StorageShim 控制器将创建一个同名的 PVC `storageshim-cephfs-demo`，该 PVC 的根目录对应 CephFS 文件系统的子目录 `/cephfs/data/user/mydata`，访问该子目录的登录凭证存储在 Secret `ceph-client-key-demo` 中，该 Secret 必须为 [S3-cfg 类型](./secret.md#secret-用途)，该 CephFS 文件系统的相关信息存储在 ConfigMap `ceph-cluster-config-demo` 中。
