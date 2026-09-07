# KV Cache Optimization Playbook

覆盖主题：capacity / GQA / paging / fragmentation / block size / reuse / eviction / offload / FP8 / lower-bit / long context。

## 因果关系

常规 full-attention 的 raw KV bytes 为 `2 × L × Hkv × Dhead × bytes_per_element × Σ cached_tokens`。这里是 KV heads，不能用 query heads 代替。不同层 shape/dtype 不同则逐层求和。

这是全局逻辑量，不可无条件除以 TP；复制 KV heads、padding、scale、block 对齐、prefix 共享与滑窗会改变每卡物理占用。Qwen 混合 attention/state 层必须把 full-attention KV 与 recurrent state 分开算。

较小 block 减少尾部浪费但可能增加管理/访问开销。prefix reuse 减少重复 prefill，不能消除每步 decode 的工作。FP8 KV 降低存储字节数，但 scale 质量、转换与 backend 路径可能使速度不升反降。offload 用传输时间换容量，先计算链路上限。

Playbook：容量受限先查分配与长尾；重复 prompt 查可复用前缀比例；decode 受限查权重/KV 带宽；质量下降查 scale 和长上下文切片。每条建议必须附实测与不适用条件。

## Question-driven Source Reading

选择一个主题，记录 Concept → Problem → Naive failure → Design → Source → Experiment → Benchmark → Limitations → Improvement。每个节点回答具体问题，不只是链接。

先看 config/入口，再 `rg` 搜索相关 class/function，跟踪最小调用链。记录 repository、commit、file、symbol、输入输出和实际生效分支；安装版本不同就重新定位。

## 本模块实验入口

先固定架构做 length × concurrency × dtype 小矩阵，再跨架构复验；避免直接执行所有组合造成成本膨胀。

先写预测、固定条件、失败判据；按 [实验模板](../../templates/experiment.md) 保存。Core 到 designed；真正运行后才填 Results。

## 学会的证据

能解释为什么有效、什么时候无效，以及一个反例。模型结构主题还必须逐项回答：出现原因、解决问题、training、inference、latency、throughput、KV、GPU memory、vLLM support、优化机会。

参考 [来源索引](../sources.md) 与 [Benchmark 合同](../../benchmarks/README.md)。
