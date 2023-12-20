# t9k.ah.core

## t9k.ah.core.Branch

```python
Branch(asset: Union[t9k.ah.core.Model, t9k.ah.core.Dataset], name: str, commit_id: str)
```

Represents a branch of Asset.

### Attributes

* **path** (*str*)

    Path of the branch.

* **asset** (*Union[t9k.ah.core.Model, t9k.ah.core.Dataset]*)

    A `Model` or `Dataset` instance corresponding to the Asset that the branch belongs to.

* **kind** (*str*)

    A string `'branch'`.

* **name** (*str*)

    Name of the branch.

* **commit_id** (*str*)

    ID of the commit that the branch points to.

* **alive** (*bool*)

    Whether the branch is alive.

### Ancestors

* `t9k.ah.core._Ref`

### Methods

#### create_commit

```python
create_commit(self, msg: str, delete: Optional[Sequence[str]] = None, add: Union[Sequence[str], Mapping[str, str], None] = None, force: bool = False) ‑> Optional[t9k.ah.core.Commit]
```

Commits changes to this branch.

First delete, then add.

##### Examples

Add a file as object to this branch:
```python
branch.create_commit(msg='add ...', add=['model.pt'])
```

Specify a path in Asset for a file to add:
```python
branch.create_commit(msg='add ...', add={'model.pt': 'saved_model/'})
```

Add all files under a directory as objects (with the directory):
```python
branch.create_commit(msg='add ...', add=['./saved_model'])
```

Add all files under a directory as objects (without the directory):
```python
branch.create_commit(msg='add ...', add=['./saved_model/*'])
```

Specify a path in Asset for a directory to add:
```python
branch.create_commit(msg='add ...', add={'./saved_model': 'path/to/[saved_model]'})
## or
branch.create_commit(msg='add ...', add={'./saved_model': 'path/to/renamed_dir'})
```

Delete an object from this branch:
```python
branch.create_commit(msg='delete ...', delete=['model.pt'])
```

Delete all objects under the specified path:
```python
branch.create_commit(msg='delete ...', delete=['saved_model/'])
```

##### Args

* **msg** (*str*)

    Commit message.

* **delete** (*Optional[Sequence[str]]*)

    Files or directories to delete from the branch, can be a sequence of paths in branch or `None`. If empty sequence or `None`, delete nothing. If the files or directories to delete do not exist, do nothing (rather than raise an error). Here format `a/.../b` signifies a file, while `a/.../b/` signifies a directory.

* **add** (*Union[Sequence[str], Mapping[str, str], None]*)

    Files or directories to add to the branch, can be a sequence of local paths, a mapping from local paths to their paths in Asset, or `None`. If empty sequence, empty mapping or `None`, add nothing.

* **force** (*bool*)

    Whether to create a new commit if unknown changes or unimplemented changes are found.

##### Returns

A `Commit` instance representing created commit if changes are
commited, `None` if not.

#### create_tag

```python
create_tag(self, name: str) ‑> t9k.ah.core.Tag
```

Creates a tag that points to this branch.

##### Args

* **name** (*str*)

    Name of the tag.

##### Returns

A `Tag` instance representing created tag.

#### delete

```python
delete(self) ‑> None
```

Deletes this branch.

#### download

```python
download(self, paths: Optional[Sequence[str]] = None, save_dir: str = '.') ‑> None
```

Downloads objects of this branch.

##### Args

* **paths** (*Optional[Sequence[str]]*)

    Files or directories to download from this branch, is a sequence of paths in branch. Here format `a/.../b` signifies a file while `a/.../b/` signifies a directory. Defaults to all objects.

* **save_dir** (*str*)

    Local directory which objects are downloaded to. If the directory does not exist, create it. Defaults to current working directory.

#### get_commit

```python
get_commit(self, index: Optional[int] = None, id: Optional[str] = None) ‑> t9k.ah.core.Commit
```

Gets a commit of this branch.

