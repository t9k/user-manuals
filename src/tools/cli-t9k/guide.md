# 用户指南

## 下载安装

### 下载

TensorStack CLI（以下简称 T9k CLI）可以从平台首页下载。请根据操作系统和架构（可以在命令行运行 `uname -om` 获取）选择适当的版本。

### 安装

您需要根据下载的版本，设置 T9k CLI 的版本和系统架构等变量：

``` bash
version=1.78.6
os=darwin
arch=amd64
```

然后解压下载好的 T9k CLI，并把得到的二进制文件移动到 `/usr/local/bin` 路径下：

``` bash
tar -zxvf "$HOME/Downloads/t9k-$version-$os-$arch.tar.gz"
mv t9k-$os-$arch /usr/local/bin/t9k
rm -f "$HOME/Downloads/t9k-$version-$os-$arch.tar.gz"
```

您可以运行以下命令来验证 T9k CLI 安装完成：

``` bash
t9k version
```

### 卸载

删除二进制文件以卸载 T9k CLI。

``` bash
rm -f /usr/local/bin/t9k
```

## 配置文件

TensorStack CLI 使用 T9k Config 作为配置文件。T9k Config 文件的路径通过命令行参数 `-c, --config` 进行指定，在未被指定时，使用默认路径 `$HOME/.t9k/t9k-config.yaml`。第一次使用时，可以通过 `t9k config auth` 命令来生成配置文件，详情请参阅 [t9k config auth](./command.md#auth)。

T9k Config 示例如下：

``` yaml
current-context: default-context
contexts:
- name: default-context
  server: https://<example.com>
  image-registry: https://<example.io>
  prefixes:
    aistore: /t9k/aistore/server
    asset-hub: /t9k/asset-hub/server
    build-console: /t9k/build-console/server
    cluster-admin: /t9k/cluster-admin/server
    deploy-console: /t9k/deploy-console/server
    security-console: /t9k/security/server
    workflow-manager: /t9k/workflow/server
  auth:
    apikey: <your-apikey>
    token: <your-token>
  extension:
    codepack:
      data-copy-image: <your-image>
```

T9k Config 包括以下两个部分：

* `current-context`：字符串，记录默认使用的 Context 名称。您可以通过设置命令行参数 `-x, --context` 访问其他的 Context。
* `contexts`：数组，包含集群相关信息。
    * `name`：字符串，Context 的名称。
    * `server`：字符串，记录访问这个集群服务的域名。
    * `image-registry`：字符串，记录这个集群使用镜像仓库的地址。
    * `prefixes`：数组，记录这个集群中的 T9k Servers 路径前缀。
    * `auth`：，记录认证信息，支持 `apikey` 和 `token` 两种认证方式，需要填写其中一种。
    * `extension`：记录其他工具需要用到的拓展配置。

## 全局选项

TensorStack CLI 定义了以下的全局命令行参数：

```bash
  -c, --config string      t9k config file (default: $HOME/.t9k/t9k-config.yaml)
  -x, --context string     name of the context to use (default: current-context in t9k config)
  -h, --help               t9k help
  -n, --namespace string   alias of -p and --project, invalid if --project is set by user.
  -p, --project string     project to use (default: from t9k config file)
  -v, --verbose int        Set level-based filter in logging (default -1)
```

具体说明如下：

* `-c, --config`：字符串，指定 T9k Config 文件的路径。对于子命令 `config`，设置的 T9k Config 文件会被创建或修改。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
* `-x, --context`：字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
* `-h, --help `：查看当前指令的帮助信息和示例。
* `-p, --project`：字符串，指定使用的项目（本文档中的项目和命名空间同义）。
* `-n, --namespace`：字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
* `-v, --verbose`：指定输出 log 信息的详细程度。

项目（命名空间）的使用优先级是（排在前面的优先级更高）：

1. 您通过命令行参数 `-p, --project` 设置的项目。
2. 您通过命令行参数 `-n, --namespace` 设置的项目。
3. 使用项目 `default`。
