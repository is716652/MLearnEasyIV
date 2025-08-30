from app.database import SessionLocal, engine, Base
from app import crud, models
from app.ml_content.content_generator import ContentGenerator


def populate_math_contents(db: SessionLocal, generator: ContentGenerator) -> int:
    """批量生成并插入数学内容，返回新增数量"""
    math_topics = [
        # 基础概念
        {"module": "math", "subcategory": "基础概念", "title": "常量与变量"},
        {"module": "math", "subcategory": "基础概念", "title": "函数定义与调用"},
        # 代数运算
        {"module": "math", "subcategory": "代数运算", "title": "幂运算"},
        {"module": "math", "subcategory": "代数运算", "title": "平方根计算"},
        {"module": "math", "subcategory": "代数运算", "title": "多项式函数"},
        # 特殊函数
        {"module": "math", "subcategory": "特殊函数", "title": "三角函数"},
        {"module": "math", "subcategory": "特殊函数", "title": "求和运算"},
        {"module": "math", "subcategory": "特殊函数", "title": "乘积运算"},
        {"module": "math", "subcategory": "特殊函数", "title": "随机数生成"},
        {"module": "math", "subcategory": "特殊函数", "title": "绝对值函数"},
        # 线性代数
        {"module": "math", "subcategory": "线性代数", "title": "标量与向量"},
        {"module": "math", "subcategory": "线性代数", "title": "矩阵与张量"},
        {"module": "math", "subcategory": "线性代数", "title": "行列向量转换"},
        {"module": "math", "subcategory": "线性代数", "title": "向量的转置"},
        {"module": "math", "subcategory": "线性代数", "title": "向量的加减运算"},
        {"module": "math", "subcategory": "线性代数", "title": "向量的点积和范数"},
        {"module": "math", "subcategory": "线性代数", "title": "矩阵的乘法运算"},
        # 微积分与应用
        {"module": "math", "subcategory": "微积分", "title": "导数概念与计算"},
        {"module": "math", "subcategory": "微积分", "title": "偏导数计算"},
        {"module": "math", "subcategory": "应用", "title": "损失函数(MSE/MAE)"},
        {"module": "math", "subcategory": "应用", "title": "激活函数(Sigmoid/ReLU/Tanh)"},
    ]

    created = 0
    for topic in math_topics:
        content = crud.get_content_by_title(db, topic["title"])
        if not content:
            generated = generator.generate_content(
                topic["module"], topic["subcategory"], topic["title"]
            )
            crud.create_content(
                db,
                {
                    "module": topic["module"],
                    "subcategory": topic["subcategory"],
                    "title": topic["title"],
                    **generated,
                },
            )
            created += 1
    return created


def populate_ml_contents(db: SessionLocal, generator: ContentGenerator) -> int:
    """批量生成并插入机器学习（算法理论与实践）内容，返回新增数量"""
    ml_topics = [
        # 回归
        {"module": "ml", "subcategory": "回归算法", "title": "线性回归"},
        {"module": "ml", "subcategory": "分类算法", "title": "逻辑回归"},
        # 核心分类算法
        {"module": "ml", "subcategory": "分类算法", "title": "决策树"},
        {"module": "ml", "subcategory": "分类算法", "title": "支持向量机"},
        {"module": "ml", "subcategory": "分类算法", "title": "K近邻"},
        {"module": "ml", "subcategory": "分类算法", "title": "朴素贝叶斯"},
        {"module": "ml", "subcategory": "集成学习", "title": "随机森林"},
        {"module": "ml", "subcategory": "集成学习", "title": "梯度提升机"},
    ]

    created = 0
    for topic in ml_topics:
        content = crud.get_content_by_title(db, topic["title"])
        if not content:
            generated = generator.generate_content(
                topic["module"], topic["subcategory"], topic["title"]
            )
            crud.create_content(
                db,
                {
                    "module": topic["module"],
                    "subcategory": topic["subcategory"],
                    "title": topic["title"],
                    **generated,
                },
            )
            created += 1
    return created


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    generator = ContentGenerator()
    try:
        created = populate_math_contents(db, generator)
        print(f"数学内容初始化完成，新增 {created} 条记录。")
        # 如需初始化ML模块，可取消下一行注释
        # created_ml = populate_ml_contents(db, generator)
        # print(f"机器学习内容初始化完成，新增 {created_ml} 条记录。")
    finally:
        db.close()


if __name__ == "__main__":
    main()