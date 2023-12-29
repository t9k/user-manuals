# ImageBuilder

TensorStack 平台提供 ImageBuilder，方便用户在集群中构建容器镜像。

## 创建 ImageBuilder

下面是一个基本的 ImageBuilder 配置示例：

```yaml
# notebook-example.yaml
apiVersion: tensorstack.dev/v1beta1
kind: ImageBuilder
metadata:
  name: imagebuilder-sample
spec:
  dockerConfig:
    secret: docker-config
  tag: tsz.io/t9k/kaniko-test:latest
  workspace:
    pvc:
      name: kaniko
      dockerfilePath: ./Dockerfile
      contextPath: "."
  builder:
    kaniko: {}
```

在该例中：

* 使用 `docker-config`（由 `spec.dockerConfig.secret` 字段指定） Secret 中记录的 docker 配置，上传镜像。
* 所要构建镜像的名称和标签为 `tsz.io/t9k/kaniko-test:latest`（由 `spec.tag` 字段指定）。
* 构建镜像使用 `kaniko` PVC 作为工作空间（由 `spec.workspace` 字段指定），其中：
  * 在 PVC 相对路径 `./Dockerfile` 中存放构建镜像所需的 Dockerfile。
  * 在 PVC 相对路径 `.` 中存放构建镜像所需要的上下文。
* 使用 `kaniko` 工具（由 `spec.builder` 字段指定）来构建镜像。

## 构建工具

目前 ImageBuilder 支持使用 <a target="_blank" rel="noopener noreferrer" href="https://github.com/GoogleContainerTools/kaniko">kaniko</a> 工具来构建镜像。

### kaniko

您可以通过 `spec.builder.kaniko` 字段来设置 `kaniko` 工具。

在下面示例中，ImageBuilder 使用 `t9kpublic/kaniko-project-executor:v1.17.0` 镜像启动容器，并在该容器中构建镜像；ImageBuilder 不额外设置 `kaniko` 参数。

```
spec:
  builder:
    kaniko:
      image: t9kpublic/kaniko-project-executor:v1.17.0
      args: []
```

* `image`：在部署 ImageBuilder 控制器时，会指定一个默认镜像，所以一般来说可以不设置该字段。
* `args`：在不指定该参数的情况下，ImageBuilder 构建镜像时执行 `kaniko --destination=[image-tag] --context=[context-path] --dockerfile=[dockerfile-path]` 命令。如果您需要使用其他参数，可以在该字段中指定。参考 <a target="_blank" rel="noopener noreferrer" href="https://github.com/GoogleContainerTools/kaniko?tab=readme-ov-file#additional-flags">kaniko additional flags</a>。
