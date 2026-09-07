# Qwen Architecture Evolution

追踪 Qwen2.5-VL → Qwen3-VL → Qwen3.5 → 新版本/业务 fine-tune。这里是待研究矩阵，不把同一家族所有规模视为相同结构。

| 对象 | 优先核对 | Inference 问题 |
|---|---|---|
| Qwen2.5-VL exact checkpoint | 动态图像/视频处理、位置编码、视觉 token、KV heads | 分辨率与视觉 token 如何影响 prefill 和显存？ |
| Qwen3-VL exact checkpoint | 视觉到语言接口、位置编码、Dense/MoE 变体 | 同 token 数下 encoder 与语言侧成本为何不同？ |
| Qwen3.5 exact checkpoint | full/linear attention 层、状态 shape、Dense/MoE | 哪些层存 KV，哪些层存固定/其他形态状态？ |
| business fine-tune | base revision、权重差异、模板、processor、数据分布 | 基座的量化校准与质量结论能否迁移？ |

每条记录附 config hash、层类型列表、runtime 支持证据、实验预测与更新日期。不能仅凭版本名称填写模型参数。官方入口见 [sources](../../docs/sources.md)。
