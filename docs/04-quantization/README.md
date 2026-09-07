# Quantization

覆盖主题：FP16 / BF16 / FP8 / INT8 / INT4 / W8A8 / W8A16 / W4A16 / static / dynamic / per-tensor / per-channel / per-group / calibration / GPTQ / AWQ / SmoothQuant / LLM Compressor / GPTQModel / Marlin。

## 因果关系

量化把连续值映射到有限表示。整数均匀量化常写为 `q=clip(round(x/scale)+zero_point)`，反量化约为 `scale*(q-zero_point)`；FP8 具有浮点指数/尾数，不能直接当 INT8。

权重固定、可离线观察与校准；激活依赖输入、位置与层，outlier 拉大量程，使多数值只分到很少的有效量化格。权重也可能有敏感通道，不能认为权重永远好量化。

per-channel/per-group 细化 scale 可降低局部误差，但增加元数据和 kernel 约束。静态 scale 遇到分布漂移可能失效；动态 scale 有运行时归约成本。层误差会沿网络累积，业务任务切片可能比平均 perplexity 更敏感。

W4A16 只说明位宽组合，不能证明实际用了高效 INT4 路径。packing、group size、GEMM shape、硬件指令、反量化融合与 backend 共同决定收益。配置参数不是 kernel dispatch 证据。

实验顺序：BF16 复现→独立校准/验证→单候选四维测量→层敏感性→并发曲线→质量合格后 Pareto。校准集不得包含用于最终判断的验证标签样本。

## Question-driven Source Reading

选择一个主题，记录 Concept → Problem → Naive failure → Design → Source → Experiment → Benchmark → Limitations → Improvement。每个节点回答具体问题，不只是链接。

先看 config/入口，再 `rg` 搜索相关 class/function，跟踪最小调用链。记录 repository、commit、file、symbol、输入输出和实际生效分支；安装版本不同就重新定位。

## 本模块实验入口

同 checkpoint、dataset、输出限制比较 W8A8 与 W4A16；同时记录实际 kernel、量化格式、scale 和 fallback。

先写预测、固定条件、失败判据；按 [实验模板](../../templates/experiment.md) 保存。Core 到 designed；真正运行后才填 Results。

## 学会的证据

能解释为什么有效、什么时候无效，以及一个反例。模型结构主题还必须逐项回答：出现原因、解决问题、training、inference、latency、throughput、KV、GPU memory、vLLM support、优化机会。

参考 [来源索引](../sources.md) 与 [Benchmark 合同](../../benchmarks/README.md)。
