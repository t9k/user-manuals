# 操作文件夹、模型和数据集

本教程演示如何通过多种方式操作文件夹、模型和数据集，包括创建、查看和删除。

## 准备工作

* [安装](../tools/python-sdk-t9k/index.md) TensorStack SDK 并阅读[用户指南](../tools/python-sdk-t9k/guide.md)。

## 通过命令行工具

切换到您的工作路径下：

```shell
$ cd /your/workpath
```

假设当前用户（这里假设用户名为 `demo`）没有可以访问的文件夹，使用 `ah create` 命令创建一个模型文件夹和一个数据集文件夹：

```shell
$ ah create model/llm
AH INFO: Folder /demo/t9k-assethub/model/llm created

$ ah create dataset/text
AH INFO: Folder /demo/t9k-assethub/dataset/text created
```

<aside class="note tip">
<div class="title">提示</div>

限于篇幅，本教程以及后续教程将仅展示各条命令的基本用法，请使用 `--help` 选项（例如 `ah create --help`）查看相应命令接受的参数格式、所有选项以及具体用例。

</aside>

然后使用 `ah create` 命令在模型文件夹中创建一个模型，以及在数据集文件夹中创建一个数据集：

```shell
$ ah create model/llm/gpt2
AH INFO: Model gpt2 created for Folder /demo/t9k-assethub/model/llm

$ ah create dataset/text/openwebtext
AH INFO: Dataset openwebtext created for Folder /demo/t9k-assethub/dataset/text
```

创建完成之后，使用 `ah ls` 命令查看当前用户的模型文件夹和数据集文件夹：

```shell
$ ah ls model
NAME    PATH                          LABELS    PERMISSION
llm     /demo/t9k-assethub/model/llm             own

$ ah ls dataset
NAME    PATH                              LABELS    PERMISSION
text    /demo/t9k-assethub/dataset/text              own
```

使用 `ah ls` 命令查看模型文件夹下的所有模型以及数据集文件夹下的所有数据集：

```shell
$ ah ls model/llm
NAME    PATH                              LABELS    PERMISSION
gpt2    /demo/t9k-assethub/model/llm/gpt2            own

$ ah ls dataset/text
NAME         PATH                                        LABELS    PERMISSION
openwebtext  /demo/t9k-assethub/dataset/text/openwebtext            own
```

最后使用 `ah delete` 命令删除所有创建的模型、数据集和文件夹：

```shell
$ ah delete model/llm/gpt2
AH INFO: Model /demo/t9k-assethub/model/llm/gpt2 deleted

$ ah delete dataset/text/openwebtext
AH INFO: Dataset /demo/t9k-assethub/dataset/text/openwebtext deleted

# 可以直接删除文件夹, 其中的模型或数据集都会被一并删除
$ ah delete model/llm
AH INFO: Folder /demo/t9k-assethub/model/llm deleted

$ ah delete dataset/text
AH INFO: Folder /demo/t9k-assethub/dataset/text deleted
```

<aside class="note">
<div class="title">注意</div>

删除模型、数据集和文件夹时会一并删除其中的所有内容，请慎重操作。

</aside>

## 通过 Python SDK

切换到您的工作路径下，然后以任意方式执行下面的 Python 代码。

导入 `t9k.ah` 模块，使用 `ah.login()` 函数登录到 Asset Hub 服务器（如果配置文件中的凭据仍有效，则无需提供参数）：

```python
from t9k import ah

ah.login(host='<asset-hub-server-url>',
         api_key='<your-api-key>')
```

```
AH INFO: Logged in to Asset Hub server and AIStore server as user <your-user-name>
```

假设当前用户（这里假设用户名为 `demo`）没有可以访问的文件夹，使用 `ah.create()` 函数创建一个模型文件夹和一个数据集文件夹，各返回一个 `Folder` 实例：

```python
model_folder = ah.create('model/llm')
dataset_folder = ah.create('dataset/text')
```

```
AH INFO: Folder /demo/t9k-assethub/model/llm created
AH INFO: Folder /demo/t9k-assethub/dataset/text created
```

<aside class="note tip">
<div class="title">提示</div>

限于篇幅，本教程以及后续教程将仅展示各个函数或方法的基本用法，相应函数或方法接受的参数详情以及具体用例请参考 TensorStack SDK 的 [API 文档](../tools/python-sdk-t9k/api/index.md)。

</aside>

继续使用 `ah.create()` 函数在模型文件夹中创建一个模型，以及在数据集文件夹中创建一个数据集：

```python
model = ah.create('model/llm/gpt2')
dataset = ah.create('dataset/text/openwebtext')
```

```
AH INFO: Model gpt2 created for Folder /demo/t9k-assethub/model/llm
AH INFO: Dataset openwebtext created for Folder /demo/t9k-assethub/dataset/text
```

<aside class="note tip">
<div class="title">提示</div>

亦可使用 `Folder` 实例的 `create_asset()` 方法完成上述操作。

</aside>

创建完成之后，使用 `ah.list()` 函数返回当前用户的文件夹：

```python
from pprint import pprint

pprint(ah.list('model'))
pprint(ah.list('dataset'))
```

```
[{'description': '',
  'editor': 'demo',
  'extra': '{"createdTimestamp": "2023-08-17T08:05:24.044319Z"}',
  'id': '967a5135-8b13-4283-9fad-ba53503612b3',
  'labels': [],
  'modifiedTimestamp': '2023-08-17T08:05:24.390002Z',
  'name': 'llm',
  'path': '/demo/t9k-assethub/model/llm',
  'permission': 'own',
  'storageType': 0,
  'type': 'Folder'}]
[{'description': '',
  'editor': 'demo',
  'extra': '{"createdTimestamp": "2023-08-17T08:05:24.196610Z"}',
  'id': 'd0d9f4b2-6c15-4dbb-b2d1-0619b6774c4a',
  'labels': [],
  'modifiedTimestamp': '2023-08-17T08:05:24.519213Z',
  'name': 'text',
  'path': '/demo/t9k-assethub/dataset/text',
  'permission': 'own',
  'storageType': 0,
  'type': 'Folder'}]
```

