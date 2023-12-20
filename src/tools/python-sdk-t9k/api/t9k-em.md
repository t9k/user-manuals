# t9k.em

## t9k.em.artifact.Artifact

```python
Artifact(metadata: Dict[str, Any], objects: Optional[Dict[str, Dict[str, Any]]] = None)
```

Implementation of Artifact, a set of files that a Run inputs or outputs.

### Args

* **metadata** (*Dict[str, Any]*)

    Metadata to initialize a new Artifact.

* **objects** (*Optional[Dict[str, Dict[str, Any]]]*)

    Data of objects of the Artifact.

### Attributes

* **name** (*str*)

    Name of the Artifact.

* **labels** (*List[str]*)

    Labels of the Artifact.

* **description** (*str*)

    Description of the Artifact.

* **created_timestamp** (*str*)

    Created timestamp of the Artifact.

* **alternative_name** (*str*)

    Alternative name of the Artifact.

* **objects** (*List[Dict[str, str]]*)

    Data of objects of the Artifact.

* **remote** (*List[Dict[str, str]]*)

    Upload and download history of the Artifact.

* **local** (*str*)

    Local directory of the Artifact.

### Methods

#### add_dir

```python
add_dir(self, dir_path: str, obj_path: Optional[str] = None) ‑> None
```

Adds all files under a local directory as objects of the Artifact.

The directory will be copied to local directory of the Artifact, the
specific subpath depends on its obj_path, for example:

```
# dir copied to `<local-dir>/a`
artifact.add_dir(dir_path='a/')
# or
artifact.add_dir(dir_path='a')
# or
artifact.add_dir(dir_path='a/', obj_path='a')

# dir copied to `<local-dir>/b/a`
artifact.add_dir(dir_path='a/', obj_path='b/')
# or
artifact.add_dir(dir_path='a/', obj_path='b/a')
```

#### add_file

```python
add_file(self, file_path: str, obj_path: Optional[str] = None) ‑> None
```

Adds a local file as an object of the Artifact.

The file will be copied to local directory of the Artifact, the
specific subpath depends on its object path, for example:

```
# file copied to `<local-dir>/1.png`
artifact.add_file(file_path='1.png')
# or
artifact.add_file(file_path='1.png', obj_path='1.png')

# file copied to `<local-dir>/a/1.png`
artifact.add_file(file_path='1.png', obj_path='a/')
# or
artifact.add_file(file_path='1.png', obj_path='a/1.png')
```

#### add_reference

```python
add_reference(self, uri: str, obj_path: Optional[str] = None) ‑> None
```

Adds a URI as an object reference to the Artifact.

#### parse_from_dict

```python
parse_from_dict(self, data: Dict[str, Any]) ‑> None
```

Parses an Artifact instance from a dict.

#### to_dict

```python
to_dict(self) ‑> Dict[str, Any]
```

Converts Artifact instance to a dict and returns it.

#### upload

```python
upload(self, folder: str = 'default', make_folder: bool = False, conflict_strategy: str = 'new') ‑> None
```

Uploads this Artifact to server.

##### Args

* **folder** (*str*)

    Path of the Folder to which the Artifact is uploaded. If the provided path does not start with '/', `/<current-user>/` is prepended to it.

* **make_folder** (*bool*)

    If True and Folder with path `folder` does not exist, make the Folder and parent Folders as needed.

* **conflict_strategy** (*str*)

    Strategy adopted when an Artifact with the same name as the Artifact to be uploaded already exists in the Folder, must be 'skip', 'error', 'new' or 'replace'. If 'skip', skip the upload; if 'error', error out; if 'new', upload with the alternative name of Artifact; if 'replace', delete the existing Artifact and upload.

## t9k.em.containers.Params

```python
Params(upload: Callable, init_hparams: Dict[str, Union[str, int, float, bool, None, List[~T], Tuple[], Dict[~KT, ~VT]]] = None)
```

Container class to hold hyperparameters of Run.

It is recommended to set all hyperparameters by calling `update` method once before building the model. Nevertheless, you are free to operate hyperparameters like items of a dict or attributes of an object.

### Examples

Recommended method of setting hyperparameters:
```python
run.update({
    'batch_size': 32,
    'epochs': 10,
})
```

Assign parameter like an item of dict or attribute of object:
```python
run.params['batch_size'] = 32
run.params.epochs = 10
```

### Args

* **upload** (*Callable*)

    Function that is called to upload hyperparameters every time hyperparameters are updated.

* **init_hparams** (*Dict[str, Union[str, int, float, bool, None, List[~T], Tuple[], Dict[~KT, ~VT]]]*)

    Initial hyperparameters.

### Ancestors

