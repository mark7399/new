import math
from manim import *

# =============================================================================
# 共享常量
# =============================================================================
BG_COLOR = "#16161d"
ORIGIN_POINT = np.array([0, 0, 0])
RADIUS = 5


# =============================================================================
# Scene 1: 开场与相机移动
# =============================================================================
class Scene1_Intro(MovingCameraScene):
    """开场：显示完整圆、网格、边界框，相机移动到第一象限"""
    
    def construct(self):
        self.camera.background_color = BLACK
        origin_point = ORIGIN_POINT
        
        # 创建网格
        grid = NumberPlane(
            x_range=[-20, 20],
            y_range=[-15, 15],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
        )
        
        # 初始相机设置
        zoom_factor = 1.5
        self.camera.frame.scale(zoom_factor)
        self.camera.frame.move_to(origin_point)

        # 创建完整的圆
        circle = Circle(radius=RADIUS, color=WHITE, stroke_width=3)
        circle.move_to(origin_point)

        # 1. 最初只显示圆
        self.add(circle)
        self.wait(1)
        
        # 2. 显示网格并将背景过渡到 #16161d
        bg_rect = Rectangle(width=40, height=30, fill_color=BG_COLOR, fill_opacity=1, stroke_width=0)
        bg_rect.set_z_index(-1)
        bg_rect.move_to(origin_point)

        self.play(
            Create(grid),
            FadeIn(bg_rect),
            run_time=2
        )
        
        self.camera.background_color = BG_COLOR
        self.remove(bg_rect)
        self.wait(0.5)

        # 3. 绘制外部边界框
        bounding_box = Square(side_length=10, color=WHITE, stroke_width=3)
        bounding_box.move_to(origin_point)
        self.play(Create(bounding_box))
        self.wait(1)

        # 边界框消失
        self.play(Uncreate(bounding_box))
        
        # 4. 相机移动并放大，同时圆变为圆弧
        arc = Arc(
            radius=RADIUS,
            start_angle=0,
            angle=PI / 2,
            color=WHITE,
            stroke_width=3,
            arc_center=origin_point
        )
        
        self.play(
            self.camera.frame.animate.move_to([4.5, 2.5, 0]).scale(1/zoom_factor),
            ReplacementTransform(circle, arc),
            run_time=2
        )
        
        self.wait(1)


