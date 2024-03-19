# 命令

## autotune

用于管理 [AutoTune](../../modules/building/autotune.md)。

<aside class="note info">
<div class="title">信息</div>

支持使用缩写 `at` 代替 `autotune`。

</aside>

### delete

删除指定的 AutoTune。

#### 使用

```
t9k autotune delete [names...] [--all] [-f]
```

`t9k autotune delete` 也可以用 `t9k autotune rm` 代替。

#### 选项

```
--all                   删除当前 Project 中的所有 AutoTunes。
-f, --force             跳过确认，直接执行删除操作。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

删除 Project demo 下名为 foo 和 bar 的两个 AutoTune：

```
t9k autotune delete foo bar -p demo
```

跳过确认，直接删除 Project demo 下名为 foo 的 AutoTune：

```
t9k autotune delete foo -p demo -f
```

删除 Project demo 下所有的 AutoTune：

```
t9k autotune delete foo -p demo --all
```

### describe

查看某个 AutoTune 的详细信息。

#### 使用

```
t9k at describe <name> [--color]
```

`t9k at describe` 也可以用 `t9k at desc` 代替。

#### 选项

```
--color                 使用彩色的输出信息（默认全是黑色）。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project demo 下名为 foo 的 AutoTune 的详细描述：

```
t9k at describe foo -p demo
```

### get

查看 AutoTune 相关信息。

#### 使用

```
t9k at get [names...] [-A] [-o json|yaml|template]
```

#### 选项

```
-A, --all-namespaces    获取用户具有权限的所有 Namespace（Project）中的资源。
-o, --output string     指定输出信息的形式。可选值有 `json`，`yaml` 和默认的 `template`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

以默认格式查看 Project example 下所有 AutoTune：

```
t9k at get -p example
```

以默认格式查看所有 Project 下的所有 AutoTune：

```
t9k at get -A
```

以默认格式查看 Project example 下名为 foo 和 bar 的两个 AutoTune：

```
t9k at get foo bar -p example
```

以 yaml 格式查看 Project example 下名为 foo 的 AutoTune：

```
t9k at get foo -p example -o yaml
```

### wait

等待 AutoTune 完成。

#### 使用

```
t9k at wait <name> [--timeout=<timeoutTime>] [--period=<periodTime>] [--print-log]
```

#### 选项

```
--timeout string        字符串，最长等待时间。默认值："1h"，1 小时。
--period  string        字符串，检查任务是否完成的周期。默认值："1s"，每秒检查一次。
--print-log             是否在等待时流式查看日志。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

等待 Project example 下的 AutoTune foo 完成：

```
t9k at wait foo -p example
```

等待 Project example 下的 AutoTune foo 完成，只等待 10 分钟：

```
t9k at wait foo -p example --timeout 10m
```

等待 Project example 下的 AutoTune foo 完成，同时打印 server 的日志：

```
t9k at wait foo -p example --print-log
```

## beamjob

用于管理 [BeamJob](../../modules/jobs/beamjob.md)。

<aside class="note info">
<div class="title">信息</div>

支持使用缩写 `bj` 代替 `beamjob`。

</aside>

### delete

删除指定的 BeamJob。

#### 使用

```
t9k beamjob delete [names...] [--all] [-f]
```

`t9k beamjob delete` 也可以用 `t9k bj rm` 代替。

#### 选项

```
--all                   删除当前 Project 中所有的 BeamJob。
-f, --force             跳过确认，直接执行删除操作。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

删除 Project demo 下名为 foo 和 bar 的两个 BeamJob：

```
t9k beamjob delete foo bar -p demo
```

跳过确认，直接删除 Project demo 下名为 foo 的 BeamJob：

```
t9k beamjob delete foo -p demo -f
```

删除 Project demo 下所有的 BeamJob：

```
t9k beamjob delete foo -p demo --all
```

### describe

查看某个 BeamJob 的详细信息。

#### 使用

```
t9k bj describe <name>
```

`t9k bj describe` 也可以用 `t9k bj desc` 代替。

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project demo 下名为 foo 的 BeamJob 的详细描述：

```
t9k bj describe foo -p demo
```

### get

查看 BeamJob 相关信息。

#### 使用

```
t9k bj get [names...] [-A] [-o json|yaml|template]
```

#### 选项

```
-A, --all-namespaces    获取用户具有权限的所有 Namespace（Project）中的资源。
-o, --output string     指定输出信息的形式。可选值有 `json`，`yaml` 和默认的 `template`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

以默认格式查看 Project example 下所有 BeamJob：

```
t9k bj get -p example
```

以默认格式查看所有 Project 下的所有 BeamJob：

```
t9k bj get -A
```

以默认格式查看 Project example 下名为 foo 和 bar 的两个 BeamJob：

```
t9k bj get foo bar -p example
```

以 yaml 格式查看 Project example 下名为 foo 的 BeamJob：

```
t9k bj get foo -p example -o yaml
```

### logs

查看 BeamJob 某个计算节点的日志。

#### 使用

```
t9k bj logs [--type=jobmanager|taskmanager|batchjob] [--index=<replicaIndex>] [--container=<containerName>] [-f] [--tail] [--timestamps]
```

#### 选项

```
--container string      字符串，指定要查看的 container 名称，如果计算节点的 container 不止 1 个，必须指定此项。
-f, --follow            流式查看日志。
--index string          字符串，要查看的计算节点的序号。默认值：0。
--tail int              整数，要查看的日志的行数（从后往前）。默认值：-1，查看全部日志。
--timestamps            是否展示时间戳。
--type string           字符串，要查看的计算节点的角色。可选值有 `taskmanager`，`batchjob` 以及默认值 `jobmanager`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project example 下 BeamJob foo 第 `replicaIndex` 个 `replicaType` 节点的日志：

```
t9k bj logs foo --type=replicaType --index=replicaIndex -p example
```

流式查看 Project example 下 BeamJob foo 第 `replicaIndex` 个 `replicaType` 节点的容器 `mnist` 的日志：

```
t9k bj logs foo --type=replicaType --index=replicaIndex --container=mnist --follow
```

查看 BeamJob foo 第 0 个 jobmanager 节点的最后 20 行日志：

```
t9k bj logs foo --tail 20
```

### wait

等待 BeamJob 完成。

#### 使用

```
t9k bj wait <name> [--timeout=<timeoutTime>] [--period=<periodTime>] [--print-log [--type=jobmanager|taskmanager|batchjob] [--index=<replicaIndex>] [--container=<containerName>] [--timestamps]]
```

#### 选项

```
--timeout string        字符串，最长等待时间。默认值："1h"，1 小时。
--period  string        字符串，检查任务是否完成的周期。默认值："1s"，每秒检查一次。
--print-log             是否在等待时流式查看日志。

以下参数只有在开启了 `--print-log` 后才生效。

--container string      字符串，指定要查看的 container 名称，如果计算节点的 container 不止 1 个，必须指定此项。
--index string          字符串，要查看的计算节点的序号。默认值：0。
--timestamps            是否展示时间戳。
--type string           字符串，要查看的计算节点的角色。可选值有 `taskmanager`，`batchjob` 以及默认值 `jobmanager`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

等待 Project example 下的 BeamJob foo 完成：

```
t9k bj wait foo -p example
```

等待 Project example 下的 BeamJob foo 完成，只等待 10 分钟：

```
t9k bj wait foo -p example --timeout 10m
```

等待 Project example 下的 BeamJob foo 完成，同时打印节点 flinkcluster-taskmanager-0 的日志：

```
t9k bj wait foo -p example --print-log --type taskmanager --index 0
```

## colossalaijob

用于管理 [ColossalAIJob](../../modules/jobs/colossalaijob.md)。

<aside class="note info">
<div class="title">信息</div>

支持使用缩写 `caij` 代替 `colossalaijob`。

</aside>

### delete

删除指定的 ColossalAIJob。

#### 使用

```
t9k colossalaijob delete [names...] [--all] [-f]
```

`t9k colossalaijob delete` 也可以用 `t9k caij rm` 代替。

#### 选项

