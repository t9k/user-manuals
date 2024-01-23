# Summary

[导言](./introduction.md)
[概述](./overview.md)
---

* [快速入门](get-started/index.md)
    * [训练你的第一个模型](get-started/training-first-model.md)<!-- * [在 notebook 完成训练] -->
    * [进行并行训练](get-started/parallel-training.md)<!-- * [使用 job 进行并行训练] -->
    * [部署模型](get-started/deploy-model.md)<!-- * [保存数据集和模型文件] -->

* [AI 开发和应用](modules/index.md)

    * [模型构建](modules/building/index.md)
        * [Notebook](modules/building/notebook.md)
        * [TensorBoard](modules/building/tensorboard.md)
        * [AutoTune](modules/building/autotune.md)
            * [AutoTuneExperiment](modules/building/autotuneexperiment.md)
            * [搜索空间](modules/building/autotune-search-space.md)
            * [超参数调优算法](modules/building/hpo-algorithm.md)

    * [模型部署](modules/deployment/index.md)
        * [SimpleMLService](modules/deployment/simplemlservice.md)
        * [MLService](modules/deployment/mlservice.md)

    * [作业](modules/jobs/index.md)
        * [GenericJob](modules/jobs/genericjob.md)
        * [PyTorchTrainingJob](modules/jobs/pytorchtrainingjob.md)
        * [TensorFlowTrainingJob](modules/jobs/tensorflowtrainingjob.md)
        * [DeepSpeedJob](modules/jobs/deepspeedjob.md)
        * [ColossalAIJob](modules/jobs/colossalaijob.md)
        * [XGBoostTrainingJob](modules/jobs/xgboosttrainingjob.md)
        * [MPIJob](modules/jobs/mpijob.md)
        * [BeamJob](modules/jobs/beamjob.md)

    * [工作流](modules/workflows/index.md)
        * [WorkflowTemplate](modules/workflows/workflowtemplate.md)
        * [WorkflowRun](modules/workflows/workflowrun.md)
        * [CronWorkflowRun](modules/workflows/cronworkflowrun.md)
        * [WorkflowTrigger](modules/workflows/workflowtrigger.md)

    * [资产管理](modules/asset-management.md)

    * [实验管理](modules/experiment-management.md)

* [账户和安全](modules/security/index.md)
    * [账户](modules/security/account.md)
    * [项目](modules/security/project.md)

* [计算资源](modules/scheduling/index.md)
    * [使用 GPU](modules/scheduling/use-gpu.md)
    * [资源配额](modules/scheduling/quota.md)
    * [队列](modules/scheduling/queue.md)
    * [PodGroup](modules/scheduling/podgroup.md)
    * [资源回收](modules/scheduling/reclaim.md)

* [存储](modules/storage/index.md)
    * [PVC](modules/storage/pvc.md)
    * [PVC 快照](modules/storage/pvc-snapshot.md)
    * [StorageShim](modules/storage/storageshim.md)
    * [Explorer](modules/storage/explorer.md)

* [辅助](modules/auxiliary/index.md)
    * [Secret](modules/auxiliary/secret.md)
    * [ConfigMap](modules/auxiliary/configmap.md)
    * [Pod](modules/auxiliary/pod.md)
    * [ImageBuilder](modules/auxiliary/imagebuilder.md)

* [任务](tasks/index.md)
    * [使用模型构建控制台](tasks/model-building.md)
        * [创建 Notebook](tasks/create-notebook.md)
        * [使用 Notebook](tasks/use-notebook.md)
        * [通过 SSH 远程使用 Notebook](tasks/ssh-notebook.md)
        * [创建 TensorBoard](tasks/create-tensorboard.md)
        * [构建镜像](tasks/build-image.md)
        * [调试镜像](tasks/debug-image.md)
        * [管理 PVC](tasks/manage-pvc.md)
        * [使用 Explorer](tasks/use-explorer.md)
        * [使用 StorageShim 适配 S3 服务](tasks/use-storageshim-s3.md)
        * [管理 Secret](tasks/manage-secret.md)
        * [管理 ConfigMap](tasks/manage-configmap.md)

    * [运行模型训练](tasks/model-training.md)
        * [使用 PyTorchTrainingJob 进行数据并行训练](tasks/pytorch-training-parallel.md)
        * [使用 PyTorchTrainingJob 进行参数服务器训练](tasks/pytorch-training-ps.md)
        * [使用 TensorFlowTrainingJob 进行数据并行训练](tasks/tensorflow-training-parallel.md)
        * [使用 TensorFlowTrainingJob 进行参数服务器训练](tasks/tensorflow-training-ps.md)
        * [使用 Horovod 进行 PyTorch 模型的数据并行训练](tasks/horovod-pytorch-parallel.md)
        * [使用 Horovod 进行 Keras 模型的数据并行训练](tasks/horovod-keras-parallel.md)
        * [使用 Profiler 分析模型训练性能](tasks/profile-model-training.md)

    * [进行超参数优化](tasks/hyperparameter-tuning.md)
        * [使用 AutoTune 进行超参数优化](tasks/autotune.md)

    * [部署推理服务](tasks/deploy-inference-service.md)
        * [简单推理服务](tasks/deploy-simplemlservice.md)
        * [生产环境推理服务](tasks/deploy-mlservice.md)
        * [包含 Transformer 的推理服务](tasks/deploy-mlservice-transformer.md)

    * [管理 AI 资产](tasks/manage-ai-assets.md)
        * [操作文件夹、模型和数据集](tasks/manipulate-folder-asset.md)
        * [通过 S3 访问模型和数据集](tasks/access-asset-via-s3.md)
        * [修改文件夹、模型和数据集的基本信息](tasks/modify-folder-asset.md)
        * [操作模型和数据集的分支、tag 和 commit](tasks/manipulate-asset-branch-tag.md)
        * [操作模型和数据集的对象](tasks/manipulate-asset-objects.md)

    * [追踪模型训练](tasks/track-model-training.md)
        * [在实验管理控制台查看和管理数据](tasks/use-experiment-console.md)
        * [使用 Python SDK 记录和上传数据](tasks/record-using-python-sdk.md)
        * [单设备训练场景](tasks/record-single-device-training.md)
        * [分布式训练场景](tasks/record-distributed-training.md)
        * [在实验管理控制台查看 AutoTune](tasks/view-autotune-in-experiment-console.md)

    * [构建自动化工作流](tasks/build-automation-workflow.md)
        * [创建工作流的基本单元](tasks/create-workflow-unit.md)
        * [创建执行各类任务的工作流单元](tasks/create-task-workflow-unit.md)
        * [创建存在依赖关系的工作流](tasks/create-dependent-workflow.md)
        * [建立从数据采样到模型导出的自动化工作流](tasks/build-automated-workflow.md)

    * [调度工作负载](tasks/schedule-workload.md)
        * [使用 Queue](tasks/use-queue.md)
        * [使用 PodGroup](tasks/use-podgroup.md)

    * [使用集群存储](tasks/use-platform-storage.md)
        * [上传和下载文件](tasks/pvc-importing-and-exporting-files.md)

    * [管理个人账户](tasks/manage-personal-account.md)
        * [生成 API Key](tasks/generate-api-key.md)
        * [使用 API Key](tasks/use-api-key.md)
        * [添加项目成员](tasks/add-project-member.md)

