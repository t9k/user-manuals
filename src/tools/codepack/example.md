# 示例

下面是一个简单但完整的创建和运行 Codepack 的示例。

## 创建 Codepack

这里以进行 MNIST 手写数字图像分类的 Keras 模型为例，在工作路径下创建一个名为 `mnist-keras` 的目录。

### 准备代码、数据集和资源配置文件

首先编写一个进行模型构建、训练和测试的 Python 脚本，使用 Keras 框架和简单的卷积神经网络结构。为了在平台上进行分布式训练，训练过程采用 `tf.distribute.MultiWorkerMirroredStrategy` 分布式策略。具体代码如下：

```python
import argparse
import json
import logging
import os
import shutil

import tensorflow as tf
from tensorflow.keras import callbacks, datasets, layers, models, optimizers

parser = argparse.ArgumentParser(
    description='Distributed training of Keras model for MNIST with '
    'MultiWorkerMirroredStrategy.')
parser.add_argument('--aimd',
                    action='store_true',
                    default=False,
                    help='Use AIMD to record training data.')
parser.add_argument('--api_key',
                    type=str,
                    help='API Key for requesting AIMD server. '
                    'Required if --aimd is set.')
parser.add_argument(
    '--folder_path',
    type=str,
    default='aimd-example',
    help='Path of AIMD folder in which trial is to be created. '
    'Required if --aimd is set.')
parser.add_argument('--log_dir',
                    type=str,
                    help='Path of the TensorBoard log directory.')
parser.add_argument('--no_cuda',
                    action='store_true',
                    default=False,
                    help='Disable CUDA training.')
parser.add_argument(
    '--server_url',
    type=str,
    default='https://proxy.nc201.kube.tensorstack.net/t9k/aimd/server',
    help='URL of AIMD server. Required if --aimd is set.')
parser.add_argument('--save_path',
                    type=str,
                    default=None,
                    help='Save path of the trained model.')
parser.add_argument('--trial_name',
                    type=str,
                    default='mnist_keras_distributed',
                    help='Name of AIMD trial to create. '
                    'Required if --aimd is set.')
args = parser.parse_args()
logger = logging.getLogger('print')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
logger.propagate = False

if args.no_cuda:
    # Sets all GPUs invisible
    tf.config.set_visible_devices([], 'GPU')
gpus = tf.config.get_visible_devices('GPU')
if gpus:
    # Print GPU info
    logger.info('NVIDIA_VISIBLE_DEVICES: {}'.format(
        os.getenv('NVIDIA_VISIBLE_DEVICES')))
    logger.info('T9K_GPU_PERCENT: {}'.format(os.getenv('T9K_GPU_PERCENT')))
    logger.info('Visible GPUs: {}'.format(
        tf.config.get_visible_devices('GPU')))
    # Set memory growth
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
    # # Set GPU memory limit
    # tf.config.set_logical_device_configuration(
    #     gpus[0], [tf.config.LogicalDeviceConfiguration(memory_limit=1024)])

    strategy = tf.distribute.MultiWorkerMirroredStrategy()

# Get information for current worker.
tf_config = json.loads(os.environ['TF_CONFIG'])
world_size = len(tf_config['cluster']['worker'])
task_index = tf_config['task']['index']

if args.aimd and task_index == 0:
    from t9k import aimd
    trial = aimd.init(server_url=args.server_url,
                    trial_name=args.trial_name,
                    folder_path=args.folder_path,
                    api_key=args.api_key)

params = {
    'batch_size': 32 * world_size,
    'epochs': 10,
    'learning_rate': 0.001 * world_size,
    'conv_channels1': 32,
    'conv_channels2': 64,
    'conv_channels3': 64,
    'conv_kernel_size': 3,
    'maxpool_size': 2,
    'linear_features1': 64,
    'seed': 1,
}

if args.aimd and task_index == 0:
    trial.params.update(params)
    trial.params.parse(dist_tf_strategy=strategy)

with strategy.scope():
    model = models.Sequential([
        layers.Conv2D(params['conv_channels1'],
                    params['conv_kernel_size'],
                    activation='relu',
                    input_shape=(28, 28, 1)),
        layers.MaxPooling2D((params['maxpool_size'], params['maxpool_size'])),
        layers.Conv2D(params['conv_channels2'],
                    params['conv_kernel_size'],
                    activation='relu'),
        layers.MaxPooling2D((params['maxpool_size'], params['maxpool_size'])),
        layers.Conv2D(params['conv_channels3'],
                    params['conv_kernel_size'],
                    activation='relu'),
        layers.Flatten(),
        layers.Dense(params['linear_features1'], activation='relu'),
        layers.Dense(10, activation='softmax'),
    ])
    model.compile(
        optimizer=optimizers.Adam(learning_rate=params['learning_rate']),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])

print(os.path.join(os.getcwd(), 'mnist.npz'))
(train_images, train_labels), (test_images,
                            test_labels) = datasets.mnist.load_data(
                                path=os.path.join(os.getcwd(), 'mnist.npz'))
train_images = train_images.reshape((60000, 28, 28, 1)).astype("float32") / 255
test_images = test_images.reshape((10000, 28, 28, 1)).astype("float32") / 255
train_images, val_images = tf.split(train_images, [48000, 12000], axis=0)
train_labels, val_labels = tf.split(train_labels, [48000, 12000], axis=0)
train_dataset = tf.data.Dataset.from_tensor_slices(
    (train_images, train_labels)).shuffle(
        48000, seed=params['seed']).repeat().batch(params['batch_size'])
val_dataset = tf.data.Dataset.from_tensor_slices(
    (val_images, val_labels)).batch(400)
test_dataset = tf.data.Dataset.from_tensor_slices(
    (test_images, test_labels)).batch(1000)

train_callbacks = []
test_callbacks = []

if args.aimd and task_index == 0:
    from t9k.aimd.keras import AIMDFitCallback, AIMDEvalCallback
    train_callbacks.append(AIMDFitCallback(trial))
    test_callbacks.append(AIMDEvalCallback(trial))

if args.log_dir and task_index == 0:
    log_dir = args.log_dir
    if os.path.exists(log_dir):
        shutil.rmtree(log_dir, ignore_errors=True)
    tensorboard_callback = callbacks.TensorBoard(log_dir=log_dir)
    train_callbacks.append(tensorboard_callback)

model.fit(train_dataset,
        epochs=params['epochs'],
        steps_per_epoch=48000 // params['batch_size'],
        validation_data=val_dataset,
        callbacks=train_callbacks,
        verbose=2)

if args.save_path:
    if task_index == 0:
        save_path = args.save_path
    else:
        dirname = os.path.dirname(args.save_path)
        basename = os.path.basename(
            args.save_path) + '_temp_' + str(task_index)
        save_path = os.path.join(dirname, basename)
    if os.path.exists(save_path):
        shutil.rmtree(save_path, ignore_errors=True)
    model.save(save_path)
    if task_index != 0:
        shutil.rmtree(save_path, ignore_errors=True)

model.evaluate(test_dataset, callbacks=test_callbacks, verbose=2)

if args.aimd and task_index == 0:
    trial.finish()
```

