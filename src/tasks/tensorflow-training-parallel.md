# 使用 TensorFlowTrainingJob 进行数据并行训练

本教程演示如何使用 TensorFlowTrainingJob 对 Keras 模型进行数据并行训练（采用 <a target="_blank" rel="noopener noreferrer" href="https://www.tensorflow.org/api_docs/python/tf/distribute/MultiWorkerMirroredStrategy">`tf.distribute.MultiWorkerMirroredStrategy`</a> 分布式策略）。

## 运行示例

请按照<a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/tutorial-examples/blob/master/docs/README-zh.md#%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95">使用方法</a>准备环境，然后前往<a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/tutorial-examples/tree/master/job/tensorflowtrainingjob/multiworker">本教程对应的示例</a>，参照其 README 文档运行。

<aside class="note tip">
<div class="title">提示</div>

上述操作使用 YAML 配置文件创建 TensorFlowTrainingJob，您也可以在模型构建控制台进行创建。

</aside>

## 检查训练日志和指标

训练开始后，进入模型构建控制台的 Job 页面，可以看到名为 **keras-mnist-trainingjob** 的 TensorFlowTrainingJob 正在运行：

<figure class="screenshot">
    <img alt="running" src="../assets/tasks/run-distributed-training/tensorflow/multiworker-training/running.png" />
</figure>

点击**该名称**进入详情页面，可以看到刚才创建的 TensorFlowTrainingJob 的基本信息、状况信息和事件信息：

<figure class="screenshot">
    <img alt="details" src="../assets/tasks/run-distributed-training/tensorflow/multiworker-training/details.png" />
</figure>

点击 **TensorBoard** 右侧的 **Running** 打开 TensorBoard，可以查看可视化展示的训练和验证指标：

<figure class="screenshot">
    <img alt="tensorboard" src="../assets/tasks/run-distributed-training/tensorflow/multiworker-training/tensorboard.png" />
</figure>

点击上方标签页的**副本**，查看 TensorFlowTrainingJob 的 Pod 信息：

<figure class="screenshot">
    <img alt="replicas" src="../assets/tasks/run-distributed-training/tensorflow/multiworker-training/replicas.png" />
</figure>

点击副本右侧的**更多按钮&nbsp;> 日志**以查看训练脚本执行过程中的日志输出：

<figure class="screenshot">
    <img alt="view-log" src="../assets/tasks/run-distributed-training/tensorflow/multiworker-training/view-log.png" />
</figure>

点击上方标签页的**资源监测**，查看 TensorFlowTrainingJob 运行过程中使用集群计算资源、网络资源和存储资源的情况：

<figure class="screenshot">
    <img alt="replicas" src="../assets/tasks/run-distributed-training/tensorflow/multiworker-training/metrics.png" />
</figure>

一段时间之后，TensorFlowTrainingJob 的状态变为 **Succeeded**，表示训练成功完成。

<figure class="screenshot">
    <img alt="done" src="../assets/tasks/run-distributed-training/tensorflow/multiworker-training/done.png" />
</figure>

若 TensorFlowTrainingJob 在运行过程中出错，其状态会变为 **Error**，并在事件信息和 Pod 信息部分显示错误信息，此时需要根据给出的错误信息进行问题排查。

<aside class="note tip">
<div class="title">提示</div>

除了上述方法外，您也可以在 Notebook 中直接使用 `kubectl` 命令查看 TensorFlowTrainingJob 以及其下各个 Pod 的状态、基本信息、事件、日志等以检查训练的进度和结果。

</aside>
