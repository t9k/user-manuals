# API Reference

## Packages
- [tensorstack.dev/v1beta1](#tensorstackdevv1beta1)


## tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the  v1beta1 API group

### Resource Types
- [MLService](#mlservice)
- [MLServiceList](#mlservicelist)
- [MLServiceRuntime](#mlserviceruntime)
- [MLServiceRuntimeList](#mlserviceruntimelist)



#### AddressStatus



AddressStatus store state of serving address

_Appears in:_
- [MLServiceStatus](#mlservicestatus)

| Field | Description |
| --- | --- |
| `url` _string_ | URL used for predictor. |


#### ContainerResources





_Appears in:_
- [PredictorSpec](#predictorspec)

| Field | Description |
| --- | --- |
| `name` _string_ | Name of container |
| `resources` _[ResourceRequirements](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#resourcerequirements-v1-core)_ | Resource requirements |


#### DeploymentSpec



DeploymentSpec defines the configuration for knative service

_Appears in:_
- [PredictorSpec](#predictorspec)
- [TransformerSpec](#transformerspec)

| Field | Description |
| --- | --- |
| `minReplicas` _integer_ | Minimum number of replicas, pods won't scale down to 0 in case of no traffic |
| `maxReplicas` _integer_ | This is the up bound for autoscaler to scale to |
| `template` _[PatchTemplateSpec](#patchtemplatespec)_ | Custom template of knative service |
| `logger` _[LoggerSpec](#loggerspec)_ | Logger spec |


#### EditableMetadata



Metadata includes the editable part of metav1.ObjectMeta. Now only contains labels and annotations

_Appears in:_
- [PatchTemplateSpec](#patchtemplatespec)
- [RuntimeTemplateSpec](#runtimetemplatespec)

| Field | Description |
| --- | --- |
| `labels` _object (keys:string, values:string)_ | Labels |
| `annotations` _object (keys:string, values:string)_ | Annotations |


#### LoggerMode

_Underlying type:_ `string`



_Appears in:_
- [LoggerSpec](#loggerspec)



#### LoggerSpec





_Appears in:_
- [DeploymentSpec](#deploymentspec)

| Field | Description |
| --- | --- |
| `urls` _string array_ | Logger sink url array |
| `mode` _[LoggerMode](#loggermode)_ | Logger mode |
| `resources` _[ResourceRequirements](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#resourcerequirements-v1-core)_ | Resource requirements |


#### MLService



MLService is the Schema for the mlservices API

_Appears in:_
- [MLServiceList](#mlservicelist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `MLService`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[MLServiceSpec](#mlservicespec)_ |  |
| `status` _[MLServiceStatus](#mlservicestatus)_ |  |


#### MLServiceCondition





_Appears in:_
- [MLServiceStatus](#mlservicestatus)

| Field | Description |
| --- | --- |
| `type` _[MLServiceConditionType](#mlserviceconditiontype)_ | Type of condition. |
| `status` _[ConditionStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#conditionstatus-v1-core)_ | Status of the condition, one of True, False, Unknown. |
| `lastTransitionTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta)_ | Last time the condition transitioned from one status to another. |
| `reason` _string_ | The reason for the condition's last transition. |
| `message` _string_ | A human readable message indicating details about the transition. |


#### MLServiceConditionType

_Underlying type:_ `string`



_Appears in:_
- [MLServiceCondition](#mlservicecondition)



#### MLServiceList



MLServiceList contains a list of MLService



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `MLServiceList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[MLService](#mlservice) array_ |  |


#### MLServiceRuntime



MLServiceRuntime is the Schema for the mlserviceruntimes API

_Appears in:_
- [MLServiceRuntimeList](#mlserviceruntimelist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `MLServiceRuntime`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[MLServiceRuntimeSpec](#mlserviceruntimespec)_ |  |
| `status` _[MLServiceRuntimeStatus](#mlserviceruntimestatus)_ |  |


#### MLServiceRuntimeList



MLServiceRuntimeList contains a list of MLServiceRuntime



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `MLServiceRuntimeList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[MLServiceRuntime](#mlserviceruntime) array_ |  |


#### MLServiceRuntimeSpec





_Appears in:_
- [MLServiceRuntime](#mlserviceruntime)

| Field | Description |
| --- | --- |
| `enabled` _boolean_ | Set true if enabled |
| `template` _[RuntimeTemplateSpec](#runtimetemplatespec)_ | Template defines the knative revision that will be created from this pod template. |




#### MLServiceSpec



MLServiceSpec defines the desired state of MLService

_Appears in:_
- [MLService](#mlservice)

| Field | Description |
| --- | --- |
| `releases` _[ReleaseSpec](#releasespec) array_ | Releases define multiple versions of predictor |
| `transformer` _[TransformerSpec](#transformerspec)_ | Transformer will pre-process and post-process data |
| `default` _string_ | Default specifies the release name which will be used as default version. |
| `canary` _string_ | Canary specifies the release name which will be used as canary version. |
| `canaryTrafficPercent` _integer_ | CanaryTrafficPercent specifies traffic percent of canary version, range is (0,100). |
| `scheduler` _[SchedulePolicy](#schedulepolicy)_ | Default Scheduler is default-scheduler |
| `runMode` _[RunMode](#runmode)_ | MLService RunMode |


#### MLServiceStatus



MLServiceStatus defines the observed state of MLService

_Appears in:_
- [MLService](#mlservice)

| Field | Description |
| --- | --- |
| `defaultRelease` _string_ | Default release name |
| `canaryRelease` _string_ | Canary release name |
| `conditions` _[MLServiceCondition](#mlservicecondition) array_ | Conditions |
| `releases` _[ReleaseStatus](#releasestatus) array_ | The observed statuses of MLService releases |
| `transformer` _[TransformerStatus](#transformerstatus)_ | The observed statuses of transformers. |
| `address` _[AddressStatus](#addressstatus)_ | Address |


#### ModelSpec





_Appears in:_
- [PredictorSpec](#predictorspec)

| Field | Description |
| --- | --- |
| `parameters` _object (keys:string, values:string)_ | Model parameters |
| `runtime` _string_ | Specific ServingRuntime name to use for deployment. |


#### PVCStorage



PVCStorage defines infos of pvc

_Appears in:_
- [Storage](#storage)

| Field | Description |
| --- | --- |
| `name` _string_ | PVC name |
| `subPath` _string_ | Directory path where model is located in PVC. Must be a relative path. e.g. "model/mnist" Defaults to "" (volume's root). |
| `mountPath` _string_ | Directory path where model locates in container, default is "/var/lib/t9k/model" |


#### PatchTemplateSpec



podSpec and containers are optional. This will be patched to runtime

_Appears in:_
- [DeploymentSpec](#deploymentspec)

| Field | Description |
| --- | --- |
| `metadata` _[EditableMetadata](#editablemetadata)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[PodSpec](#podspec)_ | Pod Spec with optional containers |


#### PodSpec



PodSpec is a description of a pod.

_Appears in:_
- [PatchTemplateSpec](#patchtemplatespec)

| Field | Description |
| --- | --- |
| `volumes` _[Volume](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#volume-v1-core) array_ | List of volumes that can be mounted by containers belonging to the pod. More info: https://kubernetes.io/docs/concepts/storage/volumes |
| `initContainers` _[Container](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#container-v1-core) array_ | List of initialization containers belonging to the pod. Init containers are executed in order prior to containers being started. If any init container fails, the pod is considered to have failed and is handled according to its restartPolicy. The name for an init container or normal container must be unique among all containers. Init containers may not have Lifecycle actions, Readiness probes, Liveness probes, or Startup probes. The resourceRequirements of an init container are taken into account during scheduling by finding the highest request/limit for each resource type, and then using the max of of that value or the sum of the normal containers. Limits are applied to init containers in a similar fashion. Init containers cannot currently be added or removed. Cannot be updated. More info: https://kubernetes.io/docs/concepts/workloads/pods/init-containers/ |
| `containers` _[Container](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#container-v1-core) array_ | List of containers belonging to the pod. Containers cannot currently be added or removed. There must be at least one container in a Pod. Cannot be updated. |
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


#### PredictorSpec



PredictorSpec defines the configuration for a predictor, The following fields follow a "1-of" semantic. Users must specify exactly one spec.

_Appears in:_
- [ReleaseSpec](#releasespec)

| Field | Description |
| --- | --- |
| `model` _[ModelSpec](#modelspec)_ | Model info |
| `storage` _[Storage](#storage)_ | Model storage spec |
| `DeploymentSpec` _[DeploymentSpec](#deploymentspec)_ | Model deploy spec |
| `containersResources` _[ContainerResources](#containerresources) array_ | Container's resources |


#### ReleaseSpec



ReleaseSpec defines the specific spec of release

_Appears in:_
- [MLServiceSpec](#mlservicespec)

| Field | Description |
| --- | --- |
| `name` _string_ | Name is the release name |
| `predictor` _[PredictorSpec](#predictorspec)_ | Predictor defines the model serving spec |


#### ReleaseStatus



ReleaseStatus defines the observed status of one MLService release

_Appears in:_
- [MLServiceStatus](#mlservicestatus)

| Field | Description |
| --- | --- |
| `name` _string_ | Release name |
| `ready` _boolean_ | True if release service ready |
| `trafficPercent` _integer_ | Traffic percent of this release |
| `url` _string_ | Service url |
| `reason` _string_ | Reason for not ready, empty if ready |
| `message` _string_ | Message for not ready, empty if ready |
| `readyReplicas` _integer_ | Ready replicas numbers |
| `totalReplicas` _integer_ | Total replicas numbers |


#### RunMode

_Underlying type:_ `string`



_Appears in:_
- [MLServiceSpec](#mlservicespec)



#### RuntimeTemplateSpec



this will be applied to RevisionTemplateSpec

_Appears in:_
- [MLServiceRuntimeSpec](#mlserviceruntimespec)

| Field | Description |
| --- | --- |
| `metadata` _[EditableMetadata](#editablemetadata)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[PodSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podspec-v1-core)_ | Pod Spec with optional containers |


#### S3Storage



S3Storage defines infos of s3

_Appears in:_
- [Storage](#storage)

| Field | Description |
| --- | --- |
| `secretRef` _[LocalObjectReference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#localobjectreference-v1-core)_ | SecretRef is reference to the secret storing s3cmd config |
| `uri` _string_ | Directory path where model locates in s3. e.g. `"s3://<bucket>/<dir>/"` |
| `mountPath` _string_ | Directory path where model locates in container, default is "/var/lib/t9k/model" |


#### SchedulePolicy



SchedulePolicy defines how k8s to schedule the replicas.

_Appears in:_
- [MLServiceSpec](#mlservicespec)

| Field | Description |
| --- | --- |
| `t9kScheduler` _[T9kScheduler](#t9kscheduler)_ | TensorStack scheduler spec |


#### Storage



Storage defines the storage where the model locates

_Appears in:_
- [PredictorSpec](#predictorspec)
- [TransformerSpec](#transformerspec)

| Field | Description |
| --- | --- |
| `s3` _[S3Storage](#s3storage)_ | Model locates in S3 |
| `pvc` _[PVCStorage](#pvcstorage)_ | Model locates in pvc |


#### T9kScheduler





_Appears in:_
- [SchedulePolicy](#schedulepolicy)

| Field | Description |
| --- | --- |
| `queue` _string_ | Queue name |


#### TransformerSpec



TransformerSpec defines the transformer

_Appears in:_
- [MLServiceSpec](#mlservicespec)

| Field | Description |
| --- | --- |
| `DeploymentSpec` _[DeploymentSpec](#deploymentspec)_ | Transformer deployment spec |
| `storage` _[Storage](#storage)_ | Transformer model storage spec |


#### TransformerStatus



TransformerStatus defines the observed status of transformer

_Appears in:_
- [MLServiceStatus](#mlservicestatus)

| Field | Description |
| --- | --- |
| `ready` _boolean_ | True if transformer service ready |
| `url` _string_ | Transformer url |
| `reason` _string_ | Reason for not ready, empty if ready |
| `message` _string_ | Message for not ready, empty if ready |
| `readyReplicas` _integer_ | Ready replicas numbers |
| `totalReplicas` _integer_ | Total replicas numbers |


