# 使用 Python SDK 记录和上传训练数据

本教程介绍如何在模型的训练脚本中使用 [TensorStack SDK](../tools/python-sdk-t9k/index.md) 进行创建和结束试验、设定超参数、记录指标、上传数据到 AIMD 服务器等操作。

## 创建试验

### 基本方法

在模型的训练脚本中，您需要首先创建一个新的试验，通过调用 `t9k.aimd.create_trial()` 函数。其返回的 `Trial` 实例即代表了一次试验。此方法调用后，试验将被创建并具有状态“Initializing”。

最常见和基本的初始化方法需要提供 AIMD 服务器的 URL、试验名称、文件夹路径以及用户的 API Key 作为参数，试验将创建在该文件夹下。

```python
from t9k import aimd

trial = aimd.create_trial(                       # 返回Trial实例
    trial_name='cnn_keras',                      # 试验名称
    folder_path='image_classification/mnist')    # 文件夹路径
```

### 自动创建多级路径

如果在提供文件夹路径的同时设定关键字参数 `make_folder` 为 `True`，则会在上传数据时自动创建不存在的各级文件夹。

```python
trial = aimd.create_trial(
    trial_name='cnn_keras',
    folder_path='image_classification/mnist',
    make_folder=True)                            # 文件夹不存在时创建文件夹
```

### 提供文件夹 ID

