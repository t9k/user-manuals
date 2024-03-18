# 日志收集

MLService 支持对 predictor 和 transformer 服务进行日志收集，包括接收到的 request 和返回的 response 消息。开启日志收集后，系统会为 MLService 添加日志发送能力，其根据配置的接收 URL，将日志发送到 URL 指定的服务。

## 设置 MLService

用户可以为每个 predictor 和 transformer 设置日志收集功能：

1. predictor： MLService 的 `spec.releases[*].predictor.logger` 字段来启用 predictor 的日志收集功能。
2. transformer：通过设置 MLService 的 `spec.transformer.logger` 字段启用 transformer 的日志收集功能。

用户可以通过日志收集的下列字段，来设置日志收集配置：

* `urls`：url 数组，系统会将收集到的日志发送到 url 对应的服务。
* `mode`：表示对哪些内容进行收集记录。可选值是 all, response, request，默认值是 all。
    * all：requests 和 response 都会被收集记录。
    * response：只记录收集 response。
    * request：只记录收集 requests。

## 接收日志

日志数据通过 HTTP 协议被发送（HTTP POST）到用户提供的 URL。

日志数据格式是 <a target="_blank" rel="noopener noreferrer" href="https://cloudevents.io">CloudEvent</a>，如下例所示：

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
* `type`：表明当前 CloudEvent 数据记录 response 内容。
* `source`：release 名称是 origin（source 命名规则是 `<mlservice-name>-<component>-<release-name>`）
* `component`：组件是 predict
* `inferenceurl`：URL path 是 `/v1/models/mnist`
* `mlservicename`：MLService 的名称是 torch-mnist-logger
* `namespace`：MLService 所在的 namespace 是 example
* `Data`：MLService 向用户返回的 response 内容是 {"0": 1.0,"2": 1.3369...}


在 HTTP Request 中：
1. CloudEvent 的 Data 内容存在 Request Body 中
2. CloudEvent 的其他内容存在 Request Header 中

可使用 CloudEvent 库来实现接收日志数据的 HTTP Server，具体实现可参考 <a target="_blank" rel="noopener noreferrer" href="https://github.com/cloudevents/sdk-go/blob/v2.10.0/samples/http/receiver-direct/main.go">CloudEvent Sample</a>。

## 示例

### 部署日志接收服务


<aside class="note">
<div class="title">注意</div>

实际生产使用，应当使用合适的 CloudEvent 接收服务。一些常见的接收服务可查看 <a target="_blank" rel="noopener noreferrer" href="https://cloudevents.io/#:~:text=the%20CloudEvents%20project!-,CloudEvents%20Adopters,-Adobe%20I/O">CloudEvents Adopters</a>。
</aside>


我们在集群内部署 <a target="_blank" rel="noopener noreferrer" href="https://github.com/knative/eventing-contrib/blob/v0.18.8/cmd/event_display/main.go">event-display</a> 服务来接受日志，注意：

1. event-display 仅简单地将接收到的 CloudEvents 打印出来；
2. event-display 作为演示的目的。

<details><summary><code class="hljs">event-display.yaml</code></summary>

```yaml
{{#include ../../assets/modules/deployment/event-display.yaml}}
```

</details>


部署命令
```bash
kubectl create -f event-display.yaml
```

### 部署 MLService

请按照[使用方法](https://github.com/t9k/tutorial-examples/blob/v20240206/docs/README-zh.md#%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95)准备环境，基于[部署用于生产环境的模型推理服务](https://github.com/t9k/tutorial-examples/tree/v20240206/deployment/mlservice/torch-pvc)示例来部署 MLService logger-example。

首先将 mlservice.yaml 修改为下列内容，注意：

1. event-display 和 MLService 需要部署在同一个 namespace/project 中。
2. 这个 MLService 仅对 predictor 设置了 logger 服务。

<details><summary><code class="hljs">mlservice.yaml</code></summary>

```yaml
{{#include ../../assets/modules/deployment/mlservice.yaml}}
```

</details>


然后按照 [README 文档](https://github.com/t9k/tutorial-examples/blob/v20240206/deployment/mlservice/torch-pvc/README.md#%E6%93%8D%E4%BD%9C%E6%AD%A5%E9%AA%A4)的操作步骤进行操作。



### 查看日志

查看 event-display 容器的日志，可看到日志中打印的 CloudEvent 记录了预测请求的详细信息：

<details><summary><code class="hljs">terminal.log</code></summary>

```console
{{#include ../../assets/modules/deployment/terminal.log}}
```

</details>

## 参考

* API 参考：[MLService](../../references/api-reference/mlservice.md)
* <a target="_blank" rel="noopener noreferrer" href="https://cloudevents.io/">CloudEvents </a>
* <a target="_blank" rel="noopener noreferrer" href="https://github.com/knative/eventing-contrib/blob/v0.18.8/cmd/event_display/main.go">event display 源码</a>