继续使用 `ah.list()` 函数返回模型文件夹下的所有模型和数据集文件夹下的所有数据集：

```python
pprint(ah.list('model/llm'))
pprint(ah.list('dataset/text'))
```

```
[{'description': '',
  'editor': 'demo',
  'extra': '{"createdTimestamp": "2023-08-17T08:11:09.948554Z"}',
  'id': '2157a139-e20b-4736-9e25-d4495e287af8',
  'labels': [],
  'modifiedTimestamp': '2023-08-17T08:11:10.327166Z',
  'name': 'gpt2',
  'path': '/demo/t9k-assethub/model/llm/gpt2',
  'permission': 'own',
  'storageType': 3,
  'type': 'Model'}]
[{'description': '',
  'editor': 'demo',
  'extra': '{"createdTimestamp": "2023-08-17T08:11:10.508407Z"}',
  'id': '6826131c-2c88-483e-8a48-0f6d8fa59cfa',
  'labels': [],
  'modifiedTimestamp': '2023-08-17T08:11:10.830665Z',
  'name': 'openwebtext',
  'path': '/demo/t9k-assethub/dataset/text/openwebtext',
  'permission': 'own',
  'storageType': 3,
  'type': 'Dataset'}]
```

<aside class="note tip">
<div class="title">提示</div>

亦可使用 `Folder` 实例的 `list_asset()` 方法完成上述操作。

</aside>

最后使用 `ah.delete()` 函数删除所有创建的模型、数据集和文件夹：

```python
ah.delete('model/llm/gpt2')
ah.delete('dataset/text/openwebtext')
ah.delete('model/llm')    # 可以直接删除文件夹, 其中的模型或数据集都会被一并删除
ah.delete('dataset/text')
```

```
AH INFO: Model /demo/t9k-assethub/model/llm/gpt2 deleted
AH INFO: Dataset /demo/t9k-assethub/dataset/text/openwebtext deleted
AH INFO: Folder /demo/t9k-assethub/model/llm deleted
AH INFO: Folder /demo/t9k-assethub/dataset/text deleted
```

<aside class="note tip">
<div class="title">提示</div>

亦可使用各实例的 `delete()` 方法完成上述操作。

</aside>

## 通过控制台

数据集文件夹、数据集的控制台操作分别和模型文件夹、模型完全一致。本教程后续仅展示模型文件夹和模型的创建、查看、删除、分享功能，您可以用同样的方式操作数据集文件夹和数据集。

在左侧的导航菜单中点击**模型**，选择查看范围为 **My Own**，查看当前用户的所有模型文件夹。然后点击右上角的 **+** 创建新的模型文件夹：

<figure class="screenshot">
  <img alt="model-all" src="../assets/tasks/manage-asset/manipulate-folder-and-asset/model-owned.png" class="screenshot"/>
</figure>

填写名称 `image-classification`，点击**创建**：

<figure class="screenshot">
  <img alt="folder-create" src="../assets/tasks/manage-asset/manipulate-folder-and-asset/folder-create.png" class="screenshot"/>
</figure>

接下来分享这个文件夹。点击文件夹右侧的 **更多 > 分享**：

<figure class="screenshot">
  <img alt="folder-share" src="../assets/tasks/manage-asset/manipulate-folder-and-asset/folder-share.png" class="screenshot"/>
</figure>

点击**添加分享目标**，选择分享的对象为 **Public**（所有用户可见），分享的权限是 **Edit**，最后点击**分享**：

<figure class="screenshot">
  <img alt="folder-share-setting" src="../assets/tasks/manage-asset/manipulate-folder-and-asset/folder-share-setting.png" class="screenshot"/>
</figure>

回到 Asset Hub 控制台，点击模型文件夹 **image-classification** 查看其中的模型：

<figure class="screenshot">
  <img alt="folder-list" src="../assets/tasks/manage-asset/manipulate-folder-and-asset/folder-list.png" class="screenshot"/>
</figure>

新创建的模型文件夹中没有模型，点击右上角的 **+** 创建一个模型：

<figure class="screenshot">
  <img alt="model-list" src="../assets/tasks/manage-asset/manipulate-folder-and-asset/model-list.png" class="screenshot"/>
</figure>

填写名称 `mnist`，然后点击**创建**：

<figure class="screenshot">
  <img alt="model-create" src="../assets/tasks/manage-asset/manipulate-folder-and-asset/model-create.png" class="screenshot"/>
</figure>

创建成功后，在模型文件夹中可以看到模型信息：

<figure class="screenshot">
  <img alt="model-created" src="../assets/tasks/manage-asset/manipulate-folder-and-asset/model-created.png" class="screenshot"/>
</figure>

点击**更多 > 删除**，删除创建的模型，然后点击左上角的**返回**，返回模型文件夹的页面：

<figure class="screenshot">
  <img alt="model-delete" src="../assets/tasks/manage-asset/manipulate-folder-and-asset/model-delete.png" class="screenshot"/>
</figure>

最后，返回 Asset Hub 控制台，点击**更多 > 删除**，删除模型文件夹：

<figure class="screenshot">
  <img alt="folder-delete" src="../assets/tasks/manage-asset/manipulate-folder-and-asset/folder-delete.png" class="screenshot"/>
</figure>
