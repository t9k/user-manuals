# 使用 vLLM 部署 LLM 推理服务

部署 LLM 推理服务面临着多方面的挑战，包括计算资源需求、延迟和吞吐量、成本控制等。<a target="_blank" rel="noopener noreferrer" href="https://github.com/vllm-project/vllm">vLLM</a> 是一个快速、灵活且易于使用的 LLM 推理和服务库，其利用 PagedAttention 注意力算法优化注意力机制的键值存储，有效节约内存空间以用于批处理请求，从而显著提高服务的吞吐量。vLLM 能够有效控制运行成本，利用有限的计算资源为更多用户提供高吞吐量和低延迟的 LLM 推理服务。

本示例使用 MLService 和 vLLM 框架部署一个 LLM 推理服务。模型存储使用 PVC。

相比[使用 FastChat 部署 LLM 推理服务](./deploy-llm-using-fastchat.md)，本示例使用了更高效的推理后端，以及可用于生产环境的 MLService。

## 准备

在项目中创建一个名为 `vllm`、大小 30 GiB 以上的 PVC，然后创建一个同样名为 `vllm` 的 Notebook 挂载该 PVC（镜像类型和模板不限）。

进入 Notebook，启动一个终端，执行以下命令以克隆 <a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/examples">`t9k/examples`</a> 仓库：

```bash
cd ~
git clone https://github.com/t9k/examples.git
```

然后从 Hugging Face 或 ModelScope 下载要部署的模型，这里以 <a target="_blank" rel="noopener noreferrer" href="https://huggingface.co/codellama/CodeLlama-7b-Instruct-hf">CodeLlama-7b-Instruct-hf</a> 模型为例：

```bash
# 方法 1：如果可以直接访问 Hugging Face
huggingface-cli download codellama/CodeLlama-7b-Instruct-hf \
  --local-dir CodeLlama-7b-Instruct-hf --local-dir-use-symlinks False

# 方法 2：对于国内用户，访问 ModelScope 的网络连通性更好
pip install modelscope
python -c \
  "from modelscope import snapshot_download; snapshot_download('AI-ModelScope/CodeLlama-7b-Instruct-hf')"
mv .cache/modelscope/hub/AI-ModelScope/CodeLlama-7b-Instruct-hf .
```

<aside class="note info">
<div class="title">Code Llama 系列模型</div>

<a target="_blank" rel="noopener noreferrer" href="https://github.com/facebookresearch/codellama">Code Llama</a> 是 Llama 2 的代码专精版本，提供当下开源模型中的 SOTA 性能、填充能力（inflling capability）、对长上下文的支持，以及对编程任务的 zero-shot 指令遵循能力。更多信息请参阅<a target="_blank" rel="noopener noreferrer" href="https://ai.meta.com/blog/code-llama-large-language-model-coding/">官方博客</a>。

</aside>

## 部署

这里将 vLLM 部署为兼容 OpenAI API 的服务器，这样 vLLM 可以作为使用 OpenAI API 的应用程序的即插即用替代品。

使用以下 YAML 配置文件创建 MLServiceRuntime 和 MLService 以部署服务：

```bash
cd examples/deployments/vllm
kubectl apply -f mlservice-runtime.yaml
kubectl create -f mlservice.yaml
```

监控服务是否准备就绪：

```bash
kubectl get -f mlservice.yaml -w
```

输出应类似于：

```
NAME           READY   REASON   URL
codellama-7b   False            http://codellama-7b.<project>.<domain>
```

待其 `READY` 值变为 `true` 后，便可开始使用该服务。第一次拉取镜像可能会花费较长的时间，具体取决于集群的网络状况。

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

## 编写代码

现在让它发挥自己的特长，写一个<a target="_blank" rel="noopener noreferrer" href="https://leetcode.cn/problems/roman-to-integer/">罗马数字转整数</a>的 Python 程序。一次编写代码的聊天记录如下：

<details><summary>聊天记录</summary>

