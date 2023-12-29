# 命令

## notebook

针对 TensorStack AI 平台的 Notebook 资源，我们提供了直接通过其 URL 地址获取 SSH 连接方式的功能。使用该命令，您不需要指定名称、命名空间等信息。关于 SSH 连接的详细内容请参阅[通过 SSH 连接远程使用 Notebook](../../tasks/ssh-notebook.md)。

### 使用

``` bash
t9k-pf notebook <url> <localPort>
```

其中 `<url>` 代表地址栏中的地址，`<localPort>` 代表您指定的本地端口号（小于 1024 的本地端口需要管理员权限才可以绑定），如果不指定，会随机使用一个本地端口。

`t9k-pf notebook` 也可以用 `t9k-pf nb` 代替。
    

<aside class="note">
<div class="title">注意</div>

为了方便用户快速连接 SSH，t9k-pf 命令行不支持指定 Notebook 资源的目标端口。如果您有相关需求，可以先获取 Notebook 对应的 Pod 资源，然后参照[访问 Pod ](#pod)来访问特定的目标端口。

</aside>

### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-h, --help              查看当前指令的帮助信息和示例。
-n, --namespace         字符串，指定使用的项目（命名空间）名称。
-k, --apikey            开启交互式输入 API Key。
--address               本地监听地址。默认为 `localhost`。
```

### 示例

通过本地 127.0.0.1 的随机端口访问 Project demo 下 Notebook ml-labs 的 SSH 端口。

``` bash
t9k-pf notebook <tensorstack-host>/t9k/build-console/projects/demo/notebooks/ml-labs/lab
```

通过本地 127.0.0.1:8888 访问 Project demo 下 Notebook ml-labs 的 SSH 端口。

``` bash
t9k-pf nb <tensorstack-host>/t9k/build-console/projects/demo/notebooks/ml-labs/lab 8888
```

通过本地 0.0.0.0:8888 访问 Project demo 下 Notebook ml-labs 的 SSH 端口。

``` bash
t9k-pf nb <tensorstack-host>/t9k/build-console/projects/demo/notebooks/ml-labs/lab 8888 --address 0.0.0.0
```

<aside class="note">
<div class="title">注意</div>

在 port-forward 成功后，您仍然需要保持您的 t9k-pf 命令行窗口一直保持运行状态。

</aside>

## pod

访问指定 Pod 的指定端口。

### 使用

``` bash
t9k-pf pod <name> [<localPort>:]<targetPort>
```

其中 `<localPort>` 代表本地监听的端口（小于 1024 的本地端口需要管理员权限才可以绑定），`<targetPort>` 代表目标 Pod 的端口。

### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-h, --help              查看当前指令的帮助信息和示例。
-n, --namespace         字符串，指定使用的项目（命名空间）名称。
-k, --apikey            开启交互式输入 API Key。
--address               本地监听地址。默认为 `localhost`。
```

### 示例

通过本地 127.0.0.1:3333 访问命名空间 dev 下的 Pod example 的 2222 端口。

``` bash
t9k-pf pod example 3333:2222 -n dev
```

通过本地 0.0.0.0:3333 访问命名空间 dev 下的 Pod example 的 2222 端口。

``` bash
t9k-pf pod example 3333:2222 -n dev --address 0.0.0.0
```

通过本地 127.0.0.1 的随机端口访问命名空间 dev 下的 Pod example 的 2222 端口。

``` bash
t9k-pf pod example 2222 -n dev
```

<aside class="note">
<div class="title">注意</div>

在 port-forward 成功后，您仍然需要保持您的 t9k-pf 命令行窗口一直保持运行状态。

</aside>

## service

访问指定 Service 的指定端口。

### 使用

``` bash
t9k-pf service <name> [<localPort>:]<targetPort>
```

其中 `<localPort>` 代表本地监听的端口（小于 1024 的本地端口需要管理员权限才可以绑定），`<targetPort>` 代表目标 Service 的端口。

`t9k-pf service` 也可以用 `t9k-pf svc` 代替。

### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-h, --help              查看当前指令的帮助信息和示例。
-n, --namespace         字符串，指定使用的项目（命名空间）名称。默认是 `default`。
-k, --apikey            开启交互式输入 API Key。
--address               本地监听地址。默认为 `localhost`。
```

### 示例

通过本地 127.0.0.1:8888 访问默认命名空间 default 下的 Service myservice 的 80 端口。

``` bash
t9k-pf service myservice 8888:80
```

通过本地 0.0.0.0:8888 访问默认命名空间 default 下的 Service myservice 的 80 端口。

``` bash
t9k-pf service myservice 8888:80 --address 0.0.0.0
```

通过本地 127.0.0.1 的随机端口访问命名空间 dev 下的 Service myservice 的 80 端口。

``` bash
t9k-pf service myservice 80 -n dev
```

<aside class="note">
<div class="title">注意</div>

在 port-forward 成功后，您仍然需要保持您的 t9k-pf 命令行窗口一直保持运行状态。

</aside>
