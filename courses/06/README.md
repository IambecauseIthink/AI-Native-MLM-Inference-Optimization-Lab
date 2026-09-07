# 06 · INT4 更小，为什么不一定更快？

**这次只解决：W4A16 权重文件小很多，实际服务 QPS 却没升。先检查量化精度还是先检查 kernel？为什么两者都需要？**

用时 30–45 分钟，可随时暂停。让助手说“带我学第 06 课”，由助手先解释例子，再分步展开。无需先读完教材，不安装模型。

## 先理解这个例子

量化把数值映射到有限格点，scale 控制格子大小。outlier 扩大量程，让普通值落到更粗的格子上；分组 scale 可隔离 outlier，但有额外 metadata。权重是固定的，激活随输入变化，校准分布不匹配会截断。FP8 是浮点格式，不是本实验的 INT8。

## 做一个预测，然后操作

bits=4 且 outlier=20 时，把 group_size 从 12 改为 4，普通值误差与 scale 存储分别如何变？

允许回答“不确定，因为……”。在仓库根目录运行；每次只改变一个条件，恢复默认后再试下一个：

```bash
python3 scripts/lab.py lesson --id 06
python3 scripts/lab.py lesson --id 06 --set group_size=4
python3 scripts/lab.py lesson --id 06 --set calibration_max=2
python3 scripts/lab.py lesson --id 06 --params
```

[交互图源码](../visuals/lesson-06.html) 可由助手直接在对话中展示；不要依赖 VS Code 默认 Markdown 预览执行脚本。可选本地预览方法见 [交互实验说明](../visuals/README.md)。结果始终标明 synthetic/analytical，不是 GPU 实测。

## 用一点原理解释

`q=clip(round(x/scale),−qmax,qmax)，x_hat=q×scale，qmax=2^(bits−1)−1；MSE=mean((x−x_hat)^2)。权重 payload 比 BF16=bits/16，不是耗时比。`

即使误差合格，packing、group size、反量化融合、硬件和 batch shape 也可能使 INT4 更慢。

## 带着问题看源码和教材

vLLM **v0.19.0 / 2a69949bdadf0e8942b7a1619b229cb475beef20**；源码导航不是运行证明。

- [CompressedTensorsConfig.get_quant_method](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors.py#L155) · `vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors.py` · L155。
- [CompressedTensorsLinearMethod.apply](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors.py#L906) · `vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors.py` · L906。
- [LinearBase.__init__](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/model_executor/layers/linear.py#L245) · `vllm/model_executor/layers/linear.py` · L245。

从 LinearBase.quant_method 到 CompressedTensorsConfig.get_quant_method，再到 CompressedTensorsLinearMethod.apply。找 scheme 如何选择及如何 apply_weights。未匹配 scheme 的层可选 UnquantizedLinearMethod；标记预期未量化层与意外 fallback 的区别。

教材：[MLSysBook · Quantization and Precision](https://mlsysbook.ai/vol1/model_compression/model_compression.html)。只读 Quantization and Precision、Numerical format comparison 与 Measuring optimization effectiveness，区分表示更小和执行更快。

## 今天如何结束

回答：如果校准上界只有 2，却看到值 20，是变成更精细的量化还是严重截断？为何不能只看普通值 MSE？

在 [进度记录](../progress.md) 留下自己的预测、观察、未知与下一步。读完或跑完不自动等于掌握，不自动进入下一课。

下一步：进入能力地图，选一个实际瓶颈，再到执行开发或论文迁移路径。

[远程验证设计](remote.md) · [教师页：带学时再看](teacher.md) · [回到课程入口](../README.md)
