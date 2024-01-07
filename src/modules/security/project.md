# 项目

Project（项目）是 TensorStack AI 平台为了有效使用集群资源，实现多用户、多项目同时、安全、共享使用集群而提供的机制；它是一个 CRD。

它具有以下特征：

* 每个项目有一个**项目管理员**，他可以管理项目的**成员**。
* 只有项目的管理员和成员可以在项目中执行操作。
* 每个项目对应一个同名的 Kubernetes 命名空间（Namespace），项目的成员拥有当前命名空间中几乎所有 K8s 资源的操作权限。

<aside class="note info">
<div class="title"> 集群管理员和项目管理员的区别 </div>

**集群管理员**拥有 TensorStack AI 平台的管理权限，包括但不限于创建、修改和删除用户、用户组、项目和队列。集群管理员也具有所有项目的项目管理员和成员的设置权限。

**项目管理员**具有一个项目的成员管理权限。每一个项目只能设置一个项目管理员，由集群管理员在创建项目时设置或在创建后修改。

需要说明的是：集群管理员虽然有集群管理的权限，但是在项目的使用上，集群管理员同样要遵循项目授权的规则，即如果集群管理员不是项目的成员，则集群管理员不能使用这个项目。当然，集群管理员可以通过将自己设置为项目成员的方式来使用项目。

本节所有“普通用户”指的都是除“集群管理员”之外的用户，也包括项目管理员。

</aside>

## 项目定义

以下是一个项目的定义（Custom Resource）示例：

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: Project
metadata:
spec:
  networkPolicy:
    template:
      spec:
        egress:
          - to:
              - namespaceSelector:
                  matchLabels:
                    kubernetes.io/metadata.name: t9k-system
                podSelector:
                  matchLabels:
                    app: security-console-server
        ingress:
          - from:
              - namespaceSelector:
                  matchLabels:
                    kubernetes.io/metadata.name: t9k-system
        policyTypes:
          - Ingress
          - Egress
    useDefaultTemplate: false
  quotaProfile: demo
  resourceQuota:
    template:
      spec:
        hard:
          cpu: '200'
          memory: 1280Gi
          nvidia.com/gpu: '18'
          persistentvolumeclaims: 200Gi
          pods: 1k
```

注：普通用户（包括项目管理员）不可修改上述项目配置，这里仅用该配置进行演示和讲解。

在上述示例中：

* 该项目中设置以下网络策略：
  * 该项目中的工作负载可以访问 `t9k-system` 命名空间中的 `security-console-server` 服务（由字段 `spec.networkPolicy.template.spec.egress` 字段指定）。
  * 该项目中的服务可以被 `t9k-system` 命名空间的任一工作负载访问（由字段 `spec.networkPolicy.template.spec.ingress` 字段指定）。
* 该项目使用 `demo` 资源配额模版。

### 资源配额与配额模版

一个项目的资源配额（由 `spec.resourceQuota` 字段指定）表示：当前项目中所能使用的资源上限，包括但不限于 cpu、内存、gpu 和 pod 数量。

值得说明的一点：项目的资源配额中关于 cpu、内存、gpu、pod 等资源数量的限制都直接作用于 pod。即如果您创建一个 T9k Job，它即将创建的 pod 需要申请超过项目资源配额的资源数量，则 T9k Job 会被成功创建，但是 T9k Job 创建 pod 的请求会被拒绝。

管理员可以使用**配额模版**批量设置或修改项目的资源配额。项目控制器会自动查找配额模版（由 `spec.quotaProfile` 字段指定）的内容，据此同步项目的资源配额。

### 网络策略

管理员可以通过项目的网络策略（由字段 `spec.networkPolicy` 字段指定）实现以下功能：

1. 禁止普通用户访问系统级应用，避免保密信息泄漏和系统遭到恶意攻击。
2. 阻断项目间通信，避免项目之间的互相干扰。
3. 限定项目的访客 IP，构建安全的项目环境。

## 项目授权

项目授权信息存储在特定的授权服务器而非项目定义中。

普通用户（包括项目管理员）可以在安全控制台（Security Console）查看自己所在和所管理的项目以及项目的成员。

项目管理员可以通过安全控制台编辑项目成员。

### 项目的使用范围

项目可以被应用到 TensorStack AI 平台的模型构建、模型部署和工作流三个模块，集群管理员可以设置一个项目的使用范围。

目前项目可选的使用范围包括：

* `build`：用户可以在模型构建和工作流模块中使用此项目。
* `deploy`：用户可以在模型部署模块中使用此项目。

一个项目可以同时设置上述两个使用范围。

### 项目成员管理

项目管理员可以在安全控制台设置项目成员：

* 项目成员可以是用户或用户组，一个用户组被设置为项目成员表示该组中的所有用户都可以使用该项目。
* 设置项目成员时，可以对每一个成员单独设置项目的使用范围，对成员设置的项目使用范围应为项目所有使用范围的子集。

## 下一步

* 了解项目管理员如何：[添加 Project 成员](../../tasks/add-project-member.md)