```
--all                   删除当前 Project 中所有的 ColossalAIJob。
-f, --force             跳过确认，直接执行删除操作。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

删除 Project demo 下名为 foo 和 bar 的两个 ColossalAIJob：

```
t9k colossalaijob delete foo bar -p demo
```

跳过确认，直接删除 Project demo 下名为 foo 的 ColossalAIJob：

```
t9k colossalaijob delete foo -p demo -f
```

删除 Project demo 下所有的 ColossalAIJob：

```
t9k colossalaijob delete foo -p demo --all
```

### describe

查看某个 ColossalAIJob 的详细信息。

#### 使用

```
t9k caij describe <name>
```

`t9k caij describe` 也可以用 `t9k caij desc` 代替。

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project demo 下名为 foo 的 ColossalAIJob 的详细描述：

```
t9k caij describe foo -p demo
```

### get

查看 ColossalAIJob 相关信息。

#### 使用

```
t9k caij get [names...] [-A] [-o json|yaml|template]
```

#### 选项

```
-A, --all-namespaces    获取用户具有权限的所有 Namespace（Project）中的资源。
-o, --output string     指定输出信息的形式。可选值有 `json`，`yaml` 和默认的 `template`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

以默认格式查看 Project example 下所有 ColossalAIJob：

```
t9k caij get -p example
```

以默认格式查看所有 Project 下的所有 ColossalAIJob：

```
t9k caij get -A
```

以默认格式查看 Project example 下名为 foo 和 bar 的两个 ColossalAIJob：

```
t9k caij get foo bar -p example
```

以 yaml 格式查看 Project example 下名为 foo 的 ColossalAIJob：

```
t9k caij get foo -p example -o yaml
```

### logs

查看 ColossalAIJob 某个计算节点的日志。

#### 使用

```
t9k caij logs [--type=master|worker] [--index=<replicaIndex>] [--container=<containerName>] [-f] [--tail] [--timestamps]
```

#### 选项

```
--container string      字符串，指定要查看的 container 名称，如果计算节点的 container 不止 1 个，必须指定此项。
-f, --follow            流式查看日志。
--index string          字符串，要查看的计算节点的序号。默认值：0。
--tail int              整数，要查看的日志的行数（从后往前）。默认值：-1，查看全部日志。
--timestamps            是否展示时间戳。
--type string           字符串，要查看的计算节点的角色。可选值有 `master` 以及默认值 `worker`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project example 下 ColossalAIJob foo 第 `replicaIndex` 个 `replicaType` 节点的日志：

```
t9k caij logs foo --type=replicaType --index=replicaIndex -p example
```

流式查看 Project example 下 ColossalAIJob foo 第 `replicaIndex` 个 `replicaType` 节点的容器 `mnist` 的日志：

```
t9k caij logs foo --type=replicaType --index=replicaIndex --container=mnist --follow
```

查看 ColossalAIJob foo 第 0 个 worker 节点的最后 20 行日志：

```
t9k caij logs foo --tail 20
```

### wait

等待 ColossalAIJob 完成。

#### 使用

```
t9k caij wait <name> [--timeout=<timeoutTime>] [--period=<periodTime>] [--print-log [--type=master|worker] [--index=<replicaIndex>] [--container=<containerName>] [--timestamps]]
```

#### 选项

```
--timeout string        字符串，最长等待时间。默认值："1h"，1 小时。
--period  string        字符串，检查任务是否完成的周期。默认值："1s"，每秒检查一次。
--print-log             是否在等待时流式查看日志。

以下参数只有在开启了 `--print-log` 后才生效。

--container string      字符串，指定要查看的 container 名称，如果计算节点的 container 不止 1 个，必须指定此项。
--index string          字符串，要查看的计算节点的序号。默认值：0。
--timestamps            是否展示时间戳。
--type string           字符串，要查看的计算节点的角色。可选值有 `master` 以及默认值 `worker`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```
#### 示例

等待 Project example 下的 ColossalAIJob foo 完成：

```
t9k caij wait foo -p example
```

等待 Project example 下的 ColossalAIJob foo 完成，只等待 10 分钟：

```
t9k caij wait foo -p example --timeout 10m
```

等待 Project example 下的 ColossalAIJob foo 完成，同时打印节点 master-0 的日志：

```
t9k caij wait foo -p example --print-log --type master --index 0
```

## config

对指定的 [T9k Config](./guide.md#配置文件) 进行生成、管理、查看。T9k Config 默认使用文件 `${HOME}/.t9k/t9k-config.yaml`，可通过全局选项 `-c, --config` 指定该文件路径。

### auth

完成用户身份认证，生成 T9k Config。用户第一次使用 T9k 命令行工具时，需要使用此命令来进行身份认证。认证成功后，此命令会修改（如果是首次认证会新建）T9k Config。之后用户便可以通过该认证信息去使用 T9k 其他命令。

#### 使用

```
t9k config auth <server> [--apikey] [--user=<username>]
```

#### 选项

```
-k, --apikey            启用交互式输入 API Key。
-u, --user string       字符串，指定用户密码登录的用户名称。
```

#### 全局选项

```
-c, --config            字符串，指定要查看、修改的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定新增 Context 的名称。
-h, --help              查看当前指令的帮助信息和示例。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

##### 通过用户密码完成认证

用户指定要登录的域名，然后输入用户名和密码完成认证。认证完成后，当前的 T9k Config 中便会新增一个 `<用户名>-<域名>` 的 Context，用户也可以自己指定 Context 的名称。

```
$ t9k config auth <http://example.com>
Authenticating using username and password by default, add --apikey to use apikey.
Please enter your username: demo
Please enter your password:
Please enter Context name [default: demo-example.com]: demo
Login succeeded!
```

!!! note "注意" 
    Context 的名称需要满足 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names">DNS Subdomain Names</a> 的要求，如果 Context 名字重复，可以选择覆盖原内容或者重新输入。

##### 通过 API Key 完成认证

用户指定要登录的域名，然后输入 API Key。认证完成后，当前的 T9k Config 中便会新增一个 `apikey-<hash>-<域名>` 的 Context，用户也可以自己指定 Context 的名称。

```
$ t9k config auth <http://example.com> --apikey
Authenticating using API Key...
Please enter your API Key:
Please enter Context name [default: apikey-<hash>-example.com]: demo-apikey
Login succeeded!
```

### delete-context

删除指定的 Context。

!!! note "注意" 
    即使指定的 Context 是 current-context，此命令也会直接删除掉。所以务必确认之后再删除。

#### 使用

```
t9k config delete-context <name>
```

#### 全局选项

```
-c, --config            字符串，指定要查看、修改的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-h, --help              查看当前指令的帮助信息和示例。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

删除 Context demo：

```
t9k config delete-context demo
```

### get-contexts

用于获取当前使用的 T9k Config 中 Context 的相关信息。具体包括：

* `CURRENT`：是否是当前正在使用的 Context
* `NAME`：Context 的名称
* `SERVER`：T9k 平台的地址
* `AUTH_TYPE`：认证信息的类型（token 或者 apikey）

#### 使用

```
t9k config get-contexts [name] 
```

#### 全局选项

```
-c, --config            字符串，指定要查看、修改的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-h, --help              查看当前指令的帮助信息和示例。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

获取当前 T9k Config 中所有 Context 的信息：

```
t9k config get-contexts
```

获取指定 Context 的信息：

```
t9k config get-contexts my-context
```

### use-context

切换当前使用的 Context，此命令会修改当前 T9k Config 中 current-context 的值。

#### 使用

```
t9k config use-context <name>
```

#### 全局选项

```
-c, --config            字符串，指定要查看、修改的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-h, --help              查看当前指令的帮助信息和示例。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

切换到 Context foo：

```
t9k config use-context foo
```

将文件 `$HOME/t9kConfig.yaml` 下的 Context 切换到 foo：

```
t9k config use-context foo -c $HOME/t9kConfig.yaml
```

## create

通过文件创建 TensorStack AI 平台的资源或者其他支持的资源 （PVC 和 secret）。

#### 使用

```
t9k create --filename=<file>
```

#### 选项

```
-f, --filename          文件路径
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

通过文件在 Project demo 下创建一个 Notebook 资源。

```
t9k create -f notebook.yaml -p demo
```

## delete

根据文件删除资源。

#### 使用

```
t9k delete --filename=<file>
```

#### 选项

```
-f, --filename          文件路径
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

根据文件内容删除 Project demo 下相应的 Notebook 资源。

```
t9k delete -f notebook.yaml -p demo
```

## deepspeedjob

用于管理 [DeepSpeedJob](../../modules/jobs/deepspeedjob.md)。

<aside class="note info">
<div class="title">信息</div>

支持使用缩写 `dj` 代替 `deepspeedjob`。

</aside>

### delete

删除指定的 DeepSpeedJob。

#### 使用

```
t9k deepspeedjob delete [names...] [--all] [-f]
```

`t9k deepspeedjob delete` 也可以用 `t9k dj rm` 代替。

#### 选项

```
--all                   删除当前 Project 中所有的 DeepSpeedJob。
-f, --force             跳过确认，直接执行删除操作。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

