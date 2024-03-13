# 日志收集

MLService 支持对 release 和 transformer 服务进行日志收集，具体可以对用户发送的 requests 和服务返回的 response 进行收集。开启日志收集后，系统会为 MLService Pod 添加 container t9k-proxy，container t9k-proxy 会根据用户提供的 URL，将日志数据发送到 HTTP 服务。

## 设置 MLService

用户可以为每个 release 和 transformer 设置日志收集功能：
1. release：通过设置 MLService 的 `spec.releases[*].predictor.logger` 字段来启用 release 的日志收集功能。
2. transformer：通过设置 MLService 的 `spec.transformer.predictor.logger` 字段启用 transformer 的日志收集功能。

用户可以通过日志收集的下列字段，来设置日志收集配置：
* urls：url 数组，系统会将收集到的日志发送到 url 对应的服务。
* mode：表示对哪些内容进行收集记录。可选值是 all, response, request，默认值是 all。
    * all：requests 和 response 都会被收集记录。
    * response：只记录收集 response。
    * request：只记录收集 requests。

## 接收日志

MLService Pod Container t9k-proxy 会使用 HTTP 协议将日志数据发送到用户提供的 URL，HTTP Method 是 POST。

发送的日志数据格式是 <a target="_blank" rel="noopener noreferrer" href="https://cloudevents.io">CloudEvent</a>，下面是一个示例：

```
Context Attributes,
  specversion: 1.0
  type: tensorstack.dev.mlservice.response
  source: torch-mnist-logger-predict-origin
  id: 0009174a-24a8-4603-b098-09c8799950e9
  time: 2021-04-10T00:23:26.080736102Z
  datacontenttype: application/json
Extensions,
  component: predict
  inferenceurl: /v1/models/mnist
  mlservicename: torch-mnist-logger
  namespace: example
  traceparent: 00-6d69e2d3917689ee301610780af06de8-be01c3cfdf8e446e-00
Data,
{
  "0": 1.0,
  "2": 1.3369853835154544e-10,
  "6": 7.10219507987428e-14,
  "5": 5.859705488843112e-14,
  "9": 3.2580891499658536e-15
}
```

在上述示例中：
* type：表明当前 CloudEvent 数据记录 response 内容。
* source：release 名称是 origin（source 命名规则是 `<mlservice-name>-<component>-<release-name>`）
* component：组件是 predict
* inferenceurl：URL path 是 `/v1/models/mnist`
* mlservicename：MLService 的名称是 torch-mnist-logger
* namespace：MLService 所在的 namespace 是 example
* Data：MLService 向用户返回的 response 内容是 {"0": 1.0,"2": 1.3369...}


在 HTTP Request 中：
1. CloudEvent 的 Data 内容存在 Request Body 中
2. CloudEvent 的其他内容存在 Request Header 中

可使用 CloudEvent 库来实现接收日志数据的 HTTP Server，具体实现可参考 <a target="_blank" rel="noopener noreferrer" href="https://github.com/cloudevents/sdk-go/blob/v2.10.0/samples/http/receiver-direct/main.go">CloudEvent Sample</a>。

## 示例

### 部署日志接收服务

我们在集群内部署 <a target="_blank" rel="noopener noreferrer" href="https://github.com/knative/eventing-contrib/blob/v0.18.8/cmd/event_display/main.go">event-display</a> 服务来接受日志：
1. event-display 仅简单地将接收到的 CloudEvents 打印出来；
2. event-display 作为演示的目的。

<aside class="note">
<div class="title">注意</div>

