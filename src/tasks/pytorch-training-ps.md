# 使用 PyTorchTrainingJob 进行参数服务器训练

本教程演示如何使用 PyTorchTrainingJob 对 PyTorch 模型进行基于 RPC 的参数服务器训练（使用<a target="_blank" rel="noopener noreferrer" href="https://pytorch.org/docs/stable/rpc.html">分布式 RPC 框架 `torch.distributed.rpc`</a>）。示例修改自 PyTorch 官方教程 <a target="_blank" rel="noopener noreferrer" href="https://pytorch.org/tutorials/intermediate/rpc_param_server_tutorial.html">Implementing a Parameter Server Using Distributed RPC Framework</a>，关于训练脚本的更多细节信息请参考此教程。

## 运行示例

请按照<a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/tutorial-examples/blob/master/docs/README-zh.md#%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95">使用方法</a>准备环境，然后前往<a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/tutorial-examples/tree/master/job/pytorchtrainingjob/ps">本教程对应的示例</a>，参照其 README 文档运行。

<aside class="note tip">
<h1>提示</h1>

上述操作使用 YAML 配置文件创建 PyTorchTrainingJob，您也可以在模型构建控制台进行创建。

</aside>

## 检查训练日志和指标

训练开始后，进入模型构建控制台的 Job 页面，可以看到名为 **torch-mnist-trainingjob-ps** 的 PyTorchTrainingJob 正在运行：

<figure class="screenshot">
    <img alt="running" src="../assets/tasks/run-distributed-training/pytorch/rpc-implemented-parameter-server-training/running.png" class="screenshot"/>
</figure>

点击**该名称**进入详情页面，可以看到刚才创建的 PyTorchTrainingJob 的基本信息、状况信息和事件信息：

<figure class="screenshot">
    <img alt="details" src="../assets/tasks/run-distributed-training/pytorch/rpc-implemented-parameter-server-training/details.png" class="screenshot"/>
</figure>

点击 **TensorBoard** 右侧的 **Running** 打开 TensorBoard，可以查看可视化展示的训练和验证指标：

<figure class="screenshot">
    <img alt="tensorboard" src="../assets/tasks/run-distributed-training/pytorch/rpc-implemented-parameter-server-training/tensorboard.png" class="screenshot"/>
</figure>

点击上方标签页的**副本**，查看 PyTorchTrainingJob 的 Pod 信息：

<figure class="screenshot">
    <img alt="replicas" src="../assets/tasks/run-distributed-training/pytorch/rpc-implemented-parameter-server-training/replicas.png" class="screenshot"/>
</figure>

点击 Pod 列表右侧，**更多信息**下的 **:material-dots-vertical:&nbsp;> 日志**以查看训练脚本执行过程中的日志输出：

<figure class="screenshot">
    <img alt="view-log" src="../assets/tasks/run-distributed-training/pytorch/rpc-implemented-parameter-server-training/view-log.png" class="screenshot"/>
</figure>

点击上方标签页的**资源监测**，查看 PyTorchTrainingJob 运行过程中使用集群计算资源、网络资源和存储资源的情况：

<figure class="screenshot">
    <img alt="replicas" src="../assets/tasks/run-distributed-training/pytorch/rpc-implemented-parameter-server-training/metrics.png" class="screenshot"/>
</figure>

一段时间之后，PyTorchTrainingJob 的状态变为 **Succeeded**，表示训练成功完成。

<figure class="screenshot">
    <img alt="done" src="../assets/tasks/run-distributed-training/pytorch/rpc-implemented-parameter-server-training/done.png" class="screenshot"/>
</figure>

若 PyTorchTrainingJob 在运行过程中出错，其状态会变为 **Error**，并在事件信息和 Pod 信息部分显示错误信息，此时需要根据给出的错误信息进行问题排查。

<aside class="note tip">
<h1>提示</h1>

除了上述方法外，您也可以在 Notebook 中直接使用 `kubectl` 命令查看 PyTorchTrainingJob 以及其下各个 Pod 的状态、基本信息、事件、日志等以检查训练的进度和结果。

</aside>
