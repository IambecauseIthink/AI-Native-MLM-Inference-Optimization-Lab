# batching

状态：designed；无实测。

## Question

权重复用何时不再增加吞吐？

## Matrix

concurrency 1/4/16/32；另组 scheduler limits。

## Controls

输入/输出分布、cache、资源数。运行顺序交错或随机化；baseline/candidate 各 3 轮完整数据；profiler 独立运行。

## Metrics and falsification

QPS、TPOT、memory、排队。预先填写质量阈值、SLO、最小有意义差异、失败率和不确定性估计。若收益落在噪声内或关键质量切片失败，拒绝推荐。

## Run contract

从 [模板](../../templates/experiment.md) 创建带 ID 的协议；保存 raw events、退出码和环境 hash。GPU 资源与数据尚未指定，不能直接执行这些组合。
