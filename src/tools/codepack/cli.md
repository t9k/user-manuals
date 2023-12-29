# 命令行工具

Codepack CLI（命令行工具）用于在命令行终端中运行 Codepack。

## 安装

### 前置条件

Codepack CLI 使用 Python 3 编写，在安装之前请确保您的本地环境安装了 3.6 或以上版本的 Python 以及 pip 工具。

为使 Codepack CLI 提供的文件复制功能正常运行，还需要安装 3.1.0 及以上版本的 rsync。macOS 执行以下命令安装：

```shell
brew install rsync
```

基于 Debian 的 Linux 发行版执行以下命令安装：

```shell
apt-get install rsync
```

基于 rpm 的 Linux 发行版执行以下命令安装：

```shell
yum install rsync
```

然后您可以执行以下命令来验证安装完成，并且确认安装的 rsync 版本。

```shell
rsync --version
```

### 安装

目前 TensorStack SDK 仅提供用于本地安装的 Python 包，您可以从平台首页下载。

然后使用以下命令进行安装：

```shell
pip install codepack-<version>.tar.gz [-i <pypi-mirror-url>]
```

## 命令

<aside class="note tip">
<div class="title">提示</div>

执行 `codepack --help` 命令以查看帮助信息，执行 `codepack <subcommand> --help` 命令以查看相应子命令的帮助信息。

</aside>

### check

检查 Codepack 的有效性。

#### 使用

```shell
codepack check [CODEPACK_PATH]

CODEPACK_PATH    Codepack 或 Codepack 定义文件的路径, 默认为当前路径
```

#### 示例

```shell
$ codepack check examples/mnist-keras
Checked, no errors found in codepack mnist-keras
```

### config

查看、修改 Codepack CLI 的配置。

Codepack CLI 各项配置的含义如下：

| 配置项           | 含义                             | 默认值 |
| ---------------- | -------------------------------- | ------ |
| `api_key`        | 用于身份验证的 API Key           | `None` |
| `copy_pod_image` | copy 动词创建的 Pod 所使用的镜像 | `None` |

#### 使用

```shell
$ codepack config [--list] [--get KEY] [--set KEY=VALUE]

--list, -l             列出所有 CLI 配置项
--get=KEY, -g          获取 CLI 配置项
--set=KEY=VALUE, -s    设置 CLI 配置项
```

#### 示例

```shell
$ codepack config --list
api_key=None
copy_pod_image=t9kpublic/sshd-rsync:0.0.0.6

$ codepack config --get api_key
api_key=None

$ codepack config --set api_key=5b398842-7c92-4922-a472-c905553beefd
api_key=5b398842-7c92-4922-a472-c905553beefd
config items set

$ codepack config --get api_key
api_key=5b398842-7c92-4922-a472-c905553beefd
```

### describe

查看 Codepack 的详细信息。

#### 使用

```shell
codepack describe [CODEPACK_PATH]

CODEPACK_PATH    Codepack 或 Codepack 定义文件的路径, 默认为当前路径
```

#### 示例

```shell
$ codepack describe examples/mnist-keras 
name: mnist-keras
description: A simple image classifier based on CNN using tf2.
project: demo
targets:
  - prepare-env
  - copy-file
  - create-notebook
  - run-distributed-training
  - run-e2e-workflow
```

### run

运行 Codepack 的指定 target。

#### 使用

```shell
codepack run [--project PROJECT_NAME] [--target TARGET_NAME] [--verbose] [--wait-timeout INTEGER] [CODEPACK_PATH]

--project=PROJECT_NAME, -p    项目名称, 运行在该项目下
--target=TARGET_NAME, -t      target 名称, 运行该 target
--verbose, -v                 打印更多信息
--wait-timeout=INT, -W        设定以秒为单位的 Pod 超时等待时间
CODEPACK_PATH                 Codepack 或 Codepack 定义文件的路径, 默认为当前路径
```

#### 示例

```shell
$ codepack run examples/mnist-keras -t run-distributed-training -p demo
RUN target run-distributed-training of codepack mnist-keras in project demo
Running sequence: prepare-env -> copy-file -> run-distributed-training

Target 1/3: prepare-env
APPLY by files ['pvc.yaml']
PersistentVolumeClaim with the name codepack-example already exists, skip
Target 2/3: copy-file
COPY from . to codepack-example:.
copied
Target 3/3: run-distributed-training
CREATE by files ['trainingjob.yaml']
TensorFlowTrainingJob codepack-example created
```

## 配置

### 配置文件

Codepack CLI 没有单独的配置文件，而是使用 [TensorStack CLI 的配置文件](../tensorstack-cli/user-guide.md#配置文件)。在执行 `codepack` 命令时，会自动读取位于路径 `~/.t9k/t9k-config.yaml` 的配置文件（如果设置了环境变量 `T9K_CONFIG`，则读取其值给出的路径）。如果配置文件不存在或缺少部分配置项，则缺少的这些配置项会被设置为 `None`，这可能导致 Codepack CLI 的部分功能不能正常工作。

### 扩展配置

配置文件中的 `contexts[*].extension.codepack` 字段是 Codepack CLI 的扩展配置，其包含以下字段：

| 字段             | 功能                          |
| ---------------- | ----------------------------- |
| `copy-pod-image` | 用于复制文件的 Pod 使用的镜像 |

### 查看配置

使用 `codepack config -l` 命令以查看所有配置项的值。

## 身份验证

Codepack CLI 支持下列身份验证方式，您可以选择其中的一种进行相应的配置。

### 平台内运行（incluster）

用户需要在平台资源内（平台所在 Kubernetes 集群的 Pod 内）使用 Codepack CLI，例如在 Notebook 的终端中使用。

注意在运行 target 时只能指定当前项目（不指定则默认为当前项目）。

在此方式下，Codepack CLI 直接利用 Kubernetes 提供给 Pod 的 Service Account 向 kube-apiserver 发送请求以执行各 action。

### kubeconfig 文件

用户需要持有平台所在 Kubernetes 集群的 kubeconfig 文件，并将其放置在路径 `~/.kube/config` 下（如果设置了环境变量 `KUBECONFIG`，则放置在其值给出的路径下）。

在此方式下，Codepack CLI 直接利用 kubeconfig 文件向 kube-apiserver 发送请求以执行各 action。

### t9kconfig 文件

用户持有的[配置文件](#配置文件)需要提供 API Key 或 token。

在此方式下，Codepack CLI 向平台的各服务器发送请求，再由它们向 kube-apiserver 转发请求以执行各 action。
