# Advanced Inference Optimization

覆盖主题：speculative / draft / Medusa-like / lookahead / prefix caching / sparse attention / long-context / KV offload。

## 因果关系

Speculative decoding 通过候选 token 与目标模型验证减少串行目标步骤；收益取决于接受率、draft 成本、验证开销和 workload。必须区分保持目标分布的算法与改变输出分布的近似方法，并验证实际实现。

Prefix caching 的收益来自重复 token 前缀，不能只报告人为构造的 100% 命中场景。prompt cache 还可能指应用层结果缓存，二者需分开。稀疏 attention 与低比特 KV 的质量风险受上下文和任务影响。

筛选顺序：确定瓶颈→估算节省比例上界→检查 runtime/hardware 支持→最小消融→组合。Amdahl 定律限制局部优化的端到端收益，多个局部加速比不能直接相乘。

## Question-driven Source Reading

选择一个主题，记录 Concept → Problem → Naive failure → Design → Source → Experiment → Benchmark → Limitations → Improvement。每个节点回答具体问题，不只是链接。

先看 config/入口，再 `rg` 搜索相关 class/function，跟踪最小调用链。记录 repository、commit、file、symbol、输入输出和实际生效分支；安装版本不同就重新定位。

## 本模块实验入口

对 speculative 扫描输出长度、batch 与接受率，记录 draft GPU 成本；对 cache 分别测试 cold/warm 与真实命中分布。

先写预测、固定条件、失败判据；按 [实验模板](../../templates/experiment.md) 保存。Core 到 designed；真正运行后才填 Results。

## 学会的证据

能解释为什么有效、什么时候无效，以及一个反例。模型结构主题还必须逐项回答：出现原因、解决问题、training、inference、latency、throughput、KV、GPU memory、vLLM support、优化机会。

参考 [来源索引](../sources.md) 与 [Benchmark 合同](../../benchmarks/README.md)。
