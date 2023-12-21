# 使用 PyTorchTrainingJob 进行数据并行训练

本教程演示如何使用 PyTorchTrainingJob 对 PyTorch 模型进行多工作器同步训练（使用 <a target="_blank" rel="noopener noreferrer" href="https://pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html">`torch.nn.parallel.DistributedDataParallel`</a> 分布式数据并行模块）。

## 运行示例

请按照<a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/tutorial-examples/blob/master/docs/README-zh.md#%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95">使用方法</a>准备环境，然后前往<a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/tutorial-examples/tree/master/job/pytorchtrainingjob/ddp">本教程对应的示例</a>，参照其 README 文档运行。

!!! tip "提示"
    除了上述直接提供 YAML 配置文件的方法外，您也可以选择从网页控制台创建 PyTorchTrainingJob。

## 检查训练日志和指标

训练开始后，进入模型构建控制台的 Job 页面，可以看到名为 **torch-mnist-trainingjob** 的 PyTorchTrainingJob 正在运行：

<figure class="screenshot">
    <img alt="running" src="../assets/tasks/run-distributed-training/pytorch/ddp-training/running.png" class="screenshot"/>
</figure>

点击**该名称**进入详情页面，可以看到刚才创建的 PyTorchTrainingJob 的基本信息、状况信息和事件信息：

<figure class="screenshot">
    <img alt="details" src="../assets/tasks/run-distributed-training/pytorch/ddp-training/details.png" class="screenshot"/>
</figure>

点击 **TensorBoard** 右侧的 **Running** 打开 TensorBoard，可以查看可视化展示的训练和验证指标：

<figure class="screenshot">
    <img alt="tensorboard" src="../assets/tasks/run-distributed-training/pytorch/ddp-training/tensorboard.png" class="screenshot"/>
</figure>

点击上方标签页的**副本**，查看 PyTorchTrainingJob 的 Pod 信息：

<figure class="screenshot">
    <img alt="replicas" src="../assets/tasks/run-distributed-training/pytorch/ddp-training/replicas.png" class="screenshot"/>
</figure>

点击 Pod 列表右侧，**更多信息**下的 **:material-dots-vertical:&nbsp;> 日志**以查看训练脚本执行过程中的日志输出：

<figure class="screenshot">
    <img alt="view-log" src="../assets/tasks/run-distributed-training/pytorch/ddp-training/view-log.png" class="screenshot"/>
</figure>

点击上方标签页的**资源监测**，查看 PyTorchTrainingJob 运行过程中使用集群计算资源、网络资源和存储资源的情况：

<figure class="screenshot">
    <img alt="replicas" src="../assets/tasks/run-distributed-training/pytorch/ddp-training/metrics.png" class="screenshot"/>
</figure>

一段时间之后，PyTorchTrainingJob 的状态变为 **Succeeded**，表示训练成功完成。

<figure class="screenshot">
    <img alt="done" src="../assets/tasks/run-distributed-training/pytorch/ddp-training/done.png" class="screenshot"/>
</figure>

若 PyTorchTrainingJob 在运行过程中出错，其状态会变为 **Error**，并在事件信息和 Pod 信息部分显示错误信息，此时需要根据给出的错误信息进行问题排查。

!!! tip "提示"
    除了上述方法外，您也可以在 Notebook 中直接使用 `kubectl` 命令查看 PyTorchTrainingJob 以及其下各个 Pod 的状态、基本信息、事件、日志等以检查训练的进度和结果。
