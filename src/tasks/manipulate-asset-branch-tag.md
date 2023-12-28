# 操作 Asset 的分支、tag 和 commit

本教程演示如何通过多种方式操作 Asset 的分支、tag 和 commit，包括创建、查看和删除分支，创建、查看和删除 tag，以及查看 commit。

## 准备工作

* 完成教程[操作 Folder 和 Asset](./manipulate-folder-asset.md)。

## 通过命令行工具

切换到您的工作路径下：

```shell
$ cd /your/workpath
```

操作 tag 和 commit 的方式对于 Model 和 Dataset 都是相同的，只有 Model 允许操作分支。下面将以 Model 为例进行演示（这里以 `user` 表示当前用户）。

依次创建 Model Folder 和 Model：

```shell
$ ah create model/llm
AH INFO: Folder /xyx/t9k-assethub/model/llm created

$ ah create model/llm/gpt2
AH INFO: Model gpt2 created for Folder /xyx/t9k-assethub/model/llm
```

继续使用 `ah create` 命令为 Model 创建一个分支：

```shell
$ ah create model/llm/gpt2:v1
AH INFO: Branch v1 created for Model /xyx/t9k-assethub/model/llm/gpt2
```

<aside class="note">
<h1>注意</h1>

Model 可以在初始的主分支（`main` 分支）之外创建新的分支，Dataset 则不可以。

</aside>

使用 `ah ls --branch` 命令查看 Model 的所有分支：

```shell
$ ah ls model/llm/gpt2 --branch
NAME    COMMIT_ID
main    fe46da7e
v1      fe46da7e
```

继续使用 `ah create` 命令为 Model 创建一个 tag：

```shell
$ ah create model/llm/gpt2:20230101 --tag --source v1
AH INFO: Tag 20230101 created from branch v1 for Model /xyx/t9k-assethub/model/llm/gpt2
```

使用 `ah ls --tag` 命令查看 Model 的所有 tag：

```shell
$ ah ls model/llm/gpt2 --tag
    NAME  COMMIT_ID
20230101  fe46da7e
```

使用 `ah ls --commit` 命令查看 Model 的一个分支下的所有 commit：

```shell
$ ah ls model/llm/gpt2:v1 --commit
COMMIT_ID    MESSAGE             CREATED
fe46da7e     Repository created  3m16s ago
```

最后使用 `ah delete` 命令删除所有创建的分支和 tag：

```shell
$ ah delete model/llm/gpt2:v1
AH INFO: Branch v1 deleted for Model /xyx/t9k-assethub/model/llm/gpt2

$ ah delete model/llm/gpt2:20230101
AH INFO: Tag 20230101 deleted for Model /xyx/t9k-assethub/model/llm/gpt2
```

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

操作 tag 和 commit 的方式对于 Model 和 Dataset 都是相同的，只有 Model 允许操作分支。下面将以 Model 为例进行演示（这里以 `user` 表示当前用户）。

依次创建 Model Folder 和 Model：

```python
model_folder = ah.create('model/llm')
model = ah.create('model/llm/gpt2')
```

```
AH INFO: Folder /xyx/t9k-assethub/model/llm created
AH INFO: Model gpt2 created for Folder /xyx/t9k-assethub/model/llm
```

继续使用 `ah.create()` 函数为 Model 创建一个分支：

```python
branch = ah.create('model/llm/gpt2:v1')
```

```
AH INFO: Branch v1 created for Model /xyx/t9k-assethub/model/llm/gpt2
```

<aside class="note tip">
<h1>提示</h1>

亦可使用 `Model` 实例的 `create_branch()` 方法完成上述操作。

</aside>

使用 `ah.list()` 函数查看 Model 的所有分支：

```python
from pprint import pprint

pprint(ah.list('model/llm/gpt2', resource='branch'))
```

```
[{'commit_id': 'a15799f8f601d514a1a385a57b3078f8e178614a66aa920217175f6dcac2b083',
  'id': 'main'},
 {'commit_id': 'a15799f8f601d514a1a385a57b3078f8e178614a66aa920217175f6dcac2b083',
  'id': 'v1'}]
```

<aside class="note tip">
<h1>提示</h1>

亦可使用 `Model` 实例的 `list_branch()` 方法完成上述操作。

</aside>

继续使用 `ah.create()` 函数为 Model 创建一个 tag：

```python
tag = ah.create('model/llm/gpt2:20230101', resource='tag', source='v1')
```

```
AH INFO: Tag 20230101 created from branch v1 for Model /xyx/t9k-assethub/model/llm/gpt2
```

<aside class="note tip">
<h1>提示</h1>

亦可使用 `Branch` 实例的 `create_tag()` 方法完成上述操作。

</aside>

使用 `ah.list()` 函数查看 Model 的所有 tag：

```python
pprint(ah.list('model/llm/gpt2', resource='tag'))
```

```
[{'commit_id': 'a15799f8f601d514a1a385a57b3078f8e178614a66aa920217175f6dcac2b083',
  'id': '20230101'}]
```

<aside class="note tip">
<h1>提示</h1>

亦可使用 `Model` 实例的 `list_tag()` 方法完成上述操作。

</aside>

最后使用 `ah.delete()` 函数删除所有创建的分支和 tag：

```python
ah.delete('model/llm/gpt2:v1')
ah.delete('model/llm/gpt2:20230101')
```

```
AH INFO: Branch v1 deleted for Model /xyx/t9k-assethub/model/llm/gpt2
AH INFO: Tag 20230101 deleted for Model /xyx/t9k-assethub/model/llm/gpt2
```

<aside class="note tip">
<h1>提示</h1>

亦可使用各实例的 `delete()` 方法完成上述操作。

</aside>

## 通过控制台
