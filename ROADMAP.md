# Roadmap · 约 9–12 个月

按能力出口推进，不按日历追债。下表为正常节奏下约 32–45 个活跃 Sprint；每个 Sprint 可用 1–3 周，忙时暂停，因此 9–12 个月是规划窗口而非承诺截止日。超时缩减 Stretch 或延长周期，不跳过质量门槛。

量化优先：完成 Phase 0 和 Phase 1 的 config/KV 基础后，即可交错启动 Phase 4 的 calibration 与 BF16 baseline；Phase 2–3 为量化结果解释补齐 runtime 背景。GPU 基础随每个实验提前学习。

## Phase 0 — Inference Mental Model

参考进度窗口：第 1–3 周；2–3 个活跃 Sprint。

范围：请求生命周期；prefill/decode；roofline；latency/throughput。

- **Core**：用 FLOPs/bytes 预测长输入、长输出和 batch 改变时的瓶颈；定位一次 request 的调度入口；设计反例。每个 Sprint 必须保留 Theory、Source、Experiment design、Reflection 四项。
- **Stretch**：绘制 timeline 并用 profiler 验证。
- **出口证据**：不看笔记解释 compute/memory/queue 三种瓶颈，并指出公式边界。未取得 GPU 时实验状态停在 designed，不伪造 measured。

## Phase 1 — Model Architecture

参考进度窗口：第 4–7 周；3–4 个活跃 Sprint。

范围：Qwen + Llama；MHA/MQA/GQA；RoPE；RMSNorm；SwiGLU；Dense/MoE。

- **Core**：读取指定 config；手算参数/KV；定位 attention 和 FFN；完成一份模型分析。每个 Sprint 必须保留 Theory、Source、Experiment design、Reflection 四项。
- **Stretch**：比较训练稳定性、专家路由和通信成本。
- **出口证据**：对未见 config 提出三条可验证 inference 预测。未取得 GPU 时实验状态停在 designed，不伪造 measured。

## Phase 2 — vLLM Deep Dive

参考进度窗口：第 8–13 周；4–6 个活跃 Sprint。

范围：engine、scheduler、block manager、continuous batching、CUDA Graph、backend。

- **Core**：从请求为什么等待出发追踪一个调用链；设计 chunked prefill 与缓存实验。每个 Sprint 必须保留 Theory、Source、Experiment design、Reflection 四项。
- **Stretch**：Multi-LoRA、TP/PP、spec decoding、multimodal 路径。
- **出口证据**：给出固定 commit 的源码地图与至少一个失败场景。未取得 GPU 时实验状态停在 designed，不伪造 measured。

## Phase 3 — KV Cache

参考进度窗口：第 14–17 周；3–4 个活跃 Sprint。

范围：容量、GQA、分页、碎片、复用、驱逐、offload、FP8/低比特。

- **Core**：算清 KV 与状态内存；设计 length × batch × dtype × architecture 的分层矩阵。每个 Sprint 必须保留 Theory、Source、Experiment design、Reflection 四项。
- **Stretch**：测 block size、长上下文质量、offload 传输上限。
- **出口证据**：产出有适用边界的 KV Playbook。未取得 GPU 时实验状态停在 designed，不伪造 measured。

## Phase 4 — Quantization

参考进度窗口：第 18–23 周；4–6 个活跃 Sprint。

范围：BF16/FP16、FP8/INT8/INT4、W8A8/W8A16/W4A16、GPTQ/AWQ/SmoothQuant。

- **Core**：固定校准与独立验证集；定位 scale 和 kernel dispatch；四维质量/时延/吞吐/内存对比。每个 Sprint 必须保留 Theory、Source、Experiment design、Reflection 四项。
- **Stretch**：逐层敏感性、Marlin/GPTQModel、静态/动态激活消融。
- **出口证据**：解释同为 INT4 为什么速度不同，淘汰质量不合格候选。未取得 GPU 时实验状态停在 designed，不伪造 measured。

