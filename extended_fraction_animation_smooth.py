from manim import *
import numpy as np

class ExtendedFractionAnimation(Scene):

    def construct(self):

        self.camera.background_color = "#16161d"

        # 1. 创建对象

        # -----------------------------------------

       

        # 分子：为了方便控制，我们将字符串拆得更细一些，虽然MathTex会自动拆分，

        # 但显式从对象中切片更准确。

        # 这里的 substring 逻辑：MathTex 会把运算符和字符分开作为子对象

        numerator = MathTex(r"0 + 1 + 2 + 3 + \cdots + ", r"n")

       

        # 设置颜色：前半部分默认白色，最后一部分(n)设为蓝色

        numerator[0].set_color(WHITE)

        numerator[1].set_color(BLUE)

       

        # 分母：n + n + ... + n

        denominator = MathTex(r"n + n + n + n + \cdots + n")

       

        # 分离分母中的元素

        # 在 "n + n + n + n + ... + n" 中：

        # 偶数索引 (0, 2, 4...) 是 'n'

        # 奇数索引 (1, 3, 5...) 是 '+' 或 '\cdots'

        denom_ns = VGroup(*[denominator[i] for i in range(0, len(denominator), 2)])

        denom_others = VGroup(*[denominator[i] for i in range(1, len(denominator), 2)])

       

        # 设置分母中 n 的颜色为蓝色

        denom_ns.set_color(BLUE)

        denom_others.set_color(WHITE)

       

        # 分数线

        fraction_line = Line(LEFT, RIGHT) # 长度稍后自动适配

       

        # 等号和答案

        equals_sign = MathTex("=")

        answer = MathTex(r"\frac{1}{2}", color=YELLOW)

       

        # 2. 布局排版 (在动画开始前先排好位置)

        # -----------------------------------------

       

        # 临时组合以便计算位置

        # 先把分子放在上面

        numerator.move_to(UP * 0.8)

       

        # 确定分数线长度 (比分子稍宽)

        fraction_line.match_width(numerator)

        fraction_line.scale(1.1) # 稍微拉长一点点

        fraction_line.next_to(numerator, DOWN, buff=0.2)

       

        # 分母放在分数线下面

        denominator.next_to(fraction_line, DOWN, buff=0.2)

       

        # 等号和答案放在右边

        equals_sign.next_to(fraction_line, RIGHT, buff=0.4)

        answer.next_to(equals_sign, RIGHT, buff=0.2)

       

        # 将整体居中

        full_group = VGroup(numerator, fraction_line, denominator, equals_sign, answer)

        full_group.move_to(ORIGIN)

        fraction_group = VGroup(numerator, fraction_line, denominator)

        rect = SurroundingRectangle(

            fraction_group,

            color=WHITE,

            stroke_width=2,

            fill_opacity=0,

            buff=0.02

        )

       

        # 3. 执行动画 sequence

        # -----------------------------------------

       

        # 第一步：渲染白色分子部分 (0+1+2+3+...+)

        self.play(Write(numerator[0]), run_time=1.5)

        self.wait(0.5)

       

        # 第二步：渲染蓝色 n

        self.play(Write(numerator[1]), run_time=0.5)

        self.wait(0.5)

       

        # 第三步：蓝色 n 分身到分母位置

        # 我们使用 TransformFromCopy，从分子的 n 变换出分母的每一个 n

        animations = [

            TransformFromCopy(numerator[1], target_n)

            for target_n in denom_ns

        ]

       

        self.play(*animations, Create(rect), run_time=2, lag_ratio=0.1)

        self.wait(0.5)

       

