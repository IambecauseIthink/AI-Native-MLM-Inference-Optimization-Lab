# 六个交互实验

这些 HTML 是对话用 fragment，不是完整网站。每个选择器对应 Python 预先计算的确定性场景，浏览器不另写一套模型公式，也不请求网络。

- [01](lesson-01.html) · [02](lesson-02.html) · [03](lesson-03.html) · [04](lesson-04.html) · [05](lesson-05.html) · [06](lesson-06.html)

## 使用

对助手说“展示第 01 课交互图”，助手在对话里展示相应 fragment。学习正文的公式与图内假设一起阅读。图表更新不会修改学习进度。

可选离线预览：

```bash
python3 scripts/preview_lesson.py --id 01 --output /tmp/lesson-01-preview.html
```

然后用浏览器打开输出文件；这是 CPU 可视化，不是模型 benchmark。默认拒绝覆盖输出文件，不需要网络或安装依赖。

## 维护

公式和场景在 Python `scripts/lessons.py`；页面由模板及所有有限 preset 生成。修改后运行：

```bash
python3 scripts/build_lesson_visuals.py
python3 scripts/build_lesson_visuals.py --check
```

测试逐个核对嵌入场景与 Python 输出；浏览器检查选择器、指标变化、窄屏与明暗主题。选择器限定在课程设计的取值，不声称能模拟任意生产配置。

可选浏览器 QA（维护者环境已安装 Playwright/Chrome 时）：先用 preview_lesson 为六课生成到同一目录的 `01.html` … `06.html`，再执行 `LESSON_BROWSER_CHANNEL=chrome node scripts/check_lesson_browser.cjs /absolute/preview-directory`。它检查 360/736px、明暗主题、选择器更新和水平溢出，截图仅写入该预览目录；不是上课前置依赖。
