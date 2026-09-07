# Research workspace instructions

- 中文解释为主，保留精确英文术语；先陈述假设与可证伪预测。
- 遵循用户当前要求；不要把阅读记录、模拟结果或命令启动写成 measured / quality-passed / deployed。
- 修改前阅读相关实验协议。没有批准的变更，不修改冻结的 workload、token cap 或质量阈值。
- 源码引用使用 repository + commit + file + symbol；latest 链接只用于导航。
- 所有论文复现必须包含同 workload、同协议的 vLLM baseline。
- Mac 只用于文档、静态分析、CPU 工具和 SSH 编排；不得在本地加载模型或运行 GPU benchmark/profiler。
- 远程工作前读取用户维护的两份 GPU inventory，过期一小时或启动长任务前按用户规定顺序刷新。具体本机路径放 local 配置，不把内部地址写入 Git。
- 一次只改变一个解释变量；隔离 profiler、辅助负载和正式性能实验。
- 原始证据不可覆盖；失败、未完成、缺标签与 fallback 必须显式记录。
- 不把已有生产 Agent 代码复制进本仓库；通过脱敏输入/输出契约集成。
- AI 可写代码、定位源码和反驳假设；研究者负责问题、协议、质量阈值、结果解释和生产决策。
- 运行 `python3 -m unittest discover -s tests -v`、`python3 scripts/check_links.py` 和 `git diff --check`。
