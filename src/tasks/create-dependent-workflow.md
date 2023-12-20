# 创建存在依赖关系的工作流

本教程演示如何创建存在依赖关系的工作流。

## 准备工作

* 完成教程[创建工作流的基本单元](./create-basic-unit-of-workflow.md)。
* 了解 [DAG WorkflowTemplate](../../module/workflow/workflow/workflowtemplate.md#dag-workflowtemplate) 的基本概念。
* 成为一个 [Project](../../module/security/index.md#project) 的所有者或者成员。

## 创建一些简单的 WorkflowTemplate

在浏览器中进入工作流控制台之后，点击左侧导航栏的 **WorkflowTemplate** 进入 WorkflowTemplate 列表页面，然后点击右上角的 **Project 选择框**选择一个 Project。

本教程使用[创建工作流的基本单元](./create-basic-unit-of-workflow.md#步骤1创建-workflowtemplate) 教程中创建好的 WorkflowTemplate “hello” 即可。如果有需要，您可以点击列表右上角的加号，按照[创建工作流的基本单元](./create-basic-unit-of-workflow.md#步骤1创建-workflowtemplate) 教程中的步骤，创建一些简单的 WorkflowTemplate。

## 创建 DAG WorkflowTemplate

点击左侧导航栏的 **WorkflowTemplate** 进入 WorkflowTemplate 列表页面，然后点击列表右上角的**树状图标**来创建一个 DAG WorkflowTemplate。

<figure class="screenshot">
  <img alt="workflowtemplate-list" src="../../assets/guide/build-automatic-workflow/create-workflow-including-dependencies/workflowtemplate-list.png" class="screenshot"/>
</figure>

进入创建 DAG WorkflowTemplate 页面之后，除了最左侧的导航栏之外整个页面分为三个部分，左边是 WorkflowTemplate 列表，中间是用于组建 DAG 的画布，右边是 DAG WorkflowTemplate 的详情。您可以从左边的 WorkflowTemplate 列表中用鼠标选取一个 WorkflowTemplate 拖拽到中间的画布上，然后通过绿色锚点连接多个 WorkflowTemplate，表示它们的执行顺序。画布中所有的 WorkflowTemplate 由依赖关系组成一个有向无环图（DAG）。

<figure class="screenshot">
  <img alt="create-workflowtemplate" src="../../assets/guide/build-automatic-workflow/create-workflow-including-dependencies/create-workflowtemplate.png" class="screenshot"/>
</figure>

建立好有向无环图之后，您可以在右边的表格编辑 DAG WorkflowTemplate 的详情，例如 WorkflowTemplate 的名称、工作空间、参数等。点击画布中的方块即可编辑该节点的详情，点击画布的空白处可以编辑整个 DAG WorkflowTemplate 的详情。

最后，点击表格上方的 **Create DAG WorkflowTemplate** 创建该 DAG WorkflowTemplate，右下角会有悬浮框提示是否创建成功。

## 创建 WorkflowRun

再次点击左侧导航栏的 **WorkflowTemplate** 进入 WorkflowTemplate 列表页面，找到您刚刚创建的 WorkflowTemplate “hello-again”，点击 WorkflowTemplate 的名称进入 WorkflowTemplate 的详情页面。

<figure class="screenshot">
  <img alt="workflowtemplate-detail" src="../../assets/guide/build-automatic-workflow/create-workflow-including-dependencies/workflowtemplate-detail.png" class="screenshot"/>
</figure>

在 WorkflowTemplate 的详情页面，点击右上角的 **Create WorkflowRun** 为该 WorkflowTemplate 创建一个 WorkflowRun。

<figure class="screenshot">
  <img alt="create-workflowrun" src="../../assets/guide/build-automatic-workflow/create-workflow-including-dependencies/create-workflowrun.png" class="screenshot"/>
</figure>

在弹出的创建 WorkflowRun 对话框中。按步骤依次填写 WorkflowRun 所需要的参数，最后点击 **Create** 创建 WorkflowRun，右下角会有悬浮框提示是否创建成功。

## 查看 WorkflowRun 运行情况

点击左侧导航栏的 **WorkflowRun** 进入 WorkflowRun 列表页面，找到您刚刚创建的 WorkflowRun “hello-again-run-9214x”，点击 WorkflowRun 的名称进入 WorkflowRun 的详情页面。

<figure class="screenshot">
  <img alt="workflowrun-detail" src="../../assets/guide/build-automatic-workflow/create-workflow-including-dependencies/workflowrun-detail.png" class="screenshot"/>
</figure>

在 WorkflowRun 的详情页面，您可以点击 **GRAPH** 标签，查看 DAG 的详细情况，点击 DAG 的节点可以在弹框中查看节点的详细情况。

<figure class="screenshot">
  <img alt="workflowrun-detail-node" src="../../assets/guide/build-automatic-workflow/create-workflow-including-dependencies/workflowrun-detail-node.png" class="screenshot"/>
</figure>
