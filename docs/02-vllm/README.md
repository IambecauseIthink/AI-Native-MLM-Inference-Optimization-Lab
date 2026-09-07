# vLLM Deep Dive

覆盖主题：Engine / request lifecycle / PagedAttention / block manager / scheduler / continuous batching / chunked prefill / prefix caching / CUDA Graph / attention backend / quantization / TP / PP / distributed / speculative decoding / Multi-LoRA / multimodal。

## 因果关系

朴素按请求预留最大连续 KV 空间，会浪费容量并限制并发；分页通过逻辑 block 到物理 block 的映射管理增长与共享。注意原始 PagedAttention 论文不是现代 vLLM 所有 backend 的逐行实现说明。

continuous batching 在迭代边界重新组织活跃请求；scheduler 受到 token budget、KV 容量和请求状态约束。chunked prefill 把大 prompt 拆成块以调节与 decode 的干扰；更细粒度也可能增加开销。CUDA Graph 减少部分 CPU/launch 开销，但捕获形状、内存与动态路径决定覆盖率。

以问题驱动：请求为什么等待？KV 为什么分配失败？为什么启用量化却没变快？从外部现象追到 policy、数据结构、执行和真实 kernel。禁止从第一行通读整个仓库。

## Question-driven Source Reading

选择一个主题，记录 Concept → Problem → Naive failure → Design → Source → Experiment → Benchmark → Limitations → Improvement。每个节点回答具体问题，不只是链接。

先看 config/入口，再 `rg` 搜索相关 class/function，跟踪最小调用链。记录 repository、commit、file、symbol、输入输出和实际生效分支；安装版本不同就重新定位。

## 本模块实验入口

固定 workload 扫描 scheduler token budget；记录排队、TTFT、TPOT、KV usage 和 dispatch，区分策略与 kernel 效应。

先写预测、固定条件、失败判据；按 [实验模板](../../templates/experiment.md) 保存。Core 到 designed；真正运行后才填 Results。

## 学会的证据

能解释为什么有效、什么时候无效，以及一个反例。模型结构主题还必须逐项回答：出现原因、解决问题、training、inference、latency、throughput、KV、GPU memory、vLLM support、优化机会。

参考 [来源索引](../sources.md) 与 [Benchmark 合同](../../benchmarks/README.md)。
