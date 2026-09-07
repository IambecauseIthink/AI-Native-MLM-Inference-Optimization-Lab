# 首期课程交付验证

日期：2026-09-07。该页描述课程工具验证，不是学习效果、模型性能或生产验收。

- 六课均有学习页、教师页、远程验证设计、独立 CLI 场景和交互图。
- `bash scripts/check.sh`：44 项测试通过；本地文档文件链接通过；六张图与 Python 预设完全一致。
- 399 个有限预设覆盖公式/模拟输入组合，全部为 synthetic 或 analytical-estimate，未输出 measured/质量通过/生产推荐。
- 浏览器检查：本地 Chrome 无头独立配置；6 课 × 360/736px × light/dark，共 24 个视图、88 次选择器变化；无 JavaScript 页面错误、无水平溢出。人工检查第 01 课宽屏和第 06 课窄屏截图。浏览器检查是本地验收，不声称在 CI 中运行。
- vLLM 源码导航：官方 v0.19.0 完整 commit 下对源码文本做 AST symbol 定位，记录文件 SHA256；未导入 vLLM、未加载权重、未验证 GPU dispatch。
- CI 将执行 CPU 测试、文档链接、可视化生成一致性和 Git 空白检查。实际远端结果见 [Actions](https://github.com/IambecauseIthink/AI-Native-MLM-Inference-Optimization-Lab/actions/workflows/check.yml) 的对应提交。

远程 GPU、业务 evaluator、Triton/vLLM 实测、论文复现和学员掌握程度均未在本次交付中宣称完成。