编写一个下载数据集的脚本并运行，以将数据集文件 `mnist.npz` 下载到 Codepack 中。具体代码如下：

```python
import os
import tensorflow as tf

_, _ = tf.keras.datasets.mnist.load_data(
os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mnist.npz'))
```

<!-- TODO: Use dataset management module / s3 database
<aside class="note tip">
<div class="title">提示</div>

本例中的数据集文件较小（只有 11 MB），因此将其放到 Codepack 中，并随同 Codepack 整个复制到 PVC 中是可行的。但在数据集文件较大的情况下更加推荐将其存放到平台的数据集管理模块中。

</aside>
-->

考虑在平台上运行时需要创建 PVC、Notebook（可选，便于进一步开发或对 PVC 中的文件进行修改）和 TensorFlowTrainingJob，分别编写相应的资源配置文件如下：

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: codepack-example
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 2Gi
```

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: Notebook
metadata:
  name: codepack-example
spec:
  template:
    spec:
      containers:
        - name: notebook
          image: 'registry.tensorstack.cn/t9k/tensorflow-2.8.0-notebook-cpu:1.50.0'
          resources:
            limits:
              cpu: '1'
              memory: 1Gi
            requests:
              cpu: 500m
              memory: 500Mi
          volumeMounts:
            - name: workingdir
              mountPath: /t9k/mnt
      volumes:
        - name: workingdir
          persistentVolumeClaim:
            claimName: codepack-example
```

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: TensorFlowTrainingJob
metadata:
  name: codepack-example
