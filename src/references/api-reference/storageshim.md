# API Reference

## Packages
- [tensorstack.dev/v1beta1](#tensorstackdevv1beta1)
- [tensorstack.dev/v1beta2](#tensorstackdevv1beta2)


## tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the  v1beta1 API group

### Resource Types
- [StorageShim](#storageshim)
- [StorageShimList](#storageshimlist)



#### S3Config



S3Config defines the config of s3

_Appears in:_
- [StorageShimSpec](#storageshimspec)

| Field | Description |
| --- | --- |
| `uri` _string_ |  |


#### SecretReference



SecretReference defines a Secret Reference

_Appears in:_
- [StorageShimSpec](#storageshimspec)

| Field | Description |
| --- | --- |
| `name` _string_ |  |


#### StorageShim



StorageShim is the Schema for the storageshims API

_Appears in:_
- [StorageShimList](#storageshimlist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `StorageShim`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta">ObjectMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[StorageShimSpec](#storageshimspec)_ |  |
| `status` _[StorageShimStatus](#storageshimstatus)_ |  |


#### StorageShimCondition



StorageShimCondition contains details for the current condition of this StorageShim

_Appears in:_
- [StorageShimStatus](#storageshimstatus)

| Field | Description |
| --- | --- |
| `type` _[StorageShimConditionType](#storageshimconditiontype)_ | Type is the type of the condition |
| `status` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#conditionstatus-v1-core">ConditionStatus</a>_ | Status is the status of the condition. Can be True, False, Unknown. |
| `message` _string_ | Human-readable message indicating details about last transition. |
| `lastTransitionTime` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta">Time</a>_ | Last time the condition transitioned from one status to another. |


#### StorageShimConditionType

_Underlying type:_ `string`

StorageShimConditionType is a valid value for StorageShimCondition.Type

_Appears in:_
- [StorageShimCondition](#storageshimcondition)



#### StorageShimList



StorageShimList contains a list of StorageShim



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `StorageShimList`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta">ListMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[StorageShim](#storageshim) array_ |  |


#### StorageShimSpec



StorageShimSpec defines the desired state of StorageShim

_Appears in:_
- [StorageShim](#storageshim)

| Field | Description |
| --- | --- |
| `s3` _[S3Config](#s3config)_ | S3 defines the config of s3, such as uri |
| `readOnly` _boolean_ | Specifies a read-only configuration. Defaults to false. |
| `secretRef` _[SecretReference](#secretreference)_ | Specifies a secret reference, must be in the same namespace of this StorageShim currently |


#### StorageShimStatus



StorageShimStatus defines the observed state of StorageShim

_Appears in:_
- [StorageShim](#storageshim)

| Field | Description |
| --- | --- |
| `phase` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#persistentvolumeclaimphase-v1-core">PersistentVolumeClaimPhase</a>_ | The phase of this StorageShim |
| `conditions` _[StorageShimCondition](#storageshimcondition) array_ | Conditions is an array of current conditions |



## tensorstack.dev/v1beta2

Package v1beta2 contains API Schema definitions for the  v1beta2 API group

### Resource Types
- [StorageShim](#storageshim)
- [StorageShimList](#storageshimlist)



#### CephFSClient



CephFSClient defines the client configurations to connnect to the cephfs server.

_Appears in:_
- [CephFSConfig](#cephfsconfig)

| Field | Description |
| --- | --- |
| `secretRef` _[SecretReference](#secretreference)_ | SecretRef references a Kubernetes v1.Secret object that securely stores the CephFS client configurations. |


#### CephFSConfig



CephFSConfig defines configuration details for a cephfs storage system.

_Appears in:_
- [StorageShimSpec](#storageshimspec)

| Field | Description |
| --- | --- |
| `path` _string_ | Path specifies the absolute path within a CephFS volume to be mounted. It should be a valid directory path within the mounted volume. For example, `/path/to/directory`. |
| `server` _[CephFSServer](#cephfsserver)_ | Server provides the configuration details for the CephFS cluster. This includes information such as the Ceph monitor IP addresses and the CephFS volume name. |
| `client` _[CephFSClient](#cephfsclient)_ | Client defines the details of a cephFS client. |


#### CephFSServer



CephFSServer defines the configuration details for the CephFS cluster.

_Appears in:_
- [CephFSConfig](#cephfsconfig)

| Field | Description |
| --- | --- |
| `configMapRef` _[ConfigMapReference](#configmapreference)_ | ConfigMapRef defines a reference to a K8s v1/configmap that stores CephFS cluster details such as the Ceph monitor IP addresses and the CephFS volume name. |


#### ConfigMapReference



ConfigMapReference defines a Kubernetes v1.ConfigMap reference.

_Appears in:_
- [CephFSServer](#cephfsserver)

| Field | Description |
| --- | --- |
| `name` _string_ | Name of the configmap. |
| `namespace` _string_ | Namespace where the configmap resides in. |


#### S3Config



S3Config defines the configuration details for an S3 object storage service.

_Appears in:_
- [StorageShimSpec](#storageshimspec)

| Field | Description |
| --- | --- |
| `readOnly` _boolean_ | Specifies that this S3 service can only be used as read-only. Defaults to false. |
| `uri` _string_ | The S3 prefix to mount, specified as `s3://<bucket>[/path]`. |
| `secretRef` _[SecretReference](#secretreference)_ | References a Kubernetes v1.Secret object. The referenced Secret must reside in the same namespace as the referencing StorageShim. |


#### SecretReference



SecretReference defines a reference to a Kubernetes v1.Secret object.

_Appears in:_
- [CephFSClient](#cephfsclient)
- [S3Config](#s3config)

| Field | Description |
| --- | --- |
| `name` _string_ | The name of a Kubernetes v1.Secret object that holds the CephFS client configurations. This Secret must reside within the same namespace as the referencing StorageShim. |


#### StorageShim



StorageShim is the Schema for the storageshims API

_Appears in:_
- [StorageShimList](#storageshimlist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta2`
| `kind` _string_ | `StorageShim`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta">ObjectMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[StorageShimSpec](#storageshimspec)_ |  |
| `status` _[StorageShimStatus](#storageshimstatus)_ |  |


#### StorageShimCondition



StorageShimCondition contains details for the current condition of this StorageShim

_Appears in:_
- [StorageShimStatus](#storageshimstatus)

| Field | Description |
| --- | --- |
| `type` _[StorageShimConditionType](#storageshimconditiontype)_ | Type is the type of the condition |
| `status` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#conditionstatus-v1-core">ConditionStatus</a>_ | Status is the status of the condition. Can be True, False, Unknown. |
| `message` _string_ | Human-readable message indicating details about last transition. |
| `lastTransitionTime` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta">Time</a>_ | Last time the condition transitioned from one status to another. |


#### StorageShimConditionType

_Underlying type:_ `string`

StorageShimConditionType is a valid value for StorageShimCondition.Type

_Appears in:_
- [StorageShimCondition](#storageshimcondition)



#### StorageShimList



StorageShimList contains a list of StorageShim



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta2`
| `kind` _string_ | `StorageShimList`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta">ListMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[StorageShim](#storageshim) array_ |  |


#### StorageShimSpec



StorageShimSpec defines the desired state of StorageShim

_Appears in:_
- [StorageShim](#storageshim)

| Field | Description |
| --- | --- |
| `type` _[StorageShimType](#storageshimtype)_ | Type specifies the type of storage system to be integrated with. One of the supported values is required, and currently `cephfs`, `s3` are supported. More storage system types will be added in the future. |
| `s3` _[S3Config](#s3config)_ | S3 defines the configuration details for an s3 object store service. |
| `cephfs` _[CephFSConfig](#cephfsconfig)_ | CephFS defines the configuraitons for a `cephfs`. |


#### StorageShimStatus



StorageShimStatus defines the observed state of StorageShim

_Appears in:_
- [StorageShim](#storageshim)

| Field | Description |
| --- | --- |
| `phase` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#persistentvolumeclaimphase-v1-core">PersistentVolumeClaimPhase</a>_ | The phase of this StorageShim. |
| `conditions` _[StorageShimCondition](#storageshimcondition) array_ | Conditions represent an array of current conditions observed within the system. |


#### StorageShimType

_Underlying type:_ `string`



_Appears in:_
- [StorageShimSpec](#storageshimspec)



