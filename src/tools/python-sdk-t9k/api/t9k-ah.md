# t9k.ah

## t9k.ah.commit

```python
commit(path: str, msg: str, delete: Optional[Sequence[str]] = None, add: Union[Sequence[str], Mapping[str, str], None] = None, force: bool = False) ‑> Optional[t9k.ah.core.Commit]
```

Commits changes to a branch of an Asset.

First delete, then add.

If no branch is provided, `:main` will be used.

For Windows platform, if you provide absolute paths for parameter `add`, change its format from 'C:\local\path' to '\C\local\path'.

### Examples

Add a file as object to specified branch of Model:
```python
ah.commit('model/llm/gpt2:v1', msg='add ...', add=['model.pt'])
```

Specify a path in Asset for a file to add:
```python
ah.commit('model/llm/gpt2:v1', msg='add ...', add={'model.pt': 'saved_model/'})
```

Add all files under a directory as objects (with the directory):
```python
ah.commit('model/llm/gpt2:v1', msg='add ...', add=['./saved_model'])
```

Add all files under a directory as objects (without the directory):
```python
ah.commit('model/llm/gpt2:v1', msg='add ...', add=['./saved_model/*'])
```

Specify a path in Asset for a directory to add:
```python
ah.commit('model/llm/gpt2:v1', msg='add ...', add={'./saved_model': 'path/to/[saved_model]'})
## or
ah.commit('model/llm/gpt2:v1', msg='add ...', add={'./saved_model': 'path/to/renamed_dir'})
```

Delete an object from a Dataset:
```python
ah.commit('dataset/images/cifar10', msg='delete ...', delete=['0.png'])
```

Delete all objects under the specified path:
```python
ah.commit('dataset/images/cifar10', msg='delete ...', delete=['data/'])
```

### Args

* **path** (*str*)

    Path of the branch.

* **msg** (*str*)

    Commit message.

* **delete** (*Optional[Sequence[str]]*)

    Files or directories to delete from the branch, can be a sequence of paths in branch or `None`. If empty sequence or `None`, delete nothing. If the files or directories to delete do not exist, do nothing (rather than raise an error). Here format `a/.../b` signifies a file, while `a/.../b/` signifies a directory.

* **add** (*Union[Sequence[str], Mapping[str, str], None]*)

    Files or directories to add to the branch, can be a sequence of local paths, a mapping from local paths to their paths in Asset, or `None`. If empty sequence, empty mapping or `None`, add nothing.

* **force** (*bool*)

    Whether to create a new commit if unknown changes or unimplemented changes are found.

### Returns

A `Commit` instance representing created commit if changes are
commited, `None` if not.

## t9k.ah.create

```python
create(path: str, labels: Optional[Sequence[str]] = None, description: str = '', exist_ok: bool = False, create_tag: bool = False, source: str = 'main') ‑> Union[t9k.ah.core.Folder, t9k.ah.core.Model, t9k.ah.core.Dataset, t9k.ah.core.Branch, t9k.ah.core.Tag]
```

Creates a resource.

Note that you cannot create a Folder for another user.

### Examples

Create a Folder:
```python
folder = ah.create('model/llm')
```

Create a Model with labels:
```python
model = ah.create('model/llm/gpt2', labels=['PyTorch'])
```

Create a Dataset with a description:
```python
description = 'CIFAR-10 is a widely used benchmark dataset ...'
dataset = ah.create('dataset/images/cifar10', description=description)
```

Create a non-main branch of specified Model:
```python
branch = ah.create('model/llm/gpt2:v1')
```

Create a tag:
```python
tag = ah.create('model/llm/gpt2:20220101', create_tag=True, source='v1')
## or
tag = ah.create('model/llm/gpt2:20220101', create_tag=True, source='model/llm/gpt2:v1')
```

Create a Model for another user:
```python
model = ah.create('/user/t9k-assethub/model/llm/gpt2')
```

### Args

* **path** (*str*)

    Path of the resource.

* **labels** (*Optional[Sequence[str]]*)

    Labels of the resource. Only applicable for creating a Folder, Model or Dataset.

