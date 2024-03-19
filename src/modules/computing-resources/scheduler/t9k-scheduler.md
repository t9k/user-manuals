# T9k Scheduler

T9k Scheduler 专为大规模分布式并行计算及异构资源集群设计，可以更加有效地管理 AI 集群的计算资源和计算任务。相比 [kube-scheduler](./kube-scheduler.md)，T9k Scheduler 在对 AI 计算场景的支持方面进行了增强，并增加了额外的机制以对集群进行更加精细化管理。（这一段介绍是否存在改进空间？）

这一部分将首先介绍 T9k Scheduler 引入的两个重要的管理计算资源的机制，同时也是 API 资源：队列（Queue）和 PodGroup。然后在它们的基础上说明 T9k Scheduler 的一些调度策略。
