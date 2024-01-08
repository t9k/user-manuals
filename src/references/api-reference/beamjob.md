# API Reference

## Packages
- [batch.tensorstack.dev/v1beta1](#batchtensorstackdevv1beta1)


## batch.tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the batch v1beta1 API group

### Resource Types
- [BeamJob](#beamjob)
- [BeamJobList](#beamjoblist)



#### BeamJob



BeamJob is the Schema for the beamjobs API

_Appears in:_
- [BeamJobList](#beamjoblist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/v1beta1`
| `kind` _string_ | `BeamJob`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[BeamJobSpec](#beamjobspec)_ |  |
| `status` _[BeamJobStatus](#beamjobstatus)_ |  |


#### BeamJobList



BeamJobList contains a list of BeamJob



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/v1beta1`
| `kind` _string_ | `BeamJobList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[BeamJob](#beamjob) array_ |  |


#### BeamJobSpec



BeamJobSpec defines the desired state of BeamJob

_Appears in:_
- [BeamJob](#beamjob)

| Field | Description |
| --- | --- |
| `flinkClusterTemplate` _[FlinkClusterTemplateSpec](#flinkclustertemplatespec)_ | Specifies the FlinkCluster that will be created when executing a BeamJob. |
| `jobTemplate` _[JobTemplateSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#jobtemplatespec-v1beta1-batch)_ | Specifies the Job that will be created when executing a BeamJob. |
| `runPolicy` _[RunPolicy](#runpolicy)_ | Runtime policies governing the behavior of the BeamJob. |
| `scheduler` _SchedulePolicy_ | Identifies the preferred scheduler for allocating resources to replicas. Defaults to cluster default scheduler. |
| `runMode` _[RunMode](#runmode)_ | Normal mode and debug mode are supported now. |


#### BeamJobStatus



BeamJobStatus defines the observed state of BeamJob

_Appears in:_
- [BeamJob](#beamjob)

| Field | Description |
| --- | --- |
| `phase` _JobPhase_ | Phase is a label for the condition of the job at the current time. |
| `conditions` _[JobCondition](#jobcondition) array_ | The latest available observations of the BeamJob's current state. |
| `tasks` _[Tasks](#tasks) array_ | The statuses of individual tasks. |
| `aggregate` _[Aggregate](#aggregate)_ |  |
| `jobURL` _string_ | The URL to Web UI of the cluster where details of the job is displayed. |


#### FlinkClusterTemplateSpec



FlinkClusterTemplateSpec describes the data a FlinkCluster should have when created from a template

_Appears in:_
- [BeamJobSpec](#beamjobspec)

| Field | Description |
| --- | --- |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[FlinkClusterSpec](#flinkclusterspec)_ | Specification of the desired behavior of the FlinkCluster. |


#### RunPolicy



RunPolicy encapsulates runtime policies governing the behavior of the BeamJob.

_Appears in:_
- [BeamJobSpec](#beamjobspec)

| Field | Description |
| --- | --- |
| `cleanUpCluster` _boolean_ | Whether or not delete cluster after the job finished. Default false. |


