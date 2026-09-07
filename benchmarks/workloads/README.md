# Workloads

synthetic-events 用于手算指标：2 成功/1 失败、4 秒窗口、QPS 0.5、input TPS 5、output TPS 1、total TPS 6。它不是模型运行结果。

synthetic-runs 用于验证 compare 拒绝虚构成绩：baseline 和 candidate 都 synthetic，所以 frontier 必须为空。

业务 manifest 需样本 ID/hash、dataset revision、输入/输出/视觉长度分布、分层采样方式、权限与 evaluator。生成器的字符重复次数不是 token 数，需固定 tokenizer 后统计。公开与业务数据分别报告。
