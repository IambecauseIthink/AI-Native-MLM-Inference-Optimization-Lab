# Experiment · ID / question

Status: designed。Owner、日期、关联笔记、不可变协议 ID。

## Hypothesis

如果改变 X，Y 将变化多少/什么方向，因为 Z；可证伪条件与竞争解释。

## Baseline and controls

明确当前 vLLM baseline；模型 revision/hash、tokenizer/processor/template、数据 manifest hash、业务 evaluator hash、runtime commit、镜像 digest、driver/CUDA/GPU/拓扑、协议与资源数。

## Treatment and matrix

自变量、取值、固定条件、顺序随机化/交错、最小消融。跨模型/硬件单独 cohort。列出候选参数和允许变化的字段。

## Workload and measurement

输入/输出/visual token 分布、EOS 与 max_tokens、sampling、seed、warmup、3 轮完整样本、closed/open-loop、到达率、并发、timeout、retry、缓存 cold/warm、质量任务切片。profiler 独立运行。

## Quality and SLO gate

指标名、方向、单位、绝对/相对损失上限、最小切片要求、置信区间；无标签只能做一致性检查。TTFT/E2E/TPOT SLO 与错误率上限在运行前固定。

## Execution and stop

精确命令、环境配置、超时、PID/PGID、日志位置、清理步骤。OOM/业务质量失败/缺样本/环境变化时停止；保持失败记录。远程运行前刷新本机 GPU inventory。

## Results

not-measured。完整样本数、退出码、错误、证据 URI/hash、每轮指标和不确定性。

## Interpretation and decision

预测是否成立、替代解释、Pareto、成本、适用边界、下一步。selected candidate 在质量验收前为 null。
