# Model analysis · exact checkpoint

Model ID/revision/hash；fine-tune lineage；config/processor/tokenizer/template hashes；状态与来源。

## Architecture

模态、vision encoder、projector、语言骨干、Dense/MoE、总/激活参数、层类型、Hq/Hkv/head_dim、FFN、RoPE、context、sliding window、recurrent state。

每个结构回答：为什么出现？解决什么问题？training、inference、latency、throughput、KV、显存有什么影响？vLLM 如何支持？还能优化哪里？

## Inference implications

prefill/decode/vision/communication 成本；按层 KV/state 公式；每卡布局、权重/scale/激活/workspace；compute/memory/communication 假设。

## Runtime support

vLLM commit、model implementation symbol、processor、backend、quant path、实际 dispatch；标记 tested/documented-only/unknown。

## Business and experiments

输入/视觉/输出分布、质量 evaluator 与切片、baseline、前三个最小可证伪实验、风险。
