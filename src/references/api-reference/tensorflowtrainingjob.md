# API Reference

## Packages
- [batch.tensorstack.dev/v1beta1](#batchtensorstackdevv1beta1)


## batch.tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the batch v1beta1 API group

### Resource Types
- [TensorFlowTrainingJob](#tensorflowtrainingjob)
- [TensorFlowTrainingJobList](#tensorflowtrainingjoblist)



#### ReplicaSpec



ReplicaSpec describes the spec of a replica.

_Appears in:_
- [TensorFlowTrainingJobSpec](#tensorflowtrainingjobspec)

| Field | Description |
| --- | --- |
| `type` _[ReplicaType](#replicatype)_ | ReplicaType is the type of the replica, one of "`chief`", "`worker`", "`ps`", or "`evaluator`". |
| `replicas` _integer_ | The desired number of replicas created for the current replica type. If unspecified, defaults to 1. |
| `template` _[PodTemplateSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podtemplatespec-v1-core)_ | Describes the pod that will be created for this replica. Note that RestartPolicy in PodTemplateSpec will always be set to `Never` as the job controller will create new pods if restart is required. |
| `restartPolicy` _[RestartPolicy](#restartpolicy)_ | The restart policy for this replica, one of `Always`, `OnFailure`, `Never`, or `ExitCode`. |


#### ReplicaType

_Underlying type:_ `string`

ReplicaType is the type of the replica, one of "`chief`", "`worker`", "`ps`", or "`evaluator`".

_Appears in:_
- [ReplicaSpec](#replicaspec)



#### RestartPolicy

_Underlying type:_ `string`

RestartPolicy describes how the replicas should be restarted. Can be one of: `Always`, `OnFailure`, `Never`, or `ExitCode`.

_Appears in:_
- [ReplicaSpec](#replicaspec)



#### RunPolicy



RunPolicy encapsulates various runtime policies of the distributed training job, for example how to clean up resources and how long the job can stay active.

_Appears in:_
- [TensorFlowTrainingJobSpec](#tensorflowtrainingjobspec)

| Field | Description |
| --- | --- |
| `activeDeadlineSeconds` _integer_ | Specifies the duration in seconds relative to the startTime that the job may be active before the system tries to terminate it; value must be positive integer. |
| `backoffLimit` _integer_ | Optional number of retries before marking this job failed. |
| `cleanUpPolicy` _CleanUpPolicy_ | Clean the tasks after the training job finished. |


#### TensorFlowTrainingJob



TensorFlowTrainingJob is the Schema for the TensorFlowTrainingJob API.

_Appears in:_
- [TensorFlowTrainingJobList](#tensorflowtrainingjoblist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/v1beta1`
| `kind` _string_ | `TensorFlowTrainingJob`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[TensorFlowTrainingJobSpec](#tensorflowtrainingjobspec)_ |  |
| `status` _[TensorFlowTrainingJobStatus](#tensorflowtrainingjobstatus)_ |  |


#### TensorFlowTrainingJobList



TensorFlowTrainingJobList contains a list of TensorFlowTrainingJob



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/v1beta1`
| `kind` _string_ | `TensorFlowTrainingJobList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[TensorFlowTrainingJob](#tensorflowtrainingjob) array_ |  |


#### TensorFlowTrainingJobSpec



TensorFlowTrainingJobSpec outlines the intended configuration and execution parameters for a TensorFlowTrainingJob.

_Appears in:_
- [TensorFlowTrainingJob](#tensorflowtrainingjob)

| Field | Description |
| --- | --- |
| `replicaSpecs` _[ReplicaSpec](#replicaspec) array_ | Describes the spec of the replicas of the job. |
| `runMode` _[RunMode](#runmode)_ | Job's execution behavior. If omitted, defaults to `Immediate` mode, and tasks are executed immediately upon submission. |
| `tensorboardSpec` _TensorBoardSpec_ | Describes the Tensorboard to be created for showing training logs. |
| `runPolicy` _[RunPolicy](#runpolicy)_ | Execution policy configurations governing the behavior of the TensorFlowTrainingJob. |
| `scheduler` _SchedulePolicy_ | Identifies the preferred scheduler for allocating resources to replicas. Defaults to cluster default scheduler. |


#### TensorFlowTrainingJobStatus



TensorFlowTrainingJobStatus defines the observed state of TensorFlowTrainingJob

_Appears in:_
- [TensorFlowTrainingJob](#tensorflowtrainingjob)

| Field | Description |
| --- | --- |
| `tasks` _[Tasks](#tasks) array_ | The statuses of individual tasks. |
| `tensorboard` _DependentStatus_ | The status of tensorboard. |
| `backoffCount` _integer_ | The number of restarts being performed. |
| `aggregate` _[Aggregate](#aggregate)_ |  |
| `conditions` _[JobCondition](#jobcondition) array_ | Represents the latest available observations of a TensorFlowTrainingJob's current state. |
| `phase` _JobPhase_ | Phase is the phase-style status of the TensorFlowTrainingJob. |


