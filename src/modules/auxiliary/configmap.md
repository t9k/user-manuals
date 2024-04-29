# ConfigMap

ConfigMap 是一种 Kubernetes 原生资源，用于存储非机密性配置信息，它可以用来保存配置文件、命令行参数和环境变量等数据。ConfigMap使得容器化应用程序的配置与镜像内容分离，从而提高了应用的可移植性和灵活性。

## 创建 ConfigMap

下面是一个基本的 ConfigMap 示例：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: configmap-demo
data:
  key1: value1
  key2: value2
```

在该例中，`configmap-demo` 明文存储了两对键值对。


## 使用 ConfigMap

与 [PVC](./pvc.md) 类似，ConfigMap 可以以同样的方式作为数据卷被 Pod、Notebook、Job 等资源挂载。以 PyTorchTrainingJob 为例：

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
                - name: configuration
                  mountPath: /config
          volumes:
            - name: data
              persistentVolumeClaim:
                claimName: pvc-demo
            - name: configuration
              configMap:
                name: configmap-demo
```

在该例中，`pytorchtrainingjob-demo` 将 `pvc-demo` 和 `configmap-demo` 均作为数据卷（volume）来使用，其中容器 `pytorch` 将两个数据卷分别挂载到 `/data` 和 `/config` 目录下。因此，容器 `pytorch` 的 `/config` 目录下将存在两个文件 `/config/key1` 和 `/config/key2`，文件内容分别是 `value1` 和 `value2`。

## 下一步

* 了解 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/configuration/configmap/">ConfigMap 的概念</a>
* 了解 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/kubernetes-api/config-and-storage-resources/config-map-v1/">ConfigMap 的定义</a>