{{#include ../assets/examples/deploy-llm-using-vllm/roman-to-integer.log}}

</details>

得益于 vLLM 提供的高吞吐量推理服务，该解答的生成仅用了 6s，然而并不正确，未能通过 LeetCode 的测试。

顺带一提，使用相同的 prompt（由于 CodeLlama-7b-Python-hf 未经过指令微调，prompt 的格式略有不同），CodeLlama-13b-Instruct-hf 和 CodeLlama-7b-Python-hf 提供的解答可以通过，GPT 3.5、GPT-4 和 Bard 提供的解答也都可以通过。

用户可以自行尝试[部署规模更大的 Code Llama 模型](#扩展部署规模更大的-llm)，并让其编写更加复杂的代码。

## 扩展：部署其他 LLM

本示例以 Code Llama 模型为例，我们还可以部署其他<a target="_blank" rel="noopener noreferrer" href="https://docs.vllm.ai/en/latest/models/supported_models.html">支持的模型</a>。例如要将部署的模型从 CodeLlama-7b-Instruct-hf 换成 Mistral-7B-Instruct-v0.1，只需：

1. 下载 Mistral-7B-Instruct-v0.1 的模型文件：

```bash
# 方法 1：如果可以直接访问 Hugging Face
# 需要登录
huggingface-cli download mistralai/Mistral-7B-Instruct-v0.1 \
  --local-dir Mistral-7B-Instruct-v0.1 --local-dir-use-symlinks False

# 方法 2：对于国内用户，访问 ModelScope 的网络连通性更好
pip install modelscope
python -c \
  "from modelscope import snapshot_download; snapshot_download('AI-ModelScope/Mistral-7B-Instruct-v0.1')"
mv .cache/modelscope/hub/AI-ModelScope/Mistral-7B-Instruct-v0___1 ./Mistral-7B-Instruct-v0.1
```

2. 对 MLService 的 YAML 配置文件作以下修改，再次创建即可。修改后的 YAML 配置文件请参阅 <a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/examples/blob/master/deployments/vllm/mlservice-mistral.yaml">`mlservice-mistral.yaml`</a>。

```diff
$ diff --color -u mlservice.yaml mlservice-mistral.yaml
--- mlservice.yaml      2024-07-04 16:04:02
+++ mlservice-mistral.yaml      2024-07-04 16:03:38
@@ -1,7 +1,7 @@
 apiVersion: tensorstack.dev/v1beta1
 kind: MLService
 metadata:
-  name: codellama-7b
+  name: mistral-7b
 spec:
   # scheduler:
   #   t9kScheduler:
@@ -15,7 +15,7 @@
           runtime: vllm-openai
           parameters:
             MODEL_PATH: /var/lib/t9k/model
-            MODEL_NAME: codellama-7b
+            MODEL_NAME: mistral-7b
         containersResources:
         - name: user-container
           resources:
@@ -26,4 +26,4 @@
         storage:
           pvc:
             name: vllm
-            subPath: CodeLlama-7b-Instruct-hf
+            subPath: Mistral-7B-Instruct-v0.1
```

```bash
kubectl create -f mlservice-mistral.yaml
```

## 扩展：部署规模更大的 LLM

本示例以 7B 模型为例，我们还可以部署 13B、34B 和 70B 模型，但需要更多的计算资源。下表给出了相应的计算资源需求：

| 模型大小 | PVC 大小 | 并行度×显存大小          |
| -------- | -------- | ------------------------ |
| 7B       | 30GiB    | 1×24GB                   |
| 13B      | 55GiB    | 2×24GB / 1×40GB          |
| 34B      | 130GiB   | 4×24GB / 2×40GB / 1×80GB |
| 70B      | 260GiB   | 4×40GB / 2×80GB          |

<aside class="note tip">
<div class="title">提示</div>

如果没有足够的显存，可以尝试<a target="_blank" rel="noopener noreferrer" href="https://docs.vllm.ai/en/latest/quantization/auto_awq.html">量化</a>方法。

</aside>

例如要将部署的模型从 CodeLlama-7b-Instruct-hf 换成 CodeLlama-70b-Instruct-hf，只需：

1. 下载 CodeLlama-70b-Instruct-hf 的模型文件：

```bash
# 方法 1：如果可以直接访问 Hugging Face
huggingface-cli download codellama/CodeLlama-70b-Instruct-hf \
  --local-dir CodeLlama-70b-Instruct-hf --local-dir-use-symlinks False

# 方法 2：对于国内用户，访问 ModelScope 的网络连通性更好
# modelscope 没有 CodeLlama-70b-Instruct-hf 模型，用 CodeLlama-70b 模型替代
pip install modelscope
python -c \
  "from modelscope import snapshot_download; snapshot_download('AI-ModelScope/CodeLlama-70b')"
mv .cache/modelscope/hub/AI-ModelScope/CodeLlama-70b .
```

2. 对 MLServiceRuntime 和 MLService 的 YAML 配置文件作以下修改，再次创建即可。修改后的 YAML 配置文件请参阅 <a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/examples/blob/master/deployments/vllm/mlservice-runtime-70b.yaml">`mlservice-runtime-70b.yaml`</a> 和 <a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/examples/blob/master/deployments/vllm/mlservice-70b.yaml">`mlservice-70b.yaml`</a>。

```diff
$ diff --color -u mlservice-runtime.yaml mlservice-runtime-70b.yaml
--- mlservice-runtime.yaml
+++ mlservice-runtime-70b.yaml
@@ -1,7 +1,7 @@
 apiVersion: tensorstack.dev/v1beta1
 kind: MLServiceRuntime
 metadata:
-  name: vllm-openai
+  name: vllm-openai-2xtp
 spec:
   enabled: true
   template:
@@ -13,10 +13,18 @@
           - --model={{.MODEL_PATH}}
           - --served-model-name={{.MODEL_NAME}}
           - --trust-remote-code
+          - --tensor-parallel-size=2    # 2 度张量并行
         resources:
           limits:
             cpu: 4
             memory: 64Gi
-            nvidia.com/gpu: 1
+            nvidia.com/gpu: 2    # 对于 CodeLlama-70b 须为 A100 80GB
         ports:
         - containerPort: 8000
+        volumeMounts:
+          - mountPath: /dev/shm  # 并行需要
+            name: dshm
+      volumes:
+        - emptyDir:
+            medium: Memory
+          name: dshm

$ diff --color -u mlservice.yaml mlservice-70b.yaml
--- mlservice.yaml      2024-07-04 16:04:02
+++ mlservice-70b.yaml  2024-07-04 16:05:02
@@ -1,7 +1,7 @@
 apiVersion: tensorstack.dev/v1beta1
 kind: MLService
 metadata:
-  name: codellama-7b
+  name: codellama-70b
 spec:
   # scheduler:
   #   t9kScheduler:
@@ -12,18 +12,18 @@
       predictor:
         minReplicas: 1
         model:
-          runtime: vllm-openai
+          runtime: vllm-openai-2xtp
           parameters:
             MODEL_PATH: /var/lib/t9k/model
-            MODEL_NAME: codellama-7b
+            MODEL_NAME: codellama-70b
         containersResources:
         - name: user-container
           resources:
             limits:
               cpu: 4
               memory: 64Gi
-              nvidia.com/gpu: 1
+              nvidia.com/gpu: 2
         storage:
           pvc:
             name: vllm
-            subPath: CodeLlama-7b-Instruct-hf
+            subPath: CodeLlama-70b-Instruct-hf
```

```bash
kubectl apply -f mlservice-runtime-70b.yaml
kubectl create -f mlservice-70b.yaml
```

## 参考

* <a target="_blank" rel="noopener noreferrer" href="https://github.com/vllm-project/vllm">GitHub 上的 vLLM</a>
* <a target="_blank" rel="noopener noreferrer" href="https://github.com/facebookresearch/codellama">GitHub 上的 Code Llama 模型介绍</a>
* <a target="_blank" rel="noopener noreferrer" href="https://huggingface.co/codellama/CodeLlama-7b-Instruct-hf">HuggingFace 上的 CodeLlama-7b-Instruct-hf 模型</a>
