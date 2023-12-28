# API Reference

## Packages
- [batch.tensorstack.dev/v1beta1](#batchtensorstackdevv1beta1)


## batch.tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the batch v1beta1 API group

### Resource Types
- [PyTorchTrainingJob](#pytorchtrainingjob)
- [PyTorchTrainingJobList](#pytorchtrainingjoblist)



#### ElasticConfig



Configuration governing the elastic scaling behavior of the job.

_Appears in:_
- [PyTorchTrainingJobSpec](#pytorchtrainingjobspec)

| Field | Description |
| --- | --- |
| `enabled` _boolean_ | Set true to use elastic training. |
| `minReplicas` _integer_ | The minimum number of replicas to start to run this elastic compute. The autoscaler cannot scale down an elastic job below this number. This value cannnot be changed once the job is created. |
| `maxReplicas` _integer_ | The maximum number of replicas to start to run this elastic compute. The autoscaler cannot scale up an elastic job over this number. This value cannnot be changed once the job is created. |
| `expectedReplicas` _integer_ | Number of replicas to be created. This number can be set to an initial value upon creation. This value can be modified dynamically by an external entity, such as a user or an autoscaler, to scale the job up or down. |




#### PyTorchTrainingJob



PyTorchTrainingJob is the Schema for the pytorchtrainingjobs API.

_Appears in:_
- [PyTorchTrainingJobList](#pytorchtrainingjoblist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/v1beta1`
| `kind` _string_ | `PyTorchTrainingJob`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta">ObjectMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[PyTorchTrainingJobSpec](#pytorchtrainingjobspec)_ |  |
| `status` _[PyTorchTrainingJobStatus](#pytorchtrainingjobstatus)_ |  |


#### PyTorchTrainingJobList



PyTorchTrainingJobList contains a list of PyTorchTrainingJob



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/v1beta1`
| `kind` _string_ | `PyTorchTrainingJobList`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta">ListMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[PyTorchTrainingJob](#pytorchtrainingjob) array_ |  |


#### PyTorchTrainingJobSpec



PyTorchTrainingJobSpec outlines the intended configuration and execution parameters for a PyTorchTrainingJo.

_Appears in:_
- [PyTorchTrainingJob](#pytorchtrainingjob)

| Field | Description |
| --- | --- |
| `replicaSpecs` _[ReplicaSpec](#replicaspec) array_ | An array of ReplicaSpec. Specifies the pytorch cluster configuration. |
| `elastic` _[ElasticConfig](#elasticconfig)_ | Configurations for how to launch an elastic training. Elastic training is effective only in torchrun mode. |
| `torchrunConfig` _[TorchrunConfig](#torchrunconfig)_ | Whether and how to use torchrun to launch a training process. |
| `runMode` _[RunMode](#runmode)_ | Job's execution behavior. If omitted, defaults to `Immediate` mode, and tasks are executed immediately upon submission. |
| `runPolicy` _[RunPolicy](#runpolicy)_ | Execution policy configurations governing the behavior of a PytorchTrainingJob. |
| `tensorboardSpec` _TensorBoardSpec_ | If specified, controller will create a Tensorboard for showing training logs. |
| `scheduler` _SchedulePolicy_ | Identifies the preferred scheduler for allocating resources to replicas. Defaults to cluster default scheduler. |


#### PyTorchTrainingJobStatus



PyTorchTrainingJobStatus defines the observed state of PyTorchTrainingJob.

_Appears in:_
- [PyTorchTrainingJob](#pytorchtrainingjob)

| Field | Description |
| --- | --- |
| `tasks` _[Tasks](#tasks) array_ | The status details of individual tasks. |
| `tensorboard` _DependentStatus_ | The status of the tensorboard. |
| `backoffCount` _integer_ | The number of restarts having been performed. |
| `aggregate` _[Aggregate](#aggregate)_ | The number of tasks in each state. |
| `conditions` _[JobCondition](#jobcondition) array_ | The latest available observations of an object's current state. |
| `phase` _JobPhase_ | Provides a simple, high-level summary of where the Job is in its lifecycle. Note that this is NOT indended to be a comprehensive state machine. |


#### ReplicaSpec



ReplicaSpec is a description of the job replica.

_Appears in:_
- [PyTorchTrainingJobSpec](#pytorchtrainingjobspec)

| Field | Description |
| --- | --- |
| `type` _string_ | ReplicaType is the type of the replica. |
| `replicas` _integer_ | The desired number of replicas of the current template. Defaults to 1. |
| `scalingWeight` _integer_ | Scaling weight of the current replica used in elastic training. |
| `template` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podtemplatespec-v1-core">PodTemplateSpec</a>_ | Describes the pod that will be created for this replica. Note that `RestartPolicy` in `PodTemplateSpec` will always be set to `Never` as the job controller will decide if restarts are desired. |
| `restartPolicy` _RestartPolicy_ | Restart policy for all replicas within the job. One of `Always`, `OnFailure`, `Never`, or `ExitCode`. |


#### TorchrunConfig



Describes how to launch pytorch training with torchrun.

_Appears in:_
- [PyTorchTrainingJobSpec](#pytorchtrainingjobspec)

| Field | Description |
| --- | --- |
| `enabled` _boolean_ | Set true to use torchrun launch pytorch training. |
| `maxRestarts` _integer_ |  |
| `procPerNode` _string_ | Number of processes to be started on every replica. |
| `rdzvBackend` _string_ | Communication backed used for the group. Defaults to `c10d`. |
| `extraOptions` _string array_ | Extra options for torchrun. |