删除 Project demo 下名为 foo 和 bar 的两个 DeepSpeedJob：

```
t9k deepspeedjob delete foo bar -p demo
```

跳过确认，直接删除 Project demo 下名为 foo 的 DeepSpeedJob：

```
t9k deepspeedjob delete foo -p demo -f
```

删除 Project demo 下所有的 DeepSpeedJob：

```
t9k deepspeedjob delete foo -p demo --all
```

### describe

查看某个 DeepSpeedJob 的详细信息。

#### 使用

```
t9k dj describe <name>
```

`t9k dj describe` 也可以用 `t9k dj desc` 代替。

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project demo 下名为 foo 的 DeepSpeedJob 的详细描述：

```
t9k dj describe foo -p demo
```

### get

查看 DeepSpeedJob 相关信息。

#### 使用

```
t9k dj get [names...] [-A] [-o json|yaml|template]
```

#### 选项

```
-A, --all-namespaces    获取用户具有权限的所有 Namespace（Project）中的资源。
-o, --output string     指定输出信息的形式。可选值有 `json`，`yaml` 和默认的 `template`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

以默认格式查看 Project example 下所有 DeepSpeedJob：

```
t9k dj get -p example
```

以默认格式查看所有 Project 下的所有 DeepSpeedJob：

```
t9k dj get -A
```

以默认格式查看 Project example 下名为 foo 和 bar 的两个 DeepSpeedJob：

```
t9k dj get foo bar -p example
```

以 yaml 格式查看 Project example 下名为 foo 的 DeepSpeedJob：

```
t9k dj get foo -p example -o yaml
```

### logs

查看 DeepSpeedJob 某个计算节点的日志。

#### 使用

```
t9k dj logs [--type=master|worker] [--index=<replicaIndex>] [--container=<containerName>] [-f] [--tail] [--timestamps]
```

#### 选项

```
--container string      字符串，指定要查看的 container 名称，如果计算节点的 container 不止 1 个，必须指定此项。
-f, --follow            流式查看日志。
--index string          字符串，要查看的计算节点的序号。默认值：0。
--tail int              整数，要查看的日志的行数（从后往前）。默认值：-1，查看全部日志。
--timestamps            是否展示时间戳。
--type string           字符串，要查看的计算节点的角色。可选值有 `master` 以及默认值 `worker`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project example 下 DeepSpeedJob foo 第 `replicaIndex` 个 `replicaType` 节点的日志：

```
t9k dj logs foo --type=replicaType --index=replicaIndex -p example
```

流式查看 Project example 下 DeepSpeedJob foo 第 `replicaIndex` 个 `replicaType` 节点的容器 `mnist` 的日志：

```
t9k dj logs foo --type=replicaType --index=replicaIndex --container=mnist --follow
```

查看 DeepSpeedJob foo 第 0 个 worker 节点的最后 20 行日志：

```
t9k dj logs foo --tail 20
```

### wait

等待 DeepSpeedJob 完成。

#### 使用

```
t9k dj wait <name> [--timeout=<timeoutTime>] [--period=<periodTime>] [--print-log [--type=master|worker] [--index=<replicaIndex>] [--container=<containerName>] [--timestamps]]
```

#### 选项

```
--timeout string        字符串，最长等待时间。默认值："1h"，1 小时。
--period  string        字符串，检查任务是否完成的周期。默认值："1s"，每秒检查一次。
--print-log             是否在等待时流式查看日志。

以下参数只有在开启了 `--print-log` 后才生效。

--container string      字符串，指定要查看的 container 名称，如果计算节点的 container 不止 1 个，必须指定此项。
--index string          字符串，要查看的计算节点的序号。默认值：0。
--timestamps            是否展示时间戳。
--type string           字符串，要查看的计算节点的角色。可选值有 `master` 以及默认值 `worker`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

等待 Project example 下的 DeepSpeedJob foo 完成：

```
t9k dj wait foo -p example
```

等待 Project example 下的 DeepSpeedJob foo 完成，只等待 10 分钟：

```
t9k dj wait foo -p example --timeout 10m
```

等待 Project example 下的 DeepSpeedJob foo 完成，同时打印节点 master-0 的日志：

```
t9k dj wait foo -p example --print-log --type master --index 0
```

## genericjob

用于管理 [GenericJob](../../modules/jobs/genericjob.md)。

<aside class="note info">
<div class="title">信息</div>

支持使用缩写 `gj` 代替 `genericjob`。

</aside>

### delete

删除指定的 GenericJob。

#### 使用

```
t9k genericjob delete [names...] [--all] [-f]
```

`t9k genericjob delete` 也可以用 `t9k gj rm` 代替。

#### 选项

```
--all                   删除当前 Project 中所有的 GenericJob。
-f, --force             跳过确认，直接执行删除操作。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

删除 Project demo 下名为 foo 和 bar 的两个 GenericJob：

```
t9k genericjob delete foo bar -p demo
```

跳过确认，直接删除 Project demo 下名为 foo 的 GenericJob：

```
t9k genericjob delete foo -p demo -f
```

删除 Project demo 下所有的 GenericJob：

```
t9k genericjob delete foo -p demo --all
```

### describe

查看某个 GenericJob 的详细信息。

#### 使用

```
t9k gj describe <name>
```

`t9k gj describe` 也可以用 `t9k gj desc` 代替。

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project demo 下名为 foo 的 GenericJob 的详细描述：

```
t9k gj describe foo -p demo
```

### get

查看 GenericJob 相关信息。

#### 使用

```
t9k gj get [names...] [-A] [-o json|yaml|template]
```

#### 选项

```
-A, --all-namespaces    获取用户具有权限的所有 Namespace（Project）中的资源。
-o, --output string     指定输出信息的形式。可选值有 `json`，`yaml` 和默认的 `template`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

以默认格式查看 Project example 下所有 GenericJob：

```
t9k gj get -p example
```

以默认格式查看所有 Project 下的所有 GenericJob：

```
t9k gj get -A
```

以默认格式查看 Project example 下名为 foo 和 bar 的两个 GenericJob：

```
t9k gj get foo bar -p example
```

以 yaml 格式查看 Project example 下名为 foo 的 GenericJob：

```
t9k gj get foo -p example -o yaml
```

### logs

查看 GenericJob 某个计算节点的日志。

#### 使用

```
t9k gj logs [--type=master|worker] [--index=<replicaIndex>] [--container=<containerName>] [-f] [--tail] [--timestamps]
```

#### 选项

```
--container string      字符串，指定要查看的 container 名称，如果计算节点的 container 不止 1 个，必须指定此项。
-f, --follow            流式查看日志。
--index string          字符串，要查看的计算节点的序号。默认值：0。
--tail int              整数，要查看的日志的行数（从后往前）。默认值：-1，查看全部日志。
--timestamps            是否展示时间戳。
--type string           字符串，要查看的计算节点的角色。可选值有 `master` 以及默认值 `worker`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project example 下 GenericJob foo 第 `replicaIndex` 个 `replicaType` 节点的日志：

```
t9k gj logs foo --type=replicaType --index=replicaIndex -p example
```

流式查看 Project example 下 GenericJob foo 第 `replicaIndex` 个 `replicaType` 节点的容器 `mnist` 的日志：

```
t9k gj logs foo --type=replicaType --index=replicaIndex --container=mnist --follow
```

查看 GenericJob foo 第 0 个 worker 节点的最后 20 行日志：

```
t9k gj logs foo --tail 20
```

### wait

等待 GenericJob 完成。

#### 使用

```
t9k gj wait <name> [--timeout=<timeoutTime>] [--period=<periodTime>] [--print-log [--type=master|worker] [--index=<replicaIndex>] [--container=<containerName>] [--timestamps]]
```

#### 选项