* **description** (*str*)

    Description of the resource. Only applicable for creating a Folder, Model or Dataset.

* **exist_ok** (*bool*)

    If True and the resource already exists, return a corresponding instance representing the resource; if False and resource exists, raise a `RuntimeError`. Only applicable for creating a Folder, Model or Dataset.

* **create_tag** (*bool*)

    Whether to create a tag instead of a branch. Only applicable for creating a branch or tag.

* **source** (*str*)

    Name/ID or path of the source reference (branch, tag or commit) from which a tag is created. Only applicable for creating a tag.

### Returns

A corresponding instance representing retrieved resource.

## t9k.ah.delete

```python
delete(path: str, force: bool = False) ‑> None
```

Deletes a resource.

### Examples

Delete a Folder:
```python
ah.delete('model/llm')
```

Delete a Model:
```python
ah.delete('model/llm/gpt2')
```

Delete a Dataset:
```python
ah.delete('dataset/images/cifar10')
```

Delete a non-main branch of specified Model:
```python
ah.delete('model/llm/gpt2:v1')
```

Delete a tag:
```python
ah.delete('model/llm/gpt2:20220101')
```

Delete another user's Folder:
```python
ah.delete('/user/t9k-assethub/model/llm')
```

If the Folder does not exist, do nothing:
```python
ah.delete('model/llm', force=True)
```

### Args

* **path** (*str*)

    Path of the resource.

* **force** (*bool*)

    If True, ignore non-existent resources.

## t9k.ah.download

```python
download(path: str, objects: Optional[Sequence[str]] = None, save_dir: str = '.')
```

Download objects of a reference of an Asset.

If no reference is provided, `:main` will be used.

### Examples

Download all objects of specified branch of Model to current working directory:
```python
ah.download('model/llm/gpt2:v1')
```

Download an object to specified directory:
```python
ah.download('model/llm/gpt2:v1', objects=['model.pt'], save_dir='./saved_model')
```

Download all objects under the same path:
```python
ah.download('model/llm/gpt2:v1', objects=['saved_model/'])
```

Specify the reference by tag:
```python
ah.download('dataset/images/cifar10:20220101')
```

Specify the reference by commit:
```python
ah.download('dataset/images/cifar10:a41ac4ec')
```

### Args

* **path** (*str*)

    Path of the reference from which objects are downloaded.

* **objects** (*Optional[Sequence[str]]*)

    Objects to download.

* **save_dir** (*str*)

    Local directory which objects are downloaded to.

## t9k.ah.get

```python
get(path: str) ‑> Union[t9k.ah.core.Folder, t9k.ah.core.Model, t9k.ah.core.Dataset, t9k.ah.core.Branch, t9k.ah.core.Tag, t9k.ah.core.Commit]
```

Gets a resource.

To get a commit, please provide a commit ID with a length of at least 4 to avoid potential conflicts with branches or tags.

### Examples

Get a Folder:
```python
folder = ah.get('model/llm')
```

Get a Model:
```python
model = ah.get('model/llm/gpt2')
```

Get a Dataset:
```python
dataset = ah.get('dataset/images/cifar10')
```

Get a non-main branch of specified Model:
```python
branch = ah.get('model/llm/gpt2:v1')
```

Get a tag:
```python
tag = ah.get('model/llm/gpt2:20220101')
```

Get another user's Folder:
```python
folder = ah.get('/user/t9k-assethub/model/llm')
```

### Args

* **path** (*str*)

    Path of the resource.

### Returns

A instance representing retrieved resource.

## t9k.ah.list

```python
list(path: str, resource: str = 'default') ‑> List[Dict[str, Any]]
```

Lists resources.

Based on the provided `path`, list Folders with the specified Asset kind, Assets within the specified Folder, or all objects of the specified reference (branch, tag or commit) of Asset.

To list Folders that are shared with you, set `path='shared/model'` (or `path='shared/dataset'`); to list Folders that are public, set `path='/public/t9k-assethub/model'` (or `path='/public/t9k-assethub/dataset'`).

To list branches, provide a `path` that points to an Asset and set `resource='branch'`; to list tags, provide a `path` that points to an Asset and set `resource='tag'`; to list commits, provide a `path` that points to a branch of an Asset and set `resource='commit'`.

