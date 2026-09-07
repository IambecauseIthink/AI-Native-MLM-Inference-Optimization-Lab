# Bottleneck-driven reading list

先读 PagedAttention 建立 runtime 视角，再优先 GPTQ/AWQ/SmoothQuant 连接工作中的量化，FlashAttention 连接 GPU IO。每 Sprint 最多一篇 Core，其他是候选，不追论文数量。

| Paper | 瓶颈 | 阅读问题 | 状态 |
|---|---|---|---|
| [PagedAttention](https://arxiv.org/abs/2309.06180) | KV 容量与碎片 | 分页如何提高可服务并发？现代 backend 是否沿用同一实现？ | unread |
| [FlashAttention](https://arxiv.org/abs/2205.14135) | attention IO | 减少 HBM 访问的收益如何受形状和 batch 影响？ | unread |
| [GPTQ](https://arxiv.org/abs/2210.17323) | weight PTQ | 权重重建误差与业务质量是否一致？ | unread |
| [AWQ](https://arxiv.org/abs/2306.00978) | activation-aware weight PTQ | 保护显著权重的收益是否能迁移校准分布？ | unread |
| [SmoothQuant](https://arxiv.org/abs/2211.10438) | activation outliers | 把难度迁移到权重后，实际 W8A8 kernel 收益是什么？ | unread |

后续队列按业务瓶颈选择：speculative decoding、P/D、KV offload、低比特 KV、visual token reduction。先补原论文/官方代码与 workload 信息再入库，不根据热度指定生产方法。

[笔记目录](notes/README.md) · [复现规则](reproduction/README.md) · [paper-note](../templates/paper-note.md)
