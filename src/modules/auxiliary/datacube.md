# DataCube

平台提供 CRD `DataCube`，用于 PVC 和数据存储服务之间的数据传输：

* 下载数据到 PVC。
* 上传数据到 Git、Hugging Face 和 S3 等数据存储服务。

## 创建 DataCube

下面是一个基本的 DataCube 示例：

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: DataCube
metadata:
  name: git-download
spec:
  source:
    type: git
    options:
    - name: url
      value: https://github.com/owner/repo.git
  sink: 
    type: pvc
    pvc:
      name: datacube-pvc
```

在该例中，下载（克隆）Git 仓库（repository）`https://github.com/user/repo.git`（由 `spec.source.options` 字段指定）到 PVC `datacube-pvc`（由 `spec.sink.pvc.name` 字段指定）。

## 下载数据

### 设置 PVC

下载数据到 PVC 时，支持自动创建 PVC 和指定 PVC 子目录：

```yaml
spec:
  sink: 
    type: pvc
    pvc:
      template:
        spec:
          accessModes:
          - ReadWriteMany
          resources:
            requests:
              storage: 100Gi
      name: datacube-pvc
      subPath: dev/git
```

在该例中，声明创建一个存储容量为 100Gi（由 `spec.sink.pvc.template.spec.resources` 字段指定）、可多处读写（由 `spec.sink.pvc.template.spec.accessModes` 字段指定）的 PVC `datacube-pvc`，并将数据下载到该 PVC 的 `dev/git`（由 `spec.sink.pvc.subPath` 字段指定）子目录下。

<aside class="note">
<div class="title">注意</div>

1. 如果该 PVC `datacube-pvc` 已存在，可不填写 `spec.sink.pvc.template`，系统不会重新创建 PVC。
2. 如果该 PVC 子目录 `dev/git` 不存在，系统会自动创建该目录。

</aside>

### 设置源存储服务

#### Git

下载（克隆）一个 Git 仓库到 PVC：

```yaml
spec:
  source:
    type: git
    options:
    - name: token
      valueFrom:
        secretKeyRef:
          name: github-token
          key: token
    - name: url
      value: https://$(TOKEN)@github.com/user/repo.git
    - name: ref
      value: main
```

在该例中，通过 `spec.source.type` 字段指定源存储服务类型为 Git，通过 `spec.source.options` 字段指定源存储服务选项：

* `token`：个人访问令牌（personal access token），使用 Secret `github-token` 的键 `token` 的值，该字段是可选的。
* `url`：Git 仓库路径，以 `$(TOKEN)` 引用的形式嵌入 token。
* `ref`：分支、标签或 commit，下载完成后切换到该 ref。该字段是可选的，默认为 `master`。

#### Hugging Face

下载一个 Hugging Face 仓库（repository）或其中的部分文件到 PVC：

```yaml
spec:
  source:
    type: huggingface
    options:
    - name: token
      valueFrom:
        secretKeyRef:
          name: hf-token
          key: token
    - name: repo
      value: openai/whisper-large-v3
    - name: files
      value: README.md,tokenizer.json,tokenizer_config.json
```

在该例中，通过 `spec.source.type` 字段指定源存储服务类型为 Hugging Face，通过 `spec.source.options` 字段指定源存储服务选项：

* `token`：Hugging Face token，引用 Secret `hf-token` 的键 `token` 的值，该字段是可选的。
* `repo`：Hugging Face 仓库名称。
* `files`：下载的文件列表。该字段是可选的，默认下载仓库的所有文件。

<aside class="note">
<div class="title">注意</div>

* 对于受保护的（gated）仓库，必须指定 `token` 为拥有访问权限的用户的 token。
* 指定 `files` 时，必须通过 `value` 直接设置值，不可以通过 `valueFrom` 间接引用 Secret 或 ConfigMap 的内容。

</aside>

#### S3

下载 S3 的文件或目录到 PVC：

```yaml
spec:
  source:
    type: s3
    options:
    - name: s3-endpoint
      valueFrom:
        secretKeyRef:
          name: s3-config
          key: endpoint
    - name: s3-access-key-id
      valueFrom:
        secretKeyRef:
          name: s3-config
          key: accessKeyID
    - name: s3-secret-access-key
      valueFrom:
        secretKeyRef:
          name: s3-config
          key: secretAccessKey
    - name: s3-uri
      value: s3://bucket/path/subpath
```

在该例中，通过 `spec.source.type` 字段指定源存储服务类型为 S3，通过 `spec.source.options` 字段指定源存储服务选项：

* `s3-endpoint`：S3 端点，引用 Secret `s3-config` 的键 `endpoint` 的值。
* `s3-access-key-id`：S3 服务的 AccessKeyID 凭证，引用 Secret `s3-config` 的键 `accessKeyID` 的值。
* `s3-secret-access-key`：S3 服务的 SecretAccessKey 凭证，引用 Secret `s3-config` 的键 `secretAccessKey` 的值。
* `s3-uri`：S3 文件或目录的路径。

