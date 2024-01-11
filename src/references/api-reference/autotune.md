# API Reference

## Packages
- [tensorstack.dev/v1beta1](#tensorstackdevv1beta1)


## tensorstack.dev/v1beta1

Package apis defines the CRD types.
This file specifies the group of CRD resource. It is required by controller-gen.
Details: https://github.com/kubernetes-sigs/kubebuilder/blob/v2.0.0-alpha.4/designs/simplified-scaffolding.md#example

### Resource Types
- [AutoTuneExperiment](#autotuneexperiment)
- [AutoTuneExperimentList](#autotuneexperimentlist)



#### AIStoreConfig



AIStoreConfig defines how to use aistore to store experiment data.

_Appears in:_
- [AutoTuneExperimentSpec](#autotuneexperimentspec)

| Field | Description |
| --- | --- |
| `secret` _string_ | Secret name. The secret is used to store api key which has authority to upload data to aistore. |
| `folder` _string_ | The folder id that the autotune experiment's data will be stored into. |


#### AdvisorConfig



Advisor algorithm and parameter.

_Appears in:_
- [AutoTuneExperimentSpec](#autotuneexperimentspec)

| Field | Description |
| --- | --- |
| `builtinAdvisorName` _string_ | Advisor algorithm name. Optional algorithms: Hyperband, BOHB. |
| `classArgs` _string_ | The parameters of the specific Advisor algorithm. Different algorithms require different parameters. |


#### AssessorConfig



Assessor algorithm and parameter.

_Appears in:_
- [AutoTuneExperimentSpec](#autotuneexperimentspec)

| Field | Description |
| --- | --- |
| `builtinAssessorName` _string_ | Assessor algorithm name. Optional algorithms: Medianstop, Curvefitting. |
| `classArgs` _string_ | The parameters of the specific Assessor algorithm. Different algorithms require different parameters. |


#### AutoTuneExperiment



AutoTuneExperiment is the Schema for the autotune API

_Appears in:_
- [AutoTuneExperimentList](#autotuneexperimentlist)

| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/apis`
| `kind` _string_ | `AutoTuneExperiment`
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[AutoTuneExperimentSpec](#autotuneexperimentspec)_ |  |
| `status` _[AutoTuneExperimentStatus](#autotuneexperimentstatus)_ |  |


#### AutoTuneExperimentList



AutoTuneExperimentList contains a list of AutoTuneExperiment



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/apis`
| `kind` _string_ | `AutoTuneExperimentList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[AutoTuneExperiment](#autotuneexperiment) array_ |  |


#### AutoTuneExperimentSpec



AutoTuneExperimentSpec defines the desired state of AutoTuneExperiment

_Appears in:_
- [AutoTuneExperiment](#autotuneexperiment)

| Field | Description |
| --- | --- |
| `aistore` _[AIStoreConfig](#aistoreconfig)_ | Uploads experiment data and status to AIStore. If this field is not filled out, this function will be skipped. |
| `maxExecSeconds` _integer_ | Time limit. Autotune experiment turns to failure phase if the limit is exceeded. |
| `maxTrialNum` _integer_ | The max number of trials. Autotune experiment is finished if there are already 'maxTrialNum' trials. |
| `trialConcurrency` _integer_ | The max number of running trials at the same time. |
| `searchSpace` _string_ | Hyperparameter search space (a JSON string). The scope for autotune experiment to search the optimized hyperparameters. Example:  {    "batch_size": {"_type": "choice", "_value": [16, 32, 64, 128]},    "learning_rate": {"_type": "choice", "_value": [0.0001, 0.001, 0.01, 0.1]},    "conv_channels1": {"_type": "choice", "_value": [16, 32, 64, 128]}  } |
| `storage` _Quantity_ | Autotune experiment uses a pvc to store config and training metric, use this field to set pvc size. |
| `trainingConfig` _[TrainingConfig](#trainingconfig)_ | TrainingConfig is the configuration used to create trainingjobs. The trainingjob is used to test performance of a set of hyperparameters. |
| `tuner` _[TunerConfig](#tunerconfig)_ | Uses a tuner algorithm to optimize hyperparameters. |
| `assessor` _[AssessorConfig](#assessorconfig)_ | Uses an assessor algorithm to filter hyperparameters, and interrupt training with unqualified hyperparameters. Note: Assessor algorithm is only used when optimizing hyperparameters with tuner. |
| `advisor` _[AdvisorConfig](#advisorconfig)_ | Uses an advisor algorithm to optimize hyperparameters. Note: Tuner and advisor cannot be used at the same time. If both fields are set, tuner will be used for hyperparameter tuning as a priority. |


#### AutoTuneExperimentStatus



AutoTuneExperimentStatus defines the observed state of AutoTuneExperiment

_Appears in:_
- [AutoTuneExperiment](#autotuneexperiment)

| Field | Description |
| --- | --- |
| `OwnerStatus` _[OwnerStatus](#ownerstatus)_ |  |
| `nextCheckedTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta)_ | The next time when the controller will check the status of the experiment process. |
| `phase` _[ExperimentStatus](#experimentstatus)_ | Provides a simple, high-level summary of where the Experiment is in its lifecycle. Note that this is NOT indended to be a comprehensive state machine. optional |
| `serverNote` _string_ | Status of the experiment process. The controller will periodically send requests to the server, check the status of the experiment, and record the status information in this field. |


#### ExperimentStatus

_Underlying type:_ `string`



_Appears in:_
- [AutoTuneExperimentStatus](#autotuneexperimentstatus)



#### TunerConfig



Tuner algorithm and parameter.

_Appears in:_
- [AutoTuneExperimentSpec](#autotuneexperimentspec)

| Field | Description |
| --- | --- |
| `builtinTunerName` _string_ | Tuner algorithm name. Optional algorithms: Random, Anneal, TPE, Evolution, Batch, GridSearch, MetisTuner, GPTuner, PPOTuner and PBTTuner. |
| `classArgs` _string_ | The parameters of the specific Tuner algorithm. Different algorithms require different parameters. |


