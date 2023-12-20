# Explorer

Explorer 提供几种展示和管理集群中数据的方法。

## 创建 Explorer

下面是一个基本的 Explorer 配置示例：

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: Explorer
metadata:
  name: example
spec:
  runMode: running
  storageName: test
  storageType: pvc
```

在该例中，Explorer 展示和管理名为 `test` 的持久卷（Persistent Volume）中的数据。

## 数据存储方式

Explorer 目前仅支持展示存储在 PVC 中的数据（即 `spec.storageType` 字段暂时只能设置为 `pvc`）。

## 数据展示和管理方式

Explorer 会自动以多种方式展示和管理数据，目前支持文件浏览器和代码编辑器两种。

### 文件浏览器
  
使用第三方软件 [File Browser:octicons-link-external-16:](https://github.com/filebrowser/filebrowser){target=_blank} 提供文件管理器形式的界面，支持文件系统浏览、文件上传、文件下载、基本的文件编辑等功能。

### 代码编辑器

使用第三方软件 [VS Code:octicons-link-external-16:](https://github.com/cdr/code-server){target=_blank} 提供云端集成开发环境（IDE）的支持。开发者可以方便地运行网页版 VS Code，进行远程项目开发。

## 资源回收

Explorer 提供空闲资源回收的支持，在检测到 Explorer 处于空闲状态并超过一定时长时，删除工作负载以释放计算资源。默认情况下（管理员可修改配置）：

* Explorer 无人使用超过 1h 后，标记该 Explorer 为 `Idle`。
* Explorer 进入 `Idle` 状态超过 24h 后，删除该 Explorer 底层工作负载。

如果需要再次使用该 Explorer，您可以在模型构建控制台中手动点击**恢复**按钮。
