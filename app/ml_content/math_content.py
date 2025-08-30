import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sympy as sp
from io import BytesIO
import base64
import math
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class MathContentGenerator:
    def __init__(self):
        self.x, self.y, self.z = sp.symbols('x y z')

    # 统一公式结构：latex/explanation/symbols
    def _formula(self, latex: str, explanation: str = "", symbols: Dict[str, str] = None) -> Dict[str, Any]:
        return {
            "latex": latex,
            "explanation": explanation,
            "symbols": symbols or {}
        }

    def generate_math_content(self, subcategory: str, title: str) -> Dict[str, Any]:
        """根据子分类和标题生成数学内容"""
        content_methods = {
            # 基础概念
            "常量": self._generate_constant_content,
            "变量": self._generate_variable_content,
            "函数": self._generate_function_content,

            # 代数运算
            "幂": self._generate_power_content,
            "平方根": self._generate_sqrt_content,
            "多项式函数": self._generate_polynomial_content,

            # 特殊函数 / 运算
            "三角函数": self._generate_trigonometric_content,
            "求和": self._generate_sum_content,
            "求和运算": self._generate_sum_content,
            "总和": self._generate_sum_content,
            "乘积": self._generate_product_content,
            "乘积运算": self._generate_product_content,
            "随机数": self._generate_random_content,
            "随机数生成": self._generate_random_content,
            "绝对值": self._generate_absolute_content,
            "绝对值函数": self._generate_absolute_content,

            # 线性代数
            "标量与向量": self._generate_scalar_vector_content,
            "矩阵与张量": self._generate_matrix_tensor_content,
            "行列向量": self._generate_row_column_vector_content,
            "行列向量转换": self._generate_row_column_vector_content,
            "向量的转置": self._generate_vector_transpose_content,
            "向量的加减": self._generate_vector_operations_content,
            "向量的点积和范数": self._generate_dot_norm_content,
            "矩阵的积": self._generate_matrix_multiplication_content,
            "矩阵的乘法运算": self._generate_matrix_multiplication_content,

            # 微积分与应用
            "导数": self._generate_derivative_content,
            "偏导数": self._generate_partial_derivative_content,
            "损失函数": self._generate_loss_function_content,
            "激活函数": self._generate_activation_function_content,
        }

        # 优先进行精确匹配（按关键字长度降序），避免短词抢占
        texts = [(title or ""), (subcategory or "")]
        for key, method in sorted(content_methods.items(), key=lambda kv: len(kv[0]), reverse=True):
            for t in texts:
                if t == key:
                    return method()

        # 其次进行包含匹配（按关键字长度降序），确保更具体的词优先
        for key, method in sorted(content_methods.items(), key=lambda kv: len(kv[0]), reverse=True):
            for t in texts:
                if key in t:
                    return method()

        # 默认内容
        return self._generate_default_content()

    def _create_chart_base64(self, fig) -> str:
        """将matplotlib图表转换为base64字符串"""
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        return img_str

    # 基础概念
    def _generate_constant_content(self) -> Dict[str, Any]:
        content_body = (
            "\n## 常量（Constants）\n\n"
            "### 生活化类比\n"
            "想象一下数学中的π（圆周率）≈ 3.14159，它是一个固定不变的值，就像你的生日一样永远不会改变。\n\n"
            "### 理论讲解\n"
            "常量是程序中固定不变的值，一旦定义就不能修改。在数学和编程中，常量用于表示不会改变的数值。\n\n"
            "### 数学表示\n"
            "- 数学常量：$\\pi$, $e$, $\\phi$ (黄金比例)\n"
            "- 物理常量：$c$ (光速), $G$ (万有引力常数)\n"
        )
        python_code = (
            "\n# Python中的常量表示\n"
            "PI = 3.141592653589793\n"
            "E = 2.718281828459045\n"
            "SPEED_OF_LIGHT = 299792458  # 光速，单位m/s\n\n"
            "print(f\"圆周率π: {PI}\")\n"
            "print(f\"自然常数e: {E}\")\n"
            "print(f\"光速c: {SPEED_OF_LIGHT} m/s\")\n\n"
            "# 在Python中，通常用全大写字母表示常量（约定俗成）\n"
            "GRAVITY = 9.8  # 重力加速度\n"
            "print(f\"重力加速度g: {GRAVITY} m/s²\")\n\n"
            "# 注意：Python没有真正的常量，这只是命名约定\n"
            "# 实际开发中应该避免修改这些\"常量\"值\n"
        )
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "pi": self._formula(
                    r"\pi \approx 3.141592653589793",
                    "圆的周长与直径之比，是最常见的数学常数。",
                    {"\\pi": "圆周率常数"}
                ),
                "e": self._formula(
                    r"e \approx 2.718281828459045",
                    "自然对数的底，在指数增长与连续复利中广泛出现。",
                    {"e": "自然常数，欧拉数"}
                )
            },
            "charts_data": {},
        }

    def _generate_variable_content(self) -> Dict[str, Any]:
        content_body = (
            "\n## 变量（Variables）\n\n"
            "### 生活化类比\n变量就像数学中的未知数x，或者编程中的存储容器。比如：年龄 = 25，这里的\"年龄\"就是一个变量。\n\n"
            "### 理论讲解\n变量是存储数据的容器，其值可以在程序执行过程中改变。每个变量都有名称和数据类型。\n\n"
            "### 变量类型\n- 整型 (int)\n- 浮点型 (float)\n- 字符串 (str)\n- 布尔型 (bool)\n"
        )
        python_code = (
            "\n# 变量定义和赋值\n"
            "age = 25\nname = \"张三\"\nheight = 1.75\nis_student = True\n\n"
            "print(f\"姓名: {name}\")\nprint(f\"年龄: {age}岁\")\nprint(f\"身高: {height}米\")\nprint(f\"是否是学生: {is_student}\")\n\n"
            "# 变量重新赋值\n"
            "age = 26\nprint(f\"明年年龄: {age}岁\")\n\n"
            "# 多重赋值\n"
            "x, y, z = 1, 2, 3\nprint(f\"x={x}, y={y}, z={z}\")\n"
        )
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "variable_definition": self._formula(
                    r"x = 5,\quad y = 3.14,\quad z = \\text{'hello'}",
                    "变量是可变化的数据容器，上式展示了不同类型变量的示例。",
                    {"x": "整数变量", "y": "浮点变量", "z": "字符串变量"}
                )
            },
            "charts_data": {},
        }

    def _generate_function_content(self) -> Dict[str, Any]:
        content_body = (
            "\n## 函数（Functions）\n\n"
            "### 生活化类比\n函数就像一台自动售货机：你投入参数，它返回结果。\n\n"
            "### 理论讲解\n函数是一段可重复使用的代码块，接受输入，进行处理，然后返回输出。\n"
        )
        python_code = (
            "\n# 函数定义和调用\n"
            "def square(x):\n    return x ** 2\n\n"
            "def add(a, b):\n    return a + b\n\n"
            "print(square(5))\nprint(add(3, 7))\n"
        )
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "function_definition": self._formula(
                    r"f(x) = x^2",
                    "将输入 x 映射为它的平方，是最简单的函数示例。",
                    {"f(x)": "函数符号", "x": "自变量"}
                ),
                "function_call": self._formula(
                    r"f(2) = 4",
                    "当把 2 代入 f(x)=x^2 时，输出为 4。",
                    {"2": "实参", "4": "返回值"}
                )
            },
            "charts_data": {},
        }

    # 代数运算
    def _generate_power_content(self) -> Dict[str, Any]:
        content_body = (
            "\n## 幂运算（Power）\n\n"
            "幂运算表示一个数自乘若干次，如 2³ = 8。\n"
        )
        python_code = (
            "\nimport math\n"
            "print(2 ** 3)\nprint(5 ** 2)\nprint(math.pow(2, 3))\n"
        )
        fig, ax = plt.subplots(figsize=(8, 5))
        x = np.linspace(0, 5, 100)
        y1 = x ** 2
        y2 = x ** 3
        y3 = 2 ** x
        ax.plot(x, y1, label='$y = x^2$')
        ax.plot(x, y2, label='$y = x^3$')
        ax.plot(x, y3, label='$y = 2^x$')
        ax.legend(); ax.grid(True); ax.set_title('幂函数图像')
        chart_data = self._create_chart_base64(fig)
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "power_definition": self._formula(
                    r"a^n = \\underbrace{a \\times a \\times \\cdots \\times a}_{n\\text{次}}",
                    "幂运算表示将同一个底数 a 连乘 n 次。",
                    {"a": "底数", "n": "指数（正整数）"}
                ),
                "negative_exponent": self._formula(
                    r"a^{-n} = \\frac{1}{a^n}",
                    "负指数表示倒数的正幂。",
                    {"a": "底数", "n": "指数（正整数）"}
                )
            },
            "charts_data": {"power_function": chart_data},
        }

    def _generate_sqrt_content(self) -> Dict[str, Any]:
        content_body = (
            "\n## 平方根（Square Root）\n\n"
            "平方根是一个数的1/2次方，例如 √16 = 4。\n"
        )
        python_code = (
            "\nimport math\nimport numpy as np\n"
            "print(math.sqrt(16))\nprint(16 ** 0.5)\n"
        )
        fig, ax = plt.subplots(figsize=(8, 5))
        x = np.linspace(0, 10, 100)
        y = np.sqrt(x)
        ax.plot(x, y, label='$y = \\sqrt{x}$')
        ax.fill_between(x, y, alpha=0.2)
        ax.legend(); ax.grid(True); ax.set_title('平方根函数图像')
        chart_data = self._create_chart_base64(fig)
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "sqrt_definition": self._formula(
                    r"\\sqrt{x} = x^{1/2}",
                    "平方根是将一个非负数映射到其平方等于原数的非负值。",
                    {"x": "被开方数"}
                )
            },
            "charts_data": {"sqrt_function": chart_data},
        }

    # 线性代数示例
    def _generate_vector_operations_content(self) -> Dict[str, Any]:
        content_body = (
            "\n## 向量的加减运算\n\n"
            "向量加减遵循分量相加/相减原则。\n"
        )
        python_code = (
            "\nimport numpy as np\n"
            "a = np.array([1,2,3]); b = np.array([4,5,6])\n"
            "print('A+B=', a+b); print('A-B=', a-b)\n"
        )
        fig, ax = plt.subplots(figsize=(8, 6))
        a = np.array([2, 3])
        b = np.array([3, 1])
        ax.quiver(0, 0, a[0], a[1], angles='xy', scale_units='xy', scale=1, color='r', label='A')
        ax.quiver(0, 0, b[0], b[1], angles='xy', scale_units='xy', scale=1, color='b', label='B')
        s = a + b
        ax.quiver(0, 0, s[0], s[1], angles='xy', scale_units='xy', scale=1, color='g', label='A+B')
        ax.set_xlim(-1, 6); ax.set_ylim(-1, 5); ax.set_aspect('equal')
        ax.grid(True); ax.legend(); ax.set_title('向量加减法几何意义')
        chart_data = self._create_chart_base64(fig)
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "vector_addition": self._formula(
                    r"\\vec{a}+\\vec{b} = [a_1+b_1, a_2+b_2]^T",
                    "同维度向量按分量相加组成新向量。",
                    {"\\vec{a}": "向量 a", "\\vec{b}": "向量 b", "a_i,b_i": "第 i 个分量"}
                ),
                "vector_subtraction": self._formula(
                    r"\\vec{a}-\\vec{b} = [a_1-b_1, a_2-b_2]^T",
                    "同维度向量按分量相减组成新向量。",
                    {"\\vec{a}": "向量 a", "\\vec{b}": "向量 b", "a_i,b_i": "第 i 个分量"}
                )
            },
            "charts_data": {"vector_operations": chart_data},
        }

    def _generate_activation_function_content(self) -> Dict[str, Any]:
        content_body = (
            "\n## 激活函数（Activation Functions）\n\n"
            "激活函数为神经网络引入非线性。\n"
        )
        python_code = (
            "\nimport numpy as np\n"
            "def sigmoid(x): return 1/(1+np.exp(-x))\n"
            "def relu(x): return np.maximum(0, x)\n"
            "def tanh(x): return np.tanh(x)\n"
        )
        x = np.linspace(-5, 5, 200)
        def sigmoid(arr):
            return 1/(1+np.exp(-arr))
        def relu(arr):
            return np.maximum(0, arr)
        def tanh(arr):
            return np.tanh(arr)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        ax1.plot(x, sigmoid(x), label='Sigmoid')
        ax1.plot(x, relu(x), label='ReLU')
        ax1.plot(x, tanh(x), label='Tanh')
        ax1.grid(True); ax1.legend(); ax1.set_title('常用激活函数')
        sig = sigmoid(x)
        ax2.plot(x, sig*(1-sig), label='Sigmoid导数', color='red')
        ax2.plot(x, sig, label='Sigmoid', color='blue')
        ax2.grid(True); ax2.legend(); ax2.set_title('Sigmoid及其导数')
        chart_data = self._create_chart_base64(fig)
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "sigmoid": self._formula(
                    r"\\sigma(x) = \\frac{1}{1 + e^{-x}}",
                    "Sigmoid 函数把输入压缩到 (0,1) 的区间，常用于二分类概率。",
                    {"x": "实数输入", "\\sigma(x)": "输出概率"}
                ),
                "relu": self._formula(
                    r"\\text{ReLU}(x) = \\max(0, x)",
                    "ReLU 只保留正数部分，负数部分置零，计算高效。",
                    {"x": "实数输入"}
                ),
                "tanh": self._formula(
                    r"\\tanh(x) = \\frac{e^x - e^{-x}}{e^x + e^{-x}}",
                    "Tanh 将输入映射到 (-1,1) 区间，均值为 0。",
                    {"x": "实数输入"}
                ),
                "sigmoid_derivative": self._formula(
                    r"\\sigma'(x) = \\sigma(x)(1-\\sigma(x))",
                    "Sigmoid 的导数在靠近 0 或 1 时会很小，可能导致梯度消失。",
                    {"\\sigma(x)": "Sigmoid 函数值"}
                ),
            },
            "charts_data": {"activation_functions": chart_data},
        }

    # 未实现条目统一返回“开发中”占位
    def _placeholder(self, title: str) -> Dict[str, Any]:
        return {
            "content_body": f"{title} 内容正在开发中...",
            "python_code": "# 代码示例待添加",
            "formulas": {},
            "charts_data": {},
        }

    def _generate_polynomial_content(self):
        content_body = (
            "\n## 多项式函数\n\n"
            "多项式是由变量的非负整数次幂及其系数组成的表达式。\n\n"
            "### 一般形式\n"
            "n次多项式：$P(x) = a_n x^n + a_{n-1} x^{n-1} + \\cdots + a_1 x + a_0$\n\n"
            "### 常见类型\n"
            "- 一次多项式（线性）：$f(x) = ax + b$\n"
            "- 二次多项式（抛物线）：$f(x) = ax^2 + bx + c$\n"
        )
        python_code = (
            "\nimport numpy as np\nimport matplotlib.pyplot as plt\n\n"
            "# 定义多项式系数 [最高次, ..., 最低次, 常数项]\n"
            "poly1 = np.poly1d([1, -2, 1])  # x^2 - 2x + 1\n"
            "poly2 = np.poly1d([1, 0, -4])  # x^2 - 4\n\n"
            "print(f\"多项式1: {poly1}\")\n"
            "print(f\"多项式2: {poly2}\")\n"
            "print(f\"poly1(3) = {poly1(3)}\")\n\n"
            "# 绘制图像\n"
            "x = np.linspace(-3, 5, 100)\n"
            "plt.plot(x, poly1(x), label='$x^2-2x+1$')\n"
            "plt.plot(x, poly2(x), label='$x^2-4$')\n"
            "plt.legend(); plt.grid(True); plt.show()\n"
        )
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "general_form": self._formula(
                    r"P(x) = \sum_{i=0}^{n} a_i x^i = a_n x^n + a_{n-1} x^{n-1} + \cdots + a_1 x + a_0",
                    "n次多项式的一般形式，其中$a_i$为系数，$a_n \\neq 0$。",
                    {"a_i": "第i项系数", "n": "多项式的次数"}
                )
            },
            "charts_data": {},
        }

    def _generate_trigonometric_content(self):
        content_body = (
            "\n## 三角函数\n\n"
            "三角函数描述单位圆上点的坐标与角度的关系。\n\n"
            "### 基本三角函数\n"
            "- 正弦：$\\sin(\\theta)$ = 对边/斜边\n"
            "- 余弦：$\\cos(\\theta)$ = 邻边/斜边\n"
            "- 正切：$\\tan(\\theta) = \\sin(\\theta)/\\cos(\\theta)$\n"
        )
        python_code = (
            "\nimport numpy as np\nimport matplotlib.pyplot as plt\n\n"
            "# 角度范围\n"
            "x = np.linspace(0, 4*np.pi, 1000)\n\n"
            "# 计算三角函数值\n"
            "y_sin = np.sin(x)\n"
            "y_cos = np.cos(x)\n"
            "y_tan = np.tan(x)\n\n"
            "print(f\"sin(π/2) = {np.sin(np.pi/2):.3f}\")\n"
            "print(f\"cos(0) = {np.cos(0):.3f}\")\n"
            "print(f\"tan(π/4) = {np.tan(np.pi/4):.3f}\")\n"
        )
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "unit_circle": self._formula(
                    r"\\sin^2(\\theta) + \\cos^2(\\theta) = 1",
                    "毕达哥拉斯恒等式，三角函数的基本关系。",
                    {"\\theta": "角度（弧度制）"}
                )
            },
            "charts_data": {},
        }

    def _generate_sum_content(self):
        content_body = (
            "\n## 求和运算\n\n"
            "求和运算使用∑符号表示一系列数的加法。\n\n"
            "### 基本语法\n"
            "$\\sum_{i=1}^{n} a_i = a_1 + a_2 + \\cdots + a_n$\n\n"
            "### 常见求和公式\n"
            "- 自然数求和：$\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}$\n"
            "- 平方数求和：$\\sum_{i=1}^{n} i^2 = \\frac{n(n+1)(2n+1)}{6}$\n"
        )
        python_code = (
            "\nimport numpy as np\n\n"
            "# 方法1：直接计算\n"
            "numbers = [1, 2, 3, 4, 5]\n"
            "total1 = sum(numbers)\n"
            "print(f\"直接求和: {total1}\")\n\n"
            "# 方法2：使用numpy\n"
            "arr = np.array(numbers)\n"
            "total2 = np.sum(arr)\n"
            "print(f\"numpy求和: {total2}\")\n\n"
            "# 公式验证：1+2+...+n = n(n+1)/2\n"
            "n = 100\n"
            "formula_result = n * (n + 1) // 2\n"
            "direct_result = sum(range(1, n+1))\n"
            "print(f\"公式结果: {formula_result}\")\n"
            "print(f\"直接计算: {direct_result}\")\n"
        )
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "arithmetic_sum": self._formula(
                    r"\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}",
                    "等差数列求和公式，首项为1，公差为1。",
                    {"n": "项数", "i": "第i项"}
                )
            },
            "charts_data": {},
        }

    def _generate_product_content(self):
        content_body = (
            "\n## 乘积运算\n\n"
            "乘积运算使用∏符号表示一系列数的乘法。\n\n"
            "### 基本语法\n"
            "$\\prod_{i=1}^{n} a_i = a_1 \\times a_2 \\times \\cdots \\times a_n$\n\n"
            "### 阶乘\n"
            "最常见的乘积是阶乘：$n! = \\prod_{i=1}^{n} i$\n"
        )
        python_code = (
            "\nimport numpy as np\nimport math\n\n"
            "# 方法1：手动计算乘积\n"
            "numbers = [2, 3, 4, 5]\n"
            "product = 1\n"
            "for num in numbers:\n"
            "    product *= num\n"
            "print(f\"手动乘积: {product}\")\n\n"
            "# 方法2：使用numpy\n"
            "arr = np.array(numbers)\n"
            "product_np = np.prod(arr)\n"
            "print(f\"numpy乘积: {product_np}\")\n\n"
            "# 阶乘计算\n"
            "n = 5\n"
            "factorial_math = math.factorial(n)\n"
            "factorial_manual = np.prod(range(1, n+1))\n"
            "print(f\"5! = {factorial_math}\")\n"
            "print(f\"手动计算: {factorial_manual}\")\n"
        )
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "factorial": self._formula(
                    r"n! = \\prod_{i=1}^{n} i = 1 \\times 2 \\times 3 \\times \\cdots \\times n",
                    "n的阶乘，表示从1到n所有正整数的乘积。",
                    {"n": "正整数", "n!": "n的阶乘"}
                )
            },
            "charts_data": {},
        }

    def _generate_random_content(self):
        content_body = (
            "\n## 随机数生成\n\n"
            "随机数在数据科学、模拟和机器学习中极其重要。\n\n"
            "### 类型\n"
            "- 均匀分布：所有值等概率出现\n"
            "- 正态分布：钟形分布，符合自然现象\n"
            "- 伯努利分布：0/1二项分布\n"
        )
        python_code = (
            "\nimport numpy as np\nimport random\n\n"
            "# 设置随机种子（保证可重现）\n"
            "np.random.seed(42)\n"
            "random.seed(42)\n\n"
            "# 均匀分布随机数\n"
            "uniform_random = np.random.uniform(0, 1, 5)\n"
            "print(f\"均匀分布: {uniform_random}\")\n\n"
            "# 正态分布随机数（均值=0，标准差=1）\n"
            "normal_random = np.random.normal(0, 1, 5)\n"
            "print(f\"正态分布: {normal_random}\")\n\n"
            "# 整数随机数\n"
            "int_random = np.random.randint(1, 10, 5)\n"
            "print(f\"随机整数: {int_random}\")\n\n"
            "# 随机选择\n"
            "choices = ['A', 'B', 'C', 'D']\n"
            "random_choice = np.random.choice(choices, 3)\n"
            "print(f\"随机选择: {random_choice}\")\n"
        )
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "uniform_distribution": self._formula(
                    r"X \\sim U(a,b), \\quad f(x) = \\frac{1}{b-a}",
                    "均匀分布的概率密度函数，在区间[a,b]内等概率。",
                    {"X": "随机变量", "a,b": "区间端点", "f(x)": "概率密度"}
                )
            },
            "charts_data": {},
        }

    def _generate_absolute_content(self):
        content_body = (
            "\n## 绝对值函数\n\n"
            "绝对值表示数到零点的距离，总是非负的。\n\n"
            "### 定义\n"
            "$|x| = \\begin{cases} x & \\text{if } x \\geq 0 \\\\ -x & \\text{if } x < 0 \\end{cases}$\n\n"
            "### 性质\n"
            "- $|x| \\geq 0$（非负性）\n"
            "- $|xy| = |x||y|$（乘法性质）\n"
            "- $||x| - |y|| \\leq |x - y|$（三角不等式）\n"
        )
        python_code = (
            "\nimport numpy as np\nimport matplotlib.pyplot as plt\n\n"
            "# 绝对值计算\n"
            "numbers = [-5, -3, 0, 2, 4]\n"
            "absolute_values = [abs(x) for x in numbers]\n"
            "print(f\"原数组: {numbers}\")\n"
            "print(f\"绝对值: {absolute_values}\")\n\n"
            "# 使用numpy\n"
            "arr = np.array(numbers)\n"
            "abs_arr = np.abs(arr)\n"
            "print(f\"numpy绝对值: {abs_arr}\")\n\n"
            "# 绘制绝对值函数图像\n"
            "x = np.linspace(-5, 5, 100)\n"
            "y = np.abs(x)\n"
            "plt.plot(x, y, 'b-', linewidth=2, label='|x|')\n"
            "plt.grid(True); plt.xlabel('x'); plt.ylabel('|x|')\n"
            "plt.title('绝对值函数'); plt.legend(); plt.show()\n"
        )
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "definition": self._formula(
                    r"|x| = \\sqrt{x^2}",
                    "绝对值的另一种定义，利用平方根的非负性质。",
                    {"|x|": "x的绝对值", "x": "实数"}
                )
            },
            "charts_data": {},
        }

    def _generate_scalar_vector_content(self):
        content_body = (
            "\n## 标量与向量\n\n"
            "### 标量（Scalar）\n"
            "标量是只有大小没有方向的量，如温度、质量、时间。\n\n"
            "### 向量（Vector）\n"
            "向量是既有大小又有方向的量，如速度、力、位移。\n"
            "向量通常表示为：$\\vec{v} = [v_1, v_2, \\ldots, v_n]^T$\n"
        )
        python_code = (
            "\nimport numpy as np\n\n"
            "# 标量示例\n"
            "temperature = 25.5  # 温度（摄氏度）\n"
            "mass = 10.0         # 质量（kg）\n"
            "print(f\"温度: {temperature}°C\")\n"
            "print(f\"质量: {mass} kg\")\n\n"
            "# 向量示例\n"
            "velocity_2d = np.array([3.0, 4.0])  # 2D速度向量\n"
            "position_3d = np.array([1.0, 2.0, 3.0])  # 3D位置向量\n"
            "print(f\"2D速度向量: {velocity_2d}\")\n"
            "print(f\"3D位置向量: {position_3d}\")\n\n"
            "# 向量的大小（模长）\n"
            "magnitude_2d = np.linalg.norm(velocity_2d)\n"
            "magnitude_3d = np.linalg.norm(position_3d)\n"
            "print(f\"2D向量大小: {magnitude_2d:.2f}\")\n"
            "print(f\"3D向量大小: {magnitude_3d:.2f}\")\n"
        )
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "vector_norm": self._formula(
                    r"\\|\\vec{v}\\| = \\sqrt{v_1^2 + v_2^2 + \\cdots + v_n^2}",
                    "向量的模长（欧几里得范数），表示向量的大小。",
                    {"\\vec{v}": "n维向量", "v_i": "第i个分量", "\\|\\vec{v}\\|": "向量的模长"}
                )
            },
            "charts_data": {},
        }

    def _generate_matrix_tensor_content(self):
        content_body = (
            "\n## 矩阵与张量\n\n"
            "### 矩阵（Matrix）\n"
            "矩阵是二维数组，用于线性变换和方程组求解。\n"
            "记作：$A \\in \\mathbb{R}^{m \\times n}$，有m行n列。\n\n"
            "### 张量（Tensor）\n"
            "张量是矩阵的高维推广，在深度学习中广泛使用。\n"
            "- 0阶张量：标量\n"
            "- 1阶张量：向量\n"
            "- 2阶张量：矩阵\n"
            "- n阶张量：n维数组\n"
        )
        python_code = (
            "\nimport numpy as np\n\n"
            "# 创建矩阵\n"
            "matrix_2x3 = np.array([[1, 2, 3],\n"
            "                       [4, 5, 6]])\n"
            "print(f\"2×3矩阵:\\n{matrix_2x3}\")\n"
            "print(f\"矩阵形状: {matrix_2x3.shape}\")\n\n"
            "# 特殊矩阵\n"
            "identity_3x3 = np.eye(3)  # 单位矩阵\n"
            "zeros_2x2 = np.zeros((2, 2))  # 零矩阵\n"
            "ones_2x3 = np.ones((2, 3))    # 全1矩阵\n"
            "print(f\"3×3单位矩阵:\\n{identity_3x3}\")\n\n"
            "# 创建张量（3阶）\n"
            "tensor_3d = np.random.rand(2, 3, 4)  # 2×3×4张量\n"
            "print(f\"3D张量形状: {tensor_3d.shape}\")\n"
            "print(f\"张量维度: {tensor_3d.ndim}\")\n"
        )
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "matrix_element": self._formula(
                    r"A_{ij} \\text{ 表示矩阵 } A \\text{ 的第 } i \\text{ 行第 } j \\text{ 列元素}",
                    "矩阵元素的索引表示法，从1开始计数。",
                    {"A": "矩阵", "i": "行索引", "j": "列索引"}
                )
            },
            "charts_data": {},
        }

    def _generate_row_column_vector_content(self):
        content_body = (
            "\n## 行列向量\n\n"
            "### 行向量（Row Vector）\n"
            "行向量是1×n的矩阵：$\\vec{r} = [r_1, r_2, \\ldots, r_n]$\n\n"
            "### 列向量（Column Vector）\n"
            "列向量是n×1的矩阵：$\\vec{c} = \\begin{bmatrix} c_1 \\\\ c_2 \\\\ \\vdots \\\\ c_n \\end{bmatrix}$\n\n"
            "### 转换关系\n"
            "行向量和列向量可通过转置互相转换。\n"
        )
        python_code = (
            "\nimport numpy as np\n\n"
            "# 创建行向量（1D数组默认为行向量）\n"
            "row_vector = np.array([1, 2, 3, 4])\n"
            "print(f\"行向量: {row_vector}\")\n"
            "print(f\"行向量形状: {row_vector.shape}\")\n\n"
            "# 创建列向量（需要reshape或转置）\n"
            "column_vector = row_vector.reshape(-1, 1)\n"
            "print(f\"列向量:\\n{column_vector}\")\n"
            "print(f\"列向量形状: {column_vector.shape}\")\n\n"
            "# 转置操作\n"
            "row_from_col = column_vector.T  # 转置得到行向量\n"
            "col_from_row = row_vector.reshape(-1, 1)  # reshape得到列向量\n"
            "print(f\"从列向量转换的行向量: {row_from_col}\")\n"
            "print(f\"从行向量转换的列向量:\\n{col_from_row}\")\n"
        )
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "transpose": self._formula(
                    r"\\vec{r}^T = \\vec{c}, \\quad \\vec{c}^T = \\vec{r}",
                    "行向量和列向量通过转置操作互相转换。",
                    {"\\vec{r}": "行向量", "\\vec{c}": "列向量", "T": "转置操作"}
                )
            },
            "charts_data": {},
        }

    def _generate_vector_transpose_content(self):
        content_body = (
            "\n## 向量的转置\n\n"
            "转置是线性代数中的基本操作，将行转为列，列转为行。\n\n"
            "### 定义\n"
            "向量$\\vec{v} = [v_1, v_2, \\ldots, v_n]$的转置记为$\\vec{v}^T$：\n"
            "$\\vec{v}^T = \\begin{bmatrix} v_1 \\\\ v_2 \\\\ \\vdots \\\\ v_n \\end{bmatrix}$\n\n"
            "### 性质\n"
            "- $(\\vec{v}^T)^T = \\vec{v}$（双重转置）\n"
            "- $(\\vec{u} + \\vec{v})^T = \\vec{u}^T + \\vec{v}^T$（加法转置）\n"
        )
        python_code = (
            "\nimport numpy as np\n\n"
            "# 创建向量\n"
            "vector = np.array([1, 2, 3, 4])\n"
            "print(f\"原向量: {vector}\")\n"
            "print(f\"原向量形状: {vector.shape}\")\n\n"
            "# 转置操作\n"
            "vector_T = vector.T\n"
            "print(f\"转置后: {vector_T}\")\n"
            "print(f\"转置后形状: {vector_T.shape}\")\n\n"
            "# 注意：1D数组的转置还是自己\n"
            "# 要真正看到效果，需要2D数组\n"
            "vector_2d = vector.reshape(1, -1)  # 1×4行向量\n"
            "vector_2d_T = vector_2d.T          # 4×1列向量\n"
            "print(f\"2D行向量:\\n{vector_2d}\")\n"
            "print(f\"2D列向量:\\n{vector_2d_T}\")\n\n"
            "# 验证双重转置性质\n"
            "double_transpose = vector_2d_T.T\n"
            "print(f\"双重转置:\\n{double_transpose}\")\n"
            "print(f\"是否相等: {np.array_equal(vector_2d, double_transpose)}\")\n"
        )
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "transpose_definition": self._formula(
                    r"(A^T)_{ij} = A_{ji}",
                    "转置的定义：转置矩阵的第i行第j列元素等于原矩阵的第j行第i列元素。",
                    {"A": "原矩阵", "A^T": "转置矩阵"}
                )
            },
            "charts_data": {},
        }

    def _generate_dot_norm_content(self):
        content_body = (
            "\n## 向量的点积和范数\n\n"
            "### 点积（内积）\n"
            "两个向量的点积衡量它们的相似性和夹角关系。\n"
            "$\\vec{u} \\cdot \\vec{v} = \\sum_{i=1}^{n} u_i v_i = |\\vec{u}||\\vec{v}|\\cos\\theta$\n\n"
            "### 范数（模长）\n"
            "向量的范数衡量向量的\"大小\"或\"长度\"。\n"
            "- L2范数：$\\|\\vec{v}\\|_2 = \\sqrt{\\sum_{i=1}^{n} v_i^2}$\n"
            "- L1范数：$\\|\\vec{v}\\|_1 = \\sum_{i=1}^{n} |v_i|$\n"
        )
        python_code = (
            "\nimport numpy as np\n\n"
            "# 创建两个向量\n"
            "u = np.array([3, 4, 0])\n"
            "v = np.array([1, 2, 2])\n"
            "print(f\"向量u: {u}\")\n"
            "print(f\"向量v: {v}\")\n\n"
            "# 点积计算\n"
            "dot_product_manual = np.sum(u * v)\n"
            "dot_product_numpy = np.dot(u, v)\n"
            "print(f\"点积（手动）: {dot_product_manual}\")\n"
            "print(f\"点积（numpy）: {dot_product_numpy}\")\n\n"
            "# 范数计算\n"
            "l2_norm_u = np.linalg.norm(u, ord=2)  # L2范数\n"
            "l1_norm_u = np.linalg.norm(u, ord=1)  # L1范数\n"
            "print(f\"u的L2范数: {l2_norm_u:.3f}\")\n"
            "print(f\"u的L1范数: {l1_norm_u:.3f}\")\n\n"
            "# 夹角计算\n"
            "cos_theta = dot_product_numpy / (np.linalg.norm(u) * np.linalg.norm(v))\n"
            "angle_rad = np.arccos(cos_theta)\n"
            "angle_deg = np.degrees(angle_rad)\n"
            "print(f\"夹角: {angle_deg:.1f}度\")\n"
        )
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "dot_product": self._formula(
                    r"\\vec{u} \\cdot \\vec{v} = \\|\\vec{u}\\|\\|\\vec{v}\\|\\cos\\theta",
                    "向量点积的几何意义，其中θ是两向量夹角。",
                    {"\\vec{u}, \\vec{v}": "向量", "\\theta": "夹角", "\\cos\\theta": "夹角余弦值"}
                ),
                "l2_norm": self._formula(
                    r"\\|\\vec{v}\\|_2 = \\sqrt{v_1^2 + v_2^2 + \\cdots + v_n^2}",
                    "L2范数（欧几里得范数），是最常用的向量长度度量。",
                    {"\\vec{v}": "n维向量", "v_i": "第i个分量"}
                )
            },
            "charts_data": {},
        }

    def _generate_matrix_multiplication_content(self):
        content_body = (
            "\n## 矩阵的乘法运算\n\n"
            "矩阵乘法是线性代数的核心运算，广泛应用于机器学习。\n\n"
            "### 乘法条件\n"
            "矩阵A(m×n)与矩阵B(p×q)可相乘当且仅当n=p。\n"
            "结果矩阵C的维度为m×q。\n\n"
            "### 计算规则\n"
            "$C_{ij} = \\sum_{k=1}^{n} A_{ik} \\cdot B_{kj}$\n"
        )
        python_code = (
            "\nimport numpy as np\n\n"
            "# 创建矩阵\n"
            "A = np.array([[1, 2, 3],\n"
            "              [4, 5, 6]])  # 2×3矩阵\n"
            "B = np.array([[7, 8],\n"
            "              [9, 10],\n"
            "              [11, 12]])   # 3×2矩阵\n"
            "print(f\"矩阵A (2×3):\\n{A}\")\n"
            "print(f\"矩阵B (3×2):\\n{B}\")\n\n"
            "# 矩阵乘法\n"
            "C = np.dot(A, B)  # 或者 A @ B\n"
            "print(f\"A×B (2×2):\\n{C}\")\n\n"
            "# 验证计算过程\n"
            "# C[0,0] = A[0,:]·B[:,0] = 1×7 + 2×9 + 3×11\n"
            "c00 = A[0, :] @ B[:, 0]\n"
            "print(f\"C[0,0]手动计算: {c00}\")\n"
            "print(f\"C[0,0]结果验证: {C[0, 0]}\")\n\n"
            "# 单位矩阵的性质\n"
            "I = np.eye(2)\n"
            "print(f\"C×I = \\n{C @ I}\")\n"
            "print(f\"是否相等: {np.allclose(C @ I, C)}\")\n"
        )
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "matrix_mult": self._formula(
                    r"(AB)_{ij} = \\sum_{k=1}^{n} A_{ik} B_{kj}",
                    "矩阵乘法的定义：结果矩阵第i行第j列元素等于A第i行与B第j列对应元素乘积之和。",
                    {"A": "m×n矩阵", "B": "n×p矩阵", "AB": "m×p结果矩阵"}
                )
            },
            "charts_data": {},
        }

    def _generate_derivative_content(self):
        content_body = (
            "\n## 导数概念与计算\n\n"
            "导数描述函数在某点的瞬时变化率，是微积分的核心概念。\n\n"
            "### 几何意义\n"
            "导数是函数图像在某点的切线斜率。\n\n"
            "### 物理意义\n"
            "- 位置函数的导数是速度\n"
            "- 速度函数的导数是加速度\n\n"
            "### 基本求导法则\n"
            "- 常数法则：$(c)' = 0$\n"
            "- 幂函数法则：$(x^n)' = nx^{n-1}$\n"
            "- 和差法则：$(f \\pm g)' = f' \\pm g'$\n"
            "- 乘积法则：$(fg)' = f'g + fg'$\n"
        )
        python_code = (
            "\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom scipy.misc import derivative\n\n"
            "# 定义函数 f(x) = x^2\n"
            "def f(x):\n"
            "    return x**2\n\n"
            "# 解析导数 f'(x) = 2x\n"
            "def f_prime(x):\n"
            "    return 2*x\n\n"
            "# 数值导数计算\n"
            "x_point = 3\n"
            "analytical_derivative = f_prime(x_point)\n"
            "numerical_derivative = derivative(f, x_point, dx=1e-6)\n"
            "print(f\"在x={x_point}处：\")\n"
            "print(f\"解析导数: {analytical_derivative}\")\n"
            "print(f\"数值导数: {numerical_derivative:.6f}\")\n\n"
            "# 可视化函数和切线\n"
            "x = np.linspace(-1, 5, 100)\n"
            "y = f(x)\n"
            "plt.plot(x, y, 'b-', label='f(x)=x²')\n"
            "# 在x=3处的切线\n"
            "tangent_y = f(x_point) + f_prime(x_point) * (x - x_point)\n"
            "plt.plot(x, tangent_y, 'r--', label=f'切线在x={x_point}')\n"
            "plt.scatter([x_point], [f(x_point)], color='red', s=50, zorder=5)\n"
            "plt.grid(True); plt.legend(); plt.title('函数及其切线')\n"
            "plt.show()\n"
        )
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "derivative_definition": self._formula(
                    r"f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}",
                    "导数的定义：函数在某点的极限变化率。",
                    {"f'(x)": "f在x处的导数", "h": "无穷小增量"}
                ),
                "power_rule": self._formula(
                    r"\\frac{d}{dx}x^n = nx^{n-1}",
                    "幂函数的求导法则，是最基本的求导公式之一。",
                    {"n": "实数指数"}
                )
            },
            "charts_data": {},
        }

    def _generate_partial_derivative_content(self):
        content_body = (
            "\n## 偏导数计算\n\n"
            "偏导数是多元函数对其中一个变量的导数，其他变量视为常数。\n\n"
            "### 记号\n"
            "函数$f(x,y)$对x的偏导数记为：$\\frac{\\partial f}{\\partial x}$或$f_x$\n\n"
            "### 几何意义\n"
            "偏导数表示多元函数在某个方向上的变化率。\n\n"
            "### 计算方法\n"
            "求$\\frac{\\partial f}{\\partial x}$时，将y看作常数，按普通求导法则计算。\n"
        )
        python_code = (
            "\nimport numpy as np\nimport sympy as sp\nfrom mpl_toolkits.mplot3d import Axes3D\nimport matplotlib.pyplot as plt\n\n"
            "# 使用sympy计算偏导数\n"
            "x, y = sp.symbols('x y')\n"
            "f = x**2 + 3*x*y + y**2  # 定义函数 f(x,y) = x² + 3xy + y²\n"
            "print(f\"函数: f(x,y) = {f}\")\n\n"
            "# 计算偏导数\n"
            "df_dx = sp.diff(f, x)  # 对x求偏导\n"
            "df_dy = sp.diff(f, y)  # 对y求偏导\n"
            "print(f\"∂f/∂x = {df_dx}\")\n"
            "print(f\"∂f/∂y = {df_dy}\")\n\n"
            "# 在特定点计算偏导数值\n"
            "point = (2, 1)\n"
            "df_dx_val = df_dx.subs([(x, point[0]), (y, point[1])])\n"
            "df_dy_val = df_dy.subs([(x, point[0]), (y, point[1])])\n"
            "print(f\"在点{point}处：\")\n"
            "print(f\"∂f/∂x = {df_dx_val}\")\n"
            "print(f\"∂f/∂y = {df_dy_val}\")\n\n"
            "# 梯度向量\n"
            "gradient = np.array([float(df_dx_val), float(df_dy_val)])\n"
            "print(f\"梯度向量: {gradient}\")\n"
        )
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "partial_derivative": self._formula(
                    r"\\frac{\\partial f}{\\partial x} = \\lim_{h \\to 0} \\frac{f(x+h,y) - f(x,y)}{h}",
                    "偏导数的定义：对其中一个变量求导，其他变量保持不变。",
                    {"f": "多元函数", "x,y": "自变量"}
                ),
                "gradient": self._formula(
                    r"\\nabla f = \\left[\\frac{\\partial f}{\\partial x}, \\frac{\\partial f}{\\partial y}\\right]^T",
                    "梯度是所有偏导数组成的向量，指向函数增长最快的方向。",
                    {"\\nabla f": "梯度向量"}
                )
            },
            "charts_data": {},
        }

    def _generate_loss_function_content(self):
        content_body = (
            "\n## 损失函数(MSE/MAE)\n\n"
            "损失函数衡量预测值与真实值之间的差异，是机器学习优化的目标。\n\n"
            "### 均方误差(MSE)\n"
            "MSE对大误差更敏感，适用于回归问题。\n"
            "$MSE = \\frac{1}{n}\\sum_{i=1}^{n}(y_i - \\hat{y}_i)^2$\n\n"
            "### 平均绝对误差(MAE)\n"
            "MAE对异常值更鲁棒，误差单位与原数据相同。\n"
            "$MAE = \\frac{1}{n}\\sum_{i=1}^{n}|y_i - \\hat{y}_i|$\n"
        )
        python_code = (
            "\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.metrics import mean_squared_error, mean_absolute_error\n\n"
            "# 真实值和预测值\n"
            "y_true = np.array([3, -0.5, 2, 7, 4.2])\n"
            "y_pred = np.array([2.5, 0.0, 2.1, 7.8, 4.0])\n"
            "print(f\"真实值: {y_true}\")\n"
            "print(f\"预测值: {y_pred}\")\n\n"
            "# 手动计算MSE和MAE\n"
            "errors = y_true - y_pred\n"
            "mse_manual = np.mean(errors**2)\n"
            "mae_manual = np.mean(np.abs(errors))\n"
            "print(f\"\\n误差: {errors}\")\n"
            "print(f\"MSE (手动): {mse_manual:.4f}\")\n"
            "print(f\"MAE (手动): {mae_manual:.4f}\")\n\n"
            "# 使用sklearn计算\n"
            "mse_sklearn = mean_squared_error(y_true, y_pred)\n"
            "mae_sklearn = mean_absolute_error(y_true, y_pred)\n"
            "print(f\"MSE (sklearn): {mse_sklearn:.4f}\")\n"
            "print(f\"MAE (sklearn): {mae_sklearn:.4f}\")\n\n"
            "# 可视化损失函数形状\n"
            "error_range = np.linspace(-3, 3, 100)\n"
            "squared_loss = error_range**2\n"
            "absolute_loss = np.abs(error_range)\n"
            "plt.figure(figsize=(10, 4))\n"
            "plt.subplot(1, 2, 1)\n"
            "plt.plot(error_range, squared_loss, 'b-', label='Squared Loss')\n"
            "plt.xlabel('Error'); plt.ylabel('Loss'); plt.title('MSE Loss')\n"
            "plt.grid(True); plt.legend()\n"
            "plt.subplot(1, 2, 2)\n"
            "plt.plot(error_range, absolute_loss, 'r-', label='Absolute Loss')\n"
            "plt.xlabel('Error'); plt.ylabel('Loss'); plt.title('MAE Loss')\n"
            "plt.grid(True); plt.legend()\n"
            "plt.tight_layout(); plt.show()\n"
        )
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "mse": self._formula(
                    r"MSE = \\frac{1}{n}\\sum_{i=1}^{n}(y_i - \\hat{y}_i)^2",
                    "均方误差：对预测误差平方求平均，对大误差惩罚更重。",
                    {"y_i": "第i个真实值", "\\hat{y}_i": "第i个预测值", "n": "样本数"}
                ),
                "mae": self._formula(
                    r"MAE = \\frac{1}{n}\\sum_{i=1}^{n}|y_i - \\hat{y}_i|",
                    "平均绝对误差：对预测误差绝对值求平均，对异常值更鲁棒。",
                    {"y_i": "第i个真实值", "\\hat{y}_i": "第i个预测值", "n": "样本数"}
                ),
                "rmse": self._formula(
                    r"RMSE = \\sqrt{MSE} = \\sqrt{\\frac{1}{n}\\sum_{i=1}^{n}(y_i - \\hat{y}_i)^2}",
                    "均方根误差：MSE的平方根，单位与原数据相同。",
                    {"RMSE": "均方根误差"}
                )
            },
            "charts_data": {},
        }

    def _generate_default_content(self) -> Dict[str, Any]:
        return {
            "content_body": "该数学知识点内容正在开发中...",
            "python_code": "# 代码示例待添加",
            "formulas": {},
            "charts_data": {},
        }