from manim import *
import numpy as np

# ═══════════════════════════════════════════════════════════════════════════════
#  SPLIT of ExtendedFractionAnimation into 9 independent, seamless scenes.
#
#  Render all scenes in order and concatenate the videos to reproduce the
#  original animation exactly:
#
#    manim -pqh split_scenes.py Scene01_FractionIntro
#    manim -pqh split_scenes.py Scene02_BarChartExponents
#    ...
#    manim -pqh split_scenes.py Scene09_SqrtAndFinalTable
#
#  Then concatenate:
#    ffmpeg -f concat -safe 0 -i list.txt -c copy final.mp4
#
#  Each scene silently reconstructs the ending visual state of the previous
#  scene (using self.add, not self.play) and then runs its own animations.
# ═══════════════════════════════════════════════════════════════════════════════

BG_COLOR = "#16161d"

# Layout constants
LEFT_ALIGN_X = -4.0
START_Y      = 1.0
LINE_SPACING = 1.5

# Exponent scale factor
EXP_SCALE = 0.6

# Graph constants (Scene 7+)
GRAPH_CENTER    = np.array([2.5, 0, 0])
BLUE_BOX_WIDTH  = 3.0
BLUE_BOX_HEIGHT = 3.0


# ───────────── Shared helper functions ─────────────

def build_base_fraction():
    """Build the initial fraction layout and return all pieces."""
    numerator = MathTex(r"0 + 1 + 2 + 3 + \cdots + ", r"n")
    numerator[0].set_color(WHITE)
    numerator[1].set_color(BLUE)

    denominator = MathTex(r"n + n + n + n + \cdots + n")
    denom_ns = VGroup(*[denominator[i] for i in range(0, len(denominator), 2)])
    denom_others = VGroup(*[denominator[i] for i in range(1, len(denominator), 2)])
    denom_ns.set_color(BLUE)
    denom_others.set_color(WHITE)

    fraction_line = Line(LEFT, RIGHT)
    equals_sign   = MathTex("=")
    answer        = MathTex(r"\frac{1}{2}", color=YELLOW)

    numerator.move_to(UP * 0.8)
    fraction_line.match_width(numerator).scale(1.1)
    fraction_line.next_to(numerator, DOWN, buff=0.2)
    denominator.next_to(fraction_line, DOWN, buff=0.2)
    equals_sign.next_to(fraction_line, RIGHT, buff=0.4)
    answer.next_to(equals_sign, RIGHT, buff=0.2)

    full_group = VGroup(numerator, fraction_line, denominator, equals_sign, answer)
    full_group.move_to(ORIGIN)

    frac_group = VGroup(numerator, fraction_line, denominator)
    rect = SurroundingRectangle(frac_group, color=WHITE, stroke_width=2,
                                fill_opacity=0, buff=0.02)

    return (numerator, fraction_line, denominator, equals_sign, answer,
            rect, denom_ns, denom_others, full_group)


def _build_top_formula_at_scene3_end():
    """
    Rebuild the 'top formula group' as it looks at the END of Scene 3
    (numerator + exponents + fraction_line2 + denominator n^2 terms),
    BEFORE the scale(0.8).to_edge() that Scene 4 applies.
    Returns (top_formula_group, numerator, exps, fraction_line2).
    """
    (numerator, *_) = build_base_fraction()
    numerator.move_to(UP * 2.5)
    numerator.shift(UP * 0.6)

    exps = []
    for i in [0, 2, 4, 6]:
        e = MathTex("2", color=WHITE).scale(EXP_SCALE)
        e.move_to(numerator[0][i].get_corner(UR) + RIGHT * 0.1 + UP * 0.15)
        exps.append(e)
    e_n = MathTex("2", color=WHITE).scale(EXP_SCALE)
    e_n.move_to(numerator[1].get_corner(UR) + RIGHT * 0.1 + UP * 0.15)
    exps.append(e_n)

    fraction_line2 = Line(LEFT, RIGHT)
    fraction_line2.match_width(numerator).scale(1.1)
    fraction_line2.next_to(numerator, DOWN, buff=0.2)

    dummy_denom = MathTex("n").next_to(fraction_line2, DOWN, buff=0.3)
    denom_y = dummy_denom.get_y()

    denom_terms = VGroup()
    for i in range(len(numerator[0])):
        if i in [0, 2, 4, 6]:
            tn = numerator[1].copy()
            tn.set_x(numerator[0][i].get_x()); tn.set_y(denom_y)
            t2 = exps[-1].copy()
            t2.move_to(tn.get_corner(UR) + RIGHT * 0.10 + UP * 0.15)
            denom_terms.add(tn, t2)
        else:
            ts = numerator[0][i].copy()
            ts.set_y(denom_y)
            denom_terms.add(ts)
    tn_f = numerator[1].copy()
    tn_f.set_x(numerator[1].get_x()); tn_f.set_y(denom_y)
    t2_f = exps[-1].copy()
    t2_f.move_to(tn_f.get_corner(UR) + RIGHT * 0.10 + UP * 0.15)
    denom_terms.add(tn_f, t2_f)

    top_formula_group = Group(numerator, *exps, fraction_line2, denom_terms)
    return top_formula_group, numerator, exps, fraction_line2


def create_graph_content(n, center=None):
    if center is None:
        center = GRAPH_CENTER
    box_w, box_h = BLUE_BOX_WIDTH, BLUE_BOX_HEIGHT
    origin = center + np.array([-box_w / 2, -box_h / 2, 0])
    rects = VGroup()
    dx = box_w / n
    for k in range(n + 1):
        h = box_h * (k / n) ** 2
        rect = Rectangle(width=dx, height=h if h > 1e-6 else 1e-6)
        rect.set_stroke(WHITE, 2).set_fill(opacity=0)
        rect.move_to(origin + np.array([k * dx + dx / 2, h / 2, 0]))
        rects.add(rect)
    return rects


