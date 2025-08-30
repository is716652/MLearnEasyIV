---
# 请选择一个模块类别（保留一个并删除其余）：
module: A|B|C
# 子类，例如：微积分 / 线性代数 / 概率统计 / 监督学习 / 无监督学习 / 优化等
subcategory: 在此填写子类
# 标题必须全局唯一，用于去重/更新判断
title: 在此填写标题（必须唯一）
# 标签可选，逗号分隔或列表形式
tags: [示例, 可删除]
# 可选：如需将公式以键值形式显式管理，可开启下方示例
# formulas:
#   law_large_numbers: "\\lim_{n\\to\\infty} \\bar{X}_n = \\mu"
#   bayes: "\\mathbb{P}(A|B) = \\frac{\\mathbb{P}(B|A)\\mathbb{P}(A)}{\\mathbb{P}(B)}"
---

这里是正文内容（Markdown）。建议结构化编写：先给出定义/定理，再给直观解释与例子，最后给练习或扩展阅读。

行内公式示例：$a^2 + b^2 = c^2$。

## 块级 LaTeX 公式
使用块级公式（会被自动提取并保留到内容中）：
$$
E = mc^2
$$

## Python 代码示例
```python
import numpy as np
np.mean([1, 2, 3])
```

## 图片示例（二选一）
- 外链图片（最省事）：
  ![chart_1](https://example.com/your_image.png)
- 本地相对路径（导入时需要提供 base_dir，指向图片相对的根目录）：
  ![chart_2](images/your-local-image.png)

---
使用小贴士与校验清单（可阅读后删除）
- YAML 头部与尾部必须是三条短横线 ---
- 请选择并仅保留一个 module（A|B|C），删除另两个
- title 必须存在且全局唯一；若重复且未开启覆盖，将被跳过
- 行内公式用 $...$，块级公式用 $$...$$，注意成对闭合
- 代码块使用 ```python 与 ``` 成对包裹
- 如果使用本地相对图片路径，导入时请一并提供 base_dir（绝对路径）