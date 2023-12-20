# t9k.config

## t9k.config.Config

```python
Config()
```

SDK config.

### Methods

#### get

```python
get(self, key: str, default: Any = None) ‑> Any
```

#### items

```python
items(self) ‑> ItemsView[str, Any]
```

#### to_dict

```python
to_dict(self) ‑> Dict[str, Any]
```

#### update

```python
update(self, new_config: Dict[str, Any]) ‑> None
```

## t9k.config.ConfigItem

```python
ConfigItem(name: str, value: Optional[Any] = None, processor: Union[Callable, Sequence[Callable], None] = None, validator: Union[Callable, Sequence[Callable], None] = None, hook: Union[Callable, Sequence[Callable], None] = None)
```

SDK config item.

### Attributes

* **name** (*str*)

    Name of config item.

* **value** (*Any*)

    Value of config item.
