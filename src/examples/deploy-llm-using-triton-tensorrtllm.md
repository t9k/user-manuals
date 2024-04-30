# 使用 Triton 部署 LLM 推理服务（TensorRT-LLM 后端）

<a target="_blank" rel="noopener noreferrer" href="https://github.com/triton-inference-server/server">Triton Inference Server</a> 是一个开源的推理服务软件，旨在简化 AI 推理流程。Triton 使用户能够部署多种深度学习框架的模型，包括 TensorRT、TensorFlow、PyTorch、ONNX、OpenVINO 等。Triton 支持在云、数据中心、边缘和嵌入式设备的 NVIDIA GPU、x86 CPU 和 ARM CPU 上进行推理。Triton 为许多查询类型提供了优化的性能，包括实时、批处理、集成和音频/视频流。

<a target="_blank" rel="noopener noreferrer" href="https://github.com/NVIDIA/TensorRT-LLM">TensorRT-LLM</a> 是一个工具包，用于组装优化的解决方案以执行大型语言模型（LLM）推理。它提供了一个 Python API 来定义模型，并为 NVIDIA GPU 编译高效的 TensorRT 引擎。它还包含了 Python 和 C++ 组件，用于构建运行时以执行这些引擎，以及 Triton 推理服务器的后端，以便轻松构建基于 Web 的 LLM 服务。TensorRT-LLM 支持多 GPU 和多节点配置（通过 MPI）。

本示例使用 MLService，以及 Triton 推理服务器和它的 TensorRT-LLM 后端部署一个 LLM 推理服务。模型存储使用 PVC。

相比[使用 Triton 部署 Hugging Face 模型（Python 后端）](./deploy-hf-model-using-triton-python.md)，本示例使用了 Triton 的另一个后端——<a target="_blank" rel="noopener noreferrer" href="https://github.com/triton-inference-server/tensorrtllm_backend">TensorRT-LLM 后端</a>，专用于部署 TensorRT-LLM 模型。

## 准备

在项目中创建一个名为 `triton-tensorrtllm`、大小 100 GiB 以上的 PVC，然后创建一个同样名为 `triton-tensorrtllm` 的 Notebook 挂载该 PVC（镜像选择带有 sudo 权限的 PyTorch 2.0 的类型，模板选择分配一个共享 NVIDIA GPU 的类型，并且分配的 GPU 需要有至少 16GB 的显存）。

进入 Notebook，启动一个终端，执行以下命令以克隆 <a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/examples">`t9k/examples`</a> 仓库：

```bash
cd ~
git clone https://github.com/t9k/examples.git
```

然后从 Hugging Face 或 ModelScope 下载要部署的模型，这里以 <a target="_blank" rel="noopener noreferrer" href="https://huggingface.co/meta-llama/Llama-2-7b-chat-hf">Llama-2-7b-chat-hf</a> 模型为例：

```bash
# 方法 1：如果可以直接访问 Hugging Face
# 需要登录
huggingface-cli download meta-llama/Llama-2-7b-chat-hf \
  --local-dir Llama-2-7b-chat-hf --local-dir-use-symlinks False

# 方法 2：对于国内用户，访问 ModelScope 的网络连通性更好
pip install modelscope
python -c \
  "from modelscope import snapshot_download; snapshot_download('shakechen/Llama-2-7b-chat-hf')"
mv .cache/modelscope/hub/shakechen/Llama-2-7b-chat-hf .
```

## 构建 TensorRT 引擎

安装 TensorRT-LLM：

```bash
sudo apt-get update && sudo apt-get -y install openmpi-bin libopenmpi-dev  # password: tensorstack
sudo rm /opt/conda/compiler_compat/ld  # a workaround to build mpi4py within a conda env using an external MPI
pip install tensorrt_llm==0.8.0 --extra-index-url https://pypi.nvidia.com
```

克隆 <a target="_blank" rel="noopener noreferrer" href="https://github.com/NVIDIA/TensorRT-LLM">`NVIDIA/TensorRT-LLM`</a> 仓库，利用其中的 LLaMA 示例代码，先将模型转换为 TensorRT-LLM 检查点格式，再构建 TensorRT 引擎：

```bash
git clone https://github.com/NVIDIA/TensorRT-LLM.git && cd TensorRT-LLM && git reset --hard 655524d
cd examples/llama/
python convert_checkpoint.py --model_dir ~/Llama-2-7b-chat-hf \
    --output_dir ~/Llama-2-7b-chat-hf/tllm-checkpoint-fp16-1gpu \
    --dtype float16
trtllm-build --checkpoint_dir ~/Llama-2-7b-chat-hf/tllm-checkpoint-fp16-1gpu \
    --output_dir ~/engines/1gpu \
    --gemm_plugin float16  # ~14GB GPU memory
```

## 创建模型仓库

我们还需要创建一个<a target="_blank" rel="noopener noreferrer" href="https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_repository.md">模型仓库（model repository）</a>并放入刚才构建的 TensorRT 引擎，用于 Triton 加载模型。