您也可以直接提供文件夹 ID 以代替文件夹路径。获取文件夹 ID 的方法请参阅[其他文件夹操作](./use-experiment-console.md#其他文件夹操作)。

```python
trial = aimd.create_trial(
    trial_name='cnn_keras',
    folder_id='c06c9117-9057-40a0-8963-289569ed01af')      # 文件夹ID
```

如果您同时提供了文件夹的 ID 和路径，则路径不会被使用。如果您既没有提供文件夹的 ID，也没有提供文件夹的路径，则试验将创建在名为“default”的默认文件夹下。

<!-- 
### 提供描述

TODO
 -->

## 设定超参数

### 基本方法

为模型选用的超参数是分析模型训练效果的重要参照，记录模型的超参数十分必要，尤其是当您聚焦于某几个特定的超参数时。`Trial` 实例的 `params` 属性是一个容器对象，负责保存所有您想要记录的本次试验中模型的超参数，您可以像操作 Python 字典的键值对一样操作它当中的超参数项。推荐的设定超参数的方法是调用一次该容器对象的 `update()` 方法完成所有超参数的设定。

```python
trial.params.update({
    'batch_size': 32,
    'epochs': 10,
    'learning_rate': 0.001,
    'conv_channels': 32,
    'conv_kernel_size': 3,
    'maxpool_size': 2,
    'linear_features': 64,
})

params = trial.params      # 便于之后访问
```

当然，您也可以多次调用 `update()` 方法，或者使用类似 Python 字典键值对的赋值方法设定单个超参数。

```python
trial.params['batch_size'] = 32
```

<!-- 目前无法自动同步
<aside class="note">
<h1>注意</h1>

试验的超参数在每次更新后都会自动同步到服务器。

</aside>
 -->

设定完成之后，使用这些超参数配置模型，同样使用类似 Python 字典键值对的访问方法。

```python
from tensorflow.keras import layers, models, optimizers

model = models.Sequential()
model.add(layers.Conv2D(params['conv_channels'],     # 使用超参数配置模型
                        params['conv_kernel_size'],
                        input_shape=(28, 28, 1)))
...
optimizer = optimizers.Adam(learning_rate=params['learning_rate'])
model.compile(
    optimizer=optimizer,
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'])
...
model.fit(train_images,
          train_labels,
          batch_size=params['batch_size'],
          epochs=params['epochs'])
```

### 设定作为标记的超参数

在上面的示例中，所有的超参数都是数字类型并且可以直接传入各函数以配置模型。但除此之外，还有一些包含了模型重要信息的超参数，例如网络结构类型、优化器类型、损失函数类型、指标类型、激活函数类型等，它们由一些具体的计算过程或函数调用实现。您也可以设定这些超参数为标记其名称或类型的字符串，尽管这些字符串在大部分情况下不能直接参与配置模型，但它们能够在日后帮助您快速回顾这些重要信息。

```python
trial.params.update({
    'network_structure': 'cnn',
    'optimizer': 'Adam',
    'loss': 'sparse categorical crossentropy',
    'metric': 'accuracy',
    'linear_acti': 'relu',
})
```

<!-- 
## 使用配置文件

TODO
 -->

### 配合 argparse 模块使用

许多训练脚本的超参数都是从命令行传入，由 `argparse` 模块解析。这些超参数可以方便地转换为字典对象并传入 `update()` 方法。

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(...)
args = parser.parse_args()

trial.params.update(args.__dict__)
```

## 记录指标

### 手动记录

`Trial` 实例的 `log()` 方法用于记录模型在训练、验证或测试过程中产生的指标。被传入的字典对象会被作为指标记录，与此同时还需要提供指标的类型、当前的全局（训练）步数以及（可选的）当前的回合数。此方法第一次调用后，试验的状态将更新为“Running”。

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

            trial.log(
                metrics_type='train',          # 指标类型
                metrics={'loss': train_loss},  # 指标名称及相应值
                step=global_step,              # 当前全局步数
                epoch=epoch)                   # 当前回合数
```

<aside class="note">
<h1>注意</h1>

训练指标、验证指标和测试指标请分别使用指标类型 `'train'`（或 `'training'`）、`'val'`（或 `'validate'`、`'validation'`）和 `'test'`（或 `'testing'`、`'eval'`、`'evaluate'`、`'evaluation'`）。除此之外，您也可以使用其他任意字符串作为自定义指标类型。

指标的值可以是 Python 数字类型，或仅有一个元素的 NumPy 数组、TensorFlow 张量或 PyTorch 张量。

</aside>

### 自动记录

对于建立在 Keras API 上的模型，更简单的方法是在模型的训练和测试方法中分别添加回调 `t9k.aimd.keras.AIMDFitCallback` 和 `t9k.aimd.keras.AIMDEvalCallback` 的实例。回调会相应地调用 `log()` 方法以自动记录各指标并同步到服务器。

```python
# Keras模型
# 训练/验证过程和测试过程分别使用不同的回调
from t9k.aimd.keras import AIMDFitCallback, AIMDEvalCallback

model.fit(train_images,
          train_labels,
          epochs=10,
          validation_split=0.2,
          callbacks=AIMDFitCallback(trial))

model.evaluate(test_images,
               test_labels,
               callbacks=AIMDEvalCallback(trial))
```

<aside class="note tip">
<h1>提示</h1>

除了记录训练指标，`AIMDFitCallback` 回调还会获取模型的优化器配置、损失函数类型和指标类型并更新试验的超参数。

</aside>

<!-- 
```python
# PyTorch Lightning模型
from t9k.aimd.lightning import AIMDCallback

trainer = Trainer(max_epochs=10,
                  callbacks=AIMDCallback(trial))
``` -->

## 结束试验

模型的训练与测试全部完成后，您需要结束试验，通过调用 `Trial` 实例的 `finish()` 方法。此方法调用后，试验的状态将更新为“Succeeded”。

```python
trial.finish()
```

试验的全部数据保存在当前工作目录的 `.aimd/trials` 路径下，每个试验拥有一个独立的名为 `<trial_name>_<date>_<time>_<random_suffix>`（称为该试验的替代名称）的子目录。您可以启动一个本地的实验管理控制台，或将试验的数据上传到 AIMD 服务器，来方便地查看和分析数据。

## 上传数据

### 基本方法

上传数据之前，您需要先登录到 AIMD 服务器，通过调用 `t9k.aimd.login()` 函数。

```python
aimd.login(host='<your-server-host>', api_key='<your-api-key>')
```

<aside class="note info">
<h1>信息</h1>

生成包含 AIMD 权限的 API Key 的方法请参阅[生成 API Key](../api-key/generate-api-key.md)。

如要了解 API Key 的更多细节和使用方法，请参阅 [API Key](../modules/account-and-security.md#api-key) 和[使用 API Key](../api-key/use-api-key.md)。

</aside>

<aside class="note tip">
<h1>提示</h1>

AIMD 服务器位于平台主机域名的 `/t9k/experiment/server` 路径下。例如，如果平台首页的 URL 为 `https://www.tensorstack.net/t9k/landing-page/`，那么 AIMD 服务器的 URL 为 `https://www.tensorstack.net/t9k/experiment/server`。

</aside>

<aside class="note tip">
<h1>提示</h1>

如果您在 [TensorStack SDK 配置文件](../tools/python-sdk-t9k/guide.md#配置文件)中提供了 `host` 或 `api_key` 配置项的值，则它们将作为调用 `login()` 函数时相应参数的默认值。

</aside>

然后调用 `Trial` 实例的 `upload()` 方法。

```python
trial.upload()
```

此时前往实验管理控制台，可以看到相应的试验已经被展示。

### 上传本地保存的试验数据

您也可以在训练结束之后将本地保存的试验数据上传到 AIMD 服务器，以应对训练时无网络连接、最初未打算上传、误删服务器中的数据等情形。

这里使用到 TensorStack SDK 提供的[命令行工具](../tools/python-sdk-t9k/guide.md#命令行工具)。首先登录到 AIMD 服务器，通过执行 `aimd login` 命令。

```shell
aimd login -H <your-server-host> -k <your-api-key>
```

然后上传试验数据，通过在保存数据的工作目录下执行 `aimd trial upload` 命令。

```shell
aimd trial upload [-p <trial-path>] [-n <trial-name>] [-d <trial-dir>]
```

<aside class="note tip">
<h1>提示</h1>

使用 `--help` 参数来查看相应命令的详细使用方法，例如 `aimd trial upload --help`。

</aside>

## 下一步

* 进一步学习如何[在单个设备的训练中使用 AIMD](./single-device-training-use-aimd.md)