* `collections.abc.MutableMapping`

### Methods

#### as_dict

```python
as_dict(self)
```

#### items

```python
items(self)
```

D.items() -> a set-like object providing a view on D's items

#### keys

```python
keys(self)
```

D.keys() -> a set-like object providing a view on D's keys

#### parse

```python
parse(self, dist_tf_strategy=None, dist_torch_model=None, dist_hvd=None)
```

Parses hyperparameters from various objects of various frameworks.

##### Args

* **dist_tf_strategy**

    TensorFlow distribution strategy instance if `tf.distribute` is used for distributed training.

* **dist_torch_model**

    PyTorch model wrapped with DP or DDP if `torch.distributed` is used for distributed training.

* **dist_hvd**

    Used module such as `horovod.keras` and `horovod.torch` if Horovod is used for distributed training.

#### update

```python
update(self, new_params: Dict[str, Any], override: bool = True)
```

Updates with new params.

##### Args

* **new_params** (*Dict[str, Any]*)

    New params to be updated with.

* **override** (*bool*)

    Whether to override current params.

#### values

```python
values(self)
```

D.values() -> an object providing a view on D's values

## t9k.em.create_artifact

```python
create_artifact(name: str, labels: Optional[Sequence[str]] = None, description: str = '') ‑> t9k.em.artifact.Artifact
```

Creates and initializes a new Artifact.

The local files of Artifact are placed under the parent directory specified by the environment variable `EM_ARTIFACT_PARENT_DIR` (default is relative path `.em/artifacts`).

### Examples

```python
tensorboard_artifact = em.create_artifact(name='tensorboard_logs')
```

### Args

* **name** (*str*)

    Name of the Artifact.

* **labels** (*Optional[Sequence[str]]*)

    Labels of the Artifact.

* **description** (*str*)

    Description of the Artifact.

### Returns

An Artifact instance created and initialized.

## t9k.em.create_run

```python
create_run(config_path: Optional[str] = None, name: str = 'default', hparams: Optional[Dict[str, Any]] = None, labels: Optional[Sequence[str]] = None, description: str = '', auto_upload: bool = False, folder: str = 'default', make_folder: bool = False, conflict_strategy: str = 'new') ‑> t9k.em.run.Run
```

Creates and initializes a new Run.

The local files of Run are placed under the parent directory specified by the environment variable `EM_RUN_PARENT_DIR` (default is relative path `.em/runs`).

### Examples

Basic usage:
```python
from t9k import em

run = em.create_run(name='cnn_keras',
                    folder='cv/image-classification/mnist')
```

Provide initial parameters of Run:
```python
hparams = {
    'batch_size': 32,
    'epochs': 1,
    'learning_rate': 0.001,
    'conv_channels1': 32,
    'conv_channels2': 64,
    'conv_channels3': 64,
    'conv_kernel_size': 3,
    'maxpool_size': 2,
    'linear_features1': 64,
}

run = em.create_run(name='cnn_keras',
                    hparams=hparams,
                    folder_path='cv/image-classification/mnist')
```

Provide a Run config file:
```python
run = em.create_run(config_path='./run_config.yaml')
```
where the config file `run_config.yaml` is like:
```python
name: cnn_keras
hparams:
  batch_size: 32
  epochs: 1
  learning_rate: 0.001
  conv_channels1: 32
  conv_channels2: 64
  conv_channels3: 64
  conv_kernel_size: 3
  maxpool_size: 2
  linear_features1: 64
labels:
- Keras
description: Train a simple CNN model that classifies images of handwritten digits.
```

### Args

* **config_path** (*Optional[str]*)

    Local path of the Run config file. For all of the following args, the values parsed from the config file take precedence over values passed in.

* **name** (*str*)

    Name of the Run.

* **hparams** (*Optional[Dict[str, Any]]*)

    Initial hyperparameters of the Run.

* **labels** (*Optional[Sequence[str]]*)

    Labels of the Run.

* **description** (*str*)

    Description of the Run.

* **auto_upload** (*bool*)

    Whether to upload the Run and its data automatically and asynchronously. If False, all of the following args will not be used.

* **folder** (*str*)

    Path of the Folder to which the Run is uploaded. If the provided path does not start with '/', `/<current-user>/` is prepended to it. If `auto_upload` is False, this arg will not be used.

* **make_folder** (*bool*)

    If True and Folder with path `folder` does not exist, make the Folder and parent Folders as needed. If `auto_upload` is False, this arg will not be used.

* **conflict_strategy** (*str*)

    Strategy adopted when a Run with the same name as the Run to be uploaded already exists in the Folder, must be 'skip', 'error', 'new' or 'replace'. If 'skip', skip the upload; if 'error', error out; if 'new', upload with the alternative name of Run; if 'replace', delete the existing Run and upload. If `auto_upload` is False, this arg will not be used.

