# 03 远程验证 · 权重放得下，为什么还 OOM？

状态：**designed / not-run**。本课 CPU 实验不依赖此步骤。此文件是待具体化的课程验证协议，不是已冻结的业务 RunRecord。

## 问题与单变量

假设 GPU 容量 64 GiB、权重 54 GiB、其他开销 6 GiB，剩下 4 GiB。请求变长后为何可能装不下？

自变量：sequence length、KV dtype 或 block size，分别单变量。预先写出方向预测与竞争解释，禁止用量化/数据/并发多个变化共同解释单一原因。

## 执行前门槛

未来实际执行前读取两份本机 GPU inventory，过期一小时或长任务前按用户规定顺序刷新；本次不 SSH、不启动 GPU。选定 exact checkpoint/processor/template hash、镜像、vLLM commit、硬件/GPU数及数据与 evaluator 后，复制 [实验模板](../../templates/experiment.md) 为独立协议，锁定参数、质量阈值和资源期限。

## 最小设计

读取 exact config 和每层类型，预测 raw KV 与分页数量；在指定 GPU 上测固定长度/并发下的 allocator、device memory、peak 与请求完成状态。FP8 KV 另做长上下文质量切片。

baseline/candidate 同数据、采样、输出 cap、EOS、缓存定义和计时边界；10 个固定 warmup 不计入统计，3 轮完整样本。交错运行，profiler 单独采集；客户端和采样实现也记录版本。

## 应收证据

raw 预测/物理分配差额、峰值显存、KV 使用率、完整请求、质量切片及吞吐。保存命令、PID/PGID、退出码、样本 expected/success/failure、原始 evidence hash 和清理回执。输入 TPS、输出 TPS、总 TPS 分列。

## 停止与解释

OOM、缺样本、质量失败、意外 fallback、未授权资源或环境改变时停止并保留失败证据。无标签仅能做一致性/机制检查；不得选择生产候选。即使预测正确也检查其他解释；真实结果可与 toy 趋势不同。