def get_smooth_curve_group(center=None):
    if center is None:
        center = GRAPH_CENTER
    box_w, box_h = BLUE_BOX_WIDTH, BLUE_BOX_HEIGHT
    origin = center + np.array([-box_w / 2, -box_h / 2, 0])
    pts = [origin + np.array([t * box_w, (t ** 2) * box_h, 0]) for t in np.linspace(0, 1, 100)]
    curve = VMobject(); curve.set_points_smoothly(pts); curve.set_stroke(WHITE, 2)
    poly = [origin, origin + np.array([box_w, 0, 0])] + list(reversed(pts))
    area = Polygon(*poly); area.set_stroke(width=0); area.set_fill(WHITE, 0.2)
    lbl = MathTex("x^2").scale(0.8)
    lbl.move_to(origin + np.array([0.5 * box_w, 0.25 * box_h + 0.5, 0]))
    return VGroup(area, curve, lbl)


def create_row_complex(n, left_latex, denom_val):
    label = MathTex(f"n={n}").scale(0.8)
    eq = MathTex(left_latex, r"\frac{1}{3}", "+",
                 r"\frac{1}{" + str(denom_val) + "}").scale(0.8)
    eq[1].set_color(YELLOW)
    return VGroup(label, eq)


def create_graph_content_power(n, p, center):
    box_w, box_h = BLUE_BOX_WIDTH, BLUE_BOX_HEIGHT
    origin = center + np.array([-box_w / 2, -box_h / 2, 0])
    rects = VGroup()
    dx = box_w / n
    for k in range(n + 1):
        h = box_h * (k / n) ** p
        rect = Rectangle(width=dx, height=h if h > 1e-6 else 1e-6)
        rect.set_stroke(WHITE, 2).set_fill(opacity=0)
        rect.move_to(origin + np.array([k * dx + dx / 2, h / 2, 0]))
        rects.add(rect)
    return rects


def create_smooth_curve_power(p, center, show_label=False):
    box_w, box_h = BLUE_BOX_WIDTH, BLUE_BOX_HEIGHT
    origin = center + np.array([-box_w / 2, -box_h / 2, 0])
    pts = [origin + np.array([t * box_w, (t ** p) * box_h, 0]) for t in np.linspace(0, 1, 100)]
    curve = VMobject(); curve.set_points_smoothly(pts); curve.set_stroke(WHITE, 2)
    poly = [origin, origin + np.array([box_w, 0, 0])] + list(reversed(pts))
    area = Polygon(*poly); area.set_stroke(width=0); area.set_fill(WHITE, 0.2)
    grp = VGroup(area, curve)
    if show_label:
        lpos = origin + np.array([0.6 * box_w, (0.6 ** p) * box_h + 0.4, 0])
        lbl = MathTex(r"\sqrt{x}").scale(0.8).move_to(lpos)
        grp.add(lbl)
    return grp


def build_sqrt_row(n):
    label = MathTex(f"n={n}").scale(0.8)
    num_t = " + ".join([rf"\sqrt{{{k}}}" for k in range(n + 1)])
    den_t = " + ".join([rf"\sqrt{{{n}}}" for _ in range(n + 1)])
    eq = MathTex(rf"\frac{{{num_t}}}{{{den_t}}}").scale(0.8)
    return VGroup(label, eq)


def _build_table(table_center=None):
    if table_center is None:
        table_center = np.array([-1.5, 0, 0])
    h_scale = 0.7
    col_widths = [2.5, 0.8, 0.8, 0.8, 0.8, 1.2]
    row_height = 1.0

    t_idx = VGroup(Text("指数：", font_size=24), MathTex("m")).arrange(RIGHT, buff=0.1)
    t_1, t_2, t_3, t_4, t_m = MathTex("1"), MathTex("2"), MathTex("3"), MathTex("4"), MathTex("m")
    row1_els = [t_idx, t_1, t_2, t_3, t_4, t_m]

    t_coeff = VGroup(MathTex(r"n \to \infty"), Text("求积系数", font_size=24)).arrange(RIGHT, buff=0.1)
    t_v1 = MathTex(r"\frac{1}{2}", color=YELLOW)
    t_v2 = MathTex(r"\frac{1}{3}", color=YELLOW)
    t_v3 = MathTex(r"\frac{1}{4}", color=YELLOW)
    t_v4 = MathTex(r"\frac{1}{5}", color=YELLOW)
    t_vm = MathTex(r"\frac{1}{m+1}", color=YELLOW)
    row2_els = [t_coeff, t_v1, t_v2, t_v3, t_v4, t_vm]

    table_group = VGroup()
    total_width = sum(col_widths)
    top_line = Line(LEFT * total_width/2, RIGHT * total_width/2).set_stroke(WHITE, 3)
    mid_line = Line(LEFT * total_width/2, RIGHT * total_width/2).set_stroke(WHITE, 1)
    bot_line = Line(LEFT * total_width/2, RIGHT * total_width/2).set_stroke(WHITE, 3)
    top_line.move_to(table_center + UP * row_height)
    mid_line.move_to(table_center)
    bot_line.move_to(table_center + DOWN * row_height)
    table_group.add(VGroup(top_line, mid_line, bot_line))

    cx = table_center[0] - total_width / 2
    col_centers_x = []
    for w in col_widths:
        col_centers_x.append(cx + w / 2); cx += w
    r1y = table_center[1] + row_height / 2
    r2y = table_center[1] - row_height / 2
    for i, (e1, e2) in enumerate(zip(row1_els, row2_els)):
        e1.scale(h_scale).move_to(np.array([col_centers_x[i], r1y, 0]))
        e2.scale(h_scale).move_to(np.array([col_centers_x[i], r2y, 0]))
        table_group.add(e1, e2)

    return dict(table_group=table_group, top_line=top_line, mid_line=mid_line,
                bot_line=bot_line, col_widths=col_widths, col_centers_x=col_centers_x,
                row_height=row_height, total_width=total_width, table_center=table_center,
                row1_y=r1y, row2_y=r2y, t_idx=t_idx, t_coeff=t_coeff, h_scale=h_scale)


# ═══════════════════════════════════════════════════════════════════════════════
# Scene 1 – Fraction Introduction  (original lines 1-104)
# ═══════════════════════════════════════════════════════════════════════════════

