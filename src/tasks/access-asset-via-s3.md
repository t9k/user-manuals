# 通过 S3 访问 Asset

本教程演示如何 S3 访问 Asset。

## 准备工作

* 完成教程[操作 Folder 和 Asset](./manipulate-folder-and-asset.md)。

## 创建 S3 凭证

在 Asset Hub 控制台进入 Asset 详情页面，点击 **S3 凭证**可以查看目前已有的所有 S3 凭证。然后点击表格右上角的 **+** 创建一个 S3 凭证：

<figure class="screenshot">
  <img alt="s3-cred-list" src="../assets/guide/manage-asset/access-asset-by-s3/s3-cred-list.png" class="screenshot"/>
</figure>

填写名称 `s3-rw`，选择类型为**可读/可写**，最后点击**创建**：

<figure class="screenshot">
  <img alt="s3-cred-create" src="../assets/guide/manage-asset/access-asset-by-s3/s3-cred-create.png" class="screenshot"/>
</figure>

## 查看 S3 凭证

创建完成后，点击表格左上角的**可读/可写**，查看所有类型为可读/可写的 S3 凭证：

<figure class="screenshot">
  <img alt="s3-cred-list-rw" src="../assets/guide/manage-asset/access-asset-by-s3/s3-cred-list-rw.png" class="screenshot"/>
</figure>

点击刚刚创建的 S3 凭证 `s3-rw`，查看其详情：

<figure class="screenshot">
  <img alt="s3-cred-detail" src="../assets/guide/manage-asset/access-asset-by-s3/s3-cred-detail.png" class="screenshot"/>
</figure>

S3 凭证有三种格式：

1. `.s3cfg`：命令行工具 s3cmd 的配置文件。
2. `S3-cfg Secret`：在项目中创建此 Secret，用于在创建 Notebook、Job、Workflow 等工作负载时挂载此 Secret。
3. `S3-env Secret`：在项目中创建此 Secret，用于在创建 Notebook、Job、Workflow 等工作负载时挂载此 Secret。

## 通过 s3cmd 访问 Asset

点击右侧的**复制**，复制 `.s3cfg` 格式的 S3 凭证，保存在 `$HOME/.s3cfg` 文件中，即可通过 s3cmd 命令行工具访问此 Asset 中的文件。

!!! 信息 "如何安装 s3cmd 命令行工具？"

    根据操作系统的不同，分别通过以下命令安装 s3cmd 命令行工具：

    ```bash
    # macOS
    brew install s3cmd

    # Linux
    apt install s3cmd

    # Windows
    pip install s3cmd
    ```

例如，在上述示例中，所创建的 S3 凭证 `s3-rw` 仅可用于访问名为 `stable-diffusion-2-1` 的 Asset。根据页面上的提示，此 Asset 对应的 bucket 名称为 `baa98ded-2f93-4e9b-835a-6515a63a6eb4`，您可以通过以下命令查看此 Asset 的 `main` 分支的 `README.md` 文件：

```bash
s3cmd ls s3://baa98ded-2f93-4e9b-835a-6515a63a6eb4/main/README.md
```

通过以下命令下载此 Asset 的某个分支下某个路径的文件：

```bash
s3cmd get s3://baa98ded-2f93-4e9b-835a-6515a63a6eb4/branch-name/path/to/object
```

## 通过 StorageShim 访问 Asset

除了通过命令行工具访问，您还可以创建一个 [StorageShim](../manage-auxiliary-resources/manage-datasetconnect.md)，将 S3 bucket 的某个子路径形式化为一个持久卷，以便在 Notebook、Job、Workflow 等工作负载中挂载，直接以文件系统的形式查看、编辑 S3 bucket 中的文件。

在创建 StorageShim 之前，您首先需要创建一个 Secret 保存 S3 bucket 的相关信息。在 S3 凭证的详情页面，点击左侧的 **S3-cfg Secret** 标签，然后点击右上角的**复制**：

<figure class="screenshot">
  <img alt="s3-cred-detail-s3-cfg-secret" src="../assets/guide/manage-asset/access-asset-by-s3/s3-cred-detail-s3-cfg-secret.png" class="screenshot"/>
</figure>

在模型构建控制台的左侧导航栏中点击**辅助 > Secret** 进入 Secret 管理页面，然后点击右上角的**创建**进入 Secret 创建页面：

<figure class="screenshot">
  <img alt="secret-list" src="../assets/guide/manage-asset/access-asset-by-s3/secret-list.png" class="screenshot"/>
</figure>

在 Secret 创建页面，将所复制的 `S3-cfg Secret` 粘贴到右侧的 YAML 编辑框中，左侧表格会自动解析出各个字段，最后点击**创建 Secret**。

<figure class="screenshot">
  <img alt="secret-create" src="../assets/guide/manage-asset/access-asset-by-s3/secret-create.png" class="screenshot"/>
</figure>

在模型构建控制台的左侧导航栏中点击**存储 > 持久卷**进入持久卷管理页面，然后点击上方的 S3 进入 S3 类型的持久卷管理页面，最后点击右上角的**创建**进入 StorageShim 创建页面：

<figure class="screenshot">
  <img alt="storageshim-list" src="../assets/guide/manage-asset/access-asset-by-s3/storageshim-list.png" class="screenshot"/>
</figure>

在 StorageShim 创建页面，

1. 名称填写 `stable-diffusion-2-1`；
2. S3 URI 填写 `s3://baa98ded-2f93-4e9b-835a-6515a63a6eb4/main`，以便把上述示例 Asset 的 main 分支挂载为持久卷；
3. S3 Secret 选择刚刚创建的 `s3-rw`。

最后点击**创建 StorageShim**。

<figure class="screenshot">
  <img alt="storageshim-create" src="../assets/guide/manage-asset/access-asset-by-s3/storageshim-create.png" class="screenshot"/>
</figure>

StorageShim 创建完成后，等待其阶段变为 **Bound**，您即可通过以下方式使用这个名为 `stable-diffusion-2-1` 的持久卷：

1. 点击**启动**，创建一个 Explorer 来浏览持久卷中的文件。
2. 在创建 Notebook 时，添加持久卷 `stable-diffusion-2-1`，以便在 Notebook 中查看和编辑此 Asset 中的文件。
3. 在创建 Job 时，添加持久卷 `stable-diffusion-2-1`，以便在 Job 中使用此 Asset 中的文件。

<figure class="screenshot">
  <img alt="storageshim-list-after-create" src="../assets/guide/manage-asset/access-asset-by-s3/storageshim-list-after-create.png" class="screenshot"/>
</figure>
