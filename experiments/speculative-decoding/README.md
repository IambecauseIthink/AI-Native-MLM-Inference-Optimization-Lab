# speculative-decoding

状态：designed；无实测。

## Question

接受率能否覆盖 draft 成本？

## Matrix

draft length × concurrency × 输出长度。

## Controls

target sampling、draft 资源预算、任务集合。运行顺序交错或随机化；baseline/candidate 各 3 轮完整数据；profiler 独立运行。

## Metrics and falsification

acceptance、目标步数、TPOT、QPS/GPU、质量。预先填写质量阈值、SLO、最小有意义差异、失败率和不确定性估计。若收益落在噪声内或关键质量切片失败，拒绝推荐。

## Run contract

从 [模板](../../templates/experiment.md) 创建带 ID 的协议；保存 raw events、退出码和环境 hash。GPU 资源与数据尚未指定，不能直接执行这些组合。
