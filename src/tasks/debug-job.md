# 调试 Job

本教程演示如何使用 Job 的[调试模式](../modules/jobs/pytorchtrainingjob.md#调试模式)这一功能来对计算任务进行调试。

## 运行示例

请按照<a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/tutorial-examples/blob/v20240206/docs/README-zh.md#%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95">使用方法</a>准备环境，然后前往<a target="_blank" rel="noopener noreferrer" href="https://github.com/t9k/tutorial-examples/tree/v20240206/job/debug">本教程对应的示例</a>，参照其 README 文档运行。

## 通过 SSH 远程连接

对于开启了 SSH 服务的容器，建立 SSH 连接的操作步骤和 Notebook 相同，请参照[通过 SSH 远程使用 Notebook](./ssh-notebook.html)进行操作。唯一不同的是端口转发使用 `t9k-pf pod` 命令，而非 
`t9k-pf notebook` 命令：

```shell
t9k-pf pod <POD_NAME> 5001:2222 -n <PROJECT_NAME>
```

## 进行调试

不论是进入休眠的容器，还是远程连接开启了 SSH 服务的容器，调试都是通过执行一些命令来进行。例如使用 `nvidia-smi` 命令检查当前可用的 GPU，再使用 `ls` 命令检查训练脚本是否存在：

```shell
# 在容器中
nvidia-smi
ls
```

然后使用 `torchrun` 命令启动训练：

```shell
# 在容器中
cd ~/tutorial-examples/job/debug
torchrun --nnodes 1 --nproc_per_node 4 --rdzv_backend c10d torch_mnist_trainingjob.py --save_path model_state_dict.pt --log_dir log --backend nccl
```

随即分布式训练开始进行。如果训练脚本出错，则可以立即在终端中进行调试，不会造成 Job 的失败。调试完成后禁用 debug 模式（将 `spec.runMode.debug.enable` 设为 `false`，或直接注释第 6-12 行），再次创建 PyTorchTrainingJob 则正常启动训练。
