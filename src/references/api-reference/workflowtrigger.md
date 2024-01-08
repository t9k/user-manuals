# API Reference

## Packages
- [tensorstack.dev/v1beta1](#tensorstackdevv1beta1)


## tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the  v1beta1 API group

### Resource Types
- [EventListener](#eventlistener)
- [EventListenerList](#eventlistenerlist)
- [WorkflowTrigger](#workflowtrigger)
- [WorkflowTriggerList](#workflowtriggerlist)



#### Condition



Condition contains details about resource state

_Appears in:_
- [EventListenerStatus](#eventlistenerstatus)
- [WorkflowTriggerStatus](#workflowtriggerstatus)

| Field | Description |
| --- | --- |
| `type` _[ConditionType](#conditiontype)_ | Condition type. |
| `status` _[ConditionStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#conditionstatus-v1-core)_ | Condition status, True, False or Unknown. |
| `lastTransitionTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta)_ | Last time the condition transitioned from one status to another. |
| `message` _string_ | Human-readable message indicating details about last transition. |


#### ConditionType

_Underlying type:_ `string`

ConditionType is a valid value of Condition.Type

_Appears in:_
- [Condition](#condition)



#### EventListener



EventListener is the Schema for the eventlisteners API

_Appears in:_
- [EventListenerList](#eventlistenerlist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `EventListener`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[EventListenerSpec](#eventlistenerspec)_ |  |
| `status` _[EventListenerStatus](#eventlistenerstatus)_ |  |


#### EventListenerAddress



The access address for in-cluster and out-cluster

_Appears in:_
- [EventListenerStatus](#eventlistenerstatus)

| Field | Description |
| --- | --- |
| `url` _string_ | The access address for out-cluster |
| `inClusterURL` _string_ | The access address for in-cluster |


#### EventListenerList



EventListenerList contains a list of EventListener



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `EventListenerList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[EventListener](#eventlistener) array_ |  |


#### EventListenerSpec



EventListenerSpec defines the desired state of EventListener

_Appears in:_
- [EventListener](#eventlistener)

| Field | Description |
| --- | --- |
| `replicas` _integer_ | Number of desired pods. This is a pointer to distinguish between explicit zero and not specified. Defaults to 1. |
| `resources` _[ResourceRequirements](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#resourcerequirements-v1-core)_ | Compute Resources required by this container. Cannot be updated. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |


#### EventListenerStatus



EventListenerStatus defines the observed state of EventListener

_Appears in:_
- [EventListener](#eventlistener)

| Field | Description |
| --- | --- |
| `address` _[EventListenerAddress](#eventlisteneraddress)_ | The access address for in-cluster and out-cluster |
| `conditions` _[Condition](#condition) array_ | Represents the latest available observations of a eventListener's current state. |


#### EventSource



The source that events come from.

_Appears in:_
- [WorkflowTriggerSpec](#workflowtriggerspec)

| Field | Description |
| --- | --- |
| `eventListenerName` _string_ | Name of an existing EventListener. |
| `filters` _[Filter](#filter) array_ | List of filters to filter events from the EventListener. |


#### Filter



Filter defines how to filter events from the EventListener.

_Appears in:_
- [EventSource](#eventsource)

| Field | Description |
| --- | --- |
| `path` _string_ | Path is the JSONPath of the event's (JSON decoded) data key Path is a series of keys separated by a dot. A key may contain wildcard characters '*' and '?'. To access an array value use the index as the key. The dot and wildcard characters can be escaped with '\\'. See https://github.com/tidwall/gjson#path-syntax for more information on how to use this. |
| `type` _[JSONType](#jsontype)_ | Type contains the JSON type of the data |
| `values` _string array_ | Values is the allowed string values for this key Booleans are passed using strconv.ParseBool() Numbers are parsed using as float64 using strconv.ParseFloat() Strings are taken as is Nils this value is ignored |


#### JSONType

_Underlying type:_ `string`

JSONType contains the supported JSON types for data filtering

_Appears in:_
- [Filter](#filter)



#### WorkflowTrigger



WorkflowTrigger is the Schema for the workflowtriggers API

_Appears in:_
- [WorkflowTriggerList](#workflowtriggerlist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `WorkflowTrigger`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[WorkflowTriggerSpec](#workflowtriggerspec)_ |  |
| `status` _[WorkflowTriggerStatus](#workflowtriggerstatus)_ |  |


#### WorkflowTriggerList



WorkflowTriggerList contains a list of WorkflowTrigger



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `WorkflowTriggerList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[WorkflowTrigger](#workflowtrigger) array_ |  |


#### WorkflowTriggerSpec



WorkflowTriggerSpec defines the desired state of WorkflowTrigger

_Appears in:_
- [WorkflowTrigger](#workflowtrigger)

| Field | Description |
| --- | --- |
| `replicas` _integer_ | Number of desired pods. This is a pointer to distinguish between explicit zero and not specified. Defaults to 1. |
| `eventSources` _[EventSource](#eventsource) array_ | List of sources that events come from. |
| `serviceAccountName` _string_ | Name of a service account used by WorkflowTrigger to create WorkflowRuns. |
| `resources` _[ResourceRequirements](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#resourcerequirements-v1-core)_ | Compute Resources required by this container. Cannot be updated. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| `workflowRunSpec` _WorkflowRunSpec_ | Spec of WorkflowRun to be created by WorkflowTrigger. |


#### WorkflowTriggerStatus



WorkflowTriggerStatus defines the observed state of WorkflowTrigger

_Appears in:_
- [WorkflowTrigger](#workflowtrigger)

| Field | Description |
| --- | --- |
| `conditions` _[Condition](#condition) array_ | Represents the latest available observations of a eventListener's current state. |


