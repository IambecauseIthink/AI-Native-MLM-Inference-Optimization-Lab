# Distributed Inference

覆盖主题：TP / PP / DP / EP / collective communication / topology / P-D disaggregation。

## 因果关系

TP 分割层内计算并增加 collective；PP 分割层并引入 pipeline 气泡；DP 扩展独立副本但不减少每副本权重；EP 分割专家并承担路由通信。选择取决于模型能否装入、互联拓扑、batch 与 SLO。

单副本速度不是成本效率。对比 TP1/TP2/TP4 时同时列总 QPS、QPS/GPU、显存、TTFT、TPOT 与尾延迟。跨卡通信会随消息大小、拓扑和并发改变；不要仅凭峰值 NVLink 带宽估算最终收益。

## Question-driven Source Reading

选择一个主题，记录 Concept → Problem → Naive failure → Design → Source → Experiment → Benchmark → Limitations → Improvement。每个节点回答具体问题，不只是链接。

先看 config/入口，再 `rg` 搜索相关 class/function，跟踪最小调用链。记录 repository、commit、file、symbol、输入输出和实际生效分支；安装版本不同就重新定位。

## 本模块实验入口

同样 GPU 总预算下比较一个多卡副本与多个单卡副本；保持请求集、负载和路由策略可比。

先写预测、固定条件、失败判据；按 [实验模板](../../templates/experiment.md) 保存。Core 到 designed；真正运行后才填 Results。

## 学会的证据

能解释为什么有效、什么时候无效，以及一个反例。模型结构主题还必须逐项回答：出现原因、解决问题、training、inference、latency、throughput、KV、GPU memory、vLLM support、优化机会。

参考 [来源索引](../sources.md) 与 [Benchmark 合同](../../benchmarks/README.md)。