If neither `index` or `id` is provided, return the last commit. If both
`index` and `id` are provided, `id` will not be used.

##### Args

* **index** (*Optional[int]*)

    Index of the commit in this branch, `0` for the last commit, `-1` for the first commit.

* **id** (*Optional[str]*)

    A prefix of ID of the commit.

##### Returns

A `Commit` instance representing retrieved commit.

#### list_commit

```python
list_commit(self) ‑> List[Dict[str, Any]]
```

Lists commits of this branch.

#### list_object

```python
list_object(self) ‑> List[Dict[str, Any]]
```

Lists objects of this branch.

#### merge

```python
merge(self) ‑> None
```

Merges this branch to the main branch.

Here, the specific operation of "merge" involves deleting all objects
from the main branch and then copying all objects from this branch to
the main branch.

Note that this branch itself cannot be the main branch.

#### reset

```python
reset(self) ‑> None
```

Resets this branch to clear all uncommitted changes.

## t9k.ah.core.Commit

```python
Commit(asset: Union[t9k.ah.core.Model, t9k.ah.core.Dataset], id_: str)
```

Represents a commit of Asset.

### Attributes

* **path** (*str*)

    Path of the commit.

* **asset** (*Union[t9k.ah.core.Model, t9k.ah.core.Dataset]*)

    A `Model` or `Dataset` instance corresponding to the Asset that the commit belongs to.

* **kind** (*str*)

    A string `'commit'`.

* **name** (*str*)

    First 8 characters of ID of the commit.

* **id** (*str*)

    ID of the commit.

* **alive** (*bool*)

    Whether the commit is alive.

### Ancestors

* `t9k.ah.core._Ref`

### Methods

#### create_tag

```python
create_tag(self, name: str) ‑> t9k.ah.core.Tag
```

Creates a tag that points to this commit.

##### Args

* **name** (*str*)

    Name of the tag.

##### Returns

A `Tag` instance representing created tag.

#### download

```python
download(self, paths: Optional[Sequence[str]] = None, save_dir: str = '.') ‑> None
```

Downloads objects of this commit.

##### Args

* **paths** (*Optional[Sequence[str]]*)

    Files or directories to download from this commit, is a sequence of paths in commit. Here format `a/.../b` signifies a file while `a/.../b/` signifies a directory. Defaults to all objects.

* **save_dir** (*str*)

    Local directory which objects are downloaded to. If the directory does not exist, create it. Defaults to current working directory.

#### list_commit

```python
list_commit(self) ‑> List[Dict[str, Any]]
```

Lists commits of this commit.

#### list_object

```python
list_object(self) ‑> List[Dict[str, Any]]
```

Lists objects of this commit.


## t9k.ah.core.Dataset

```python
Dataset(id_: str, folder: t9k.ah.core.Folder, name: str, labels: List[str], description: str, extra: str)
```

Represents a Dataset in server.

### Attributes

* **path** (*str*)

    Path of the Dataset in server.

* **id** (*str*)

    ID of the Dataset in server.

* **folder** (*t9k.ah.core.Folder*)

    A `Folder` instance corresponding to the Folder that the Dataset belongs to.

* **kind** (*str*)

    A string `'Dataset'`.

* **name** (*str*)

    Name of the Dataset.

* **labels** (*List[str]*)

    Labels of the Dataset.

* **description** (*str*)

    Description of the Dataset.

* **commit_id** (*str*)

    ID of the commit that the main branch points to.

* **extra** (*str*)

    Extra information about the Dataset.

* **alive** (*bool*)

    Whether the Dataset is alive.

### Ancestors

* `t9k.ah.core._Dataset`

### Methods

#### create_commit

```python
create_commit(self, msg: str, delete: Optional[Sequence[str]] = None, add: Union[Sequence[str], Mapping[str, str], None] = None) ‑> Optional[t9k.ah.core.Commit]
```

Commits changes to this Dataset.

