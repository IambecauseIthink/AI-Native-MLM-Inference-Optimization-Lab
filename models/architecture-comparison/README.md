# Architecture comparison

| Model/revision | Dense/MoE | Attention/state layers | Hq/Hkv/D | Vision tokens | Weight bytes | KV/state formula | Runtime/commit | Evidence |
|---|---|---|---|---|---|---|---|---|
| 未指定 | unknown | unknown | unknown | unknown | unestimated | 按层求和 | unknown | not-measured |

匹配 workload、硬件和资源数后再谈速度；跨 tokenizer 的 token TPS 不能直接等同工作量。业务模型另列基座、processor、template 和质量目标。
