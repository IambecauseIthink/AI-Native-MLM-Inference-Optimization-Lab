# Benchmark contract

工具分为：workload 生成 → 外部 runtime 执行并保存原始结果 → 规范化 request events → summarize → quality evaluator → compare。当前仓库提供 CPU 生成/汇总/筛选和命令证据捕获；真实 Triton/vLLM 负载驱动与业务 evaluator 需要按固定版本接入，尚未实现通用服务客户端。

## Protocol

冻结 model/processor/template、数据 manifest、evaluator、runtime commit、镜像、硬件/拓扑、GPU 数、采样、seed、max_tokens、EOS、输入/输出/视觉长度分布、cache 状态、并发/到达率、timeout/retry。量化配置是明确的 treatment；其他变化进入独立 cohort。

正式 baseline/candidate 各 10 个固定 warmup 请求（不计入统计）+ 3 轮完整冻结数据，保存逐轮数据与范围；业务协议不同则预先声明新协议。不得把三轮的并发墙钟时间简单加总为一个并行窗口，不得只汇报最好一轮。

同时报告 closed-loop 并发曲线与代表性 open-loop 到达负载；后者记录计划到达时刻、防止客户端积压和 coordinated omission。优先小矩阵筛选，避免无限跑满所有组合。

## Metric definitions

- QPS = 成功请求 / 稳态测量墙钟秒；QPS/GPU 同时报告。
- Input/output/total TPS = 成功请求对应 token 数 / 同一墙钟窗口；input TPS 不是独立 prefill kernel 吞吐。
- TTFT = 首 token 到达 - 实际发送；另存计划到达→发送的客户端排队。
- TPOT = (最后 token 到达 - 首 token 到达)/(输出 token 数 - 1)，仅输出至少 2 token；不是 chunk ITL 的平均值。
- E2E = 完成 - 发送，保留协议收尾时间；各请求分位数线性插值，n 很小时 P99 不稳定。
- 非 streaming 数据可测 E2E，TTFT/TPOT 缺失写 null，不能从总时间推算。
- 显存是实际 peak allocated/reserved/device-used 中哪一种必须写明；不能把配置的 utilization 当实测。
- Goodput 依赖冻结 SLO 与逐请求数据；当前汇总工具不自动计算 SLO goodput。

## Event interface

每行 JSON：`id, kind, status, start_s, end_s, input_tokens, output_tokens, token_times_s`。时间为同一测量窗口起点的单调时钟秒；错误请求保留 id/status/start/end。`kind` 为 synthetic 或 measured，不能混用。无法逐 token 计时设 `token_times_s: null`；一个 SSE chunk 可能包含多个 token，不可假装逐 token 时间。

```bash
python3 scripts/lab.py summarize benchmarks/workloads/synthetic-events.jsonl --duration 4
```

单轮汇总不是“完整三轮通过”的证明。完整 run 另存环境、命令、退出码、每轮 manifest 和质量 evidence。

## Quality-gated comparison

参考 [synthetic-runs.json](workloads/synthetic-runs.json) 的字段。`contract` 必须完全一致，质量 gate 支持 higher/lower 和 absolute/relative。`expected/succeeded/failed` 为三轮总计，`rounds` 至少 3。必须 measured、完整、exit 0、无 fallback、质量切片与 SLO 已由外部 evaluator 审核通过、有 evidence 和 quality_evidence 才进入比较。

质量无标签时不填写业务 quality；相似度仅为辅助屏查。相对损失以 baseline 绝对值为分母；baseline 为零必须选绝对阈值。quality 用统一非负标量，多个指标/切片先由 evaluator 通过所有门槛。

工具对质量、QPS/GPU、E2E P99、peak GPU GiB 求非支配集合，保留 tradeoff 和相等候选。不会处理置信区间或自动选择生产配置；`evidence` 字段是外部回执引用，工具不验证其存储真实性。接入正式 Agent 时需验证回执 hash、样本覆盖、切片与 SLO，不能靠手填布尔值完成验收。

## Evidence layout

大文件放外部存储或 `results/raw/`（已忽略）。Git 仅提交脱敏摘要、manifest/hash、合同和报告。协议冻结后修改必须新 ID；失败 run 不覆盖。部署验收还需 Triton live/ready/model-ready、真实协议请求与回滚，不属于 compare 工具。
