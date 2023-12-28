# API Reference

## Packages
- [tensorstack.dev/v1beta1](#tensorstackdevv1beta1)


## tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the  v1beta1 API group

### Resource Types
- [Project](#project)
- [ProjectList](#projectlist)
- [QuotaProfile](#quotaprofile)
- [QuotaProfileList](#quotaprofilelist)



#### EventControllerStatus





_Appears in:_
- [ProjectStatus](#projectstatus)

| Field | Description |
| --- | --- |
| `deployment` _[EventDeploymentStatus](#eventdeploymentstatus)_ |  |


#### EventDeploymentStatus





_Appears in:_
- [EventControllerStatus](#eventcontrollerstatus)

| Field | Description |
| --- | --- |
| `name` _string_ |  |
| `readyReplicas` _integer_ |  |
| `podStatus` _[EventPodStatus](#eventpodstatus)_ |  |


#### EventPodStatus





_Appears in:_
- [EventDeploymentStatus](#eventdeploymentstatus)

| Field | Description |
| --- | --- |
| `name` _string_ |  |
| `uid` _UID_ |  |
| `phase` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podphase-v1-core">PodPhase</a>_ |  |


#### NetworkPolicy





_Appears in:_
- [ProjectSpec](#projectspec)

| Field | Description |
| --- | --- |
| `useDefaultTemplate` _boolean_ | If `true`, the default NetworkPolicy defined by the administrator will be applied. |
| `template` _[NetworkPolicyTemplate](#networkpolicytemplate)_ | A NethworkPolicy defined for this project. |


#### NetworkPolicyTemplate





_Appears in:_
- [NetworkPolicy](#networkpolicy)

| Field | Description |
| --- | --- |
| `spec` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#networkpolicyspec-v1-networking">NetworkPolicySpec</a>_ |  |


#### Project



Project is the Schema for the projects API

_Appears in:_
- [ProjectList](#projectlist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `Project`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta">ObjectMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[ProjectSpec](#projectspec)_ |  |
| `status` _[ProjectStatus](#projectstatus)_ |  |


#### ProjectCondition





_Appears in:_
- [ProjectStatus](#projectstatus)

| Field | Description |
| --- | --- |
| `type` _[ProjectConditionType](#projectconditiontype)_ | Type is the type of the condition. |
| `status` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#conditionstatus-v1-core">ConditionStatus</a>_ | Status is the status of the condition. Can be True, False, Unknown. |
| `lastUpdateTime` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta">Time</a>_ | Last time we probed the condition. |
| `lastTransitionTime` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta">Time</a>_ | Last time the condition transitioned from one status to another. |
| `reason` _string_ | Unique, one-word, CamelCase reason for the condition's last transition. |
| `message` _string_ | Human-readable message indicating details about last transition. |


#### ProjectConditionType

_Underlying type:_ `string`



_Appears in:_
- [ProjectCondition](#projectcondition)



#### ProjectList



ProjectList contains a list of Project



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `ProjectList`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta">ListMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[Project](#project) array_ |  |


#### ProjectSpec



ProjectSpec defines the desired state of Project

_Appears in:_
- [Project](#project)

| Field | Description |
| --- | --- |
| `resourceQuota` _[ResourceQuota](#resourcequota)_ |  |
| `networkPolicy` _[NetworkPolicy](#networkpolicy)_ |  |
| `quotaProfile` _string_ |  |
| `defaultScheduler` _[SchedulePolicy](#schedulepolicy)_ | DefaultScheduler defines the default scheduler and queue information for the project. It is just a configuration information, the controller does not need to do anything. |


#### ProjectStatus



ProjectStatus defines the observed state of Project

_Appears in:_
- [Project](#project)

| Field | Description |
| --- | --- |
| `conditions` _[ProjectCondition](#projectcondition) array_ |  |
| `eventController` _[EventControllerStatus](#eventcontrollerstatus)_ |  |
| `resourceQuota` _[ResourceQuotaStatus](#resourcequotastatus)_ |  |


#### QuotaProfile



QuotaProfile is the Schema for the quotaprofiles API. This API resource represents a template for project/namespace resource quota  specifications, defined as an instance of `corev1.ResourceQuotaSpec`.

_Appears in:_
- [QuotaProfileList](#quotaprofilelist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `QuotaProfile`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta">ObjectMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#resourcequotaspec-v1-core">ResourceQuotaSpec</a>_ |  |


#### QuotaProfileList



QuotaProfileList contains a list of QuotaProfile



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `QuotaProfileList`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta">ListMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[QuotaProfile](#quotaprofile) array_ |  |


#### ResourceQuota





_Appears in:_
- [ProjectSpec](#projectspec)

| Field | Description |
| --- | --- |
| `template` _[ResourceQuotaTemplate](#resourcequotatemplate)_ | A `corev1.ResourceQuota` defined for this project. |


#### ResourceQuotaStatus





_Appears in:_
- [ProjectStatus](#projectstatus)

| Field | Description |
| --- | --- |
| `name` _string_ |  |
| `ResourceQuotaStatus` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#resourcequotastatus-v1-core">ResourceQuotaStatus</a>_ |  |


#### ResourceQuotaTemplate





_Appears in:_
- [ResourceQuota](#resourcequota)

| Field | Description |
| --- | --- |
| `spec` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#resourcequotaspec-v1-core">ResourceQuotaSpec</a>_ |  |


#### SchedulePolicy



SchedulePolicy specifies preferences for resource allocation requests, including the name of the preferred scheduler and additional configuration parameters.

_Appears in:_
- [ProjectSpec](#projectspec)

| Field | Description |
| --- | --- |
| `t9kScheduler` _[T9kScheduler](#t9kscheduler)_ |  |


#### T9kScheduler





_Appears in:_
- [SchedulePolicy](#schedulepolicy)

| Field | Description |
| --- | --- |
| `queue` _string_ | Name of the resource `Queue` of a `T9kScheduler`. |


