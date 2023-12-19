# API Reference

## Packages
- [batch.tensorstack.dev/v1beta1](#batchtensorstackdevv1beta1)


## batch.tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the batch v1beta1 API group

### Resource Types
- [ColossalAIJob](#colossalaijob)
- [ColossalAIJobList](#colossalaijoblist)



#### ColossalAIJob



ColossalAIJob is the Schema for the colossalaijobs API

_Appears in:_
- [ColossalAIJobList](#colossalaijoblist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/v1beta1`
| `kind` _string_ | `ColossalAIJob`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[ColossalAIJobSpec](#colossalaijobspec)_ |  |
| `status` _[ColossalAIJobStatus](#colossalaijobstatus)_ |  |


#### ColossalAIJobList



ColossalAIJobList contains a list of ColossalAIJob.



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/v1beta1`
| `kind` _string_ | `ColossalAIJobList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[ColossalAIJob](#colossalaijob) array_ |  |


#### ColossalAIJobSpec



ColossalAIJobSpec defines the configurations of a ColossalAI training job.

_Appears in:_
- [ColossalAIJob](#colossalaijob)

| Field | Description |
| --- | --- |
| `ssh` _[SSHConfig](#sshconfig)_ | SSH configs. |
| `runMode` _[RunMode](#runmode)_ | The desired running mode of the job, defaults to `Immediate`. |
| `runPolicy` _[RunPolicy](#runpolicy)_ | Controls the handling of completed replicas and other related processes. |
| `scheduler` _SchedulePolicy_ | Specifies the scheduler to request for resources. Defaults to cluster default scheduler. |
| `launcher` _[Launcher](#launcher)_ | Specication for the launcher replica. |
| `worker` _[Worker](#worker)_ | Specication for the launcher replica. |


#### ColossalAIJobStatus



ColossalAIJobStatus describes the observed state of ColossalAIJob.

_Appears in:_
- [ColossalAIJob](#colossalaijob)

| Field | Description |
| --- | --- |
| `tasks` _[Tasks](#tasks) array_ | The statuses of individual tasks. |
| `aggregate` _[Aggregate](#aggregate)_ | The number of replicas in each phase. |
| `phase` _JobPhase_ | Provides a simple, high-level summary of where the Job is in its lifecycle. Note that this is NOT indended to be a comprehensive state machine. |
| `conditions` _[JobCondition](#jobcondition) array_ | The latest available observations of an object's current state. |


#### Launcher



Specification of replica `launcher`.

_Appears in:_
- [ColossalAIJobSpec](#colossalaijobspec)

| Field | Description |
| --- | --- |
| `image` _string_ | Container image name. |
| `workingDir` _string_ | Working directory of container `launcher`. If not specified, the container runtime's default will be used, which might be configured in the container image. Cannot be updated. |
| `env` _[EnvVar](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#envvar-v1-core) array_ | List of environment variables set for the container. Cannot be updated. |
| `resources` _[ResourceRequirements](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#resourcerequirements-v1-core)_ | Compute Resources required by this container. Cannot be updated. More info: https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/ |


#### RunPolicy



RunPolicy dictates specific actions to be taken by the controller upon job completion.

_Appears in:_
- [ColossalAIJobSpec](#colossalaijobspec)

| Field | Description |
| --- | --- |
| `cleanUpWorkers` _boolean_ | Defaults to false. |


#### SSHConfig



SSHConfig specifies various configurations for running the SSH daemon (sshd).

_Appears in:_
- [ColossalAIJobSpec](#colossalaijobspec)

| Field | Description |
| --- | --- |
| `authMountPath` _string_ | SSHAuthMountPath is the directory where SSH keys are mounted. Defaults to "/root/.ssh". |
| `sshdPath` _string_ | The location of the sshd executable file. |


#### Worker



Specification of the worker replicas.

_Appears in:_
- [ColossalAIJobSpec](#colossalaijobspec)

| Field | Description |
| --- | --- |
| `replicas` _integer_ | Number of replicas to launch. Defaults to 1. |
| `procPerWorker` _integer_ | The number of processes of a worker. Defaults to 1. |
| `command` _string array_ | Specifies the command used to start the workers. |
| `torchArgs` _string array_ | Args of torchrun. |
| `template` _[PodTemplateSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podtemplatespec-v1-core)_ | Template defines the workers that will be created from this pod template. |


