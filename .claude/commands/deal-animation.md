# 发牌式动画 (Deal Animation)

用于实现"从源元素 X 飞出，逐一填入目标序列 Y"的丝滑发牌效果。

## 调用方式

用户说：**"用发牌式动画实现从 [源元素X] 飞出组成 [目标序列Y]"**

## 标准模板

```python
# ── 1. 源对象隔离 ──────────────────────────────────────────────────────────
# 将"发牌源"拆成独立字符串参数，通过索引访问
source_tex = MathTex(r"源内容", r"其余内容")   # [0] = 发牌源，[1] = 遮罩部分
# 若整项都是源，则直接 source_tex = MathTex(r"源内容")

# ── 2. 隐藏 emitter（核心：让牌从源位置"凭空"飞出）─────────────────────
emitter = source_tex[0].copy()
emitter.move_to(source_tex[0].get_center())
emitter.set_opacity(0)
self.add(emitter)

# ── 3. 目标阵列（用源的 copy 定位，保持字体/大小一致）──────────────────
targets = [source_tex[0].copy().move_to([x_i, den_y, 0]) for x_i in target_x_list]

# ── 4. 构建动画列表 ────────────────────────────────────────────────────────
deal_anims = [TransformFromCopy(emitter, t) for t in targets]

# ── 5. 错位播放（推荐参数）────────────────────────────────────────────────
self.play(
    LaggedStart(*deal_anims, lag_ratio=0.15),
    Create(frac_line),          # 可选：同帧出现的配套元素
    FadeIn(VGroup(...)),        # 可选：加号、省略号等
    run_time=1.5
)
```

## 关键参数（实测最佳）

| 参数 | 值 | 说明 |
|------|-----|------|
| `lag_ratio` | **0.15** | 相邻牌错开时间比例；0.1~0.2 均可，0.15 节奏感最好 |
| `run_time` | **1.5** | 整体时长（秒）；牌数多时可适当加长 |
| emitter opacity | **0** | 必须为 0；让每张牌"淡出"而非"复制" |

## 为什么用隐藏 emitter 而不直接用源对象

| 方式 | 效果 |
|------|------|
| `TransformFromCopy(visible_source, t)` | 牌从可见源复制，起点 opacity=1，视觉上像"克隆" |
| `TransformFromCopy(hidden_emitter, t)` | 牌从源位置淡出飞入，起点 opacity=0，视觉上像"凭空发牌" ✓ |

## 与"暴露源"配合的完整流程

```python
# 若第一项原本是 "R^2-(0s)^2"，需先淡出后缀暴露源再发牌：
self.play(FadeOut(source_tex[1]), run_time=0.6)   # 隐藏 -(0s)^2
self.wait(0.3)
# ... 执行上方发牌模板 ...
self.play(FadeIn(source_tex[1]), run_time=0.6)    # 还原
```
