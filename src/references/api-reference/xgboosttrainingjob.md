# API Reference

## Packages
- [batch.tensorstack.dev/v1beta1](#batchtensorstackdevv1beta1)


## batch.tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the batch v1beta1 API group

### Resource Types
- [XGBoostTrainingJob](#xgboosttrainingjob)
- [XGBoostTrainingJobList](#xgboosttrainingjoblist)



#### ReplicaSpec



ReplicaSpec outlines the intended configuration and execution parameters for a XGBoostTrainingJob.

_Appears in:_
- [XGBoostTrainingJobSpec](#xgboosttrainingjobspec)

| Field | Description |
| --- | --- |
| `type` _[ReplicaType](#replicatype)_ | ReplicaType is the type of the replica, one of "master" or "worker". |
| `replicas` _integer_ | The desired number of replicas of the current template. If unspecified, defaults to 1. |
| `template` _[PodTemplateSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podtemplatespec-v1-core)_ | Describes the pod that will be created for this replica. Note that `RestartPolicy` in `PodTemplateSpec` will always be set to `Never` as the job controller will decide if restarts are desired. |
| `restartPolicy` _RestartPolicy_ | Restart policy for all replicas within the job. One of Always, OnFailure, Never, or ExitCode. Defaults to `OnFailure`. |


#### ReplicaType

_Underlying type:_ `string`

ReplicaType is the type of the replica, one of "`master`" or "`worker`".

_Appears in:_
- [ReplicaSpec](#replicaspec)



#### XGBoostTrainingJob





_Appears in:_
- [XGBoostTrainingJobList](#xgboosttrainingjoblist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/v1beta1`
| `kind` _string_ | `XGBoostTrainingJob`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[XGBoostTrainingJobSpec](#xgboosttrainingjobspec)_ |  |
| `status` _[XGBoostTrainingJobStatus](#xgboosttrainingjobstatus)_ |  |


#### XGBoostTrainingJobList



XGBoostTrainingJobList contains a list of XGBoostTrainingJob.



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/v1beta1`
| `kind` _string_ | `XGBoostTrainingJobList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[XGBoostTrainingJob](#xgboosttrainingjob) array_ |  |


#### XGBoostTrainingJobSpec





_Appears in:_
- [XGBoostTrainingJob](#xgboosttrainingjob)

| Field | Description |
| --- | --- |
| `replicaSpecs` _[ReplicaSpec](#replicaspec) array_ | An array of ReplicaSpec. Specifies the XGBoost replica configurations. |
| `runMode` _[RunMode](#runmode)_ | Job's execution behavior. If omitted, defaults to `Immediate` mode, and tasks are executed immediately upon submission. |
| `runPolicy` _[RunPolicy](#runpolicy)_ | Execution policy configurations governing the behavior of the XGBoostTrainingJob. |
| `scheduler` _SchedulePolicy_ | Identifies the preferred scheduler for allocating resources to replicas. Defaults to cluster default scheduler. |


#### XGBoostTrainingJobStatus



XGBoostTrainingJobStatus defines the observed state of XGBoostTrainingJob.

_Appears in:_
- [XGBoostTrainingJob](#xgboosttrainingjob)

| Field | Description |
| --- | --- |
| `tasks` _[Tasks](#tasks) array_ | The status details of individual tasks. |
| `backoffCount` _integer_ | The number of restarts being performed. |
| `aggregate` _[Aggregate](#aggregate)_ |  |
| `conditions` _[JobCondition](#jobcondition) array_ | The latest available observations of an object's current state. |
| `phase` _JobPhase_ | Provides a simple, high-level summary of where the Job is in its lifecycle. Note that this is NOT indended to be a comprehensive state machine. |


