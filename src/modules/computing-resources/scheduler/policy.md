# 调度策略

T9k Scheduler 的一些调度策略介绍如下。

## 优先级和抢占

当集群资源不足，无法为所有 Pod 分配资源时，T9k Scheduler 会尝试为未被分配资源的 Pod（Pod A）抢占资源。Pod A 只能抢占所属队列的优先级比自己低的 Pod 的资源。资源抢占成功后，被抢占资源的 Pod 会被删除，Pod A 会被分配资源。

尽管被抢占资源的 Pod 会被直接删除，但是 Pod 所属的父资源（例如 Deployment、[T9k Job](../../../workflow/job/index.md) 等）不会被删除，此时父资源会重新创建 Pod 来申请集群资源，从而可能触发新一轮的抢占行为。以此类推，一次抢占行为可能会触发一系列的抢占行为。因此需要通过设置队列的某些属性，来控制集群对队列的资源抢占行为，例如关闭生产级别队列的抢占开关。

假设集群总资源为 `{cpu: 300}`，集群中有 4 个队列，当前状态如下：

| 队列名称 | 资源配额     | 优先级 | Pod                                            |
| -------- | ------------ | ------ | ---------------------------------------------- |
| A        | `{cpu: 200}` | 1      | A1 `{cpu: 50}`，A2 `{cpu: 50}`，A3 `{cpu: 50}` |
| B        | `{cpu: 100}` | 1      | B1 `{cpu: 50}`                                 |
| C        | `{cpu: 50}`  | 2      | C1 `{cpu: 50}`                                 |
| D        | `{cpu: 200}` | 2      | D1 `{cpu: 50}`                                 |

设想用户接下来进行的操作，并给出相应的结果和原因：

| 用户操作                                 | 结果 | 原因                                                                                 |
| ---------------------------------------- | ---- | ------------------------------------------------------------------------------------ |
| 在队列 B 中创建 <br/> Pod B2 `{cpu: 50}` | 阻塞 | 集群资源已全部分配且队列 B 优先级低，无法抢占其他队列的资源。                        |
| 在队列 C 中创建 <br/> Pod C2 `{cpu: 50}` | 阻塞 | 超过队列 C 的资源配额。                                                              |
| 在队列 D 中创建 <br/> Pod D2 `{cpu: 50}` | 成功 | 发生资源抢占行为，抢占队列 A 的资源：删除 Pod A3（优先级低于 A1、A2），创建 Pod D2。 |

## 公平排序

当两个队列的优先级相同时，T9k Scheduler 会根据队列的**主导资源占比**来确定资源分配顺序，主导资源占比较低的队列将优先获得资源分配。这里的主导资源占比指的是队列中资源占比最高的资源类型所占的比例。

假设队列 A 和 B 的优先级相同，资源配额及使用情况如下图所示：

![fair-ranking](../../../assets/modules/computing-resources/share.drawio.svg)

| 队列名称 | 资源占比                  | 主导资源占比 |
| -------- | ------------------------- | ------------ |
| A        | `{cpu: 3/6, Memory: 5/8}` | 5/8          |
| B        | `{cpu: 3/8, Memory: 1/2}` | 1/2          |

根据前述公平排序原则，T9k Scheduler 会优先为队列 B 分配资源。