### Returns

A Run instance created and initialized.

## t9k.em.load_artifact

```python
load_artifact(path: str) ‑> t9k.em.artifact.Artifact
```

Loads an Artifact from local or server.

This function will first search for the corresponding local directory, followed by remote path. If the path is not found in either location, raise a `RuntimeError`.

In the case of the remote path, if the provided path does not start with '/', `/<current-user>/` is prepended to it.

### Examples

Load by local path:
```python
em.load_artifact(path=
    '.em/artifacts/tensorboard_logs_220823_194728_4e48t2')
```

Load by remote path:
```python
em.load_artifact(path='/user/path/to/tensorboard_logs')
```

### Args

* **path** (*str*)

    Local directory of the Artifact, or path of the Artifact in server.

### Returns

An Artifact instance loaded.

## t9k.em.load_run

```python
load_run(path: str, auto_upload: bool = False, folder: str = 'default', make_folder: bool = False, conflict_strategy: str = 'new') ‑> t9k.em.run.Run
```

Loads a Run from local or server.

This function will first search for the corresponding local path, followed by remote path. If the path is not found in either location, raise a `RuntimeError`.

In the case of the remote path, if the provided path does not start with '/', `/<current-user>/` is prepended to it.

### Examples

Load by local path:
```python
em.load_run(path='.em/runs/cnn_keras_220823_194728_4e48t2')
```

Load by remote path:
```python
em.load_run(path='/user/path/to/cnn_keras')
```

### Args

* **path** (*str*)

    Local directory of the Run, or path of the Run in server.

* **auto_upload** (*bool*)

    Whether to upload the Run and its data automatically and asynchronously. If False, all of the following args will not be used.

* **folder** (*str*)

    Path of the Folder to which the Run is uploaded. If the provided path does not start with '/', `/<current-user>/` is prepended to it. If `auto_upload` is False, this arg will not be used.

* **make_folder** (*bool*)

    If True and Folder with path `folder` does not exist, make the Folder and parent Folders as needed. If `auto_upload` is False, this arg will not be used.

* **conflict_strategy** (*str*)

    Strategy adopted when a Run with the same name as the Run to be uploaded already exists in the Folder, must be 'skip', 'error', 'new' or 'replace'. If 'skip', skip the upload; if 'error', error out; if 'new', upload with the alternative name of Run; if 'replace', delete the existing Run and upload. If `auto_upload` is False, this arg will not be used.

### Returns

A Run instance loaded.

## t9k.em.login

```python
login(ais_host: Optional[str] = None, api_key: Optional[str] = None, timeout: Optional[int] = None) ‑> None
```

Logs in to AIStore server.

Sets up the client that corresponds with AIStore server.

### Args

* **ais_host** (*Optional[str]*)

    URL of AIStore server. Defaults to `t9k.CONFIG['aistore_host']`.

* **api_key** (*Optional[str]*)

    API Key for requesting server. Defaults to `t9k.CONFIG['api_key']`.

* **timeout** (*Optional[int]*)

    How many seconds to wait for server to send data before giving up.

### Raises

* **requests.HTTPError**

    Unable to connect to the server and `unable_to_connect_ok` is False.

## t9k.em.logout

```python
logout() ‑> None
```

Logs out from the current AIStore server.

The client is unset, it can no longer correspond with AIStore server until it is set up again.

## t9k.em.run.Run

```python
Run(metadata: Dict[str, Any], hparams: Optional[Dict[str, Any]] = None, metrics: Optional[Dict[str, List[Dict[str, Dict[str, Union[str, int, float]]]]]] = None, platform: Optional[Dict[str, Any]] = None, git: Optional[Dict[str, Any]] = None)
```

Implementation of Run, a run of a specific model for certain ML task.

### Args

* **metadata** (*Dict[str, Any]*)

    Metadata to initialize a new Run.

* **hparams** (*Optional[Dict[str, Any]]*)

    Hyperparameters of the Run.

* **metrics** (*Optional[Dict[str, List[Dict[str, Dict[str, Union[str, int, float]]]]]]*)

    Metrics of the Run.

* **platform** (*Optional[Dict[str, Any]]*)

    Platform information of the Run.

* **git** (*Optional[Dict[str, Any]]*)

    Git information of the Run.

### Attributes

* **name** (*str*)

    Name of the Run.

* **labels** (*List[str]*)

    Labels of the Run.

* **description** (*str*)

    Description of the Run.

* **start_timestamp** (*str*)

    Start timestamp of the Run.

* **end_timestamp** (*str*)

    End timestamp of the Run.

