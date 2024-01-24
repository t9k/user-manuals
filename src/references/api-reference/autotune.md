# API Reference

## Packages
- [tensorstack.dev/v1beta1](#tensorstackdevv1beta1)


## tensorstack.dev/v1beta1

Package v1beta1 contains API Schema definitions for the v1beta1 API group

### Resource Types
- [AutoTuneExperiment](#autotuneexperiment)
- [AutoTuneExperimentList](#autotuneexperimentlist)



#### AIStoreConfig



AIStoreConfig represents the configuration for using AIStore as a data storage for experiments.

_Appears in:_
- [AutoTuneExperimentSpec](#autotuneexperimentspec)

| Field | Description |
| --- | --- |
| `secret` _string_ | Secret specifies the secret containing the API Key authorized to upload data to AIStore. |
| `folder` _string_ | Folder indicates the destination folder where the experiment data will be stored. |


#### AdvisorConfig



AdvisorConfig represents the configuration for the advisor algorithm and its parameters.

_Appears in:_
- [AutoTuneExperimentSpec](#autotuneexperimentspec)

| Field | Description |
| --- | --- |
| `builtinAdvisorName` _string_ | BuiltInAdvisorName specifies the name of the built-in advisor algorithm to be used. Available options include: Hyperband, BOHB. |
| `classArgs` _string_ | ClassArgs defines the parameters specific to the chosen advisor algorithm. Different algorithms may require distinct parameters. |


#### AssessorConfig



AssessorConfig represents the configuration for the assessor algorithm and its parameters.

_Appears in:_
- [AutoTuneExperimentSpec](#autotuneexperimentspec)

| Field | Description |
| --- | --- |
| `builtinAssessorName` _string_ | BuiltInAssessorName specifies the name of the built-in assessor algorithm to be used. Available options include: Medianstop, Curvefitting. |
| `classArgs` _string_ | ClassArgs defines the parameters specific to the chosen assessor algorithm. Different algorithms may require distinct parameters. |


#### AutoTuneExperiment



AutoTuneExperiment is the Schema for the autotune API.

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



AutoTuneExperimentList contains a list of AutoTuneExperiment.



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `tensorstack.dev/apis`
| `kind` _string_ | `AutoTuneExperimentList`
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `items` _[AutoTuneExperiment](#autotuneexperiment) array_ |  |


#### AutoTuneExperimentSpec



AutoTuneExperimentSpec defines the desired state of the AutoTuneExperiment.

_Appears in:_
- [AutoTuneExperiment](#autotuneexperiment)

| Field | Description |
| --- | --- |
| `aistore` _[AIStoreConfig](#aistoreconfig)_ | AIStore configures an AIStore as storage for experiment data. If this field is set, data will be uploaded to the AIStore. |
| `maxExecSeconds` _integer_ | MaxExecSeconds is the time limit (in seconds) for the AutoTuneExperiment, If this limit is exceeded, the AutoTuneExperiment reaches phase TIMEOUT. |
| `maxTrialNum` _integer_ | MaxTrialNum specifies the maximum number of trials for the AutoTuneExperiment. Once this number of trials is reached, the AutoTuneExperiment reaches phase DONE. |
| `trialConcurrency` _integer_ | TrialConcurrency is the maximum number of trials running simultaneously. |
| `searchSpace` _string_ | SearchSpace defines the hyperparameter search space as a JSON string. It specifies the range for searching optimized hyperparameters. Example:  {    "batch_size": {"_type": "choice", "_value": [16, 32, 64, 128]},    "learning_rate": {"_type": "choice", "_value": [0.0001, 0.001, 0.01, 0.1]},    "conv_channels1": {"_type": "choice", "_value": [16, 32, 64, 128]}  } |
| `storage` _Quantity_ | Storage specifies the size of PVC for storing configurations and training metrics. |
| `trainingConfig` _[TrainingConfig](#trainingconfig)_ | TrainingConfig represents the configuration for creating Jobs, which evaluate the performance of different hyperparameters. |
| `tuner` _[TunerConfig](#tunerconfig)_ | Tuner configures a tuner for optimizing hyperparameter. |
| `assessor` _[AssessorConfig](#assessorconfig)_ | Assessor configures an assessor for filtering hyperparameters and interrupting training when hyperparameters are deemed unqualified. Note that this field is ignored if Tuner is not set. |
| `advisor` _[AdvisorConfig](#advisorconfig)_ | Advisor configures an advisor for optimizing hyperparameter. Note that when both Tuner and Advisor are set, Tuner takes precedence. |


#### AutoTuneExperimentStatus



AutoTuneExperimentStatus defines the observed state of the AutoTuneExperiment.

_Appears in:_
- [AutoTuneExperiment](#autotuneexperiment)

| Field | Description |
| --- | --- |
| `OwnerStatus` _[OwnerStatus](#ownerstatus)_ |  |
| `nextCheckedTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#time-v1-meta)_ | NextCheckedTime indicates the scheduled time for the next status check of the experiment process by the controller. |
| `phase` _[ExperimentStatus](#experimentstatus)_ | Phase provides a simple, high-level summary of where the AutoTuneExperiment is in its lifecycle. Note that it is NOT intended to serve as a comprehensive state machine. This field is optional. |
| `serverNote` _string_ | ServerNote contains the current status of the experiment process. |


#### ExperimentStatus

_Underlying type:_ `string`



_Appears in:_
- [AutoTuneExperimentStatus](#autotuneexperimentstatus)



#### TunerConfig



TunerConfig represents the configuration for the tuner algorithm and its parameters.

_Appears in:_
- [AutoTuneExperimentSpec](#autotuneexperimentspec)

| Field | Description |
| --- | --- |
| `builtinTunerName` _string_ | BuiltInTunerName specifies the name of the built-in tuner algorithm to be used. Available options include: Random, Anneal, TPE, Evolution, Batch, GridSearch, MetisTuner, GPTuner, PPOTuner, PBTTuner. |
| `classArgs` _string_ | ClassArgs defines the parameters specific to the chosen tuner algorithm. Different algorithms may require distinct parameters. |


