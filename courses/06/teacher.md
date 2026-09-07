# 06 教师指导 · INT4 更小，为什么不一定更快？

## 带学节奏

- 0–5 分钟：讲具体情境“W4A16 权重文件小很多，实际服务 QPS 却没升。先检查量化精度还是先检查 kernel？为什么两者都需要？”。先给一个已解释的例子，不连续抛术语或测验。
- 5–10 分钟：共同画出对象/shape/时间线。基础只补学习页的一段，让学员用自己的话指认变量。
- 10–20 分钟：展示默认实验，再询问学习页的一个预测；允许未知。只改一个条件，显示前后结果。
- 20–28 分钟：解释公式与假设，邀请学员指出哪个成本被省略；不要把 toy 数字解释成硬件事实。
- 28–35 分钟：跟读以下真实 symbol，最多打开两个必要调用片段；较长调用链可留到下次。
- 35–45 分钟：做一个反例，记录学员原话、未知与下一步；未经学员明确完成判断，不更新为掌握。

## 结果与递进提示

group4 将 outlier 的 scale 限制在最后一组，普通值 MSE 通常减小，但 scale 数增加。校准上界2会截断20；这可能降低普通值误差却显著增加整体误差。12个数的 scale 开销明显，不用于推断真实模型压缩率。

提示一：先看改变了哪个输入。提示二：指出公式中的对应项。提示三：一起算最小数字，再回到完整例子。不要用“显然”“你应该知道”评价学员。

## 真实实现导航

- [CompressedTensorsConfig.get_quant_method](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors.py#L155) · `vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors.py` · L155。
- [CompressedTensorsLinearMethod.apply](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors.py#L906) · `vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors.py` · L906。
- [LinearBase.__init__](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/model_executor/layers/linear.py#L245) · `vllm/model_executor/layers/linear.py` · L245。

从 LinearBase.quant_method 到 CompressedTensorsConfig.get_quant_method，再到 CompressedTensorsLinearMethod.apply。找 scheme 如何选择及如何 apply_weights。未匹配 scheme 的层可选 UnquantizedLinearMethod；标记预期未量化层与意外 fallback 的区别。

不要把最新文档与固定源码混用；如果实际运行选择了别的 runner/backend，另记证据，不改写这份教学基准。

## 误区与边界

量化采用每组观测最大值再施加校准上界的教学混合模型，不是 LLM Compressor 静态校准或 AWQ/GPTQ 实现；真实静态量化要先在独立 calibration 数据确定 scale。

反例：即使误差合格，packing、group size、反量化融合、硬件和 batch shape 也可能使 INT4 更慢。

## 理解出口

学员能解释一个预测、指出一个假设、提出一条可以否证解释的观察。未达到时，把困难拆成更小例子，不重复整套讲义。

进度初始为 ready；根据真实对话填写 [progress](../progress.md)。本课远程实验仍是 designed，没有启动 GPU。
