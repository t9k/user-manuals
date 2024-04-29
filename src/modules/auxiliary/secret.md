# Secret

Secret 是一种 Kubernetes 原生资源，用于存储少量敏感信息，比如密码、OAuth 令牌、SSH 密钥等。使用 Secret 可以避免将敏感数据直接写入到 Pod 的定义中或者应用程序代码里，从而提高了安全性。

## 创建 Secret

下面是一个基本的 Secret 示例：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-demo
type: Opaque
data:
  key1: dmFsdWUxCg==
  key2: dmFsdWUyCg==
```

在该例中，`secret-demo` 存储了两对键值对，其中值经过了 base64 编码。

## 使用 Secret

与 [PVC](./pvc.md) 类似，Secret 可以以同样的方式作为数据卷被 Pod、Notebook、Job 等资源挂载。以 PyTorchTrainingJob 为例：

```yaml
apiVersion: batch.tensorstack.dev/v1beta1
kind: PyTorchTrainingJob
metadata:
  name: pytorchtrainingjob-demo
spec:
  replicaSpecs:
    - type: worker
      replicas: 1
      restartPolicy: OnFailure
      template:
        spec:
          containers:
            - image: pytorch/pytorch:2.0.0-cuda11.7-cudnn8-devel
              name: pytorch
              command:
                - python
                - dist_mnist.py
              resources:
                limits:
                  cpu: '1'
                  memory: 1Gi
                requests:
                  cpu: 500m
                  memory: 500Mi
              volumeMounts:
                - name: data
                  mountPath: /data
                - name: secret
                  mountPath: /secret
          volumes:
            - name: data
              persistentVolumeClaim:
                claimName: pvc-demo
            - name: secret
              secret:
                name: secret-demo
```

在该例中，`pytorchtrainingjob-demo` 将 `pvc-demo` 和 `secret-demo` 均作为数据卷（volume）来使用，其中容器 `pytorch` 将两个数据卷分别挂载到 `/data` 和 `/secret` 目录下。因此，容器 `pytorch` 的 `/secret` 目录下将存在两个文件 `/secret/key1` 和 `/secret/key2`，文件内容是经过 base64 解码后的对应的值。


## Secret 用途

TensorStack AI 平台通过 label `tensorstack.dev/resource` 来标识 Secret 的用途，主要有以下几种：

* API Key：拥有 label `tensorstack.dev/resource: apikey`，用于存放 API Key，可在安全管理控制台创建 API Key。
* S3-cfg：拥有 label `tensorstack.dev/resource: s3-cfg`，用于存放 S3 配置文件的内容，可从本地的 `$HOME/.s3cfg` 文件中获取。
* S3-env：拥有 label `tensorstack.dev/resource: s3-env`，用于存放 S3 配置文件的每个字段，请从本地的 `$HOME/.s3cfg` 文件中获取。
* Docker：拥有 label `tensorstack.dev/resource: docker`，用于存放 Docker 配置文件的内容，可从本地的 `$HOME/.docker/config.json` 文件中获取。
* SSH Public Key：拥有 label `tensorstack.dev/resource: ssh`，用于存放 SSH 公钥，可从本地的 `$HOME/.ssh/id_rsa.pub` 文件中获取。
* Ceph Client：拥有 label `tensorstack.dev/resource: ceph-client`，用于存放 Ceph 客户端配置，可从管理员处获取。
* Custom：拥有 label `tensorstack.dev/resource: other`，自定义用途。

例如：

* SSH Public Key 类型的 Secret 可用于 [Notebook SSH 访问](../building/notebook.md#ssh-访问)
* Docker 类型的 Secret 可用于 [ImageBuilder](./imagebuilder.md) 构建并上传镜像
* S3-cfg 类型的 Secret 可用于创建 [S3 类型的 StorageShim](./storageshim.md#s3-类型)
* Ceph Client 类型的 Secret 可用于创建 [CephFS 类型的 StorageShim](./storageshim.md#cephfs-类型)

## 下一步

* 了解 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/configuration/configmap/">Secret 的概念</a>
* 了解 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/kubernetes-api/config-and-storage-resources/secret-v1/">Secret 的定义</a>