spec:
  scheduler:
    t9kScheduler:
      queue: default
      priority: 50
  runPolicy:
    cleanUpPolicy: Unfinished
    backoffLimit: 20           # 所有Pod最多共重启20次
  tensorboardSpec:
    trainingLogFilesets:
      - t9k://pvc/codepack-example/mnist-keras/log
    image: t9kpublic/tensorflow-2.7.0:cpu
  replicaSpecs:
    - type: worker
      replicas: 4
      restartPolicy: OnFailure
      template:
        spec:
          securityContext:
            runAsUser: 1000
          containers:
            - command:
                - python        # 运行脚本的命令
                - main.py
                - "--no_cuda"
                - "--log_dir"
                - "log"
                - "--save_path"
                - "saved-model"
              workingDir: /mnt/mnist-keras/    # 工作路径,与定义文件中Codepack的
              imagePullPolicy: IfNotPresent    # 复制路径一致
              image: t9kpublic/tensorflow-2.7.0:cpu
              name: tensorflow
              resources:
                requests:
                  cpu: 2000m
                  memory: 2Gi
                limits:
                  cpu: 4000m
                  memory: 4Gi
              volumeMounts:
                - mountPath: /mnt
                  name: data
          volumes:
            - name: data
              persistentVolumeClaim:
                claimName: codepack-example
```

现在 Codepack 的文件结构如下：

```
mnist-keras
├── download_dataset.py
├── main.py
├── mnist.npz
├── notebook.yaml
├── pvc.yaml
└── trainingjob.yaml
```

### 编写 Codepack 定义文件

然后编写 [Codepack 的定义文件](./codepack.md)。考虑在平台中运行该 Codepack 的过程，将其拆分为 4 个具体的任务，分别是：

1. 准备环境，这里只包含创建 PVC。使用 verb apply 并提供 `pvc.yaml` 文件的路径。
1. 复制整个 Codepack 到 PVC。使用 verb copy 并提供源和目标位置的路径。
1. 创建 Notebook。使用 verb create 并提供 `notebook.yaml` 文件的路径。需要依赖 1 和 2。
1. 进行分布式训练，即创建 TrainingJob。使用 verb create 并提供 `trainingjob.yaml` 文件的路径。需要依赖 1 和 2。

据此完成的定义文件如下：

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
  - name: create-notebook    # Create a notebook with the codepack in it
    deps: ["prepare-env", "copy-file"]
    actions:
      - name: notebook
        verb: create
        files: [notebook.yaml]
  - name: run-distributed-training    # Run a distributed training
    deps: ["prepare-env", "copy-file"]
    actions:
      - name: trainingjob
        verb: create
        files: [trainingjob.yaml]

```

最终 Codepack 的文件结构如下：

```
mnist-keras
├── codepack.yaml
├── download_dataset.py
├── main.py
├── mnist.npz
├── notebook.yaml
├── pvc.yaml
└── trainingjob.yaml
```

### 对 Codepack 进行版本控制（可选）

将 Codepack 创建为一个 Git 仓库以进行版本控制，之后您就可以使用任意的本地或远程仓库方便地进行版本控制和分发。

## 运行 Codepack

使用 [Codepack CLI](./cli.md) 运行 Codepack。

### 配置身份验证信息

Codepack CLI 支持多种身份验证方式，您可以选择其中一种并进行相应的配置。详细步骤请参阅[身份验证](./cli.md#身份验证)。

### 使用命令行工具运行 Codepack

先使用以下命令运行 target `create-notebook`：

```shell
$ codepack run examples/mnist-keras -t create-notebook -p demo
RUN target create-notebook of codepack mnist-keras in project demo
Running sequence: prepare-env -> copy-file -> create-notebook

Target 1/3: prepare-env
APPLY by files ['pvc.yaml']
PersistentVolumeClaim codepack-example created
Target 2/3: copy-file
COPY from . to codepack-example:.
copied
Target 3/3: create-notebook
CREATE by files ['notebook.yaml']
Notebook codepack-example created
```

再使用以下命令运行 target `run-distributed-training`：

```shell
$ codepack run examples/mnist-keras -t run-distributed-training -p demo
RUN target run-distributed-training of codepack mnist-keras in project demo
Running sequence: prepare-env -> copy-file -> run-distributed-training

Target 1/3: prepare-env
APPLY by files ['pvc.yaml']
PersistentVolumeClaim with the name codepack-example already exists, skip
Target 2/3: copy-file
COPY from . to codepack-example:.
copied
Target 3/3: run-distributed-training
CREATE by files ['trainingjob.yaml']
TensorFlowTrainingJob codepack-example created
```

可以看到在运行这两个 target 的过程中，Codepack CLI 自动解析了工作流并顺序运行各个依赖的 target，按照 YAML 配置文件创建了各资源以及复制整个 Codepack 到 PVC。在运行 target `run-distributed-training` 的过程中，Codepack CLI 跳过了第一个 target（因为 PVC 已经创建），第二个 target 也实际上没有更新 PVC 中的文件（因为背后调用的是 rsync）。
