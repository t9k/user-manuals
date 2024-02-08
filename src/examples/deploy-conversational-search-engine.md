# 部署对话式搜索引擎

对话式搜索引擎（conversational search engine）是利用自然语言处理技术来理解和响应用户查询的下一代搜索引擎。与传统的基于关键字的搜索引擎不同，对话式搜索引擎能够与用户以自然语言对话的形式进行互动，从而提供更为精准和个性化的搜索结果。这种搜索引擎通过分析用户的查询意图和上下文信息，能够提出问题、澄清疑惑，并给出更加直观和详细的回答。

当下最火热的对话式搜索引擎产品无疑是 Perplexity，但最近广受好评的开源项目 <a target="_blank" rel="noopener noreferrer" href="https://github.com/leptonai/search_with_lepton">Search with Lepton</a> 仅用 500 行 Python 代码就实现了类似的功能。阅读这 500 行代码，其核心逻辑为：

1. 获取用户的查询文本，调用传统搜索引擎的 API 以获取上下文，即结果页面的片段（snippet）。
1. 将上下文添加到 system prompt（用于编写回答）中，将查询文本作为 user prompt，调用 LLM 生成回答。
1. 将同样的上下文添加到另一个 system prompt（用于产生关联问题）中，将查询文本作为 user prompt，调用 LLM 生成关联问题。
1. 将上下文、回答和关联问题返回给 UI 以供展示。
1. （可选）将当次查询结果存储到数据库中，若用户再次进行相同的查询则直接返回该结果。

本示例使用 MLService 部署 Search with Lepton 对话式搜索引擎应用。

## 准备

请先参阅[使用 vLLM 部署 LLM 推理服务](./deploy-llm-using-vllm.md)部署一个推理服务。

</aside>

<aside class="note tip">
<div class="title">提示</div>

通过调用更强大的 LLM，对话式搜索引擎应用可以生成更高质量的回答。

</aside>

在项目中创建一个名为 `search`、大小 1 GiB 以上的 PVC，然后创建一个同样名为 `search` 的 Notebook 挂载该 PVC（镜像类型和模板不限）。

进入 Notebook 或远程连接到 Notebook，启动一个终端，执行以下命令以克隆 <a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/examples">`t9k/examples` 仓库</a>：

```bash
cd ~
git clone https://github.com/t9k/examples.git
```

## 部署

<a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/search_with_lepton">`t9k/search_with_lepton`</a> fork 了 Search with Lepton 项目并进行了以下修改：

* 移除使用 Lepton AI 云服务的代码。
* 增加 Dockerfile 并构建应用镜像 `t9kpublic/search-with-lepton`。

接下来使用上述镜像部署该应用。使用以下 YAML 配置文件创建 MLServiceRuntime：

<details><summary><code class="hljs">examples/deploy-conversational-search-engine/mlservice-runtime.yaml</code></summary>

```yaml
{{#include ../assets/examples/deploy-conversational-search-engine/mlservice-runtime.yaml}}
```

</details>

```bash
kubectl apply -f examples/applications/search-with-lepton/mlservice-runtime.yaml
```

在以下 YAML 配置文件中提供环境变量，再使用它创建 MLService 以部署应用：

<details><summary><code class="hljs">examples/deploy-conversational-search-engine/mlservice.yaml</code></summary>

```yaml
{{#include ../assets/examples/deploy-conversational-search-engine/mlservice.yaml}}
```

</details>

```bash
vim examples/applications/search-with-lepton/mlservice.yaml
kubectl create -f examples/applications/search-with-lepton/mlservice.yaml
```

<aside class="note tip">
<div class="title">提示</div>

请参阅 <a target="_blank" rel="noopener noreferrer" href="https://github.com/leptonai/search_with_lepton/tree/main?tab=readme-ov-file#setup-search-engine-api">Setup Search Engine API</a> 以获取相应搜索引擎后端的 API key 或 subscription key。

</aside>

## 搜索

在本地的终端中，使用 [t9k-pf 命令行工具](../tools/cli-t9k-pf/index.md)，将 MLService 创建的以下服务的 80 端口转发到本地的 8080 端口：

```bash
t9k-pf service search-with-lepton-vllm-predict-version1-00001-private 8080:80 -n <PROJECT NAME>
```

然后使用浏览器访问 `127.0.0.1:8080`，搜索以下问题：

1. when will nvidia RTX 5000 series be released?
1. 二进制小品是什么
1. 武汉火车站是否已经恢复正常运行

需要说明的是，这里 Search with Lepton 所使用的搜索引擎后端是 Bing，调用的 LLM 是 <a target="_blank" rel="noopener noreferrer" href="https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1">Mixtral-8x7B-Instruct-v0.1</a>。以下搜索于 2024 年 2 月 8 日进行。

<figure class="screenshot">
  <img alt="search-with-lepton-q1" src="../assets/examples/deploy-conversational-search-engine/search-with-lepton-q1.png" />
</figure>

<figure class="screenshot">
  <img alt="search-with-lepton-q2" src="../assets/examples/deploy-conversational-search-engine/search-with-lepton-q2.png" />
</figure>

<figure class="screenshot">
  <img alt="search-with-lepton-q3" src="../assets/examples/deploy-conversational-search-engine/search-with-lepton-q3.png" />
</figure>

作为比较，我们在 Perplexity 搜索相同的问题：

<figure class="screenshot">
  <img alt="perplexity-q1" src="../assets/examples/deploy-conversational-search-engine/perplexity-q1.png" />
</figure>

<figure class="screenshot">
  <img alt="perplexity-q2" src="../assets/examples/deploy-conversational-search-engine/perplexity-q2.png" />
</figure>

<figure class="screenshot">
  <img alt="perplexity-q3" src="../assets/examples/deploy-conversational-search-engine/perplexity-q3.png" />
</figure>

可以看到，Search with Lepton 的回答基本准确且详细，但存在以下问题：

1. 尽管该应用可以理解中文查询和上下文，但它仅以英文回复，这是因为其调用的 Mixtral 8x7B 模型<a target="_blank" rel="noopener noreferrer" href="https://mistral.ai/news/mixtral-of-experts">仅支持英语和一些欧洲语言</a>。用户可以自行尝试调用其他支持中文的 LLM。

1. 在回答问题 2 时，应用给出的解释“It is a form of light and humorous artistic work that explores the characteristics, applications, nad computer-related topics of binary.（它是一种轻松幽默的艺术作品形式，探索了二进制的特征、应用和与计算机相关的话题。）”存在明显误解，追溯其引用的<a target="_blank" rel="noopener noreferrer" href="https://zhidao.baidu.com/question/274974338041104445.html">参考源</a>，我们发现该来源的解释就存在错误，且很有可能是由另一个 LLM 产生的虚构的信息。这提示我们在对话式搜索引擎中，搜索的准确性比内容生成更为关键，凸显了优化获取和处理上下文信息步骤的重要性。

相比之下，Perplexity 支持中文，并且生成回答的速度更快。尽管如此，其回答的质量并没有更好，尤其是对于问题 2 的回答出现了问题，完全没有引用参考源，而是由 LLM 直接生成的。其对于问题 3 的回答所包含的有用信息也较少。
