# 使用 API Key

本教程演示几种 API Key 的使用实例。

## 在 TensorStack CLI 中使用 API Key

您可以使用以下命令并按照提示信息完成 API Key 的录入，随后命令行工具将使用该 API Key 作为用户身份凭证向平台服务器发送请求。

```bash
t9k config auth <server-address> -u <user-name> -k
```

登录操作实质上就是将身份信息记录在 [T9k Config 文件](../tools/cli-t9k/guide.md#配置文件)中作为一个上下文（context），该配置文件中可以同时记录多个上下文，使用以下命令查看、切换和删除：

```bash
# 查看所有上下文
% t9k config get-contexts
CURRENT   NAME            SERVER                     AUTH_TYPE
*         <config-name>   <server-address>           apikey

# 切换所要使用的上下文，即当前上下文
% t9k config use-context <config-name>

# 删除上下文
% t9k config delete-context <config-name>
```

关于 TensorStack CLI 的详细使用说明，请参阅[CLI 用户指南](../tools/cli-t9k/guide.md)。

## 使用 API Key 作为凭证向 AIStore 上传数据

您可以在模型训练中使用 API Key 作为凭证向 AIStore 上传数据。

### 通常的模型训练

<!-- 在通常的模型训练中（不论是单个设备训练还是分布式训练）使用 AIStore 记录训练数据时，您需要在调用 `t9k.em` 模块的 `login()` 函数时提供 API Key，如下所示： -->

在使用 [Python SDK](../tools/python-sdk-t9k/index.md) 将数据上传到 AIStore 中时，您需要调用 `t9k.em` 模块的 `login()` 函数进行身份验证，在不设置 `login()` 函数参数的情况下，SDK 会自动使用 [T9k Config 文件](../tools/cli-t9k/guide.md#配置文件)中当前上下文中的身份信息，如果您想在训练时使用其他身份信息，则可以设置 `ais_host` 和 `api_key` 参数。

```python
from t9k import em

# 使用 T9k Config 中当前上下文中的身份信息
em.login()

# 使用其他身份信息
em.login(ais_host='url-of-em-server', api_key='api-key-of-user')
```

### AutoTuneExperiment

为了让 AutoTuneExperiment 能够使用 API Key，您需要创建一个 Secret 来存储 API Key，Secret 的格式如下：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: aistore-secret
  namespace: t9k-example
data:
  apikey: ZDQyMjJjZjUtMmI0Ni00Mjk2LWFiMzYtYWI4NmVhZGUwZjQx  # API Key 的 Base64 编码
type: Opaque
```

在上述 Secret 中，在 `data.apikey` 字段中记录 API Key 的 Base64 编码。然后在 AutoTuneExperiment 的配置中引用这个 Secret，具体方式请参阅 [AutoTuneExperiment 文档](../modules/building/autotuneexperiment.md#aistore-的使用)。
