# 作业

作业（Job）是一类统一协调多个计算节点（replica）共同完成一项任务的 Kubernetes 资源。为了与 Kubernetes 原生的 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/job/">Job</a> 资源作区分，后文称本平台的 Job 为 T9k Job。

## 作业类型

根据所要完成的任务不同，本平台提供以下 8 种作业：

* [GenericJob](./genericjob.md)：最基本的 T9k Job 资源，支持使用 T9k 高级调度策略。GenericJob 用法十分灵活，一个熟练的使用者可以使用 GenericJob 实现 MPIJob、PyTorchTrainingJob 等特定功能的 T9k Job。
* TrainingJob：一类使用分布式计算框架进行机器学习的 T9k Job。
    * [PyTorchTrainingJob](./pytorchtrainingjob.md)：服务于 <a target="_blank" rel="noopener noreferrer" href="https://pytorch.org/">PyTorch</a> 分布式训练框架的 TrainingJob。
    * [TensorFlowTrainingJob](./tensorflowtrainingjob.md)：服务于 <a target="_blank" rel="noopener noreferrer" href="https://www.tensorflow.org/guide/distributed_training">TensorFlow</a> 分布式训练框架的 TrainingJob。
    * [XGBoostTrainingJob](./xgboosttrainingjob.md)：服务于 <a target="_blank" rel="noopener noreferrer" href="https://xgboost.readthedocs.io/en/latest/">XGBoost</a> 分布式计算框架的 TrainingJob。  
    * [ColossalAIJob](./colossalaijob.md)：服务于 <a target="_blank" rel="noopener noreferrer" href="https://colossalai.org/">ColossalAI</a> 分布式训练框架的 T9k Job。
    * [DeepSpeedJob](./deepspeedjob.md)：服务于 <a target="_blank" rel="noopener noreferrer" href="https://www.deepspeed.ai/">DeepSpeed</a> 分布式训练框架的 T9k Job。
* [MPIJob](./mpijob.md)：<a target="_blank" rel="noopener noreferrer" href="https://www.open-mpi.org/">OpenMPI</a> 是一个开源的 MPI（Message Passing Interface）协议的实现项目。MPIJob 使您能够方便地在集群环境中使用 OpenMPI 进行训练。
* [BeamJob](./beamjob.md)：用于在集群中通过 <a target="_blank" rel="noopener noreferrer" href="https://beam.apache.org/documentation/sdks/python/">Apache Beam Python SDK</a> 运行分布式计算任务，并提供多种底层计算引擎。

## 作业模式

我们为 T9k Job 设计以下模式：

* 立即（Immediate）模式：默认、基本模式。立即按照 YAML 配置开始运行。
* 调试（Debug）模式：帮助用户创建任务环境，但不直接执行任务，用户可以在训练环境中手动执行任务和调试代码。
* 暂停（Pause）模式：在一些场合下（如集群资源不足），用户可随时暂停任务，待条件允许再继续执行任务。
* 弹性（Elastic）伸缩模式：可以动态调整作业规模。

以下是各类型作业支持的模式列表：

|        作业类型        | 立即模式 | 调试模式 | 暂停模式 | 弹性伸缩模式 |  
| --------------------- | ------ | ------- | ------ | ----------- |  
| GenricJob             | *      | *       | *      |             | 
| PyTorchTrainingJob    | *      | *       | *      | *           | 
| TensorFlowTrainingJob | *      | *       | *      |             |
| XGBoostTrainingJob    | *      | *       | *      |             |
| MPIJob                | *      | *       | *      |             |
| ColossalAIJob         | *      | *       | *      |             |
| DeepSpeedJob          | *      | *       | *      | *           |
| BeamJob               | *      |         |        |             |

各种模式的具体使用方式，请参考对应作业类型的文档。
