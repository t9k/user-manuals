# 用户指南

## 下载安装

### 下载

t9k-pf 可以从平台首页下载。请根据操作系统和架构（可以在命令行运行 `uname -om` 获取）选择适当的版本。

### 安装

根据下载的版本，设置 t9k-pf 的版本和系统架构等变量：

``` bash
version=0.1.9
os=darwin
arch=amd64
```

然后解压下载好的 t9k-pf，并把得到的二进制文件移动到 `/usr/local/bin` 路径下：

``` bash
tar -zxvf "$HOME/Downloads/t9k-pf-$version-$os-$arch.tar.gz"
mv t9k-pf-$os-$arch /usr/local/bin/t9k-pf
rm -f "$HOME/Downloads/t9k-pf-$version-$os-$arch.tar.gz"
```

安装完成后，运行以下命令来验证安装是否成功：

``` bash
t9k-pf version
```

### 卸载

删除二进制文件即可卸载 t9k-pf。

``` bash
rm -f /usr/local/bin/t9k-pf
```

## 身份认证和授权

### 通过 T9k Config 进行身份认证和授权

t9k-pf 默认使用 [T9k Config](../tensorstack-cli/user-guide.md#配置文件) 来进行身份认证和授权。您可以通过命令行参数 `-c, --config` 来指定 t9k-pf 使用的 T9k Config 文件的路径，未指定时，默认使用 `$HOME/.t9k/t9k-config.yaml` 路径下 T9k Config 中 current-context 的认证信息。

下面是一个 T9k Config 的示例，其中 current-context 为 `demo1`，该 Context 的 token 字段不为空，因此最终 t9k-pf 使用该值 `demo1-token` 来完成身份验证（如果 apikey 和 token 均不为空，t9k-pf 优先使用 apikey）。

``` yaml
current-context: demo1
contexts:
- name: demo1
  server: https://<example.com>
  image-registry: https://<example.io>
  prefixes:
    aimd: /t9k/aimd/server
    asset-hub: /t9k/asset-hub/server
    build-console: /t9k/build-console/server
    cluster-admin: /t9k/cluster-admin/server
    deploy-console: /t9k/deploy-console/server
    workflow: /t9k/workflow/server
  auth:
    apikey: ""
    token: demo1-token
  extension:
    codepack:
      data-copy-image: <your-image>
- name: demo2
  server: https://<example.com>
  ...
```

### 通过 API Key 进行临时身份认证和授权

t9k-pf 支持通过命令行参数 `-k,--apikey` 直接指定 API Key，完成单次端口转发的身份认证和授权。

例如输入以下指令（其中 `notebook <URL>` 会在[命令](./commands.md)中介绍，此处只用关注 `--apikey` 的使用）：

``` bash
t9k-pf notebook <url> --apikey
```

命令行会进入交互式输入界面，粘贴您的 API Key 再按下回车即可。

<aside class="note">
<h1>注意</h1>

此方式指定的 API Key 不会被保存，认证信息只在这次端口转发中生效。

</aside>

## 全局选项

* **-c, --config**

    使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。

* **-k, --apikey**

    开启交互式输入 API Key。

* **-n, --namespace** 

    使用的项目（命名空间）名称。

* **-h, --help** 

    查看当前指令的帮助信息和示例。

* **--address** 

    本地监听地址。默认为 `localhost`。
