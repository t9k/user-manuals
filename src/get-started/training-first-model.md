# 训练你的第一个模型

本教程将带领用户使用 [Notebook](../modules/building/notebook.md) 和 [PyTorchTrainingJob](../modules/jobs/pytorchtrainingjob.md) 资源，来构建和训练用户的第一个机器学习模型。

<aside class="note info">
<div class="title"> Resources（资源）</div>

在 Kubernetes 中，Resources（资源）是用于描述集群中工作负载的概念。资源可分为 Kubernetes 原生资源，例如 `Pod`，`Service` 等；及 Custom Resource Defintion（CRD，定制资源），其扩展 Kubernetes，提供特定领域（例如 AI）的额外能力。 `Notebook` 和 `PyTorchTrainingJob` 是 TensorStack 提供的 CRD。

详细信息请参阅 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/"> Custom Resources （定制资源）</a>。

</aside>

## 创建 Notebook

在 TensorStack AI 平台首页，点击**模型构建**进入模型构建控制台。

<figure class="screenshot">
  <img alt="landing-page" src="../assets/get-started/training-first-model/landing-page.png" class="screenshot"/>
</figure>

模型构建控制台的总览页面展示了多种资源，用户可以点击右上角的按钮切换 Project，也可以点击**事件**和**配额**标签页以查看当前 Project 最近发生的事件以及计算资源（CPU、Memory、GPU 等）配额。

<figure class="screenshot">
  <img alt="project" src="../assets/get-started/training-first-model/overview.png" class="screenshot"/>
</figure>

### 创建 PVC

在创建 Notebook 之前，首先需要创建一个用于存储文件的 PVC（持久卷）。在左侧的导航菜单中点击**存储&nbsp;> 持久卷**进入 PVC 管理页面，然后点击右上角的**创建 PVC**。

<aside class="note info">
<div class="title">PVC</div>

<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/zh/docs/concepts/storage/persistent-volumes/">PVC（PersistentVolumeClaim，持久卷申领）</a>是一种 Kubernetes 原生资源，表示用户对存储的请求。参阅[管理 PVC](../tasks/manage-pvc.md) 以进一步了解如何在平台上使用 PVC。

</aside>

<figure class="screenshot">
  <img alt="project" src="../assets/get-started/training-first-model/create-pvc.png" class="screenshot"/>
</figure>

在 PVC 创建页面，如下填写各个参数：

* **Name** 填写 `mnist`。
* **Size** 填写 `1Gi`。

其他参数保持默认即可。完成之后，点击**创建**。

<figure class="screenshot">
  <img alt="project" src="../assets/get-started/training-first-model/create-pvc-detail.png" class="screenshot"/>
</figure>

在跳转回到 PVC 管理页面之后，可点击右上角的**刷新图标**来手动刷新 PVC 状态。下图展示 PVC `mnist` 已经创建完成。

<figure class="screenshot">
  <img alt="project" src="../assets/get-started/training-first-model/create-pvc-finish.png" class="screenshot"/>
</figure>

### 创建 Notebook

在左侧的导航菜单中点击**构建 > Notebook** 进入 Notebook 管理页面，然后点击右上角的**创建 Notebook**。

<aside class="note info">
<div class="title">Notebook</div>

[Notebook](../modules/building/notebook.md) 是一种 TensorStack CRD，用于在集群中运行在线交互式开发环境的服务（例如 JupyterLab、RStudio），同时提供 GPU 使用、SSH 访问等补充功能。

</aside>

<figure class="screenshot">
  <img alt="create-notebook" src="../assets/get-started/training-first-model/create-notebook.png" class="screenshot"/>
</figure>

在 Notebook 创建页面，如下填写各个参数：

* **名称**填写 `mnist`。
* **镜像类型**选择 `Jupyter`，**镜像**选择 `t9kpublic/tensorflow-2.14.0-notebook-cpu:1.77.1`。
* **存储卷**选择 `mnist`。
* **调度器**选择**默认调度器**，**模板**选择 **small**。

完成之后，点击**创建**。

<figure class="screenshot">
  <img alt="create-notebook-detail" src="../assets/get-started/training-first-model/create-notebook-detail.png" class="screenshot"/>
</figure>

<aside class="note info">
<div class="title">调度器</div>

调度器负责将工作负载调度到合适的节点上以运行。平台支持 Kubernetes 的默认调度器 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/#kube-scheduler">kube-scheduler</a>，同时提供了更加强大的 T9k 调度器。详情请参阅[调度](../modules/scheduling/index.md)。

</aside>

在跳转回到 Notebook 管理页面之后，等待刚才创建的 Notebook 准备就绪。第一次拉取镜像可能会花费较长的时间，具体取决于用户集群的网络状况。点击右上角的**刷新图标**来手动刷新 Notebook 状态，待 Notebook 开始运行之后，点击右侧的**打开**进入其前端页面。

<figure class="screenshot">
  <img alt="connect-notebook" src="../assets/get-started/training-first-model/connect-notebook.png" class="screenshot"/>
</figure>

现在 Notebook 已经可以使用了，用户可以在这里进行模型的开发与测试。

<figure class="screenshot">
  <img alt="jupyter" src="../assets/get-started/training-first-model/jupyter.png" class="screenshot"/>
</figure>

## 使用 Notebook 训练模型

<aside class="note tip">
<div class="title">提示</div>

如果用户之前从未使用过 JupyterLab，建议在使用之前先阅读<a target="_blank" rel="noopener noreferrer" href="https://jupyterlab.readthedocs.io/en/stable/">官方文档</a>以熟悉 JupyterLab 的功能特性以及基本操作。

</aside>

在 Notebook 的前端页面，点击左上角的 **+**，然后点击 Notebook 下的 **Python3** 以新建一个 `.ipynb` 文件。

<figure class="screenshot">
  <img alt="jupyter-create-notebook" src="../assets/get-started/training-first-model/jupyter-create-notebook.png" class="screenshot"/>
</figure>

复制下面的训练脚本到该 `.ipynb` 文件的代码框中。该脚本基于 TensorFlow 框架和 Keras API，建立一个简单的卷积神经网络模型，并使用 MNIST 数据集的手写数字图像进行训练和测试。

```python title="keras_mnist.py"
from tensorflow.keras import callbacks, datasets, layers, models, optimizers

model = models.Sequential([
    layers.Conv2D(32, 3, activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPool2D((2, 2)),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPool2D((2, 2)),
    layers.Conv2D(64, 3, activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax'),
])
model.compile(optimizer=optimizers.Adam(learning_rate=0.001),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


(train_images, train_labels), (test_images,
                               test_labels) = datasets.mnist.load_data()

train_images = train_images.reshape((60000, 28, 28, 1))
test_images = test_images.reshape((10000, 28, 28, 1))

train_images, test_images = train_images / 255.0, test_images / 255.0

model.fit(train_images,
          train_labels,
          batch_size=32,
          epochs=10,
          validation_split=0.2,
          callbacks=callbacks.TensorBoard(log_dir='./log'))
model.evaluate(test_images, test_labels)

```

点击上方的运行按钮，可以看到训练开始进行，如下图：

<figure class="screenshot">
  <img alt="jupyter-training" src="../assets/get-started/training-first-model/jupyter-training.png" class="screenshot"/>
</figure>


## 下一步

* 对上述模型[进行分布式训练](./training-using-job.md)
* 了解[模型构建](../modules/building/index.md)
