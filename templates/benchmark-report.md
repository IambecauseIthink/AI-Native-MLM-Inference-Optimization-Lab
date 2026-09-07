# Benchmark report · ID

状态：not-measured。报告日期、协议 ID、baseline/candidate run IDs。

## Business question and contract

业务目标、质量阈值、SLO、固定 workload/环境/资源、允许差异。

## Provenance and completion

模型/数据/evaluator/runtime hashes、GPU/拓扑/镜像、命令、每轮 expected/succeeded/failed、退出码、原始日志与 hash。缺样本不得藏在平均值里。

## Four-dimensional comparison

| Run | Quality/切片 | QPS / QPS per GPU | Input / output / total TPS | TTFT P50/95/99 | TPOT P50/95/99 | E2E P50/95/99 | Peak GiB | Errors |
|---|---|---|---|---|---|---|---|---|
| baseline | not-measured | — | — | — | — | — | — | — |

## Why and uncertainty

每轮结果、差异范围/CI、实际 token 长度、kernel dispatch、排队、profiler；理论估计与实测分列。

## Quality gate and Pareto

淘汰理由、非支配候选、SLO goodput、成本。Pareto 不自动产生唯一推荐；预先声明选择偏好。

## Production feasibility

灰度方案、回滚配置、健康检查与真实请求回执、监控、维护成本。未部署写 not-deployed。