# =============================================================================
# Scene 2: n=2 演示
# =============================================================================
class Scene2_N2(MovingCameraScene):
    """n=2 演示：两个矩形逼近，带详细标注"""
    
    def construct(self):
        self.camera.background_color = BG_COLOR
        origin_point = ORIGIN_POINT
        
        # === 重建 Scene1 结束状态 ===
        # 网格
        grid = NumberPlane(
            x_range=[-20, 20],
            y_range=[-15, 15],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
        )
        
        # 圆弧
        arc = Arc(
            radius=RADIUS,
            start_angle=0,
            angle=PI / 2,
            color=WHITE,
            stroke_width=3,
            arc_center=origin_point
        )
        
        # 相机位置
        self.camera.frame.move_to([4.5, 2.5, 0])
        
        self.add(grid, arc)
        
        # === Scene2 动画 ===
        # 显示 n=2
        n_label = MathTex("n=2")
        n_label.move_to([8, 5, 0])
        n_label.scale(1.2)
        self.play(Write(n_label), run_time=1)
        
        # 半径角度追踪器
        angle_tracker = ValueTracker(PI / 2)
        
        # 半径线
        l1 = Line(origin_point, origin_point + UP * RADIUS, color=WHITE, stroke_width=3)
        l1.add_updater(lambda m: m.put_start_and_end_on(
            origin_point,
            origin_point + np.array([
                RADIUS * np.cos(angle_tracker.get_value()),
                RADIUS * np.sin(angle_tracker.get_value()),
                0
            ])
        ))
        
        # R标签
        label_R = MathTex("R").scale(1)
        def update_label_R(m):
            theta = angle_tracker.get_value()
            midpoint = np.array([2.5 * np.cos(theta), 2.5 * np.sin(theta), 0])
            normal = np.array([-np.sin(theta), np.cos(theta), 0])
            m.move_to(midpoint + normal * 0.5)
        label_R.add_updater(update_label_R)
        
        # s标签
        label_s = MathTex("s").scale(1)
        def update_label_s(m):
            theta = angle_tracker.get_value()
            current_x = RADIUS * np.cos(theta)
            m.move_to([current_x / 2, -0.24, 0])
        label_s.add_updater(update_label_s)
        
        self.add(l1, label_R, label_s)
        
        # 目标角度
        x_step = 2.5
        target_angle_1 = np.arccos(x_step / RADIUS)
        
        # 第一组动态线
        v_line = always_redraw(lambda: Line(
            start=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())),
            end=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())) + UP * RADIUS,
            color=WHITE, stroke_width=2
        ))
        h_line = always_redraw(lambda: Line(
            start=origin_point + UP * RADIUS,
            end=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())) + UP * RADIUS,
            color=WHITE, stroke_width=2
        ))
        self.add(v_line, h_line)
        
        # 第一阶段动画
        self.play(angle_tracker.animate.set_value(target_angle_1), run_time=2, rate_func=linear)
        
        v_line.clear_updaters()
        h_line.clear_updaters()
        label_s.clear_updaters()
        
        self.wait(1)
        
        # 蓝色高亮线
        y1 = RADIUS * np.sin(target_angle_1)
        temp_blue_line = Line([2.5, 0, 0], [2.5, y1, 0], color=BLUE, stroke_width=4)
        self.add(temp_blue_line)
        self.wait(1)
        
        # 显示公式
        formula_1 = MathTex(r"\sqrt{R^2 - (0s)^2}")
        formula_2 = MathTex(r"\sqrt{R^2 - (1s)^2}")
        formula_1.next_to(n_label, DOWN)
        formula_2.next_to(formula_1, DOWN)
        self.play(Write(formula_1), Write(formula_2), run_time=1)
        
        # 动态 1.0s 标签
        coeff_val = DecimalNumber(1.0, num_decimal_places=1, include_sign=False)
        unit_label = MathTex("s")
        moving_label = VGroup(coeff_val, unit_label)
        moving_label.arrange(RIGHT, buff=0.1)
        moving_label.move_to(label_s.get_center())
        
        def update_moving_label(m):
            theta = angle_tracker.get_value()
            current_x = RADIUS * np.cos(theta)
            val = current_x / 2.5
            truncated_val = math.floor(val * 10) / 10
            coeff_val.set_value(truncated_val)
            unit_label.next_to(coeff_val, RIGHT, buff=0.1)
            m.move_to([current_x / 2, -0.24, 0])
        
        moving_label.add_updater(update_moving_label)
        self.add(moving_label)
        
        self.remove(temp_blue_line)
        
        # 第二组动态线
        v_line_2 = always_redraw(lambda: Line(
            start=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())),
            end=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())) + UP * y1,
            color=WHITE, stroke_width=2
        ))
        h_line_2 = always_redraw(lambda: Line(
            start=origin_point + RIGHT * 2.5 + UP * y1,
            end=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())) + UP * y1,
            color=WHITE, stroke_width=2
        ))
        self.add(v_line_2, h_line_2)
        
        # 第二阶段动画
        self.play(angle_tracker.animate.set_value(0), run_time=3, rate_func=linear)
        
        v_line_2.clear_updaters()
        h_line_2.clear_updaters()
        moving_label.clear_updaters()
        
        self.wait(1)


# =============================================================================
# Scene 3: n=3 演示
# =============================================================================
class Scene3_N3(MovingCameraScene):
    """n=3 演示：三个矩形连续绘制"""
    
    def construct(self):
        self.camera.background_color = BG_COLOR
        origin_point = ORIGIN_POINT
        
        # === 重建 Scene2 结束状态（清理后）===
        grid = NumberPlane(
            x_range=[-20, 20], y_range=[-15, 15],
            background_line_style={"stroke_color": GREY, "stroke_width": 1, "stroke_opacity": 0.5},
        )
        arc = Arc(radius=RADIUS, start_angle=0, angle=PI/2, color=WHITE, stroke_width=3, arc_center=origin_point)
        n_label = MathTex("n=3")
        n_label.move_to([8, 5, 0])
        n_label.scale(1.2)
        
        self.camera.frame.move_to([4.5, 2.5, 0])
        self.add(grid, arc, n_label)
        
        # === Scene3 动画 ===
        angle_tracker = ValueTracker(PI / 2)
        x_step_3 = 5.0 / 3.0
        target_angle_1 = np.arccos(1/3)
        target_angle_2 = np.arccos(2/3)
        
        # s标签
        label_s_3 = MathTex("s").scale(1)
        def update_label_s_3(m):
            theta = angle_tracker.get_value()
            current_x = RADIUS * np.cos(theta)
            if current_x <= x_step_3:
                m.move_to([current_x / 2, -0.24, 0])
            else:
                m.move_to([x_step_3 / 2, -0.24, 0])
        label_s_3.add_updater(update_label_s_3)
        self.add(label_s_3)
        
        # 公式
        formula_1 = MathTex(r"\sqrt{R^2 - (0s)^2}")
        formula_2 = MathTex(r"\sqrt{R^2 - (1s)^2}")
        formula_1.next_to(n_label, DOWN)
        formula_2.next_to(formula_1, DOWN)
        self.add(formula_1, formula_2)
        
        # 矩形1
        v_line_3_1 = always_redraw(lambda: Line(
            start=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())),
            end=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())) + UP * RADIUS,
            color=WHITE, stroke_width=2
        ))
        h_line_3_1 = always_redraw(lambda: Line(
            start=origin_point + UP * RADIUS,
            end=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())) + UP * RADIUS,
            color=WHITE, stroke_width=2
        ))
        self.add(v_line_3_1, h_line_3_1)
        
        self.play(angle_tracker.animate.set_value(target_angle_1), run_time=1.5, rate_func=linear)
        v_line_3_1.clear_updaters()
        h_line_3_1.clear_updaters()
        y1_3 = RADIUS * np.sin(target_angle_1)
        
        # 矩形2
        v_line_3_2 = always_redraw(lambda: Line(
            start=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())),
            end=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())) + UP * y1_3,
            color=WHITE, stroke_width=2
        ))
        h_line_3_2 = always_redraw(lambda: Line(
            start=origin_point + RIGHT * x_step_3 + UP * y1_3,
            end=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())) + UP * y1_3,
            color=WHITE, stroke_width=2
        ))
        self.add(v_line_3_2, h_line_3_2)
        
        self.play(angle_tracker.animate.set_value(target_angle_2), run_time=1.5, rate_func=linear)
        v_line_3_2.clear_updaters()
        h_line_3_2.clear_updaters()
        y2_3 = RADIUS * np.sin(target_angle_2)
        
        # 矩形3
        v_line_3_3 = always_redraw(lambda: Line(
            start=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())),
            end=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())) + UP * y2_3,
            color=WHITE, stroke_width=2
        ))
        h_line_3_3 = always_redraw(lambda: Line(
            start=origin_point + RIGHT * (2 * x_step_3) + UP * y2_3,
            end=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())) + UP * y2_3,
            color=WHITE, stroke_width=2
        ))
        self.add(v_line_3_3, h_line_3_3)
        
        formula_3 = MathTex(r"\sqrt{R^2 - (2s)^2}")
        formula_3.next_to(formula_2, DOWN, aligned_edge=LEFT)
        
        self.play(angle_tracker.animate.set_value(0), Write(formula_3), run_time=1.5, rate_func=linear)
        v_line_3_3.clear_updaters()
        h_line_3_3.clear_updaters()
        label_s_3.clear_updaters()
        
        self.wait(1)


