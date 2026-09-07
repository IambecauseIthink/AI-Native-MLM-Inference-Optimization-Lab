# 01 远程验证 · 两个服务，谁真的更快？

状态：**designed / not-run**。本课 CPU 实验不依赖此步骤。此文件是待具体化的课程验证协议，不是已冻结的业务 RunRecord。

## 问题与单变量

同样 8 个请求，B 更快处理完全部请求，但是中位请求体验更差。选 A 还是 B？

自变量：请求并发；其他模型/采样/token cap/cache 不变。预先写出方向预测与竞争解释，禁止用量化/数据/并发多个变化共同解释单一原因。

## 执行前门槛

未来实际执行前读取两份本机 GPU inventory，过期一小时或长任务前按用户规定顺序刷新；本次不 SSH、不启动 GPU。选定 exact checkpoint/processor/template hash、镜像、vLLM commit、硬件/GPU数及数据与 evaluator 后，复制 [实验模板](../../templates/experiment.md) 为独立协议，锁定参数、质量阈值和资源期限。

## 最小设计

固定相同模型、硬件、32 个或更多公开请求及真实长度分布，先验证 streaming 计时，再冻结完整样本和并发配置。分别做 closed-loop 容量与固定到达序列；记录计划到达、实际发送、首 token、末 token、完成、错误。

baseline/candidate 同数据、采样、输出 cap、EOS、缓存定义和计时边界；10 个固定 warmup 不计入统计，3 轮完整样本。交错运行，profiler 单独采集；客户端和采样实现也记录版本。

## 应收证据

成功 QPS、TTFT/TPOT/E2E 分位数、输入/输出 TPS、错误率和客户端积压。保存命令、PID/PGID、退出码、样本 expected/success/failure、原始 evidence hash 和清理回执。输入 TPS、输出 TPS、总 TPS 分列。

## 停止与解释

OOM、缺样本、质量失败、意外 fallback、未授权资源或环境改变时停止并保留失败证据。无标签仅能做一致性/机制检查；不得选择生产候选。即使预测正确也检查其他解释；真实结果可与 toy 趋势不同。