```
--timeout string        字符串，最长等待时间。默认值："1h"，1 小时。
--period  string        字符串，检查任务是否完成的周期。默认值："1s"，每秒检查一次。
--print-log             是否在等待时流式查看日志。

以下参数只有在开启了 `--print-log` 后才生效。

--container string      字符串，指定要查看的 container 名称，如果计算节点的 container 不止 1 个，必须指定此项。
--index string          字符串，要查看的计算节点的序号。默认值：0。
--timestamps            是否展示时间戳。
--type string           字符串，要查看的计算节点的角色。可选值有 `master` 以及默认值 `worker`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

等待 Project example 下的 GenericJob foo 完成：

```
t9k gj wait foo -p example
```

等待 Project example 下的 GenericJob foo 完成，只等待 10 分钟：

```
t9k gj wait foo -p example --timeout 10m
```

等待 Project example 下的 GenericJob foo 完成，同时打印节点 master-0 的日志：

```
t9k gj wait foo -p example --print-log --type master --index 0
```

## mlservice

用于管理 [MLService](../../modules/deployment/mlservice.md)。

<aside class="note info">
<div class="title">信息</div>

支持使用缩写 `mls` 代替 `mlservice`。

</aside>

### canary

设置[金丝雀发布](../../modules/deployment/mlservice.md#金丝雀发布)。

#### 使用

```
t9k mlservice set-canary [--default=default-release] [--canary=canary-release] [--traffic=canary-percentage] [--dry-run] [-o yaml|json]
```

#### 选项

```
--canary string         字符串，指定金丝雀发布的版本名称
--default string        字符串，指定默认发布的版本名称
--dry-run               只打印更新后的 yaml 文件，但是不执行 apply 操作。
-o, --output string     字符串，指定 --dry-run 打印的格式。可选值有 `json`，`yaml`。
--traffic int           整数，指定金丝雀发布的路由权重
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

将 Project demo 下 MLService maskdetection 的默认发布版本设为 `foo`，金丝雀发布版本设为 `bar` 且权重为 20%：

```
t9k mlservice set-canary maskdetection --default=foo --canary=bar --traffic=20 -n demo
```

将 Project demo 下 MLService maskdetection 的金丝雀发布版本权重设为 30%：

```
t9k mlservice set-canary maskdetection --traffic=30 -n demo
```

将 Project demo 下 MLService maskdetection 的默认发布版本设为 `foo`：

```
t9k mlservice set-canary maskdetection --default=foo
```
将 Project demo 下 MLService maskdetection 的金丝雀发布版本设为 `bar`：

```
t9k mlservice set-canary maskdetection --canary=bar -n demo
```

### delete

删除指定的 MLService。

#### 使用

```
t9k mls delete [names...] [-f] [--all]
```

`t9k mls delete` 也可以用 `t9k mls rm` 代替。

#### 选项

```
--all                   删除当前 Project 中所有的 XGBoostTrainingJob。
-f, --force             跳过确认，直接执行删除操作。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

删除 Project demo 下名为 foo 和 bar 的两个 MLService：

```
t9k mls delete foo bar -p demo
```

跳过确认，直接删除 Project demo 下名为 foo 的 MLService：

```
t9k mls delete foo -p demo -f
```

删除 Project demo 下所有的 MLService：

```
t9k mls delete foo -p demo --all
```

### describe

查看 MLService 详细信息。

#### 使用

```
t9k mls describe <name> [--color]
```

#### 选项

```
--color                 使用彩色的输出信息（默认全是黑色）。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project demo 下名为 foo 的 MLService 的详细描述：

```
t9k mls describe foo -p demo
```

### get

查看 MLService 相关信息。

#### 使用

```
t9k mls get [names...] [-A] [-o json|yaml|template]
```

#### 选项

```
-A, --all-namespaces       获取用户具有权限的所有 Namespace（Project）中的资源。
-o, --output string        指定输出信息的形式。可选值有 `json`，`yaml` 和默认的 `template`
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

以默认格式查看 Project example 下所有 MLService：

```
t9k mls get -p example
```

以默认格式查看所有 Project 下的所有 MLService：

```
t9k mls get -A
```

以默认格式查看 Project example 下名为 foo 和 bar 的两个 MLService：

```
t9k mls get foo bar -p example
```

以 yaml 格式查看 Project example 下名为 foo 的 MLService：

```
t9k mls get foo -p example -o yaml
```

### delete-release

删除 MLService 中发布的版本。

#### 使用

```
t9k delete-release <name> [--release=release-names...]
```

#### 选项

```
--release string        字符串，删除的版本名称，如要删除多个版本，用 `,` 进行分割。
--dry-run               只打印更新后的 yaml 文件，但是不执行 apply 操作。
-o, --output string     字符串，指定 --dry-run 打印的格式。可选值有 `json`，`yaml`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

删除 Project demo 下的推理服务 maskdetection 的 foo 和 bar 两个已发布的版本：

```
t9k delete-release maskdetection --release foo,bar -p demo
```

## mpijob

用于管理 [MPIJob](../../modules/jobs/mpijob.md)。

<aside class="note info">
<div class="title">信息</div>

支持使用缩写 `mj` 代替 `mpijob`。

</aside>

### delete

删除指定的 MPIJob。

#### 使用

```
t9k mpijob delete [names...] [--all] [-f]
```

`t9k mpijob delete` 也可以用 `t9k mj rm` 代替。

#### 选项

```
--all                   删除当前 Project 中所有的 MPIJob。
-f, --force             跳过确认，直接执行删除操作。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

删除 Project demo 下名为 foo 和 bar 的两个 MPIJob：

```
t9k mpijob delete foo bar -p demo
```

跳过确认，直接删除 Project demo 下名为 foo 的 MPIJob：

```
t9k mpijob delete foo -p demo -f
```

删除 Project demo 下所有的 MPIJob：

```
t9k mpijob delete foo -p demo --all
```

### describe

查看某个 MPIJob 的详细信息。

#### 使用

```
t9k mj describe <name>
```

`t9k mj describe` 也可以用 `t9k mj desc` 代替。

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project demo 下名为 foo 的 MPIJob 的详细描述：

```
t9k mj describe foo -p demo
```

### get

查看 MPIJob 相关信息。

#### 使用

```
t9k mj get [names...] [-A] [-o json|yaml|template]
```

#### 选项

```
-A, --all-namespaces    获取用户具有权限的所有 Namespace（Project）中的资源。
-o, --output string     指定输出信息的形式。可选值有 `json`，`yaml` 和默认的 `template`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

以默认格式查看 Project example 下所有 MPIJob：

```
t9k mj get -p example
```

以默认格式查看所有 Project 下的所有 MPIJob：

```
t9k mj get -A
```

以默认格式查看 Project example 下名为 foo 和 bar 的两个 MPIJob：

```
t9k mj get foo bar -p example
```

以 yaml 格式查看 Project example 下名为 foo 的 MPIJob：

```
t9k mj get foo -p example -o yaml
```

### logs

查看 MPIJob 某个计算节点的日志。

#### 使用

```
t9k mj logs [--type=launcher|worker] [--index=<replicaIndex>] [--container=<containerName>] [-f] [--tail] [--timestamps]
```

#### 选项

```
--container string      字符串，指定要查看的 container 名称，如果计算节点的 container 不止 1 个，必须指定此项。
-f, --follow            流式查看日志。
--index string          字符串，要查看的计算节点的序号。默认值：0。
--tail int              整数，要查看的日志的行数（从后往前）。默认值：-1，查看全部日志。
--timestamps            是否展示时间戳。
--type string           字符串，要查看的计算节点的角色。可选值有 `launcher` 以及默认值 `worker`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project example 下 MPIJob foo 第 `replicaIndex` 个 `replicaType` 节点的日志：

```
t9k mj logs foo --type=replicaType --index=replicaIndex -p example
```

流式查看 Project example 下 MPIJob foo 第 `replicaIndex` 个 `replicaType` 节点的容器 `mnist` 的日志：

```
t9k mj logs foo --type=replicaType --index=replicaIndex --container=mnist --follow
```

查看 MPIJob foo 第 0 个 worker 节点的最后 20 行日志：

```
t9k mj logs foo --tail 20
```

### wait

等待 MPIJob 完成。

#### 使用

```
t9k mj wait <name> [--timeout=<timeoutTime>] [--period=<periodTime>] [--print-log [--type=launcher|worker] [--index=<replicaIndex>] [--container=<containerName>] [--timestamps]]
```

#### 选项

```
--timeout string        字符串，最长等待时间。默认值："1h"，1 小时。
--period  string        字符串，检查任务是否完成的周期。默认值："1s"，每秒检查一次。
--print-log             是否在等待时流式查看日志。

以下参数只有在开启了 `--print-log` 后才生效。

--container string      字符串，指定要查看的 container 名称，如果计算节点的 container 不止 1 个，必须指定此项。
--index string          字符串，要查看的计算节点的序号。默认值：0。
--timestamps            是否展示时间戳。
--type string           字符串，要查看的计算节点的角色。可选值有 `launcher` 以及默认值 `worker`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

