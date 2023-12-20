# Codepack 定义

一个包含机器学习代码及相关文件的文件系统目录，加上 Codepack 的定义文件就构成了一个 Codepack。Codepack 定义文件是一个通常名为 `codepack.yaml` 的 YAML 文件，其包含 Codepack 的版本、名称、描述等基本信息以及 target 定义、action 定义等运行相关的信息。

下面将具体介绍 Codepack 定义文件中的各个字段以及它们的作用，从而指导用户如何创建一个 Codepack。

## 创建 Codepack 定义文件

下面是一个基本的 Codepack 定义文件的示例：

```yaml
apiVersion: codepack.tensorstack.dev/v1beta1
name: mnist-keras
description: A simple image classifier based on CNN using tf2.
targets:
  - name: prepare-env    # target definition
    actions:
      - name: workspace-for-training    # action definition
        verb: apply
        files: [pvc.yaml]
      - name: copy-code
        verb: copy
        src: .
        dst: codepack-pvc:.
```

在该例中：

* 指定 Codepack 的版本、名称和详细描述（分别由 `apiVersion`、`name` 和 `description` 字段指定）。
* `targets` 字段定义一个 target，这个 target 又通过 `actions` 字段定义两个 action。这里 target 的 `name` 字段是必需的；action 的 `name` 字段不是必需的，但 `verb` 字段以及相应动词需要提供的字段是必需的（请参阅 [action 动词](#action-动词)）。

## 指定默认项目和 target

可以通过 `project` 和 `default` 字段指定 Codepack 的默认项目和 target，这样在使用命令行工具运行 Codepack 时如果不提供相应的参数，则会使用这些默认值。

```yaml
apiVersion: codepack.tensorstack.dev/v1beta1
name: mnist-keras
description: A simple image classifier based on CNN using tf2.
project: demo           # default project to run in
default: prepare-env    # default target to run
targets:
  - name: prepare-env
    actions:
      - name: workspace-for-training
        verb: apply
        files: [pvc.yaml]
      - name: copy-code
        verb: copy
        src: .
        dst: codepack-pvc:.
```

## 工作流机制

target 是对 Codepack 的一个具体任务的抽象，多个 target 之间可能存在依赖关系，例如负责从本地复制文件到 PVC 的 target 需要依赖负责创建 PVC 的 target 运行完毕。每一个 target 可以通过 `deps` 字段传入一个 target 名称列表来指定其依赖的其他 target。

在使用命令行工具运行某一个 target 时，命令行工具会递归地解析所有依赖的 target，动态地构建一个有向无环图，然后串行或者并行地运行图中当前没有依赖或依赖已经运行完毕的 target，直到所有 target 全部运行。

利用工作流机制，可以将上面示例中的 target `prepare-env` 拆分为具有依赖关系的两个 target，并且在此基础上再创建一个依赖它们的负责启动分布式训练的 target。

```yaml
apiVersion: codepack.tensorstack.dev/v1beta1
name: mnist-keras
description: A simple image classifier based on CNN using tf2.
project: demo
default: prepare-env
targets:
  - name: prepare-env        # Prepare running env
    actions:
      - name: workspace-for-training
        verb: apply
        files: [pvc.yaml]
  - name: copy-file          # Copy the Codepack to PVC
    deps: ["prepare-env"]
    actions:
      - name: copy-code
        verb: copy
        src: .
        dst: codepack-pvc:.
  - name: run-distributed-training    # Run a distributed training
    deps: ["prepare-env", "copy-file"]
    actions:
      - name: trainingjob
        verb: create
        files: [trainingjob.yaml]
```

<!-- TODO: Implement control logics
## 控制逻辑
 -->

## action 动词

action 的动词通过 `verb` 字段指定，表示其操作类型，目前定义了下列值。

### apply

应用配置到资源，类似于 `kubectl apply`。若同名资源已经存在，则更新其配置，否则创建该资源。

需要提供以下字段：

* `files`：定义资源的 YAML 配置文件的路径、文件路径的列表或者包含 YAML 配置文件的目录的路径。

示例：

```yaml
actions:
  - name: workspace-for-training
    verb: apply
    files: [pvc.yaml]
```

### copy

将文件或目录从源位置复制到目标位置，具体实现取决于源和目标的类型：

1. 若都为本地路径，则直接在本地进行 rsync 操作。
1. 若一个为本地路径，一个为 PVC 路径，则在集群中创建一个挂载这个 PVC 并且运行 sshd 服务的 Pod，在本地进行远程 rsync 操作。
1. 若都为 PVC 路径，则在集群中创建一个挂载这两个 PVC 的 Pod，在 Pod 中进行 rsync 操作。

需要提供以下字段：

* `src`：文件或目录的源位置，可以是本地路径或 PVC 路径，格式如下：

    * 本地路径：
        * `.`（Codepack 的全部文件）
        * `./data`（Codepack 的子目录）
        * `./data/`（Codepack 的子目录下的全部文件）
        * `./train.py`（Codepack 的文件） 

    * PVC 路径：
        * `<pvc-name>:.`（PVC 的根目录）
        * `<pvc-name>:data`（PVC 的子目录）
        * `<pvc-name>:data/`（PVC 的子目录下的全部文件）
        * `<pvc-name>:data/mnist.npz`（PVC 的文件）

* `dst`：文件或目录的目标位置，可以是本地路径或 PVC 路径，格式同上。

示例：

```yaml
actions:
  - name: copy-code
    verb: copy
    src: .
    dst: codepack-pvc:.
```

### create

创建资源，类似于 `kubectl create`。若同名资源已经存在，则错误退出，或为名称添加随机后缀再进行创建。

需要提供以下字段：

* `files`：定义资源的 YAML 配置文件的路径、文件路径的列表或者包含 YAML 配置文件的目录的路径。
* `new`：若为 `True`，并且同名资源已经存在，则为名称添加随机后缀再进行创建；若为 `False` 则错误退出。默认为 True。

示例：

```yaml
actions:
  - name: trainingjob
    verb: create
    files: [trainingjob.yaml]
```