If a reference is expected but omitted, `:main` will be used.

### Examples

List Model Folders that you own:
```python
folders = ah.list('model')
```

List Model Folders that are shared with you:
```python
folders = ah.list('shared/model')
```

List Model Folders that are public:
```python
folders = ah.list('/public/t9k-assethub/model')
```

List Models in your own Folder:
```python
models = ah.list('model/llm')
```

List Models in another user's Folder:
```python
models = ah.list('/user1/t9k-assethub/model/llm')
```

List objects of specified branch of Model:
```python
objects = ah.list('model/llm/gpt2:v1')
```

List objects of specified tag of Dataset:
```python
objects = ah.list('dataset/images/cifar10:20220101')
```

List branches of specified Model:
```python
branches = ah.list('model/llm/gpt2', resource='branch')
```

List tags of specified Model:
```python
tags = ah.list('model/llm/gpt2', resource='tag')
```

List commits of specified branch of Model:
```python
commits = ah.list('model/llm/gpt2:v1', resource='commit')
```

List commits of specified Dataset:
```python
commits = ah.list('dataset/images/cifar10', resource='commit')
```

### Args

* **path** (*str*)

    Path to be listed.

* **resource** (*str*)

    Kind of the resources, must be `'default'`, `'branch'`, '`tag`' or `'commit'`. This parameter is used to list branches, tags or commits: to list branches, provide a `path` that points to an Asset and set `resource='branch'`; to list tags, provide a `path` that points to an Asset and set `resource='tag'`; to list commits, provide a `path` that points to a branch of an Asset and set `resource='commit'`.

### Returns

A list of resources.

## t9k.ah.login

```python
login(ah_host: Optional[str] = None, ais_host: Optional[str] = None, api_key: Optional[str] = None, timeout: Optional[int] = None) ‑> None
```

Logs in to AIStore server and Asset Hub server.

Sets up the client that corresponds with AIStore server and Asset Hub server.

### Args

* **ah_host** (*Optional[str]*)

    URL of Asset Hub server. Defaults to `t9k.CONFIG['asset_hub_host']`.

* **ais_host** (*Optional[str]*)

    URL of AIStore server. Defaults to `t9k.CONFIG['aistore_host']`.

* **api_key** (*Optional[str]*)

    API Key for requesting server. Defaults to `t9k.CONFIG['api_key']`.

* **timeout** (*Optional[int]*)

    How many seconds to wait for server to send data before giving up.

### Raises

* **requests.HTTPError**

    Unable to connect to the server.

## t9k.ah.logout

```python
logout() ‑> None
```

Logs out from the current AIStore server and Asset Hub server.

The client is unset, it can no longer correspond with AIStore server and Asset Hub server until it is set up again.

## t9k.ah.merge

```python
merge(path: str) ‑> None
```

Merges a branch of a Model to the main branch.

Here, the specific operation of "merge" involves deleting all objects from the main branch and then copying all objects from the specified branch to the main branch.

Note that the specified branch itself cannot be the main branch.

### Examples

```python
ah.merge('model/llm/gpt2:v1')
```

### Args

* **path** (*str*)

    Path of the branch.

## t9k.ah.reset

```python
reset(path: str) ‑> None
```

Resets a branch to clear all uncommitted changes.

### Examples

```python
ah.reset('model/llm/gpt2:main')
```

### Args

* **path** (*str*)

    Path of the branch.

## t9k.ah.update

```python
update(path: str, name: Optional[str] = None, labels: Optional[Sequence[str]] = None, description: Optional[str] = None) ‑> None
```

Updates a resource.

Only Folders and Assets can be updated.

If none of the args is provided, do nothing.

### Examples

Rename a Folder:
```python
ah.update('model/llm', name='generative-language-model')
```

Relabel a Model:
```python
ah.update('model/llm/gpt2', labels=['JAX'])
```

### Args

* **name** (*Optional[str]*)

    New name of the resource.

* **labels** (*Optional[Sequence[str]]*)

    New labels of the resource.

* **description** (*Optional[str]*)

    New description of the resource.