等待 Project example 下的 MPIJob foo 完成：

```
t9k mj wait foo -p example
```

等待 Project example 下的 MPIJob foo 完成，只等待 10 分钟：

```
t9k mj wait foo -p example --timeout 10m
```

等待 Project example 下的 MPIJob foo 完成，同时打印节点 launcher 的日志：

```
t9k mj wait foo -p example --print-log --type launcher
```

## notebook

用于管理 [Notebook](../../modules/building/notebook.md)。

<aside class="note info">
<div class="title">信息</div>

支持使用缩写 `nb` 代替 `notebook`。

</aside>

### delete

删除指定的 Notebook。

#### 使用

```
t9k notebook delete [names...] [--all] [-f]
```

`t9k notebook delete` 也可以用 `t9k nb rm` 代替。

#### 选项

```
--all                   删除当前 Project 中所有的 Notebook。
-f, --force             跳过确认，直接执行删除操作。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

删除 Project demo 下名为 foo 和 bar 的两个 Notebook：

```
t9k notebook delete foo bar -p demo
```

跳过确认，直接删除 Project demo 下名为 foo 的 Notebook：

```
t9k notebook delete foo -p demo -f
```

删除 Project demo 下所有的 Notebook：

```
t9k notebook delete foo -p demo --all
```

### describe

查看某个 Notebook 的详细信息。

#### 使用

```
t9k nb describe <name>
```

`t9k nb describe` 也可以用 `t9k nb desc` 代替。

#### 选项

```
--color                 使用彩色的输出信息（默认全是黑色）。
```
#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project demo 下名为 foo 的 Notebook 的详细描述：

```
t9k nb describe foo -p demo
```

### get

查看 Notebook 相关信息。

#### 使用

```
t9k nb get [names...] [-A] [-o json|yaml|template]
```

#### 选项

```
-A, --all-namespaces    获取用户具有权限的所有 Namespace（Project）中的资源。
-o, --output string     字符串，指定输出信息的形式。可选值有 `json`，`yaml` 和默认的 `template`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

以默认格式查看 Project example 下所有 Notebook：

```
t9k nb get -p example
```

以默认格式查看所有 Project 下的所有 Notebook：

```
t9k nb get -A
```

以默认格式查看 Project example 下名为 foo 和 bar 的两个 Notebook：

```
t9k nb get foo bar -p example
```

以 yaml 格式查看 Project example 下名为 foo 的 Notebook：

```
t9k nb get foo -p example -o yaml
```

## podgroup

用于管理 [PodGroup](../../modules/computing-resources/podgroup.md)，只有集群管理员才有相关权限。

### get 

查看 PodGroup 相关信息。

#### 使用

```
t9k podgroup get [names...] [-A] [-o json|yaml|template]
```

#### 选项

```
-A, --all-namespaces       获取用户具有权限的所有 Namespace（Project）中的资源。
-o, --output string        指定输出信息的形式。可选值有 `json`，`yaml` 和默认的 `template`
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例


以默认格式查看 Project example 下所有 PodGroup：

```
t9k podgroup get -p example
```

以默认格式查看所有 Project 下的所有 PodGroup：

```
t9k podgroup get -A
```

以默认格式查看 Project example 下名为 foo 和 bar 的两个 PodGroup：

```
t9k podgroup get foo bar -p example
```

以 yaml 格式查看 Project example 下名为 foo 的 PodGroup：

```
t9k podgroup get foo -p example -o yaml
```

## project

用于管理 [Project](../../modules/account-and-security.md#project)。

<aside class="note info">
<div class="title">信息</div>

支持使用缩写 `proj` 代替 `project`。

</aside>

### create

创建新项目，只有集群管理员才有权限创建新项目。

#### 使用

```
t9k project create <name> <owner> [--build] [--deploy]
```

#### 选项

```
--build                 项目拥有者是否拥有模型构建权限
--deploy                项目拥有者是否拥有模型部署权限
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

创建一个名为 sample 的项目，管理员为 admin，且 admin 只有模型构建的权限，没有模型部署的权限：

```
t9k project create sample admin --build
```

### describe

查看项目详细描述，只能查看当前用户所拥有的项目。

#### 使用

```
t9k proj describe <name>
```

`t9k proj describe` 也可以用 `t9k proj desc` 代替。

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

详细描述项目 demo：

```
t9k proj describe demo
```

### get

查看项目的相关信息，只能查看用户拥有权限的项目。

#### 使用

```
t9k project get [name...]
```

可以通过指定 name 获取一个或多个 project，不指定的话默认获取所有当前用户有权限的项目。

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看当前用户有权限的所有项目：

```
t9k project get
```

查看当前用户有权限的项目中名为 foo 的项目：

```
t9k project get foo
```

## pytorchtrainingjob

用于管理 [PyTorchTrainingJob](../../modules/jobs/pytorchtrainingjob.md)。

<aside class="note info">
<div class="title">信息</div>

支持使用缩写 `pj` 代替 `pytorchtrainingjob`。

</aside>

### delete

删除指定的 PyTorchTrainingJob。

#### 使用

```
t9k pytorchtrainingjob delete [names...] [--all] [-f]
```

`t9k pytorchtrainingjob delete` 也可以用 `t9k pj rm` 代替。

#### 选项

```
--all                   删除当前 Project 中所有的 PyTorchTrainingJob。
-f, --force             跳过确认，直接执行删除操作。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

删除 Project demo 下名为 foo 和 bar 的两个 PyTorchTrainingJob：

```
t9k pytorchtrainingjob delete foo bar -p demo
```

跳过确认，直接删除 Project demo 下名为 foo 的 PyTorchTrainingJob：

```
t9k pytorchtrainingjob delete foo -p demo -f
```

删除 Project demo 下所有的 PyTorchTrainingJob：

```
t9k pytorchtrainingjob delete foo -p demo --all
```

### describe

查看某个 PyTorchTrainingJob 的详细信息。

#### 使用

```
t9k pj describe <name>
```

`t9k pj describe` 也可以用 `t9k pj desc` 代替。

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project demo 下名为 foo 的 PyTorchTrainingJob 的详细描述：

```
t9k pj describe foo -p demo
```

### get

查看 PyTorchTrainingJob 相关信息。

#### 使用

```
t9k pj get [names...] [-A] [-o json|yaml|template]
```

#### 选项

```
-A, --all-namespaces    获取用户具有权限的所有 Namespace（Project）中的资源。
-o, --output string     指定输出信息的形式。可选值有 `json`，`yaml` 和默认的 `template`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

以默认格式查看 Project example 下所有 PyTorchTrainingJob：

```
t9k pj get -p example
```

以默认格式查看所有 Project 下的所有 PyTorchTrainingJob：

```
t9k pj get -A
```

以默认格式查看 Project example 下名为 foo 和 bar 的两个 PyTorchTrainingJob：

```
t9k pj get foo bar -p example
```

以 yaml 格式查看 Project example 下名为 foo 的 PyTorchTrainingJob：

```
t9k pj get foo -p example -o yaml
```

### logs

查看 PyTorchTrainingJob 某个计算节点的日志。

#### 使用

```
t9k pj logs [--type=master|worker] [--index=<replicaIndex>] [--container=<containerName>] [-f] [--tail] [--timestamps]
```

#### 选项

```
--container string      字符串，指定要查看的 container 名称，如果计算节点的 container 不止 1 个，必须指定此项。
-f, --follow            流式查看日志。
--index string          字符串，要查看的计算节点的序号。默认值：0。
--tail int              整数，要查看的日志的行数（从后往前）。默认值：-1，查看全部日志。
--timestamps            是否展示时间戳。
--type string           字符串，要查看的计算节点的角色。可选值有 `master` 以及默认值 `worker`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project example 下 PyTorchTrainingJob foo 第 `replicaIndex` 个 `replicaType` 节点的日志：

```
t9k pj logs foo --type=replicaType --index=replicaIndex -p example
```

流式查看 Project example 下 PyTorchTrainingJob foo 第 `replicaIndex` 个 `replicaType` 节点的容器 `mnist` 的日志：

```
t9k pj logs foo --type=replicaType --index=replicaIndex --container=mnist --follow
```

查看 PyTorchTrainingJob foo 第 0 个 worker 节点的最后 20 行日志：

```
t9k pj logs foo --tail 20
```

### wait

等待 PyTorchTrainingJob 完成。

#### 使用

```
t9k pj wait <name> [--timeout=<timeoutTime>] [--period=<periodTime>] [--print-log [--type=master|worker] [--index=<replicaIndex>] [--container=<containerName>] [--timestamps]]
```

#### 选项

```
--timeout string        字符串，最长等待时间。默认值："1h"，1 小时。
--period  string        字符串，检查任务是否完成的周期。默认值："1s"，每秒检查一次。
--print-log             是否在等待时流式查看日志。

