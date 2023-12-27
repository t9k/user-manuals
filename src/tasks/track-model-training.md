# 追踪模型训练

在复杂的 AI 实验中，研究人员或工程师需要处理数以百计的实验配置和结果，在缺乏有效管理工具的情况下很容易迷失在海量的数据和文件中。因此，追踪和记录实验变得十分重要，它能够帮助研究人员快速识别最佳模型，比较不同模型的差异，洞悉关键因素的作用，并且迅速迭代改进，从而大幅提升研究和开发的效率。

这一部分将使用[实验管理模块](../modules/experiment-management.md)和 [Python SDK](../tools/python-sdk-t9k/index.md) 追踪模型的训练过程和结果。Python SDK 负责自动记录超参数、指标、平台信息以及任何重要的输入输出文件，实验管理控制台则提供直观的可视化界面以及便捷的团队协作体验。我们将从介绍实验管理控制台与 Python SDK 的基本用法开始，进而到实际场景中追踪模型的训练，最后我们查看 AutoTune 进行超参数优化的结果。

* [在实验管理控制台查看和管理数据](./use-experiment-console.md)
* [使用 Python SDK 记录和上传数据](./record-using-python-sdk.md)
* [单设备训练场景](./record-single-device-training.md)
* [分布式训练场景](./record-distributed-training.md)
* [在实验管理控制台查看 AutoTune](./view-autotune-in-experiment-console.md)
