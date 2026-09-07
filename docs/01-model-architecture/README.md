# Model Architecture

覆盖主题：Transformer / MHA / MQA / GQA / RoPE / FFN / SwiGLU / RMSNorm / Dense / MoE / attention variants。

## 因果关系

MHA 为各 query head 保存独立 K/V；MQA 共享一个 KV head；GQA 介于两者，减少 KV 存储与读取，但真实速度仍依赖 kernel、batch 和并行布局。训练时的容量/精度变化不能通过推理缓存公式推断。

RoPE 影响位置编码与缓存复用的条件；SwiGLU/FFN 改变矩阵形状与计算量；RMSNorm 的归约可能受带宽与 launch 开销影响。MoE 每 token 激活部分专家，但全部权重仍需存放或分布式管理；路由、负载失衡与 all-to-all 可能抵消减少的 FLOPs。

不要只看 model family。精确读取 checkpoint 的层类型、KV heads、head dimension、滑窗、视觉模块、专家数与量化配置；微调模型还可能更改 tokenizer、processor、模板或输出分布。

## Question-driven Source Reading

选择一个主题，记录 Concept → Problem → Naive failure → Design → Source → Experiment → Benchmark → Limitations → Improvement。每个节点回答具体问题，不只是链接。

先看 config/入口，再 `rg` 搜索相关 class/function，跟踪最小调用链。记录 repository、commit、file、symbol、输入输出和实际生效分支；安装版本不同就重新定位。

## 本模块实验入口

对同一模型手算 full-attention KV，然后用 allocator 统计解释差额；混合层分别核算。

先写预测、固定条件、失败判据；按 [实验模板](../../templates/experiment.md) 保存。Core 到 designed；真正运行后才填 Results。

## 学会的证据

能解释为什么有效、什么时候无效，以及一个反例。模型结构主题还必须逐项回答：出现原因、解决问题、training、inference、latency、throughput、KV、GPU memory、vLLM support、优化机会。

参考 [来源索引](../sources.md) 与 [Benchmark 合同](../../benchmarks/README.md)。
