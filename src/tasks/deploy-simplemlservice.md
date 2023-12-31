# 简单模型推理服务

本教程演示使用 SimpleMLService 部署用于测试环境的模型推理服务。

## 运行示例

请按照<a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/tutorial-examples/blob/master/docs/README-zh.md#%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95">使用方法</a>准备环境，然后前往<a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/tutorial-examples/blob/master/deployment/simplemlservice">本教程的示例</a>，参照其 README 文档运行。本示例使用 PVC 中存储的模型创建了一个 SimpleMLService 服务。

<aside class="note tip">
<div class="title">提示</div>

除了上述直接提供 YAML 配置文件的方法外，您也可以选择从网页控制台创建 SimpleMLService。

</aside>


## 查看推理服务状态

部署完成后，进入模型部署控制台的 SimpleMLService 页面，可以看到名为 **mnist** 的 SimpleMLService。

列表页面：

<figure class="screenshot">
    <img alt="list" src="../assets/tasks/deploy-simplemlservice/list.png" class="screenshot"/>
</figure>

SimpleMLService **mnist** 的详情页面：

<figure class="screenshot">
    <img alt="detail" src="../assets/tasks/deploy-simplemlservice/details.png" class="screenshot"/>
</figure>