# AI 开发和应用

TensorStack AI 平台提供了一套完整、全面的工具和服务，对 AI 模型的构建、训练和部署提供全流程的支持，从而助力研究人员轻松、高效地实现 AI 项目，加速 AI 模型的研究、开发和应用。

<aside class="note tip">
<div class="title">提示</div>

用户并不总是需要使用所有的功能模块。例如，用户可以直接使用集群的 “[共享文件系统卷](./storage/index.md#共享文件系统卷shared-filesystem-volumes)” 来保存训练数据、模型本身等，而不需要使用 “[资产管理](./asset-management.md)” 模块。

</aside>

下图展示了在平台上开发一个深度学习模型的完整流程，以及各个模块发挥的功能：

<figure>
  <img alt="ai-development" src="../assets/modules/ai-development.drawio.svg" />
</figure>

## 下一步

* 学习并使用：[模型构建](./building/index.md)
* 部署模型为推理服务：[模型部署](./deployment/index.md)
* 在集群中运行大规模计算：[Job](./jobs/index.md)、[工作流](./workflows/index.md)
* 系统化 AI 计算的过程：[存储 AI 资产](./asset-management.md)、[追踪 AI 实验](./experiment-management.md)
