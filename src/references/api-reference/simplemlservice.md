# API Reference

## Packages
- [tensorstack.dev/v1beta1](#tensorstackdevv1beta1)


## tensorstack.dev/v1beta1

Package v1beta1 defines the CRD types.
This file specifies the group of CRD resource. It is required by controller-gen.
Details: https://github.com/kubernetes-sigs/kubebuilder/blob/v2.0.0-alpha.4/designs/simplified-scaffolding.md#example

### Resource Types
- [SimpleMLService](#simplemlservice)
- [SimpleMLServiceList](#simplemlservicelist)



#### Address





_Appears in:_
- [SimpleMLServiceStatus](#simplemlservicestatus)

| Field | Description |
| --- | --- |
| `dns` _string_ | the service's in-cluster dns, e.g. managed-simplemlservice-41309.demo.svc.cluster.local |
| `ports` _[AddressPort](#addressport) array_ | an array of serivce port & protocol |


#### AddressPort





_Appears in:_
- [Address](#address)

| Field | Description |
| --- | --- |
| `port` _integer_ |  |
| `nodePort` _integer_ |  |
| `protocol` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#protocol-v1-core">Protocol</a>_ | default is TCP |


#### Condition



Condition for simpleMLService

_Appears in:_
- [SimpleMLServiceStatus](#simplemlservicestatus)

| Field | Description |
| --- | --- |
| `lastTransitionTime` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta">Time</a>_ |  |
| `type` _[SimpleMLServiceConditionType](#simplemlserviceconditiontype)_ |  |
| `status` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#conditionstatus-v1-core">ConditionStatus</a>_ |  |
| `reason` _string_ |  |
| `message` _string_ |  |


#### CustomSpec



CustomSpec defines a pod template to run model serving

_Appears in:_
- [SimpleMLServiceSpec](#simplemlservicespec)

| Field | Description |
| --- | --- |
| `spec` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podspec-v1-core">PodSpec</a>_ |  |


#### DeploymentSpec



DeploymentSpec defines the configuration for replicas & scheduler

_Appears in:_
- [SimpleMLServiceSpec](#simplemlservicespec)

| Field | Description |
| --- | --- |
| `scheduler` _[SchedulePolicy](#schedulepolicy)_ | Scheduler responsible for handling resource allocation requests. default is default-scheduler |
| `replicas` _integer_ | Replicas of pods running model serving |
| `strategy` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#deploymentstrategy-v1-apps">DeploymentStrategy</a>_ | The deployment strategy to use to replace existing pods with new ones |


#### PVCStorage



PVCStorage defines infos of pvc

_Appears in:_
- [Storage](#storage)

| Field | Description |
| --- | --- |
| `name` _string_ | PVC name |
| `subPath` _string_ | Directory path where model is located in PVC. Must be a relative path. e.g. "model/mnist" |
| `containerPath` _string_ | Directory path where model locates in container. Must be absolute path, default is "/var/lib/t9k/model" |


#### PyTorchSpec



PyTorchSpec defines arguments for configuring PyTorch model serving

_Appears in:_
- [SimpleMLServiceSpec](#simplemlservicespec)

| Field | Description |
| --- | --- |
| `modelsFlag` _string_ | Value of torchserve's flag --models |
| `image` _string_ | Image of torchserve |
| `resources` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#resourcerequirements-v1-core">ResourceRequirements</a>_ | Compute Resources required by a replica |


#### S3Storage



S3Storage defines infos of s3

_Appears in:_
- [Storage](#storage)

| Field | Description |
| --- | --- |
| `secretName` _string_ | Name of secret storing s3cmd config |
| `uri` _string_ | Directory path where model locates in s3. e.g. "s3://<bucket>/<dir>/" |
| `containerPath` _string_ | Directory path where model locates in container, default is "/var/lib/t9k/model" |


#### SchedulePolicy



SchedulePolicy defines which scheduler is responsible for handling resource allocation requests

_Appears in:_
- [DeploymentSpec](#deploymentspec)

| Field | Description |
| --- | --- |
| `t9kScheduler` _[T9kScheduler](#t9kscheduler)_ | Use t9k-scheduler |


#### ServiceSpec



ServiceSpec defines the desired state of Service created by Controller

_Appears in:_
- [SimpleMLServiceSpec](#simplemlservicespec)

| Field | Description |
| --- | --- |
| `ports` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#serviceport-v1-core">ServicePort</a> array_ | The list of ports that are exposed by this service. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies |
| `type` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#servicetype-v1-core">ServiceType</a>_ | type determines how the Service is exposed. Defaults to ClusterIP. Valid options are ExternalName, ClusterIP, NodePort, and LoadBalancer. "ExternalName" maps to the specified externalName. "ClusterIP" allocates a cluster-internal IP address for load-balancing to endpoints. Endpoints are determined by the selector or if that is not specified, by manual construction of an Endpoints object. If clusterIP is "None", no virtual IP is allocated and the endpoints are published as a set of endpoints rather than a stable IP. "NodePort" builds on ClusterIP and allocates a port on every node which routes to the clusterIP. "LoadBalancer" builds on NodePort and creates an external load-balancer (if supported in the current cloud) which routes to the clusterIP. More info: https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types |


#### SimpleMLService



SimpleMLService is the Schema for service API.

_Appears in:_
- [SimpleMLServiceList](#simplemlservicelist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `SimpleMLService`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta">ObjectMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[SimpleMLServiceSpec](#simplemlservicespec)_ |  |
| `status` _[SimpleMLServiceStatus](#simplemlservicestatus)_ |  |


#### SimpleMLServiceConditionType

_Underlying type:_ `string`

SimpleMLServiceConditionType is a type

_Appears in:_
- [Condition](#condition)



#### SimpleMLServiceList



SimpleMLServiceList contains a list of SimpleMLService



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `SimpleMLServiceList`
| `metadata` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta">ListMeta</a>_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[SimpleMLService](#simplemlservice) array_ |  |


#### SimpleMLServiceSpec



SimpleMLServiceSpec defines the desired state of SimpleMLService

_Appears in:_
- [SimpleMLService](#simplemlservice)

| Field | Description |
| --- | --- |
| `tensorflow` _[TensorflowSpec](#tensorflowspec)_ | Spec for Tensorflow Serving (https://github.com/tensorflow/serving) |
| `pytorch` _[PyTorchSpec](#pytorchspec)_ | Spec for TorchServe |
| `custom` _[CustomSpec](#customspec)_ | Custom Spec |
| `storage` _[Storage](#storage)_ | Storage of model |
| `DeploymentSpec` _[DeploymentSpec](#deploymentspec)_ | Configuration for replicas & scheduler |
| `service` _[ServiceSpec](#servicespec)_ | Configuration for service. Controller will create default service if spec.service not set |


#### SimpleMLServiceStatus



SimpleMLServiceStatus defines the observed state of SimpleMLService

_Appears in:_
- [SimpleMLService](#simplemlservice)

| Field | Description |
| --- | --- |
| `OwnerStatus` _[OwnerStatus](#ownerstatus)_ |  |
| `address` _[Address](#address)_ |  |
| `conditions` _[Condition](#condition) array_ |  |


#### Storage



Storage defines the storage where the model locates

_Appears in:_
- [SimpleMLServiceSpec](#simplemlservicespec)

| Field | Description |
| --- | --- |
| `s3` _[S3Storage](#s3storage)_ | Model locates in S3 |
| `pvc` _[PVCStorage](#pvcstorage)_ | Model locates in pvc |


#### T9kScheduler



T9kScheduler defines SimpleMLService use t9k-scheduler.

_Appears in:_
- [SchedulePolicy](#schedulepolicy)

| Field | Description |
| --- | --- |
| `queue` _string_ | Name of queue which SimpleMLService's pod belongs to |


#### TensorflowSpec



TensorflowSpec defines arguments for configuring Tensorflow model serving

_Appears in:_
- [SimpleMLServiceSpec](#simplemlservicespec)

| Field | Description |
| --- | --- |
| `image` _string_ | Image of Tensorflow Serving |
| `resources` _<a target="_blank" rel="noopener noreferrer" href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#resourcerequirements-v1-core">ResourceRequirements</a>_ | Compute Resources required by a replica |


