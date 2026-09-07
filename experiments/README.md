# 实验索引

所有初始计划状态为 designed，未执行远程工作。由小矩阵筛选后再放大，避免全笛卡尔积。

- [kv-cache](kv-cache/README.md)：KV 容量能否换来 SLO 容量？
- [quantization](quantization/README.md)：低比特是否改善业务可接受吞吐？
- [batching](batching/README.md)：权重复用何时不再增加吞吐？
- [scheduling](scheduling/README.md)：长 prefill 如何干扰 decode？
- [prefix-cache](prefix-cache/README.md)：真实前缀重复能节省多少 prefill？
- [speculative-decoding](speculative-decoding/README.md)：接受率能否覆盖 draft 成本？
- [multimodal](multimodal/README.md)：视觉 token 减少是否损伤关键能力？
- [paper-reproduction](paper-reproduction/README.md)：论文优化能否超过当前 vLLM？

执行前复制 [实验模板](../templates/experiment.md)，冻结协议。
