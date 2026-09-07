# Inference Mental Model

覆盖主题：prefill / decode / arithmetic intensity / roofline / latency / throughput / batch / sequence length。

## 因果关系

一个 prompt 的多个位置可并行计算，权重跨 token 复用，把小矩阵乘法变成更大的 GEMM；因此 prefill 较容易提高算术强度。decode 每个序列通常每步只生成一个 token，小 batch 下仍要读取大量权重，又要读取历史 KV，因此经常受内存带宽约束。batch 增大提高权重复用，但也增加 KV 读写与总显存需求，最终可能转为 compute-bound 或容量受限。

`arithmetic intensity = FLOPs / 实际从目标内存层搬运的 bytes`；roofline 上界为 `min(峰值 FLOP/s, 带宽 × intensity)`。使用实际 dtype/硬件峰值，并区分理论峰值与可达效率。该上界不含排队、CPU、网络和跨 GPU 同步。

长序列增加 attention 的历史访问量与 KV 容量。prefill 不是永远 compute-bound；短 prompt、小 GEMM、视觉预处理、CPU 或启动开销都可能主导。decode 在高 batch、大专家计算或长上下文下也可能改变瓶颈。

提高并发可让 GPU 更忙，却增加等待时间。QPS 提升不能推出单请求 E2E 改善；必须同时看负载、队列和尾延迟。

## Question-driven Source Reading

选择一个主题，记录 Concept → Problem → Naive failure → Design → Source → Experiment → Benchmark → Limitations → Improvement。每个节点回答具体问题，不只是链接。

先看 config/入口，再 `rg` 搜索相关 class/function，跟踪最小调用链。记录 repository、commit、file、symbol、输入输出和实际生效分支；安装版本不同就重新定位。

## 本模块实验入口

预测 batch 1→16 时 QPS、TPOT 与显存；保持输出上限一致，再用实际 token 数解释偏差。

先写预测、固定条件、失败判据；按 [实验模板](../../templates/experiment.md) 保存。Core 到 designed；真正运行后才填 Results。

## 学会的证据

能解释为什么有效、什么时候无效，以及一个反例。模型结构主题还必须逐项回答：出现原因、解决问题、training、inference、latency、throughput、KV、GPU memory、vLLM support、优化机会。

参考 [来源索引](../sources.md) 与 [Benchmark 合同](../../benchmarks/README.md)。
