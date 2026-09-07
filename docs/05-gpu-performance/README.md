# GPU Performance

覆盖主题：SM / warp / Tensor Core / HBM / shared memory / registers / bandwidth / FLOPs / occupancy / launch / fusion / Nsight Systems / Nsight Compute / PyTorch profiler / DCGM / Triton language / CUDA。

## 因果关系

从请求时间分解开始：CPU 准备、队列、GPU 工作、跨卡通信、响应传输。Nsight Systems 用于时间线与空隙；Nsight Compute 用于目标 kernel 的计数器与 roofline。先找关键路径，再选少数 kernel 深挖。

SM occupancy 是活跃 warp 等资源状态的描述，不等于计算效率。较高 occupancy 可能隐藏访存延迟，但寄存器压力、shared memory 和 spill 会改变结果。nvidia-smi utilization 不是 Tensor Core FLOPs，也不是实际 HBM GB/s。

fusion 减少中间读写和 launch，却可能增加寄存器占用。Tensor Core dtype 支持不等于当前 shape/backend 使用了它。 profiler 改变运行开销，正式吞吐与 profiler run 分开保存。

无法读取硬件计数器时记录权限边界，不能用估算替代实测带宽。学习 Triton language/CUDA 是为了看懂、验证、定位瓶颈，不以手写所有 kernel 为目标。

## Question-driven Source Reading

选择一个主题，记录 Concept → Problem → Naive failure → Design → Source → Experiment → Benchmark → Limitations → Improvement。每个节点回答具体问题，不只是链接。

先看 config/入口，再 `rg` 搜索相关 class/function，跟踪最小调用链。记录 repository、commit、file、symbol、输入输出和实际生效分支；安装版本不同就重新定位。

## 本模块实验入口

挑选一个关键 GEMM/attention kernel，预测 fusion 的收益与寄存器风险；比较正确性和独立运行性能。

先写预测、固定条件、失败判据；按 [实验模板](../../templates/experiment.md) 保存。Core 到 designed；真正运行后才填 Results。

## 学会的证据

能解释为什么有效、什么时候无效，以及一个反例。模型结构主题还必须逐项回答：出现原因、解决问题、training、inference、latency、throughput、KV、GPU memory、vLLM support、优化机会。

参考 [来源索引](../sources.md) 与 [Benchmark 合同](../../benchmarks/README.md)。
