# 集成

平台支持集成第三方应用，用户可以在自己的项目中使用 Helm 轻松快速地部署各种丰富的第三方应用，例如部署一个 GitLab 以托管私有代码，部署一个 Label Studio 以进行数据标注等。

<aside class="note info">
<div class="title">Helm</div>

<a target="_blank" rel="noopener noreferrer" href="https://helm.sh/">Helm</a> 是 Kubernetes 的包管理工具，用于简化 Kubernetes 应用程序的部署和管理，其作用类似于 Linux 中的 apt 或 yum。Helm 通过将 Kubernetes 资源和配置封装为 Chart，提供了一种高效、一致的方式来部署和管理应用。

如要了解 Helm 的基本概念和使用方法，请参阅 Helm 的<a target="_blank" rel="noopener noreferrer" href="https://helm.sh/docs/">文档</a>。如要寻找可用的 Kubernetes 包（Helm Charts），请访问 <a target="_blank" rel="noopener noreferrer" href="https://artifacthub.io/packages/search">Artifact Hub</a>。

平台提供的 Notebook 标准镜像预装了 Helm，接下来的应用部署和管理操作都将在 Notebook 中进行。

</aside>

这一部分将介绍一些与机器学习相关的常用第三方应用的部署流程和使用方法。在开始之前，先确定在哪一个项目中部署应用，在该项目中创建一个名为 `app`、大小 1 GiB 的 PVC，然后创建一个同样名为 `app` 的 Notebook 挂载该 PVC（镜像类型和模板不限）。
