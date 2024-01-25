# API Reference

## Packages
- [tensorstack.dev/v1beta1](#tensorstackdevv1beta1)


## tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the  v1beta1 API group

### Resource Types
- [TensorBoard](#tensorboard)
- [TensorBoardList](#tensorboardlist)



#### HttpDataSource



Details of HTTP data source.

_Appears in:_
- [TensorBoardDataSource](#tensorboarddatasource)

| Field | Description |
| --- | --- |
| `url` _string array_ | Url pointing to the log files. |


#### PVCDataSource



Details of PVC data source.

_Appears in:_
- [TensorBoardDataSource](#tensorboarddatasource)

| Field | Description |
| --- | --- |
| `name` _string_ | PVC name. |
| `subPath` _string array_ | The relative paths of logs in the PVC. |


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
| `phase` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podphase-v1-core">PodPhase</a>_ | Replicated from the corresponding field in the subordinate `v1.Pod`. |


#### S3DataSource



Details of S3 data source.

_Appears in:_
- [TensorBoardDataSource](#tensorboarddatasource)

| Field | Description |
| --- | --- |
| `secretRef` _[SecretRef](#secretref)_ | S3 data source uses a secret to transmit access/secret key and service enpoint. |
| `uri` _string array_ | S3 object uri. |


#### SchedulePolicy



SchedulePolicy specifies the preferred scheduler responsible for handling resource allocation requests.

_Appears in:_
- [TensorBoardSpec](#tensorboardspec)

| Field | Description |
| --- | --- |
| `t9kScheduler` _[T9kScheduler](#t9kscheduler)_ |  |


#### SecretRef





_Appears in:_
- [S3DataSource](#s3datasource)

| Field | Description |
| --- | --- |
| `name` _string_ | Secret name. |


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
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta">ObjectMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[TensorBoardSpec](#tensorboardspec)_ |  |
| `status` _[TensorBoardStatus](#tensorboardstatus)_ |  |


#### TensorBoardCondition



TensorBoardCondition defines the observed condition of TensorBoard

_Appears in:_
- [TensorBoardStatus](#tensorboardstatus)

| Field | Description |
| --- | --- |
| `type` _[TensorBoardConditionType](#tensorboardconditiontype)_ | Type is the type of the condition. Possible values are Idle, etc |
| `status` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#conditionstatus-v1-core">ConditionStatus</a>_ | Status is the status of the condition type. Possible values of type Idle are True|False|Unknown |
| `message` _string_ | Message is the reason of the status |
| `lastTransitionTime` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta">Time</a>_ | LastTransitionTime is the last time the status was changed |
| `lastProbeTime` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta">Time</a>_ | LastProbeTime is the last time the condition was probed |


#### TensorBoardConditionType

_Underlying type:_ `string`



_Appears in:_
- [TensorBoardCondition](#tensorboardcondition)



#### TensorBoardDataSource



TensorBoardDataSource represents the location and type of the tensorboard data source. It includes three types of data sources: PVC, S3, and HTTP. In a tensorboard service, these three types of data sources can be used simultaneously.

_Appears in:_
- [TensorBoardSpec](#tensorboardspec)

| Field | Description |
| --- | --- |
| `pvc` _[PVCDataSource](#pvcdatasource) array_ | PVC represents PVCs that are mounted to workload as directories to provide log data. |
| `s3` _[S3DataSource](#s3datasource)_ | S3 represents a s3 service and access/secret key to access the service. |
| `http` _[HttpDataSource](#httpdatasource)_ | HTTP provides several urls. |


#### TensorBoardList



TensorBoardList contains a list of TensorBoard



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `TensorBoardList`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta">ListMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[TensorBoard](#tensorboard) array_ |  |


#### TensorBoardPhase

_Underlying type:_ `string`



_Appears in:_
- [TensorBoardStatus](#tensorboardstatus)



#### TensorBoardSpec



TensorBoardSpec defines the desired state of TensorBoard

_Appears in:_
- [TensorBoard](#tensorboard)

| Field | Description |
| --- | --- |
| `trainingLogFilesets` _string array_ | TrainingLogFilesets is the list of filesets containing training log. The format of fileset:   t9k://pvc/[pvc-name]/[subpath]   t9k://minio/[secret-name]/[bucket]/[subpath] To be deprecated: Use spec.logDir instead. |
| `logDir` _[TensorBoardDataSource](#tensorboarddatasource)_ | LogDir is a series of data source containing training log. |
| `image` _string_ | The container image used to run the tensorboard. |
| `suspend` _boolean_ | suspend specifies whether the TensorBoard controller should delete Pods or not. If true, the associated v1.Pod can be terminated. However, other API resources, such as ConfigMaps and Services, will be preserved for use upon resuming the TensorBoard. Defaults to false. |
| `scheduler` _[SchedulePolicy](#schedulepolicy)_ |  |
| `resources` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#resourcerequirements-v1-core">ResourceRequirements</a>_ | Compute Resources required by this container. Cannot be updated. More info: https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/ |


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


