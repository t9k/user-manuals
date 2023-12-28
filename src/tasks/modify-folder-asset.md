# 修改 Folder 和 Asset 的名称和标签

本教程演示如何通过多种方式修改 Folder 和 Asset 的名称和标签。

## 准备工作

* 完成教程[操作 Folder 和 Asset](./manipulate-folder-asset.md)。

## 通过命令行工具

切换到您的工作路径下：

```shell
$ cd /your/workpath
```

修改名称和标签的方式对于 Folder、Model 和 Dataset 都是相同的。下面将以 Model Folder 和 Model 为例进行演示（这里以 `user` 表示当前用户）。

依次创建 Model Folder 和 Model：

```shell
$ ah create model/llm
AH INFO: Folder /xyx/t9k-assethub/model/llm created

$ ah create model/llm/gpt2
AH INFO: Model gpt2 created for Folder /xyx/t9k-assethub/model/llm
```

使用 `ah update` 命令修改 Folder 和 Model 的名称：

```shell
$ ah update model/llm -n chat
AH INFO: Folder /xyx/t9k-assethub/model/llm updated to /xyx/t9k-assethub/model/chat

$ ah update model/chat/gpt2 -n gpt3
AH INFO: Model /xyx/t9k-assethub/model/chat/gpt2 updated to /xyx/t9k-assethub/model/chat/gpt3
```

使用 `ah ls` 命令查看 Folder 和 Model 的标签：

```shell
$ ah ls model --detail
NAME    PATH                          ...  LABELS  ...
chat    /xyx/t9k-assethub/model/chat

$ ah ls model/chat
NAME    PATH                               LABELS  ...
gpt3    /xyx/t9k-assethub/model/chat/gpt3
```

两者都没有标签，再次使用 `ah update` 命令为它们添加标签：

```shell
$ ah update model/chat --label "NLP" --label "AIGC"
AH INFO: Folder /xyx/t9k-assethub/model/chat updated

$ ah ls model --detail
NAME    PATH                          ...  LABELS     ...
chat    /xyx/t9k-assethub/model/chat       AIGC, NLP
```

```shell
$ ah update model/chat/gpt3 --label "GPT"
AH INFO: Model /xyx/t9k-assethub/model/chat/gpt3 updated

$ ah ls model/chat
NAME    PATH                               LABELS    PERMISSION
gpt3    /xyx/t9k-assethub/model/chat/gpt3  GPT       own
```

!!! tip "提示"
    标签的更新是全量的：每次添加标签都会移除已有的标签。

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

修改名称和标签的方式对于 Folder、Model 和 Dataset 都是相同的。下面将以 Model Folder 和 Model 为例进行演示（这里以 `user` 表示当前用户）。

依次创建 Model Folder 和 Model：

```python
model_folder = ah.create('model/llm')
model = ah.create('model/llm/gpt2')
```

```
AH INFO: Folder /xyx/t9k-assethub/model/llm created
AH INFO: Model gpt2 created for Folder /xyx/t9k-assethub/model/llm
```

使用 `ah.update()` 函数修改 Folder 和 Model 的名称：

```python
ah.update('model/llm', name='chat')
ah.update('model/chat/gpt2', name='gpt3')
```

```
AH INFO: Folder /xyx/t9k-assethub/model/llm updated to /xyx/t9k-assethub/model/chat
AH INFO: Model /xyx/t9k-assethub/model/chat/gpt2 updated to /xyx/t9k-assethub/model/chat/gpt3
```

!!! tip "提示"
    亦可使用 `Folder` 和 `Model` 实例的 `update()` 方法完成上述操作。

使用 `ah.list()` 函数查看 Folder 和 Model 的标签：

```python
from pprint import pprint

pprint(ah.list('model'))
pprint(ah.list('model/chat'))
```

```
[{...
  'labels': [],
  'name': 'chat',
  'path': '/xyx/t9k-assethub/model/chat',
  'type': 'Folder'}]
[{...
  'labels': [],
  'name': 'gpt3',
  'path': '/xyx/t9k-assethub/model/chat/gpt3',
  'type': 'Model'}]
```

两者都没有标签，继续使用 `ah.update()` 函数为它们添加标签：

```python
ah.update('model/chat', labels=['NLP', 'AIGC'])
ah.update('model/chat/gpt3', labels=['GPT'])
```

```
AH INFO: Folder /xyx/t9k-assethub/model/chat updated
AH INFO: Model /xyx/t9k-assethub/model/chat/gpt3 updated
```

```python
pprint(ah.list('model'))
pprint(ah.list('model/chat'))
```

```
[{...
  'labels': ['AIGC', 'NLP'],
  'name': 'chat',
  'path': '/xyx/t9k-assethub/model/chat',
  'type': 'Folder'}]
[{...
  'labels': ['GPT'],
  'name': 'gpt3',
  'path': '/xyx/t9k-assethub/model/chat/gpt3',
  'type': 'Model'}]
```

!!! tip "提示"
    标签的更新是全量的：每次添加标签都会移除已有的标签。

!!! tip "提示"
    亦可使用 `Folder` 和 `Model` 实例的 `update()` 方法完成上述操作。

## 通过控制台
