# API Reference

## Packages
- [tensorstack.dev/v1beta1](#tensorstackdevv1beta1)


## tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the  v1beta1 API group

### Resource Types
- [Explorer](#explorer)
- [ExplorerList](#explorerlist)



#### Explorer



Explorer is the Schema for the explorers API

_Appears in:_
- [ExplorerList](#explorerlist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `Explorer`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta">ObjectMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[ExplorerSpec](#explorerspec)_ |  |
| `status` _[ExplorerStatus](#explorerstatus)_ |  |


#### ExplorerCondition



ExplorerCondition defines the observed condition of Explorer resource

_Appears in:_
- [ExplorerStatus](#explorerstatus)

| Field | Description |
| --- | --- |
| `type` _[ExplorerConditionType](#explorerconditiontype)_ | Type is the type of the condition. Possible values are Idle, etc |
| `status` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#conditionstatus-v1-core">ConditionStatus</a>_ | Status is the status of the condition type. Possible values of type Idle are True|False|Unknown |
| `message` _string_ | Message is the reason of the status |
| `lastTransitionTime` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta">Time</a>_ | LastTransitionTime is the last time the status was changed |
| `lastProbeTime` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta">Time</a>_ | LastProbeTime is the last time the condition was probed |


#### ExplorerConditionType

_Underlying type:_ `string`



_Appears in:_
- [ExplorerCondition](#explorercondition)



#### ExplorerList



ExplorerList contains a list of Explorer



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `ExplorerList`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta">ListMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[Explorer](#explorer) array_ |  |


#### ExplorerRunMode

_Underlying type:_ `string`



_Appears in:_
- [ExplorerSpec](#explorerspec)



#### ExplorerSpec



ExplorerSpec defines the desired state of Explorer

_Appears in:_
- [Explorer](#explorer)

| Field | Description |
| --- | --- |
| `storageType` _[StorageType](#storagetype)_ | Type of storage, only `pvc` is supported for now. |
| `storageName` _string_ | Name of the StorageType instance. |
| `runMode` _[ExplorerRunMode](#explorerrunmode)_ |  |
| `scheduler` _[SchedulePolicy](#schedulepolicy)_ |  |


#### ExplorerStatus



ExplorerStatus defines the observed state of Explorer

_Appears in:_
- [Explorer](#explorer)

| Field | Description |
| --- | --- |
| `conditions` _[ExplorerCondition](#explorercondition) array_ | Conditions is an array of current conditions |
| `codeServer` _[ResourceStatus](#resourcestatus)_ |  |
| `fileBrowser` _[ResourceStatus](#resourcestatus)_ |  |


#### PodReference



PodReference refers to a replica.

_Appears in:_
- [PodStatus](#podstatus)

| Field | Description |
| --- | --- |
| `name` _string_ | Name of the Pod. |
| `uid` _string_ | UID of the Pod. |


#### PodStatus



Pod defines the observed state of a replica.

_Appears in:_
- [ResourceStatus](#resourcestatus)

| Field | Description |
| --- | --- |
| `reference` _[PodReference](#podreference)_ | References to the subordinate v1.Pod. |
| `phase` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podphase-v1-core">PodPhase</a>_ | Replicated from the corresponding field in the subordinate v1.Pod. |


#### ResourcePhase

_Underlying type:_ `string`



_Appears in:_
- [ResourceStatus](#resourcestatus)



#### ResourceStatus





_Appears in:_
- [ExplorerStatus](#explorerstatus)

| Field | Description |
| --- | --- |
| `phase` _[ResourcePhase](#resourcephase)_ |  |
| `pod` _[PodStatus](#podstatus)_ |  |


#### SchedulePolicy



SchedulePolicy specifies preferences for resource allocation requests, including the name of the preferred scheduler and additional configuration parameters.

_Appears in:_
- [ExplorerSpec](#explorerspec)

| Field | Description |
| --- | --- |
| `t9kScheduler` _[T9kScheduler](#t9kscheduler)_ |  |


#### StorageType

_Underlying type:_ `string`

StorageType is the type of storage volume.

_Appears in:_
- [ExplorerSpec](#explorerspec)



#### T9kScheduler





_Appears in:_
- [SchedulePolicy](#schedulepolicy)

| Field | Description |
| --- | --- |
| `queue` _string_ | Name of the resource `Queue` of a `T9kScheduler`. |