# =============================================================================
# Scene 4: n=4 演示
# =============================================================================
class Scene4_N4(MovingCameraScene):
    """n=4 演示：四个矩形连续绘制"""
    
    def construct(self):
        self.camera.background_color = BG_COLOR
        origin_point = ORIGIN_POINT
        
        # === 重建 Scene3 结束状态（清理后）===
        grid = NumberPlane(
            x_range=[-20, 20], y_range=[-15, 15],
            background_line_style={"stroke_color": GREY, "stroke_width": 1, "stroke_opacity": 0.5},
        )
        arc = Arc(radius=RADIUS, start_angle=0, angle=PI/2, color=WHITE, stroke_width=3, arc_center=origin_point)
        n_label = MathTex("n=4")
        n_label.move_to([8, 5, 0])
        n_label.scale(1.2)
        
        # 公式
        formula_1 = MathTex(r"\sqrt{R^2 - (0s)^2}")
        formula_2 = MathTex(r"\sqrt{R^2 - (1s)^2}")
        formula_3 = MathTex(r"\sqrt{R^2 - (2s)^2}")
        formula_1.next_to(n_label, DOWN)
        formula_2.next_to(formula_1, DOWN)
        formula_3.next_to(formula_2, DOWN, aligned_edge=LEFT)
        
        self.camera.frame.move_to([4.5, 2.5, 0])
        self.add(grid, arc, n_label, formula_1, formula_2, formula_3)
        
        # === Scene4 动画 ===
        angle_tracker = ValueTracker(PI / 2)
        x_step_4 = 5.0 / 4.0
        target_angle_1 = np.arccos(1/4)
        target_angle_2 = np.arccos(2/4)
        target_angle_3 = np.arccos(3/4)
        
        # s标签
        label_s_4 = MathTex("s").scale(1)
        def update_label_s_4(m):
            theta = angle_tracker.get_value()
            current_x = RADIUS * np.cos(theta)
            if current_x <= x_step_4:
                m.move_to([current_x / 2, -0.24, 0])
            else:
                m.move_to([x_step_4 / 2, -0.24, 0])
        label_s_4.add_updater(update_label_s_4)
        self.add(label_s_4)
        
        # 矩形1
        v_line_4_1 = always_redraw(lambda: Line(
            start=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())),
            end=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())) + UP * RADIUS,
            color=WHITE, stroke_width=2
        ))
        h_line_4_1 = always_redraw(lambda: Line(
            start=origin_point + UP * RADIUS,
            end=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())) + UP * RADIUS,
            color=WHITE, stroke_width=2
        ))
        self.add(v_line_4_1, h_line_4_1)
        
        self.play(angle_tracker.animate.set_value(target_angle_1), run_time=1, rate_func=linear)
        v_line_4_1.clear_updaters()
        h_line_4_1.clear_updaters()
        y1_4 = RADIUS * np.sin(target_angle_1)
        
        # 矩形2
        v_line_4_2 = always_redraw(lambda: Line(
            start=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())),
            end=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())) + UP * y1_4,
            color=WHITE, stroke_width=2
        ))
        h_line_4_2 = always_redraw(lambda: Line(
            start=origin_point + RIGHT * x_step_4 + UP * y1_4,
            end=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())) + UP * y1_4,
            color=WHITE, stroke_width=2
        ))
        self.add(v_line_4_2, h_line_4_2)
        
        self.play(angle_tracker.animate.set_value(target_angle_2), run_time=1, rate_func=linear)
        v_line_4_2.clear_updaters()
        h_line_4_2.clear_updaters()
        y2_4 = RADIUS * np.sin(target_angle_2)
        
        # 矩形3
        v_line_4_3 = always_redraw(lambda: Line(
            start=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())),
            end=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())) + UP * y2_4,
            color=WHITE, stroke_width=2
        ))
        h_line_4_3 = always_redraw(lambda: Line(
            start=origin_point + RIGHT * (2 * x_step_4) + UP * y2_4,
            end=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())) + UP * y2_4,
            color=WHITE, stroke_width=2
        ))
        self.add(v_line_4_3, h_line_4_3)
        
        self.play(angle_tracker.animate.set_value(target_angle_3), run_time=1, rate_func=linear)
        v_line_4_3.clear_updaters()
        h_line_4_3.clear_updaters()
        y3_4 = RADIUS * np.sin(target_angle_3)
        
        # 矩形4
        v_line_4_4 = always_redraw(lambda: Line(
            start=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())),
            end=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())) + UP * y3_4,
            color=WHITE, stroke_width=2
        ))
        h_line_4_4 = always_redraw(lambda: Line(
            start=origin_point + RIGHT * (3 * x_step_4) + UP * y3_4,
            end=origin_point + RIGHT * (RADIUS * np.cos(angle_tracker.get_value())) + UP * y3_4,
            color=WHITE, stroke_width=2
        ))
        self.add(v_line_4_4, h_line_4_4)
        
        formula_4 = MathTex(r"\sqrt{R^2 - (3s)^2}")
        formula_4.next_to(formula_3, DOWN, aligned_edge=LEFT)
        
        self.play(angle_tracker.animate.set_value(0), Write(formula_4), run_time=1, rate_func=linear)
        v_line_4_4.clear_updaters()
        h_line_4_4.clear_updaters()
        label_s_4.clear_updaters()
        
        self.wait(1)


