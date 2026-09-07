# Llama 对照

选一个精确公开 checkpoint，读取层数、KV heads、head dimension、FFN、RoPE 与 context config。用与 Qwen 相同的 [模型模板](../../templates/model-analysis.md) 比较。

Core：解释 MHA/GQA 与 FFN 的内存和计算含义；定位 runtime 的 model class。Stretch：匹配参数量与 workload 后比较 QPS/GPU；模型质量与 tokenizer 差异必须单列，不解释为纯架构因果。
