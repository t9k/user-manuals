# 虚拟服务器

虚拟服务器（VirtualServer）在集群中创建一个虚拟机，与容器环境相比：

- 虚拟机提供与物理计算机类似的运行环境，便于一些应用的开发和测试；
- 虚拟机提供更强的隔离，可以限制潜在的安全影响范围。

## 创建虚拟服务器

下面是一个基本的 VirtualServer 配置示例：

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: VirtualServer
metadata:
  name: vs-example
spec:
  resources:
    cpu:
      cores: "1"
    memory: 8Gi
  storage:
    root:
      pvc:
        size: 4Gi
        volumeMode: Filesystem
        accessModes: ["ReadWriteOnce"]
        storageClassName: cephfs-hdd
      source:
        http:
          url: https://cloud-images.ubuntu.com/releases/focal/release/ubuntu-20.04-server-cloudimg-amd64.img
      bus: virtio
    additionalDisks:
      - name: disk-name
        persistentVolumeClaim:
          claimName: pvc-as-disk
        bus: virtio
    filesystems:
      - name: my-filesys
        persistentVolumeClaim:
          claimName: pvc-as-fs
  network:
    tcp: [80, 5901]
    udp: []
    macAddress: ""
    dnsConfig: {}
    dnsPolicy: ClusterFirst
  cloudInit: |-
    #cloud-config
    bootcmd:
    - test "$(lsblk /dev/vdb)" && mkfs.ext4 /dev/vdb
    - mkdir -p /mnt/vdb
    - mkdir -p /mnt/file-sys
    - mount -t virtiofs my-filesys /mnt/file-sys
    mounts:
    - [ "/dev/vdb", "/mnt/vdb", "ext4", "defaults,nofail", "0", "2" ]
