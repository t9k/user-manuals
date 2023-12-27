# AutoTuneExperiment

您可以通过创建 AutoTuneExperiment 来实现自动优化模型超参数。

## 创建 AutoTuneExperiment

下面是一个基本的 AutoTuneExperiment 示例：

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: AutoTuneExperiment
metadata:
  name: experiment-sample
spec:
  maxExecSeconds: 7200
  maxTrialNum: 50
  trialConcurrency: 3
  searchSpace: |-
    {
      "batch_size": {"_type": "choice", "_value": [512, 1024, 2048, 4096, 8092]},
      "learning_rate": {"_type": "choice", "_value": [0.0001, 0.001, 0.01, 0.1]}
    }
  trainingConfig:
    type: tensorflow
    tasks:
      - type: worker
        replicas: 1
        template:
          spec:
            securityContext:
              runAsUser: 1000
            containers:
              - command:
                  - python3
                  - dist_mnist.py
                workingDir: /mnt/mnist-distributed
                imagePullPolicy: IfNotPresent
                image: registry.tensorstack.cn/t9k/tensorflow-1.15.2:tuner-2.23
                name: tensorflow
  tuner:
    builtinTunerName: TPE
    classArgs: |-
      {
        "optimize_mode": "minimize", 
        "constant_liar_type": "min"
      }
```

在该例中：

* 使用 TensorFlowTrainingJob 进行训练（由 `trainingConfig` 字段指定，详细配置方法请参阅[训练框架支持](#训练框架支持)）。
* 使用 TPE 算法进行超参数调优，算法的参数为 `{"optimize_mode": "minimize", "constant_liar_type": "min"}`（由 `tuner` 字段指定，更多参数请参阅[超参数调优算法](./concepts/tuner.md)）。
* 超参数的搜索空间为 `{"batch_size": {"_type": "choice", "_value": [512, 1024, 2048, 4096, 8092]},"learning_rate": {"_type": "choice", "_value": [0.0001, 0.001, 0.01, 0.1]}}`（由 `searchSpace` 字段指定，搜索空间的格式及含义请参阅[搜索空间](./concepts/search_space.md)）。
* 可以同时测试 3 组超参数，最大测试次数为 50（分别由 `trialConcurrency` 和 `maxTrialNum` 字段指定），实验的最大执行时间为 2 小时（7200 秒，由 `maxExecSeconds` 字段指定），如果时间超出，实验进入 `TIMEOUT` 状态。

## 数据库的使用

AutoTuneExperiment 支持将实验数据存储在 AIMD 中，通过设置 `spec.aimd` 字段以使用 AIMD 数据库，其中：

* `spec.aimd.folder` 声明实验数据存储在哪个 AIMD 文件夹中，内容应填写文件夹的 ID。
* `spec.aimd.secret` 引用一个 K8s Secret，其中应记录 API Key，用于上传数据时进行身份验证。

下面是一个存储 APIKey 的 Secret 示例：

```yaml
apiVersion: v1
data:
  apikey: ZDQyMjJjZjUtMmI0Ni00Mjk2LWFiMzYtYWI4NmVhZGUwZjQx
kind: Secret
metadata:
  name: aimd-secret
type: Opaque
```

## 搜索空间

搜索空间是实验过程中超参数的设置范围，AutoTuneExperiment 会在此范围中选择超参数进行训练，最后找出最优的超参数组合。

搜索空间是一个 JSON 结构，具体格式请参阅[搜索空间](./concepts/search_space.md)。

## 训练框架支持

AutoTuneExperiment 支持对多种训练框架进行超参数的调优，包括 TensorFlow、PyTorch 和 XGBoost。

AutoTuneExperiment 通过设置 `spec.trainingConfig` 字段实现对上述框架的支持。其中：

* `spec.trainingConfig.type` 可设置为 `tensorflow`、`pytorch` 和 `xgboost`，分别表示使用 TensorFlow、PyTorch 和 XGBoost 框架进行训练。
* `spec.trainingConfig.tasks` 字段的设置请根据所使用的框架种类分别参阅 [TensorFlowTrainingJob](../../workflow/job/tensorflowtrainingjob.md)、[PyTorchTrainingJob](../../workflow/job/pytorchtrainingjob.md) 和 [XGBoostTrainingJob](../../workflow/job/xgboosttrainingjob.md)。

## 超参数调优算法

AutoTuneExperiment 在调参过程中需要使用超参数调优算法对超参数进行选择，对于不同的训练框架和不同的超参数种类，超参数调优算法的效率和效果也是不一样的。

算法根据功能和定义分为两类：

* Tuner 算法：超参数调优算法，用于选取合适的超参数组合。
* Assessor 算法：训练评估算法，用于判断当前训练是否符合预期，如果不符合则终止训练。

算法的详细介绍以及参数配置请参阅[超参数调优算法](./concepts/tuner.md)。

## 实验状态

AutoTuneExperiment 的生命周期包括以下五个阶段：

* `PENDING`：AutoTune 的相关组件（包括 AutoTune Server 和 AutoTune Web）已经创建成功，等待控制器启动 AutoTuneExperiment。
* `RUNNING`：AutoTuneExperiment 运行中。
* `TIMEOUT`：如果达到最大执行时间（由 `spec.maxExecSeconds` 字段指定）后，实验仍未完成（实际训练次数小于 `maxTrialNum` 字段指定的训练次数），则实验超时，不再创建新的训练。
* `DONE`：AutoTuneExperiment 在最大执行时间内完成了 `maxTrialNum` 字段指定的训练次数（无论成功或失败），则实验完成。
* `ERROR`：AutoTuneExperiment 初始化阶段或运行阶段出现错误。

<figure>
  <img alt="phase" src="../../assets/modules/building/autotune/phase.drawio.svg" width="350" />
</figure>

## 下一步

* 了解如何[使用 AutoTune 进行超参数优化](../../tasks/autotune.md)
