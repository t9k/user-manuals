# ServiceAccountToken

平台提供 CRD `ServiceAccountToken`，用于生成一个 kubeconfig，以便用户从本地通过 kubectl 访问集群。

## 创建 ServiceAccountToken

下面是一个基本的 ServiceAccountToken 示例：

```yaml
apiVersion: tensorstack.dev/v1beta1
kind: ServiceAccountToken
metadata:
  name: sat-sample
spec:
  duration: 1h
```

在该例中，创建一个有效期为 `1h`（由 `spec.duration` 字段指定）的 ServiceAccountToken。系统将会生成一个 `JSON 网络令牌`（JSON Web Token）和一个 `kubeconfig`，您可以使用它们作为凭证来访问集群。

## 有效期设置

`spec.duration` 字段定义 ServiceAccountToken 的有效期：

* 类型是 string，并且需要匹配正则表达式 `^(0|(([0-9]+)y)?(([0-9]+)w)?(([0-9]+)d)?(([0-9]+)h)?(([0-9]+)m)?(([0-9]+)s)?)$`。
* 支持的时间单位：y, w（周）, d, h, m, s。
* 示例：“3w”，“2h45m”。

<aside class="note">
<div class="title">注意</div>

该字段定义的有效期为期望有效期，实际有效期以状态信息中的[过期时间](#过期时间)为准。

</aside>

## 状态

### Secret 名称

ServiceAccountToken 创建后，系统同步创建的 `token` 和 `kubeconfig` 存储在一个 Secret 中，并将 Secret 名称记录在 `status.secretRef.name` 中：

```yaml
status:
  secretRef:
    name: sat-sample-fced8
```

Secret `sat-sample-fced8` 存储以下两个键值对：

* `token`：表示一个 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/access-authn-authz/authentication/#service-account-tokens">ServiceAccount token</a>，您可以在 HTTP 请求头中以 `Authorization: Bearer <token>` 的形式使用。
* `kubeconfig`：表示一个 <a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/">kubeconfig</a> 文件内容，您可以将该内容保存到本地路径下，并在 `kubectl` 命令中通过 `--kubeconfig` 参数指定文件路径使用。

通过如下命令将 kubeconfig 保存到本地并使用：

```bash
kubectl get secret sat-sample-fced8 -o jsonpath='{.data.kubeconfig}' | base64 -d > mykubeconfig
kubectl --kubeconfig mykubeconfig get pod
```

<aside class="note">
<div class="title">注意</div>

上述 `token` 和 `kubeconfig` 只具备访问 ServiceAccountToken 所在命名空间的各类资源的权限。

</aside>

### 过期时间

ServiceAccountToken 创建后，`token` 的实际过期时间记录在 `status.expirationTime` 中：

```yaml
status:
  expirationTime: "2024-05-10T04:11:41Z"
```

在该例中，ServiceAccountToken 将在 `2024-05-10T04:11:41Z`（即北京时间 2024-05-10 12:11:41）过期。

<aside class="note info">
<div class="title">信息</div>

如果希望在过期前将 `token` 置为失效，直接删除该 ServiceAccountToken 即可。

</aside>

### ServiceAccountToken 状态

`status.conditions` 字段用于描述当前 ServiceAccountToken 的状态，包括以下一种类型：

* `Ready`：ServiceAccountToken 准备就绪，处于可用状态。

下面是一个状态信息的示例：

```yaml
status:
  conditions:
  - lastTransitionTime: "2024-05-10T02:51:41Z"
    message: All subresources are ready
    reason: SubresourcesReady
    status: "True"
    type: Ready
```

在该例中，所有子资源均就绪，ServiceAccountToken 是可用的。

<aside class="note info">
<div class="title">信息</div>

到过期时间之后，ServiceAccountToken 将不可用，状态信息示例为：

```yaml
status:
  conditions:
  - lastTransitionTime: "2024-05-10T04:11:41Z"
    message: This token has expired
    reason: TokenExpired
    status: "False"
    type: Ready
```

</aside>

<aside class="note">
<div class="title">注意</div>

如果 ServiceAccountToken 的某些子资源在过期前被删除了，ServiceAccountToken 将不可用，状态信息示例为：

```yaml
status:
  conditions:
  - lastTransitionTime: "2024-05-10T06:13:33Z"
    message: 'subresource not found: ServiceAccount <sat-namespace>/sat-sample has been deleted'
    reason: SubresourceNotFound
    status: "False"
    type: Ready
```

如果需要继续使用，您可以删除该 ServiceAccountToken 并重新创建，然后再使用新创建的 Secret 的 `token` 或 `kubeconfig`。

</aside>

## 参考

* API 参考：[ServiceAccountToken](../../references/api-reference/serviceaccounttoken.md)
