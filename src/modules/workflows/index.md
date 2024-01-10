# 工作流

AI 应用由很多基础计算步骤构成，具有很大灵活性，在不同场景需要做各种定制计算处理。例如，一个模型训练过程可能包含数据取样、数据转换、模型训练、模型质检、模型导出等步骤。

为此 TensorStack AI 平台提供了一个灵活的工作流服务，将这些计算步骤组合在一起，集中进行管理和调度，自动化复杂的流程。

## 架构

工作流模块提供了 [WorkflowTemplate](./workflowtemplate.md)、[WorkflowRun](./workflowrun.md)、[CronWorkflowRun](./cronworkflowrun.md) 等自定义扩展资源，以及控制台、服务器、操作器等组件。整体架构如下图所示：

<figure> 
<img alt="architecture" src="../../assets/modules/workflow/architecture.drawio.svg"/>
</figure>

其中：

* 控制台（Console）提供前端界面，方便用户对 WorkflowTemplate、WorkflowRun 等资源进行创建、查看、删除等操作。
  * 用户也可以直接使用命令行工具 `kubectl` 创建 workflow 的资源。
* 服务器（Server）向工作流控制台提供 API 接口，帮助获取 WorkflowTemplate、WorkflowRun 等资源的详细信息。
* 控制器（Controller），负责监控集群中的 WorkflowTemplate、WorkflowRun 等资源，并执行一些与资源相关的操作，使资源当前的状态与其理想状态一致。

## 与其他模块的关系

如下图所示，Workflow 可以将分布式并行作业、非并行作业组合在一起成为复合作业，而且复合作业中可以嵌套复合作业，并通过 T9k 调度器进行计算资源的匹配，最终完成复杂的多步骤计算。

<figure> 
<img alt="workflow-and-jobs" src="../../assets/modules/workflow/workflow-and-jobs.drawio.svg"/>
</figure>
