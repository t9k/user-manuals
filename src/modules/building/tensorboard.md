# TensorBoard

TensorBoard 是 TensorFlow 提供的一种可视化机器学习过程和结果的工具，功能强大且广泛应用于多种框架。

<aside class="note info">
<div class="title">延伸阅读</div>

* <a target="_blank" rel="noopener noreferrer" href="https://www.tensorflow.org/tensorboard/get_started">TensorBoard 官方教程</a>  
* <a target="_blank" rel="noopener noreferrer" href="https://pytorch.org/docs/stable/tensorboard.html">使用 TensorBoard 可视化 PyTorch 模型</a>  
* <a target="_blank" rel="noopener noreferrer" href="https://keras.io/api/callbacks/tensorboard/">使用 TensorBoard 可视化 Keras 模型</a>

</aside>

你可以使用本产品在集群中一键部署 TensorBoard，可视化训练模型。

## 创建 TensorBoard

下面是一个基本的 TensorBoard 配置示例：

```yaml
# tensorboard-example.yaml
apiVersion: tensorstack.dev/v1beta1
kind: TensorBoard
metadata:
  name: pytorchtrainingjob-tensorboard
  namespace: t9k-example
spec:
  image: docker.mirrors.ustc.edu.cn/tensorflow/serving:2.6.0-gpu
  trainingLogFilesets:
  - t9k://pvc/pytorchtrainingjob-tensorboard-pvc/log
```

在该例中，TensorBoard 使用 `docker.mirrors.ustc.edu.cn/tensorflow/serving:2.6.0-gpu` 镜像，对名为 `pytorchtrainingjob-tensorboard-pvc` 的 PVC 中 `/log` 路径下的模型数据进行可视化。

### FileSet

FileSet 是一种特殊的资源定位符（URI），是一种用于定位多种存储技术中的资源的字符串。

FileSet 的格式为 `t9k://storage-type/storage-identity/path`，由下列四部分构成：

* 协议：`t9k://`。
* 存储器类型：当前 FileSet 支持 PVC（在 FileSet 中写作 `pvc`） 和 MinIO（在 FileSet 中写作 `minio`) 两种存储器。
* 存储器定位方式：FileSet 使用 PVC 的名称来定位 PVC 存储器，使用记录了 MinIO 地址、用户名和密码的 Secret 来定位 MinIO 存储器。
* 数据在存储器中的路径：模型在存储器中的准确位置。

下面是两个 FileSet 示例：

* `t9k://pvc/pytorchtrainingjob-tensorboard-pvc/log/model` 表示：所指向的资源被存储在名为 `pytorchtrainingjob-tensorboard-pvc` 的 PVC 中的 `log/model` 路径下。
* `t9k://minio/secret-name/bucket1/log/model` 表示：所指向的资源被存储在一个 MinIO 中名为 `bucket1` 的 Bucket 中的 `log/model` 路径下，该 MinIO 的地址、用户名和密码被存储在名为 `secret-name` 的 Secret 中。

<aside class="note info">
<div class="title">信息</div>

创建 MinIO Secret 的方法请参阅[管理 Secret](../../tasks/manage-secret.md)。

MinIO 的相关介绍（比如 Bucket 的含义）请参阅<a target="_blank" rel="noopener noreferrer" href="https://min.io/">官方介绍</a>。

</aside>

## TrainingJob 自动创建 TensorBoard

我们在 [TensorFlowTrainingJob](../jobs/tensorflowtrainingjob.md#tensorboard-的使用) 和 [PyTorchTrainingJob](../jobs/pytorchtrainingjob.md#tensorboard-的使用) 中集成了 TensorBoard 的创建，你可以在创建 TrainingJob 后直接进入 TensorBoard 监控训练进程和查看训练结果。

## 资源回收

TensorBoard 提供空闲资源回收的支持，在检测到 TensorBoard 处于空闲状态并超过一定时长时，删除工作负载以释放计算资源。默认情况下（管理员可修改配置）：

* TensorBoard 无人使用超过 1h 后，标记该 TensorBoard 为 `Idle`。
* TensorBoard 进入 `Idle` 状态超过 24h 后，删除该 TensorBoard 底层工作负载。

如果需要再次使用该 TensorBoard，你可以在模型构建控制台中手动点击**恢复**按钮。
