# 作业

作业（Job）是一类统一协调多个计算节点（replica）共同完成一项任务的 Kubernetes 资源。为了与 Kubernetes 原生的 [Job:octicons-link-external-16:](https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/job/){target=_blank} 资源作区分，后文称本平台的 Job 为 T9k Job。

根据所要完成的任务不同，T9k Job 分为以下几种资源：

* [GenericJob](./genericjob.md)

    GenericJob 是最基本的 T9k Job 资源，支持使用 T9k 高级调度策略。GenericJob 用法十分灵活，一个熟练的使用者可以使用 GenericJob 实现 MPIJob、PyTorchTrainingJob 等特定功能的 T9k Job。

* TrainingJob

    TrainingJob 是一类使用分布式计算框架进行机器学习的 T9k Job。

    * [PyTorchTrainingJob](./pytorchtrainingjob.md)

        PyTorchTrainingJob 是服务于 [PyTorch:octicons-link-external-16:](https://pytorch.org/){target=_blank} 分布式训练框架的 TrainingJob。

    * [TensorFlowTrainingJob](./tensorflowtrainingjob.md)

        TensorFlowTrainingJob 是服务于 [TensorFlow:octicons-link-external-16:](https://www.tensorflow.org/guide/distributed_training){target=_blank} 分布式训练框架的 TrainingJob。

    * [XGBoostTrainingJob](./xgboosttrainingjob.md)

        XGBoostTrainingJob 是服务于 [XGBoost:octicons-link-external-16:](https://xgboost.readthedocs.io/en/latest/){target=_blank} 分布式计算框架的 TrainingJob。  

    * [ColossalAIJob](./colossalaijob.md)

        ColossalAIJob 是服务于 [ColossalAI:octicons-link-external-16:](https://colossalai.org/){target=_blank} 分布式训练框架的 T9k Job。

    * [DeepSpeedJob](./deepspeedjob.md)

        DeepSpeedJob 是服务于 [DeepSpeed:octicons-link-external-16:](https://www.deepspeed.ai/){target=_blank} 分布式训练框架的 T9k Job。

* [MPIJob](./mpijob.md)

    [OpenMPI:octicons-link-external-16:](https://www.open-mpi.org/){target=_blank} 是一个开源的 MPI（Message Passing Interface）协议的实现项目。MPIJob 使您能够方便地在集群环境中使用 OpenMPI 进行训练。
