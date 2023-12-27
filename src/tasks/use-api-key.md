# 使用 API Key

本教程演示几种 API Key 的使用实例。

## 在 TensorStack CLI 中使用 API Key

您可以编辑 `$HOME/.t9k/t9k-config.yaml`，在 `users` 中找到您当前的用户名，在该用户的 `auth-provider` 字段中添加 `apikey: <your-apikey>`。

关于 `$HOME/.t9k/t9k-config.yaml` 的详细使用说明，请参阅[配置文件](../../tool/tensorstack-cli/user-guide.md#配置文件)。

## 使用 API Key 作为凭证向 AIMD 上传数据

您可以在模型训练中使用 API Key 作为凭证向 AIMD 上传数据。

### 通常的模型训练

在通常的模型训练中（不论是单个设备训练还是分布式训练）使用 AIMD 记录训练数据时，您需要在调用 `t9k.aimd` 模块的 `init()` 函数[初始化 Trial]() 时提供 API Key，如下所示：

```python
from t9k import aimd

if __name__ == '__main__':
    ...
    trial = aimd.init(
        server_url='url-of-aimd-server',
        trial_name='torch-mnist',
        folder_path='t9k-example',
        api_key='api-key-of-user')          # 用户的 API Key
    ...
```

### AutoTuneExperiment

为了让 AutoTuneExperiment 能够使用 API Key，您需要创建一个 Secret 来存储 API Key，Secret 的格式如下：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: aimd-secret
  namespace: t9k-example
data:
  apikey: ZDQyMjJjZjUtMmI0Ni00Mjk2LWFiMzYtYWI4NmVhZGUwZjQx  # API Key 的 Base64 编码
type: Opaque
```

在上述 Secret 中，在 `data.apikey` 字段中记录 API Key 的 Base64 编码。然后在 AutoTuneExperiment 的配置中引用这个 Secret，具体方式请参阅 [AutoTuneExperiment 文档](../modules/building/autotune/usage.md)。