# =============================================================================
# Scene 5: n 推广（n=4→5→6→16→32）
# =============================================================================
class Scene5_N_General(MovingCameraScene):
    """n 推广：从 n=4 平滑变换到 n=32"""
    
    def construct(self):
        self.camera.background_color = BG_COLOR
        origin_point = ORIGIN_POINT
        
        # === 重建 Scene4 结束状态 ===
        grid = NumberPlane(
            x_range=[-20, 20], y_range=[-15, 15],
            background_line_style={"stroke_color": GREY, "stroke_width": 1, "stroke_opacity": 0.5},
        )
        arc = Arc(radius=RADIUS, start_angle=0, angle=PI/2, color=WHITE, stroke_width=3, arc_center=origin_point)
        
        # n=4 的4个矩形
        def create_n_rects_group(n):
            group = VGroup()
            dx = 5.0 / n
            for i in range(n):
                x_left = i * dx
                x_right = (i + 1) * dx
                height = np.sqrt(25 - x_left**2)
                v_line = Line([x_right, 0, 0], [x_right, height, 0], color=WHITE, stroke_width=2)
                h_line = Line([x_left, height, 0], [x_right, height, 0], color=WHITE, stroke_width=2)
                group.add(v_line, h_line)
            return group
        
        rects_n4 = create_n_rects_group(4)
        
        # s标签
        label_s_4 = MathTex("s").scale(1)
        label_s_4.move_to([5.0/4.0/2, -0.24, 0])
        
        # 标签和公式
        n_label = MathTex("n")
        n_label.move_to([8, 5, 0])
        n_label.scale(1.2)
        
        formula_1 = MathTex(r"\sqrt{R^2 - (0s)^2}")
        formula_2 = MathTex(r"\sqrt{R^2 - (1s)^2}")
        formula_3 = MathTex(r"\sqrt{R^2 - (2s)^2}")
        dots = MathTex(r"\vdots")
        formula_final = MathTex(r"\sqrt{R^2 - ((n-1)s)^2}")
        
        formula_1.next_to(n_label, DOWN)
        formula_2.next_to(formula_1, DOWN)
        formula_3.next_to(formula_2, DOWN, aligned_edge=LEFT)
        dots.next_to(formula_3, DOWN)
        formula_final.next_to(dots, DOWN, aligned_edge=LEFT)
        formula_final.align_to(formula_3, LEFT)
        
        self.camera.frame.move_to([4.5, 2.5, 0])
        self.add(grid, arc, rects_n4, label_s_4, n_label, formula_1, formula_2, formula_3, dots, formula_final)
        
        # === Scene5 动画 ===
        # n=4 -> n=5
        rects_n5 = create_n_rects_group(5)
        self.play(
            ReplacementTransform(rects_n4, rects_n5),
            label_s_4.animate.move_to([0.5, -0.24, 0]),
            run_time=1.5
        )
        self.wait(0.5)
        
        # n=5 -> n=6
        rects_n6 = create_n_rects_group(6)
        self.play(
            ReplacementTransform(rects_n5, rects_n6),
            label_s_4.animate.move_to([(5.0/6.0)/2, -0.24, 0]),
            run_time=1.5
        )
        self.wait(0.5)
        
        # n=6 -> n=16
        rects_n16 = create_n_rects_group(16)
        self.play(
            ReplacementTransform(rects_n6, rects_n16),
            label_s_4.animate.move_to([(5.0/16.0)/2, -0.24, 0]),
            run_time=1.5
        )
        self.wait(0.5)
        
        # n=16 -> n=32
        rects_n32 = create_n_rects_group(32)
        self.play(
            ReplacementTransform(rects_n16, rects_n32),
            label_s_4.animate.move_to([(5.0/32.0)/2, -0.24, 0]),
            run_time=1.5
        )
        
        self.wait(1)


