# 2027-kaoyan-english-redbook-json
> 2027考研英语红宝书（正序版）单词数据，来自网络流传的PDF文件，提供结构化JSON格式与批量提取脚本

---

## 项目简介
本项目整理了 **2027考研英语红宝书（正序版）** 的完整词汇数据，通过Python脚本从PDF版本批量提取并结构化，生成可直接用于开发、学习的JSON格式单词表，数据来自网络流传的不背单词APP的2027红宝书PDF文件。

## 数据格式
`words.json` 中每条单词数据结构如下：
```json
[
  {
    "page": 1,
    "index": 1,
    "word": "radiate",
    "meaning": "vt. vi. 散发，流露；发出 (光、辐射等) vi. 呈辐射状发散 (或伸展)"
  }
]
```
- `page`: 单词所在PDF页码
- `index`: 页面内单词序号
- `word`: 英文单词
- `meaning`: 中文释义（包含词性、多个义项）

## 文件说明
| 文件 | 说明                               |
|------|----------------------------------|
| `2027考研英语红宝书-不背单词版.pdf` | 来自网络流传的不背单词APP的2027红宝书PDF文件（正序版） |
| `script.py` | 批量提取PDF单词并生成JSON的Python脚本        |
| `words.json` | 提取完成的结构化单词数据（完整词汇表）              |
| `LICENSE` | 开源协议文件                           |

## 使用方法
### 1. 直接使用JSON数据
直接下载 `words.json` 文件，即可在任何支持JSON的环境中使用（如前端项目、后端接口、单词学习工具等）。

### 2. 运行提取脚本（自定义提取）
如果需要基于原PDF重新提取或修改提取逻辑，可运行 `script.py`：
#### 环境依赖
- Python 3.6+
- 依赖库安装：
  ```bash
  # 文本型PDF依赖（推荐，适用于可复制文字的PDF）
  pip install PyPDF2 regex

  # 图片型PDF额外依赖（若为扫描件PDF，需额外安装）
  pip install pdf2image pytesseract pillow
  ```
  > 图片型PDF需额外安装 [Tesseract OCR引擎](https://github.com/UB-Mannheim/tesseract/wiki) 并配置路径。

#### 运行脚本
1. 将 `2027考研英语红宝书-不背单词版.pdf` 与 `script.py` 放在同一目录
2. 修改 `script.py` 中的PDF路径为实际文件路径
3. 执行脚本：
   ```bash
   python script.py
   ```
4. 脚本运行完成后，会在当前目录生成 `words.json` 结果文件。

## 开源协议
本项目采用 **MIT协议** 开源：

## 注意事项
1. 本项目仅为学习交流使用，**请勿用于商业用途**
2. PDF原文件版权归原作者/出版社所有，本项目仅提供结构化提取数据与提取工具
3. 若数据存在错误，欢迎提交Issue或PR修正

---

## 贡献
欢迎提交PR优化提取脚本、修正单词数据，或补充更多年份/版本的红宝书数据。

---
