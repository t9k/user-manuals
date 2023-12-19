# API Reference

## Packages
- [scheduler.tensorstack.dev/v1beta1](#schedulertensorstackdevv1beta1)


## scheduler.tensorstack.dev/v1beta1

Package v1beta1 is the v1beta1 version of the API.

### Resource Types
- [PodGroup](#podgroup)
- [PodGroupList](#podgrouplist)
- [Queue](#queue)
- [QueueList](#queuelist)



#### PodGroup



PodGroup represents a collection of Pods to be scheduled together to facilicate with parallel computing. PodGroup is usually automatically created by workload controllers to manage parallel batch workloads such as machine learning training and to enable coscheduling/gang-scheduling strategies. Users can also manually create a PodGroup and associates Pods with it if desired.

_Appears in:_
- [PodGroupList](#podgrouplist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `scheduler.tensorstack.dev/v1beta1`
| `kind` _string_ | `PodGroup`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[PodGroupSpec](#podgroupspec)_ | Specification of the desired behavior of the pod group. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#spec-and-status |
| `status` _[PodGroupStatus](#podgroupstatus)_ | Status represents the current status of a pod group. This data may not be up to date. |


#### PodGroupCondition



PodGroupCondition contains details for the current state of this pod group.

_Appears in:_
- [PodGroupStatus](#podgroupstatus)

| Field | Description |
| --- | --- |
| `type` _PodGroupConditionType_ | The type of the condition. |
| `status` _[ConditionStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#conditionstatus-v1-core)_ | The status of the condition. |
| `transitionID` _string_ | The ID of condition transition. |
| `lastTransitionTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta)_ | Last time of condition transition(s). |
| `reason` _string_ | Unique, one-word, CamelCase, machine-readable reason for the condition's last change. |
| `message` _string_ | Human-readable message indicating details about last change. |


#### PodGroupInQueueStatus





_Appears in:_
- [QueueStatus](#queuestatus)

| Field | Description |
| --- | --- |
| `total` _integer_ |  |


#### PodGroupList



PodGroupList is a collection of pod groups.



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `scheduler.tensorstack.dev/v1beta1`
| `kind` _string_ | `PodGroupList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[PodGroup](#podgroup) array_ | The list of PodGroup. |


#### PodGroupSpec



PodGroupSpec represents the desired specification of a pod group.

_Appears in:_
- [PodGroup](#podgroup)

| Field | Description |
| --- | --- |
| `roles` _[Role](#role) array_ |  |
| `minMember` _integer_ | MinMember defines the minimal number of pods to run the PodGroup. If there less than `minMember` of pods joining the PodGroup, none of the existing pods in the group will be scheduled. After `minMember` of pods joined, the scheduler will only schedule them if there are sufficient resources to allow `minMember` of pods start together. |
| `queue` _string_ | Queue defines the queue from which resources for pods of the PodGroup should be allocated. If queue is not specified, the PodGroup will be scheduled to queue "default". |
| `priority` _integer_ | If specified, indicates the PodGroup's priority; groups with larger `priority` values will be considered for scheduling first; range is [0,100]. |
| `topologyPolicy` _TopologyPolicyType_ | TopologyPolicy declares the topology policy PodGroup needs. |


#### PodGroupStatus



PodGroupStatus represents the current state of a pod group.

_Appears in:_
- [PodGroup](#podgroup)

| Field | Description |
| --- | --- |
| `conditions` _[PodGroupCondition](#podgroupcondition) array_ | The conditions of PodGroup. |
| `allocated` _object (keys:[ResourceName](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#resourcename-v1-core), values:Quantity)_ | Allocated represents resources and their qunatities allocated to the PodGroup. |
| `pending` _integer_ | The number of pods in phase Pending. |
| `running` _integer_ | The number of pods in phase running. |
| `succeeded` _integer_ | The number of pods in phase Succeeded. |
| `failed` _integer_ | The number of pods in phase Failed. |
| `unknown` _integer_ | The number of pods in phase Unknown. |


#### PodInQueueStatus





_Appears in:_
- [QueueStatus](#queuestatus)

| Field | Description |
| --- | --- |
| `pending` _integer_ | The number of 'Pending' Pods in this queue. |
| `running` _integer_ | The number of 'Running' Pods in this queue. |
| `succeeded` _integer_ | The number of 'Succeeded' Pods in this queue. |
| `failed` _integer_ | The number of 'Failed' Pods in this queue |
| `unknown` _integer_ | The number of 'Unknown' Pods in this queue. |


#### Queue



Queue is an API-resource to reprenent a sub-set of cluster compute resources and associated administrative policies, such as allowed users, resource quota, allowed workload types, max duration of workload runtime and etc.

_Appears in:_
- [QueueList](#queuelist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `scheduler.tensorstack.dev/v1beta1`
| `kind` _string_ | `Queue`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[QueueSpec](#queuespec)_ | Specification of the desired behavior of the queue. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#spec-and-status |
| `status` _[QueueStatus](#queuestatus)_ | The status of queue. |


#### QueueCondition





_Appears in:_
- [QueueStatus](#queuestatus)

| Field | Description |
| --- | --- |
| `type` _[QueueConditionType](#queueconditiontype)_ | Type is the type of the condition. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#pod-conditions |
| `status` _[ConditionStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#conditionstatus-v1-core)_ | Status is the status of the condition. Can be True, False, Unknown. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#pod-conditions |
| `lastTransitionTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta)_ | Last time the condition transitioned. |
| `reason` _string_ | Unique, one-word, CamelCase reason for the condition's last transition. |
| `message` _string_ | Human-readable message indicating details about last transition. |


#### QueueConditionType

_Underlying type:_ `string`



_Appears in:_
- [QueueCondition](#queuecondition)



#### QueueList



QueueList is a collection of queues.



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `scheduler.tensorstack.dev/v1beta1`
| `kind` _string_ | `QueueList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[Queue](#queue) array_ | The list of Queue. |


#### QueueSpec



QueueSpec represents the desired specification of a Queue.

_Appears in:_
- [Queue](#queue)

| Field | Description |
| --- | --- |
| `quota` _[QuotaRequirements](#quotarequirements)_ |  |
| `priority` _integer_ | If specified, indicates the Queue's priority. range is [0,100] The higher value of `priority`, workloads in this queue will be scheduled with resources with higher preferences. |
| `preemptible` _boolean_ | Preemptible indicate whether the queue can be preempted by other queue when cluster resources are in short. Queue can be preempted if Preemptible is not set. |
| `closed` _boolean_ | After queue is closed, new workloads (pods) will not be allocated with resources and no new workloads will be accepted either. |
| `nodeSelector` _[LabelSelector](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#labelselector-v1-meta)_ | NodeSelector specifies the nodes whoses resource can be used by a Queue. This provides a machanism to restrict workloads submitted to a particular queue to a sub-set of nodes in the cluster. if `nil`, all nodes are eligible. |
| `namespaceSelector` _[LabelSelector](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#labelselector-v1-meta)_ | NamespaceSelector specifies the set of namespaces from which workloads are allowed to use this Queue. if `nil`,  no namespaces are selected. Note: There may be other authorization procedures that permit workloads in a queue. They are OR'ed with this selector. |


#### QueueStatus



QueueStatus represents the status of Queue.

_Appears in:_
- [Queue](#queue)

| Field | Description |
| --- | --- |
| `allocated` _object (keys:[ResourceName](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#resourcename-v1-core), values:Quantity)_ | Count of resource allocated to the queue. |
| `conditions` _[QueueCondition](#queuecondition) array_ | Current service state of Queue. |
| `podGroups` _[PodGroupInQueueStatus](#podgroupinqueuestatus)_ | PodGroup Status in Queue. |
| `pods` _[PodInQueueStatus](#podinqueuestatus)_ | Pod Status in Queue. |


#### QuotaRequirements





_Appears in:_
- [QueueSpec](#queuespec)

| Field | Description |
| --- | --- |
| `requests` _object (keys:[ResourceName](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#resourcename-v1-core), values:Quantity)_ | Requests describes max amount of resources pods in the Queue can potentially request. However, these are the upper limits for resources, not necessarily always available for use. This can be used by cluster administrators to control the upper bounds of resources submitted to a particular queue. Togethe with allowed users of queues, this provides a mechanism for admins to set policies to constrain some aspects of user resource usages. |


#### Role



Role describes pod's role and minMember constraint for this role.

_Appears in:_
- [PodGroupSpec](#podgroupspec)

| Field | Description |
| --- | --- |
| `name` _string_ | Role Name |
| `minMember` _integer_ | MinMember defines minimal number of pods of the role. |


