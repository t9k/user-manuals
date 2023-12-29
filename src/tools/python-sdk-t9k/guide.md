# 用户指南

## 安装

目前 TensorStack SDK 仅提供用于本地安装的 Python 包，您可以从平台首页下载。

然后使用以下命令进行安装：

```shell
pip install t9k-sdk-<version>.tar.gz [-i <pypi-mirror-url>]
```

## 配置

### 配置文件

TensorStack SDK 没有单独的配置文件，而是使用 [TensorStack CLI 的配置文件](../tensorstack-cli/user-guide.md#配置文件)。在导入 `t9k` 模块时，会自动读取位于路径 `~/.t9k/t9k-config.yaml` 的配置文件（如果设置了环境变量 `T9K_CONFIG`，则读取其值给出的路径）。如果配置文件不存在或缺少部分配置项，则缺少的这些配置项会被设置为 `None`，这可能导致 TensorStack SDK 的部分功能不能正常工作。

### 使用和修改配置

在 Python 脚本中导入 `t9k` 模块之后，`t9k.CONFIG` 对象就代表了 TensorStack SDK 的配置，您可以像操作 Python 字典一样操作它，例如获取、设置、更新值。

```python
import t9k

print(t9k.CONFIG['api_key'])
t9k.CONFIG['api_key'] = 'e4ccd2a3-3425-44b0-8b44-148bd303a0f9'
t9k.CONFIG.update({'api_key': 'e4ccd2a3-3425-44b0-8b44-148bd303a0f9'})
```

<aside class="note">
<div class="title">注意</div>

您对于配置的任何修改都只是临时的，这些修改不会被保存到配置文件中。

</aside>

## 命令行工具

TensorStack SDK 提供了两个命令行工具：

* `aimd`：对应于 `t9k.aimd` 模块，用于用户登录和登出 AIMD 服务器（会修改配置文件）、查看和上传当前工作目录下保存的试验和 Artifact 数据。执行 `aimd --help` 和 `aimd COMMAND --help` 以查看相应命令的详细使用方法。
* `ah`：对应于 `t9k.ah` 模块，用于用户登录和登出 Asset Hub 服务器（会修改配置文件），查看、创建、修改和删除资产和资产目录，以及上传、修改和下载资产文件。执行 `ah --help` 和 `ah COMMAND --help` 命令以查看相应命令的详细使用方法。

<!-- 
详细教程
 -->

## 各主题教程

* AI 资产管理相关：请参阅 [AI 资产管理模块的操作指南](../../guide/manage-asset/manipulate-folder-and-asset.md)。
* 实验管理相关：请参阅[记录模型训练数据](../../guide/record-model-training-data/use-experiment-console.md)。
* 模型构建相关：请参阅[使用 AutoTune 进行超参数优化](../../guide/run-hyperparameter-optimization/hpo-with-autotune.md)。
* 模型部署相关：请参阅[制作并部署含有 Transformer 的模型推理服务](../../guide/deploy-model-reference-serving/deploy-mlservice-with-transformer.md)。
