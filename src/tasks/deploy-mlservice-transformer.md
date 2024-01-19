# 制作并部署含有 Transformer 的模型推理服务

本教程演示如何使用 TensorStack SDK 创建 Transformer 镜像，然后部署包含该 Transformer 的 MLService。

## 准备工作

请按照<a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/tutorial-examples/blob/master/docs/README-zh.md#%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95">使用方法</a>准备此次部署需要用到的 PVC。

请在本地的 Linux 或 macOS 平台上完成本教程，并确认安装了 <a target="_blank" rel="noopener noreferrer" href="https://www.docker.com/">docker</a>。

执行以下命令以安装 Python 依赖包：

```bash
pip install tensorflow==2.8.0 numpy
```

## 制作 Transformer 镜像

<aside class="note tip">
<div class="title">提示</div>

您可以跳过此步，直接使用我们制作好的镜像

</aside>

接下来制作供 MLService 使用的 Transformer 镜像。返回工作目录，创建并进入目录 `transformer`：

```bash
cd ..
mkdir transformer
cd transformer
```

使用 TensorStack SDK 编写 Transformer 的代码文件 `__main__.py` ，内容如下：

```py title="__main__.py"
import json
from t9k import mlservice

import argparse
import io
import numpy as np
from PIL import Image
from typing import Dict

# inherit parser to get command-line-args help
# feel free to add your command line args
par = argparse.ArgumentParser(parents=[mlservice.option.parser])
args, _ = par.parse_known_args()

def image_transform(instance):
    image = Image.open(io.BytesIO(instance))
    a = np.asarray(image)
    a = a / 255.0
    return a.reshape(28, 28, 1).tolist()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

def get_prediction(prediction: list)->str:
    max_value = max(prediction)
    max_index = prediction.index(max_value)
    return class_names[max_index]

class Transformer(mlservice.MLTransformer):
    def preProcess(self, path: str, requestData: bytes, headers: Dict[str, str]) -> any:
        return json.dumps({'instances': [image_transform(requestData)]})

    def postProcess(self, path: str, statusCode: int, responseContent: bytes, headers: Dict[str, str]) -> bytes:
        data = responseContent.decode('utf-8')
        jsonData = json.loads(data)
        jsonStr = json.dumps({'predictions': [get_prediction(predict) for predict in jsonData['predictions']]})
        return jsonStr.encode('utf-8')
    
if __name__ == "__main__":
    transformer = Transformer()
    server = mlservice.MLServer()
    server.start(transformer=transformer)
```

如文件 `__main__.py` 所示，使用 TensorStack SDK 编写 Transformer 只需要重载 `preprocess` 和 `postprocess` 函数即可：

* `preprocess`：预处理函数，Transformer 收到用户发送的数据，使用 `preprocess` 对数据进行处理，然后再发送给推理服务。在这个示例中，先转换输入图片的数据格式，需要保持与训练的模型的输入数据一致，然后再转换为推理服务的输入格式。
* `postprocess`：后处理函数，Transformer 收到推理服务返回的结果，使用 `postprocess` 对其进行处理，然后再返回给用户。在这个示例中，模型用于处理分类问题，从推理服务返回的预测概率向量中解析出该图片的分类类别，并返回给用户。

下载 <a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/tutorial-examples/tree/master/deployment/mlservice-v2/mlservice-transformer/t9k-sdk.tar.gz">t9k-sdk.tar.gz</a> 至本地 `transformer` 文件夹下。

然后编写 Transformer 镜像的 Dockerfile，内容如下：

```dockerfile title="Dockerfile.transformer"
FROM python:3.8-slim

COPY t9k-sdk.tar.gz t9k-sdk.tar.gz
COPY server.py server.py

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple \
    numpy \
    pillow \
    requests
RUN pip install t9k-sdk.tar.gz  -i https://pypi.tuna.tsinghua.edu.cn/simple

ENTRYPOINT ["python", "server.py"]
```

最后制作并上传 Transformer 镜像：

```bash
docker build -t <your-docker-registry-address>/mnist-transformer:test -f Dockerfile.transformer .
docker push <your-docker-registry-address>/mnist-transformer:test
```

## 部署 MLService

进入模型部署控制台，先点击左侧导航栏辅助一栏下的的 **MLServiceRuntime**，再点击 **创建 MLServiceRuntime** ，然后点击 **预览 YAML**， 并将下面 `tensorflow_serving.yaml` 的内容复制到 YAML 编辑框中，最后点击 **创建** 创建 MLServiceRuntime。

```yaml title=tensorflow_serving.yaml
apiVersion: tensorstack.dev/v1beta1
kind: MLServiceRuntime
metadata:
  name: t9k-tensorflow-serving
spec:
  enabled: true
  template:
    spec:
      containers:
      - name: user-container
        image: t9kpublic/tensorflow-serving:2.13.1
        command:
          - /usr/bin/tensorflow_model_server
        args:
          - --model_name={{if .MODEL_NAME}}{{.MODEL_NAME}}{{else}}model{{end}}
          - --port={{if .GRPC_PORT}}{{.GRPC_PORT}}{{else}}9000{{end}}
          - --rest_api_port=8000
          - --model_base_path=/var/lib/t9k/model
        resources:
          limits:
            cpu: "200m"
            memory: 200Mi
        ports:
        - containerPort: 8000
          protocol: TCP
```

进入模型部署控制台的 MLService 页面，点击右上角**创建 MLService**，然后点击**预览 YAML**。如下图所示，将 `image_transformer.yaml` 的内容复制到右侧的 YAML 编辑框，最后点击 **创建** 创建 MLService：

<aside class="note">
<div class="title">注意</div>

请将 transformer 定义中的 `image` 替换为刚制作好的镜像地址。

</aside>

```yaml title="image_transformer.yaml"
apiVersion: tensorstack.dev/v1beta1
kind: MLService
metadata:
  name: pic-mnist
spec:
  default: origin
  transformer:
    minReplicas: 1
    template:
      spec:
        containers:
        - name: user-container
          image: "<your-docker-registry-address>/mnist-transformer:test"
  releases:
    - name: origin
      predictor:
        minReplicas: 1
        model:
          runtime: t9k-tensorflow-serving
          modelUri: pvc://tutorial/tutorial-examples/deployment/mlservice-v2/mlservice-transformer/model/
```

<figure class="screenshot">
  <img alt="create-mlservcie-transformer" src="../../assets/tasks/deploy-model-reference-serving/transformer/create-mlservice.png" class="screenshot" />
</figure>


## 发送预测请求

使用图片 <a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/tutorial-examples/tree/master/deployment/mlservice-v2/mlservice-transformer/shoe.png">shoe.png</a> 作为发送预测请求的测试数据。

``` shell
address=$(kubectl get mls pic-mnist -ojsonpath='{.status.address.url}') && echo $address
curl --data-binary @./shoe.png ${address}/v1/models/model:predict
```
