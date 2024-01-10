# 使用 Python SDK 记录和上传数据

本教程介绍如何使用 [Python SDK](../tools/python-sdk-t9k/guide.md) 进行创建、加载、上传 Run 和 Artifact，设定超参数，记录指标等操作。

## 创建 Run

### 基本方法

在模型的训练脚本中，您需要首先创建一个 Run，通过调用 `t9k.em.create_run()` 函数。其返回的 `Run` 实例即代表了一次训练的运行。此方法调用后，Run 将被创建，具有状态“Running”，其本地文件默认保存在相对路径 `.em/runs` 下，每个 Run 拥有一个独立的名为 `<run_name>_<date>_<time>_<random_suffix>`（称为该 Run 的备用名称）的子目录。

最基本的初始化方法只需要提供名称作为参数。

```python
from t9k import em

run = em.create_run(name='mnist_torch')    # 返回Run实例
```

<aside class="note tip">
<div class="title">提示</div>

您可以通过设置环境变量 `EM_RUN_PARENT_DIR` 来修改 Run 的本地文件的保存路径。

</aside>

### 自动上传

如果想要自动异步上传 Run 的更新，可以设定 `auto_upload=True`，并提供文件夹路径，以及设定是否创建不存在的各级文件夹。在这种情况下，您在创建 Run 之前需要先[登录到 AIStore 服务器](#基本方法-2)。

```python
run = em.create_run(name='mnist_torch',
                    auto_upload=True,      # 启用自动上传
                    folder='new-folder',   # 文件夹路径
                    make_folder=True)      # 创建不存在的各级文件夹
```

如果目标文件夹已经存在同名的 Run，则需要指定 `conflict_strategy` 参数以处理冲突，参数接受以下值：

* `'skip'`：跳过上传。
* `'error'`：错误退出。
* `'new'`：以 Run 的备用名称上传。
* `'replace'`：替换同名的 Run。

例如，运行以下代码两次，第二次创建的 Run 会以类似 `mnist_torch_231231_235959_61p5jc` 的名称被上传到 `new-folder` 文件夹下。

```python
run = em.create_run(name='mnist_torch',
                    auto_upload=True,
                    folder='new-folder',
                    make_folder=True,
                    conflict_strategy='new')
```

### 提供标签和描述

您可以为创建的 Run 提供用于分类或介绍的标签或描述。

```python
run = em.create_run(
    name='mnist_torch',
    labels=['torch', 'CNN'],  # 标签
    description=              # 描述
    'Train a simple CNN model that classifies images of handwritten digits.')
```

### 提供配置文件

您可以将上面的所有配置（以及下面将要提到的超参数）都写进一个 YAML 文件里，然后传入该配置文件的路径即可。

```python
run = em.create_run(config_path='./run_config.yaml')  # 提供配置文件
```

其中 `run_config.yaml` 的内容如下：

```yaml
name: mnist_torch
auto_upload: true
folder: new-folder
make_folder: true
conflict_strategy: new
labels:
- torch
- CNN
description: Train a simple CNN model that classifies images of handwritten digits.
```

## 设定超参数

### 基本方法

超参数是影响模型训练效果的重要因素，记录训练的超参数十分必要，尤其是当您聚焦于某几个特定的超参数时。`Run` 实例的 `hparams` 属性是一个容器对象，用于保存您想要记录的所有超参数，您可以像操作 Python 字典一样操作它。一种推荐的设定超参数的方法是调用一次该容器对象的 `update()` 方法完成所有超参数的设定。

```python
run.hparams.update({
    'batch_size': 32,
    'epochs': 10,
    'learning_rate': 0.001,
    'conv_channels': 32,
    'conv_kernel_size': 3,
    'maxpool_size': 2,
    'linear_features': 64,
})

hparams = run.hparams      # 便于之后访问
```

另一种推荐的方法是在创建 Run 的时候就传入所有超参数，此时可以将超参数也写进配置文件。

```python
run = em.create_run(
    name='mnist_torch',
    hparams={
    'batch_size': 32,
    'epochs': 10,
    'learning_rate': 0.001,
    'conv_channels': 32,
    'conv_kernel_size': 3,
    'maxpool_size': 2,
    'linear_features': 64,
})

# 或

run = em.create_run(config_path='./run_config.yaml')
```

其中 `run_config.yaml` 的内容如下：

```yaml
name: mnist_torch
hparams:
  batch_size: 32
  epochs: 10
  learning_rate: 0.001
  conv_channels: 32
  conv_kernel_size: 3
  maxpool_size: 2
  linear_features: 64
```

当然，您也可以多次调用 `update()` 方法，或者使用类似 Python 字典的键值对赋值方法设定单个超参数。

```python
run.hparams['batch_size'] = 32
```

设定完成之后，使用这些超参数配置模型，同样使用类似 Python 字典的键值对访问方法。

```python
from tensorflow.keras import layers, models, optimizers

model = models.Sequential()
model.add(layers.Conv2D(hparams['conv_channels'],     # 使用超参数配置模型
                        hparams['conv_kernel_size'],
                        input_shape=(28, 28, 1)))
...
optimizer = optimizers.Adam(learning_rate=hparams['learning_rate'])
model.compile(
    optimizer=optimizer,
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'])
...
model.fit(train_images,
          train_labels,
          batch_size=hparams['batch_size'],
          epochs=hparams['epochs'])
```

### 设定作为标记的超参数

在上面的示例中，所有超参数都是直接传入各函数以配置模型。您也可以设定一些作为标记的超参数，例如网络类型、优化器类型、损失函数类型、激活函数类型等，以便日后快速回顾重要信息。

```python
run.hparams.update({
    'network_structure': 'CNN',
    'optimizer': 'Adam',
    'loss': 'sparse categorical crossentropy',
    'linear_acti': 'relu',
})
```

### 配合 argparse 模块使用

许多训练脚本的超参数都是从命令行传入，由 `argparse` 模块解析。这些超参数可以方便地转换为字典对象并传入 `update()` 方法。

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(...)
args = parser.parse_args()

run.hparams.update(args.__dict__)
```

## 记录指标

### 手动记录

`Run` 实例的 `log()` 方法用于记录模型在训练、验证或测试过程中产生的指标。被传入的字典对象会被作为指标记录，与此同时还需要提供指标的类型、当前的全局训练步数以及（可选的）当前的回合数。

```python
# PyTorch模型
for epoch in range(1, epochs + 1):
    model.train()
    for step, (data, target) in enumerate(train_loader, 1):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        if step % 500 == 0:
            train_loss = loss.item()
            logging.info(
                'epoch {:d}/{:d}, batch {:5d}/{:d} with loss: {:.4f}'.
                format(epoch, epochs, step, steps_per_epoch, train_loss))
            global_step = (epoch - 1) * steps_per_epoch + step

            run.log(
                type='train',                    # 指标类型
                metrics={'loss': train_loss},    # 指标名称及相应值
                step=global_step,                # 当前全局步数
                epoch=epoch)                     # 当前回合数
```

<aside class="note">
<div class="title">注意</div>

训练指标、验证指标和测试指标请分别使用指标类型 `'train'`（或 `'training'`）、`'val'`（或 `'validate'`、`'validation'`）和 `'test'`（或 `'testing'`、`'eval'`、`'evaluate'`、`'evaluation'`）。除此之外，您也可以使用其他任意字符串作为自定义指标类型。

指标的值可以是 Python 数字类型，或仅有一个元素的 NumPy 数组、TensorFlow 张量或 PyTorch 张量。

</aside>

### 自动记录

对于建立在 Keras API 上的模型，更简单的方法是在模型的训练和测试方法中分别添加回调 `t9k.em.keras.EMFitCallback` 和 `t9k.em.keras.EMEvalCallback` 的实例。回调会相应地调用 `log()` 方法以自动记录各指标并同步到服务器。

```python
# Keras模型
# 训练/验证过程和测试过程分别使用不同的回调
from t9k.em.keras import EMFitCallback, EMEvalCallback

model.fit(train_images,
          train_labels,
          epochs=10,
          validation_split=0.2,
          callbacks=EMFitCallback(run))

model.evaluate(test_images,
               test_labels,
               callbacks=EMEvalCallback(run))
```

<aside class="note tip">
<div class="title">提示</div>

除了记录训练指标，`EMFitCallback` 回调还会获取模型的优化器配置、损失函数类型和指标类型并更新 Run 的超参数。

</aside>

<!-- 
```python
# PyTorch Lightning模型
from t9k.em.lightning import emCallback

trainer = Trainer(max_epochs=10,
                  callbacks=emCallback(trial))
``` -->

## 结束 Run

模型的训练与测试全部完成后，您需要结束 Run，通过调用 `Run` 实例的 `finish()` 方法。此方法调用后，Run 的状态将更新为“Complete”。

```python
run.finish()
```

## 创建 Artifact

### 基本方法

如要记录和保存与训练过程有关的文件，您需要创建一个 Artifact，通过调用 `t9k.em.create_artifact()` 函数。此方法调用后，Artifact 将被创建，其本地文件默认保存在相对路径 `.em/artifacts` 下。与 Run 相同，每个 Artifact 拥有一个独立的名为 <artifact_name>_<date>_<time>_<random_suffix>（称为该 Artifact 的备用名称）的子目录。

最基本的初始化方法只需要提供名称作为参数。

```python
dateset_artifact = em.create_artifact(name='mnist_dataset')
```

### 提供标签和描述

您可以为创建的 Artifact 提供用于分类或介绍的标签或描述。

```python
dateset_artifact = em.create_artifact(
    name='mnist_dataset',
    labels=['dataset', 'MNIST'],                           # 标签
    description='Image dataset of handwritten digits.')    # 描述
```

## 为 Artifact 添加文件

与训练过程有关的文件通过 `Artifact` 实例的 `add_file()` 和 `add_dir()` 方法添加到 Artifact 中。

```python
dateset_artifact.add_file(file_path='./mnist.npz')    # 添加单个文件
dateset_artifact.add_dir(dir_path='./mnist/')         # 添加目录
```

Artifact 中的文件对象具有层次结构，您可以指定文件或目录位于 Artifact 的何路径下。

```python
dateset_artifact.add_file(file_path='./mnist.npz', obj_path='dataset/')
dateset_artifact.add_dir(dir_path='./mnist/', obj_path='dataset/')
```

还可以通过 `add_reference()` 方法为 Artifact 添加一个网络文件的引用。

```python
dateset_artifact.add_reference(uri='https://storage.googleapis.com/cvdf-datasets/mnist/train-images-idx3-ubyte.gz', obj_path='dataset/')
```

## 标记 Artifact 为 Run 的输入输出

为了构成 Run 与 Artifact 之间的数据流，需要调用 `Run` 实例的 `mark_input()` 和 `mark_output()` 方法以标记 `Artifact` 实例为其输入或输出。

```python
run.mark_input(dateset_artifact)
run.mark_output(model_artifact)
```

<aside class="note tip">
<div class="title">提示</div>

Model、Dataset、Branch、Tag 和 Commit 实例也可以被标记为 Run 的输入或输出。

</aside>

## 上传数据

### 基本方法

上传数据之前，您需要先登录到 [AIStore](../modules/asset-management.md#产品架构) 服务器，通过调用 `t9k.em.login()` 函数。

```python
em.login(ais_host='<your-server-host>', api_key='<your-api-key>')
```

<aside class="note info">
<div class="title">信息</div>

生成包含 EM 权限的 API Key 的方法请参阅[生成 API Key](./generate-api-key.md)。

如要了解 API Key 的更多细节和使用方法，请参阅 [API Key](../modules/security/account.md#api-key) 和[使用 API Key](./use-api-key.md)。

</aside>

<aside class="note tip">
<div class="title">提示</div>

AIStore 服务器位于平台主机域名的 `/t9k/aistore/server` 路径下。例如，如果平台首页的 URL 为 `https://www.tensorstack.net/t9k/landing-page/`，那么 AIStore 服务器的 URL 为 `https://www.tensorstack.net/t9k/aistore/server`。

</aside>

<aside class="note tip">
<div class="title">提示</div>

如果您在 [Python SDK 配置文件](../tools/python-sdk-t9k/guide.md#配置文件)中提供了 `contexts[*].prefixes.aistore` 或 `contexts[*].auth.api_key` 字段的值，则它们将作为调用 `login()` 函数时相应参数的默认值。

</aside>

然后调用 `Run` 或 `Artifact` 实例的 `upload()` 方法。

```python
run.upload()
artifact.upload()
```

<aside class="note">
<div class="title">注意</div>

当一个 Run 被上传时，被标记为其输入输出的 Artifact 也会同时被上传。

</aside>

### 上传本地保存的数据

您也可以在训练结束之后将本地保存的数据上传到 AIStore 服务器，以应对训练时无网络连接、最初未打算上传、误删服务器中的数据等情形。

首先[登录到 AIStore 服务器](#基本方法-2)，然后加载保存在本地的 Run 或 Artifact，调用其 `upload()` 方法。

```python
run = em.load_run(path='.em/runs/mnist_torch_231222_141932_61p5jc')
run.upload(folder='default', make_folder=True)

artifact = em.load_artifact(path='.em/runs/mnist_torch_saved_model_230908_165433_tou3ai')
artifact.upload(folder='default', make_folder=True)
```

## 下一步

* 进一步学习如何[在单设备训练场景下追踪模型训练](./record-single-device-training.md)
