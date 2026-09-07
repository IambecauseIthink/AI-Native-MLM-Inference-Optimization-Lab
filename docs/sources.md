# 来源与版本策略

初始化核对日期：2026-09-07。以下是官方导航/论文入口，不代表仓库已复现。latest/main 可变化，研究笔记和实验必须另存实际 revision 与访问日期。

| 来源 | 用途 |
|---|---|
| [vLLM Architecture](https://docs.vllm.ai/en/latest/design/arch_overview/) | engine 与执行层导航 |
| [vLLM quantization](https://docs.vllm.ai/en/latest/features/quantization/) | 运行时支持矩阵入口，具体版本需复核 |
| [PagedAttention](https://arxiv.org/abs/2309.06180) | KV 分页的原始设计动机 |
| [FlashAttention](https://arxiv.org/abs/2205.14135) | attention 的 IO-aware 设计 |
| [AWQ](https://arxiv.org/abs/2306.00978) | activation-aware weight quantization |
| [GPTQ](https://arxiv.org/abs/2210.17323) | post-training weight quantization |
| [SmoothQuant](https://arxiv.org/abs/2211.10438) | activation/weight 量化难度迁移 |
| [Qwen3-VL official](https://github.com/QwenLM/Qwen3-VL) | Qwen VL 模型与处理流程；旧 Qwen2.5-VL 仓库链接当前会跳转，追溯旧版用固定历史 revision |
| [Qwen3.5 Transformers](https://huggingface.co/docs/transformers/model_doc/qwen3_5) | hybrid attention 实现入口；精确层数仍读取 checkpoint config |

不维护一个永远声称“当前支持”的静态清单。每次记录 tested / documented-only / unsupported / unknown，backend 名称不证明 kernel dispatch。
