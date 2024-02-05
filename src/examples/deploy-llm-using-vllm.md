# 使用 vLLM 部署 LLM 推理服务

部署 LLM 推理服务面临着多方面的挑战，包括计算资源需求、延迟和吞吐量、成本控制等。[vLLM](https://github.com/vllm-project/vllm) 是一个快速、灵活且易于使用的 LLM 推理和服务库，其利用 PagedAttention 注意力算法优化注意力机制的键值存储，有效节约内存空间以用于批处理请求，从而显著提高服务的吞吐量。vLLM 能够有效控制运行成本，利用有限的计算资源为更多用户提供高吞吐量和低延迟的 LLM 推理服务。

本示例使用 MLService 部署一个 vLLM 推理服务。模型存储使用 PVC。

相比[部署 LLM 聊天机器人](./deploy-llm-chatbot.md)，本示例使用了更高效的推理后端，以及可用于生产环境的 MLService。

## 准备

在项目中创建一个名为 `vllm`、大小 30 GiB 以上的 PVC，然后创建一个同样名为 `vllm` 的 Notebook 挂载该 PVC（镜像类型和模板不限）。

进入 Notebook 或远程连接到 Notebook，启动一个终端，执行以下命令以下载 CodeLlama-7b-Instruct-hf 的模型文件：

```bash
# 方法1：如果可以直接访问 huggingface
huggingface-cli download codellama/CodeLlama-7b-Instruct-hf \
  --local-dir CodeLlama-7b-Instruct-hf --local-dir-use-symlinks False

# 方法2：对于国内用户，使用 modelscope
pip install modelscope
python -c \
  "from modelscope import snapshot_download; snapshot_download('AI-ModelScope/CodeLlama-7b-Instruct-hf')"
mv .cache/modelscope/hub/AI-ModelScope/CodeLlama-7b-Instruct-hf .
```

<aside class="note info">
<div class="title">Code Llama 系列模型</div>

<a target="_blank" rel="noopener noreferrer" href="https://github.com/facebookresearch/codellama">Code Llama</a> 是 Llama 2 的代码专精版本，提供当下开源模型中的 SOTA 性能、填充能力（inflling capability）、对长上下文的支持，以及对编程任务的 zero-shot 指令遵循能力。更多信息请参阅<a target="_blank" rel="noopener noreferrer" href="https://ai.meta.com/blog/code-llama-large-language-model-coding/">官方博客</a>。

</aside>

## 部署推理服务

这里将 vLLM 部署为兼容 OpenAI API 的服务器，这样 vLLM 可以作为使用 OpenAI API 的应用程序的即插即用替代品。

使用以下 YAML 配置文件创建 MLServiceRuntime：

<details><summary><code class="hljs">mlservice-runtime.yaml</code></summary>

```yaml
{{#include ../assets/examples/deploy-llm-using-vllm/mlservice-runtime.yaml}}
```

</details>

```bash
kubectl apply -f mlservice-runtime.yaml
```

再使用以下 YAML 配置文件创建 MLService 以部署服务（必要时修改 `spec.scheduler.t9kScheduler.queue` 字段指定的队列）：

<details><summary><code class="hljs">mlservice.yaml</code></summary>

```yaml
{{#include ../assets/examples/deploy-llm-using-vllm/mlservice.yaml}}
```

</details>

```bash
kubectl create -f mlservice.yaml
```

<aside class="note tip">
<div class="title">提示</div>

本示例以 7B 模型为例，用户也可以尝试部署 13B、34B 和 70B 模型，但需要提供更多的计算资源。下面给出了相应的计算资源需求，以及部署 70B 模型的 YAML 配置文件：

| 大小 | PVC 大小 | 并行度×显存大小          |
| ---- | -------- | ------------------------ |
| 7B   | 30GiB    | 1×24GB                   |
| 13B  | 55GiB    | 2×24GB / 1×40GB          |
| 34B  | 130GiB   | 4×24GB / 2×40GB / 1×80GB |
| 70B  | 260GiB   | 4×40GB / 2×80GB          |

<details><summary><code class="hljs">mlservice-runtime-70b.yaml</code></summary>

```yaml
{{#include ../assets/examples/deploy-llm-using-vllm/mlservice-runtime-70b.yaml}}
```

</details>

<details><summary><code class="hljs">mlservice-70b.yaml</code></summary>

```yaml
{{#include ../assets/examples/deploy-llm-using-vllm/mlservice-70b.yaml}}
```

</details>

如果没有足够的显存，可以尝试<a target="_blank" rel="noopener noreferrer" href="https://docs.vllm.ai/en/latest/quantization/auto_awq.html">量化</a>方法。

</aside>

## 使用推理服务

继续使用 Notebook 的终端，使用 `curl` 命令发送聊天或生成文本的请求：

``` bash
address=$(kubectl get -f mlservice.yaml -ojsonpath='{.status.address.url}')

# 聊天
curl ${address}/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "codellama-7b",
    "messages": [{"role": "user", "content": "hello"}],
    "temperature": 0.5
  }'

# 生成文本
curl ${address}/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "codellama-7b",
    "prompt": "Long long ago, there was",
    "max_tokens": 100,
    "temperature": 0.5
  }'
```

返回的响应类似于：

<details><summary>响应</summary>

```json
{{#include ../assets/examples/deploy-llm-using-vllm/response.log}}
```

</details>

[部署 LLM 聊天机器人](./deploy-llm-chatbot.md)提供的[聊天方法](./deploy-llm-chatbot.md#开始聊天)在这里同样适用。

## 编写代码

现在让它发挥自己的特长，写一个<a target="_blank" rel="noopener noreferrer" href="https://leetcode.cn/problems/roman-to-integer/">罗马数字转整数</a>的 Python 程序。一次编写代码的聊天记录如下：

<details><summary>聊天记录</summary>

{{#include ../assets/examples/deploy-llm-using-vllm/roman-to-integer.log}}

</details>

得益于 vLLM 提供的高吞吐量推理服务，该解答的生成仅用了 6s，然而并不正确，未能通过 LeetCode 的测试。

顺带一提，使用相同的 prompt（由于 CodeLlama-7b-Python-hf 未经过指令微调，prompt 的格式略有不同），CodeLlama-13b-Instruct-hf 和 CodeLlama-7b-Python-hf 提供的解答可以通过，GPT 3.5、GPT-4 和 Bard 提供的解答也都可以通过。

用户可以自行尝试部署更大的 Code Llama 系列模型，并让其编写更加复杂的代码。


## 参考

<https://github.com/vllm-project/vllm>

<https://github.com/facebookresearch/codellama>

<https://huggingface.co/codellama/CodeLlama-7b-Instruct-hf>