```

在该例中：

1. 虚拟机申请使用 1 个 CPU 和 8Gi 内存（由 `spec.resources` 字段指定）。
2. 虚拟机绑定一个 4Gi 的 PVC 作为根磁盘，并在 PVC 中下载 `https://cloud-images.ubuntu.com/releases/focal/release/ubuntu-20.04-server-cloudimg-amd64.img` 系统镜像（由 `spec.storage.root` 字段指定）。
3. 虚拟机声明 PVC `pvc-as-disk` 为磁盘 `/dev/vdb`（由 `spec.storage.additionalDisks` 字段指定，根磁盘为 `/dev/vda`，其他磁盘按顺序命名，但预设名称的方式不完全可靠，建议使用 `serial` 字段确认磁盘，参考 [disk](#disk)），并将该磁盘格式化为 `ext4` 文件系统，挂载到 `/mnt/vdb` 路径（格式化和绑定操作由 `spec.cloudInit` 字段指定）。
4. 虚拟机声明 PVC `pvc-as-fs` 为文件系统 `my-filesys`（由 `spec.storage.filesystems` 字段指定），并将该文件系统挂载到 `/mnt/file-sys` 路径（绑定操作由 `spec.cloudInit` 字段指定）。
5. 虚拟机会暴露 `80` 和 `5901` 两个 TCP 服务端口（由 `spec.network` 字段指定）。

## 虚拟机配置详解

### 资源申请

VirtualServer 支持设置 `spec.resources` 字段来申请 CPU、GPU 和内存三种资源。

```yaml
spec:
  resources:
    gpu:
      type: nvidia.com/GA100_A100_PCIE_40GB
      count: 2
    cpu:
      model: Conroe
      cores: 1
    memory: 10Gi
```

在该例中，虚拟机申请使用 `2` 张 `nvidia.com/GA100_A100_PCIE_40GB` GPU 卡、`1` 个 `Conroe` 型号的 CPU 以及 `10Gi` 的内存。

<aside class="note info">
<div class="title">CPU 型号</div>

CPU 的型号（Model）是 CPU 厂商为了更好地管理自己生产的众多型号的产品，也为了能更好地让消费者对自己家的产品快速地了解而制定的一套产品规则。不同型号的 CPU 支持不同的指令集。

在 `spec.resources.cpu.model` 字段中指定 CPU 的型号，并非要求必须使用该型号的 CPU，而是要求使用的 CPU 所支持的指令集应覆盖该型号 CPU 的所有指令集。在这种情况下，申请到的 CPU 虽然不是该型号 CPU，但在使用时可以模拟成该型号的 CPU。

</aside>

<aside class="note info">
<div class="title">GPU 类型</div>

T9k 平台会在集群中部署一个 Device Plugin，该程序会自动检查节点上的 GPU 型号以及各型号 GPU 数量。

具体哪些 GPU 型号可以使用请咨询管理员。

</aside>

### 数据卷

VirtualServer 支持以 disk 和 filesystem 方式绑定任意数量的数据卷。

#### 绑定方式

##### filesystem

VirtualServer 通过 `spec.storage.filesystems` 字段声明文件系统：

```yaml
spec:
  storage:
    filesystems:
      - name: my-filesys
        persistentVolumeClaim:
          claimName: pvc-as-fs
```

在上述示例中，VirtualServer 将 PVC `pvc-as-fs` 声明为文件系统 `my-filesys`。

但是上面字段值只是声明了文件系统，用户还需要将文件系统挂载到一个路径才可以使用。用户可以用 `spec.cloudInit` 字段来挂载该文件系统：

```yaml
spec:
  cloudInit: |-
    #cloud-config
    bootcmd:
    - mkdir -p /mnt/file-sys
    - mount -t virtiofs my-filesys /mnt/file-sys
```

此外，用户也可以在虚拟机启动后，进入虚拟机手动执行上述挂载命令，此处不再演示。

##### disk

VirtualServer 通过 `spec.storage.additionalDisks` 字段声明磁盘：

```yaml
spec:
  storage:
    additionalDisks:
      - name: disk-name
        persistentVolumeClaim:
          claimName: pvc-as-disk
        bus: virtio
        serial: CVLY623300HK240D
```

在上述示例中:

* VirtualServer 将 PVC `pvc-as-disk` 声明为一个磁盘；
* 该磁盘使用 `virtio` 总线，在虚拟机中可以设置的总线类型包括 `virtio`、`sata`、`scsi` 和 `usb`，不同总线的读写速度、对硬件的依赖不同；
* 序列号为 `CVLY623300HK240D`，如果不设置该字段，则磁盘序列号会随机生成，在重启虚拟机后，序列号会发生改变。序列号有助于确认磁盘，如通过命令 `lsblk --nodeps -no name,serial | grep CVLY623300HK240D | cut -f1 -d' '` 确认上述示例中磁盘的名称。

如果该磁盘是第一次使用，用户还需要将磁盘格式化并挂载到一个路径，可以用 `spec.cloudInit` 字段完成该操作：

```yaml
spec:
  cloudInit: |-
    #cloud-config
    bootcmd:
    - test "$(lsblk /dev/vdb)" && mkfs.ext4 /dev/vdb
    - mkdir -p /mnt/file-sys
    mounts:
    - [ "/dev/vdb", "/mnt/vdb", "ext4", "defaults,nofail", "0", "2" ]
```

此外，用户也可以在虚拟机启动后，进入虚拟机手动执行格式化和挂载操作，此处不再演示。

#### 数据卷类型

##### PersistentVolumeClaim

使用一个 PVC 作为磁盘或文件系统：

```yaml
spec:
  storage:
    filesystems:
      - name: filesys-name
        persistentVolumeClaim:
          claimName: pvc-name
---
spec:
  storage:
    additionalDisks:
      - name: disk-name
        persistentVolumeClaim:
          claimName: pvc-name
        bus: virtio
```

<aside class="note info">
<div class="title">disk vs filesystem</div>

1. filesystem 更灵活，即绑即用，且可以通过其他应用（如 jupyter）直接修改 PVC 中的内容；disk 格式化后，在 PVC 中表现为一个 `disk.img` 文件，用户难以通过其他方式修改该磁盘镜像。
2. disk 和物理机上的磁盘一样，可以执行分盘等操作。
3. PVC 创建时设置了 `storage size`，该字段只表示该 PVC 可使用空间的上限，存储服务器并不会为 PVC 预留这些空间。而 disk 在格式化时，会创建一个 `disk.img` 文件，该文件会尽可能占用所有可用空间。如一个 PVC 的大小为 10Gi，则在存储服务器空间足够的情况下，`disk.img` 的大小就是 10Gi。这会使集群存储空间的利用率较低。

</aside>

##### 临时 PVC

临时 PVC 指的是虚拟机将 PVC 作为只读存储，虚拟机在启动后会在本地维护一个临时镜像，记录用户对 PVC 的写入都会记录在该临时镜像中，而不会实际写入到 PVC 中。如果虚拟机停止或重启，则临时镜像丢失。

```yaml
spec:
  storage:
    filesystems:
      - name: filesys-name
        ephemeral:
          persistentVolumeClaim:
            claimName: pvc-name
---
spec:
  storage:
    additionalDisks:
      - name: disk-name
        ephemeral:
          persistentVolumeClaim:
            claimName: pvc-name
        bus: virtio
```

##### ConfigMap

ConfigMap 也可以作为磁盘或文件系统绑定到虚拟机上：

```yaml
spec:
  storage:
    filesystems:
      - name: config-fs
        configMap:
          name: app-config
  cloudInit: |-
    #cloud-config
    bootcmd:
    - "sudo mkdir /mnt/app-config"
    - "sudo mount -t virtiofs config-fs /mnt/app-config"
---
spec:
  storage:
    additionalDisks:
      - name: disk-name
        configMap:
          name: app-config
        bus: virtio
        serial: CVLY623300HK240D
  cloudInit: |-
    #cloud-config
    bootcmd:
    - "sudo mkdir /mnt/app-config"
    - "sudo mount /dev/$(lsblk --nodeps -no name,serial | grep CVLY623300HK240D | cut -f1 -d' ') /mnt/app-config"
```

与 PVC 不同，以 ConfigMap 作为 disk 绑定给虚拟机时不需要格式化，控制器会自动创建磁盘并将 ConfigMap `data` 中的内容以文件的形式存入磁盘。

用户可以给磁盘设置 `serial` 字段，以便查找磁盘。

##### ServiceAccount

```yaml
spec:
  storage:
    filesystems:
      - name: sa-fs
        serviceAccount:
          serviceAccountName: app-secret
  cloudInit: |-
    #cloud-config
    bootcmd:
    - "sudo mkdir /mnt/app-sa"
    - "sudo mount -t virtiofs sa-fs /mnt/app-sa"
---
spec:
  storage:
    additionalDisks:
      - name: disk-name
        serviceAccount:
          serviceAccountName: serviceaccountdisk
        bus: virtio
        serial: SERVICEACCOUNT12
  cloudInit: |-
    #cloud-config
    bootcmd:
    - "sudo mkdir /mnt/app-sa"
    - "sudo mount /dev/$(lsblk --nodeps -no name,serial | grep SERVICEACCOUNT12 | cut -f1 -d' ') /mnt/app-sa"
```

以 ServiceAccount 作为 disk 绑定给虚拟机时不需要格式化，控制器会自动创建磁盘，并在磁盘中创建 `ca.crt`、`namespace` 和 `token` 三个文件，这些文件中记录着 ServiceAccount 的权限信息。

以 ServiceAccount 作为 filesystem 绑定给虚拟机，控制器也会在挂在路径中创建 `ca.crt`、`namespace` 和 `token` 三个文件，这些文件中记录着 ServiceAccount 的权限信息。

### 网络策略

用户可通过 `spec.network` 字段设置虚拟机的 DNS 策略，暴露虚拟机服务：

```yaml
spec:
  network:
    tcp: [80, 5901]
    udp: []
    macAddress: ""
    dnsConfig: {}
    dnsPolicy: ClusterFirst
```

字段说明：

- `tcp` 和 `udp`：表示虚拟机所要暴露的服务端口。
- `macAddress`：网络接口的 MAC 地址，以便在虚拟机重启前后 MAC 地址保持一致。如果不指定该字段，虚拟机每次重启都会被分配随机 MAC 地址。
- `dnsPolicy`：DNS 策略，默认为 `ClusterFirst`，可选值参考 [DNS Policy](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#pod-s-dns-policy)。
- `dnsConfig`：虚拟机 DNS 配置，参考 [DNS Config](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#pod-dns-config)。

在设置 `spec.network` 字段后，控制器会自动创建一个与虚拟机[同名](#虚拟机名称)的 Service。用户可以通过该 Service 访问虚拟机的上述 TCP/UDP 接口，比如通过以下命令将服务暴露到本地 `8080` 端口：

```bash
kubectl port-forward service/managed-virtualserver-9dda9 8080:80
```

### CloudInit

CloudInit 是 Canonical 公司开发的系统初始化工具，已被许多云服务提供商和 Linux 发行版广泛接受。

用户可通过 `spec.cloudInit` 字段设置 CloudInit 配置来初始化虚拟机环境，包括用户密码、启动命令等：

```yaml
spec:
  cloudInit: |-
    #cloud-config
    user: ubuntu
    password: ubuntu
    chpasswd: { expire: False }
    package_update: true
    package_upgrade: true
    packages: 
    - qemu-guest-agent
    runcmd:
    - [ systemctl, start, qemu-guest-agent ]
    bootcmd:
    - "sudo mkdir /mnt/app-configmap"
    - "sudo mount -t virtiofs configmap-fs /mnt/app-configmap"
    - "sudo mkdir /mnt/app-sa"
    - "sudo mount /dev/$(lsblk --nodeps -no name,serial | grep SERVICEACCOUNT12 | cut -f1 -d' ') /mnt/app-sa"
```

在上述示例中，虚拟机会执行以下初始化操作：

- 创建用户 `ubuntu:ubuntu`（用户名:密码）；
- 更新系统软件包；
- 安装并启动 `qemu-guest-agent` 服务；
- 绑定文件系统 `configmap-fs` 和磁盘（序列号为 `SERVICEACCOUNT12`）。

更多 CloudInit 配置请参考 [Cloud Config](https://cloudinit.readthedocs.io/en/latest/reference/examples.html)。

## 虚拟机运行策略

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: VirtualServer
metadata:
  name: example-vs
spec:
  runStrategy: Always
  ...
status:
  runStrategy: Halted
  ...
```

在上述示例中：

- `spec.runStrategy` 表示 VirtualServer 创建时，使用的运行策略
- `status.runStrategy` 表示当前 VirtualServer 的运行策略。

<aside class="note info">
<div class="title">运行策略说明</div>

- `Always`：当虚拟机处于未运行状态（如刚创建或以任何原因退出），启动虚拟机。
- `RerunOnFailure`：如果用户在虚拟机内主动停止虚拟机，则虚拟机不会重启；如果虚拟机刚创建或以其他非正常方式终止（OOMKILLED、节点崩溃等），则虚拟机启动/重启。
- `Manual`：虚拟机不会自动启动、重启、停止，只能通过 `kubectl virt` 命令控制启动、停止。
- `Halted`：虚拟机停止。

说明：上述提到的`停止`并非删除 VirtualServer，而是删除虚拟机实体，用户仍可以通过[虚拟机操作](#虚拟机操作)一节中提到的方法，重新创建虚拟机实体。

</aside>

用户可以通过[虚拟机操作](#虚拟机操作)切换虚拟机运行策略：

| Run Strategy     | start            | stop     | restart          |
| ---------------- | ---------------- | -------- | ---------------- |
| `Always`         | `-`              | `Halted` | `Always`         |
| `RerunOnFailure` | `RerunOnFailure` | `Halted` | `RerunOnFailure` |
| `Manual`         | `Manual`         | `Manual` | `Manual`         |
| `Halted`         | `Always`         | `-`      | `-`              |

- 第一行后三项为虚拟机操作，分别为启动、停止和重启。
- 最左侧一列为操作前的运行策略，右侧为操作后的运行策略。
- `-` 表示在当前运行策略下，不可执行该操作。

<aside class="note info">
<div class="title">示例</div>

假设 VirtualServer 的 `spec.runStrategy` 为 `Always`：

1. 在创建后，`status.runStrategy` 根据 `spec.runStrategy` 设置为 `Always`，虚拟机启动，且在虚拟机以任何原因退出后，控制器都会尝试重新启动虚拟机。
2. 当执行 `stop` 操作后，根据上表 VirtualServer 的 `status.runStrategy` 变为 `Halted`，根据该策略，虚拟机停止。
3. 再次执行 `start` 操作后，根据上表 VirtualServer 的 `status.runStrategy` 变为 `Always`，根据该策略，虚拟机启动。

</aside>

## 虚拟机操作

用户可以通过 K8s 拓展 API 来操控虚拟机，常见的虚拟机操作方式包括：

- `kubectl virt start $vm_name`：启动虚拟机；
- `kubectl virt stop $vm_name`：停止虚拟机；
- `kubectl virt restart $vm_name`：重启虚拟机；
- `kubectl virt console $vm_name`：连接虚拟机终端。

更多虚拟机操作请通过 `kubectl virt -h` 命令查看。

<aside class="note info">
<div class="title">说明</div>

`vm_name` 为虚拟机名称，获取方式参考[虚拟机名称](#虚拟机名称)。

`kubectl virt` 插件的安装方式参考 [GitHub kubectl-virt-plugin](https://github.com/kubevirt/kubectl-virt-plugin#kubectl-virt-plugin)。

</aside>

## 状态

### 虚拟机名称

为避免资源名称过长，导致创建子资源时失败，VirtualServer 在创建虚拟机时，将名称和 UID 进行哈希编码构成虚拟机名称，并将虚拟机名称记录在 `status.vm.name` 字段中。

```yaml
status:
  vm:
    name: managed-virtualserver-9dda9
```

### 虚拟服务器的状态

`status.conditions` 字段用于描述当前 VirtualServer 的状态，包括以下 4 种类型：

- `DataImported`：VirtualServer 已经创建根磁盘 PVC，并下载好系统镜像。
- `Ready`：虚拟机已经成功启动，这里指的是系统成功启动，但是不考虑 CloudInit 过程。
- `Failure`：虚拟机意外关闭，如节点崩溃、OOMKILLED 等。
- `Paused`：虚拟机暂停，无法使用 CPU 和内存。

在下面的示例中，VirtualServer 成功创建了根磁盘并下载好系统镜像，所以类型为 `DataImported` 的 `condition` 被设为 `True`；VirtualServer 此时被停止（不是暂停），工作负载被删除，所以类型为 `Ready` 的 `condition` 被设为 `False`。

```yaml
status:
  conditions:
    - lastTransitionTime: "2024-03-21T08:26:59Z"
      message: Root disk has been imported successfully.
      reason: Succeeded
      status: "True"
      type: DataImported
    - lastTransitionTime: "2024-03-21T08:35:23Z"
      message: VMI does not exist
      reason: VMINotExists
      status: "False"
      type: Ready
```

### 虚拟服务器的可读状态

`status.printableStatus` 字段是一个易被用户理解的状态字符串，该字段可能为以下取值：

- `Stopped`：虚拟机当前处于停止状态，且不会主动启动。
- `Provisioning`：集群正在为虚拟机准备资源，包括向磁盘中下载数据。
- `Starting`：正在启动虚拟机。
- `Running`：虚拟机处于运行阶段。
- `Paused`：虚拟机被暂停。
- `Stopping`：虚拟机正在停止，包括删除工作负载等步骤。
- `Terminating`：虚拟机正在被删除。
- `CrashLoopBackOff`：虚拟机目前已崩溃，正等待重启。
- `Migrating`：虚拟机正在迁移到另一个主机（目前不支持）。
- `Unknown`：虚拟机状态未知，通常发生在虚拟机所在主机失去连接。
- `FailedUnschedulable`：虚拟机无法被分配，可能的原因包括集群资源不足等。
- `ErrImagePull`：镜像拉取失败，只发生在以 `containerDisk` 作为磁盘的情况下。
- `ImagePullBackOff`：镜像拉取失败后，等待重启，只发生在以 `containerDisk` 作为磁盘的情况下。
