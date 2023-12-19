# API Reference

## Packages
- [tensorstack.dev/v1beta1](#tensorstackdevv1beta1)


## tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the  v1beta1 API group

### Resource Types
- [TensorBoard](#tensorboard)
- [TensorBoardList](#tensorboardlist)



#### PodReference



PodReference references to a `v1.pod`.

_Appears in:_
- [PodStatus](#podstatus)

| Field | Description |
| --- | --- |
| `name` _string_ | Name of the Pod. |
| `uid` _string_ | UID of the Pod. |


#### PodStatus



Pod defines the observed state of a replica.

_Appears in:_
- [TensorBoardStatus](#tensorboardstatus)

| Field | Description |
| --- | --- |
| `reference` _[PodReference](#podreference)_ | References to the subordinate `v1.Pod`. |
| `phase` _[PodPhase](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podphase-v1-core)_ | Replicated from the corresponding field in the subordinate `v1.Pod`. |


#### SchedulePolicy



SchedulePolicy specifies the preferred scheduler responsible for handling resource allocation requests.

_Appears in:_
- [TensorBoardSpec](#tensorboardspec)

| Field | Description |
| --- | --- |
| `t9kScheduler` _[T9kScheduler](#t9kscheduler)_ |  |


#### T9kScheduler





_Appears in:_
- [SchedulePolicy](#schedulepolicy)

| Field | Description |
| --- | --- |
| `queue` _string_ | Name of the queue to use with the T9kScheduler. |


#### TensorBoard



TensorBoard is the Schema for the tensorboards API

_Appears in:_
- [TensorBoardList](#tensorboardlist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `TensorBoard`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[TensorBoardSpec](#tensorboardspec)_ |  |
| `status` _[TensorBoardStatus](#tensorboardstatus)_ |  |


#### TensorBoardCondition



TensorBoardCondition defines the observed condition of TensorBoard

_Appears in:_
- [TensorBoardStatus](#tensorboardstatus)

| Field | Description |
| --- | --- |
| `type` _[TensorBoardConditionType](#tensorboardconditiontype)_ | Type is the type of the condition. Possible values are Idle, etc |
| `status` _[ConditionStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#conditionstatus-v1-core)_ | Status is the status of the condition type. Possible values of type Idle are True|False|Unknown |
| `message` _string_ | Message is the reason of the status |
| `lastTransitionTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta)_ | LastTransitionTime is the last time the status was changed |
| `lastProbeTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta)_ | LastProbeTime is the last time the condition was probed |


#### TensorBoardConditionType

_Underlying type:_ `string`



_Appears in:_
- [TensorBoardCondition](#tensorboardcondition)



#### TensorBoardList



TensorBoardList contains a list of TensorBoard



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `TensorBoardList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[TensorBoard](#tensorboard) array_ |  |


#### TensorBoardPhase

_Underlying type:_ `string`



_Appears in:_
- [TensorBoardStatus](#tensorboardstatus)



#### TensorBoardRunMode

_Underlying type:_ `string`



_Appears in:_
- [TensorBoardSpec](#tensorboardspec)



#### TensorBoardSpec



TensorBoardSpec defines the desired state of TensorBoard

_Appears in:_
- [TensorBoard](#tensorboard)

| Field | Description |
| --- | --- |
| `trainingLogFilesets` _string array_ | TrainingLogFilesets is the list of filesets containing training log. TODO: Document the syntax of this field. |
| `image` _string_ | The container image used to run the tensorboard. |
| `runMode` _[TensorBoardRunMode](#tensorboardrunmode)_ |  |
| `scheduler` _[SchedulePolicy](#schedulepolicy)_ |  |
| `resources` _[ResourceRequirements](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#resourcerequirements-v1-core)_ | Compute Resources required by this container. Cannot be updated. More info: https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/ |


#### TensorBoardStatus



TensorBoardStatus defines the observed state of TensorBoard

_Appears in:_
- [TensorBoard](#tensorboard)

| Field | Description |
| --- | --- |
| `phase` _[TensorBoardPhase](#tensorboardphase)_ |  |
| `pod` _[PodStatus](#podstatus)_ |  |
| `conditions` _[TensorBoardCondition](#tensorboardcondition) array_ | Conditions is an array of current conditions |
| `url` _string_ | The URL to Web UI of the tensorboard |


