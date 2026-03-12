## mrxn jswz 抓取脚本（Playwright）

使用无头浏览器抓取 `https://mrxn.net/jswz`，导出为 **Markdown**，并将文章图片内联为 base64 data URI（单文件可离线查看）。

### 本地运行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install --with-deps chromium

python scripts/crawl_mrxn_jswz.py --output output/jswz
```

### 输出结果

- `output/jswz/markdown/*.md`（按文章标题清洗后命名）
- `output/jswz/manifest.json`
- `output/jswz/crawl_report.json`

### 说明

- 仅导出 Markdown，不再输出 HTML 文件。
- 每次抓取前会清理旧的 `output/jswz`，避免历史 md/html 混入新结果。
- 图片会优先读取 `src/data-src/data-original/srcset`，先按“每张图打开一个无头浏览器页面”方式抓取；若失败再回退到 request API 抓取，成功后写入 Markdown（base64 data URI）。
- 工作流会把 `output/jswz` 打包为 `jswz-output.tgz` 并上传 artifact，同时推送到 `mrxn-jswz-archive` 分支。

### 快速验证工作流（仅抓 10 篇）

已新增：`.github/workflows/crawl-mrxn-jswz-smoke-10.yml`

- 仅支持手动触发（`workflow_dispatch`）
- 最多抓取 10 篇文章（`--max-articles 10`）
- 会先清理 `output/jswz-smoke10`，再抓取 10 篇并上传测试 artifact（`jswz-smoke10-output`）
- smoke 工作流会在日志中打印每篇 Markdown 的 base64 图片数量与大小统计（sum/max/min chars）用于调试
- 会把 smoke 结果推送到独立分支 `mrxn-jswz-smoke10`，方便核对是否为最新下载

本地也可快速验证：

```bash
python scripts/crawl_mrxn_jswz.py --output output/jswz-smoke10 --max-articles 10
```