# =============================================================================
# Scene 6: n→∞ 与积分填充
# =============================================================================
class Scene6_N_Infinity(MovingCameraScene):
    """最终阶段：n→∞ 和曲线下方面积填充"""
    
    def construct(self):
        self.camera.background_color = BG_COLOR
        origin_point = ORIGIN_POINT
        
        # === 重建 Scene5 结束状态 ===
        grid = NumberPlane(
            x_range=[-20, 20], y_range=[-15, 15],
            background_line_style={"stroke_color": GREY, "stroke_width": 1, "stroke_opacity": 0.5},
        )
        arc = Arc(radius=RADIUS, start_angle=0, angle=PI/2, color=WHITE, stroke_width=3, arc_center=origin_point)
        
        # n=32 矩形
        def create_n_rects_group(n):
            group = VGroup()
            dx = 5.0 / n
            for i in range(n):
                x_left = i * dx
                x_right = (i + 1) * dx
                height = np.sqrt(25 - x_left**2)
                v_line = Line([x_right, 0, 0], [x_right, height, 0], color=WHITE, stroke_width=2)
                h_line = Line([x_left, height, 0], [x_right, height, 0], color=WHITE, stroke_width=2)
                group.add(v_line, h_line)
            return group
        
        rects_n32 = create_n_rects_group(32)
        
        # s标签
        label_s_4 = MathTex("s").scale(1)
        label_s_4.move_to([(5.0/32.0)/2, -0.24, 0])
        
        # n→∞ 标签和公式
        n_label = MathTex(r"n \to \infty")
        n_label.move_to([8, 5, 0])
        n_label.scale(1.2)
        
        formula_1 = MathTex(r"\sqrt{R^2 - (0s)^2}")
        formula_2 = MathTex(r"\sqrt{R^2 - (1s)^2}")
        formula_3 = MathTex(r"\sqrt{R^2 - (2s)^2}")
        dots = MathTex(r"\vdots")
        formula_final = MathTex(r"\sqrt{R^2 - ((n-1)s)^2}")
        
        formula_1.next_to(n_label, DOWN)
        formula_2.next_to(formula_1, DOWN)
        formula_3.next_to(formula_2, DOWN, aligned_edge=LEFT)
        dots.next_to(formula_3, DOWN)
        formula_final.next_to(dots, DOWN, aligned_edge=LEFT)
        formula_final.align_to(formula_3, LEFT)
        
        self.camera.frame.move_to([4.5, 2.5, 0])
        self.add(grid, arc, rects_n32, label_s_4, n_label, formula_1, formula_2, formula_3, dots, formula_final)
        
        # === Scene6 动画 ===
        # FadeOut 左侧元素
        self.play(FadeOut(label_s_4), FadeOut(rects_n32), run_time=1)
        
        # 半径角度追踪器
        angle_tracker = ValueTracker(PI / 2)
        
        # 填充区域函数
        def get_under_curve_points(x_end, radius=RADIUS, num_points=30):
            points = [[0, 0, 0]]
            for i in range(num_points + 1):
                x = x_end * (i / num_points)
                y = np.sqrt(radius**2 - x**2) if x <= radius else 0
                points.append([x, y, 0])
            points.append([x_end, 0, 0])
            points.append([0, 0, 0])
            return points
        
        # 初始填充区域
        fill_area = Polygon(
            *get_under_curve_points(0),
            fill_color=WHITE, fill_opacity=0.28, stroke_width=0
        )
        self.add(fill_area)
        
        # 半径线
        radius_line = Line([0, 0, 0], [0, RADIUS, 0], color=WHITE, stroke_width=3)
        def update_radius(m):
            theta = angle_tracker.get_value()
            x = RADIUS * np.cos(theta)
            y = RADIUS * np.sin(theta)
            m.put_start_and_end_on([0, 0, 0], [x, y, 0])
        radius_line.add_updater(update_radius)
        self.add(radius_line)
        
        # 填充区域更新
        def update_fill_area(m):
            theta = angle_tracker.get_value()
            x_end = RADIUS * np.cos(theta)
            points = get_under_curve_points(x_end)
            m.set_points_as_corners(points)
        fill_area.add_updater(update_fill_area)
        
        # 动画：半径旋转，填充区域展开
        self.play(angle_tracker.animate.set_value(0), run_time=3, rate_func=linear)
        
        radius_line.clear_updaters()
        fill_area.clear_updaters()
        
        self.wait(0.5)
        
        # === 添加大括号和面积公式 ===
        # 创建包含四个公式的大括号
        formulas_group = VGroup(formula_1, formula_2, formula_3, formula_final)
        
        # 左侧大括号
        brace = Brace(formulas_group, direction=LEFT, color=WHITE)
        
        # = s × 标签
        s_times_label = MathTex("= s \\times").scale(1.2)
        s_times_label.next_to(brace, LEFT, buff=0.2)
        
        # 动画显示：先显示 =s×，再显示大括号
        self.play(Write(s_times_label), run_time=0.8)
        self.play(Create(brace), run_time=0.8)
        
        self.wait(2)


