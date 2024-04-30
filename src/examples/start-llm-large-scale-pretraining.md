# 启动 LLM 大规模预训练

LLM（大型语言模型）是当前 AI 领域备受瞩目的研究和应用领域。预训练是构建 LLM 的初始步骤，通常需要在 GPU 集群上进行大规模（10^3~10^4 卡）的并行训练，从而使模型获得对语言结构、语义直至语言所描述的世界和各种规律的全面理解。

在集群上运行大规模模型训练面临着一些关键挑战：

* 有效地分配和管理计算资源以满足模型训练的计算需求是一项复杂任务，需要避免资源浪费和不必要的等待时间。
* 数据的并行加载和分发以及模型参数的同步和更新，需要高效的通信和协调机制，以确保训练的一致性和速度。
* 故障容错和中断恢复必不可少，因为在大规模集群上运行时硬件故障和网络问题可能导致训练中断。

<a target="_blank" rel="noopener noreferrer" href="https://github.com/microsoft/DeepSpeed">DeepSpeed</a> 是目前最受欢迎的大规模分布式训练框架，而平台提供了 [DeepSpeedJob](../modules/jobs/deepspeedjob.md)，这是专为使用 DeepSpeed 框架的分布式训练而设计的 Job 类型。

本示例将使用 DeepSpeedJob 以简便迅速的方式启动 Megatron-LM GPT-3 系列（125M、1.3B、13B 和 175B）模型的预训练任务。

## 准备

在你的项目中创建一个名为 `megatron`、大小 250 GiB 以上的 PVC，然后创建一个同样名为 `megatron` 的 Notebook 挂载该 PVC（镜像类型和模板不限）。

进入 Notebook，启动一个终端，执行以下命令以克隆必要的仓库：

```bash
cd ~
git clone https://github.com/microsoft/Megatron-DeepSpeed.git
git clone https://github.com/NVIDIA/Megatron-LM.git
git clone https://github.com/t9k/examples.git
```

<aside class="note info">
<div class="title">Megatron-LM</div>

<a target="_blank" rel="noopener noreferrer" href="https://github.com/NVIDIA/Megatron-LM">Megatron-LM</a> 是 NVIDIA 应用深度学习研究团队开发的大型 transformer 代码库，用于高效地训练多达 1 trillion 参数的 LLM，并实现了多种并行技术。<a target="_blank" rel="noopener noreferrer" href="https://github.com/microsoft/Megatron-DeepSpeed">Megatron-DeepSpeed</a> 是 DeepSpeed 版本的 Megatron-LM，其增加了对几个功能的额外支持，如 MoE 训练、课程学习、3D 并行性等。

本示例所使用的训练代码即来自这两个项目。

</aside>

选用 enwiki（英文维基百科）作为数据集，使用脚本下载数据集并进行预处理：

```bash
pip install wikiextractor
cd examples/deepspeed/megatron-gpt/dataset
python download_wiki.py en
cd ../dataset
./preprocess_wiki.sh
```

然后使用这一数据集重新训练类 GPT-2 的 tokenzier：

```bash
cd ../tokenizer
python train_tokenizer.py ../dataset/wiki-en/all wiki-en-tokenizer
```

## 启动训练

使用以下 YAML 配置文件创建 DeepSpeedJob 以启动 125M 模型的训练：

```bash
# 数据并行训练 125M 参数的 GPT 模型
kubectl create -f \
  examples/deepspeed/megatron-gpt/training/gpt-125m-4xdp.yaml
```

<aside class="note info">
<div class="title">DeepSpeedJob</div>

这里仅使用到 DeepSpeedJob 的基本功能，DeepSpeedJob 还提供了其他高级功能，例如：

1. 失败重启，以自动处理长时间训练过程中的故障场景（例如 GPU 故障）；
2. 弹性训练，以有效利用 GPU 集群的可用计算资源。

</aside>

通过以下命令查看训练过程中打印的日志：

```bash
export POD=$(kubectl get dj gpt-125m -o jsonpath="{.status.tasks[0].replicas[0].name}")
kubectl logs $POD -f
```

<figure class="screenshot">
  <img alt="log" src="../assets/examples/start-llm-large-scale-pretraining/log.png" />
</figure>

训练过程中产生的 TensorBoard 日志文件保存在 `output/gpt-1-3b/tensorboard` 路径下，同样可以在 Notebook 中创建一个 TensorBoard 实例以查看：

<figure class="screenshot">
  <img alt="tensorboard" src="../assets/examples/start-llm-large-scale-pretraining/tensorboard.png" />
</figure>

训练完成之后，模型文件将保存到 `output/gpt-125m/model` 路径下，后续用于文本生成或进一步的微调。

## 使用其他训练配置

`examples/deepspeed/megatron-gpt/training` 路径下有多个 YAML 配置文件，分别对应不同模型参数量的不同并行训练策略。例如 `gpt-13b-4xdp-4xpp-4xtp.yaml` 对应 13B 模型、4 度数据并行、4 度流水线并行以及 4 度张量并行。用户可以选择其中任意一个 YAML 配置文件创建 DeepSpeedJob，只要确保有足够的计算资源可用。

下表总结了训练 125M 和 1.3B 模型的主要参数上的差异：

<table>
  <tr>
    <td>模型参数量</td>
    <td>125M</td>
    <td>1.3B</td>
    <td>13B</td>
    <td>175B</td>
  </tr>
  <tr>
    <td>并行方式</td>
    <td>- / 2x DP / 4x DP</td>
    <td>4x DP / 8x DP / 4x DP + 4xPP</td>
    <td>4x DP + 4xPP / 4x DP + 8x PP / 4x DP + 4x PP + 4x TP</td>
    <td></td>
  </tr>
  <tr>
    <td>GPU 使用总数</td>
    <td>1 / 2 / 4</td>
    <td>4 / 8 / 16</td>
    <td>16 / 32 / 32</td>
    <td></td>
  </tr>
  <tr>
    <td>模型层数 / hidden size / 注意力头数</td>
    <td>12 / 768 / 12</td>
    <td>24 / 2048 / 16</td>
    <td>40 / 5120 / 40</td>
    <td></td>
  </tr>
  <tr>
    <td>训练的 token 数量</td>
    <td>2.5e9</td>
    <td>2.6e10</td>
    <td>2.6e11</td>
    <td>3.5e12</td>
  </tr>
  <tr>
    <td>学习率</td>
    <td>6e-4</td>
    <td>2e-4</td>
    <td>1e-4</td>
    <td></td>
  </tr>
  <tr>
    <td>预计时间*</td>
    <td>~60min</td>
    <td>~12h</td>
    <td></td>
    <td></td>
  </tr>
</table>
<p style="color: gray; text-align: center; font-size: 14px">*预计时间为参考值，与具体的硬件环境有关，这里以 A100 SXM4 80GB GPU 节点 + IB 网络连接为例。</p>
