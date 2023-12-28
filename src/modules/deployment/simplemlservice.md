# SimpleMLService

SimpleMLService 用于在 TensorStack AI 平台上部署机器学习模型预测服务，常用于快速测试。SimpleMLService 具有以下特性：

* 默认支持 TensorFlow、PyTorch 框架，并允许用户自定义框架，具有良好的可扩展性。
* 支持 S3 模型存储方式。
* 支持从集群内部访问服务，集群外访问需要用户自行配置。
* 服务容量固定，不支持自动伸缩。

## 创建 SimpleMLService

下面是一个基本的 SimpleMLService 配置示例：
```yaml
apiVersion: tensorstack.dev/v1beta1
kind: SimpleMLService
metadata:
  name: sample
spec:
  replicas: 1
  storage:
    s3:
      secretName: s3-secret
      uri: s3://models/mnist/
      containerPath: /var/lib/t9k/model
  tensorflow:
    image: t9kpublic/tensorflow-serving:2.6.0
    resources: 
      requests:
        cpu: 1
        memory: 1Gi
```

本示例的 spec 字段的子字段释义如下：
* `replicas`: 定义运行推理服务的副本数量是 1。
* `storage.s3`: 推理服务的模型存储存储在 S3 服务中，子字段的释义如下
    * `secretName`: Secret s3-secret 中存储着 S3 配置信息，Secret 的[内容格式](#创建-s3-secret)。
    * `uri`: 模型在 S3 中的存储路径是 `s3://models/mnist/`。
    * `containerPath`: 模型被下载到容器时，在容器中存储模型的路径是 `/var/lib/t9k/model`。
* `tensorflow`: 推理服务的框架是 tensorflow，子字段释义如下
    * `image`: 使用的推理服务镜像是 `t9kpublic/tensorflow-serving:2.6.0`。
    * `resources`: 定义一个副本 Pod 使用的资源量。

## 默认支持的框架

SimpleMLService 默认支持 TensorFlow、PyTorch 两种框架。

### TensorFlow

可以通过设置 `spec.tensorflow` 字段来部署 TensorFlow 框架，示例可以参考[创建 SimpleMLService](#创建-simplemlservice)。

当使用 TensorFlow 时，控制器会在容器中设置下列启动命令：
```bash
/usr/bin/tensorflow_model_server
--port=9090
--rest_api_port=8080
--model_name=<SimpleMLService name>
--model_base_path=<model-dir-in-container>
```

### PyTorch

可以通过设置 `spec.pytorch` 字段来部署 PyTorch 框架，示例如下：
```yaml
spec:
  pytroch:
    image: <pytorch-image>
    modelsFlag: "resnet-18=resnet-18.mar"
    resources: 
      requests:
        cpu: 1
        memory: 1Gi
```

当使用 PyTorch 时，控制器会在容器中设置下列启动命令：
```bash
torchserve
--start
--model-store=<mode-dir>
--models <models-flag>
```

## 自定义框架

可以通过设置 `spec.custom` 字段来自定义框架，在 `spec.custom.spec` 字段中定义 PodSpec，并需要满足下列要求：
* 至少设置一个 Container。
* 启动推理服务运行命令时，指定正确的模型路径。
* 未设置 [Service](#service) 时，推理服务的服务端口应该被设置为 8080。

示例如下：
```yaml
apiVersion: tensorstack.dev/v1beta1
kind: SimpleMLService
metadata:
  name: pvc-custom
spec:
  replicas: 1
  storage:
    s3:
      secretName: s3-secret
      uri: s3://models/mnist/
      containerPath: /custom/path
  custom:
    spec:
      containers:
      - name: user-container
        args:
        - --port=9000
        - --rest_api_port=8080
        - --model_name=mnist
        - --model_base_path=/custom/path
        command:
        - /usr/bin/tensorflow_model_server
        image: "t9kpublic/tensorflow-serving:2.6.0"
```

## 副本数量

副本数量通过字段 `spec.replicas` 设置，用于定义 SimpleMLService 的 Pods 数量，默认值是 1。

## 暴露副本服务

通过设置 `spec.service` 字段来选择将副本的哪个端口暴露出来，未设置时，默认暴露 8080 端口。

在下面的示例中，暴露端口 7070：
```yaml
spec:
  service:
    ports:
    - name: http
      port: 7070
```

## 调度器

SimpleMLService 支持使用两种调度器：
* <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/#kube-scheduler">Kubernetes 默认调度器</a>
* [T9k Scheduler 调度器](../scheduling/index.md)

通过 `spec.scheduler` 字段可以设置使用哪个调度器：
* 不设置 `spec.scheduler` 字段，默认使用 Kubernetes 调度器
* 设置 `spec.scheduler.t9kScheduler` 字段，使用 T9k Scheduler 调度器

在下面的示例中，SimpleMLService 使用 T9k Scheduler 调度器，并将副本放入 default [队列](../scheduling/queue.md)中进行资源调度。

```yaml
spec:
  scheduler:
    t9kScheduler:
      queue: default
```

## 模型存储

SimpleMLService 默认支持的模型存储是 S3 或 [PVC](../auxiliary/pvc.md)。

### S3

通过下列步骤，可以创建 SimpleMLService 以使用存储在 S3 中的模型：
1. 创建存储 S3 信息的 Secret
2. 设置 SimpleMLService 的 `spec.storage.s3` 字段

#### 创建 S3 Secret

存储 S3 信息的 Secret 需要满足下列条件：
1. 设置 label `tensorstack.dev/resource: s3`。
2. 设置 data[.s3cfg] 字段，内容是 <a target="_blank" rel="noopener noreferrer" href="https://s3tools.org/s3cmd">s3cmd</a> config 的 base64 编码。

S3 Secret 的 YAML 示例如下：
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: s3-sample
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
# signature_v2 = False" | base64 -w 0
  .s3cfg: aG9zdF9iYXNlID0gZXhhbXBsZS5zMwpob3N0X2J1Y2tldCA9IGV4YW1wbGUuczMKYnVja2V0X2xvY2F0aW9uID0gdXMtZWFzdC0xCnVzZV9odHRwcyA9IEZhbHNlCmFjY2Vzc19rZXkgPSB1c2VyCnNlY3JldF9rZXkgPSBwYXNzd29yZApzaWduYXR1cmVfdjIgPSBGYWxzZQo=
```

#### 设置字段

设置 SimpleMLService 的 `spec.storage.s3` 字段来使用存储在 S3 中的模型数据。`spec.storage.s3` 字段包含下列子字段: 
* `secretName`: 存储着 S3 配置信息的 Secret 名称。
* `uri`: 模型在 S3 中的存储路径。
* `containerPath`: 模型在容器中的存储路径。


示例如下：
```yaml
spec:
  storage:
    s3:
      secretName: s3-secret
      uri: s3://models/mnist/
      containerPath: /var/lib/t9k/model
```

### PVC

通过配置 `spec.storage.pvc` 字段可以使用存储在 PVC 中的模型数据。`spec.storage.pvc` 字段包含下列子字段：
* `name`: 存储模型数据的 PVC 的名称
* `subPath`: 模型在 PVC 中的路径，不可以是绝对路径（即开头不能是 `/`）。
* `containerPath`: 模型在容器中的存储路径。

示例如下：
```yaml
spec:
  storage:
    pvc:
      name: demo
      subPath: path/mnist
      containerPath: /var/lib/custom
```

## 状态查询

SimpleMLService 的状态记录在 status 字段中。

`status.address` 字段记录了推理服务在集群内的访问地址，子字段如下：
* `dns`: 推理服务在集群内的访问地址
* `ports`: 推理服务可供访问的服务端口

`status.conditions` 字段记录了当前 SimpleMLService 的状态，包括下列 2 种类型：
* `ModelDownloaded`: 记录模型是否成功地从 S3 下载到容器本地。
* `Ready`: 推理服务是否就绪。 

在下面的示例中：
* 访问推理服务的地址是 `sample.czx.svc.cluster.local`
* 模型已经下载到容器本地
* 推理服务处于就绪状态

```yaml
status:
  address:
    dns: sample.czx.svc.cluster.local
    ports:
    - port: 80
      protocol: TCP
  conditions:
  - lastTransitionTime: "2023-12-27T06:52:39Z"
    status: "True"
    type: ModelDownloaded
  - lastTransitionTime: "2023-12-27T06:52:41Z"
    message: Deployment has minimum availability.
    reason: MinimumReplicasAvailable
    status: "True"
    type: Ready
```
