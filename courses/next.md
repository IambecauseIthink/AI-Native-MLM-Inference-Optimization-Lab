# 六课之后：从理解到开发与论文迁移

先由学员解释一个已完成案例，再选择与业务瓶颈最接近的一条线，不同时开所有项目。

## 路线 A · 执行与开发

1. CUDA Graph / torch.compile / attention backend：先区分图、编译与实际 kernel。
2. Nsight Systems 找关键路径，再用可用计数器或 shape 分析定位原因；权限不足保留边界。
3. 对固定 vLLM checkout 做一个有界修改：先增加观测或修改一条教学可控策略，写独立 oracle/边界测试。
4. 比较正确性、stream/cancel、缓存隔离、并发与性能；再决定是否保留补丁。

交付：一份固定 commit 调用链、一个有测试的最小 patch、一份可解释的正/负结果。无需从第一行读完整个 vLLM。

## 路线 B · Serving 与多模态

从 TP/PP/DP/EP、输入处理、多模态缓存、Multi-LoRA、KV offload、P/D 中选择一个真实瓶颈。首先解释资源账本：算力、HBM、KV、CPU、网络和排队各占什么。比较 QPS/GPU、goodput、TTFT/TPOT/P99 与质量，不把 total QPS 单独作为成本收益。

## 路线 C · 论文到 runtime

| 瓶颈 | 经典论文/方法 | 当前方向（不是已验证的 SOTA 排名） | runtime 证据状态 | 最小判别实验 |
|---|---|---|---|---|
| KV 浪费与可服务并发 | [PagedAttention](https://arxiv.org/abs/2309.06180) | 混合缓存布局、offload、分离式缓存 | 首期已定位 v0.19.0 block manager；其他方向待课程时锁版本 | 同长度分布比较物理分配、并发和质量 |
| attention 的 IO | [FlashAttention](https://arxiv.org/abs/2205.14135) | 适配新硬件/attention variant 的 backend | 官方 backend 支持不等于当前 dispatch | 固定 dtype/shape 查 kernel 与独立性能 |
| 权重 PTQ | [GPTQ](https://arxiv.org/abs/2210.17323)、[AWQ](https://arxiv.org/abs/2306.00978) | 量化方案与高效低比特 kernel 组合 | 首期定位 compressed-tensors 分派；未复现算法 | 校准独立，比较质量、batch 曲线与实际 kernel |
| activation outlier | [SmoothQuant](https://arxiv.org/abs/2211.10438) | 静态/动态 scale、细粒度低精度 | 不从格式名推断方法或支持 | calibration 漂移与层/任务切片消融 |
| 串行 decode | speculative sampling/draft 方法（进阶时选原论文） | MTP、EAGLE 类方法、接受率与调度融合 | 阅读具体实现/采样证明后再定支持状态 | 同 target/采样，计入 draft 资源与验证成本 |
| 视觉 token 导致 prefill/KV 压力 | pruning/merging/compression 文献（进阶时筛选） | 自适应分辨率与运行时 token reduction | 不能把 Transformers prototype 当 vLLM 支持 | OCR/计数/定位切片＋encoder/prefill/decode 分拆 |

进入每个前沿课之前，重新检索原论文、作者代码、后续复现/勘误与 vLLM release/commit。按 workload、硬件、质量、公平 baseline 和复现成熟度筛选，不按热度或一个宣传加速比选题。保留“排除某方法”的理由，明确 paper-claimed / prototype / integrated / measured。

所有性能复现必须包含同协议 vLLM baseline；允许 Transformers 辅助理解机制，但不作为唯一对照。完成论文复现不等于可生产：还需维护成本、版本升级、灰度和回滚判断。

## 学会的证据

面对新模型，能提出三条有条件的瓶颈假设；挑出最便宜的判别实验；找到实际实现；解释反常结果；对质量/SLO 不合格的方法给出 no-go。不是记住更多开关或论文标题。
