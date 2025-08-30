import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris, load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from io import BytesIO
import base64
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class MLContentGenerator:
    """机器学习模块（算法理论与实践）内容生成器"""

    def __init__(self):
        # 使用与 seaborn v0.13 兼容的样式名
        plt.style.use('seaborn-v0_8')
        np.random.seed(42)

    def generate_ml_content(self, subcategory: str, title: str) -> Dict[str, Any]:
        """根据子分类与标题生成ML内容"""
        mapping = {
            # 回归算法
            "线性回归": self._generate_linear_regression_content,
            "逻辑回归": self._generate_logistic_regression_content,
            # 分类算法
            "决策树": self._generate_decision_tree_content,
            "支持向量机": self._generate_svm_content,
            "K近邻": self._generate_knn_content,
            "朴素贝叶斯": self._generate_naive_bayes_content,
            "随机森林": self._generate_random_forest_content,
            "梯度提升机": self._generate_gradient_boosting_content,
        }

        for key, fn in mapping.items():
            if key in subcategory or key in title:
                return fn()
        return self._generate_default_content()

    # =============== 工具方法 ===============
    def _fig_to_base64(self, fig) -> str:
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=110, bbox_inches='tight')
        buf.seek(0)
        img = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        return img

    # =============== 具体算法 ===============
    def _generate_linear_regression_content(self) -> Dict[str, Any]:
        content_body = (
            "## 线性回归\n\n"
            "线性回归用一条直线刻画输入与输出的关系，常用于预测连续数值。\n"
            "- 单变量：y = wx + b\n"
            "- 多变量：y = w^T x + b\n"
            "- 训练目标：最小化均方误差(MSE)\n"
        )

        python_code = (
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "from sklearn.linear_model import LinearRegression\n"
            "from sklearn.datasets import load_diabetes\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import mean_squared_error, r2_score\n\n"
            "diabetes = load_diabetes()\n"
            "X, y = diabetes.data, diabetes.target\n"
            "X_bmi = X[:, np.newaxis, 2]\n\n"
            "X_train, X_test, y_train, y_test = train_test_split(X_bmi, y, test_size=0.2, random_state=42)\n"
            "model = LinearRegression().fit(X_train, y_train)\n"
            "y_pred = model.predict(X_test)\n\n"
            "print('w=', model.coef_[0], 'b=', model.intercept_)\n"
            "print('MSE=', mean_squared_error(y_test, y_pred))\n"
            "print('R2=', r2_score(y_test, y_pred))\n\n"
            "plt.figure(figsize=(10,4))\n"
            "plt.subplot(1,2,1); plt.scatter(X_test, y_test, alpha=0.6); plt.plot(X_test, y_pred, 'r'); plt.title('回归线')\n"
            "plt.subplot(1,2,2); res=y_test-y_pred; plt.scatter(y_pred, res, alpha=0.6); plt.axhline(0,color='r',ls='--'); plt.title('残差图')\n"
            "plt.tight_layout(); plt.show()\n"
        )

        # 生成图表
        diabetes = load_diabetes()
        X_bmi = diabetes.data[:, np.newaxis, 2]
        y = diabetes.target
        X_train, X_test, y_train, y_test = train_test_split(X_bmi, y, test_size=0.2, random_state=42)
        model = LinearRegression().fit(X_train, y_train)
        y_pred = model.predict(X_test)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
        ax1.scatter(X_test, y_test, alpha=0.6, label='真实')
        ax1.plot(X_test, y_pred, 'r', label='预测线')
        ax1.set_title('单变量线性回归'); ax1.legend(); ax1.grid(True, alpha=0.3)
        res = y_test - y_pred
        ax2.scatter(y_pred, res, alpha=0.6)
        ax2.axhline(0, color='r', ls='--'); ax2.set_title('残差图'); ax2.grid(True, alpha=0.3)
        chart = self._fig_to_base64(fig)

        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "linear": self._formula(
                    r"y = w^T x + b",
                    "线性模型：用权重向量与特征向量的内积加上偏置来预测目标值。",
                    {"w": "权重向量", "x": "特征向量", "b": "偏置项"}
                ),
                "mse": self._formula(
                    r"J = \frac{1}{m} \sum_{i=1}^{m} (y_i - \hat{y}_i)^2",
                    "均方误差（MSE）：度量预测值与真实值的平均平方偏差，训练目标是最小化该损失。",
                    {"m": "样本数量", "y_i": "第 i 个样本的真实值", "\\hat{y}_i": "第 i 个样本的预测值"}
                )
            },
            "charts_data": {"linear_regression": chart},
        }

    def _generate_logistic_regression_content(self) -> Dict[str, Any]:
        content_body = (
            "## 逻辑回归\n\n"
            "通过Sigmoid将线性输出映射到(0,1)，用于二分类，常配合交叉熵损失。\n"
        )

        python_code = (
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.datasets import load_iris\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.metrics import accuracy_score, confusion_matrix, classification_report\n\n"
            "iris = load_iris()\n"
            "X = iris.data[:100, :2]; y = iris.target[:100]\n"
            "X = StandardScaler().fit_transform(X)\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)\n"
            "model = LogisticRegression().fit(X_train, y_train)\n"
            "y_pred = model.predict(X_test)\n"
            "print('acc=', accuracy_score(y_test, y_pred))\n"
            "print('conf=\\n', confusion_matrix(y_test, y_pred))\n"
            "print(classification_report(y_test, y_pred))\n\n"
            "# 可视化Sigmoid\n"
            "z = np.linspace(-8,8,200); s=1/(1+np.exp(-z))\n"
            "plt.plot(z,s); plt.axvline(0,ls='--'); plt.axhline(0.5,ls='--',c='r'); plt.title('Sigmoid'); plt.show()\n"
        )

        iris = load_iris(); X = iris.data[:100, :2]; y = iris.target[:100]
        Xs = StandardScaler().fit_transform(X)
        model = LogisticRegression().fit(Xs, y)
        # Sigmoid 图
        z = np.linspace(-8, 8, 200); s = 1/(1+np.exp(-z))
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
        # 决策边界热力背景（简化展示）
        x_min, x_max = Xs[:,0].min()-1, Xs[:,0].max()+1
        y_min, y_max = Xs[:,1].min()-1, Xs[:,1].max()+1
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 150), np.linspace(y_min, y_max, 150))
        Z = model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        ax1.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.coolwarm)
        ax1.scatter(Xs[:,0], Xs[:,1], c=y, cmap=plt.cm.coolwarm, edgecolors='k', s=20)
        ax1.set_title('逻辑回归决策边界'); ax1.grid(True, alpha=0.2)
        ax2.plot(z, s, 'b'); ax2.axvline(0, ls='--'); ax2.axhline(0.5, ls='--', c='r'); ax2.set_title('Sigmoid')
        chart = self._fig_to_base64(fig)

        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "sigmoid": self._formula(
                    r"\sigma(z) = \frac{1}{1 + e^{-z}}",
                    "Sigmoid 函数：将任意实数映射到 (0,1)，作为概率估计。",
                    {"z": "线性得分/对数几率"}
                ),
                "ce": self._formula(
                    r"J = -\frac{1}{m} \sum_{i=1}^{m} \big[y_i \log(\hat{y}_i) + (1-y_i)\log(1-\hat{y}_i)\big]",
                    "交叉熵损失：衡量二分类预测概率与真实标签之间的差异。",
                    {"m": "样本数量", "y_i": "第 i 个样本标签(0/1)", "\\hat{y}_i": "第 i 个样本预测为 1 的概率"}
                )
            },
            "charts_data": {"logistic_regression": chart},
        }

    def _generate_decision_tree_content(self) -> Dict[str, Any]:
        content_body = (
            "## 决策树\n\n"
            "通过递归分裂特征空间来分类，支持可解释性强的树结构与特征重要性评估。\n"
        )

        python_code = (
            "import matplotlib.pyplot as plt\n"
            "from sklearn.datasets import load_iris\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.tree import DecisionTreeClassifier, plot_tree\n"
            "from sklearn.metrics import accuracy_score, confusion_matrix\n\n"
            "iris = load_iris(); X, y = iris.data, iris.target\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)\n"
            "model = DecisionTreeClassifier(max_depth=3, random_state=42).fit(X_train, y_train)\n"
            "y_pred = model.predict(X_test)\n"
            "print('acc=', accuracy_score(y_test, y_pred))\n"
            "print('conf=\\n', confusion_matrix(y_test, y_pred))\n\n"
            "plt.figure(figsize=(16,6))\n"
            "plot_tree(model, feature_names=iris.feature_names, class_names=iris.target_names, filled=True, rounded=True)\n"
            "plt.show()\n"
        )

        iris = load_iris(); X, y = iris.data, iris.target
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        model = DecisionTreeClassifier(max_depth=3, random_state=42).fit(X_train, y_train)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        plot_tree(model, feature_names=iris.feature_names, class_names=iris.target_names, filled=True, rounded=True, fontsize=8, ax=ax1)
        importances = model.feature_importances_
        ax2.barh(iris.feature_names, importances)
        ax2.set_title('特征重要性'); ax2.grid(True, alpha=0.3)
        chart = self._fig_to_base64(fig)

        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {
                "gini": self._formula(
                    r"\text{Gini} = 1 - \sum_{i} p_i^2",
                    "基尼不纯度：衡量一个节点中的样本不纯度，越小越纯。",
                    {"p_i": "属于第 i 类的样本比例"}
                ),
                "entropy": self._formula(
                    r"H = - \sum_{i} p_i \log p_i",
                    "信息熵：度量不确定性，越小越确定。",
                    {"p_i": "属于第 i 类的样本比例"}
                )
            },
            "charts_data": {"decision_tree": chart},
        }

    def _generate_svm_content(self) -> Dict[str, Any]:
        content_body = (
            "## 支持向量机（SVM）\n\n"
            "通过最大化间隔寻找最优超平面进行分类，核函数可处理非线性。\n"
        )
        python_code = (
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "from sklearn.datasets import load_iris\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.svm import SVC\n\n"
            "iris = load_iris()\n"
            "X = iris.data[:100, :2] ; y = iris.target[:100]\n"
            "X = StandardScaler().fit_transform(X)\n"
            "clf = SVC(kernel='rbf', gamma='scale', C=1.0).fit(X, y)\n\n"
            "# 绘制决策边界\n"
            "x_min, x_max = X[:,0].min()-1, X[:,0].max()+1\n"
            "y_min, y_max = X[:,1].min()-1, X[:,1].max()+1\n"
            "xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200), np.linspace(y_min, y_max, 200))\n"
            "Z = clf.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)\n"
            "plt.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.coolwarm)\n"
            "plt.scatter(X[:,0], X[:,1], c=y, cmap=plt.cm.coolwarm, edgecolors='k', s=20)\n"
            "plt.title('SVM 决策边界')\n"
            "plt.show()\n"
        )
        iris = load_iris(); X = iris.data[:100, :2]; y = iris.target[:100]
        Xs = StandardScaler().fit_transform(X)
        clf = SVC(kernel='rbf', gamma='scale', C=1.0).fit(Xs, y)
        x_min, x_max = Xs[:,0].min()-1, Xs[:,0].max()+1
        y_min, y_max = Xs[:,1].min()-1, Xs[:,1].max()+1
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200), np.linspace(y_min, y_max, 200))
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        fig, ax = plt.subplots(1, 1, figsize=(6, 4.5))
        ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.coolwarm)
        ax.scatter(Xs[:,0], Xs[:,1], c=y, cmap=plt.cm.coolwarm, edgecolors='k', s=20)
        ax.set_title('SVM 决策边界'); ax.grid(True, alpha=0.2)
        chart = self._fig_to_base64(fig)
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {"decision": "f(x)=w^T\phi(x)+b"},
            "charts_data": {"svm": chart},
        }

    def _generate_knn_content(self) -> Dict[str, Any]:
        content_body = (
            "## K近邻（KNN）\n\n"
            "基于邻近样本的多数票进行分类，K 为关键超参数。\n"
        )
        python_code = (
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "from sklearn.datasets import load_iris\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.neighbors import KNeighborsClassifier\n\n"
            "iris = load_iris()\n"
            "X = iris.data[:100, :2] ; y = iris.target[:100]\n"
            "X = StandardScaler().fit_transform(X)\n"
            "clf = KNeighborsClassifier(n_neighbors=5).fit(X, y)\n\n"
            "# 决策边界\n"
            "x_min, x_max = X[:,0].min()-1, X[:,0].max()+1\n"
            "y_min, y_max = X[:,1].min()-1, X[:,1].max()+1\n"
            "xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200), np.linspace(y_min, y_max, 200))\n"
            "Z = clf.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)\n"
            "plt.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.coolwarm)\n"
            "plt.scatter(X[:,0], X[:,1], c=y, cmap=plt.cm.coolwarm, edgecolors='k', s=20)\n"
            "plt.title('KNN 决策边界')\n"
            "plt.show()\n"
        )
        iris = load_iris(); X = iris.data[:100, :2]; y = iris.target[:100]
        Xs = StandardScaler().fit_transform(X)
        clf = KNeighborsClassifier(n_neighbors=5).fit(Xs, y)
        x_min, x_max = Xs[:,0].min()-1, Xs[:,0].max()+1
        y_min, y_max = Xs[:,1].min()-1, Xs[:,1].max()+1
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200), np.linspace(y_min, y_max, 200))
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        fig, ax = plt.subplots(1, 1, figsize=(6, 4.5))
        ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.coolwarm)
        ax.scatter(Xs[:,0], Xs[:,1], c=y, cmap=plt.cm.coolwarm, edgecolors='k', s=20)
        ax.set_title('KNN 决策边界'); ax.grid(True, alpha=0.2)
        chart = self._fig_to_base64(fig)
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {"majority": "y=\text{majority}(\mathcal{N}_k(x))"},
            "charts_data": {"knn": chart},
        }

    def _generate_naive_bayes_content(self) -> Dict[str, Any]:
        content_body = (
            "## 朴素贝叶斯（Naive Bayes）\n\n"
            "基于特征条件独立假设的概率分类器，速度快且鲁棒。\n"
        )
        python_code = (
            "import numpy as np\n"
            "import seaborn as sns\n"
            "import matplotlib.pyplot as plt\n"
            "from sklearn.datasets import load_iris\n"
            "from sklearn.naive_bayes import GaussianNB\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import confusion_matrix, accuracy_score\n\n"
            "iris = load_iris(); X, y = iris.data, iris.target\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)\n"
            "clf = GaussianNB().fit(X_train, y_train)\n"
            "y_pred = clf.predict(X_test)\n"
            "print('acc=', accuracy_score(y_test, y_pred))\n"
            "cm = confusion_matrix(y_test, y_pred)\n"
            "sns.heatmap(cm, annot=True, fmt='d'); plt.title('混淆矩阵'); plt.show()\n"
        )
        iris = load_iris(); X, y = iris.data, iris.target
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        clf = GaussianNB().fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        fig, ax = plt.subplots(figsize=(5,4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_title('朴素贝叶斯混淆矩阵')
        chart = self._fig_to_base64(fig)
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {"bayes": "P(y|x)∝P(x|y)P(y)"},
            "charts_data": {"naive_bayes_cm": chart},
        }

    def _generate_random_forest_content(self) -> Dict[str, Any]:
        content_body = (
            "## 随机森林（Random Forest）\n\n"
            "通过集成多棵决策树并进行投票，降低过拟合并提升泛化能力。\n"
        )
        python_code = (
            "from sklearn.datasets import load_iris\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import accuracy_score\n"
            "import matplotlib.pyplot as plt\n\n"
            "iris = load_iris(); X, y = iris.data, iris.target\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)\n"
            "clf = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)\n"
            "print('acc=', accuracy_score(y_test, clf.predict(X_test)))\n"
            "plt.bar(range(X.shape[1]), clf.feature_importances_); plt.title('特征重要性'); plt.show()\n"
        )
        iris = load_iris(); X, y = iris.data, iris.target
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        clf = RandomForestClassifier(n_estimators=120, random_state=42).fit(X_train, y_train)
        importances = clf.feature_importances_
        fig, ax = plt.subplots(figsize=(6,4))
        ax.bar(range(X.shape[1]), importances, color='teal')
        ax.set_xticks(range(X.shape[1]))
        ax.set_xticklabels(iris.feature_names, rotation=30)
        ax.set_title('随机森林特征重要性'); ax.grid(True, axis='y', alpha=0.3)
        chart = self._fig_to_base64(fig)
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {"bagging": "\n多数投票/平均\n"},
            "charts_data": {"random_forest_importance": chart},
        }

    def _generate_gradient_boosting_content(self) -> Dict[str, Any]:
        content_body = (
            "## 梯度提升机（GBDT）\n\n"
            "通过逐步拟合残差的弱学习器序列来提升性能，常用于结构化数据分类回归。\n"
        )
        python_code = (
            "from sklearn.datasets import load_iris\n"
            "from sklearn.ensemble import GradientBoostingClassifier\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import accuracy_score\n"
            "import matplotlib.pyplot as plt\n\n"
            "iris = load_iris(); X, y = iris.data, iris.target\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)\n"
            "clf = GradientBoostingClassifier(random_state=42).fit(X_train, y_train)\n"
            "print('acc=', accuracy_score(y_test, clf.predict(X_test)))\n"
            "plt.bar(range(X.shape[1]), clf.feature_importances_); plt.title('特征重要性'); plt.show()\n"
        )
        iris = load_iris(); X, y = iris.data, iris.target
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        clf = GradientBoostingClassifier(random_state=42).fit(X_train, y_train)
        importances = clf.feature_importances_
        fig, ax = plt.subplots(figsize=(6,4))
        ax.bar(range(X.shape[1]), importances, color='orange')
        ax.set_xticks(range(X.shape[1]))
        ax.set_xticklabels(iris.feature_names, rotation=30)
        ax.set_title('GBDT 特征重要性'); ax.grid(True, axis='y', alpha=0.3)
        chart = self._fig_to_base64(fig)
        return {
            "content_body": content_body,
            "python_code": python_code,
            "formulas": {"boosting": "逐步拟合残差"},
            "charts_data": {"gbdt_importance": chart},
        }

    def _placeholder(self, name: str) -> Dict[str, Any]:
        return {
            "content_body": f"## {name}\n该算法详细内容将很快补充。",
            "python_code": "# TODO: 即将补充完整示例",
            "formulas": {},
            "charts_data": {},
        }

    def _generate_default_content(self) -> Dict[str, Any]:
        return {
            "content_body": "该机器学习算法内容正在开发中...",
            "python_code": "# 代码示例待添加",
            "formulas": {},
            "charts_data": {},
        }

    # 新增：规范化公式结构，统一包含 latex/explanation/symbols，便于前端与全站复用
    def _formula(self, latex: str, explanation: str = "", symbols: Dict[str, str] = None) -> Dict[str, Any]:
        return {
            "latex": latex,
            "explanation": explanation,
            "symbols": symbols or {}
        }