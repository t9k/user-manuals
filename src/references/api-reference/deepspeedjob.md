# API Reference

## Packages
- [batch.tensorstack.dev/v1beta1](#batchtensorstackdevv1beta1)


## batch.tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the batch v1beta1 API group

### Resource Types
- [DeepSpeedJob](#deepspeedjob)
- [DeepSpeedJobList](#deepspeedjoblist)



#### Config



Configuration information for running a DeepSpeed job. Details are outlined in the official DeepSpeed documentation (https://www.deepspeed.ai/getting-started/) for comprehensive guidance.

_Appears in:_
- [DeepSpeedJobSpec](#deepspeedjobspec)

| Field | Description |
| --- | --- |
| `customCommand` _string_ | Custom launch commands, when enabled, other options in Config except for `slotsPerWorker` will not take effect. |
| `slotsPerWorker` _integer_ | The number of slots for each worker/replica. This is normally set to the number of GPUs requested for each replica. |
| `localRank` _boolean_ | If parameter `local_rank` should be passed to training programs. |
| `autotune` _AutotuneType_ | Parameters for running the autotuning process to find configurations for a training job on a particular cluster/machine. |
| `run` _[RunType](#runtype)_ | Mechanism to start the training program. |
| `otherArgs` _string array_ | Seting up other command line args for the deepspeed job. |


#### DeepSpeedJob



DeepSpeedJob defines the schema for the DeepSpeedJob API.

_Appears in:_
- [DeepSpeedJobList](#deepspeedjoblist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/v1beta1`
| `kind` _string_ | `DeepSpeedJob`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[DeepSpeedJobSpec](#deepspeedjobspec)_ |  |
| `status` _[DeepSpeedJobStatus](#deepspeedjobstatus)_ |  |


#### DeepSpeedJobList



DeepSpeedJobList contains a list of DeepSpeedJob



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/v1beta1`
| `kind` _string_ | `DeepSpeedJobList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[DeepSpeedJob](#deepspeedjob) array_ |  |


#### DeepSpeedJobSpec



DeepSpeedJobSpec outlines the intended configuration and execution parameters for a DeepSpeedJob.

_Appears in:_
- [DeepSpeedJob](#deepspeedjob)

| Field | Description |
| --- | --- |
| `scheduler` _SchedulePolicy_ | Identifies the preferred scheduler for allocating resources to replicas. Defaults to cluster default scheduler. |
| `runPolicy` _[RunPolicy](#runpolicy)_ | Execution policy configurations governing the behavior of the distributed training job. |
| `runMode` _[RunMode](#runmode)_ | Job's execution behavior. If omitted, defaults to `Immediate` mode, and tasks are executed immediately upon submission. |
| `elastic` _[ElasticConfig](#elasticconfig)_ | Configurations for how to launch an elastic training. |
| `config` _[Config](#config)_ | Key configurations for executing DeepSpeed training jobs. |
| `disableCustomEnv` _boolean_ | Setting environment variables during DeepSpeed training necessitates creating an env file to store the desired variables. The launcher will then distribute these variables to each worker process. Nevertheless, certain scenarios require disabling this automated behavior, and this flag enables control over this functionality. 
 `false`: (default) The environment variables set in job specs are used in the training processes. The controller  will automatically put the environment variables into the env file so that the launcher can send them to each worker; 
 `true`: The environment variables set in the job specs are only used to start the container entrypoint program, and the training program does not need these environment variables. |
| `worker` _[Worker](#worker)_ | Specifications for the worker replicas. |


#### DeepSpeedJobStatus



DeepSpeedJobStatus represents the observed state of a DeepSpeedJob.

_Appears in:_
- [DeepSpeedJob](#deepspeedjob)

| Field | Description |
| --- | --- |
| `tasks` _[Tasks](#tasks) array_ |  |
| `aggregate` _[Aggregate](#aggregate)_ |  |
| `phase` _JobPhase_ | Provides a simple, high-level summary of where the Job is in its lifecycle. Note that this is NOT indended to be a comprehensive state machine. |
| `backoffCount` _integer_ | The number of restarts being performed. |
| `conditions` _[JobCondition](#jobcondition) array_ | The latest available observations of an object's current state. |


#### ElasticConfig



Configuration governing the elastic scaling behavior of the job.

_Appears in:_
- [DeepSpeedJobSpec](#deepspeedjobspec)

| Field | Description |
| --- | --- |
| `enabled` _boolean_ | Set true to use elastic training. |
| `minReplicas` _integer_ | The minimum number of replicas to start to run this elastic compute. The autoscaler cannot scale down an elastic job below this number. This value cannnot be changed once the job is created. |
| `maxReplicas` _integer_ | The maximum number of replicas to start to run this elastic compute. The autoscaler cannot scale up an elastic job over this number. This value cannnot be changed once the job is created. |
| `expectedReplicas` _integer_ | Number of replicas to be created. This number can be set to an initial value upon creation. This value can be modified dynamically by an external entity, such as a user or an autoscaler, to scale the job up or down. |


#### RunPolicy



RunPolicy encapsulates various runtime policies of the distributed training job, for example how to clean up resources and how long the job can stay active.

_Appears in:_
- [DeepSpeedJobSpec](#deepspeedjobspec)

| Field | Description |
| --- | --- |
| `activeDeadlineSeconds` _integer_ | Specifies the duration in seconds relative to the `startTime` that the job may be active before the system tries to terminate it; value must be positive integer. |
| `backoffLimit` _integer_ | Optional number of retries before marking this job failed. |
| `cleanUpPolicy` _CleanUpPolicy_ | Clean the tasks after the training job finished. |


#### RunType



How the training program should be started. Exactly one of the 3 choices should be set.

_Appears in:_
- [Config](#config)

| Field | Description |
| --- | --- |
| `python` _string array_ | Using a python script |
| `module` _string array_ | Using a python module |
| `exec` _string array_ | Using an executable program |


#### Worker



Worker defines the configurations for DeepSpeedJob worker replicas.

_Appears in:_
- [DeepSpeedJobSpec](#deepspeedjobspec)

| Field | Description |
| --- | --- |
| `replicas` _integer_ | The number of workers to launch. |
| `template` _[PodTemplateSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podtemplatespec-v1-core)_ | Describes the pod that will be created for this replica. Note that `RestartPolicy` in `PodTemplateSpec` will always be set to `Never` as the job controller will decide if restarts are desired. |
| `restartPolicy` _RestartPolicy_ | Restart policy for all replicas owned by the job. One of Always, OnFailure, Never, or ExitCode. Defaults to `OnFailure`. |


