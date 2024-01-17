# ImageBuilder

TensorStack 平台提供 CRD `ImageBuilder`，方便用户在集群中构建容器镜像。

## 创建 ImageBuilder

下面是一个基本的 `ImageBuilder` 定义示例：

```yaml
# image-builder-example.yaml
apiVersion: tensorstack.dev/v1beta1
kind: ImageBuilder
metadata:
  name: imagebuilder-example
spec:
  dockerConfig:
    secret: docker-config
  tag: t9kpublic/kaniko-executor:v1.19.2
  workspace:
    pvc:
      name: kaniko
      dockerfilePath: ./Dockerfile
      contextPath: "."
  builder:
    kaniko: {}
```

在该例中：

* `spec.dockerConfig.secret` 字段指定使用 Secret `docker-config` 中记录的 docker 配置，以上传镜像。
* `spec.tag` 字段指定目标镜像的名称和标签为 `t9kpublic/kaniko-executor:v1.19.2`。
* `spec.workspace` 字段指定构建镜像使用 PVC `kaniko`  作为工作空间，其中：
  * 在 PVC 相对路径 `./Dockerfile` 中存放构建镜像所需的 Dockerfile。
  * 在 PVC 相对路径 `.` 中存放构建镜像所需要的上下文。
* `spec.builder` 字段指定使用 `kaniko` 来构建镜像。

## 构建工具

目前 ImageBuilder 支持使用 <a target="_blank" rel="noopener noreferrer" href="https://github.com/GoogleContainerTools/kaniko">kaniko</a> 工具来构建镜像。

### kaniko

用户可以通过 `spec.builder.kaniko` 字段来设置 kaniko 的参数。

在下面示例中，ImageBuilder 使用 `t9kpublic/kaniko-executor:v1.19.2` 启动 kaniko，并在该容器中构建用户镜像；ImageBuilder 不额外设置 kaniko 参数。

```
spec:
  builder:
    kaniko:
      image: t9kpublic/kaniko-executor:v1.19.2
      args: []
```

`spec.builder.kaniko` 的参数介绍：

* `image`：如忽略，ImageBuilder 控制器会指定一个默认镜像，所以一般来说可以不设置该字段。
* `args`：如忽略，ImageBuilder 构建镜像时执行 `kaniko --destination=[image-tag] --context=[context-path] --dockerfile=[dockerfile-path]` 命令。如果用户需要使用其他参数，可以在该字段中指定。参考 <a target="_blank" rel="noopener noreferrer" href="https://github.com/GoogleContainerTools/kaniko?tab=readme-ov-file#additional-flags">kaniko additional flags</a>。


## 参考

更加详细的 ImageBuilder API 可直接在集群中查询：

```bash
kubectl explain imagebuilder
```

## 下一步

* 使用控制台：[构建镜像](../../tasks/build-image.md)
* Github 上的 <a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/tutorial-examples/tree/master/build-image/build-image-on-platform">ImagerBuilder 示例</a>
* <a target="_blank" rel="noopener noreferrer" href="https://github.com/GoogleContainerTools/kaniko">kaniko 的详细参考</a>