* **status** (*str*)

    Status of the Run.

* **alternative_name** (*str*)

    Alternative name of the Run.

* **associations** (*Dict[str, List[Dict[str, str]]]*)

    Input and output resources of the Run.

* **hparams** (*Any*)

    Hyperparameters of the Run.

* **metrics** (*Dict[str, List[Dict[str, Dict[str, Union[str, int, float]]]]]*)

    Metrics produced in the Run.

* **platform** (*Dict[str, Any]*)

    Platform information of the Run.

* **git** (*Dict[str, Any]*)

    Git information of the Run.

* **remote** (*List[Dict[str, str]]*)

    Upload and download history of the Run.

* **local** (*str*)

    Local directory of the Run.

### Methods

#### finish

```python
finish(*args, **kwargs)
```

#### log

```python
log(self, type: str, metrics: Dict[str, float], step: int, epoch: Optional[int] = None) ‑> None
```

Logs a set of metrics of Run.

##### Args

* **type** (*str*)

    Type of the metrics, 'train' (or 'training'), 'val' (or 'validate', 'validation') and 'test' (or 'testing', 'eval', 'evaluate', 'evaluation') for training, validation and testing metrics respectively. Besides, you can also use other arbitrary string as custom type of the metrics.

* **metrics** (*Dict[str, float]*)

    Additional metrics to be logged.

* **step** (*int*)

    Number of the step that the metrics belong to.

* **epoch** (*Optional[int]*)

    Number of the epoch that the metrics belong to.

#### mark_input

```python
mark_input(self, resource: Union[t9k.em.artifact.Artifact, t9k.ah.core.Model, t9k.ah.core.Dataset, t9k.ah.core.Branch, t9k.ah.core.Tag, t9k.ah.core.Commit]) ‑> None
```

Marks an Artifact, Model or Dataset as an input of this Run.

#### mark_output

```python
mark_output(self, resource: Union[t9k.em.artifact.Artifact, t9k.ah.core.Model, t9k.ah.core.Dataset, t9k.ah.core.Branch, t9k.ah.core.Tag, t9k.ah.core.Commit]) ‑> None
```

Marks an Artifact, Model or Dataset as an output of this Run.

#### parse_from_dict

```python
parse_from_dict(self, data: Dict[str, Any]) ‑> None
```

Parses a Run instance from a dict.

#### to_dict

```python
to_dict(self) ‑> Dict[str, Any]
```

Converts Run instance to a dict and returns it.

#### upload

```python
upload(self, folder: str = 'default', make_folder: bool = False, conflict_strategy: str = 'new') ‑> None
```

Uploads this Run to server.

If this Run has input or output Artifacts, these Artifacts are uploaded
as well if they have not been uploaded, and these associations are
uploaded.

##### Args

* **folder** (*str*)

    Path of the Folder to which the Run is uploaded. If the provided path does not start with '/', `/<current-user>/` is prepended to it.

* **make_folder** (*bool*)

    If True and Folder with path `folder` does not exist, make the Folder and parent Folders as needed.

* **conflict_strategy** (*str*)

    Strategy adopted when a Run with the same name as the Run to be uploaded already exists in the Folder, must be 'skip', 'error', 'new' or 'replace'. If 'skip', skip the upload; if 'error', error out; if 'new', upload with the alternative name of Run; if 'replace', delete the existing Run and upload.

## t9k.em.upload

```python
upload(path: str, folder: str = 'default', make_folder: bool = False, conflict_strategy: str = 'new') ‑> None
```

Upload local Runs or Artifacts.

### Examples

Upload a Run by its local directory:
```python
em.upload(path='.em/runs/cnn_keras_220823_194728_4e48t2')
```

Upload all Artifact under the parent directory:
```python
em.upload(path='.em/artifacts')
```

Specify the path of Folder to which the Run is uploaded:
```python
em.upload(path='.em/runs/cnn_keras_220823_194728_4e48t2',
              folder='image_classification/mnist')
```

### Args

* **path** (*str*)

    Local directory of the Run to be uploaded, or parent directory that contains one or more Runs.

* **folder** (*str*)

    Path of the Folder to which the Run is uploaded. If the provided path does not start with '/', `/<current-user>/` is prepended to it.

* **make_folder** (*bool*)

    If True and Folder with path `folder` does not exist, make the Folder and parent Folders as needed.

* **conflict_strategy** (*str*)

    Strategy adopted when a Run with the same name as the Run to be uploaded already exists in the Folder, must be 'skip', 'error', 'new' or 'replace'. If 'skip', skip the upload; if 'error', error out; if 'new', upload with the alternative name of Run; if 'replace', delete the existing Run and upload.


