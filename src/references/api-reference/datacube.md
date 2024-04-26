# API Reference

## Packages
- [tensorstack.dev/v1beta1](#tensorstackdevv1beta1)


## tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the  v1beta1 API group

### Resource Types
- [DataCube](#datacube)
- [DataCubeList](#datacubelist)



#### DataCube



DataCube is the Schema for the datacubes API

_Appears in:_
- [DataCubeList](#datacubelist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `DataCube`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[DataCubeSpec](#datacubespec)_ |  |
| `status` _[DataCubeStatus](#datacubestatus)_ |  |


#### DataCubeCondition



DataCubeCondition contains details for the current condition of this datacube

_Appears in:_
- [DataCubeStatus](#datacubestatus)

| Field | Description |
| --- | --- |
| `type` _[DataCubeConditionType](#datacubeconditiontype)_ | Type is the type of the condition. |
| `status` _[ConditionStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#conditionstatus-v1-core)_ | Status is the status of the condition. Can be True, False, Unknown. |
| `lastProbeTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta)_ | Last time we probed the condition. |
| `lastTransitionTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta)_ | Last time the condition transitioned from one status to another. |
| `reason` _string_ | Unique, one-word, CamelCase reason for the condition's last transition. |
| `message` _string_ | Human-readable message indicating details about last transition. |


#### DataCubeConditionType

_Underlying type:_ `string`

DataCubeConditionType defines all possible types of DataCubeStatus. Can be one of: Initialized, Complete, or Failed.

_Appears in:_
- [DataCubeCondition](#datacubecondition)



#### DataCubeList



DataCubeList contains a list of DataCube



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `DataCubeList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[DataCube](#datacube) array_ |  |


#### DataCubePhase

_Underlying type:_ `string`



_Appears in:_
- [DataCubeStatus](#datacubestatus)



#### DataCubeSpec



DataCubeSpec defines the desired state of DataCube

_Appears in:_
- [DataCube](#datacube)

| Field | Description |
| --- | --- |
| `source` _[DataReference](#datareference)_ | Source defines where the data is stored |
| `sink` _[DataReference](#datareference)_ | Sink defines where the data will be transferred to |
| `executor` _[ExecutorReference](#executorreference)_ | Executor defines how the data will be transferred |


#### DataCubeStatus



DataCubeStatus defines the observed state of DataCube

_Appears in:_
- [DataCube](#datacube)

| Field | Description |
| --- | --- |
| `phase` _[DataCubePhase](#datacubephase)_ | The phase of this datacube. |
| `conditions` _[DataCubeCondition](#datacubecondition) array_ | Conditions represent an array of current conditions observed within the system. |
| `pod` _[PodStatus](#podstatus)_ | The status of the underlying Pod |


#### DataReference





_Appears in:_
- [DataCubeSpec](#datacubespec)

| Field | Description |
| --- | --- |
| `type` _[DataType](#datatype)_ | Type of the data |
| `options` _[EnvVar](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#envvar-v1-core) array_ | Options for the data |
| `pvc` _[PVCReference](#pvcreference)_ | Data in pvc |


#### DataType

_Underlying type:_ `string`



_Appears in:_
- [DataReference](#datareference)



#### ExecutorOptions





_Appears in:_
- [ExecutorReference](#executorreference)

| Field | Description |
| --- | --- |
| `sync` _boolean_ | Whether to sync data, if false, use copy |
| `backoffLimit` _integer_ | Specifies the number of retries before marking this datacube failed. Defaults to 0. |
| `activeDeadlineSeconds` _integer_ | Specifies the duration in seconds relative to the startTime that the datacube may be active before the system tries to terminate it; value must be positive integer |
| `extraArgs` _string array_ | Extra args appended to executed command |


#### ExecutorReference





_Appears in:_
- [DataCubeSpec](#datacubespec)

| Field | Description |
| --- | --- |
| `options` _[ExecutorOptions](#executoroptions)_ | Options of executor |
| `env` _[EnvVar](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#envvar-v1-core) array_ | Env of executor's contianer |
| `securityContext` _[PodSecurityContext](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podsecuritycontext-v1-core)_ | SecurityContext of executor's container |


#### PVCReference





_Appears in:_
- [DataReference](#datareference)

| Field | Description |
| --- | --- |
| `name` _string_ | Name of PVC |
| `subPath` _string_ | Path within PVC |
| `template` _[PersistentVolumeClaimTemplate](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#persistentvolumeclaimtemplate-v1-core)_ | Template to create pvc if not exist, only avaliable when uploading |


#### PodReference



PodReference references a K8s v1.Pod.

_Appears in:_
- [PodStatus](#podstatus)

| Field | Description |
| --- | --- |
| `name` _string_ | Name of the Pod. |
| `uid` _string_ | UID of the Pod. |


#### PodStatus



PodStatus defines the observed status of the Pod running file transfer.

_Appears in:_
- [DataCubeStatus](#datacubestatus)

| Field | Description |
| --- | --- |
| `reference` _[PodReference](#podreference)_ | References to the subordinate v1.Pod. |
| `phase` _[PodPhase](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podphase-v1-core)_ | Replicated from the corresponding field in the subordinate v1.Pod. |
| `status` _string_ |  |