以下参数只有在开启了 `--print-log` 后才生效。

--container string      字符串，指定要查看的 container 名称，如果计算节点的 container 不止 1 个，必须指定此项。
--index string          字符串，要查看的计算节点的序号。默认值：0。
--timestamps            是否展示时间戳。
--type string           字符串，要查看的计算节点的角色。可选值有 `master` 以及默认值 `worker`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

等待 Project example 下的 PyTorchTrainingJob foo 完成：

```
t9k pj wait foo -p example
```

等待 Project example 下的 PyTorchTrainingJob foo 完成，只等待 10 分钟：

```
t9k pj wait foo -p example --timeout 10m
```

等待 Project example 下的 PyTorchTrainingJob foo 完成，同时打印节点 master-0 的日志：

```
t9k pj wait foo -p example --print-log --type master --index 0
```

## queue

用于管理 [Queue](../../modules/computing-resources/queue.md)，只有集群管理员才有相关权限。

### close

关闭 Queue。

#### 使用

```
t9k queue close <name>
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

关闭 Queue foo：

```
t9k queue close foo
```

### get

查看 Queue 相关信息。

#### 使用

```
t9k queue get [names...] [-o json|yaml|template]
```

#### 选项

```
-o, --output string        指定输出信息的形式。可选值有 `json`，`yaml` 和默认的 `template`
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

以默认格式查看所有 Queue：

```
t9k queue get
```

以默认格式查看名为 foo 和 bar 的两个 Queue：

```
t9k queue get foo bar
```

以 yaml 格式查看名为 foo 的 Queue：

```
t9k queue get foo -o yaml
```

### open

打开 Queue。

#### 使用

```
t9k queue open <name>
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

打开 Queue foo：

```
t9k queue open foo
```

## simplemlservice

用于管理 [SimpleMLService](../../modules/deployment/simplemlservice.md)

<aside class="note info">
<div class="title">信息</div>

支持使用缩写 `smls` 代替 `simplemlservice`。

</aside>


### create

创建一个新的 SimpleMLService。

#### 使用

```
t9k simplemlservice create <name> --model=<model-url>  -image=<serving-image> [--secret=<serect-name>] [--tech tensorflow|pytorch|xgboost] [--dry-run] [-o yaml|json]
```

#### 选项

```
--model string          字符串，推理服务使用的模型地址
--image string          字符串，推理服务使用的镜像
--dry-run               只打印更新后的 yaml 文件，但是不执行 apply 操作。
-o, --output string     字符串，指定 --dry-run 打印的格式。可选值有 `json`，`yaml`。
--tech string           字符串，推理服务使用的机器学习框架，如果 image 中已经含有关键字，可不填此参数。可选值有 `tensorflow`，`pytorch`，`xgboost`。
--secret string         字符串，加载模型所使用的密钥名称
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

在 Project demo 下创建一个名为 mnist 的推理服务。其使用的镜像为`registry.tensorstack.dev/t9kmirror/tensorflow-serving:1.15.0`，模型地址为 `mms://aihub.tensorstack.dev/t9kpublic/mnist:v1`：
```
t9k simplemlservice create mnist \
  --model="mms://aihub.tensorstack.dev/t9kpublic/mnist:v1" \
  --image="registry.tensorstack.dev/t9kmirror/tensorflow-serving:1.15.0" \
  -n demo
```

在 Project t9k-sample 下创建一个名为 mnist-cnn 的推理服务。其使用的镜像为`registry.tensorstack.dev/t9kmirror/tensorflow-serving:1.15.0`，模型地址为 `mms://aihub.tensorstack.dev/private/mnist:v2`，模型下载使用的密钥为同一个 Project demo 下的 secret `mms-access`：

```
t9k mls create mnist-cnn \
  --project=t9k-sample \
  --model="mms://aihub.tensorstack.dev/private/mnist:v2" \
  --image="registry.tensorstack.dev/t9kmirror/tensorflow-serving:1.15.0" \
  --tech="tensorflow" \
  --secret="mms-access" 
```

### delete

删除指定的 SimpleMLService。

#### 使用

```
t9k smls delete [names...] [-f] [--all]
```

`t9k smls delete` 也可以用 `t9k smls rm` 代替。

#### 选项

```
--all                   删除当前 Project 中所有的 XGBoostTrainingJob。
-f, --force             跳过确认，直接执行删除操作。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

删除 Project demo 下名为 foo 和 bar 的两个 SimpleMLService：

```
t9k smls delete foo bar -p demo
```

跳过确认，直接删除 Project demo 下名为 foo 的 SimpleMLService：

```
t9k smls delete foo -p demo -f
```

删除 Project demo 下所有的 SimpleMLService：

```
t9k smls delete foo -p demo --all
```
### describe

查看 SimpleMLService 详细信息。

#### 使用

```
t9k mls describe <name>
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project demo 下名为 foo 的 SimpleMLService 的详细描述：

```
t9k mls describe foo -p demo
```

### get

查看 SimpleMLService 相关信息。

#### 使用

```
t9k smls get [names...] [-A] [-o json|yaml|template]
```

#### 选项

```
-A, --all-namespaces       获取用户具有权限的所有 Namespace（Project）中的资源。
-o, --output string        指定输出信息的形式。可选值有 `json`，`yaml` 和默认的 `template`
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

以默认格式查看 Project example 下所有 SimpleMLService：

```
t9k smls get -p example
```

以默认格式查看所有 Project 下的所有 SimpleMLService：

```
t9k smls get -A
```

以默认格式查看 Project example 下名为 foo 和 bar 的两个 SimpleMLService：

```
t9k smls get foo bar -p example
```

以 yaml 格式查看 Project example 下名为 foo 的 SimpleMLService：

```
t9k smls get foo -p example -o yaml
```

## tensorflowtrainingjob

用于管理 [TensorFlowTrainingJob](../../modules/jobs/tensorflowtrainingjob.md)。

<aside class="note info">
<div class="title">信息</div>

支持使用缩写 `tj` 代替 `tensorflowtrainingjob`。

</aside>

### delete

删除指定的 TensorFlowTrainingJob。

#### 使用

```
t9k tensorflowtrainingjob delete [names...] [--all] [-f]
```

`t9k tensorflowtrainingjob delete` 也可以用 `t9k tj rm` 代替。

#### 选项

```
--all                   删除当前 Project 中所有的 TensorFlowTrainingJob。
-f, --force             跳过确认，直接执行删除操作。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

删除 Project demo 下名为 foo 和 bar 的两个 TensorFlowTrainingJob：

```
t9k tensorflowtrainingjob delete foo bar -p demo
```

跳过确认，直接删除 Project demo 下名为 foo 的 TensorFlowTrainingJob：

```
t9k tensorflowtrainingjob delete foo -p demo -f
```

删除 Project demo 下所有的 TensorFlowTrainingJob：

```
t9k tensorflowtrainingjob delete foo -p demo --all
```

### describe

查看某个 TensorFlowTrainingJob 的详细信息。

#### 使用

```
t9k tj describe <name>
```

`t9k tj describe` 也可以用 `t9k tj desc` 代替。

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project demo 下名为 foo 的 TensorFlowTrainingJob 的详细描述：

```
t9k tj describe foo -p demo
```

### get

查看 TensorFlowTrainingJob 相关信息。

#### 使用

```
t9k tj get [names...] [-A] [-o json|yaml|template]
```

#### 选项

