# 05 远程验证 · 相似提示词，为什么没有缓存收益？

状态：**designed / not-run**。本课 CPU 实验不依赖此步骤。此文件是待具体化的课程验证协议，不是已冻结的业务 RunRecord。

## 问题与单变量

两个 prompt 语义非常相似，但第一行的时间戳不同。为什么可能没有 prefix cache 命中？

自变量：精确 token 前缀分布，或 cache cold/warm；分别单变量。预先写出方向预测与竞争解释，禁止用量化/数据/并发多个变化共同解释单一原因。

## 执行前门槛

未来实际执行前读取两份本机 GPU inventory，过期一小时或长任务前按用户规定顺序刷新；本次不 SSH、不启动 GPU。选定 exact checkpoint/processor/template hash、镜像、vLLM commit、硬件/GPU数及数据与 evaluator 后，复制 [实验模板](../../templates/experiment.md) 为独立协议，锁定参数、质量阈值和资源期限。

## 最小设计

固定同一 tokenized prompt 集合，cold/warm 分开记录；先改变公共前缀比例，再独立改变容量压力。缓存开关/清空操作依据固定版本命令，不能拿 warm candidate 对 cold baseline。

baseline/candidate 同数据、采样、输出 cap、EOS、缓存定义和计时边界；10 个固定 warmup 不计入统计，3 轮完整样本。交错运行，profiler 单独采集；客户端和采样实现也记录版本。

## 应收证据

cached tokens、prefix hit、prefill 时间、TTFT、输出长度、QPS 和缓存状态。保存命令、PID/PGID、退出码、样本 expected/success/failure、原始 evidence hash 和清理回执。输入 TPS、输出 TPS、总 TPS 分列。

## 停止与解释

OOM、缺样本、质量失败、意外 fallback、未授权资源或环境改变时停止并保留失败证据。无标签仅能做一致性/机制检查；不得选择生产候选。即使预测正确也检查其他解释；真实结果可与 toy 趋势不同。
