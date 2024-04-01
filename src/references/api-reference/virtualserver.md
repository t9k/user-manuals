# API Reference

## Packages
- [tensorstack.dev/v1beta1](#tensorstackdevv1beta1)


## tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the  v1beta1 API group

### Resource Types
- [VirtualServer](#virtualserver)
- [VirtualServerList](#virtualserverlist)



#### AdditionalDiskConfig





_Appears in:_
- [Storage](#storage)

| Field | Description |
| --- | --- |
| `name` _string_ |  |
| `bus` _DiskBus_ | Bus indicates the type of disk device to emulate. supported values: virtio, sata, scsi. |
| `serial` _string_ | The system-serial-number in SMBIOS |
| `VolumeSource` _[VolumeSource](#volumesource)_ | VolumeSource represents the location and type of the mounted volume. Defaults to Disk, if no type is specified. |


#### CPURequirements



CPU resources info, including cpu model and count.

_Appears in:_
- [ResourceRequirements](#resourcerequirements)

| Field | Description |
| --- | --- |
| `model` _string_ | virt-handler detects cpus on nodes and add cpu-model.node.kubevirt.io/[model-name] labels to nodes. Set this filed to filter nodes by model. optional |
| `cores` _Quantity_ | Count of cpu. |


#### FileSystemConfig





_Appears in:_
- [Storage](#storage)

| Field | Description |
| --- | --- |
| `name` _string_ |  |
| `VolumeSource` _[VolumeSource](#volumesource)_ | VolumeSource represents the location and type of the mounted volume. Defaults to Disk, if no type is specified. |


#### GPURequirements



GPU resources info, including device name and count.

_Appears in:_
- [ResourceRequirements](#resourcerequirements)

| Field | Description |
| --- | --- |
| `type` _string_ | kubevirt-gpu-device-plugin detects gpus on nodes and add extended resources to k8s cluster. Type is the name of gpu extended resource, it is usually related to gpu device name. |
| `count` _integer_ | Count of gpus in use. |


#### Network





_Appears in:_
- [VirtualServerSpec](#virtualserverspec)

| Field | Description |
| --- | --- |
| `tcp` _integer array_ | The ports exposed with TCP protocol. |
| `udp` _integer array_ | The ports exposed with UDP protocol. |
| `macAddress` _string_ | Interface MAC address. For example: de:ad:00:00:be:af or DE-AD-00-00-BE-AF. |
| `dnsConfig` _[PodDNSConfig](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#poddnsconfig-v1-core)_ | Specifies the DNS parameters of a VM. Parameters specified here will be merged to the generated DNS configuration based on DNSPolicy. |
| `dnsPolicy` _[DNSPolicy](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#dnspolicy-v1-core)_ | Set DNS policy for the VM. Defaults to "ClusterFirst". Valid values are 'ClusterFirstWithHostNet', 'ClusterFirst', 'Default' or 'None'. DNS parameters given in DNSConfig will be merged with the policy selected with DNSPolicy. To have DNS options set along with hostNetwork, you have to specify DNS policy explicitly to 'ClusterFirstWithHostNet'. |


#### PVCTemplate





_Appears in:_
- [RootDisk](#rootdisk)

| Field | Description |
| --- | --- |
| `size` _Quantity_ | PVC Size |
| `volumeMode` _[PersistentVolumeMode](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#persistentvolumemode-v1-core)_ | volumeMode defines what type of volume is required by the claim. Value of Filesystem is implied when not included in claim spec. |
| `accessModes` _[PersistentVolumeAccessMode](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#persistentvolumeaccessmode-v1-core) array_ | AccessModes contains the desired access modes the volume should have. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes-1 |
| `storageClassName` _string_ | Name of the StorageClass required by the claim. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#class-1 |


#### ResourceRequirements



Resources allocated to VirtualMachine.

_Appears in:_
- [VirtualServerSpec](#virtualserverspec)

| Field | Description |
| --- | --- |
| `gpu` _[GPURequirements](#gpurequirements)_ | GPU resources allocated to VirtualMachine. optional |
| `cpu` _[CPURequirements](#cpurequirements)_ | CPU required by this VirtualMachine. |
| `memory` _Quantity_ | Memory required by this VirtualMachine. |


#### RootDisk





_Appears in:_
- [Storage](#storage)

| Field | Description |
| --- | --- |
| `ephemeral` _boolean_ | Not to record the data generated in the virtual machine to the root disk. Defaults to false. |
| `pvc` _[PVCTemplate](#pvctemplate)_ | Create and bind a new pvc to DataVolume. |
| `source` _[DataVolumeSource](#datavolumesource)_ | The src of the data for the requested DataVolume. |
| `bus` _DiskBus_ | Bus indicates the type of disk device to emulate. supported values: virtio, sata, scsi. |


#### SchedulePolicy



SchedulePolicy specifies the preferred scheduler responsible for handling resource allocation requests.

_Appears in:_
- [VirtualServerSpec](#virtualserverspec)

| Field | Description |
| --- | --- |
| `t9kScheduler` _[T9kScheduler](#t9kscheduler)_ |  |


#### Storage





_Appears in:_
- [VirtualServerSpec](#virtualserverspec)

| Field | Description |
| --- | --- |
| `root` _[RootDisk](#rootdisk)_ | Root disk. |
| `additionalDisks` _[AdditionalDiskConfig](#additionaldiskconfig) array_ | Attach a volume as a disk to the VM. |
| `filesystems` _[FileSystemConfig](#filesystemconfig) array_ | Filesystems describes filesystem which is connected to the VM. |


#### T9kScheduler





_Appears in:_
- [SchedulePolicy](#schedulepolicy)

| Field | Description |
| --- | --- |
| `queue` _string_ | Name of the queue to use with the T9kScheduler. |


#### VMRef





_Appears in:_
- [VirtualServerStatus](#virtualserverstatus)

| Field | Description |
| --- | --- |
| `name` _string_ |  |


#### VirtualServer



VirtualServer is the Schema for the virtualservers API

_Appears in:_
- [VirtualServerList](#virtualserverlist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `VirtualServer`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[VirtualServerSpec](#virtualserverspec)_ |  |
| `status` _[VirtualServerStatus](#virtualserverstatus)_ |  |


#### VirtualServerCondition



VirtualServerCondition defines the observed condition of VirtualServer.

_Appears in:_
- [VirtualServerStatus](#virtualserverstatus)

| Field | Description |
| --- | --- |
| `type` _[VirtualServerConditionType](#virtualserverconditiontype)_ | Type is the type of the condition. |
| `status` _[ConditionStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#conditionstatus-v1-core)_ | Status is the status of the condition type. Possible values of are `True|False|Unknown` |
| `message` _string_ | Message is a human-readable message for the reason of the status. |
| `reason` _string_ | Unique, one-word, CamelCase reason for the vm's last transition. |
| `lastTransitionTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta)_ | LastTransitionTime is the last time the status was changed. |


#### VirtualServerConditionType

_Underlying type:_ `string`

VirtualServerConditionType defines all possible types of VirtualServerCondition. Can be one of: DataImported, Ready, Failure or Paused.

_Appears in:_
- [VirtualServerCondition](#virtualservercondition)



#### VirtualServerList



VirtualServerList contains a list of VirtualServer



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `VirtualServerList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[VirtualServer](#virtualserver) array_ |  |


#### VirtualServerSpec



VirtualServerSpec defines the desired state of VirtualServer

_Appears in:_
- [VirtualServer](#virtualserver)

| Field | Description |
| --- | --- |
| `resources` _[ResourceRequirements](#resourcerequirements)_ | Compute Resources required by this VM. |
| `storage` _[Storage](#storage)_ | Disks and filesystems attached to the VM. |
| `firmware` _Firmware_ | Firmware. |
| `network` _[Network](#network)_ | VM network config. |
| `runStrategy` _VirtualMachineRunStrategy_ | Running state indicates the requested running state of the VirtualMachineInstance |
| `useVirtioTransitional` _boolean_ | Fall back to legacy virtio 0.9 support if virtio bus is selected on devices. This is helpful for old machines like CentOS6 or RHEL6 which do not understand virtio_non_transitional (virtio 1.0). |
| `scheduler` _[SchedulePolicy](#schedulepolicy)_ | Specifies the preferred scheduler responsible for handling resource allocation requests. |
| `cloudInit` _string_ | CloudInit represents a cloud-init NoCloud user-data source. The NoCloud data will be added as a disk to the vmi. A proper cloud-init installation is required inside the guest. More info: http://cloudinit.readthedocs.io/en/latest/topics/datasources/nocloud.html |


#### VirtualServerStatus



VirtualServerStatus defines the observed state of VirtualServer

_Appears in:_
- [VirtualServer](#virtualserver)

| Field | Description |
| --- | --- |
| `conditions` _[VirtualServerCondition](#virtualservercondition) array_ | The latest available observations of a VirtualServer's current state. |
| `printableStatus` _VirtualMachinePrintableStatus_ | PrintableStatus is a human readable, high-level representation of the status of the virtual machine |
| `vm` _[VMRef](#vmref)_ | Refers to VirtualMachine created by this VirtualServer. |
| `runStrategy` _VirtualMachineRunStrategy_ | Running state indicates the requested running state of the VirtualMachineInstance mutually exclusive with Running |