```
-A, --all-namespaces    获取用户具有权限的所有 Namespace（Project）中的资源。
-o, --output string     字符串，指定输出信息的形式。可选值有 `json`，`yaml` 和默认的 `template`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

以默认格式查看 Project example 下所有 TensorFlowTrainingJob：

```
t9k tj get -p example
```

以默认格式查看所有 Project 下的所有 TensorFlowTrainingJob：

```
t9k tj get -A
```

以默认格式查看 Project example 下名为 foo 和 bar 的两个 TensorFlowTrainingJob：

```
t9k tj get foo bar -p example
```

以 yaml 格式查看 Project example 下名为 foo 的 TensorFlowTrainingJob：

```
t9k tj get foo -p example -o yaml
```

### logs

查看 TensorFlowTrainingJob 某个计算节点的日志。

#### 使用

```
t9k tj logs <name> [--type=chief|ps|evaluator|worker] [--index=<replicaIndex>] [--container=<containerName>] [-f] [--tail] [--timestamps]
```

#### 选项

```
--container string      字符串，指定要查看的 container 名称，如果计算节点的 container 不止 1 个，必须指定此项。
-f, --follow            流式查看日志。
--index string          字符串，要查看的计算节点的序号。默认值：0。
--tail int              整数，要查看的日志的行数（从后往前）。默认值：-1，查看全部日志。
--timestamps            是否展示时间戳。
--type string           字符串，要查看的计算节点的角色。可选值有 `chief`，`ps`，`evaluator` 以及默认值 `worker`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project example 下 TensorFlowTrainingJob foo 第 `replicaIndex` 个 `replicaType` 节点的日志：

```
t9k tj logs foo --type=replicaType --index=replicaIndex -p example
```

流式查看 Project example 下 TensorFlowTrainingJob foo 第 `replicaIndex` 个 `replicaType` 节点的容器 `mnist` 的日志：

```
t9k tj logs foo --type=replicaType --index=replicaIndex --container=mnist --follow
```

查看 TensorFlowTrainingJob foo 第 0 个 worker 节点的最后 20 行日志：

```
t9k tj logs foo --tail 20
```

### wait

等待 TensorFlowTrainingJob 完成。

#### 使用

```
t9k tj wait <name> [--timeout=<timeoutTime>] [--period=<periodTime>] [--print-log [--type=chief|ps|evaluator|worker] [--index=<replicaIndex>] [--container=<containerName>] [--timestamps]]
```

#### 选项

```
--timeout string        字符串，最长等待时间。默认值："1h"，1 小时。
--period  string        字符串，检查任务是否完成的周期。默认值："1s"，每秒检查一次。
--print-log             是否在等待时流式查看日志。

以下参数只有在开启了 `--print-log` 后才生效。

--container string      字符串，指定要查看的 container 名称，如果计算节点的 container 不止 1 个，必须指定此项。
--index string          字符串，要查看的计算节点的序号。默认值：0。
--timestamps            是否展示时间戳。
--type string           字符串，要查看的计算节点的角色。可选值有 `chief`，`ps`，`evaluator` 以及默认值 `worker`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

等待 Project example 下的 TensorFlowTrainingJob foo 完成：

```
t9k tj wait foo -p example
```

等待 Project example 下的 TensorFlowTrainingJob foo 完成，只等待 10 分钟：

```
t9k tj wait foo -p example --timeout 10m
```

等待 Project example 下的 TensorFlowTrainingJob foo 完成，同时打印节点 chief-0 的日志：

```
t9k tj wait foo -p example --print-log --type chief --index 0
```

## version

查看当前 T9k CLI 版本信息。

#### 使用

```
t9k version
```

#### 示例

查看当前 t9k 二进制文件的版本信息。

```
t9k version
```

## workflowrun

用于管理 [WorkflowRun](../../modules/workflows/workflowrun.md)。

<aside class="note info">
<div class="title">信息</div>

支持使用缩写 `wr` 代替 `workflowrun`。

</aside>

### delete

删除指定的 WorkflowRun。

#### 使用

```
t9k workflowrun delete [names...] [--all] [-f]
```

`t9k workflowrun delete` 也可以用 `t9k wr rm` 代替。

#### 选项

```
--all                   删除当前 Project 中所有的 WorkflowRun。
-f, --force             跳过确认，直接执行删除操作。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

删除 Project demo 下名为 foo 和 bar 的两个 WorkflowRun：

```
t9k workflowrun delete foo bar -p demo
```

跳过确认，直接删除 Project demo 下名为 foo 的 WorkflowRun：

```
t9k workflowrun delete foo -p demo -f
```

删除 Project demo 下所有的 WorkflowRun：

```
t9k workflowrun delete foo -p demo --all
```

### describe

查看某个 WorkflowRun 的详细信息。

#### 使用

```
t9k wr describe <name>
```

`t9k wr describe` 也可以用 `t9k wr desc` 代替。

#### 选项

```
--color                 使用彩色的输出信息（默认全是黑色）。
```
#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project demo 下名为 foo 的 WorkflowRun 的详细描述：

```
t9k wr describe foo -p demo
```

### get

查看 WorkflowRun 相关信息。

#### 使用

```
t9k wr get [names...] [-A] [-o json|yaml|template]
```

#### 选项

```
-A, --all-namespaces    获取用户具有权限的所有 Namespace（Project）中的资源。
-o, --output string     字符串，指定输出信息的形式。可选值有 `json`，`yaml` 和默认的 `template`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

以默认格式查看 Project example 下所有 WorkflowRun：

```
t9k wr get -p example
```

以默认格式查看所有 Project 下的所有 WorkflowRun：

```
t9k wr get -A
```

以默认格式查看 Project example 下名为 foo 和 bar 的两个 WorkflowRun：

```
t9k wr get foo bar -p example
```

以 yaml 格式查看 Project example 下名为 foo 的 WorkflowRun：

```
t9k wr get foo -p example -o yaml
```

### logs

查看 WorkflowRun 某个容器的日志，不支持直接查看 DAG 类型的 WorkflowRun 的日志。

#### 使用

```
t9k wr logs [--container=<containerName>] [-f] [--tail] [--timestamps]
```

#### 选项

```
--container string      字符串，指定要查看的 container 名称，如果计算节点的 container 不止 1 个，必须指定此项。
-f, --follow            流式查看日志。
--tail int              整数，要查看的日志的行数（从后往前）。默认值：-1，查看全部日志。
--timestamps            是否展示时间戳。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project demo 下 WorkflowRun foo 唯一容器的日志：

```
t9k wr logs foo -p demo
```

流式查看 Project demo 下 WorkflowRun foo 容器 mnist 的日志：

```
t9k wr logs foo --container=mnist -p demo -f
```

查看 Project demo 下 WorkflowRun foo 唯一容器的最后 20 行日志：

```
t9k wr logs foo -p demo --tail=20
```

### wait

等待 WorkflowRun 完成，该命令不支持 DAG 类型的 WorkflowRun。

#### 使用

```
t9k wr wait <name> [--timeout=<timeoutTime>] [--period=<periodTime>] [--print-log [--container=<containerName>] [--timestamps]]
```

#### 选项

```
--timeout string        字符串，最长等待时间。默认值："1h"，1 小时。
--period  string        字符串，检查任务是否完成的周期。默认值："1s"，每秒检查一次。
--print-log             是否在等待时流式查看日志。

以下参数只有在开启了 `--print-log` 后才生效。

--container string      字符串，指定要查看的 container 名称，如果计算节点的 container 不止 1 个，必须指定此项。
--timestamps            是否展示时间戳。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

等待 Project example 下的 WorkflowRun foo 完成：

```
t9k wr wait foo -p example
```

等待 Project example 下的 WorkflowRun foo 完成，只等待 10 分钟：

```
t9k wr wait foo -p example --timeout 10m
```

等待 Project example 下的 WorkflowRun foo 完成，同时打印其容器 mnist 的日志：

```
t9k wr wait foo -p example --print-log --container mnist
```

## workflowtemplate

用于管理 [WorkflowTemplate](../../modules/workflows/workflowtemplate.md)。

<aside class="note info">
<div class="title">信息</div>

支持使用缩写 `wt` 代替 `workflowtemplate`。

</aside>

### delete

删除指定的 WorkflowTemplate。

#### 使用

```
t9k workflowtemplate delete [names...] [--all] [-f]
```

`t9k workflowtemplate delete` 也可以用 `t9k wr rm` 代替。

#### 选项

```
--all                   删除当前 Project 中所有的 WorkflowTemplate。
-f, --force             跳过确认，直接执行删除操作。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

删除 Project demo 下名为 foo 和 bar 的两个 WorkflowTemplate：

```
t9k workflowtemplate delete foo bar -p demo
```

跳过确认，直接删除 Project demo 下名为 foo 的 WorkflowTemplate：

```
t9k workflowtemplate delete foo -p demo -f
```

删除 Project demo 下所有的 WorkflowTemplate：

```
t9k workflowtemplate delete foo -p demo --all
```

### describe

查看某个 WorkflowTemplate 的详细信息。

#### 使用

```
t9k wt describe <name>
```