克隆 <a target="_blank" rel="noopener noreferrer" href="https://github.com/triton-inference-server/tensorrtllm_backend">`triton-inference-server/tensorrtllm_backend`</a> 仓库，复制其中的模型仓库模板，并修改配置：

```bash
cd ~
git clone https://github.com/triton-inference-server/tensorrtllm_backend.git && cd tensorrtllm_backend && git reset --hard da59830 && cd ~
cp -R tensorrtllm_backend/all_models/inflight_batcher_llm inflight_batcher_llm

python tensorrtllm_backend/tools/fill_template.py -i inflight_batcher_llm/preprocessing/config.pbtxt tokenizer_dir:Llama-2-7b-chat-hf/,triton_max_batch_size:64,preprocessing_instance_count:1
python tensorrtllm_backend/tools/fill_template.py -i inflight_batcher_llm/postprocessing/config.pbtxt tokenizer_dir:Llama-2-7b-chat-hf/,triton_max_batch_size:64,postprocessing_instance_count:1
python tensorrtllm_backend/tools/fill_template.py -i inflight_batcher_llm/tensorrt_llm_bls/config.pbtxt triton_max_batch_size:64,decoupled_mode:False,bls_instance_count:1,accumulate_tokens:False
python tensorrtllm_backend/tools/fill_template.py -i inflight_batcher_llm/ensemble/config.pbtxt triton_max_batch_size:64
python tensorrtllm_backend/tools/fill_template.py -i inflight_batcher_llm/tensorrt_llm/config.pbtxt triton_max_batch_size:64,decoupled_mode:False,max_beam_width:1,engine_dir:engines/1gpu,max_tokens_in_paged_kv_cache:2560,max_attention_window_size:2560,kv_cache_free_gpu_mem_fraction:0.5,exclude_input_in_output:True,enable_kv_cache_reuse:False,batching_strategy:inflight_batching,max_queue_delay_microseconds:600
```

## 部署

接下来启动 Triton 推理服务器。使用以下 YAML 配置文件创建 MLServiceRuntime 和 MLService 以部署服务：

```bash
cd examples/deployments/triton-tensorrtllm
kubectl apply -f mlservice-runtime.yaml
kubectl create -f mlservice.yaml
```

监控服务是否准备就绪：

```bash
kubectl get -f mlservice.yaml -w
```

待其 `READY` 值变为 `true` 后，便可开始使用该服务。第一次拉取镜像可能会花费较长的时间，具体取决于集群的网络状况。

## 使用推理服务

继续使用 Notebook 的终端，使用 `curl` 命令发送推理请求：

```bash
address=$(kubectl get -f mlservice.yaml -ojsonpath='{.status.address.url}' | sed 's#^https\?://##')
curl -X POST $address/v2/models/ensemble/generate -d '{"text_input": "What is machine learning?", "max_tokens": 100, "bad_words": "", "stop_words": "", "pad_id": 2, "end_id": 2}'
```

返回的响应类似于：

```json
{"context_logits":0.0,"cum_log_probs":0.0,"generation_logits":0.0,"model_name":"ensemble","model_version":"1","output_log_probs":[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],"sequence_end":false,"sequence_id":0,"sequence_start":false,"text_output":"\n\nMachine learning is a subfield of artificial intelligence (AI) that involves the use of algorithms and statistical models to enable machines to learn from data, make decisions, and improve their performance on a specific task over time.\n\nMachine learning algorithms are designed to recognize patterns in data and learn from it, without being explicitly programmed to do so. The algorithms can be trained on large datasets, and as they process more data, they can make better predictions or decisions.\n\nMachine"}
```

## 扩展：部署其他 LLM

本示例以 LLaMA 模型为例，我们还可以部署其他<a target="_blank" rel="noopener noreferrer" href="https://github.com/NVIDIA/TensorRT-LLM?tab=readme-ov-file#models">支持的模型</a>。请参照各模型的<a target="_blank" rel="noopener noreferrer" href="https://github.com/NVIDIA/TensorRT-LLM/tree/main/examples">官方示例</a>构建相应的 TensorRT 引擎。

## 参考

* <a target="_blank" rel="noopener noreferrer" href="https://github.com/triton-inference-server/server">GitHub 上的 Triton Inference Server</a>
    * Triton 官方教程：<a target="_blank" rel="noopener noreferrer" href="https://github.com/triton-inference-server/tutorials/blob/main/Popular_Models_Guide/Llama2/trtllm_guide.md">TensorRT-LLM guide</a>
    * Triton <a target="_blank" rel="noopener noreferrer" href="https://github.com/triton-inference-server/tensorrtllm_backend">TensorRT-LLM 后端</a>
* <a target="_blank" rel="noopener noreferrer" href="https://github.com/NVIDIA/TensorRT-LLM">GitHub 上的 TensorRT-LLM</a>
    * TensorRT-LLM 官方示例：<a target="_blank" rel="noopener noreferrer" href="https://github.com/NVIDIA/TensorRT-LLM/tree/main/examples/llama">LLaMA</a>
