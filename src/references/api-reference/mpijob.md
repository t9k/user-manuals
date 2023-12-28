# API Reference

## Packages
- [batch.tensorstack.dev/v1beta1](#batchtensorstackdevv1beta1)


## batch.tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the batch v1beta1 API group

### Resource Types
- [MPIJob](#mpijob)
- [MPIJobList](#mpijoblist)



#### MPIJob



MPIJob is the Schema for the mpijobs API

_Appears in:_
- [MPIJobList](#mpijoblist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/v1beta1`
| `kind` _string_ | `MPIJob`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta">ObjectMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[MPIJobSpec](#mpijobspec)_ |  |
| `status` _[MPIJobStatus](#mpijobstatus)_ |  |


#### MPIJobList



MPIJobList contains a list of MPIJob



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/v1beta1`
| `kind` _string_ | `MPIJobList`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta">ListMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[MPIJob](#mpijob) array_ |  |


#### MPIJobSpec



MPIJobSpec outlines the intended configuration and execution parameters for a MPIJob.

_Appears in:_
- [MPIJob](#mpijob)

| Field | Description |
| --- | --- |
| `worker` _[WorkerConfig](#workerconfig)_ | Specifications for the worker replicas. |
| `mca` _object (keys:string, values:string)_ | Open MPI uses Modular Component Architecture (MCA) parameters to provide a way to tune your runtime environment. |
| `ssh` _[SSHConfig](#sshconfig)_ | SSH configs. |
| `runPolicy` _[RunPolicy](#runpolicy)_ | Execution policy configurations governing the behavior of the MPI job. |
| `runMode` _[RunMode](#runmode)_ | Job's execution behavior. If omitted, defaults to `Immediate` mode, and tasks are executed immediately upon submission. |
| `mpiHome` _string_ | Open MPI installation path. |
| `scheduler` _SchedulePolicy_ | Identifies the preferred scheduler for allocating resources to replicas. Defaults to cluster default scheduler. Use k8s default scheduler by default. |


#### MPIJobStatus



MPIJobStatus represents the observed state of a MPIJob.

_Appears in:_
- [MPIJob](#mpijob)

| Field | Description |
| --- | --- |
| `tasks` _[Tasks](#tasks) array_ | Individual task status details of the job. |
| `aggregate` _[Aggregate](#aggregate)_ |  |
| `phase` _JobPhase_ | Provides a simple, high-level summary of where the Job is in its lifecycle. Note that this is NOT indended to be a comprehensive state machine. |
| `conditions` _[JobCondition](#jobcondition) array_ | The latest available observations of an object's current state. |


#### RunPolicy



RunPolicy encapsulates various runtime policies of the MPI job, for example how to clean up resources.

_Appears in:_
- [MPIJobSpec](#mpijobspec)

| Field | Description |
| --- | --- |
| `cleanUpWorkers` _boolean_ | If worker replicas should be cleand up after they finish. Defaults false. |


#### SSHConfig



SSHConfig specifies various configurations for running the SSH daemon (sshd).

_Appears in:_
- [MPIJobSpec](#mpijobspec)

| Field | Description |
| --- | --- |
| `sshAuthMountPath` _string_ | SSHAuthMountPath is the directory where SSH keys are mounted. Defaults to "/root/.ssh". |
| `sshdPath` _string_ |  |


#### WorkerConfig



 WorkerConfig defines the configurations for MPI worker replicas.

_Appears in:_
- [MPIJobSpec](#mpijobspec)

| Field | Description |
| --- | --- |
| `replicas` _integer_ | The number of workers to launch. Default 1. |
| `extraMPIArgs` _string array_ | Extra args for mpirun. |
| `cmd` _string array_ | Command line to start the MPI programs inside a worker pod. This is invoked by the launcher after all the worker pods have been created and entered ready state. |
| `template` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podtemplatespec-v1-core">PodTemplateSpec</a>_ | Defines the pod template used to create workers. Users are responsible for ensuring that container images and configurations are properly set to guarantee the worker operates in the state anticipated by the `launcher`. |