`t9k wt describe` 也可以用 `t9k wt desc` 代替。

#### 选项

```
--color                 使用彩色的输出信息（默认全是黑色）。
```
#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project demo 下名为 foo 的 WorkflowTemplate 的详细描述：

```
t9k wt describe foo -p demo
```

### get

查看 WorkflowTemplate 相关信息。

#### 使用

```
t9k wt get [names...] [-A] [-o json|yaml|template]
```

#### 选项

```
-A, --all-namespaces    获取用户具有权限的所有 Namespace（Project）中的资源。
-o, --output string     字符串，指定输出信息的形式。可选值有 `json`，`yaml` 和默认的 `template`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

以默认格式查看 Project example 下所有 WorkflowTemplate：

```
t9k wt get -p example
```

以默认格式查看所有 Project 下的所有 WorkflowTemplate：

```
t9k wt get -A
```

以默认格式查看 Project example 下名为 foo 和 bar 的两个 WorkflowTemplate：

```
t9k wt get foo bar -p example
```

以 yaml 格式查看 Project example 下名为 foo 的 WorkflowTemplate：

```
t9k wt get foo -p example -o yaml
```

### start

执行 WorkflowTemplate。

#### 使用

```
t9k wt start <name> [-l <labelStrings>] [-r <paramStrings>] [-s <serviceAccount>] [--timeout=<timeoutTime>] [-w <workplaceStrings>] [--use-param-defaults] [--dry-run] [-o yaml|json]
```

#### 选项

```
-l, --label strings          以键值对的方式指定 workflowRun 的 label。例如 -l "LABEL_1=VAL_1,LABEL_2=VAL_2"。
-r, --param strings          以键值对的方式指定 workflowRun 的参数。例如 -l "KEY_1=VAL_1,KEY_2=VAL_2"。
-w, --workspace strings      以键值对的方式指定 workspace 相关信息。例如 -w "name=$workspace_name,type=$workspace_type,$key$value"。
--use-param-defaults         是否采用默认参数
--timeout string             字符串，指定 workflowRun 的超时时间。
--dry-run                    只打印更新后的 yaml 文件，但是不执行 apply 操作。
-o, --output string          指定 --dry-run 打印的格式。可选值有 `json`，`yaml`。
-s, --serviceaccount string  指定 workflowRun 的 serviceAccount。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

执行 Project demo 下的 WorkflowTemplate foo：

```
t9k wt start foo -p demo
```

根据指定的 workspace 信息执行 Project demo 下的 WorkflowTemplate foo：

```
t9k wt start foo --workspace=name=bar,type=pvc,claimName=bar-pvc,subPath=/user/local/Document -p demo
```

执行 Project demo 下的 WorkflowTemplate foo，并设置参数 bar 值为 hello：

```
t9k wt start foo --param=bar=hello
```

## xgboosttrainingjob

用于管理 [XGBoostTrainingJob](../../modules/jobs/xgboosttrainingjob.md)。

<aside class="note info">
<div class="title">信息</div>

支持使用缩写 `xj` 代替 `xgboosttrainingjob`。

</aside>

### delete

删除指定的 XGBoostTrainingJob。

#### 使用

```
t9k xgboosttrainingjob delete [names...] [--all] [-f]
```

`t9k xgboosttrainingjob delete` 也可以用 `t9k xj rm` 代替。

#### 选项

```
--all                   删除当前 Project 中所有的 XGBoostTrainingJob。
-f, --force             跳过确认，直接执行删除操作。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

删除 Project demo 下名为 foo 和 bar 的两个 XGBoostTrainingJob：

```
t9k xgboosttrainingjob delete foo bar -p demo
```

跳过确认，直接删除 Project demo 下名为 foo 的 XGBoostTrainingJob：

```
t9k xgboosttrainingjob delete foo -p demo -f
```

删除 Project demo 下所有的 XGBoostTrainingJob：

```
t9k xgboosttrainingjob delete foo -p demo --all
```

### describe

查看某个 XGBoostTrainingJob 的详细信息。

#### 使用

```
t9k xj describe <name>
```

`t9k xj describe` 也可以用 `t9k xj desc` 代替。

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project demo 下名为 foo 的 XGBoostTrainingJob 的详细描述：

```
t9k xj describe foo -p demo
```

### get

查看 XGBoostTrainingJob 相关信息。

#### 使用

```
t9k xj get [names...] [-A] [-o json|yaml|template]
```

#### 选项

```
-A, --all-namespaces    获取用户具有权限的所有 Namespace（Project）中的资源。
-o, --output string     字符串，指定输出信息的形式。可选值有 `json`，`yaml` 和默认的 `template`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

以默认格式查看 Project example 下所有 XGBoostTrainingJob：

```
t9k xj get -p example
```

以默认格式查看所有 Project 下的所有 XGBoostTrainingJob：

```
t9k xj get -A
```

以默认格式查看 Project example 下名为 foo 和 bar 的两个 XGBoostTrainingJob：

```
t9k xj get foo bar -p example
```

以 yaml 格式查看 Project example 下名为 foo 的 XGBoostTrainingJob：

```
t9k xj get foo -p example -o yaml
```

### logs

查看 XGBoostTrainingJob 某个计算节点的日志。

#### 使用

```
t9k xj logs [--type=master|worker] [--index=<replicaIndex>] [--container=<containerName>] [-f] [--tail] [--timestamps]
```

#### 选项

```
--container string      字符串，指定要查看的 container 名称，如果计算节点的 container 不止 1 个，必须指定此项。
-f, --follow            流式查看日志。
--index string          字符串，要查看的计算节点的序号。默认值：0。
--tail int              整数，要查看的日志的行数（从后往前）。默认值：-1，查看全部日志。
--timestamps            是否展示时间戳。
--type string           字符串，要查看的计算节点的角色。可选值有 `master` 以及默认值 `worker`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

查看 Project example 下 XGBoostTrainingJob foo 第 `replicaIndex` 个 `replicaType` 节点的日志：

```
t9k xj logs foo --type=replicaType --index=replicaIndex -p example
```

流式查看 Project example 下 XGBoostTrainingJob foo 第 `replicaIndex` 个 `replicaType` 节点的容器 `mnist` 的日志：

```
t9k xj logs foo --type=replicaType --index=replicaIndex --container=mnist --follow
```

查看 XGBoostTrainingJob foo 第 0 个 worker 节点的最后 20 行日志：

```
t9k xj logs foo --tail 20
```

### wait

等待 XGBoostTrainingJob 完成。

#### 使用

```
t9k xj wait <name> [--timeout=<timeoutTime>] [--period=<periodTime>] [--print-log [--type=master|worker] [--index=<replicaIndex>] [--container=<containerName>] [--timestamps]]
```

#### 选项

```
--timeout string        字符串，最长等待时间。默认值："1h"，1 小时。
--period  string        字符串，检查任务是否完成的周期。默认值："1s"，每秒检查一次。
--print-log             是否在等待时流式查看日志。

以下参数只有在开启了 `--print-log` 后才生效。

--container string      字符串，指定要查看的 container 名称，如果计算节点的 container 不止 1 个，必须指定此项。
--index string          字符串，要查看的计算节点的序号。默认值：0。
--timestamps            是否展示时间戳。
--type string           字符串，要查看的计算节点的角色。可选值有 `master` 以及默认值 `worker`。
```

#### 全局选项

```
-c, --config            字符串，指定使用的 T9k Config 文件的路径。默认路径是 `$HOME/.t9k/t9k-config.yaml`。
-x, --context           字符串，指定使用 T9k Config 中的哪一个 Context，在未设置这个参数时，会使用 T9k Config 中 `current-context` 字段指定的 Context。
-h, --help              查看当前指令的帮助信息和示例。
-p, --project           字符串，指定使用的项目（本文档中的项目和命名空间同义）。
-n, --namespace         字符串，和 `-p, --project` 作用一致，指定使用的项目。这个设计是为了符合 kubectl 用户的习惯。
-v, --verbose           指定输出 log 信息的详细程度。
```

#### 示例

等待 Project example 下的 XGBoostTrainingJob foo 完成：

```
t9k xj wait foo -p example
```

等待 Project example 下的 XGBoostTrainingJob foo 完成，只等待 10 分钟：

```
t9k xj wait foo -p example --timeout 10m
```

等待 Project example 下的 XGBoostTrainingJob foo 完成，同时打印节点 master-0 的日志：

```
t9k xj wait foo -p example --print-log --type master --index 0
```