class Scene01_FractionIntro(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        (numerator, fraction_line, denominator, equals_sign, answer,
         rect, denom_ns, denom_others, _) = build_base_fraction()

        self.play(Write(numerator[0]), run_time=1.5)
        self.wait(0.5)
        self.play(Write(numerator[1]), run_time=0.5)
        self.wait(0.5)

        anims = [TransformFromCopy(numerator[1], tn) for tn in denom_ns]
        self.play(*anims, Create(rect), run_time=2, lag_ratio=0.1)
        self.wait(0.5)
        self.play(Write(denom_others), run_time=1)
        self.wait(0.5)
        self.play(Create(fraction_line), Write(equals_sign), Write(answer), run_time=1.5)
        self.wait(3)


# ═══════════════════════════════════════════════════════════════════════════════
# Scene 2 – Bar Chart & Exponent Cycling  (original lines 106-197)
# ═══════════════════════════════════════════════════════════════════════════════

class Scene02_BarChartExponents(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # — reconstruct Scene 1 end state —
        (numerator, fraction_line, denominator, equals_sign, answer,
         rect, denom_ns, denom_others, _) = build_base_fraction()
        self.add(numerator, fraction_line, denominator, equals_sign, answer, rect)

        # — animations —
        num_bars = 8; bar_width = 0.5; unit_h = 0.5; baseline_y = -2
        start_x = -(num_bars * bar_width) / 2 + bar_width / 2
        bars, targets = [], []
        
        # Calculate initial max height for scaling reference
        # The last bar (i = num_bars - 1) has the maximum height
        initial_max_height = max((num_bars - 1) * unit_h, 0.001)

        for i in range(num_bars):
            x = start_x + i * bar_width
            h_t = max(i * unit_h, 0.001)
            r0 = Rectangle(width=bar_width, height=0.001, color=WHITE, stroke_width=2, fill_opacity=0)
            r0.move_to(np.array([x, 0, 0])); r0.align_to(np.array([0, baseline_y, 0]), DOWN)
            r1 = Rectangle(width=bar_width, height=h_t, color=WHITE, stroke_width=2, fill_opacity=0)
            r1.move_to(np.array([x, 0, 0])); r1.align_to(np.array([0, baseline_y, 0]), DOWN)
            bars.append(r0); targets.append(r1)
        self.add(*bars)
        self.play(
            LaggedStart(*[Transform(bars[i], targets[i], run_time=1.2) for i in range(num_bars)], lag_ratio=0.1),
            numerator.animate.move_to(UP * 2.5),
            FadeOut(rect), FadeOut(equals_sign), FadeOut(answer),
            FadeOut(fraction_line), FadeOut(denominator), run_time=2.5)
        self.wait(0.5)

        targets_sq = []
        for i in range(num_bars):
            # Normalized ratio from 0 to 1
            ratio = i / (num_bars - 1)
            # New height based on squared ratio, maintaining max height
            hs = max(initial_max_height * (ratio ** 2), 0.001)
            
            x = bars[i].get_center()[0]
            r2 = Rectangle(width=bar_width, height=hs, color=WHITE, stroke_width=2, fill_opacity=0)
            r2.move_to(np.array([x, 0, 0])); r2.align_to(np.array([0, baseline_y, 0]), DOWN)
            targets_sq.append(r2)
        exps = []
        for idx in [0, 2, 4, 6]:
            e = MathTex("2", color=WHITE).scale(EXP_SCALE)
            e.move_to(numerator[0][idx].get_corner(UR) + RIGHT * 0.1 + UP * 0.15)
            exps.append(e)
        e_n = MathTex("2", color=WHITE).scale(EXP_SCALE)
        e_n.move_to(numerator[1].get_corner(UR) + RIGHT * 0.1 + UP * 0.15)
        exps.append(e_n)
        self.play(*[Transform(bars[i], targets_sq[i]) for i in range(num_bars)],
                  *[Write(e) for e in exps], run_time=1.5)
        self.wait(0.5)

        for k in [3, 4, 5]:
            tgts = []
            for i in range(num_bars):
                ratio = i / (num_bars - 1)
                hk = max(initial_max_height * (ratio ** k), 0.001)
                
                x = bars[i].get_center()[0]
                rk = Rectangle(width=bar_width, height=hk, color=WHITE, stroke_width=2, fill_opacity=0)
                rk.move_to(np.array([x, 0, 0])); rk.align_to(np.array([0, baseline_y, 0]), DOWN)
                tgts.append(rk)
            enew = [MathTex(str(k), color=WHITE).scale(EXP_SCALE).move_to(e.get_center()) for e in exps]
            self.play(*[Transform(bars[i], tgts[i]) for i in range(num_bars)],
                      *[Transform(exps[j], enew[j]) for j in range(len(exps))], run_time=1.5)
            self.wait(0.5)

        self.play(FadeOut(VGroup(*bars)), numerator.animate.shift(UP * 0.6),
                  *[e.animate.shift(UP * 0.6) for e in exps], run_time=1.0)
        e2n = [MathTex("2", color=WHITE).scale(EXP_SCALE).move_to(e.get_center()) for e in exps]
        self.play(*[Transform(exps[i], e2n[i]) for i in range(len(exps))], run_time=0.8)


# ═══════════════════════════════════════════════════════════════════════════════
# Scene 3 – Denominator n^2 Construction  (original lines 199-293)
# ═══════════════════════════════════════════════════════════════════════════════

class Scene03_DenominatorSquared(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        (numerator, *_) = build_base_fraction()
        numerator.move_to(UP * 2.5); numerator.shift(UP * 0.6)
        self.add(numerator)

        exps = []
        for idx in [0, 2, 4, 6]:
            e = MathTex("2", color=WHITE).scale(EXP_SCALE)
            e.move_to(numerator[0][idx].get_corner(UR) + RIGHT * 0.1 + UP * 0.15)
            exps.append(e)
        e_n = MathTex("2", color=WHITE).scale(EXP_SCALE)
        e_n.move_to(numerator[1].get_corner(UR) + RIGHT * 0.1 + UP * 0.15)
        exps.append(e_n)
        self.add(*exps)
        exp2_new = exps

        fraction_line2 = Line(LEFT, RIGHT)
        fraction_line2.match_width(numerator).scale(1.1)
        fraction_line2.next_to(numerator, DOWN, buff=0.2)
        dummy = MathTex("n").next_to(fraction_line2, DOWN, buff=0.3)
        denom_y = dummy.get_y()

        em_n = numerator[1].copy(); em_2 = exp2_new[-1].copy()
        em_plus = numerator[0][1].copy(); em_dots = numerator[0][-2].copy()
        em_2.move_to(em_n.get_corner(UR) + RIGHT * 0.10 + UP * 0.15)
        em_plus.move_to(em_n.get_center() + RIGHT * 0.55)
        em_dots.move_to(em_n.get_center() + RIGHT * 1.10)
        emitter = VGroup(em_n, em_2, em_plus, em_dots)
        emitter.move_to(numerator[1].get_center()); emitter.set_opacity(0)
        self.add(emitter)

        term_groups = []
        for i in reversed(range(len(numerator[0]))):
            if i in [0, 2, 4, 6]:
                tn = numerator[1].copy(); tn.set_x(numerator[0][i].get_x()); tn.set_y(denom_y)
                t2 = exp2_new[-1].copy(); t2.move_to(tn.get_corner(UR) + RIGHT * 0.10 + UP * 0.15)
                term_groups.append(AnimationGroup(TransformFromCopy(em_n, tn), TransformFromCopy(em_2, t2), lag_ratio=0))
            else:
                ts = numerator[0][i].copy(); ts.set_y(denom_y)
                a_s = TransformFromCopy(em_dots, ts) if i == len(numerator[0]) - 2 else TransformFromCopy(em_plus, ts)
                if term_groups:
                    prev = term_groups.pop()
                    term_groups.append(AnimationGroup(prev, a_s, lag_ratio=0))
                else:
                    term_groups.append(AnimationGroup(a_s, lag_ratio=0))

        tn_f = numerator[1].copy(); tn_f.set_x(numerator[1].get_x()); tn_f.set_y(denom_y)
        t2_f = exp2_new[-1].copy(); t2_f.move_to(tn_f.get_corner(UR) + RIGHT * 0.10 + UP * 0.15)
        term_groups.append(AnimationGroup(TransformFromCopy(em_n, tn_f), TransformFromCopy(em_2, t2_f), lag_ratio=0))

        self.play(Create(fraction_line2), LaggedStart(*term_groups, lag_ratio=0.1), run_time=2.0)
        self.wait(2)


# ═══════════════════════════════════════════════════════════════════════════════
# Scene 4 – Concrete Examples n=1,2,3  (original lines 297-362)
# ═══════════════════════════════════════════════════════════════════════════════

class Scene04_ConcreteExamples(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        tfg, *_ = _build_top_formula_at_scene3_end()
        self.add(tfg)
        top_formula_group = Group(*self.mobjects)

        self.play(top_formula_group.animate.scale(0.8).to_edge(UP, buff=0.5), run_time=1.5)

        sy, ls, la = START_Y, LINE_SPACING, LEFT_ALIGN_X
        t1_label = MathTex("n=1").scale(0.8)
        t1_eq = MathTex(r"\frac{0^2+1^2}{1^2+1^2} = \frac{1}{2} = 0.5").scale(0.8)
        t2_label = MathTex("n=2").scale(0.8)
        t2_eq = MathTex(r"\frac{0+1+4}{4+4+4} = \frac{5}{12} = 0.41\dot{6}").scale(0.8)
        t3_label = MathTex("n=3").scale(0.8)
        t3_eq = MathTex(r"\frac{0+1+4+9}{9+9+9+9} = \frac{14}{36} = 0.3\dot{8}").scale(0.8)

        t1_label.move_to(np.array([la, sy, 0])); t1_eq.next_to(t1_label, RIGHT, buff=0.5)
        t2_label.move_to(np.array([la, sy-ls, 0])); t2_eq.next_to(t2_label, RIGHT, buff=0.5)
        t3_label.move_to(np.array([la, sy-2*ls, 0])); t3_eq.next_to(t3_label, RIGHT, buff=0.5)

        self.play(Write(t1_label), Write(t2_label), Write(t3_label), run_time=1.0)
        self.wait(0.5)
        self.play(Write(t1_eq), run_time=1.0); self.wait(0.5)
        self.play(Write(t2_eq), run_time=1.0); self.wait(0.5)
        self.play(Write(t3_eq), run_time=1.0); self.wait(2)


# ═══════════════════════════════════════════════════════════════════════════════
# Scene 5 – Scrolling List n=4..10  (original lines 364-512)
# ═══════════════════════════════════════════════════════════════════════════════

class Scene05_ScrollingList(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        sy, ls, la = START_Y, LINE_SPACING, LEFT_ALIGN_X

        tfg, *_ = _build_top_formula_at_scene3_end()
        tfg.scale(0.8).to_edge(UP, buff=0.5)
        self.add(tfg)

        t1_label = MathTex("n=1").scale(0.8)
        t1_eq = MathTex(r"\frac{0^2+1^2}{1^2+1^2} = \frac{1}{2} = 0.5").scale(0.8)
        t2_label = MathTex("n=2").scale(0.8)
        t2_eq = MathTex(r"\frac{0+1+4}{4+4+4} = \frac{5}{12} = 0.41\dot{6}").scale(0.8)
        t3_label = MathTex("n=3").scale(0.8)
        t3_eq = MathTex(r"\frac{0+1+4+9}{9+9+9+9} = \frac{14}{36} = 0.3\dot{8}").scale(0.8)
        t1_label.move_to(np.array([la, sy, 0])); t1_eq.next_to(t1_label, RIGHT, buff=0.5)
        t2_label.move_to(np.array([la, sy-ls, 0])); t2_eq.next_to(t2_label, RIGHT, buff=0.5)
        t3_label.move_to(np.array([la, sy-2*ls, 0])); t3_eq.next_to(t3_label, RIGHT, buff=0.5)
        row1 = VGroup(t1_label, t1_eq); row2 = VGroup(t2_label, t2_eq); row3 = VGroup(t3_label, t3_eq)
        self.add(row1, row2, row3)
        current_rows = [row1, row2, row3]

        def scroll_up(current, next_row, rt=1.5, rf=smooth):
            next_row[0].move_to(np.array([la, sy - 3*ls, 0]))
            next_row[1].next_to(next_row[0], RIGHT, buff=0.5)
            next_row.set_opacity(0); self.add(next_row)
            top = current.pop(0)
            self.play(top.animate.shift(UP*ls).set_opacity(0),
                      *[r.animate.shift(UP*ls) for r in current],
                      next_row.animate.shift(UP*ls).set_opacity(1),
                      run_time=rt, rate_func=rf)
            self.remove(top); current.append(next_row)

        r4 = VGroup(MathTex("n=4").scale(0.8), MathTex(r"\frac{0+1+4+9+16}{16+16+16+16+16} = \frac{30}{80} = 0.375").scale(0.8))
        r5 = VGroup(MathTex("n=5").scale(0.8), MathTex(r"\frac{0+1+4+9+16+25}{25+25+25+25+25+25} = \frac{55}{150} = 0.3\dot{6}").scale(0.8))
        r6 = VGroup(MathTex("n=6").scale(0.8), MathTex(r"\frac{0+1+4+9+16+25+36}{36+36+36+36+36+36+36} = \frac{91}{252} = 0.36\dot{1}").scale(0.7))
        for rr in [r4, r5, r6]:
            scroll_up(current_rows, rr, 1.5, smooth); self.wait(1.0)

        r7 = VGroup(MathTex("n=7").scale(0.8), MathTex(r"\frac{0+1+\cdots+49}{49+49+\cdots+49} = \frac{140}{392} \approx 0.357").scale(0.8))
        r8 = VGroup(MathTex("n=8").scale(0.8), MathTex(r"\frac{0+1+\cdots+64}{64+64+\cdots+64} = \frac{204}{576} \approx 0.354").scale(0.8))
        r9 = VGroup(MathTex("n=9").scale(0.8), MathTex(r"\frac{0+1+\cdots+81}{81+81+\cdots+81} = \frac{285}{810} \approx 0.352").scale(0.8))
        r10 = VGroup(MathTex("n=10").scale(0.8), MathTex(r"\frac{0+1+\cdots+100}{100+100+\cdots+100} = \frac{385}{1100} = 0.35").scale(0.8))
        for rr in [r7, r8, r9, r10]:
            scroll_up(current_rows, rr, 1.2, linear)
        self.wait(2)


# ═══════════════════════════════════════════════════════════════════════════════
# Scene 6 – Reverse Scroll to n=1 + Fraction Decomposition
#            (original lines 514-590)
# ═══════════════════════════════════════════════════════════════════════════════

class Scene06_ReverseAndDecompose(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        sy, ls, la = START_Y, LINE_SPACING, LEFT_ALIGN_X

        tfg, *_ = _build_top_formula_at_scene3_end()
        tfg.scale(0.8).to_edge(UP, buff=0.5)
        self.add(tfg)

        def mk(n, tex, sc=0.8):
            return VGroup(MathTex(f"n={n}").scale(sc), MathTex(tex).scale(sc))

        row1 = mk(1, r"\frac{0^2+1^2}{1^2+1^2} = \frac{1}{2} = 0.5")
        row2 = mk(2, r"\frac{0+1+4}{4+4+4} = \frac{5}{12} = 0.41\dot{6}")
        row3 = mk(3, r"\frac{0+1+4+9}{9+9+9+9} = \frac{14}{36} = 0.3\dot{8}")
        row4 = mk(4, r"\frac{0+1+4+9+16}{16+16+16+16+16} = \frac{30}{80} = 0.375")
        row5 = mk(5, r"\frac{0+1+4+9+16+25}{25+25+25+25+25+25} = \frac{55}{150} = 0.3\dot{6}")
        row6 = VGroup(MathTex("n=6").scale(0.8), MathTex(r"\frac{0+1+4+9+16+25+36}{36+36+36+36+36+36+36} = \frac{91}{252} = 0.36\dot{1}").scale(0.7))
        row7 = mk(7, r"\frac{0+1+\cdots+49}{49+49+\cdots+49} = \frac{140}{392} \approx 0.357")
        row8 = mk(8, r"\frac{0+1+\cdots+64}{64+64+\cdots+64} = \frac{204}{576} \approx 0.354")
        row9 = mk(9, r"\frac{0+1+\cdots+81}{81+81+\cdots+81} = \frac{285}{810} \approx 0.352")
        row10 = mk(10, r"\frac{0+1+\cdots+100}{100+100+\cdots+100} = \frac{385}{1100} = 0.35")

        for i, rw in enumerate([row8, row9, row10]):
            rw[0].move_to(np.array([la, sy - i*ls, 0]))
            rw[1].next_to(rw[0], RIGHT, buff=0.5)
        self.add(row8, row9, row10)
        current_rows = [row8, row9, row10]

        for prev_row in [row7, row6, row5, row4, row3, row2, row1]:
            prev_row[0].move_to(np.array([la, sy + ls, 0]))
            prev_row[1].next_to(prev_row[0], RIGHT, buff=0.5)
            prev_row.set_opacity(0); self.add(prev_row)
            bot = current_rows.pop()
            self.play(prev_row.animate.shift(DOWN*ls).set_opacity(1),
                      *[r.animate.shift(DOWN*ls) for r in current_rows],
                      bot.animate.shift(DOWN*ls).set_opacity(0),
                      run_time=0.3, rate_func=linear)
            self.remove(bot); current_rows.insert(0, prev_row)
        self.wait(2)

        t1_label, t1_eq = row1[0], row1[1]
        t2_label, t2_eq = row2[0], row2[1]
        t3_label, t3_eq = row3[0], row3[1]

        t1n = MathTex(r"\frac{0^2+1^2}{1^2+1^2} = \frac{1}{2} =", r"\frac{1}{3}", "+", r"\frac{1}{6}").scale(0.8)
        t1n[1].set_color(YELLOW); t1n.next_to(t1_label, RIGHT, buff=0.5)
        t2n = MathTex(r"\frac{0+1+4}{4+4+4} = \frac{5}{12} =", r"\frac{1}{3}", "+", r"\frac{1}{12}").scale(0.8)
        t2n[1].set_color(YELLOW); t2n.next_to(t2_label, RIGHT, buff=0.5)
        t3n = MathTex(r"\frac{0+1+4+9}{9+9+9+9} = \frac{14}{36} =", r"\frac{1}{3}", "+", r"\frac{1}{18}").scale(0.8)
        t3n[1].set_color(YELLOW); t3n.next_to(t3_label, RIGHT, buff=0.5)

        self.play(Transform(t1_eq, t1n), Transform(t2_eq, t2n), Transform(t3_eq, t3n), run_time=1.5)
        self.wait(1)


# ═══════════════════════════════════════════════════════════════════════════════
# Scene 7 – Scrolling with Graph -> Smooth Curve -> Infinity
#            (original lines 592-846)
# ═══════════════════════════════════════════════════════════════════════════════

class Scene07_GraphToInfinity(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        sy, ls, la = START_Y, LINE_SPACING, LEFT_ALIGN_X

        tfg, *_ = _build_top_formula_at_scene3_end()
        top_formula_group = tfg
        top_formula_group.scale(0.8).to_edge(UP, buff=0.5)
        self.add(top_formula_group)

        def mk_decomp(n, left, denom):
            lb = MathTex(f"n={n}").scale(0.8)
            eq = MathTex(left, r"\frac{1}{3}", "+", r"\frac{1}{" + str(denom) + "}").scale(0.8)
            eq[1].set_color(YELLOW)
            lb.move_to(np.array([la, sy - (n-1)*ls, 0]))
            eq.next_to(lb, RIGHT, buff=0.5)
            return VGroup(lb, eq)

        row1 = mk_decomp(1, r"\frac{0^2+1^2}{1^2+1^2} = \frac{1}{2} =", 6)
        row2 = mk_decomp(2, r"\frac{0+1+4}{4+4+4} = \frac{5}{12} =", 12)
        row3 = mk_decomp(3, r"\frac{0+1+4+9}{9+9+9+9} = \frac{14}{36} =", 18)
        self.add(row1, row2, row3)
        current_rows = [row1, row2, row3]

        r4 = create_row_complex(4, r"\frac{30}{80} =", 24)
        r5 = create_row_complex(5, r"\frac{55}{150} =", 30)
        r6 = create_row_complex(6, r"\frac{91}{252} =", 36)
        r7 = create_row_complex(7, r"\frac{140}{392} =", 42)
        r8 = create_row_complex(8, r"\frac{204}{576} =", 48)
        r9 = create_row_complex(9, r"\frac{285}{810} =", 54)
        r10 = create_row_complex(10, r"\frac{385}{1100} =", 60)
        rows_q = [r4, r5, r6, r7, r8, r9, r10]

        cur_graph = None; blue_box = None; limit_eq = None

        for nr in rows_q:
            nr[0].move_to(np.array([la, sy - 3*ls, 0]))
            nr[1].next_to(nr[0], RIGHT, buff=0.5)
            nr.set_opacity(0); self.add(nr)
            top = current_rows.pop(0)
            anims = [top.animate.shift(UP*ls).set_opacity(0),
                     *[r.animate.shift(UP*ls) for r in current_rows],
                     nr.animate.shift(UP*ls).set_opacity(1)]
            if nr is r6:
                limit_eq = MathTex(r"= \frac{1}{3} + \frac{1}{6n}")
                limit_eq[0][1:4].set_color(YELLOW)
                limit_eq[0][4].set_color(WHITE)
                limit_eq[0][5:].set_color(WHITE)
                sv = LEFT * 1.0
                anims.append(top_formula_group.animate.shift(sv))
                dummy = top_formula_group.copy().shift(sv)
                limit_eq.next_to(dummy, RIGHT, buff=0.2)
                anims.append(Write(limit_eq))
                blue_box = Rectangle(width=BLUE_BOX_WIDTH, height=BLUE_BOX_HEIGHT).move_to(GRAPH_CENTER)
                blue_box.set_stroke(BLUE, 2).set_fill(opacity=0)
                g5 = create_graph_content(5)
                anims.append(FadeIn(VGroup(blue_box, g5)))
                cur_graph = g5
            elif cur_graph is not None:
                tn = {r7: 6, r8: 7, r9: 8, r10: 9}.get(nr, 0)
                if tn > 0:
                    anims.append(Transform(cur_graph, create_graph_content(tn)))
            self.play(*anims, run_time=1.5, rate_func=linear)
            self.remove(top); current_rows.append(nr)

        accel = list(range(11, 21)) + [30, 50, 100]
        rt = 0.8
        for i, nv in enumerate(accel):
            rl = MathTex(f"n={nv}").scale(0.8); re = MathTex(r"\cdots").scale(0.8)
            nr = VGroup(rl, re)
            nr[0].move_to(np.array([la, sy - 3*ls, 0]))
            nr[1].next_to(nr[0], RIGHT, buff=0.5)
            nr.set_opacity(0); self.add(nr)
            rt = max(0.05, rt * 0.8) if i < 10 else 0.05
            top = current_rows.pop(0)
            anims = [top.animate.shift(UP*ls).set_opacity(0),
                     *[r.animate.shift(UP*ls) for r in current_rows],
                     nr.animate.shift(UP*ls).set_opacity(1),
                     Transform(cur_graph, create_graph_content(nv - 1))]
            self.play(*anims, run_time=rt, rate_func=linear)
            self.remove(top); current_rows.append(nr)

        inf_row = VGroup(MathTex(r"n \to \infty").scale(0.8), MathTex("").scale(0.8))
        inf_row[0].move_to(np.array([la, sy - 3*ls, 0])); inf_row.set_opacity(0); self.add(inf_row)
        top = current_rows.pop(0)
        self.play(top.animate.shift(UP*ls).set_opacity(0),
                  *[r.animate.shift(UP*ls) for r in current_rows],
                  inf_row.animate.shift(UP*ls).set_opacity(1),
                  Transform(cur_graph, get_smooth_curve_group()), run_time=1.5)
        self.remove(top); current_rows.append(inf_row)

        self.play(*[FadeOut(r) for r in current_rows[:-1]], run_time=1.0)
        current_rows = [current_rows[-1]]
        self.play(inf_row.animate.move_to(np.array([la, 0, 0])), run_time=1.0)
        self.wait(1)


# ═══════════════════════════════════════════════════════════════════════════════
# Scene 8 – Table & Dynamic Power Generalization  (original lines 848-1116)
# ═══════════════════════════════════════════════════════════════════════════════

class Scene08_TableAndDynamic(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        la = LEFT_ALIGN_X

        tfg, *_ = _build_top_formula_at_scene3_end()
        top_formula_group = tfg
        top_formula_group.scale(0.8).to_edge(UP, buff=0.5)
        top_formula_group.shift(LEFT * 1.0)
        self.add(top_formula_group)

        limit_eq = MathTex(r"= \frac{1}{3} + \frac{1}{6n}")
        limit_eq[0][1:4].set_color(YELLOW)
        limit_eq[0][4].set_color(WHITE)
        limit_eq[0][5:].set_color(WHITE)
        limit_eq.next_to(top_formula_group, RIGHT, buff=0.2)
        self.add(limit_eq)

        blue_box = Rectangle(width=BLUE_BOX_WIDTH, height=BLUE_BOX_HEIGHT).move_to(GRAPH_CENTER)
        blue_box.set_stroke(BLUE, 2).set_fill(opacity=0)
        cur_graph = get_smooth_curve_group()
        self.add(blue_box, cur_graph)

        inf_row = VGroup(MathTex(r"n \to \infty").scale(0.8), MathTex("").scale(0.8))
        inf_row.move_to(np.array([la, 0, 0]))
        self.add(inf_row)

        tg_pos = np.array([5.0, 0, 0]); sg = tg_pos - GRAPH_CENTER; sf = RIGHT * 1.0
        gg = VGroup(blue_box, cur_graph)
        self.play(FadeOut(limit_eq), top_formula_group.animate.shift(sf),
                  gg.animate.shift(sg), FadeOut(inf_row), run_time=1.5)

        tb = _build_table()
        tg = tb["table_group"]; ccx = tb["col_centers_x"]; cw = tb["col_widths"]
        tc = tb["table_center"]
        hb = Rectangle(width=cw[2], height=2*tb["row_height"], color=BLUE, stroke_width=3, fill_opacity=0)
        hb.move_to(np.array([ccx[2], tc[1], 0]))
        self.play(Create(tg), Create(hb))

        pt = ValueTracker(2); ngc = GRAPH_CENTER + sg

        def gf():
            p = int(round(pt.get_value())); ps = str(p)
            return MathTex(r"\frac{0^{%s}+1^{%s}+\cdots+n^{%s}}{n^{%s}+n^{%s}+\cdots+n^{%s}}" % (ps,ps,ps,ps,ps,ps)).scale(0.8).move_to(top_formula_group.get_center())
        df = always_redraw(gf)

        def gg_fn():
            p = pt.get_value(); bw, bh = BLUE_BOX_WIDTH, BLUE_BOX_HEIGHT
            o = ngc + np.array([-bw/2, -bh/2, 0])
            pts = [o + np.array([t*bw, (t**p)*bh, 0]) for t in np.linspace(0,1,100)]
            c = VMobject(); c.set_points_smoothly(pts); c.set_stroke(WHITE, 2)
            pp = [o, o+np.array([bw,0,0])] + list(reversed(pts))
            a = Polygon(*pp); a.set_stroke(width=0); a.set_fill(WHITE, 0.2)
            lx=0.6; ly=lx**p; lp=o+np.array([lx*bw, ly*bh+0.4, 0])
            lb = MathTex(f"x^{{{int(round(p))}}}").scale(0.8).move_to(lp)
            return VGroup(a, c, lb)
        dg = always_redraw(gg_fn)

        self.add(df, dg); self.remove(top_formula_group, cur_graph)
        self.wait(1)

        def mh(ci, pv, rt=1.0):
            self.play(hb.animate.move_to(np.array([ccx[ci], tc[1], 0])),
                      pt.animate.set_value(pv), run_time=rt)
            self.wait(0.5)
        mh(1, 1); mh(3, 3); mh(4, 4)
        self.play(hb.animate.move_to(np.array([ccx[5], tc[1], 0])).stretch_to_fit_width(cw[5]), run_time=1.0)

        df.clear_updaters(); dg.clear_updaters()
        mf = MathTex(r"\frac{0^m+1^m+\cdots+n^m}{n^m+n^m+\cdots+n^m}").scale(0.8).move_to(df.get_center())
        bw, bh = BLUE_BOX_WIDTH, BLUE_BOX_HEIGHT; o = ngc + np.array([-bw/2, -bh/2, 0])
        pv = 5
        cpts = [o+np.array([t*bw, (t**pv)*bh, 0]) for t in np.linspace(0,1,100)]
        cp = VMobject(); cp.set_points_smoothly(cpts); cp.set_stroke(WHITE, 2)
        pp = [o, o+np.array([bw,0,0])] + list(reversed(cpts))
        ar = Polygon(*pp); ar.set_stroke(width=0); ar.set_fill(WHITE, 0.2)
        lx=0.6; ly=lx**pv
        ml = MathTex("x^m").scale(0.8).move_to(o+np.array([lx*bw, ly*bh+0.4, 0]))
        mg = VGroup(ar, cp, ml)
        self.play(Transform(df, mf), Transform(dg, mg), run_time=1.0)
        self.wait(3)
        self.play(FadeOut(tg), FadeOut(hb), FadeOut(dg), FadeOut(blue_box), run_time=1.0)


# ═══════════════════════════════════════════════════════════════════════════════
# Scene 9 – Square Root Case (m=1/2) + Final Table Extension
#            (original lines 1118-1321)
# ═══════════════════════════════════════════════════════════════════════════════

class Scene09_SqrtAndFinalTable(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        sy, ls, la = START_Y, LINE_SPACING, LEFT_ALIGN_X

        # reconstruct: only dyn_formula (m version) visible
        tfg, *_ = _build_top_formula_at_scene3_end()
        tfg.scale(0.8).to_edge(UP, buff=0.5)
        # Scene 7 shifted LEFT*1, Scene 8 shifted RIGHT*1 -> net zero
        fpos = tfg.get_center()
        dyn_formula = MathTex(r"\frac{0^m+1^m+\cdots+n^m}{n^m+n^m+\cdots+n^m}").scale(0.8).move_to(fpos)
        self.add(dyn_formula)

        gc = np.array([4.4, 0, 0])
        sf = MathTex(r"\frac{\sqrt{0}+\sqrt{1}+\cdots+\sqrt{n}}{\sqrt{n}+\sqrt{n}+\cdots+\sqrt{n}}").scale(0.8).move_to(fpos)
        mhl = MathTex(r"m=\frac{1}{2}").scale(0.8).next_to(sf, LEFT, buff=0.3)
        self.play(Transform(dyn_formula, sf), Write(mhl), run_time=1.2)

        r1 = build_sqrt_row(1); r2 = build_sqrt_row(2); r3 = build_sqrt_row(3)
        r1[0].move_to(np.array([la, sy, 0])); r1[1].next_to(r1[0], RIGHT, buff=0.5)
        r2[0].move_to(np.array([la, sy-ls, 0])); r2[1].next_to(r2[0], RIGHT, buff=0.5)
        r3[0].move_to(np.array([la, sy-2*ls, 0])); r3[1].next_to(r3[0], RIGHT, buff=0.5)

        bb = Rectangle(width=BLUE_BOX_WIDTH, height=BLUE_BOX_HEIGHT).move_to(gc)
        bb.set_stroke(BLUE, 2).set_fill(opacity=0)
        cg = create_graph_content_power(2, 0.5, gc)
        self.play(Write(r1), Write(r2), Write(r3), FadeIn(bb), FadeIn(cg), run_time=1.2)

        rq = [build_sqrt_row(n) for n in range(4, 6)]
        re = VGroup(MathTex(r"\vdots").scale(0.8), MathTex("").scale(0.8))
        ri = VGroup(MathTex(r"n\to\infty").scale(0.8), MathTex("").scale(0.8))
        rq.extend([re, ri])
        cr = [r1, r2, r3]
        r2n = {r1: 1, r2: 2, r3: 3}
        for idx, r in enumerate(rq[:2], start=4):
            r2n[r] = idx
        scs = False

        for nr in rq:
            nr[0].move_to(np.array([la, sy - 3*ls, 0]))
            nr[1].next_to(nr[0], RIGHT, buff=0.5)
            nr.set_opacity(0); self.add(nr)
            tr = cr[1]; top = cr.pop(0)
            anims = [top.animate.shift(UP*ls).set_opacity(0),
                     *[r.animate.shift(UP*ls) for r in cr],
                     nr.animate.shift(UP*ls).set_opacity(1)]
            if not scs and tr in r2n:
                anims.append(Transform(cg, create_graph_content_power(r2n[tr], 0.5, gc)))
            self.play(*anims, run_time=1.2, rate_func=linear)
            self.remove(top); cr.append(nr)
            if nr is ri and not scs:
                art = 0.6
                for nv in [6, 8, 12, 20, 40]:
                    art = max(0.12, art * 0.7)
                    self.play(Transform(cg, create_graph_content_power(nv, 0.5, gc)), run_time=art, rate_func=linear)
                self.play(Transform(cg, create_smooth_curve_power(0.5, gc, True)), run_time=1.2, rate_func=linear)
                scs = True

        sd = -ri.get_y()
        self.play(*[r.animate.shift(UP*sd).set_opacity(1 if r is ri else 0) for r in cr],
                  run_time=1.0, rate_func=linear)
        self.play(FadeOut(ri), run_time=0.8)

        tb = _build_table()
        tg = tb["table_group"]; ccx = tb["col_centers_x"]; cw = tb["col_widths"]
        tc = tb["table_center"]; rh = tb["row_height"]; tw = tb["total_width"]
        r1y = tb["row1_y"]; r2y = tb["row2_y"]; hs = tb["h_scale"]
        tidx = tb["t_idx"]; tcf = tb["t_coeff"]
        tl = tb["top_line"]; ml = tb["mid_line"]; bl = tb["bot_line"]

        hb = Rectangle(width=cw[5], height=2*rh, color=BLUE, stroke_width=3, fill_opacity=0)
        hb.move_to(np.array([ccx[5], tc[1], 0]))
        self.play(FadeIn(tg), FadeIn(hb), run_time=1.0)

        ncw = 0.9; nccx = ccx[1] - cw[1]/2 - ncw/2
        rex = tc[0] + tw/2; ntw = tw + ncw; nle = rex - ntw
        ntl = Line(np.array([nle, tc[1]+rh, 0]), np.array([rex, tc[1]+rh, 0])).set_stroke(WHITE, 3)
        nml = Line(np.array([nle, tc[1], 0]), np.array([rex, tc[1], 0])).set_stroke(WHITE, 1)
        nbl = Line(np.array([nle, tc[1]-rh, 0]), np.array([rex, tc[1]-rh, 0])).set_stroke(WHITE, 3)
        nh = MathTex(r"\frac{1}{2}").scale(hs).move_to(np.array([nccx, r1y, 0]))
        nc = MathTex(r"\frac{2}{3}", color=YELLOW).scale(hs).move_to(np.array([nccx, r2y, 0]))

        self.play(Transform(tl, ntl), Transform(ml, nml), Transform(bl, nbl),
                  tidx.animate.shift(LEFT*ncw), tcf.animate.shift(LEFT*ncw),
                  hb.animate.move_to(np.array([nccx, tc[1], 0])).stretch_to_fit_width(ncw),
                  FadeIn(nh), FadeIn(nc), run_time=1.2)
        tg.add(nh, nc)
