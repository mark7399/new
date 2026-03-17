import math
from manim import *

BG_COLOR = "#16161d"
ORIGIN_POINT = np.array([0, 0, 0])
RADIUS = 5


class Scene8_Derivation(MovingCameraScene):
    """Scene8: 以 Scene7 最终画面为起点，继续推导"""

    def construct(self):
        self.camera.background_color = BG_COLOR

        # === 重建 Scene7 结束状态 ===

        # 网格（x轴、y轴已淡出，只保留背景格线）
        grid = NumberPlane(
            x_range=[-20, 20], y_range=[-15, 15],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
        )
        grid.get_x_axis().set_stroke(opacity=0)
        grid.get_y_axis().set_stroke(opacity=0)

        # 相机：center=[5.5, 0, 0]，zoom_out_factor=1.8
        zoom_out_factor = 1.8
        self.camera.frame.move_to([5.5, 0, 0])
        self.camera.frame.scale(zoom_out_factor)

        # 分式布局参数（与 Scene7 完全一致）
        cx = 5.5
        frac_center_y = 5.0
        gap = 0.3   # 相邻元素边缘间距

        # 复现 next_to 链，计算各项 x 坐标
        formula_1    = MathTex(r"\sqrt{R^2 - (0s)^2}")
        formula_2    = MathTex(r"\sqrt{R^2 - (1s)^2}")
        formula_3    = MathTex(r"\sqrt{R^2 - (2s)^2}")
        formula_final = MathTex(r"\sqrt{R^2 - ((n-1)s)^2}")

        _nf1 = formula_1.copy().move_to(ORIGIN)
        _np1 = MathTex("+").next_to(_nf1, RIGHT, buff=gap)
        _nf2 = formula_2.copy().next_to(_np1, RIGHT, buff=gap)
        _np2 = MathTex("+").next_to(_nf2, RIGHT, buff=gap)
        _nf3 = formula_3.copy().next_to(_np2, RIGHT, buff=gap)
        _np3 = MathTex("+").next_to(_nf3, RIGHT, buff=gap)
        _ndt = MathTex(r"\cdots").next_to(_np3, RIGHT, buff=gap)
        _np4 = MathTex("+").next_to(_ndt, RIGHT, buff=gap)
        _nff = formula_final.copy().next_to(_np4, RIGHT, buff=gap)
        num_ref = VGroup(_nf1, _np1, _nf2, _np2, _nf3, _np3, _ndt, _np4, _nff)
        num_ref.move_to([cx, 0, 0])

        x_f1 = _nf1.get_center()[0]
        x_p1 = _np1.get_center()[0]
        x_f2 = _nf2.get_center()[0]
        x_p2 = _np2.get_center()[0]
        x_f3 = _nf3.get_center()[0]
        x_p3 = _np3.get_center()[0]
        x_dt = _ndt.get_center()[0]
        x_p4 = _np4.get_center()[0]
        x_ff = _nff.get_center()[0]

        # 分子/分母行 y（边缘距分数线 0.24）
        _ref_f = formula_1.copy()
        _ref_f.next_to([cx, frac_center_y, 0], UP, buff=0.24)
        num_y = _ref_f.get_center()[1]
        _ref_r = MathTex("R")
        _ref_r.next_to([cx, frac_center_y, 0], DOWN, buff=0.24)
        den_y = _ref_r.get_center()[1]

        # 分子各项
        formula_1.move_to([x_f1, num_y, 0])
        formula_2.move_to([x_f2, num_y, 0])
        formula_3.move_to([x_f3, num_y, 0])
        formula_final.move_to([x_ff, num_y, 0])
        h_dots_num = MathTex(r"\cdots").move_to([x_dt, num_y, 0])

        plus_num_1 = MathTex("+").move_to([x_p1, num_y, 0])
        plus_num_2 = MathTex("+").move_to([x_p2, num_y, 0])
        plus_num_3 = MathTex("+").move_to([x_p3, num_y, 0])
        plus_num_4 = MathTex("+").move_to([x_p4, num_y, 0])

        # 分母各项
        r_copy_1 = MathTex("R").move_to([x_f1, den_y, 0])
        r_copy_2 = MathTex("R").move_to([x_f2, den_y, 0])
        r_copy_3 = MathTex("R").move_to([x_f3, den_y, 0])
        r_copy_4 = MathTex("R").move_to([x_ff, den_y, 0])
        h_dots_den = MathTex(r"\cdots").move_to([x_dt, den_y, 0])

        plus_den_1 = MathTex("+").move_to([x_p1, den_y, 0])
        plus_den_2 = MathTex("+").move_to([x_p2, den_y, 0])
        plus_den_3 = MathTex("+").move_to([x_p3, den_y, 0])
        plus_den_4 = MathTex("+").move_to([x_p4, den_y, 0])

        # 分数线
        frac_left  = _nf1.get_left()[0]  - 0.2
        frac_right = _nff.get_right()[0] + 0.2
        frac_line = Line(
            [frac_left,  frac_center_y, 0],
            [frac_right, frac_center_y, 0],
            color=WHITE, stroke_width=3
        )

        # n→∞ 标签
        n_label = MathTex(r"n \to \infty").scale(1.2)
        n_label.move_to([-5.0, frac_center_y, 0])

        self.add(
            grid,
            n_label,
            formula_1, plus_num_1, formula_2, plus_num_2,
            formula_3, plus_num_3, h_dots_num, plus_num_4, formula_final,
            r_copy_1,  plus_den_1, r_copy_2,  plus_den_2,
            r_copy_3,  plus_den_3, h_dots_den, plus_den_4, r_copy_4,
            frac_line,
        )

        # === Scene8 动画从这里开始 ===
        self.wait(1)

        m_label = MathTex(r"m = \frac{1}{2}").scale(1.2)
        m_label.move_to([16, 5.0, 0])
        self.play(FadeIn(m_label), run_time=1)
        self.wait(0.5)

        # --- m=1 标签 ---
        m1_label = MathTex(r"m = 1").scale(1.2)
        m1_label.move_to([16, 3.0, 0])
        self.play(FadeIn(m1_label), run_time=1)
        self.wait(0.5)

        # --- m=1 分式布局（frac_center_y=3.0，cx=5.5，gap=0.3）---
        frac2_cy = 3.0

        # 分子项
        m1_nf1 = MathTex(r"R^2", r"-(0s)^2")
        m1_nf2 = MathTex(r"R^2", r"-(1s)^2")
        m1_nf3 = MathTex(r"R^2", r"-(2s)^2")
        m1_nff = MathTex(r"R^2", r"-((n-1)s)^2")

        # 用 next_to 链推算 x 坐标，整体居中于 cx=5.5
        _r1  = m1_nf1.copy().move_to(ORIGIN)
        _rp1 = MathTex("+").next_to(_r1,  RIGHT, buff=gap)
        _r2  = m1_nf2.copy().next_to(_rp1, RIGHT, buff=gap)
        _rp2 = MathTex("+").next_to(_r2,  RIGHT, buff=gap)
        _r3  = m1_nf3.copy().next_to(_rp2, RIGHT, buff=gap)
        _rp3 = MathTex("+").next_to(_r3,  RIGHT, buff=gap)
        _rdt = MathTex(r"\cdots").next_to(_rp3, RIGHT, buff=gap)
        _rp4 = MathTex("+").next_to(_rdt, RIGHT, buff=gap)
        _rff = m1_nff.copy().next_to(_rp4, RIGHT, buff=gap)
        _m1_ref = VGroup(_r1, _rp1, _r2, _rp2, _r3, _rp3, _rdt, _rp4, _rff)
        _m1_ref.move_to([cx, 0, 0])

        m1_x1  = _r1.get_center()[0]
        m1_xp1 = _rp1.get_center()[0]
        m1_x2  = _r2.get_center()[0]
        m1_xp2 = _rp2.get_center()[0]
        m1_x3  = _r3.get_center()[0]
        m1_xp3 = _rp3.get_center()[0]
        m1_xdt = _rdt.get_center()[0]
        m1_xp4 = _rp4.get_center()[0]
        m1_xff = _rff.get_center()[0]

        # 分数线左右边界（提前计算）
        m1_frac_left  = _r1.get_left()[0]  - 0.2
        m1_frac_right = _rff.get_right()[0] + 0.2

        # 分子/分母行 y 坐标
        _yn = m1_nf1.copy().next_to([cx, frac2_cy, 0], UP,   buff=0.24)
        m1_num_y = _yn.get_center()[1]
        _yd = MathTex(r"R^2").next_to([cx, frac2_cy, 0],     DOWN, buff=0.24)
        m1_den_y = _yd.get_center()[1]

        # 分子各项就位
        m1_nf1.move_to([m1_x1,  m1_num_y, 0])
        m1_nf2.move_to([m1_x2,  m1_num_y, 0])
        m1_nf3.move_to([m1_x3,  m1_num_y, 0])
        m1_nff.move_to([m1_xff, m1_num_y, 0])
        m1_nd  = MathTex(r"\cdots").move_to([m1_xdt, m1_num_y, 0])
        m1_np1 = MathTex("+").move_to([m1_xp1, m1_num_y, 0])
        m1_np2 = MathTex("+").move_to([m1_xp2, m1_num_y, 0])
        m1_np3 = MathTex("+").move_to([m1_xp3, m1_num_y, 0])
        m1_np4 = MathTex("+").move_to([m1_xp4, m1_num_y, 0])

        # 分母加号、省略号（发牌后出现）
        m1_dd  = MathTex(r"\cdots").move_to([m1_xdt, m1_den_y, 0])
        m1_dp1 = MathTex("+").move_to([m1_xp1, m1_den_y, 0])
        m1_dp2 = MathTex("+").move_to([m1_xp2, m1_den_y, 0])
        m1_dp3 = MathTex("+").move_to([m1_xp3, m1_den_y, 0])
        m1_dp4 = MathTex("+").move_to([m1_xp4, m1_den_y, 0])
        m1_frac_line = Line(
            [m1_frac_left,  frac2_cy, 0],
            [m1_frac_right, frac2_cy, 0],
            color=WHITE, stroke_width=3
        )

        # 步骤1：分子行从左到右依次出现
        self.play(
            LaggedStart(
                FadeIn(m1_nf1),
                FadeIn(m1_np1),
                FadeIn(m1_nf2),
                FadeIn(m1_np2),
                FadeIn(m1_nf3),
                FadeIn(m1_np3),
                FadeIn(m1_nd),
                FadeIn(m1_np4),
                FadeIn(m1_nff),
                lag_ratio=0.15
            ),
            run_time=2
        )
        self.wait(0.5)

        # 步骤2：R²-(0s)² → R²（ReplacementTransform，底部对齐消除 bounding box 偏移）
        m1_r2_src = MathTex(r"R^2").move_to([m1_x1, m1_num_y, 0]).align_to(m1_nf2, UP)
        self.play(ReplacementTransform(m1_nf1, m1_r2_src), run_time=0.8)
        self.wait(0.3)

        # 步骤3：发牌 —— Scene03 模式
        # 隐藏 emitter 定位于 m1_r2_src，令每张牌从源位置淡出飞入
        emitter = m1_r2_src.copy()
        emitter.move_to(m1_r2_src.get_center())
        emitter.set_opacity(0)
        self.add(emitter)

        # 目标：m1_r2_src 的副本，分别定位到分母四列
        dr1 = m1_r2_src.copy().move_to([m1_x1,  m1_den_y, 0])
        dr2 = m1_r2_src.copy().move_to([m1_x2,  m1_den_y, 0])
        dr3 = m1_r2_src.copy().move_to([m1_x3,  m1_den_y, 0])
        dr4 = m1_r2_src.copy().move_to([m1_xff, m1_den_y, 0])

        deal_anims = [TransformFromCopy(emitter, t) for t in [dr1, dr2, dr3, dr4]]
        self.play(
            LaggedStart(*deal_anims, lag_ratio=0.15),
            Create(m1_frac_line),
            FadeIn(VGroup(m1_dd, m1_dp1, m1_dp2, m1_dp3, m1_dp4)),
            run_time=1.5
        )
        self.wait(0.5)

        # 步骤5：R² → R²-(0s)²（ReplacementTransform 还原）
        m1_nf1_restored = MathTex(r"R^2", r"-(0s)^2").move_to([m1_x1, m1_num_y, 0])
        self.play(ReplacementTransform(m1_r2_src, m1_nf1_restored), run_time=0.8)
        self.wait(1)

        # =====================================================================
        # 第二行公式：AR² - s²(0²+1²+···+(n-1)²) / AR²
        # =====================================================================
        eq_sign = MathTex(r"=").scale(1.4).move_to([-2.5, 0.5, 0])
        self.play(FadeIn(eq_sign), run_time=0.5)
        self.wait(0.3)

        frac3_cy = 0.5

        # 新分子三段：[0]=AR²，[1]=-，[2]=s²(0²+1²+···+(n-1)²)
        new_num = MathTex(r"AR^2", r"-", r"s^2(0^2+1^2+2^2+\cdots+(n-1)^2)")
        new_den = MathTex(r"AR^2")

        # Y 坐标
        _yn3 = new_num.copy().next_to([0, frac3_cy, 0], UP,   buff=0.24)
        num3_y = _yn3.get_center()[1]
        _yd3 = new_den.copy().next_to([0, frac3_cy, 0], DOWN, buff=0.24)
        den3_y = _yd3.get_center()[1]

        # X 坐标：new_num 左边距 eq_sign 右边 0.5
        new_num.move_to([0, num3_y, 0])
        new_num.set_x(eq_sign.get_right()[0] + 0.5 + new_num.width / 2)

        cx3 = new_num.get_center()[0]
        new_den.move_to([cx3, den3_y, 0])

        frac3_left  = new_num.get_left()[0]  - 0.2
        frac3_right = new_num.get_right()[0] + 0.2
        frac3_line  = Line([frac3_left,  frac3_cy, 0],
                            [frac3_right, frac3_cy, 0],
                            color=WHITE, stroke_width=3)

        # 步骤A：分数线出现 + 分母4个R²同时飞向 new_den(AR²)
        den_anims = [TransformFromCopy(src, new_den.copy())
                     for src in [dr1, dr2, dr3, dr4]]
        self.play(
            Create(frac3_line),
            *den_anims,
            run_time=1.2
        )
        self.wait(0.3)

        # 步骤B：分子各项R²（用[0]子项取实际位置）同时飞向 new_num[0]（AR²）
        r2_srcs = [m1_nf1_restored[0], m1_nf2[0], m1_nf3[0], m1_nff[0]]
        nR2_anims = [TransformFromCopy(s, new_num[0].copy()) for s in r2_srcs]
        self.play(*nR2_anims, run_time=1.2)
        self.wait(1)
