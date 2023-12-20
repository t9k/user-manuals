# 超参数调优算法

AutoTuneExperiment 在调参过程中需要使用超参数调优算法对超参数进行选择，对于不同的训练框架和不同的超参数种类，超参数调优算法的效率和效果也是不一样的。

算法根据功能和定义分为两类：

* Tuner 算法：超参数调优算法，用于选取合适的超参数组合。
* Assessor 算法：训练评估算法，用于判断当前超参数的训练中间结果是否符合预期，如果不符合则终止训练。

## Tuner 算法

### HyperOpt 类算法

HyperOpt 是一个用于超参数调优的 Python 库，其中主要包含三种超参数调优算法：`Random`、`Anneal` 和 `TPE`。三种算法之间的区别以及算法的使用方法请参阅 [HyperOpt 文档:octicons-link-external-16:](https://hyperopt.github.io/hyperopt/){target=_blank}。

算法支持使用的搜索方法有：`choice`、`randint`、`loguniform` 和 `qloguniform`。

下面是 AutoTuneExperiment 使用此算法的一个示例（示例中的 `classArgs` 字段包含当前算法所有参数，有些参数在实际使用中可以选择不指定）：

```json
{
  "tuner": {
    "builtinTunerName": "Anneal",
    "classArgs": {
      "optimize_mode": "minimize", 
      "constant_liar_type": "min"
    }
  }
}
```

### Evolution

进化算法（Evolution）是受生物进化启发得到的一种优化算法。进化算法的详细介绍请参阅 [Evolutionary algorithm WIKI 文档:octicons-link-external-16:](https://en.wikipedia.org/wiki/Evolutionary_algorithm){target=_blank}。

下面是 AutoTuneExperiment 使用此算法的一个示例（示例中的 `classArgs` 字段包含当前算法所有参数，有些参数在实际使用中可以选择不指定）：

```json
{
  "tuner": {
    "builtinTunerName": "Evolution",
    "classArgs": {
      "optimize_mode": "minimize", 
      "population_size": 32
    }
  }
}
```

### Batch

Batch 是一种最简单的选参算法，此算法只支持一种超参数的优化（搜索空间中只能有一个条目）且仅支持 `choice` 搜索方法。

下面是 AutoTuneExperiment 使用此算法的一个示例（Batch 算法不需要填写参数）：

```json
{
  "searchSpace": {
      "learning_rate": {"_type": "choice", "_value": [0.0001, 0.001, 0.01, 0.1]}
  },
  "tuner": {
    "builtinTunerName": "Batch"
  }
}
```

上述示例中，搜索空间中只有一个超参数，且 `_type` 为 `choice`；Batch 算法不需要传入参数，所以没有填写 `tuner.classArgs` 字段。

### GridSearch

一种基本的选参算法，根据搜索空间中的参数和范围，枚举所有可能的超参数组合，一一测试。

算法支持使用的搜索方法有：`choice`、`randint` 和 `quniform`。

下面是 AutoTuneExperiment 使用此算法的一个示例（GridSearch 算法不需要填写参数）：

```json
{
  "tuner": {
    "builtinTunerName": "GridSearch"
  }
}
```

### MetisTuner

Metis 算法的详细介绍请参阅论文 [*Metis: Robustly Optimizing Tail Latencies of Cloud Systems*:octicons-link-external-16:](https://www.microsoft.com/en-us/research/publication/metis-robustly-tuning-tail-latencies-cloud-systems/){target=_blank}。

算法支持使用的搜索方法有：`choice`、`randint`、`uniform` 和 `quniform`。

下面是 AutoTuneExperiment 使用此算法的一个示例（示例中的 `classArgs` 字段包含当前算法所有参数，有些参数在实际使用中可以选择不指定）：

```json
{
  "tuner": {
    "builtinTunerName": "MetisTuner",
    "classArgs": {
      "optimize_mode": "maximize",
      "no_resampling": true,
      "no_candidates": false,
      "selection_num_starting_points": 600,
      "cold_start_num": 10,
      "exploration_probability": 0.9
    }
  }
}
```

### GPTuner

GPT 是一种能够极大减少超参数优化步骤的贝叶斯优化算法。算法的详细介绍请参阅 [NNI GPTuner 文档:octicons-link-external-16:](https://nni.readthedocs.io/en/stable/Tuner/GPTuner.html){target=_blank}。

算法支持使用的搜索方法有：`randint`、`uniform`、`quniform`、`loguniform`、`qloguniform` 和数字形式的 `choice`。

下面是 AutoTuneExperiment 使用此算法的一个示例（示例中的 `classArgs` 字段包含当前算法所有参数，有些参数在实际使用中可以选择不指定）：

```json
{
  "tuner": {
    "builtinTunerName": "GPTuner",
    "classArgs": {
      "optimize_mode": "maximize",
      "utility": "ei",
      "kappa": 5,
      "xi": 0,
      "nu": 2.5,
      "alpha": 1e-6,
      "cold_start_num": 10,
      "selection_num_warm_up": 100000,
      "selection_num_starting_points": 250
    }
  }
}
```

### PPOTuner

PPO 算法继承了 [OpenAI 中 ppo2:octicons-link-external-16:](https://github.com/openai/baselines/tree/master/baselines/ppo2){target=_blank} 的主要逻辑，并适应 NAS 场景。

算法支持使用的搜索方法有：`layer_choice` 和 `input_choice`。下面是一个搜索空间设置的示例：

```json
{
  "first_conv": {"_type": "layer_choice", "_value": ["conv5x5", "conv3x3"]},
  "mid_conv": {"_type": "layer_choice", "_value": ["0", "1"]},
  "skip": {
    "_type": "input_choice",
    "_value": {"candidates": ["", ""], "n_chosen": 1}
  }
}
```

下面是 AutoTuneExperiment 使用此算法的一个示例（示例中的 `classArgs` 字段包含当前算法所有参数，有些参数在实际使用中可以选择不指定）：

```json
{
  "tuner": {
    "builtinTunerName": "PPOTuner",
    "classArgs": {
      "optimize_mode": "maximize",
      "trials_per_update": 20,
      "epochs_per_update": 4,
      "minibatch_size": 4,
      "ent_coef": 0.0,
      "lr": 3e-4,
      "vf_coef": 0.5,
      "max_grad_norm": 0.5,
      "gamma": 0.99,
      "lam": 0.95,
      "cliprange": 0.2
    }
  }
}
```

### PBTTuner

PBT 算法得自 [*Population Based Training of Neural Networks*:octicons-link-external-16:](https://arxiv.org/abs/1711.09846){target=_blank}。

下面是 AutoTuneExperiment 使用此算法的一个示例（示例中的 `classArgs` 字段包含当前算法所有参数，有些参数在实际使用中可以选择不指定）：

```json
{
  "tuner": {
    "builtinTunerName": "PBTTuner",
    "classArgs": {
      "optimize_mode": "maximize",
      "population_size": 10,
      "factor": 0.2,
      "resample_probability": 0.25,
      "fraction": 0.2
    }
  }
}
```

## Assessor 算法

### Medianstop

Medianstop 算法的逻辑是：如果在某一步 `S`，当前运行的实验的最佳观测值比所有已经完成的训练的第 S 步前的观测值的中位数差，则停止此次训练。此策略出自论文 [*Google Vizier: A Service for Black-Box Optimization*:octicons-link-external-16:](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/46180.pdf){target=_blank} 。

下面是 AutoTuneExperiment 使用此算法的一个示例（示例中的 `classArgs` 字段包含当前算法所有参数，有些参数在实际使用中可以选择不指定）：

```json
{
  "assessor": {
    "builtinAssessorName": "Medianstop",
    "classArgs": {
      "optimize_mode": "maximize",
      "start_step": 0
    }
  }
}
```

在上述示例中，`start_step` 表示从第几步开始上传观测值（过早上传观测值，可能会错误的停止一些刚开始表现较差的训练）。

### Curvefitting

Curvefitting 算法使用学习曲线拟合算法来预测未来的学习曲线性能。其逻辑是：如果在某一步，当前训练的预测结果是收敛的并且比历史上的最佳结果差，则停止此次训练。Curvefitting 算法的详细介绍请参阅 [NNI Curvefitting 文档:octicons-link-external-16:](https://nni.readthedocs.io/en/latest/Assessor/CurvefittingAssessor.html){target=_blank}。

下面是 AutoTuneExperiment 使用此算法的一个示例（示例中的 `classArgs` 字段包含当前算法所有参数，有些参数在实际使用中可以选择不指定）：

```json
{
  "assessor": {
    "builtinAssessorName": "Curvefitting",
    "classArgs": {
      "optimize_mode": "minimize",
      "epoch_num": 20,
      "start_step": 6,
      "threshold": 0.95,
      "gap": 1
    }
  }
}
```