# =============================================================================
# Scene 7: 四分之一圆与外接正方形比值
# =============================================================================
class Scene7_Ratio(MovingCameraScene):
    """场景7：展示四分之一圆与外接正方形的比值计算"""
    
    def construct(self):
        self.camera.background_color = BG_COLOR
        origin_point = ORIGIN_POINT
        
        # === 重建 Scene6 结束状态 ===
        # 网格
        grid = NumberPlane(
            x_range=[-20, 20], y_range=[-15, 15],
            background_line_style={"stroke_color": GREY, "stroke_width": 1, "stroke_opacity": 0.5},
        )
        
        # 圆弧
        arc = Arc(radius=RADIUS, start_angle=0, angle=PI/2, color=WHITE, stroke_width=3, arc_center=origin_point)
        
        # 填充区域（四分之一圆）
        def get_under_curve_points(x_end, radius=RADIUS, num_points=30):
            points = [[0, 0, 0]]
            for i in range(num_points + 1):
                x = x_end * (i / num_points)
                y = np.sqrt(radius**2 - x**2) if x <= radius else 0
                points.append([x, y, 0])
            points.append([x_end, 0, 0])
            points.append([0, 0, 0])
            return points
        
        fill_area = Polygon(
            *get_under_curve_points(RADIUS),
            fill_color=WHITE, fill_opacity=0.28, stroke_width=0
        )
        
        # 半径线（水平）
        radius_line = Line([0, 0, 0], [RADIUS, 0, 0], color=WHITE, stroke_width=3)
        
        # 右侧公式组
        n_label = MathTex(r"n \to \infty")
        n_label.move_to([8, 5, 0])
        n_label.scale(1.2)
        
        formula_1 = MathTex(r"\sqrt{R^2 - (0s)^2}")
        formula_2 = MathTex(r"\sqrt{R^2 - (1s)^2}")
        formula_3 = MathTex(r"\sqrt{R^2 - (2s)^2}")
        dots = MathTex(r"\vdots")
        formula_final = MathTex(r"\sqrt{R^2 - ((n-1)s)^2}")
        
        formula_1.next_to(n_label, DOWN)
        formula_2.next_to(formula_1, DOWN)
        formula_3.next_to(formula_2, DOWN, aligned_edge=LEFT)
        dots.next_to(formula_3, DOWN)
        formula_final.next_to(dots, DOWN, aligned_edge=LEFT)
        formula_final.align_to(formula_3, LEFT)
        
        # 大括号和 =s×
        formulas_group = VGroup(formula_1, formula_2, formula_3, formula_final)
        brace = Brace(formulas_group, direction=LEFT, color=WHITE)
        s_times_label = MathTex("= s \\times").scale(1.2)
        s_times_label.next_to(brace, LEFT, buff=0.2)
        
        # 相机位置
        self.camera.frame.move_to([4.5, 2.5, 0])
        
        self.add(grid, arc, fill_area, radius_line, n_label, formula_1, formula_2, formula_3, dots, formula_final, brace, s_times_label)
        
        # === Scene7 动画 ===
        
        # 1. 将 =s× 大括号以及 n→∞ 整体向右平移 0.5 格
        right_group = VGroup(n_label, formula_1, formula_2, formula_3, dots, formula_final, brace, s_times_label)
        self.play(right_group.animate.shift(RIGHT * 0.5), run_time=0.8)
        
        # 2. FadeIn 外接正方形白框
        bounding_square = Square(side_length=RADIUS, color=WHITE, stroke_width=2)
        bounding_square.move_to([RADIUS/2, RADIUS/2, 0])
        self.play(FadeIn(bounding_square), run_time=0.8)
        
        # 3. 只取消 y 轴显示，保留网格和 x 轴
        # 方法：获取原网格的 y 轴并设置为不可见
        y_axis = grid.get_y_axis()
        y_axis.set_stroke(opacity=0)
        self.wait(0.8)
        
        # 4. 在 √(R²-(0s)²) 右侧添加 =R
        equals_R = MathTex("= R").scale(1.2)
        equals_R.next_to(formula_1, RIGHT, buff=0.3)
        self.play(Write(equals_R), run_time=0.8)
        
        self.wait(0.5)
        
        # 5. 镜头远离并移动对准 (5.5, 0)
        # 当前相机在 [4.5, 2.5]，目标中心是 [5.5, 0]
        # 远离程度：scale(1.5) 表示放大视野（远离）
        # 调整方法：修改 scale 因子，越大越远离
        zoom_out_factor = 1.8  # 可以调整这个值来改变远离程度
        self.play(
            self.camera.frame.animate.move_to([5.5, 0, 0]).scale(zoom_out_factor),
            run_time=1.5
        )
        
        self.wait(0.5)
        
        # 6. 外接白框向下移动 5.7 格，四分之一圆往上微调 0.7 格
        quarter_circle_group = VGroup(arc, fill_area, radius_line)
        self.play(
            bounding_square.animate.shift(DOWN * 5.7),
            quarter_circle_group.animate.shift(UP * 0.7),
            run_time=1.2
        )
        
        self.wait(0.5)
        
        # 7. "=R" 变成 "R"，然后 R 分裂为4个分身飞向目标位置
        R_label = MathTex("R").scale(1.2)
        R_label.move_to(equals_R.get_center() + LEFT * 0.3)

        self.play(Transform(equals_R, R_label), run_time=0.5)

        # 先按目标布局定义各副本的最终位置
        R_copies = VGroup()
        r_copy_1 = MathTex("R").scale(1)
        r_copy_1.move_to([8.5, -1.2, 0])
        R_copies.add(r_copy_1)

        r_copy_2 = MathTex("R").scale(1)
        r_copy_2.next_to(r_copy_1, DOWN)
        R_copies.add(r_copy_2)

        r_copy_3 = MathTex("R").scale(1)
        r_copy_3.next_to(r_copy_2, DOWN)
        R_copies.add(r_copy_3)

        v_dots = MathTex(r"\vdots").scale(1)
        v_dots.next_to(r_copy_3, DOWN)

        r_copy_4 = MathTex("R").scale(1)
        r_copy_4.next_to(v_dots, DOWN)
        R_copies.add(r_copy_4)

        # 记录目标位置
        tgt = [mob.get_center().copy() for mob in [R_copies[0], R_copies[1], R_copies[2], v_dots, R_copies[3]]]

        # 所有副本先挪到源头（equals_R 当前位置），加入场景
        src = equals_R.get_center().copy()
        for mob in [R_copies[0], R_copies[1], R_copies[2], v_dots, R_copies[3]]:
            mob.move_to(src)
        self.add(R_copies[0], R_copies[1], R_copies[2], v_dots, R_copies[3])

        # 分裂动画：equals_R 淡出，同时各副本从源头飞向目标
        self.play(
            FadeOut(equals_R),
            R_copies[0].animate.move_to(tgt[0]),
            R_copies[1].animate.move_to(tgt[1]),
            R_copies[2].animate.move_to(tgt[2]),
            v_dots.animate.move_to(tgt[3]),
            R_copies[3].animate.move_to(tgt[4]),
            run_time=1.2
        )
        
        self.wait(0.5)
        
        # 8. 根据下方 R 的位置，绘制 =s× 大括号
        # 大括号要扩到所有 R
        # 调整方法：修改 R_copies 的 y 坐标，或调整大括号的参数
        
        R_group = VGroup(R_copies[0], R_copies[1], R_copies[2], v_dots, R_copies[3])
        brace_down = Brace(R_group, direction=LEFT, color=WHITE)
        s_times_label_down = MathTex("= s \\times").scale(1.2)
        s_times_label_down.next_to(brace_down, LEFT, buff=0.2)
        
        # 调整位置的方法：
        # 1. 调整 R 的初始 y 坐标（上面 r_copy_1.move_to([8.5, -3.8, 0]) 中的 -3.8）
        # 2. 或使用 shift 整体移动 R_group
        # 3. 或调整 brace_down 的 buff 参数
        
        # 动画显示下方的 =s× 大括号
        self.play(
            Write(s_times_label_down),
            Create(brace_down),
            run_time=1.5
        )

        self.wait(2)

        # 9. FadeOut 上下两侧的 =s×大括号（不含大括号右侧的公式/R组）
        self.play(
            FadeOut(s_times_label),
            FadeOut(brace),
            FadeOut(s_times_label_down),
            FadeOut(brace_down),
            run_time=1.0
        )

        # 10. FadeOut 四分之一圆（圆弧、下方半径、填充面积）、下方白边框，以及y轴
        self.play(
            FadeOut(quarter_circle_group),
            FadeOut(bounding_square),
            FadeOut(y_axis),
            run_time=1.0
        )

        self.wait(1)

        # 11. FadeOut x轴
        x_axis = grid.get_x_axis()
        self.play(FadeOut(x_axis), run_time=0.8)

        self.wait(0.5)

        # 12. 手动排版：把各项移动到分式的合适位置
        cx = 5.5
        frac_center_y = 5.0
        gap = 0.3   # 相邻元素边缘间距（调这一个参数控制分子项与+号、···与+号的间隔）

        # 用 next_to(buff=gap) 链构建布局参考，自动计算各项真实 x 坐标
        # 顺序：f1 + f2 + f3 + ··· + f_final（共4个+号）
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
        num_ref.move_to([cx, 0, 0])  # 先水平居中，y 后单独处理

        # 提取各项 x 坐标
        x_f1 = _nf1.get_center()[0]
        x_p1 = _np1.get_center()[0]
        x_f2 = _nf2.get_center()[0]
        x_p2 = _np2.get_center()[0]
        x_f3 = _nf3.get_center()[0]
        x_p3 = _np3.get_center()[0]
        x_dt = _ndt.get_center()[0]
        x_p4 = _np4.get_center()[0]
        x_ff = _nff.get_center()[0]

        # 分子/分母行 y：以边缘距分数线 0.24 格计算真实中心 y
        _ref_f = formula_1.copy()
        _ref_f.next_to([cx, frac_center_y, 0], UP, buff=0.24)
        num_y = _ref_f.get_center()[1]
        _ref_r = MathTex("R")
        _ref_r.next_to([cx, frac_center_y, 0], DOWN, buff=0.24)
        den_y = _ref_r.get_center()[1]

        # \vdots → \cdots，放置到正确终点位置
        h_dots_num = MathTex(r"\cdots").move_to([x_dt, num_y, 0])
        h_dots_den = MathTex(r"\cdots").move_to([x_dt, den_y, 0])

        # 所有元素一步到位；n→∞ 移到分数线左侧 [-5.0, frac_center_y, 0]
        self.play(
            formula_1.animate.move_to([x_f1, num_y, 0]),
            formula_2.animate.move_to([x_f2, num_y, 0]),
            formula_3.animate.move_to([x_f3, num_y, 0]),
            FadeOut(dots),
            FadeIn(h_dots_num),
            formula_final.animate.move_to([x_ff, num_y, 0]),
            R_copies[0].animate.move_to([x_f1, den_y, 0]),
            R_copies[1].animate.move_to([x_f2, den_y, 0]),
            R_copies[2].animate.move_to([x_f3, den_y, 0]),
            FadeOut(v_dots),
            FadeIn(h_dots_den),
            R_copies[3].animate.move_to([x_ff, den_y, 0]),
            n_label.animate.move_to([-5.0, frac_center_y, 0]),
            run_time=1.5
        )

        self.wait(0.3)

        # 13. 添加 + 号（分子和分母各4个，含 ··· 后的 +）
        plus_num_1 = MathTex("+").move_to([x_p1, num_y, 0])
        plus_num_2 = MathTex("+").move_to([x_p2, num_y, 0])
        plus_num_3 = MathTex("+").move_to([x_p3, num_y, 0])
        plus_num_4 = MathTex("+").move_to([x_p4, num_y, 0])
        plus_den_1 = MathTex("+").move_to([x_p1, den_y, 0])
        plus_den_2 = MathTex("+").move_to([x_p2, den_y, 0])
        plus_den_3 = MathTex("+").move_to([x_p3, den_y, 0])
        plus_den_4 = MathTex("+").move_to([x_p4, den_y, 0])

        self.play(
            FadeIn(plus_num_1), FadeIn(plus_num_2), FadeIn(plus_num_3), FadeIn(plus_num_4),
            FadeIn(plus_den_1), FadeIn(plus_den_2), FadeIn(plus_den_3), FadeIn(plus_den_4),
            run_time=0.8
        )

        self.wait(0.3)

        # 14. 添加分数线（根据实际分式宽度自动确定长度）
        frac_left  = _nf1.get_left()[0]  - 0.2
        frac_right = _nff.get_right()[0] + 0.2
        frac_line = Line(
            [frac_left,  frac_center_y, 0],
            [frac_right, frac_center_y, 0],
            color=WHITE, stroke_width=3
        )
        self.play(Create(frac_line), run_time=0.8)

        self.wait(2)