* [命令行工具和 SDK](tools/index.md)

    * [命令行工具：t9k](tools/cli-t9k/index.md)
        * [用户指南](tools/cli-t9k/guide.md)
        * [命令](tools/cli-t9k/commands.md)

    * [命令行工具：t9k-pf](tools/cli-t9k-pf/index.md)
        * [用户指南](tools/cli-t9k-pf/guide.md)
        * [命令](tools/cli-t9k-pf/commands.md)

    * [Python SDK：t9k](tools/python-sdk-t9k/index.md)
        * [用户指南](tools/python-sdk-t9k/guide.md)
        * [API](tools/python-sdk-t9k/api/index.md)
            * [t9k.ah](tools/python-sdk-t9k/api/t9k-ah.md)
            * [t9k.ah.core](tools/python-sdk-t9k/api/t9k-ah-core.md)
            * [t9k.config](tools/python-sdk-t9k/api/t9k-config.md)
            * [t9k.em](tools/python-sdk-t9k/api/t9k-em.md)
            * [t9k.tuner](tools/python-sdk-t9k/api/t9k-tuner.md)

    * [Codepack](tools/codepack/index.md)
        * [概念](tools/codepack/concepts.md)
        * [Codepack 定义](tools/codepack/definition.md)
        * [命令行工具](tools/codepack/cli.md)
        * [示例](tools/codepack/example.md)
---

* [参考](references/index.md)
    * [术语表](references/glossary.md)
    * [API 参考](references/api-reference/index.md)
        * [Project](references/api-reference/project.md)
        * [GenericJob](references/api-reference/genericjob.md)
        * [TensorFlowTrainingJob](references/api-reference/tensorflowtrainingjob.md)
        * [PyTorchTrainingJob](references/api-reference/pytorchtrainingjob.md)
        * [XGBoostTrainingJob](references/api-reference/xgboosttrainingjob.md)
        * [ColossalAIJob](references/api-reference/colossalaijob.md)
        * [DeepSpeedJob](references/api-reference/deepspeedjob.md)
        * [MPIJob](references/api-reference/mpijob.md)
        * [BeamJob](references/api-reference/beamjob.md)
        * [TensorBoard](references/api-reference/tensorboard.md)
        * [Notebook](references/api-reference/notebook.md)
        * [AutoTuneExperiment](references/api-reference/autotune.md)
        * [Explorer](references/api-reference/explorer.md)
        * [StorageShim](references/api-reference/storageshim.md)
        * [Scheduler](references/api-reference/scheduler.md)
        * [Workflow](references/api-reference/workflow.md)
        * [WorkflowTrigger](references/api-reference/workflowtrigger.md)
        * [SimpleMLService](references/api-reference/simplemlservice.md)
        * [MLService](references/api-reference/mlservice.md)
    * [标准镜像](references/standard-images.md)

---

 * [示例](examples/index.md)
    * [启动 LLM 大规模预训练](examples/start-llm-large-scale-pretraining.md)
    * [启动 LLM 微调](examples/start-llm-finetuning.md)
    * [部署 LLM 聊天机器人](examples/deploy-llm-chatbot.md)
    * [部署 Stable Diffusion 图像生成模型](examples/deploy-sd-drawing-model.md)
    * [使用 AutoGen 构建下一代 LLM 应用](examples/build-next-generation-llm-app-using-autogen.md)

* [第三方应用集成](integrations/index.md)
    * [Label Studio](integrations/label-studio.md)
---

[附录1：背景](./background.md)
