# 术语表

本术语表记录了 TensorStack AI 平台的一些专有名词，方便您随时查阅。

**API Key**

API Key 是一种 TensorStack AI 平台的安全认证方式，主要应用场景为非交互式程序化身份认证，例如自动化脚本等；或者受限制的交互式场景，例如命令行工具。详见 [API Key 文档](../module/index.md#api-key)。

**Assessor 算法**

Assessor 算法是一系列训练评估算法的统称，用于在 AutoTune 中判断当前超参数的训练中间结果是否符合预期。详见 [AutoTune 文档](../module/building/autotune/concepts/tuner.md#assessor-算法)。

**AutoTune**

AutoTune 是 TensorStack AI 平台提供的自动化机器学习工具，用于自动地进行特征工程、神经网络架构搜索、超参调优和模型压缩。详见 [AutoTune 文档](../module/building/autotune/index.md)。

**AutoTuneExperiment**

AutoTuneExperiment 是一种 TensorStack 资源，用于自动化机器学习超参数调优。详见 [AutoTuneExperiment 文档](../module/building/autotune/usage.md)。

**BeamJob**

BeamJob 是一种 TensorStack 资源，用于通过 Apache Beam 框架和 Apache Flink 等底层计算引擎运行分布式计算任务。详见 [BeamJob 文档](../module/workflow/job/beamjob.md)。

**ClusterRole**

与 Role 类似，但 Role 只能指定某个命名空间范围内的权限，ClusterRole 是整个集群范围。

**ClusterRoleBinding**

与 RoleBinding 类似，但 RoleBinding 只能指定某个命名空间范围内的权限，ClusterRoleBinding 是整个集群范围。

**ConfigMap**

ConfigMap 是一种以键值对的形式存储非机密信息的 Kubernetes 资源。Pod 可以挂载 ConfigMap，并以环境变量、命令行参数或配置文件的形式使用 ConfigMap 中的信息。您可以在 TensorStack AI 平台的模型构建控制台中创建 ConfigMap，详见[管理 ConfigMap](../guide/manage-auxiliary-resources/manage-cm.md)。

**容器（Container）**

容器是可移植、可执行的轻量级的镜像，包含其中的软件及其相关依赖。容器使应用和底层的主机基础设施解耦，降低了应用在不同云环境或者操作系统上的部署难度，便于应用扩展。

**控制器（Controller)**

控制器负责监控集群中某种 Kubernetes 资源的所有实例，并设法将资源的当前状态转变为期望状态。

**CRD（Custom Resource Definition，定制资源定义）**

CRD 是 Kubernetes 提供的一种扩展机制，允许开发者定制自己的资源，并开发对应的控制器。TensorStack AI 平台定义了一系列资源，以方便您在 Kubernetes 集群上构建机器学习应用。

**CronWorkflowRun**

CronWorkflowRun 是一种 TensorStack 资源，用于方便地定时执行 WorkflowRun。详见 [CronWorkflowRun 文档](../module/workflow/workflow/cronworkflowrun.md)。

**Docker**

Docker 是一个提供操作系统级别的虚拟化技术的软件，用于将软件应用及其相关依赖打包成所谓的容器（Container），能够在一个操作系统实例中运行多个其他操作系统中构建的容器。Kubernetes 支持使用 Docker 作为容器运行时。详见 [Docker 文档:octicons-link-external-16:](https://docs.docker.com/get-started/overview/){target=_blank}。

**Explorer**

Explorer 是一种 TensorStack 资源，用于通过浏览器访问文件管理器和集成开发环境（IDE）。详见 [Explorer 文档](../module/building/explorer.md)。

**GenericJob**

GenericJob 是一种 TensorStack 资源，用于统一协调多个 Pod 共同完成一项任务。详见 [GenericJob 文档](../module/workflow/job/genericjob.md)。

**镜像（Image）**

镜像是保存的容器实例，它打包了应用运行所需的一组软件。您可以将镜像存储在容器镜像仓库、拉取到本地系统并作为应用来运行。

**Job**

在 TensorStack AI 平台中，Job 是一类统一协调多个 Pod 共同完成一项任务的资源，包括 GenericJob、TensorFlowTrainingJob、PyTorchTrainingJob、XGBoostTrainingJob、MPIJob、BeamJob 等。

**Kubernetes（K8s）**

Kubernetes 是一个开源的容器编排引擎，用来对容器化应用进行自动化部署、 扩缩和管理。TensorStack AI 平台构建在 Kubernetes 的坚实基础之上。详见 [Kubernetes 文档:octicons-link-external-16:](https://kubernetes.io/zh/docs/home/){target=_blank}。

**标签（Label）**

标签是附属在资源上的键值对，用于标明资源的属性。您可以通过标签来选取一组资源的某个子集。

**MLService**

MLService 是一种 TensorStack 资源，用于部署机器学习模型预测服务，以供外部用户使用。详见 [MLService 文档](../module/deployment/concepts/mlservice.md)。

**MPIJob**

MPIJob 是一种 TensorStack 资源，用于通过 OpenMPI 协议进行分布式机器学习训练。详见 [MPIJob 文档](../module/workflow/job/mpijob.md)。

**命名空间（Namespace）**

命名空间是一组资源所属的工作空间，提供了一种划分集群、隔离资源的方式。同一命名空间内的资源名称必须不同，不同命名空间的资源名称可以相同。

**节点（Node）**

节点是 Kubernetes 中的工作机器。通常，Kubernetes 集群由一系列节点组成，少则一个，多则上千个。

**Notebook**

Notebook 是一种 TensorStack 资源，用于在集群中运行 Jupyter Notebook，同时提供 GPU 支持、SSH 访问支持等补充功能。详见 [Notebook 文档](../module/building/notebook.md)。

**Pod**

Pod 是可以在 Kubernetes 中创建和管理的、最小的可部署的计算单元。Pod 是一组（一个或多个）容器，这些容器共享存储、网络以及怎样运行这些容器的声明。详见 [Kubernetes 文档:octicons-link-external-16:](https://kubernetes.io/zh/docs/concepts/workloads/pods/){target=_blank}。

**PodGroup**

PodGroup 是一组 Pod 的集合，它们需要协同工作、一起被调度。详见 [PodGroup 文档](../module/cluster/scheduling/concept/podgroup.md)。

**Project**

Project 是 TensorStack AI 平台对计算集群的抽象，建立在 Kubernetes 命名空间 （namespace）之上。不同的用户通常在不同的 Project 下工作，并且可以互相分享自己 Project。详见 [Project 文档](../module/security/index.md#project)。

**PVC（PersistentVolumeClaim，持久卷申领）**

PVC 是一种持久化的存储资源，可以被 Pod 挂载、作为 Pod 的卷被访问。您可以在 TensorStack AI 平台的模型构建控制台中创建一个 PVC，并指定它的存储空间（例如 100M、1G）和访问模式（例如只读、可读写、可运行），详见[管理 PVC](../guide/manage-auxiliary-resources/manage-pvc.md)。

**PyTorchTrainingJob**

PyTorchTrainingJob 是一种 TensorStack 资源，用于通过 PyTorch 框架进行分布式机器学习训练。详见 [PyTorchTrainingJob 文档](../module/workflow/job/pytorchtrainingjob.md)。

**Queue**

Queue 是一种 TensorStack 资源，用于存放 PodGroup 并根据它们的优先级进行调度。详见 [Queue 文档](../module/cluster/scheduling/concept/queue.md)。

**RBAC（Role Based Access Control）**

RBAC 是一种管理访问控制的方式，详见 [Kubernetes 文档:octicons-link-external-16:](https://kubernetes.io/zh/docs/reference/access-authn-authz/rbac/){target=_blank}。您可以通过 ServiceAccount、Role、RoleBinding、ClusterRole、ClusterRoleBinding 等资源来管理访问控制。

**Role**

Role 中包含一组代表相关权限的规则，例如获取 Pod、创建 Pod、删除 Pod、获取 Secret、创建 Secret、删除 Secret 等。

**RoleBinding**

RoleBinding 将 Role 中定义的权限赋予一个用户或者一个 ServiceAccount，这样绑定 ServiceAccount 的 Pod 就能进行 Role 中定义的操作。

**调度器（Scheduler）**

调度器负责将 Pod 分配到合适的节点上，保证节点满足 Pod 声明的计算资源（CPU、内存、GPU等）、亲和度偏好（希望与其他 Pod 一起运行、希望运行在拥有某个标签的节点上等）等需求。

**Secret**

Secret 是一种存储密码、令牌、SSH Key 等敏感信息的 Kubernetes 资源。Pod 可以将 Secret 挂载为一个文件，并读取其中的信息。您可以在 TensorStack AI 平台的模型构建控制台中创建 Secret，详见[管理 Secret](../guide/manage-auxiliary-resources/manage-secret.md)。

**ServiceAccount**

ServiceAccount 为 Pod 提供一个身份凭证。当您创建一个 Pod 时，如果没有指定 ServiceAccount，该 Pod 会默认绑定一个名为 `default` 的 ServiceAccount。

**SimpleMLService**

SimpleMLService 是一种 TensorStack 资源，用于部署机器学习模型预测服务，以供内部开发者快速测试。详见 [SimpleMLService 文档](../module/deployment/concepts/simplemlservice.md)。

**TensorBoard**

TensorBoard 是 TensorFlow 提供的机器学习可视化工具。TensorStack AI 平台提供在集群中一键部署 TensorBoard 的功能，详见 [TensorBoard 文档](../module/building/tensorboard.md)。

**TensorFlowTrainingJob**

TensorFlowTrainingJob 是一种 TensorStack 资源，用于通过 TensorFlow 框架进行分布式机器学习训练。详见 [TensorFlowTrainingJob 文档](../module/workflow/job/tensorflowtrainingjob.md)。

**Tuner 算法**

Tuner 算法是一系列超参数调优算法的统称，用于在 AutoTune 中选取合适的超参数组合。详见 [AutoTune 文档](../module/building/autotune/concepts/tuner.md#tuner-算法)。

**卷（Volume）**

卷是一个包含数据的文件夹，可以被 Pod 中的容器访问。详见 [Kubernetes 文档:octicons-link-external-16:](https://kubernetes.io/zh/docs/concepts/storage/volumes/){target=_blank}。

**WorkflowRun**

WorkflowRun 是一种 TensorStack 资源，用于实例化 WorkflowTemplate 并提供 WorkflowTemplate 运行时所需的参数、工作空间等资源。详见 [WorkflowRun 文档](../module/workflow/workflow/workflowrun.md)。

**WorkflowTemplate**

WorkflowTemplate 是一种 TensorStack 资源，用于在 Kubernetes 中有序、高效、方便地组织运行各类工作负载。详见 [WorkflowTemplate 文档](../module/workflow/workflow/workflowtemplate.md)。

**XGBoostTrainingJob**

XGBoostTrainingJob 是一种 TensorStack 资源，用于通过 XGBoost 框架进行分布式机器学习训练。详见 [XGBoostTrainingJob 文档](../module/workflow/job/xgboosttrainingjob.md)。
