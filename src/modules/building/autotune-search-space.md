# 搜索空间

搜索空间用于定义超参数的范围，AutoTune 会在这一范围内对超参数进行组合并测试，最后得到效果最好的一组训练。

## 格式

```json
{
  "parameter1": {"_type": "choice", "_value":[1, 2, 3, 4]},
  "parameter2": {"_type": "randint", "_value":[1, 10]},
  ...
}
```

在上述结构中：

* 每一个条目都记录了一个超参数的名称和搜索方式：
    * 每一个条目的键值（例如 `parameter1` 和 `parameter2`）表示超参数的名称。
    * `_type` 是超参数搜索方法。
    * `_value` 表示搜索方法所使用的参数。
* `choice` 和 `randint` 表示超参数的搜索方法，其具体含义请参阅[搜索方法](#搜索方法)。

## 搜索方法

|     _type     |    _value 格式    |                            详细描述                          |
| ------------- | ---------------- | ----------------------------------------------------------- |
| `choice`      | 数组（数字或字符串） | 每次训练选取数组 `_value` 中一个值作为超参数。例：`{"learning_rate":{"_type": "choice", "_value": [0.01, 0.02, 0.1, 0.2]}}`，进行超参数调优时，每一组训练会从四个值中选取一个。 |
| `randint`     | `[lower, upper]` | 每次训练选取 `lower` 和 `upper` 之间中的一个随机整数（不包括 `upper`）作为超参数。例：`{"learning_rate":{"_type": "randint", "_value": [1, 10]}}`，进行超参数调优时，每一组训练可能取到的值有 `[1, 2, 3, 4, 5, 6, 7, 8, 9]`。 |
| `uniform`     | `[low, high]`    | 每次训练从 `lower` 到 `upper` 区间内均匀采样作为超参数。 |
| `quniform`    | `[low, high, q]` | 取值方法为 `clip(round(uniform(low, high) / q) * q, low, high)`，此公式含义为：从 `low` 到 `high` 区间内均匀采样，然后将取值除以 `q`，并四舍五入为整数，然后将超出 `[low, high]` 区间的值舍弃，加上 `low` 和 `upper` 两个值，构成选值区间。例：`_value` 为 `[0, 10, 2.5]`，表示超参数的选值范围时 `[0, 2.5, 5, 7.5, 10]`；`_value` 为 `[2, 10, 5]`，表示超参数的选值范围时 `[2, 5, 10]`。 |
| `loguniform`  | `[low, high]`    | 取值方法为 `exp(uniform(log(low), log(high)))`，此公式含义为：从 `log(low)` 到 `log(high)` 区间内均匀采样得到样本 `x`，然后计算 `exp(x)` 得到超参数。 |
| `qloguniform` | `[low, high, q]` | 取值方法为 `clip(round(loguniform(low, high) / q) * q, low, high)`（其中 `loguniform(low, high)` 表示 `exp(uniform(log(low), log(high)))`），此公式含义参考 `quniform` 和 `loguniform` 条目。 |
| `normal`      | `[mu, sigma]`    | 超参数的取值满足正态分布 `N(mu, sigma^2)`。 |
| `qnormal`     | `[mu, sigma, q]` | 取值方法为 `round(normal(mu, sigma) / q) * q`，此公式含义参考 `quniform` 条目。 |
| `lognormal`   | `[mu, sigma]`    | 取值方法为 `exp(normal(mu, sigma))`，此公式含义参考 `loguniform` 条目。 |
| `qlognoraml`  | `[mu, sigma, q]` | 取值方法为 `round(exp(normal(mu, sigma)) / q) * q`，此公式含义参考 `quniform` 和 `loguniform` 条目。 |

!!! info "信息"
    不同算法可以支持不同种类的搜索方法：并不是在每一种调优算法中都可以使用以上所有搜索方法；也有些调优算法支持使用上述方法之外的搜索方法，例如 [PPO 算法](./hpo-algorithm.md#ppotuner)。