First delete, then add.

##### Examples

Add a file as object to this Dataset:
```python
dataset.create_commit(msg='add ...', add=['0.png'])
```

Specify a path in Dataset for an object to add:
```python
dataset.create_commit(msg='add ...', add={'0.png': 'data/'})
```

Add all files under a directory as objects:
```python
dataset.create_commit(msg='add ...', add=['./data'])
```

Delete an object from this Dataset:
```python
dataset.create_commit(msg='delete ...', delete=['0.png'])
```

Delete all objects under the specified path:
```python
dataset.create_commit(msg='delete ...', delete=['data/'])
```

##### Args

* **msg** (*str*)

    Commit message.

* **delete** (*Optional[Sequence[str]]*)

    Files or directories to delete from the Dataset, can be a sequence of paths in Dataset or `None`. If empty sequence or `None`, delete nothing. If the files or directories to delete do not exist, do nothing (rather than raise an error). Here format `a/.../b` signifies a file, while `a/.../b/` signifies a directory.

* **add** (*Union[Sequence[str], Mapping[str, str], None]*)

    Files or directories to add to the Dataset, can be a sequence of local paths, a mapping from local paths to their paths in Dataset, or `None`. If empty sequence, empty mapping or `None`, add nothing.

##### Returns

A `Commit` instance representing created commit if changes are
commited, `None` if not.

#### delete

```python
delete(self) ‑> None
```

Deletes this Dataset.

#### download

```python
download(self, paths: Optional[Sequence[str]] = None, save_dir: str = '.') ‑> None
```

Downloads objects of this Dataset.

##### Args

* **paths** (*Optional[Sequence[str]]*)

    Files or directories to download from this Dataset, is a sequence of paths in Dataset. Here format `a/.../b` signifies a file while `a/.../b/` signifies a directory. Defaults to all objects.

* **save_dir** (*str*)

    Local directory which objects are downloaded to. If the directory does not exist, create it. Defaults to current working directory.

#### get_commit

```python
get_commit(self, index: Optional[int] = None, id: Optional[str] = None) ‑> t9k.ah.core.Commit
```

Gets a commit of this Dataset.

If neither `index` or `id` is provided, return the last commit. If both
`index` and `id` are provided, `id` will not be used.

##### Args

* **index** (*Optional[int]*)

    Index of the commit in this branch, `0` for the last commit, `-1` for the first commit.

* **id** (*Optional[str]*)

    A prefix of ID of the commit.

##### Returns

A `Commit` instance representing retrieved commit.

#### get_tag

```python
get_tag(self, name: str, verbose: bool = True) ‑> t9k.ah.core.Tag
```

Gets a tag of this Dataset.

##### Args

* **name** (*str*)

    Name of the tag.

* **verbose** (*bool*)

    Whether to log error.

##### Returns

A `Tag` instance representing retrieved tag.

#### list_branch

```python
list_branch(self) ‑> List[Dict[str, Any]]
```

Lists branches in this Dataset.

#### list_commit

```python
list_commit(self) ‑> List[Dict[str, Any]]
```

Lists commits of this Dataset.

#### list_object

```python
list_object(self) ‑> List[Dict[str, Any]]
```

Lists objects of this Dataset.

#### list_tag

```python
list_tag(self) ‑> List[Dict[str, Any]]
```

Lists tags of this Dataset.

#### update

```python
update(self, name: Optional[str] = None, labels: Optional[Sequence[str]] = None, description: Optional[str] = None) ‑> None
```

Updates the metadata of this Dataset.

If none of the args is provided, do nothing.

##### Args

* **name** (*Optional[str]*)

    New name of this Dataset.

* **labels** (*Optional[Sequence[str]]*)

    New labels of this Dataset.

* **description** (*Optional[str]*)

    New description of this Dataset.

## t9k.ah.core.Folder

```python
Folder(path: str, id_: str, owner: str, asset_kind: str, name: str, labels: List[str], description: str, extra: str)
```