<aside class="note">
<div class="title">注意</div>

指定 `s3-uri` 时，必须通过 `value` 直接设置值，不可以通过 `valueFrom` 间接引用 Secret 或 ConfigMap 的内容。

</aside>

## 上传数据

### 设置 PVC

上传 PVC 数据：

```yaml
spec:
  source:
    type: pvc
    pvc:
      name: datacube-pvc
      subPath: dev/hf/whisper-large-v3
```

在该例中，上传 PVC `datacube-pvc` 的子路径 `dev/hf/whisper-large-v3` 到目标存储服务。

<aside class="note">
<div class="title">注意</div>

1. 如果目标存储服务类型是 Git，子路径必须是一个目录，且待上传的 Git 本地仓库**位于该目录下**（Git 本地仓库**不是该目录本身**）。
2. 如果目标存储服务类型是 Hugging Face 或 S3，子路径可以是一个文件或目录，表示上传该文件或目录到目标存储服务。

</aside>

### 设置目标存储服务

#### Git 

上传 PVC 的一个 Git 仓库到目标数据存储服务：

```yaml
spec:
  source: 
    type: pvc
    pvc:
      name: datacube-pvc
      subPath: dev/git/
  sink:
    type: git
    options:
    - name: token
      valueFrom:
        secretKeyRef:
          name: github-token
          key: token
    - name: url
      value: https://$(TOKEN)@github.com/user/repo.git
```

在该例中，上传 PVC `datacube-pvc` 的 `dev/git/` 路径下的 `repo` 目录（由 `spec.sink.options` 字段指定，其中 `url` 指向的仓库名称即为目录名称），通过 `spec.sink.type` 字段指定目标存储服务类型为 Git，通过 `spec.sink.options` 字段指定目标存储选项：

* `token`：个人访问令牌（personal access token），引用 Secret `github-token` 的键 `token` 的值，该字段是可选的。
* `url`：Git 仓库路径，以 `$(TOKEN)` 引用的形式嵌入 token。

<aside class="note">
<div class="title">注意</div>

上传 Git 仓库实际上是在目标路径下执行 `git push` 命令，其要求用户已经在当前分支提交了 commit。

</aside>

#### Hugging Face

上传 PVC 的文件或目录到 Hugging Face 仓库：

```yaml
spec:
  sink: 
    type: huggingface
    options:
    - name: token
      valueFrom:
        secretKeyRef:
          name: hf-token
          key: token
    - name: repo
      value: user/repo
    - name: path-in-repo
      value: pvc/demo
    - name: commit-message
      value: Upload files from PVC
```

在该例中，通过 `spec.sink.type` 字段指定目标存储服务类型为 Hugging Face，通过 `spec.sink.options` 字段指定目标存储选项：

* `token`：Hugging Face token，引用 Secret `hf-token` 的键 `token` 的值，该字段是可选的。
* `repo`：Hugging Face 仓库名称。
* `path-in-repo`：仓库中的路径，数据将被上传到这里。
* `commit-message`：提交信息，该字段是可选的。

#### S3

上传 PVC 的文件或目录到 S3：

```yaml
spec:
  sink: 
    type: s3
    options:
    - name: s3-endpoint
      valueFrom:
        secretKeyRef:
          name: s3-config
          key: endpoint
    - name: s3-access-key-id
      valueFrom:
        secretKeyRef:
          name: s3-config
          key: accessKeyID
    - name: s3-secret-access-key
      valueFrom:
        secretKeyRef:
          name: s3-config
          key: secretAccessKey
    - name: s3-uri
      value: s3://bucket/path/subpath
    - name: s3-no-check-bucket
      value: "true"
```

在该例中，通过 `spec.sink.type` 字段指定目标存储服务类型为 S3，通过 `spec.sink.options` 字段指定目标存储选项：

* `s3-endpoint`：S3 端点，引用 Secret `s3-config` 的键 `endpoint` 的值。
* `s3-access-key-id`：S3 服务的 AccessKeyID 凭证，引用 Secret `s3-config` 的键 `accessKeyID` 的值。
* `s3-secret-access-key`：S3 服务的 SecretAccessKey 凭证，引用 Secret `s3-config` 的键 `secretAccessKey` 的值。
* `s3-uri`：S3 路径，上传数据到该路径下。
* `s3-no-check-bucket`：不检查 bucket 是否存在，当上述凭证不具备检查 bucket 的权限时需要设置，该字段是可选的。

<aside class="note info">
<div class="title">信息</div>

指定文件或目录地址 `s3-uri` 时，必须通过 `value` 直接设置其值，不可以通过 `valueFrom` 间接引用 Secret 或 ConfigMap 的内容。

