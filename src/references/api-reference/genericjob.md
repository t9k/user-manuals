# API Reference

## Packages
- [batch.tensorstack.dev/v1beta1](#batchtensorstackdevv1beta1)


## batch.tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the batch v1beta1 API group

### Resource Types
- [GenericJob](#genericjob)
- [GenericJobList](#genericjoblist)



#### Aggregate



Aggregate records the number of replica pods at each phase.

_Appears in:_
- [GenericJobStatus](#genericjobstatus)

| Field | Description |
| --- | --- |
| `creating` _integer_ | Pod has been created, but resources have not been scheduled. |
| `pending` _integer_ | Pod has been accepted by the system, but one or more of the containers has not been started. This includes time before being bound to a node, as well as time spent pulling images onto the host. |
| `running` _integer_ | Pod has been bound to a node and all of the containers have been started. At least one container is still running or is in the process of being restarted. |
| `succeeded` _integer_ | All containers in the pod have voluntarily terminated with a container exit code of 0, and the system is not going to restart any of these containers. |
| `failed` _integer_ | All containers in the pod have terminated, and at least one container has terminated in failure (exited with a non-zero exit code or was stopped by the system). |
| `unknown` _integer_ | For some reason the state of the pod could not be obtained, typically due to an error in communicating with the host of the pod. |
| `deleted` _integer_ | Pod has been deleted. |


#### CleanUpPolicy

_Underlying type:_ `string`

CleanUpPolicy specifies the collection of replicas that are to be deleted upon job completion.

_Appears in:_
- [GenericJobSpec](#genericjobspec)



#### ContainerStatus



ContainerStatus defines the observed state of the container.

_Appears in:_
- [ReplicaStatus](#replicastatus)



#### DebugMode



DebugMode configs whether and how to start a job in debug mode.

_Appears in:_
- [RunMode](#runmode)

| Field | Description |
| --- | --- |
| `enabled` _boolean_ | Whether to enable debug mode. |
| `replicaSpecs` _[ReplicaDebugSet](#replicadebugset) array_ | If provided, these specs provide overwriting values for job replicas. |


#### FinishRule



A finishRule is a condition used to check if the job has finished. A finishRule identifies a set of replicas, and the controller determines the job's status by checking the status of all of these replicas.

_Appears in:_
- [GenericJobSpec](#genericjobspec)



#### GenericJob



GenericJob represents the schema for a general-purpose batch job API. While it offers less automation compared to specialized APIs like PyTorchTrainingJob, it allows for greater flexibility in specifying parallel replicas/pods. This design serves as a comprehensive job definition mechanism when more specialized APIs are not applicable or available.

_Appears in:_
- [GenericJobList](#genericjoblist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/v1beta1`
| `kind` _string_ | `GenericJob`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta">ObjectMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[GenericJobSpec](#genericjobspec)_ |  |
| `status` _[GenericJobStatus](#genericjobstatus)_ |  |


#### GenericJobList



GenericJobList contains a list of GenericJob



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/v1beta1`
| `kind` _string_ | `GenericJobList`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta">ListMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[GenericJob](#genericjob) array_ |  |


#### GenericJobSpec



GenericJobSpec defines the desired state of GenericJob

_Appears in:_
- [GenericJob](#genericjob)

| Field | Description |
| --- | --- |
| `successRules` _[FinishRule](#finishrule) array_ | Rules used to check if a generic job has succeeded. The job succeeded when any one of the successRules is fulfilled. Each item of successRules may refer to a series of replicas, and the job succeeded only if all of the replicas referred in this series are completed successfully. |
| `failureRules` _[FinishRule](#finishrule) array_ | Rules used to check if a generic job has failed. The job failed when any one of failureRules is fulfilled. Each item of failureRules refers to a series of replicas, and the job failed only if all of the replicas in this series failed. |
| `service` _[ServiceOption](#serviceoption)_ | Details of v1/Service for replica pods. Optional: Defaults to empty and no service will be created. |
| `runMode` _[RunMode](#runmode)_ | Job running mode. Defaults to Immediate mode. |
| `cleanUpPolicy` _[CleanUpPolicy](#cleanuppolicy)_ | To avoid wasting resources on completed tasks, controller will reclaim resource according to the following policies:   None: (default) no resources reclamation;   Unfinished:  only finished pods is to be deleted;   All: all the pods are to be deleted. |
| `scheduler` _[SchedulePolicy](#schedulepolicy)_ | If specified, the pod will be dispatched by the specified scheduler. Otherwise, the pod will be dispatched by the default scheduler. |
| `replicaSpecs` _[ReplicaSpec](#replicaspec) array_ | List of replica specs belonging to the job. There must be at least one replica defined for a Job. |


#### GenericJobStatus



GenericJobStatus defines the observed state of GenericJob

_Appears in:_
- [GenericJob](#genericjob)

| Field | Description |
| --- | --- |
| `tasks` _[Tasks](#tasks) array_ | An array of status of individual tasks. |
| `phase` _[JobPhase](#jobphase)_ | Provides a simple, high-level summary of where the Job is in its lifecycle. Note that this is NOT indended to be a comprehensive state machine. |
| `aggregate` _[Aggregate](#aggregate)_ | Records the number of replicas at each phase. |
| `conditions` _[JobCondition](#jobcondition) array_ | The latest available observations of a job's current state. |


#### JobCondition



JobCondition describes the current state of a job.

_Appears in:_
- [GenericJobStatus](#genericjobstatus)

| Field | Description |
| --- | --- |
| `type` _[JobConditionType](#jobconditiontype)_ | Type of job condition: Complete or Failed. |
| `status` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#conditionstatus-v1-core">ConditionStatus</a>_ | Status of the condition, one of True, False, Unknown. |
| `lastTransitionTime` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta">Time</a>_ | Last time the condition transited from one status to another. |
| `reason` _string_ | Brief reason for the condition's last transition. |
| `message` _string_ | Human readable message indicating details about last transition. |


#### JobConditionType

_Underlying type:_ `string`

JobConditionType defines all possible types of JobStatus. Can be one of: Initialized, Running, ReplicaFailure, Completed, or Failed.

_Appears in:_
- [JobCondition](#jobcondition)



#### JobPhase

_Underlying type:_ `string`



_Appears in:_
- [GenericJobStatus](#genericjobstatus)



#### PauseMode



PauseMode configs whether and how to start a job in pause mode.

_Appears in:_
- [RunMode](#runmode)

| Field | Description |
| --- | --- |
| `enabled` _boolean_ | Whether to enable pause mode. |
| `resumeSpecs` _[ResumeSpec](#resumespec) array_ | If provided, these specs provide overwriting values for job replicas when resuming. |




#### ReplicaDebugSet



ReplicaDebugSet describes how to start replicas in debug mode.

_Appears in:_
- [DebugMode](#debugmode)

| Field | Description |
| --- | --- |
| `type` _string_ | Replica type. |
| `skipInitContainer` _boolean_ | Skips creation of initContainer, if true. |
| `command` _[string](#string)_ | Entrypoint array. Optional: Default to ["sleep", "inf"] |


#### ReplicaSpec



ReplicaSpec defines the desired state of replicas.

_Appears in:_
- [GenericJobSpec](#genericjobspec)

| Field | Description |
| --- | --- |
| `type` _string_ | Replica type. |
| `replicas` _integer_ | The desired number of replicas of this replica type. Defaults to 1. |
| `restartPolicy` _[RestartPolicy](#restartpolicy)_ | Restart policy for replicas of this replica type. One of Always, OnFailure, Never. Optional: Default to OnFailure. |
| `template` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podtemplatespec-v1-core">PodTemplateSpec</a>_ | Defines the template used to create pods. |


#### ReplicaStatus



ReplicaStatus defines the observed state of the pod.

_Appears in:_
- [Tasks](#tasks)

| Field | Description |
| --- | --- |
| `name` _string_ | Pod name. |
| `uid` _UID_ | Pod uid. |
| `phase` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podphase-v1-core">PodPhase</a>_ | Pod phase. The phase of a Pod is a simple, high-level summary of where the Pod is in its lifecycle. |
| `containers` _[ContainerStatus](#containerstatus) array_ | Containers status. |


#### RestartPolicy



RestartPolicy describes how the replica should be restarted.

_Appears in:_
- [ReplicaSpec](#replicaspec)

| Field | Description |
| --- | --- |
| `policy` _[RestartPolicyType](#restartpolicytype)_ | The policy to restart finished replica. |
| `limit` _integer_ | The maximum number of restarts. Optional: Default to 0. |


#### RestartPolicyType

_Underlying type:_ `string`



_Appears in:_
- [RestartPolicy](#restartpolicy)



#### ResumeSpec



ResumeSpec describes how to resume replicas from pause mode.

_Appears in:_
- [PauseMode](#pausemode)

| Field | Description |
| --- | --- |
| `type` _string_ | Replica type. |
| `skipInitContainer` _boolean_ | Skips creation of initContainer, if true. |
| `command` _[string](#string)_ | Entrypoint array. Provides overwriting values if provided; otherwise, values in immediate mode are used. |
| `args` _[string](#string)_ | Arguments to the entrypoint. Arguments in immediate mode are used if not provided. |


#### RunMode



RunMode defines the job's execution behavior:   Immediate mode: (Default) Tasks are executed immediately upon submission.   Debug mode: Job pods are created, but regular executions are replaced with null operations (e.g., sleep) for convenient debugging purposes.   Pause mode: Job execution is halted, and pods are deleted to reclaim resources. A graceful pod termination process is initiated to allow pods to exit cleanly.

_Appears in:_
- [GenericJobSpec](#genericjobspec)

| Field | Description |
| --- | --- |
| `debug` _[DebugMode](#debugmode)_ | Debug mode. |
| `pause` _[PauseMode](#pausemode)_ | Pause mode. |


#### SchedulePolicy



SchedulePolicy signals to K8s how the job should be scheduled.

_Appears in:_
- [GenericJobSpec](#genericjobspec)

| Field | Description |
| --- | --- |
| `t9kScheduler` _[T9kScheduler](#t9kscheduler)_ | T9k Scheduler. TODO: link to t9k scheduler docs. |


#### ServiceOption



Details of a replicas' servivce.

_Appears in:_
- [GenericJobSpec](#genericjobspec)

| Field | Description |
| --- | --- |
| `ports` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#serviceport-v1-core">ServicePort</a> array_ | The list of ports that are exposed by this service. |


#### T9kScheduler



T9kScheduler provides additonal configurations needed for the scheduling process.

_Appears in:_
- [SchedulePolicy](#schedulepolicy)

| Field | Description |
| --- | --- |
| `queue` _string_ | Specifies the name of the queue should be used for running this workload. TODO: link to t9k scheduler docs. |
| `priority` _integer_ | Indicates the priority of the PodGroup; valid range: [0, 100]. Optional: Default to 0. |


#### Tasks



Task defines the observed state of the task.

_Appears in:_
- [GenericJobStatus](#genericjobstatus)

| Field | Description |
| --- | --- |
| `type` _string_ | Replica type. |
| `restartCount` _integer_ | The number of restarts that have been performed. |
| `replicas` _[ReplicaStatus](#replicastatus) array_ | Replicas status array. |


