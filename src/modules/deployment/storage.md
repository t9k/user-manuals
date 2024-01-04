# 模型存储

模型部署支持以下两种模型存储模式：

* [S3 形式的对象存储](#S3)
* [通过 PVC 使用的共享文件系统](#pvc)

## S3

S3 是一种对象存储服务和协议，具有良好的可扩展性、数据可用性和安全性等优点，其协议被多种商业和开源产品支持，并且被广泛部署。

在模型部署中使用 S3 存储模式需要提供[模型路径](#模型路径)和 [S3 配置](#s3-配置)。

### 模型路径

S3 的模型存储路径必需包含前缀 `s3://`，例如 `s3://models/mnist/`。在 MLService 和 SimpleMLService 的 YAML 配置文件中通过如下字段设置模型存储路径：

* MLService：`spec.releases[*].predictor.model.modelUri`
* SimpleMLService：`spec.<framework>.modelUri`

### S3 配置

S3 的配置信息存储在含有标签 `tensorstack.dev/resource: s3` 的 Secret 中，设置方式如下：

* MLService：`spec.releases[*].predictor.storage.s3Storage.secretName` 指定存储 S3 配置的 Secret 的名称。
* SimpleMLService：`spec.storage.s3Storage.secretName` 指定存储 S3 配置的 Secret 的名称。

Secret 存储的 S3 配置格式是 [s3cmd](https://s3tools.org/s3cmd) 配置文件格式（YAML 配置文件见[部署示例](#s3-部署示例)）。

### S3 部署示例

下面是一个 `MLService` 将存储在 S3 中的模型部署为推理服务的示例，其中模型在 S3 中的存储路径为 `s3://models/example/`，S3 的配置信息存储在 Secret `s3-security` 中。

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: MLService
metadata:
  name: s3-test
spec:
  default: test1
  releases:
    - name: test1
      predictor:
        model:
          modelFormat:
            name: tensorflow
          modelUri: "s3://models/example/"
        storage:
          s3Storage:
            secretName: s3-security
---
apiVersion: v1
kind: Secret
metadata:
  name: s3-security
  labels:
    tensorstack.dev/resource: s3
type: Opaque
data:
# echo "host_base = example.s3
# host_bucket = example.s3
# bucket_location = us-east-1
# use_https = False
# access_key = user
# secret_key = password
# signature_v2 = False" | base64
  .s3cfg: aG9zdF9iYXNlID0gZXhhbXBsZS5zMwpob3N0X2J1Y2tldCA9IGV4YW1wbGUuczMKYnVja2V0X2xvY2F0aW9uID0gdXMtZWFzdC0xCnVzZV9odHRwcyA9IEZhbHNlCmFjY2Vzc19rZXkgPSB1c2VyCnNlY3JldF9rZXkgPSBwYXNzd29yZApzaWduYXR1cmVfdjIgPSBGYWxzZQo=
```

## PVC

模型部署服务也支持直接使用持久卷申领（Persistent Volume Claim）中的模型。

### 模型路径

模型管理服务的模型存储路径必须包含前缀 `pvc://`，前缀后面接着是 PVC 的名称。例如 `pvc://tutorial/models/example` 代表这个模型在 PVC `tutorial` 的路径 `models/example` 下。在 MLService 和 SimpleMLService 的 YAML 配置文件中通过如下字段设置模型存储路径：

* MLService：`spec.releases[*].predictor.model.modelUri`
* SimpleMLService：`spec.<framework>.modelUri`

### PVC 部署示例

下面是一个 `MLService` 将存储在 PVC 中的模型部署为推理服务的示例，其中模型存储在 pvc `tutorial` 的 `models/example/` 路径下。

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: MLService
metadata:
  name: pvc-test
spec:
  default: test1
  releases:
    - name: test1
      predictor:
        model:
          modelFormat:
            name: tensorflow
          modelUri: "pvc://tutorial/models/example"
```