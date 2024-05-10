# API Reference

## Packages
- [tensorstack.dev/v1beta1](#tensorstackdevv1beta1)


## tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the  v1beta1 API group

### Resource Types
- [ServiceAccountToken](#serviceaccounttoken)
- [ServiceAccountTokenList](#serviceaccounttokenlist)



#### SecretReference



SecretReference defines a reference to a Kubernetes v1.Secret object.

_Appears in:_
- [ServiceAccountTokenStatus](#serviceaccounttokenstatus)

| Field | Description |
| --- | --- |
| `name` _string_ | The name of a Kubernetes v1.Secret object that holds the token and kubeconfig. |


#### ServiceAccountToken



ServiceAccountToken is the Schema for the serviceaccounttokens API

_Appears in:_
- [ServiceAccountTokenList](#serviceaccounttokenlist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `ServiceAccountToken`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[ServiceAccountTokenSpec](#serviceaccounttokenspec)_ |  |
| `status` _[ServiceAccountTokenStatus](#serviceaccounttokenstatus)_ |  |


#### ServiceAccountTokenCondition



ServiceAccountTokenCondition contains details for the current condition of ServiceAccountToken

_Appears in:_
- [ServiceAccountTokenStatus](#serviceaccounttokenstatus)

| Field | Description |
| --- | --- |
| `type` _[ServiceAccountTokenConditionType](#serviceaccounttokenconditiontype)_ | Type is the type of the condition. |
| `status` _[ConditionStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#conditionstatus-v1-core)_ | Status is the status of the condition. Can be True, False, Unknown. |
| `lastTransitionTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta)_ | Last time the condition transitioned from one status to another. |
| `reason` _string_ | Unique, one-word, CamelCase reason for the condition's last transition. |
| `message` _string_ | Human-readable message indicating details about last transition. |


#### ServiceAccountTokenConditionType

_Underlying type:_ `string`

ServiceAccountTokenConditionType defines all possible types for ServiceAccountTokenCondition.Type

_Appears in:_
- [ServiceAccountTokenCondition](#serviceaccounttokencondition)



#### ServiceAccountTokenList



ServiceAccountTokenList contains a list of ServiceAccountToken



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/v1beta1`
| `kind` _string_ | `ServiceAccountTokenList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[ServiceAccountToken](#serviceaccounttoken) array_ |  |


#### ServiceAccountTokenSpec



ServiceAccountTokenSpec defines the desired state of ServiceAccountToken

_Appears in:_
- [ServiceAccountToken](#serviceaccounttoken)

| Field | Description |
| --- | --- |
| `duration` _string_ | Duration defines the requested token lifetime. The server may return a token with a longer or shorter lifetime. |


#### ServiceAccountTokenStatus



ServiceAccountTokenStatus defines the observed state of ServiceAccountToken

_Appears in:_
- [ServiceAccountToken](#serviceaccounttoken)

| Field | Description |
| --- | --- |
| `expirationTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta)_ | ExpirationTime is the time of expiration of the returned token. |
| `secretRef` _[SecretReference](#secretreference)_ | SecretRef references a Kubernetes v1.Secret object. |
| `conditions` _[ServiceAccountTokenCondition](#serviceaccounttokencondition) array_ | Conditions represent an array of current conditions observed within the system. |


