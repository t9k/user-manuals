# Codepack

Codepack 以简洁明了的形式定义在平台上开发、运行、部署一个机器学习项目所需要的全部信息，例如代码、配置文件、各种参数等。其相关工具能够根据这些信息自动地执行相应的操作，从而大幅减少用户的操作量，显著改善实验的可重复性。

例如对于 MNIST 手写数字图像分类任务，在已经准备好了训练代码、数据集和资源配置文件的情况下，您只需要再创建一个 Codepack 定义文件，然后使用 Codepack CLI 执行一条命令，就可以在平台上启动分布式训练：

<html>
<head>
  <link rel="stylesheet" type="text/css" href="../../assets/tools/codepack/asciinema-player.css" />
</head>
<body>
  <div id="player" style="width: 80%;"></div>
  <script src="../../assets/tools/codepack/asciinema-player.min.js"></script>
  <script>
    AsciinemaPlayer.create(
      '../../assets/tools/codepack/506308.cast',
      document.getElementById('player'),
      { cols: 80, rows: 27, autoPlay: true }
    );
  </script>
</body>
</html>

这里 Codepack 定义文件的内容如下：

```yaml
apiVersion: codepack.tensorstack.dev/v1beta1
name: mnist-keras
description: A simple image classifier based on CNN using tf2.
project: demo
default: prepare-env
targets:
  - name: prepare-env        # Prepare running env
    actions:
      - name: workspace-for-training
        verb: apply
        files: [pvc.yaml]
  - name: copy-file          # Copy training code and dataset to PVC
    deps: ["prepare-env"]
    actions:
      - name: copy-code
        verb: copy
        src: .
        dst: codepack-example:.
  - name: run-distributed-training    # Run a distributed training
    deps: ["prepare-env", "copy-file"]
    actions:
      - name: trainingjob
        verb: create
        files: [trainingjob.yaml]

```

整个 Codepack 的文件结构如下：

```shell
mnist-keras
├── codepack.yaml
├── main.py
├── mnist.npz
├── pvc.yaml
└── trainingjob.yaml
```

由于 Codepack 的全部信息都维护在一个定义文件中，用户创建一个新的 Codepack 或者将既有的机器学习项目修改为 Codepack 都非常容易，并且用户可以使用 Git 来轻松地对 Codepack 进行版本控制和分发。

Codepack 的相关工具包括[命令行工具](./cli.md)和集群内组件，前者负责读取 Codepack 定义并执行用户指定的 action，后者负责进行安全访问控制以及为命令行工具执行 action 提供支持。

## 下一步

* 了解 [Codepack 的概念](./concept.md)
* 了解 [Codepack 的定义](./codepack.md)
* 了解[命令行工具](./cli.md)
* 学习具体的[使用示例](./example.md)