</aside>

## 数据传输设置

### 执行策略

DataCube 支持限制数据传输的失败重试次数，以及每次数据传输的最大执行时间：

```yaml
spec:
  executor:
    options:
      backoffLimit: 2
      activeDeadlineSeconds: 3600
```

在该例中：

* 设置最多失败重试 `2` 次（由 `spec.executor.options.backoffLimit` 字段指定），重试达到限制次数时，标记该 DataCube 失败；默认为 0，即不执行失败重试。
* 设置每次数据传输最多执行 `3600` 秒（由 `spec.executor.options.activeDeadlineSeconds` 字段指定），当本次数据传输达到限制时长时，标记本次数据传输失败，将会进行重试；默认为空，即不限制执行时间。

### 额外参数

指定数据传输时额外的参数：

```yaml
spec:
  executor:
    options:
      extraArgs:
      - --cache-dir
      - /tmp/cache/hf
```

在该例中，通过 `spec.executor.options.extraArgs` 指定缓存目录 `--cache-dir` 为 `/tmp/cache/hf`，适用于下载 Hugging Face 文件。

<aside class="note info">
<div class="title">信息</div>

不同的数据存储服务支持不同的额外参数：

* Git
  * 下载
    * <a target="_blank" rel="noopener noreferrer" href="https://git-scm.com/docs/git-clone#_options">git clone</a>（如果 Git 本地仓库不存在）
    * <a target="_blank" rel="noopener noreferrer" href="https://git-scm.com/docs/git-fetch#_options">git fetch</a>（如果 Git 本地仓库存在）
  * 上传：<a target="_blank" rel="noopener noreferrer" href="https://git-scm.com/docs/git-push#_options">git push</a>
* Hugging Face
  * 下载：<a target="_blank" rel="noopener noreferrer" href="https://huggingface.co/docs/huggingface_hub/en/guides/cli#huggingface-cli-download">huggingface-cli download</a>
  * 上传：<a target="_blank" rel="noopener noreferrer" href="https://huggingface.co/docs/huggingface_hub/en/guides/cli#huggingface-cli-upload">huggingface-cli upload</a>
* S3
  * <a target="_blank" rel="noopener noreferrer" href="https://rclone.org/s3/">rclone copy</a>

</aside>

### 环境变量

设置数据传输时的环境变量：

```yaml
spec:
  executor:
    env:
    - name: HTTPS_PROXY
      value: <host>:<port>
```

在该例中，通过 `spec.executor.env` 定义了数据传输时的网络代理，表示使用该网络代理进行数据下载或上传。

<aside class="note">
<div class="title">注意</div>

环境变量的 `name` 不可以和上文中的 `options.name` 重名。

</aside>

### S3 同步

在下载 S3 数据到 PVC 时，可以设置使用同步模式：

```yaml
spec:
  executor:
    options:
      sync: true
```

在该例中，通过 `spec.executor.options.sync` 定义了使用同步模式，表示完全同步 S3 数据内容到 PVC，会删除 PVC 子目录中多余的文件。

<aside class="note info">
<div class="title">信息</div>

如果 `spec.executor.options.sync` 缺省或为 `false`，表示不使用同步模式，DataCube 仅下载 S3 数据，而不会删除 PVC 原有文件。

</aside>

<aside class="note">
<div class="title">注意</div>

仅下载 S3 数据时支持设置同步模式，其他场景不支持该模式。

</aside>

## 状态

### Pod 状态

执行数据传输的 Pod 状态信息记录在 `status.pod` 中：

```yaml
status:
  pod:
    phase: Succeeded
    reference:
      name: s3-upload-file-batchjob-h4fsn
      uid: 8789c49a-ce14-4daa-b2d3-46a32a1decec
    status: Completed
```

### DataCube 状态

DataCube 的状态信息记录在 `status.conditions` 中，包括 3 种类型：

* `Initialized`：DataCube 已经成功创建 Pod 并正常启动，执行数据传输任务。
* `Complete`：DataCube 数据传输完成。
* `Failed`：DataCube 数据传输失败。

下面是一个状态信息的示例：

```yaml
status:
  conditions:
  - lastProbeTime: "2024-04-25T06:28:45Z"
    lastTransitionTime: "2024-04-25T06:28:45Z"
    message: The DataCube is initialized
    status: "True"
    type: Initialized
  - lastProbeTime: "2024-04-25T06:28:45Z"
    lastTransitionTime: "2024-04-25T06:28:45Z"
    message: The DataCube is complete
    status: "True"
    type: Complete
  - lastProbeTime: "2024-04-25T06:28:45Z"
    lastTransitionTime: "2024-04-25T06:28:38Z"
    status: "False"
    type: Failed
```

## 参考

* API 参考：[DataCube](../../references/api-reference/datacube.md)