Represents a Asset Hub Folder in server.

### Attributes

* **path** (*str*)

    Path of the Folder.

* **id** (*str*)

    ID of the Folder in server.

* **owner** (*str*)

    Owner of the Folder.

* **kind** (*str*)

    Kind of the Folder, is a string `'Model'` or `'Dataset'`.

* **name** (*str*)

    Name of the Folder.

* **labels** (*List[str]*)

    Labels of the Folder.

* **description** (*str*)

    Description of the Folder.

* **extra** (*str*)

    Extra information about the Folder.

* **alive** (*bool*)

    Whether the Folder is alive.

### Methods

#### create_asset

```python
create_asset(self, name: str, labels: Optional[Sequence[str]] = None, description: str = '', exist_ok: bool = False) ‑> Union[t9k.ah.core.Model, t9k.ah.core.Dataset]
```

Creates an Asset in this Folder.

##### Args

* **name** (*str*)

    Name of the Asset.

* **labels** (*Optional[Sequence[str]]*)

    Labels of the Asset.

* **description** (*str*)

    Description of the Asset.

* **exist_ok** (*bool*)

    If True and Asset with `name` already exists, return a `Model` or `Dataset` instance representing this Asset; if False and Asset exists, raise a `RuntimeError`.

##### Returns

A `Model` or `Dataset` instance representing created Model or
Dataset, depending on Asset kind of this Folder.

#### delete

```python
delete(self) ‑> None
```

Deletes this Folder.

#### get_asset

```python
get_asset(self, name: str) ‑> Union[t9k.ah.core.Model, t9k.ah.core.Dataset]
```

Gets an Asset in this Folder.

If you want to get Asset directly by its path, use `ah.get_asset()`.

##### Args

* **name** (*str*)

    Name of the Asset.

##### Returns

A `Model` or `Dataset` instance representing retrieved Model or
Dataset, depending on Asset kind of this Folder.

#### list_asset

```python
list_asset(self) ‑> List[Dict[str, Any]]
```

Lists Assets in this Folder.

#### update

```python
update(self, name: Optional[str] = None, labels: Optional[Sequence[str]] = None, description: Optional[str] = None) ‑> None
```

Updates the metadata of this Folder.

If none of the args is provided, do nothing.

##### Args

* **name** (*Optional[str]*)

    New name of this Folder.

* **labels** (*Optional[Sequence[str]]*)

    New labels of this Folder.

* **description** (*Optional[str]*)

    New description of this Folder.

## t9k.ah.core.Model

```python
Model(id_: str, folder: t9k.ah.core.Folder, name: str, labels: List[str], description: str, extra: str)
```

Represents a Model in server.

### Attributes

* **path** (*str*)

    Path of the Model in server.

* **id** (*str*)

    ID of the Model in server.

* **folder** (*t9k.ah.core.Folder*)

    A `Folder` instance corresponding to the Folder that the Model belongs to.

* **kind** (*str*)

    A string `'Model'`.

* **name** (*str*)

    Name of the Model.

* **labels** (*List[str]*)

    Labels of the Model.

* **description** (*str*)

    Description of the Model.

* **extra** (*str*)

    Extra information about the Model.

* **alive** (*bool*)

    Whether the Model is alive.

### Ancestors

* `t9k.ah.core._Model`

### Methods

#### create_branch

```python
create_branch(self, name: str) ‑> t9k.ah.core.Branch
```

Creates an empty branch of this Model.

##### Args

* **name** (*str*)

    Name of the branch.

##### Returns

A `Branch` instance representing created branch.

#### delete

```python
delete(self) ‑> None
```

Deletes this Model.

#### download

```python
download(self, paths: Optional[Sequence[str]] = None, save_dir: str = '.') ‑> None
```

Downloads objects of this Model.

##### Args