实际生产使用，应当使用合适的 CloudEvent 接收服务。例如，一些云厂商提供的：[阿里云 EventBridge](https://cn.aliyun.com/product/aliware/eventbridge?from_alibabacloud=)、[腾讯云 EventBridge](https://cloud.tencent.com/product/eb) 等。
</aside>

event-display.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
 name: event-display
spec:
 replicas: 1
 selector:
   matchLabels:
     app: event-display
 template:
   metadata:
     labels:
       app: event-display
   spec:
     containers:
       - name: event-display
         image: t9kpublic/knative_event_display:1.0.0
         resources:
           limits:
             cpu: 100m
             memory: 100Mi
---
kind: Service
apiVersion: v1
metadata:
 name: event-display
spec:
 selector:
   app: event-display
 ports:
 - protocol: TCP
   port: 80
   targetPort: 8080
```

部署命令
```bash
kubectl create -f event-display.yaml
```

### 部署 MLService

请按照[使用方法](https://github.com/t9k/tutorial-examples/blob/master/docs/README-zh.md#%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95)准备环境，基于[部署用于生产环境的模型推理服务](https://github.com/t9k/tutorial-examples/tree/master/deployment/mlservice/torch-pvc)示例来部署 MLService logger-example。

首先将 mlservice.yaml 修改为下列内容（event-display 和 MLService 需要部署在同一个 namespace）：
```yaml
apiVersion: tensorstack.dev/v1beta1
kind: MLService
metadata:
 name: logger-example
spec:
 default: origin
 releases:
   - name: origin
     predictor:
       logger:
         mode: all
         resources:
           limits:
             cpu: "1"
             memory: 2Gi
           requests:
             cpu: "0.5"
             memory: 1Gi
         urls:
         - http://event-display
       minReplicas: 1
       model:
         parameters:
           "MODEL_PATH": "mnist=model.mar"
         runtime: t9k-torchserve
         modelUri: pvc://tutorial/tutorial-examples/deployment/mlservice/torch-pvc/
       containersResources:
       - name: user-container
         resources:
           limits:
             cpu: "500m"
             memory: 1Gi
```

然后按照 [README 文档](https://github.com/t9k/tutorial-examples/blob/master/deployment/mlservice/torch-pvc/README.md#%E6%93%8D%E4%BD%9C%E6%AD%A5%E9%AA%A4)的操作步骤进行操作。

### 查看日志

查看 event-display 容器的日志，可看到日志中打印的 CloudEvent 记录了预测请求的详细信息：

```bash
$ k get pod -l app=event-display
NAME                             READY   STATUS    RESTARTS   AGE
event-display-7d8d9f97db-lpgg2   1/1     Running   0          14m


$ k logs event-display-7d8d9f97db-lpgg2 
Context Attributes,
  specversion: 1.0
  type: tensorstack.dev.mlservice.request
  source: logger-example-predict-origin
  id: ff726d6b-7fd8-471e-9ddc-de03b201d882
  time: 2024-02-29T08:07:00.849119273Z
Extensions,
  component: predict
  inferenceurl: /v1/models/mnist:predict
  mlservicename: logger-example
  namespace: demo
Data,
  PNG
IHDWfHIDATxc`X`ˬUvo>C0$ůشi˿_{ ZATI̶_Q%̓*y_:=U9;4ɺpJ^{oG8NIx$!K.w;@@4^0
                                                                                                                                     G$Qp֛q?{4g^B
                                                                                                                                                                      <`Rr330
ztB?IENDB`
☁️  cloudevents.Event
Context Attributes,
  specversion: 1.0
  type: tensorstack.dev.mlservice.response
  source: logger-example-predict-origin
  id: ff726d6b-7fd8-471e-9ddc-de03b201d882
  time: 2024-02-29T08:07:01.468872477Z
Extensions,
  component: predict
  inferenceurl: /v1/models/mnist:predict
  mlservicename: logger-example
  namespace: demo
Data,
  {
  "0": 1.0,
  "2": 1.3369905182969433e-10,
  "6": 7.102208632401436e-14,
  "5": 5.859716330864836e-14,
  "9": 3.2580891499658536e-15
}
```

## 参考
* [1] [CloudEvents](https://cloudevents.io/)
* [2] [event display 源码](https://github.com/knative/eventing-contrib/blob/v0.18.8/cmd/event_display/main.go)