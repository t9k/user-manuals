# API Reference

## Packages
- [batch.tensorstack.dev/v1beta1](#batchtensorstackdevv1beta1)


## batch.tensorstack.dev/v1beta1

Package apis defines the CRD types.

### Resource Types
- [CronWorkflowRun](#cronworkflowrun)
- [CronWorkflowRunList](#cronworkflowrunlist)
- [WorkflowRun](#workflowrun)
- [WorkflowRunList](#workflowrunlist)
- [WorkflowTemplate](#workflowtemplate)
- [WorkflowTemplateList](#workflowtemplatelist)



#### BeamJobWorkflowTemplate



BeamJobWorkflowTemplate creates a t9k beam job.

_Appears in:_
- [WorkflowTemplateSpec](#workflowtemplatespec)

| Field | Description |
| --- | --- |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[BeamJobSpec](#beamjobspec)_ | Spec of the beam job. |


#### ConcurrencyPolicy

_Underlying type:_ `string`

ConcurrencyPolicy describes how the WorkflowRun will be handled. Only one of the following concurrent policies may be specified. If none of the following policies is specified, the default one is AllowConcurrent.

_Appears in:_
- [CronWorkflowRunSpec](#cronworkflowrunspec)



#### ConditionSelector



ConditionSelector selects a k8s resource if its `status.conditions` contains a condition whose type and status are exactly the same as those of the condition selector.

_Appears in:_
- [Rules](#rules)

| Field | Description |
| --- | --- |
| `type` _string_ | Type of the condition. |
| `status` _[ConditionStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#conditionstatus-v1-core)_ | Status of the condition, one of True, False, or Unknown. |


#### CronWorkflowRun



CronWorkflowRun is the Schema for the CronWorkflowRun API

_Appears in:_
- [CronWorkflowRunList](#cronworkflowrunlist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/apis`
| `kind` _string_ | `CronWorkflowRun`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[CronWorkflowRunSpec](#cronworkflowrunspec)_ |  |
| `status` _[CronWorkflowRunStatus](#cronworkflowrunstatus)_ |  |


#### CronWorkflowRunCondition



CronWorkflowRunCondition is an observation of the condition of the CronWorkflowRun.

_Appears in:_
- [CronWorkflowRunStatus](#cronworkflowrunstatus)

| Field | Description |
| --- | --- |
| `type` _[CronWorkflowRunConditionType](#cronworkflowrunconditiontype)_ | Type of CronWorkflowRun condition. |
| `status` _[ConditionStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#conditionstatus-v1-core)_ | Status of the condition, one of True, False, or Unknown. |
| `reason` _string_ | The reason for the condition's last transition. |
| `message` _string_ | A readable message indicating details about the transition. |
| `lastTransitionTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta)_ | Last time the condition transitioned from one status to another. |


#### CronWorkflowRunConditionType

_Underlying type:_ `string`

CronWorkflowRunConditionType defines all possible types of CronWorkflowRunCondition. Can be one of: HasStarted, IsRunning, HasSuccessfulRun, HasFailedRun.

_Appears in:_
- [CronWorkflowRunCondition](#cronworkflowruncondition)



#### CronWorkflowRunList



CronWorkflowRunList contains a list of CronWorkflowRun



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/apis`
| `kind` _string_ | `CronWorkflowRunList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[CronWorkflowRun](#cronworkflowrun) array_ |  |


#### CronWorkflowRunSpec



CronWorkflowRunSpec defines the desired state of CronWorkflowRun.

_Appears in:_
- [CronWorkflowRun](#cronworkflowrun)

| Field | Description |
| --- | --- |
| `schedule` _string_ | Schedule defines the schedule for the running of WorkflowRuns. |
| `concurrencyPolicy` _[ConcurrencyPolicy](#concurrencypolicy)_ | Specifies how to treat concurrent executions of a WorkflowRun. Valid values are: - "Allow" (default): allows WorkflowRuns to run concurrently; - "Forbid": forbids concurrent runs, skipping next run if previous run hasn't finished yet; - "Replace": cancels currently running WorkflowRun and replaces it with a new one |
| `successfulRunsHistoryLimit` _integer_ | The number of successful finished WorkflowRuns to retain. This is a pointer to distinguish between explicit zero and not specified. |
| `failedRunsHistoryLimit` _integer_ | The number of failed finished WorkflowRuns to retain. This is a pointer to distinguish between explicit zero and not specified. |
| `startingDeadlineSeconds` _integer_ | Deadline in seconds for starting the WorkflowRuns if it misses scheduled time for any reason.  Missed WorkflowRun runs will be counted as failed ones. |
| `suspend` _boolean_ | This flag tells the controller to suspend subsequent runs, it does not apply to already started runs.  Defaults to false. |
| `workflowRun` _[WorkflowRunTemplateSpec](#workflowruntemplatespec)_ | Specifies the WorkflowRun that will be created when executing a CronWorkflowRun. |


#### CronWorkflowRunStatus



CronWorkflowRunStatus defines the observed state of CronWorkflowRun.

_Appears in:_
- [CronWorkflowRun](#cronworkflowrun)

| Field | Description |
| --- | --- |
| `active` _[ObjectReference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectreference-v1-core) array_ | A list of pointers to currently running WorkflowRuns. |
| `lastScheduleTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta)_ | The last time when the WorkflowRun was successfully created. |
| `conditions` _[CronWorkflowRunCondition](#cronworkflowruncondition) array_ | The latest available observations of the CronWorkflowRun's current state. |


#### DAGNode



DAGNode represents a node in the graph during DAG execution.

_Appears in:_
- [DAGWorkflowTemplate](#dagworkflowtemplate)

| Field | Description |
| --- | --- |
| `name` _string_ | Name is the name of this node within the DAG. |
| `workflowTemplateRef` _string_ | WorkflowTemplateRef is a reference to a workflowTemplate definition. |
| `when` _[WhenExpression](#whenexpression) array_ | WhenExpressions is a list of when expressions that need to be true for the node to run |
| `retries` _integer_ | Retries represents how many times this node should be retried in case of failure: Condition Succeeded set to False |
| `dependencies` _string array_ | Dependencies are name of other nodes which this depends on, to force a specific ordering in graph execution. |
| `params` _[Param](#param) array_ | Parameters declares parameters passed to this node. |
| `workspaces` _[WorkspaceDAGBinding](#workspacedagbinding) array_ | Workspaces maps workspaces from the DAG WorkflowTemplate spec to the workspaces declared in the node. |




#### DAGWorkflowTemplate



DAGWorkflowTemplate creates a dag consisting of other WorkflowTemplates.

_Appears in:_
- [WorkflowTemplateSpec](#workflowtemplatespec)

| Field | Description |
| --- | --- |
| `templates` _[DAGNode](#dagnode) array_ | Templates are a list of DAG nodes. |
| `failureStrategy` _[FailureStrategy](#failurestrategy)_ | FailureStrategy is the strategy when a node in DAG fails. |


#### FailureStrategy

_Underlying type:_ `string`

FailureStrategy defines the failure strategy of DAGWorkflowTemplate.

_Appears in:_
- [DAGWorkflowTemplate](#dagworkflowtemplate)



#### GenericJobWorkflowTemplate



GenericJobWorkflowTemplate creates a t9k generic job.

_Appears in:_
- [WorkflowTemplateSpec](#workflowtemplatespec)

| Field | Description |
| --- | --- |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[GenericJobSpec](#genericjobspec)_ | Spec of the generic job. |


#### MPIJobWorkflowTemplate



MPIJobWorkflowTemplate creates a t9k mpi job.

_Appears in:_
- [WorkflowTemplateSpec](#workflowtemplatespec)

| Field | Description |
| --- | --- |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[MPIJobSpec](#mpijobspec)_ | Spec of the mpi job. |


#### NodePhase

_Underlying type:_ `string`

NodePhase is the current state of a node. Node means the node in a DAG. PodWorkflowTemplate, SeqPodWorkflowTemplate and ResourceWorkflowTemplate are also considered as an independent node. DAGWorkflowTemplate itself is considered as a parent node.

_Appears in:_
- [NodeStatus](#nodestatus)
- [WorkflowRunStatusFields](#workflowrunstatusfields)



#### NodeStatus



NodeStatus is the status of a node in DAG

_Appears in:_
- [WorkflowRunStatusFields](#workflowrunstatusfields)

| Field | Description |
| --- | --- |
| `workflowRunName` _string_ | WorkflowRunName is the name of WorkflowRun created from the node. |
| `phase` _[NodePhase](#nodephase)_ | Phase is the phase of the node. |
| `whenExpressions` _[WhenExpression](#whenexpression) array_ | WhenExpressions show why if the node is skipped. |


#### Param



Param declares a string to use for the parameter called name.

_Appears in:_
- [DAGNode](#dagnode)
- [WorkflowRunSpec](#workflowrunspec)

| Field | Description |
| --- | --- |
| `name` _string_ |  |
| `value` _string_ |  |


#### ParamSpec



ParamSpec defines values that are provided by users as inputs on a WorkflowRun.

_Appears in:_
- [WorkflowTemplateSpec](#workflowtemplatespec)

| Field | Description |
| --- | --- |
| `name` _string_ | Name declares the name by which a parameter is referenced. |
| `description` _string_ | Description is a user-facing description of the parameter that may be used to populate a UI. |
| `default` _string_ | Default is the value a parameter takes if no input value is supplied. If default is set, a WorkflowTemplate may be executed without a supplied value for the parameter. It serves as a pointer to distinguish between setting no default and setting empty string as default. |


#### PodSpecWithoutContainers



PodSpecWithoutContainers is a helper struct for SeqPodWorkflowTemplate forked from https://github.com/kubernetes/api/blob/v0.20.0/core/v1/types.go#L2914

_Appears in:_
- [SeqPodWorkflowTemplate](#seqpodworkflowtemplate)

| Field | Description |
| --- | --- |
| `volumes` _[Volume](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#volume-v1-core) array_ | List of volumes that can be mounted by containers belonging to the pod. More info: https://kubernetes.io/docs/concepts/storage/volumes |
| `initContainers` _[Container](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#container-v1-core) array_ | List of initialization containers belonging to the pod. Init containers are executed in order prior to containers being started. If any init container fails, the pod is considered to have failed and is handled according to its restartPolicy. The name for an init container or normal container must be unique among all containers. Init containers may not have Lifecycle actions, Readiness probes, Liveness probes, or Startup probes. The resourceRequirements of an init container are taken into account during scheduling by finding the highest request/limit for each resource type, and then using the max of of that value or the sum of the normal containers. Limits are applied to init containers in a similar fashion. Init containers cannot currently be added or removed. Cannot be updated. More info: https://kubernetes.io/docs/concepts/workloads/pods/init-containers/ |
| `ephemeralContainers` _[EphemeralContainer](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#ephemeralcontainer-v1-core) array_ | List of ephemeral containers run in this pod. Ephemeral containers may be run in an existing pod to perform user-initiated actions such as debugging. This list cannot be specified when creating a pod, and it cannot be modified by updating the pod spec. In order to add an ephemeral container to an existing pod, use the pod's ephemeralcontainers subresource. This field is alpha-level and is only honored by servers that enable the EphemeralContainers feature. |
| `restartPolicy` _[RestartPolicy](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#restartpolicy-v1-core)_ | Restart policy for all containers within the pod. One of Always, OnFailure, Never. Default to Always. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy |
| `terminationGracePeriodSeconds` _integer_ | Optional duration in seconds the pod needs to terminate gracefully. May be decreased in delete request. Value must be non-negative integer. The value zero indicates delete immediately. If this value is nil, the default grace period will be used instead. The grace period is the duration in seconds after the processes running in the pod are sent a termination signal and the time when the processes are forcibly halted with a kill signal. Set this value longer than the expected cleanup time for your process. Defaults to 30 seconds. |
| `activeDeadlineSeconds` _integer_ | Optional duration in seconds the pod may be active on the node relative to StartTime before the system will actively try to mark it failed and kill associated containers. Value must be a positive integer. |
| `dnsPolicy` _[DNSPolicy](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#dnspolicy-v1-core)_ | Set DNS policy for the pod. Defaults to "ClusterFirst". Valid values are 'ClusterFirstWithHostNet', 'ClusterFirst', 'Default' or 'None'. DNS parameters given in DNSConfig will be merged with the policy selected with DNSPolicy. To have DNS options set along with hostNetwork, you have to specify DNS policy explicitly to 'ClusterFirstWithHostNet'. |
| `nodeSelector` _object (keys:string, values:string)_ | NodeSelector is a selector which must be true for the pod to fit on a node. Selector which must match a node's labels for the pod to be scheduled on that node. More info: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/ |
| `serviceAccountName` _string_ | ServiceAccountName is the name of the ServiceAccount to use to run this pod. More info: https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/ |
| `serviceAccount` _string_ | DeprecatedServiceAccount is a depreciated alias for ServiceAccountName. Deprecated: Use serviceAccountName instead. |
| `automountServiceAccountToken` _boolean_ | AutomountServiceAccountToken indicates whether a service account token should be automatically mounted. |
| `nodeName` _string_ | NodeName is a request to schedule this pod onto a specific node. If it is non-empty, the scheduler simply schedules this pod onto that node, assuming that it fits resource requirements. |
| `hostNetwork` _boolean_ | Host networking requested for this pod. Use the host's network namespace. If this option is set, the ports that will be used must be specified. Default to false. |
| `hostPID` _boolean_ | Use the host's pid namespace. Optional: Default to false. |
| `hostIPC` _boolean_ | Use the host's ipc namespace. Optional: Default to false. |
| `shareProcessNamespace` _boolean_ | Share a single process namespace between all of the containers in a pod. When this is set containers will be able to view and signal processes from other containers in the same pod, and the first process in each container will not be assigned PID 1. HostPID and ShareProcessNamespace cannot both be set. Optional: Default to false. |
| `securityContext` _[PodSecurityContext](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podsecuritycontext-v1-core)_ | SecurityContext holds pod-level security attributes and common container settings. Optional: Defaults to empty.  See type description for default values of each field. |
| `imagePullSecrets` _[LocalObjectReference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#localobjectreference-v1-core) array_ | ImagePullSecrets is an optional list of references to secrets in the same namespace to use for pulling any of the images used by this PodSpec. If specified, these secrets will be passed to individual puller implementations for them to use. For example, in the case of docker, only DockerConfig type secrets are honored. More info: https://kubernetes.io/docs/concepts/containers/images#specifying-imagepullsecrets-on-a-pod |
| `hostname` _string_ | Specifies the hostname of the Pod If not specified, the pod's hostname will be set to a system-defined value. |
| `subdomain` _string_ | If specified, the fully qualified Pod hostname will be "<hostname>.<subdomain>.<pod namespace>.svc.<cluster domain>". If not specified, the pod will not have a domainname at all. |
| `affinity` _[Affinity](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#affinity-v1-core)_ | If specified, the pod's scheduling constraints |
| `schedulerName` _string_ | If specified, the pod will be dispatched by specified scheduler. If not specified, the pod will be dispatched by default scheduler. |
| `tolerations` _[Toleration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#toleration-v1-core) array_ | If specified, the pod's tolerations. |
| `hostAliases` _[HostAlias](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#hostalias-v1-core) array_ | HostAliases is an optional list of hosts and IPs that will be injected into the pod's hosts file if specified. This is only valid for non-hostNetwork pods. |
| `priorityClassName` _string_ | If specified, indicates the pod's priority. "system-node-critical" and "system-cluster-critical" are two special keywords which indicate the highest priorities with the former being the highest priority. Any other name must be defined by creating a PriorityClass object with that name. If not specified, the pod priority will be default or zero if there is no default. |
| `priority` _integer_ | The priority value. Various system components use this field to find the priority of the pod. When Priority Admission Controller is enabled, it prevents users from setting this field. The admission controller populates this field from PriorityClassName. The higher the value, the higher the priority. |
| `dnsConfig` _[PodDNSConfig](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#poddnsconfig-v1-core)_ | Specifies the DNS parameters of a pod. Parameters specified here will be merged to the generated DNS configuration based on DNSPolicy. |
| `readinessGates` _[PodReadinessGate](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podreadinessgate-v1-core) array_ | If specified, all readiness gates will be evaluated for pod readiness. A pod is ready when all its containers are ready AND all conditions specified in the readiness gates have status equal to "True" More info: https://git.k8s.io/enhancements/keps/sig-network/0007-pod-ready%2B%2B.md |
| `runtimeClassName` _string_ | RuntimeClassName refers to a RuntimeClass object in the node.k8s.io group, which should be used to run this pod.  If no RuntimeClass resource matches the named class, the pod will not be run. If unset or empty, the "legacy" RuntimeClass will be used, which is an implicit class with an empty definition that uses the default runtime handler. More info: https://git.k8s.io/enhancements/keps/sig-node/runtime-class.md This is a beta feature as of Kubernetes v1.14. |
| `enableServiceLinks` _boolean_ | EnableServiceLinks indicates whether information about services should be injected into pod's environment variables, matching the syntax of Docker links. Optional: Defaults to true. |
| `preemptionPolicy` _[PreemptionPolicy](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#preemptionpolicy-v1-core)_ | PreemptionPolicy is the Policy for preempting pods with lower priority. One of Never, PreemptLowerPriority. Defaults to PreemptLowerPriority if unset. This field is beta-level, gated by the NonPreemptingPriority feature-gate. |
| `overhead` _object (keys:[ResourceName](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#resourcename-v1-core), values:Quantity)_ | Overhead represents the resource overhead associated with running a pod for a given RuntimeClass. This field will be autopopulated at admission time by the RuntimeClass admission controller. If the RuntimeClass admission controller is enabled, overhead must not be set in Pod create requests. The RuntimeClass admission controller will reject Pod create requests which have the overhead already set. If RuntimeClass is configured and selected in the PodSpec, Overhead will be set to the value defined in the corresponding RuntimeClass, otherwise it will remain unset and treated as zero. More info: https://git.k8s.io/enhancements/keps/sig-node/20190226-pod-overhead.md This field is alpha-level as of Kubernetes v1.16, and is only honored by servers that enable the PodOverhead feature. |
| `topologySpreadConstraints` _[TopologySpreadConstraint](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#topologyspreadconstraint-v1-core) array_ | TopologySpreadConstraints describes how a group of pods ought to spread across topology domains. Scheduler will schedule pods in a way which abides by the constraints. All topologySpreadConstraints are ANDed. |
| `setHostnameAsFQDN` _boolean_ | If true the pod's hostname will be configured as the pod's FQDN, rather than the leaf name (the default). In Linux containers, this means setting the FQDN in the hostname field of the kernel (the nodename field of struct utsname). In Windows containers, this means setting the registry value of hostname for the registry key HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters to FQDN. If a pod does not have FQDN, this has no effect. Default to false. |


#### PodWorkflowTemplate



PodWorkflowTemplate creates a pod.

_Appears in:_
- [WorkflowTemplateSpec](#workflowtemplatespec)

| Field | Description |
| --- | --- |
| `PodSpec` _[PodSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podspec-v1-core)_ |  |


#### PyTorchTrainingJobWorkflowTemplate



PyTorchTrainingJobWorkflowTemplate creates a t9k pytorch training job.

_Appears in:_
- [WorkflowTemplateSpec](#workflowtemplatespec)

| Field | Description |
| --- | --- |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[PyTorchTrainingJobSpec](#pytorchtrainingjobspec)_ | Spec of the pytorch training job. |


#### ResourceWorkflowTemplate



ResourceWorkflowTemplate creates a k8s resource.

_Appears in:_
- [WorkflowTemplateSpec](#workflowtemplatespec)

| Field | Description |
| --- | --- |
| `successRules` _[Rules](#rules)_ | SuccessRules is an expression which describes the state of the k8s resource in which the task was considered succeeded. |
| `failureRules` _[Rules](#rules)_ | FailureRules is an expression which describes the state of the k8s resource in which the task was considered failed. |
| `manifest` _string_ | Manifest is the full spec of the k8s resource to create. |


#### Result



Result used to describe the results of a task

_Appears in:_
- [WorkflowTemplateSpec](#workflowtemplatespec)

| Field | Description |
| --- | --- |
| `name` _string_ | Name the given name |
| `description` _string_ | Description is a human-readable description of the result |
| `value` _string_ | Value is a expression to generate DAG result by combining node results Only required for DAG WorkflowTemplate |




#### Rules



Rules describe the state of the k8s resource.

_Appears in:_
- [ResourceWorkflowTemplate](#resourceworkflowtemplate)

| Field | Description |
| --- | --- |
| `fieldSelector` _string_ | FieldSelector selects k8s resources based on the value of one or more resource fields, examples: metadata.name=my-service metadata.namespace!=default status.phase!=Running,spec.restartPolicy=Always |
| `conditionSelector` _[ConditionSelector](#conditionselector)_ | ConditionSelector selects k8s resources based on <resource>.status.conditions. |


#### SchedulePolicy



SchedulePolicy defines how k8s schedules the WorkflowRun.

_Appears in:_
- [WorkflowRunSpec](#workflowrunspec)

| Field | Description |
| --- | --- |
| `t9kScheduler` _[T9kScheduler](#t9kscheduler)_ | T9k Scheduler. |


#### SeqPodWorkflowTemplate



SeqPodWorkflowTemplate creates a pod whose containers run sequentially. The spec of SeqPodWorkflowTemplate is almost the same with corev1.PodSpec, except that the field `Containers` is replaced by `Steps`, to emphasize the sequential execution pattern.

_Appears in:_
- [WorkflowTemplateSpec](#workflowtemplatespec)

| Field | Description |
| --- | --- |
| `PodSpecWithoutContainers` _[PodSpecWithoutContainers](#podspecwithoutcontainers)_ |  |
| `steps` _[Step](#step) array_ | Steps are the sequentially running containers of the SeqPodWorkflowTemplate |


#### Step



Step embeds the Container type, which allows it to include fields not provided by Container.

_Appears in:_
- [SeqPodWorkflowTemplate](#seqpodworkflowtemplate)

| Field | Description |
| --- | --- |
| `Container` _[Container](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#container-v1-core)_ |  |
| `script` _string_ | Script is the contents of an executable file to execute. If Script is not empty, the Step cannot have an Command and the Args will be passed to the Script. |


#### T9kScheduler



T9kScheduler provides additonal configurations needed for the scheduling process.

_Appears in:_
- [SchedulePolicy](#schedulepolicy)

| Field | Description |
| --- | --- |
| `queue` _string_ | Specifies the name of the queue should be used for running this workload. |


#### TensorFlowTrainingJobWorkflowTemplate



TensorFlowTrainingJobWorkflowTemplate creates a t9k training job.

_Appears in:_
- [WorkflowTemplateSpec](#workflowtemplatespec)

| Field | Description |
| --- | --- |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[TensorFlowTrainingJobSpec](#tensorflowtrainingjobspec)_ | Spec of the training job. |


#### WhenExpression



WhenExpression allows a node in DAG to declare expressions to be evaluated before the node is run to determine whether the node should be executed or skipped.

_Appears in:_
- [DAGNode](#dagnode)
- [NodeStatus](#nodestatus)

| Field | Description |
| --- | --- |
| `input` _string_ | Input is the string for guard checking which can be a static input or an output from a parent node |
| `operator` _Operator_ | Operator that represents an Input's relationship to the values |
| `values` _string array_ | Values is an array of strings, which is compared against the input, for guard checking It must be non-empty |




#### WorkflowRun



WorkflowRun is the Schema for the workflowrun API

_Appears in:_
- [WorkflowRunList](#workflowrunlist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/apis`
| `kind` _string_ | `WorkflowRun`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[WorkflowRunSpec](#workflowrunspec)_ |  |
| `status` _[WorkflowRunStatus](#workflowrunstatus)_ |  |


#### WorkflowRunCondition



WorkflowRunCondition is an observation of the condition of the WorkflowRun.

_Appears in:_
- [WorkflowRunStatusFields](#workflowrunstatusfields)

| Field | Description |
| --- | --- |
| `type` _[WorkflowRunConditionType](#workflowrunconditiontype)_ | Type of WorkflowRun condition. |
| `status` _[ConditionStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#conditionstatus-v1-core)_ | Status of the condition, one of True, False, or Unknown. |
| `reason` _string_ | The reason for the condition's last transition. |
| `message` _string_ | A readable message indicating details about the transition. |
| `lastTransitionTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta)_ | Last time the condition transitioned from one status to another. |


#### WorkflowRunConditionType

_Underlying type:_ `string`

WorkflowRunConditionType defines all possible types of WorkflowRunConditionType. Can be one of: Running, Completed.

_Appears in:_
- [WorkflowRunCondition](#workflowruncondition)



#### WorkflowRunList



WorkflowRunList contains a list of WorkflowRun



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/apis`
| `kind` _string_ | `WorkflowRunList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[WorkflowRun](#workflowrun) array_ |  |


#### WorkflowRunResult



WorkflowRunResult used to describe the results of a workflowTemplate

_Appears in:_
- [WorkflowRunStatusFields](#workflowrunstatusfields)

| Field | Description |
| --- | --- |
| `name` _string_ | Name the given name |
| `value` _string_ | Value the given value of the result |


#### WorkflowRunSpec



WorkflowRunSpec defines the desired state of WorkflowRun

_Appears in:_
- [WorkflowRun](#workflowrun)
- [WorkflowRunTemplateSpec](#workflowruntemplatespec)

| Field | Description |
| --- | --- |
| `workspaces` _[WorkspaceBinding](#workspacebinding) array_ | Workspaces is a list of mappings from volumes to workspace names that will be supplied to WorkflowTemplate. |
| `params` _[Param](#param) array_ | Params is a list of input parameters that will be supplied to WorkflowTemplate. |
| `serviceAccountName` _string_ | ServiceAccountName is the name of the service account that the created pod will use. |
| `workflowTemplateRef` _string_ | WorkflowTemplateRef is the name of the WorkflowTemplate that WorkflowRun will use. No more than one of the WorkflowTemplateRef and WorkflowTemplateSpec may be specified. |
| `workflowTemplateSpec` _[WorkflowTemplateSpec](#workflowtemplatespec)_ | WorkflowTemplateSpec is an embedded spec of WorkflowTemplate that WorkflowRun will use. No more than one of the WorkflowTemplateRef and WorkflowTemplateSpec may be specified. |
| `timeout` _[Duration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#duration-v1-meta)_ | Time after which the build times out. Defaults to never. Refer Go's ParseDuration documentation for expected format: https://golang.org/pkg/time/#ParseDuration |
| `depth` _integer_ | Depth indicates the depth of the WorkflowRun in DAG. If Depth exceeds limit, the WorkflowRun will not be created. |
| `scheduler` _[SchedulePolicy](#schedulepolicy)_ | Identifies the preferred scheduler for allocating resources to replicas. Defaults to cluster default scheduler. |


#### WorkflowRunStatus



WorkflowRunStatus defines the observed state of WorkflowRun

_Appears in:_
- [WorkflowRun](#workflowrun)

| Field | Description |
| --- | --- |
| `WorkflowRunStatusFields` _[WorkflowRunStatusFields](#workflowrunstatusfields)_ | WorkflowRunStatusFields inlines the status fields. |
| `retriedStatus` _[WorkflowRunStatusFields](#workflowrunstatusfields) array_ | RetriedStatus contains the history of WorkflowRunStatus in case of a retry in order to keep record of failures. |


#### WorkflowRunStatusFields



WorkflowRunStatusFields are the main fields of WorkflowRunStatus

_Appears in:_
- [WorkflowRunStatus](#workflowrunstatus)

| Field | Description |
| --- | --- |
| `phase` _[NodePhase](#nodephase)_ | Phase is a simple, high-level summary of where the WorkflowRun is in its lifecycle. |
| `message` _string_ | A human readable message indicating details about why the WorkflowRun is in this condition. |
| `nodes` _object (keys:string, values:[NodeStatus](#nodestatus))_ | Nodes is a map of DAG nodes status, with the node name as the key. |
| `startTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta)_ | StartTime is the time the build is actually started. |
| `completionTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta)_ | CompletionTime is the time the build completed. |
| `results` _[WorkflowRunResult](#workflowrunresult) array_ | Results are the list of results written out by the workflowTemplate's containers |
| `workflowTemplateSpec` _[WorkflowTemplateSpec](#workflowtemplatespec)_ | WorkflowTemplateSpec contains the Spec from the dereferenced WorkflowTemplate definition used to instantiate this WorkflowRun. |
| `podName` _string_ | PodName is the name of the pod created by WorkflowRun. |
| `conditions` _[WorkflowRunCondition](#workflowruncondition) array_ | The latest available observations of the WorkflowRun's current state. |


#### WorkflowRunTemplateSpec



WorkflowRunTemplateSpec describes the data a WorkflowRun should have when created from a template

_Appears in:_
- [CronWorkflowRunSpec](#cronworkflowrunspec)

| Field | Description |
| --- | --- |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[WorkflowRunSpec](#workflowrunspec)_ | Specification of the desired behavior of the WorkflowRun. |


#### WorkflowTemplate



WorkflowTemplate is the Schema for the WorkflowTemplate API

_Appears in:_
- [WorkflowTemplateList](#workflowtemplatelist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/apis`
| `kind` _string_ | `WorkflowTemplate`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[WorkflowTemplateSpec](#workflowtemplatespec)_ |  |
| `status` _[WorkflowTemplateStatus](#workflowtemplatestatus)_ |  |


#### WorkflowTemplateList



WorkflowTemplateList contains a list of WorkflowTemplate



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `batch.tensorstack.dev/apis`
| `kind` _string_ | `WorkflowTemplateList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[WorkflowTemplate](#workflowtemplate) array_ |  |


#### WorkflowTemplateSpec



WorkflowTemplateSpec defines the desired state of WorkflowTemplate.

_Appears in:_
- [WorkflowRunSpec](#workflowrunspec)
- [WorkflowRunStatusFields](#workflowrunstatusfields)
- [WorkflowTemplate](#workflowtemplate)

| Field | Description |
| --- | --- |
| `description` _string_ | Description is a user-facing description of the task that may be used to populate a UI. |
| `workspaces` _[WorkspaceDeclaration](#workspacedeclaration) array_ | Workspaces are the volumes that this WorkflowTemplate requires. Workspaces must be supplied as inputs in WorkflowRuns unless they are declared as optional. |
| `params` _[ParamSpec](#paramspec) array_ | Params is a list of input parameters required to run the task. Params must be supplied as inputs in WorkflowRuns unless they declare a default value. |
| `results` _[Result](#result) array_ | Results are values that this WorkflowTemplate can output |
| `type` _[WorkflowTemplateType](#workflowtemplatetype)_ | Type defines the type of WorkflowTemplate. If empty, the first non-nil field in (pod, seqPod, resource, dag) will be the type. |
| `pod` _[PodWorkflowTemplate](#podworkflowtemplate)_ | Pod is the spec of pod which WorkflowTemplate will create. |
| `seqPod` _[SeqPodWorkflowTemplate](#seqpodworkflowtemplate)_ | SeqPod is the spec of pod with sequentially running containers which WorkflowTemplate will create. |
| `resource` _[ResourceWorkflowTemplate](#resourceworkflowtemplate)_ | Resource is the spec of k8s resource which WorkflowTemplate will create. |
| `dag` _[DAGWorkflowTemplate](#dagworkflowtemplate)_ | DAG is the spec of DAG which WorkflowTemplate will create. |
| `genericJob` _[GenericJobWorkflowTemplate](#genericjobworkflowtemplate)_ | GenericJob is the spec of t9k generic job which WorkflowTemplate will create. |
| `tensorflowTrainingJob` _[TensorFlowTrainingJobWorkflowTemplate](#tensorflowtrainingjobworkflowtemplate)_ | TensorFlowTrainingJob is the spec of t9k training job which WorkflowTemplate will create. |
| `pytorchTrainingJob` _[PyTorchTrainingJobWorkflowTemplate](#pytorchtrainingjobworkflowtemplate)_ | PyTorchTrainingJob is the spec of t9k pytorch training job which WorkflowTemplate will create. |
| `xgboostTrainingJob` _[XGBoostTrainingJobWorkflowTemplate](#xgboosttrainingjobworkflowtemplate)_ | XGBoostTrainingJob is the spec of t9k xgboost training job which WorkflowTemplate will create. |
| `mpiJob` _[MPIJobWorkflowTemplate](#mpijobworkflowtemplate)_ | MPIJob is the spec of t9k mpi job which WorkflowTemplate will create. |
| `beamJob` _[BeamJobWorkflowTemplate](#beamjobworkflowtemplate)_ | BeamJob is the spec of t9k beam job which WorkflowTemplate will create. |




#### WorkflowTemplateType

_Underlying type:_ `string`

WorkflowTemplateType defines the type of WorkflowTemplate.

_Appears in:_
- [WorkflowTemplateSpec](#workflowtemplatespec)



#### WorkspaceBinding



WorkspaceBinding maps a WorkflowTemplate's declared workspace to a Volume.

_Appears in:_
- [WorkflowRunSpec](#workflowrunspec)

| Field | Description |
| --- | --- |
| `name` _string_ | Name is the name of the workspace populated by the volume. |
| `subPath` _string_ | SubPath is optionally a directory on the volume which should be used for this binding (i.e. the volume will be mounted at this sub directory). |
| `persistentVolumeClaim` _[PersistentVolumeClaimVolumeSource](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#persistentvolumeclaimvolumesource-v1-core)_ | PersistentVolumeClaimVolumeSource represents a reference to a PersistentVolumeClaim in the same namespace. Either this OR EmptyDir can be used. |
| `emptyDir` _[EmptyDirVolumeSource](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#emptydirvolumesource-v1-core)_ | EmptyDir represents a temporary directory that shares a WorkflowTemplate's lifetime. More info: https://kubernetes.io/docs/concepts/storage/volumes#emptydir Either this OR PersistentVolumeClaim can be used. |
| `configMap` _[ConfigMapVolumeSource](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#configmapvolumesource-v1-core)_ | ConfigMap represents a configMap that should populate this workspace. |
| `secret` _[SecretVolumeSource](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#secretvolumesource-v1-core)_ | Secret represents a secret that should populate this workspace. |


#### WorkspaceDAGBinding



WorkspaceDAGBinding describes how a workspace passed into a DAG WorkflowTemplate should be mapped to a node's declared workspace.

_Appears in:_
- [DAGNode](#dagnode)

| Field | Description |
| --- | --- |
| `name` _string_ | Name is the name of the workspace as declared by the node |
| `workspace` _string_ | Workspace is the name of the workspace declared by the DAG WorkflowTemplate |
| `subPath` _string_ | SubPath is optionally a directory on the volume which should be used for this binding (i.e. the volume will be mounted at this sub directory). |


#### WorkspaceDeclaration



WorkspaceDeclaration is a declaration of a volume that a WorkflowTemplate requires.

_Appears in:_
- [WorkflowTemplateSpec](#workflowtemplatespec)

| Field | Description |
| --- | --- |
| `name` _string_ | Name is the name by which you can bind the volume at runtime. |
| `description` _string_ | Description is an optional human readable description of this volume. |
| `mountPath` _string_ | MountPath overrides the directory that the volume will be made available at. |
| `readOnly` _boolean_ | ReadOnly dictates whether a mounted volume is writable. By default this field is false and so mounted volumes are writable. |
| `optional` _boolean_ | Optional marks a Workspace as not being required in WorkflowRuns. By default this field is false and so declared workspaces are required. |


#### XGBoostTrainingJobWorkflowTemplate



XGBoostTrainingJobWorkflowTemplate creates a t9k xgboost training job.

_Appears in:_
- [WorkflowTemplateSpec](#workflowtemplatespec)

| Field | Description |
| --- | --- |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[XGBoostTrainingJobSpec](#xgboosttrainingjobspec)_ | Spec of the xgboost training job. |


