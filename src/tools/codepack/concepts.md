# 概念

### Codepack

Codepack 是对用户想要在平台上运行的机器学习项目的抽象，其实质上是一个包含项目文件（模型代码、资源配置文件等）以及 Codepack 定义文件的文件系统的目录，该定义文件包含了 Codepack 的基本信息（版本、名称、描述等）和运行信息（target 和 action 的定义），见 [Codepack 定义](./codepack.md)。

### target

target 是对 Codepack 的一个具体任务的抽象，例如在平台上完成模型训练、部署模型为推理服务等。每个 target 可以指定其依赖的其他 target（例如创建推理服务需要先完成模型训练），命令行工具在运行一个 target 时，将递归地解析依赖，然后运行一个工作流。

### action

action 是对 target 的一个具体的可执行的操作的抽象，例如在平台中创建一个 PVC、创建一个进行分布式训练的 TrainingJob 等。action 定义了多个动词（verb），每个动词针对某一类的具体操作，由命令行工具和集群内组件提供实现。

<!-- TODO: Implement control logics
action 在执行时具有状态，用户可以设定策略，根据 action 的状态来决定接下来的行为（例如是否执行下一个 action、执行的时机等）。
-->
