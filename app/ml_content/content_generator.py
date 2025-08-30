import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from typing import Dict, Any
from .math_content import MathContentGenerator
from .ml_content import MLContentGenerator


class ContentGenerator:
    def __init__(self):
        self.math_generator = MathContentGenerator()
        self.ml_generator = MLContentGenerator()

    def generate_content(self, module: str, subcategory: str, title: str) -> Dict[str, Any]:
        if module == "math":
            return self.math_generator.generate_math_content(subcategory, title)
        elif module == "ml":
            return self.ml_generator.generate_ml_content(subcategory, title)
        elif module == "dl":
            return self._generate_dl_content(subcategory, title)
        else:
            return self._generate_default_content()

    def _generate_dl_content(self, subcategory: str, title: str) -> Dict[str, Any]:
        return {
            "content_body": "深度学习内容正在开发中...",
            "python_code": "# 深度学习代码示例",
            "formulas": {},
            "charts_data": {},
        }

    def _generate_default_content(self) -> Dict[str, Any]:
        return {
            "content_body": "内容正在开发中...",
            "python_code": "# 代码示例待添加",
            "formulas": {},
            "charts_data": {},
        }


# 兼容保留（不再使用）的占位类，避免与真实实现冲突
class _LegacyMLContentGenerator:
    def generate_ml_content(self, subcategory: str, title: str) -> Dict[str, Any]:
        return {
            "content_body": "## 机器学习内容占位\n即将上线。",
            "python_code": "# TODO: 添加 ML 示例代码",
            "formulas": {},
            "charts_data": {},
        }


# 兼容保留（不再使用）的旧数学占位实现，真实实现位于 math_content.py
class _LegacyMathContentGenerator:
    def generate_math_content(self, subcategory: str, title: str) -> Dict[str, Any]:
        if "向量" in subcategory:
            return self._generate_vector_content()
        elif "矩阵" in subcategory:
            return self._generate_matrix_content()
        elif "导数" in subcategory:
            return self._generate_derivative_content()
        else:
            # 默认返回向量示例
            return self._generate_vector_content()

    def _generate_vector_content(self) -> Dict[str, Any]:
        content_body = (
            "## 向量的基本概念\n\n"
            "向量是既有大小又有方向的量，可以用箭头表示。在机器学习中，向量常用于表示特征。\n\n"
            "### 生活化类比\n"
            "想象一下快递地址：省、市、区、街道、门牌号，这就像一个5维向量！\n\n"
            "### 数学表示\n"
            "向量通常表示为：$\\vec{v} = \\begin{bmatrix} v_1 \\ v_2 \\ \\vdots \\ v_n \\end{bmatrix}$\n"
        )

        python_code = (
            "import numpy as np\n\n"
            "# 创建向量\n"
            "vector_1d = np.array([1, 2, 3, 4, 5])\n"
            "print(\"一维向量:\", vector_1d)\n"
            "print(\"向量形状:\", vector_1d.shape)\n\n"
            "# 向量运算\n"
            "vector_a = np.array([1, 2, 3])\n"
            "vector_b = np.array([4, 5, 6])\n\n"
            "print(\"向量加法:\", vector_a + vector_b)\n"
            "print(\"向量点积:\", np.dot(vector_a, vector_b))\n"
        )

        chart_data = self._create_vector_visualization()

        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "vector_definition": "\\vec{v} = \\begin{bmatrix} v_1 \\ v_2 \\ \\vdots \\ v_n \\end{bmatrix}",
                "dot_product": "\\vec{a} \\cdot \\vec{b} = \\sum_{i=1}^{n} a_i b_i",
            },
            "charts_data": chart_data,
        }

    def _create_vector_visualization(self) -> Dict[str, Any]:
        fig, ax = plt.subplots(figsize=(6, 4))
        vectors = np.array([[0, 0, 2, 3], [0, 0, 3, 1], [0, 0, 1, 4]])
        for v in vectors:
            ax.arrow(v[0], v[1], v[2], v[3], head_width=0.1, head_length=0.15, fc='blue', ec='blue')
        ax.set_xlim(-1, 5)
        ax.set_ylim(-1, 5)
        ax.set_xlabel('X轴')
        ax.set_ylabel('Y轴')
        ax.set_title('向量可视化')
        ax.grid(True)
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100)
        buffer.seek(0)
        img_str = base64.b64encode(buffer.read()).decode()
        plt.close()
        return {
            "type": "matplotlib",
            "data": img_str,
            "title": "向量可视化示例",
        }

    def _generate_matrix_content(self) -> Dict[str, Any]:
        return self._generate_vector_content()

    def _generate_derivative_content(self) -> Dict[str, Any]:
        return self._generate_vector_content()