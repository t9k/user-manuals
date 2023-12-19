# 标准镜像

部分 CRD，如 Notebook、T9k Job 和 MLService，需要 Docker 镜像来提供模型开发、训练或推理所需的具体运行环境。平台提供并维护了一系列镜像以满足您的基本使用需求，这些镜像被称为标准镜像。

您也可以[构建自定义镜像]()，以满足更加特定的需求。

## Notebook 标准镜像列表

每个 Notebook 标准镜像包含特定的机器学习框架，同时预装了一些 Python 包、命令行工具和最新版本的[平台工具](../../tool/index.md)。

当前正在维护的 Notebook 标准镜像如下表所示：

| 名称                           | 环境                       |
| ------------------------------ | -------------------------- |
| tensorflow-2.14.0-notebook-cpu | TensorFlow 2（仅支持 CPU） |
| tensorflow-2.14.0-notebook-gpu | TensorFlow 2（支持 GPU）   |
| torch-2.1.0-notebook           | PyTorch 2，conda           |
| miniconda-22.11.1-notebook     | conda                      |

说明：

1. 您可以在[创建 Notebook](../../guide/develop-and-test-model/create-notebook.md#创建标准的-notebook) 时选择以使用这些镜像，也可以直接从 Docker Hub 的 [t9kpublic:octicons-link-external-16:](https://hub.docker.com/u/t9kpublic) Namespace 下拉取这些镜像以使用。
2. 这些镜像会持续更新，直到相应机器学习框架的小版本更新后被新镜像替代，此时旧镜像会被移除。镜像的标签（tag）是它的版本号，其跟随平台的版本号进行更新；镜像的每一次更新可能包含修复问题、更新包或工具、更新 Notebook 的扩展程序等内容。
3. 标签中包含 `-sudo` 的镜像包含 `sudo` 命令，其中用户（`t9kuser`）的密码为 `tensorstack`。
4. 所有镜像包含以下命令行工具：

| 名称   | 介绍                                                                   |
| ------ | ---------------------------------------------------------------------- |
| curl   | 用于从或向服务器传输数据，支持多种协议。                               |
| git    | 分布式版本控制系统，用于跟踪和协作开发软件项目的源代码。               |
| htop   | 一个交互式的系统监视器，用于实时查看和管理运行中的进程。               |
| rclone | 用于在本地和云存储之间同步、管理文件的命令行程序，支持多种云存储服务。 |
| rsync  | 用于高效同步和传输文件，支持本地和远程文件。                           |
| s3cmd  | 用于管理 Amazon S3 云存储服务。                                        |
| ssh    | 用于安全地远程访问和管理服务器。                                       |
| unzip  | 用于解压缩 ZIP 文件。                                                  |
| vim    | 一款高效、可定制的文本编辑器，常用于编程和文本编辑。                   |
| wget   | 用于从网络上下载文件，支持 HTTP、HTTPS 和 FTP 协议。                   |
| zip    | 用于创建和管理 ZIP 压缩文件。                                          |

## Job 标准镜像列表

## MLService 标准镜像列表

## TensorBoard 标准镜像列表
