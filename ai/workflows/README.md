# Workflow

1. 研究者创建 task：问题、预测、约束、证据边界。
2. AI 返回最小方案与反例；研究者封存协议。
3. AI 实现 prototype/benchmark，先验证 correctness oracle。
4. 按指定远程环境执行，记录失败、fallback、完整样本和清理。
5. 分析工具筛选可比且质量合格的结果；研究者解释差异。
6. AI 审阅结论是否超出证据，更新笔记与下一步。

权限与真实资源来自当次用户配置。没有 GPU 时继续公式、源码与实验设计，状态保持 designed。
