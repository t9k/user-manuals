# 部署模型为推理服务

本教程将带领您使用[模型部署](../modules/deployment/index.md)模块的 [SimpleMLService](../modules/deployment/simplemlservice.md) 资源，将上一篇教程中保存的模型文件部署为推理服务。

## 部署推理服务

在 TensorStack AI 平台首页，点击**Deploy**进入模型部署控制台。

<figure class="screenshot">
  <img alt="landing-page" src="../assets/get-started/deployment/landing-page.png" class="screenshot"/>
</figure>

模型部署控制台的总览页面展示了当前部署服务的数量以及资源使用情况。在左侧的导航菜单中点击**部署&nbsp;> SimpleMLService**，点击右上角的 **+** 弹出创建对话框，然后复制下面的 YAML 配置文件并粘贴到编辑框中，最后点击**创建**。

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: SimpleMLService
metadata:
  name: mnist
spec:
  replicas: 1
  storage:
    pvc:
      containerPath: /var/lib/t9k/models/mnist
      name: mnist
      subPath: .
  tensorflow:
    image: t9kpublic/tensorflow-serving:2.6.0
```

<figure class="screenshot">
  <img alt="create-simplemlservice" src="../assets/get-started/deployment/create-simplemlservice.png" class="screenshot"/>
</figure>

<aside class="note info">
<div class="title">SimpleMLService</div>

[SimpleMLService](../modules/deployment/simplemlservice.md) 是平台提供的用于部署模型推理服务的资源。与同样用于部署推理服务的 [MLService](../modules/deployment/mlservice.md) 相比，SimpleMLService 更加精简，适用于快速测试。

</aside>

在跳转回到 SimpleMLService 管理页面之后，等待刚才创建的 SimpleMLService 准备就绪。第一次拉取镜像可能会花费较长的时间，具体取决于您的网络状况。点击右上角的**刷新按钮**以手动刷新 SimpleMLService 状态。

## 使用推理服务

### 查看推理服务地址

待 SimpleMLService 就绪之后，点击其**名称**进入详情页面。

<figure class="screenshot">
  <img alt="enter-simplemlservice" src="../assets/get-started/deployment/enter-simplemlservice.png" class="screenshot"/>
</figure>

页面中展示的 DNS 即为推理服务地址，注意该地址只能从集群内部访问。

<figure class="screenshot">
  <img alt="simplemlservice-detail" src="../assets/get-started/deployment/simplemlservice-detail.png" class="screenshot"/>
</figure>

### 生成测试数据

再次连接到 Notebook mnist，在终端中执行以下命令以将保存模型文件的目录重命名为 `1`。

```bash
mv saved_model/ 1/
```

然后新建一个 `.ipynb` 文件或 Python 脚本文件以运行下面的脚本。该脚本将 MNIST 数据集的测试集中的前三个样本的数据和标签保存为 TensorFlow Serving 服务器的 REST API 所接受的 JSON 文件格式。

```python title="generate_testing_data.py"
import json
from tensorflow.keras import datasets

(_, _), (test_images, test_labels) = datasets.mnist.load_data()
test_images = test_images.reshape((10000, 28, 28, 1))
test_images = test_images / 255.0

data = {
    "signature_name": "serving_default",
    "instances": test_images[0:3].tolist()
}
target = {"labels": test_labels[0:3].tolist()}
with open('data.json', 'w') as f:
    json.dump(data, f)
with open('target.json', 'w') as f:
    json.dump(target, f)
```

### 访问推理服务

在终端中执行以下命令以向推理服务发送请求，其中 `URL` 变量的值需要修改为您实际部署的推理服务的地址。

```shell
export URL="http://mnist.demo.svc.cluster.local/v1/models/mnist:predict"
curl -d @data.json $URL
cat target.json
```

输出类似于：

```shell
{
    "predictions": [[4.62218732e-16, 4.05237122e-10, 6.88771651e-10, 2.76936946e-11, 1.08857443e-12, 1.35836481e-12, 2.55610125e-17, 1.0, 1.78349887e-11, 2.73386147e-10], [0.000252794096, 5.05418676e-08, 0.999745309, 1.99162272e-07, 2.04035135e-08, 1.28374993e-11, 3.58009686e-07, 1.3919628e-10, 1.28257238e-06, 8.09815132e-11], [2.01749484e-09, 0.999998808, 1.47222934e-09, 2.86072266e-14, 3.45859632e-07, 2.4689697e-09, 1.66409855e-08, 1.32032545e-08, 8.31589603e-07, 5.41381411e-08]
    ]
}
{"labels": [7, 2, 1]}
```

响应体的预测数组中最大值的索引分别为 7、2、1（从 0 开始计数），与这三个样本的标签一致。

或者，您也可以运行下面的 Python 脚本以向推理服务发送请求并验证推理结果，其中 `url` 的值同样需要修改为您的推理服务地址。

```python
import json
import requests
import numpy as np

with open('data.json', 'rt') as f:
    data = f.read()
with open('target.json', 'rt') as f:
    target = json.loads(f.read())['labels']

# Modify this value to your URL of inference service
url = 'http://mnist.demo.svc.cluster.local/v1/models/mnist:predict'
headers = {'content-type': 'application/json'}
resp = requests.post(url, data=data, headers=headers)
pred = json.loads(resp.text)['predictions']
pred = np.argmax(pred, axis=1).tolist()

print('Inference:')
print(pred)
print('Target:')
print(target)

```

```shell
python validate_inference.py 
```

输出为：

```shell
Inference:
[7, 2, 1]
Target:
[7, 2, 1]
```

## 下一步

* 了解模块[模型部署](../modules/deployment/index.md)
* 进一步学习如何[部署用于测试环境的模型推理服务](../tasks/deploy-simplemlservice.md)
* 进一步学习如何[部署用于生产环境的模型推理服务](../tasks/deploy-mlservice.md)
