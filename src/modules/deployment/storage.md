# 模型存储

AI 模型可以存储在集群的[文件系统](../storage/index.md)里，或者 S3 对象存储服务中。

SimpleMLService 和 MLService 采用相同的方式指定模型的存储细节，用户可以明确、方便地指定模型在集群文件系统或者 S3 对象存储服务中的位置，并设置模型在容器中的挂载路径。

## [PVC](../storage/pvc.md)

通过配置 `storage.pvc` 字段可以使用存储在 PVC 中的模型数据。`storage.pvc` 字段包含下列子字段：
* `name`: 存储模型数据的 PVC 的名称。
* `subPath`: 模型在 PVC 中的路径，不可以是绝对路径（即开头不能是 `/`）。
* `mountPath`: 模型在容器中的挂载路径，必须是绝对路径。未设置时，默认值是 `/var/lib/t9k/model`。

示例如下：
```yaml
storage:
  pvc:
    name: demo
    subPath: path/mnist
    mountPath: /var/lib/custom
```

在上述示例中：
* PVC 名称是 `demo`。
* 模型在 PVC 中的路径是 `path/mnist`。
* 模型会被挂载到容器的路径 `/var/lib/custom` 下。


## S3

当使用 S3 服务存储的模型数据时：
* SimpleMLService/MLService 需要先通过 initContainer 下载模型数据到容器本地，然后才能供给推理服务使用。如果下载失败，则推理服务无法启动。
* 当 SimpleMLService/MLService 设置了多个副本时，每个副本都需要单独下载模型数据，副本间无法共享模型数据。


如果用户想使用存储在 S3 服务中的模型数据，需要：
1. 创建存储 S3 服务信息的 Secret
2. 设置 `storage.s3` 字段

### 创建 S3 Secret

存储 S3 信息的 [Secret](../auxiliary/secret.md) 需要满足下列条件：
1. 设置 label `tensorstack.dev/resource: s3`。
2. 设置 `data[.s3cfg]` 字段，内容是 Base64 编码的 <a target="_blank" rel="noopener noreferrer" href="https://s3tools.org/s3cmd">s3cmd</a> config。

YAML 示例如下：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: s3-sample
  labels:
    tensorstack.dev/resource: s3
type: Opaque
data:
  .s3cfg: aG9zdF9iYXNlID0gczMuYXAtZWFzdC0xLmFtYXpvbmF3cy5jb20KaG9zdF9idWNrZXQgPSBleGFtcGxlLnMzLmFwLWVhc3QtMS5hbWF6b25hd3MuY29tCmJ1Y2tldF9sb2NhdGlvbiA9IGFwLWVhc3QtMQp1c2VfaHR0cHMgPSBGYWxzZQphY2Nlc3Nfa2V5ID0gdXNlcgpzZWNyZXRfa2V5ID0gcGFzc3dvcmQKc2lnbmF0dXJlX3YyID0gRmFsc2U=
```

其中 `data[.s3cfg]` 字段 Base64 解码后如下：

```
host_base = s3.ap-east-1.amazonaws.com
host_bucket = example.s3.ap-east-1.amazonaws.com
bucket_location = ap-east-1
use_https = False
access_key = user
secret_key = password
signature_v2 = False
```

### 设置 `storage.s3`

设置 `storage.s3` 字段来使用存储在 S3 中的模型数据。`storage.s3` 字段包含下列子字段: 
* `secretRef`: 记录存储 S3 配置信息的 Secret。该字段有下列子字段：
    * `name`：Secret 名称。
* `uri`: 模型在 S3 中的存储标识。
* `mountPath`: 模型在容器中的挂载路径，必须是绝对路径。未设置时，默认值是 `/var/lib/t9k/model`。

示例如下：
```yaml
storage:
  s3:
    secretRef:
      name: s3-secret
    uri: s3://models/mnist/
    mountPath: /var/lib/custom
```

在上述示例中：
* Secret `s3-secret` 存储着 S3 配置信息。
* 模型在 S3 中的存储标识是 `s3://models/mnist/`。
* 模型会被挂载到容器的路径 `/var/lib/custom` 下。

## 存储类型比较

使用 PVC 存储模型数据：
* 优点：
  * 挂载速度快
  * 多副本可以共享 PVC 数据
* 缺点：
  * 需要提前创建 PVC，并在 PVC 中准备好模型数据

使用 S3 存储模型数据：
* 优点：
  * 只需简单设置，就能 S3 服务存储的模型数据
  * 跨项目共享使用模型很方便
* 缺点：
  * S3 中的模型需要先被下载才能使用，启动时间一般较长
  * 多副本间无法共享模型数据，每个副本都需要从 S3 下载模型数据

## 下一步

* 查看 [MLService 部署示例](../../tasks/deploy-mlservice.md)的模型存储设置
* 查看 [SimpleMLService 部署示例](../../tasks/deploy-simplemlservice.md)的模型存储设置

## 参考

* [S3](https://aws.amazon.com/s3/)
* [s3cmd](https://s3tools.org/s3cmd)
* [PVC](../storage/pvc.md)
* API 参考：[Storage in MLService](../../references/api-reference/mlservice.md#storage)
* API 参考：[Storage in SimpleMLService](../../references/api-reference/simplemlservice.md#storage)
