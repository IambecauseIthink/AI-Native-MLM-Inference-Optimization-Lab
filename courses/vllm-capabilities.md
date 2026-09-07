# vLLM 能力地图：我可能已经在用什么？

目标不是把所有开关打开，而是从瓶颈挑一个可验证的能力。**你的实际启动参数、resolved config 和运行日志尚未采集，因此“我的服务是否在用”当前全部为 unknown。** 未手动开启不等于未启用；配置启用也不等于对当前 workload 生效。

## 教学基准中已核对的行为

基准：v0.19.0 / `2a69949bdadf0e8942b7a1619b229cb475beef20`，来源 [source-lock](source-lock.json)。源代码检查不等于本机/生产实测。

| 能力 | 解决的问题 | 默认/配置边界 | 适用条件 | 确认实际生效 | 验证收益 |
|---|---|---|---|---|---|
| Continuous batching / scheduler | 完成请求后及时补入新工作 | engine 的迭代调度机制，不是必须另开一个同名开关 | 固定 runner/version 的请求路径 | 运行请求状态、每步 scheduled tokens 与调用分支 | 同 workload 下批量利用、QPS 和尾延迟 |
| Paged KV / block manager | 动态缓存容量与分配 | 对应 KV manager 路径内的机制，不等同所有 backend 使用原论文同一 kernel | KV group、attention/state 架构相关 | allocator/blocks、模型缓存配置 | 容量、碎片、可服务并发；不能仅测单请求延迟 |
| Chunked prefill | 长输入与其他请求竞争 | Cache/Scheduler 类配置的默认值不能代表最终值；EngineArgs 根据模型支持推导并处理平台例外 | 需核对 model support；某些生成模型不保证关闭开关正确 | resolved enable_chunked_prefill、实际每轮 token 分配 | 合法预算扫描，短长请求 TTFT/TPOT/P99 |
| Prefix caching | 重复精确前缀的 prefill | CacheConfig 字段默认 True；EngineArgs 最终取值受模型支持与平台影响 | 精确 token/身份匹配、完整块、缓存保留；某些请求跳过读取 | resolved config + cached tokens，检查跳过条件 | cold/warm 分开、真实前缀比例；TTFT 和 QPS |
| max_num_batched_tokens / max_num_seqs | 每轮工作量与序列数量上限 | 默认由硬件、usage context、模型等条件推导；不是通用固定数 | 更改前确认显存与调度约束 | 启动 resolved config、实际有效 batch | 单变量扫描，记录抢占、队列、显存、SLO |
| compressed-tensors 量化分派 | 将压缩表示映射到 layer scheme | 由模型量化配置、层匹配、scheme 选择，非统一默认量化 | layer type、格式、shape、硬件与 kernel | quant_method → scheme → apply_weights；预期排除层单列 | 同协议 BF16/candidate，质量四维与 kernel 证据 |

默认值推导入口：[EngineArgs._set_default_chunked_prefill_and_prefix_caching_args](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/engine/arg_utils.py#L2107)。运行支持检查需要实际配置；不能直接给生产服务替换参数。

## 后续能力检查表

以下是要进一步核实和学习的能力，不是“都已在教学版本/你的模型上测过”的兼容性清单。官方 [Architecture](https://docs.vllm.ai/en/latest/design/arch_overview/)、[Optimization](https://docs.vllm.ai/en/latest/configuration/optimization/) 与 [Quantization](https://docs.vllm.ai/en/latest/features/quantization/) 仅作导航；进入某课时将相关实现锁定到具体版本。

| 能力 | 瓶颈与问题 | 配置方式/默认状态 | 适用条件 | 如何确认 | 最小验证 |
|---|---|---|---|---|---|
| CUDA Graph | CPU/launch 开销 | 编译/graph 模式与形状决定；当前路径 unknown | 支持捕获的模型、shape、backend、显存 | 实际 replay/capture trace，非只看参数 | eager 与合法 graph 模式对照，独立 profile |
| torch.compile / fusion | 图与算子调度、内存读写 | 版本与 compilation 配置决定，未核对当前部署 | 图断点、动态 shape、算子兼容性 | 编译日志、生成图、实际 kernel | 冷启动与稳态分列；误差与性能 |
| Attention backend | attention 计算/IO | 自动选择或显式配置；具体选择 unknown | dtype、head shape、GPU、attention variant | backend 日志 + kernel trace | 同 workload/质量比较可支持 backend |
| FP8/低比特 KV | KV 容量/读带宽 | 单独 KV dtype/scale 配置，不等于权重量化 | GPU/backend、scale、长上下文质量 | KV dtype、scale 和实际执行路径 | 容量、TPOT、长上下文切片 |
| TP / PP | 单副本放不下/计算分布 | 显式并行配置；当前布局 unknown | GPU 数、拓扑、shape、气泡 | rank 映射、collective、每卡内存 | 固定总 GPU 预算下 QPS/GPU 与 P99 |
| DP / EP | 副本容量或 MoE 专家分布 | 显式资源/路由配置；当前 unknown | DP 需要副本资源；EP 需要 MoE 与合适互联 | 路由负载、专家/collective trace | 同资源预算、负载均衡与质量 |
| CPU/输入处理 | tokenizer/processor/传输阻塞 | 进程/线程/缓存配置，默认随版本 | CPU 核数、多模态输入、IPC | CPU profile、队列、GPU 空洞 | 固定 GPU 配置只改输入处理 |
| 多模态 processor/encoder cache | 重复视觉处理 | 缓存类型与配置需分开核对 | 相同输入与身份、处理器及模型支持 | processor/encoder 耗时、缓存命中 | cold/warm 与真实图像重复分布 |
| Multi-LoRA | 多个微调模型共享基座 | 需 LoRA 配置和 adapter，非所有模型通用 | target modules、rank、量化/并行兼容性 | 实际 adapter 加载和每请求路由 | 与独立副本对照质量/资源/切换开销 |
| KV offload | GPU KV 容量不足 | 需 connector/offload 配置，当前 unknown | 传输带宽、CPU内存、支持的缓存布局 | H2D/D2H 与命中/驱逐回执 | 容量收益、传输成本、尾延迟 |
| P/D 分离 | prefill/decode 干扰与资源配比 | 多服务/connector/路由拓扑配置 | 网络、KV layout、资源池和模型兼容 | KV 传输与两侧队列 | 同总 GPU、同 workload 的完整 E2E/SLO |
| Speculative decoding / MTP | 串行目标 decode 步数 | 需方法/模型相关配置；当前 unknown | draft/target 支持、接受率、采样正确性 | accepted/rejected、draft 成本、目标验证路径 | 同质量/采样下 TPOT、QPS/GPU |

## 第一次实际服务审计怎么做

学员提供或授权读取脱敏启动命令、模型 config、版本和 resolved config/日志。只读标记 unknown / configured / observed / measured-benefit；每条能力回答“当前瓶颈是否让它有机会起作用”。之后只选一个实验，不批量打开开关。正式质量与性能回执不由配置状态代替。
