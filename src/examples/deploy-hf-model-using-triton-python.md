# 使用 Triton 部署 Hugging Face 模型（Python 后端）

<a target="_blank" rel="noopener noreferrer" href="https://github.com/triton-inference-server/server">Triton Inference Server</a> 是一个开源的推理服务软件，旨在简化 AI 推理流程。Triton 使用户能够部署多种深度学习框架的模型，包括 TensorRT、TensorFlow、PyTorch、ONNX、OpenVINO 等。Triton 支持在云、数据中心、边缘和嵌入式设备的 NVIDIA GPU、x86 CPU 和 ARM CPU 上进行推理。Triton 为许多查询类型提供了优化的性能，包括实时、批处理、集成和音频/视频流。

<a target="_blank" rel="noopener noreferrer" href="https://huggingface.co/">Hugging Face</a> 是一个 AI 开源社区，其提供的代码库托管了大量流行的开源模型。凭借 <a target="_blank" rel="noopener noreferrer" href="https://github.com/triton-inference-server/python_backend">Python 后端</a>所提供的灵活性，Triton 可以部署几乎任何来自 Hugging Face 的模型。

本示例使用 MLService，以及 Triton 推理服务器和它的 Python 后端部署一个 Hugging Face 模型的推理服务。模型存储使用 PVC。

## 准备

在项目中创建一个名为 `triton-python`、大小 50 GiB 以上的 PVC，然后创建一个同样名为 `triton-python` 的 Notebook 挂载该 PVC（镜像类型和模板不限）。

进入 Notebook，启动一个终端，执行以下命令以克隆 <a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/examples">`t9k/examples`</a> 仓库：

```bash
cd ~
git clone https://github.com/t9k/examples.git
```

我们需要创建一个<a target="_blank" rel="noopener noreferrer" href="https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_repository.md">模型仓库（model repository）</a>用于 Triton 加载模型。这里使用预制的模型仓库：

```bash
cp -R examples/deployments/triton-python/python_model_repository .
```

然后从 Hugging Face Hub 下载要部署的模型，这里以 <a target="_blank" rel="noopener noreferrer" href="https://huggingface.co/google/vit-base-patch16-224-in21k">vit-base-patch16-224-in21k</a> 模型为例：

```bash
huggingface-cli download google/vit-base-patch16-224-in21k \
  --local-dir vit-base-patch16-224-in21k --local-dir-use-symlinks False
```

<aside class="note info">
<div class="title">Vision Transformer 模型</div>

Vision Transformer（ViT）模型是计算机视觉领域的一项突破性创新，它首次将 Transformer 架构应用于图像识别任务。ViT 模型将图像分割成固定大小的块（patch），将每个块转换为一个向量，再使用 Transformer 对这些向量进行处理。vit-base-patch16-224-in21k 模型是在 ImageNet-21k 数据集（包含 1400 万张图像，分为 21,843 个类别）上以 224x224 分辨率预训练的 ViT 模型。

</aside>

## 部署

使用以下 YAML 配置文件创建 MLServiceRuntime 和 MLService 以部署服务：

```bash
cd examples/deployments/triton-python
kubectl apply -f mlservice-runtime.yaml
kubectl create -f mlservice.yaml
```

监控服务是否准备就绪：

```bash
kubectl get -f mlservice.yaml -w
```

待其 `READY` 值变为 `true` 后，便可开始使用该服务。第一次拉取镜像可能会花费较长的时间，具体取决于集群的网络状况。

## 使用推理服务

继续使用 Notebook 的终端，使用作为推理客户端的 Python 脚本发送推理请求：

```bash
address=$(kubectl get -f mlservice.yaml -ojsonpath='{.status.address.url}' | sed 's#^https\?://##')
pip install tritonclient gevent geventhttpclient
python client.py --server_address $address --model_name python_vit
```

<img alt="image" src="../assets/examples/deploy-model-using-triton-python/000000161642.jpg" style="max-width: 33%">

该脚本从指定 URL 下载一个图像文件（如上图所示），将其转换为 NumPy 数组，然后发送到推理服务器；从返回的响应中取出 `last_hidden_state`，即 Transformer 最后一层的输出张量，打印其值和形状。输出应类似于：

```
[[[ 0.2463658   0.12966464  0.13196409 ... -0.12697077  0.08220191
   -0.1261508 ]
  [ 0.10375027  0.15543337  0.14776552 ... -0.09246814  0.10163841
   -0.31893715]
  [ 0.04861938  0.15119025  0.14414431 ... -0.08075114  0.0719012
   -0.32684252]
  ...
  [ 0.2877585   0.15052384  0.17233661 ... -0.07538544  0.05114003
   -0.19613911]
  [ 0.21476139  0.17660537  0.14951637 ... -0.09027394  0.0747345
   -0.31565955]
  [ 0.2561764   0.16620857  0.13983792 ... -0.06043544  0.08778334
   -0.14347576]]]
(1, 197, 768)
```

最后一层的输出张量可以作为图像的整体表示，进一步用于分类、图像识别等下游任务。我们可以在这样一个推理客户端示例的基础上进一步开发 AI 应用。

## 参考

* <a target="_blank" rel="noopener noreferrer" href="https://github.com/triton-inference-server/server">GitHub 上的 Triton Inference Server</a>
  * Triton 官方教程：<a target="_blank" rel="noopener noreferrer" href="https://github.com/triton-inference-server/tutorials/tree/main/HuggingFace#deploying-huggingface-models">Deploying HuggingFace models</a>
  * Triton <a target="_blank" rel="noopener noreferrer" href="https://github.com/triton-inference-server/python_backend">Python 后端</a>
* <a target="_blank" rel="noopener noreferrer" href="https://huggingface.co/">Hugging Face</a>