## Phase 5 — GPU Performance

参考进度窗口：第 24–27 周；3–4 个活跃 Sprint。

范围：SM、warp、Tensor Core、HBM/shared/register、occupancy、fusion。

- **Core**：从端到端 timeline 找一个关键 kernel；估算算术强度；设计 profiler 证伪。每个 Sprint 必须保留 Theory、Source、Experiment design、Reflection 四项。
- **Stretch**：Triton language / CUDA prototype，验证误差与 dispatch。
- **出口证据**：区分低利用率、带宽受限、launch gap 和通信等待。未取得 GPU 时实验状态停在 designed，不伪造 measured。

## Phase 6 — Serving & Scheduling

参考进度窗口：第 28–31 周；3–4 个活跃 Sprint。

范围：static/dynamic/continuous batching、队列、优先级、admission、SLO。

- **Core**：映射 Triton + vLLM 的两个队列；设计 open-loop 负载与 goodput 测量。每个 Sprint 必须保留 Theory、Source、Experiment design、Reflection 四项。
- **Stretch**：prefill/decode 干扰、SLO-aware 调度策略。
- **出口证据**：同时解释 QPS、TTFT、TPOT、E2E P99 与错误率。未取得 GPU 时实验状态停在 designed，不伪造 measured。

## Phase 7 — Advanced Inference

参考进度窗口：第 32–35 周；3–4 个活跃 Sprint。

范围：draft、Medusa-like、lookahead、prefix/prompt cache、P/D、稀疏 attention。

- **Core**：按 workload 筛选两种方法；估计 acceptance 或 KV 传输成本；设计消融。每个 Sprint 必须保留 Theory、Source、Experiment design、Reflection 四项。
- **Stretch**：offload、长上下文、低比特 KV 组合实验。
- **出口证据**：至少否决一种不适合业务的优化并解释原因。未取得 GPU 时实验状态停在 designed，不伪造 measured。

## Phase 8 — Multimodal Optimization

参考进度窗口：第 36–39 周；3–4 个活跃 Sprint。

范围：vision encoder、visual token pruning/merging/compression、自适应分辨率。

- **Core**：拆分视觉编码、LLM prefill、decode 成本；设计 OCR/计数/定位切片质量实验。每个 Sprint 必须保留 Theory、Source、Experiment design、Reflection 四项。
- **Stretch**：把 token reduction prototype 接入固定版本 runtime。
- **出口证据**：验证 token/position/mask 对齐并给出长尾质量边界。未取得 GPU 时实验状态停在 designed，不伪造 measured。

## Phase 9 — Paper → vLLM → Production

参考进度窗口：第 40–46 周；4–6 个活跃 Sprint。

范围：瓶颈、兼容性、最小原型、runtime 集成、同协议基线、灰度与回滚。

- **Core**：完成一个 paper→prototype→vLLM 的证据链；报告失败同样有效。每个 Sprint 必须保留 Theory、Source、Experiment design、Reflection 四项。
- **Stretch**：受控生产灰度与成本核算。
- **出口证据**：基于公平 baseline、质量门槛和 SLO 给出 go/no-go。未取得 GPU 时实验状态停在 designed，不伪造 measured。

## 季度验收

- 第 1 季度：一张因果图、一份 Qwen 模型分析、一份 vLLM 调用链、一个冻结的量化协议。
- 第 2 季度：KV Playbook、量化四维报告、profile 驱动的瓶颈定位。
- 第 3 季度：SLO 容量曲线、多模态切片实验、论文迁移设计。
- 第 4 季度：一个可复现的 vLLM 集成或有证据的 no-go 报告；复盘自己做出的决策。

能力刻度：0 听过 → 1 能解释因果 → 2 能定位实现 → 3 能设计证伪实验 → 4 能解释实测 → 5 能迁移并判断生产价值。记录证据链接，不按笔记数量评分。