* **paths** (*Optional[Sequence[str]]*)

    Files or directories to download from this Dataset, is a sequence of paths in Dataset. Here format `a/.../b` signifies a file while `a/.../b/` signifies a directory. Defaults to all objects.

* **save_dir** (*str*)

    Local directory which objects are downloaded to. If the directory does not exist, create it. Defaults to current working directory.

#### get_branch

```python
get_branch(self, name: str, verbose: bool = True) ‑> t9k.ah.core.Branch
```

Gets a branch of this Model.

##### Args

* **name** (*str*)

    Name of the branch.

* **verbose** (*bool*)

    Whether to log error.

##### Returns

A `Branch` instance representing retrieved branch.

#### get_commit

```python
get_commit(self, id: str) ‑> t9k.ah.core.Commit
```

Gets a commit of this Model.

If no commit matches `id`, or two or more commits matche `id`,
raise a `RuntimeError`.

##### Args

* **id** (*str*)

    A prefix of ID of the commit.

##### Returns

A `Commit` instance representing retrieved commit.

#### get_tag

```python
get_tag(self, name: str, verbose: bool = True) ‑> t9k.ah.core.Tag
```

Gets a tag of this Model.

##### Args

* **name** (*str*)

    Name of the tag.

* **verbose** (*bool*)

    Whether to log error.

##### Returns

A `Tag` instance representing retrieved tag.

#### list_branch

```python
list_branch(self) ‑> List[Dict[str, Any]]
```

Lists branches in this Model.

#### list_object

```python
list_object(self) ‑> List[Dict[str, Any]]
```

Lists objects of this Model.

#### list_tag

```python
list_tag(self) ‑> List[Dict[str, Any]]
```

Lists tags of this Model.

#### update

```python
update(self, name: Optional[str] = None, labels: Optional[Sequence[str]] = None, description: Optional[str] = None) ‑> None
```

Updates the metadata of this Model.

If none of the args is provided, do nothing.

##### Args

* **name** (*Optional[str]*)

    New name of this Model.

* **labels** (*Optional[Sequence[str]]*)

    New labels of this Model.

* **description** (*Optional[str]*)

    New description of this Model.

## t9k.ah.core.Tag

```python
Tag(asset: Union[t9k.ah.core.Model, t9k.ah.core.Dataset], name: str, commit_id: str)
```

Represents a tag of Asset.

### Attributes

* **path** (*str*)

    Path of the tag.

* **asset** (*Union[t9k.ah.core.Model, t9k.ah.core.Dataset]*)

    A `Model` or `Dataset` instance corresponding to the Asset that the tag belongs to.

* **kind** (*str*)

    A string `'tag'`.

* **name** (*str*)

    Name of the tag.

* **commit_id** (*str*)

    ID of the commit that the tag points to.

* **alive** (*bool*)

    Whether the tag is alive.

### Ancestors

* `t9k.ah.core._Ref`

### Methods

#### create_tag

```python
create_tag(self, name: str) ‑> t9k.ah.core.Tag
```

Creates another tag that points to this tag.

##### Args

* **name** (*str*)

    Name of the tag.

##### Returns

A `Tag` instance representing created tag.

#### delete

```python
delete(self) ‑> None
```

Deletes this tag.

#### download

```python
download(self, paths: Optional[Sequence[str]] = None, save_dir: str = '.') ‑> None
```

Downloads objects of this tag.

##### Args

* **paths** (*Optional[Sequence[str]]*)

    Files or directories to download from this tag, is a sequence of paths in tag. Here format `a/.../b` signifies a file while `a/.../b/` signifies a directory. Defaults to all objects.

* **save_dir** (*str*)

    Local directory which objects are downloaded to. If the directory does not exist, create it. Defaults to current working directory.

#### list_commit

```python
list_commit(self) ‑> List[Dict[str, Any]]
```

Lists commits of this tag.

#### list_object

```python
list_object(self) ‑> List[Dict[str, Any]]
```

Lists objects of this tag.
