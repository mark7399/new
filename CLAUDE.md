# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Rendering

```bash
# Render a single scene (low quality for preview)
manim -ql grid_scene_split.py Scene1_Intro

# Render a single scene (high quality)
manim -qh grid_scene_split.py Scene7_Ratio

# Concatenate rendered scenes into final video
ffmpeg -f concat -safe 0 -i concat_list.txt -c copy output.mp4
```

Scene names: `Scene1_Intro`, `Scene2_N2`, `Scene3_N3`, `Scene4_N4`, `Scene5_N_General`, `Scene6_N_Infinity`, `Scene7_Ratio`

## Architecture

This is a Manim animation project visualizing the Wallis product and geometric rectangle approximation for circle quadrature. The main file is `grid_scene_split.py` (~980 lines).

**Seven independent `MovingCameraScene` subclasses**, each representing one segment of the animation:

| Scene | Content |
|-------|---------|
| `Scene1_Intro` | Circle display, grid fade-in, camera pan to first quadrant |
| `Scene2_N2` | n=2 rectangle approximation under the curve |
| `Scene3_N3` | n=3 rectangle approximation |
| `Scene4_N4` | n=4 rectangle approximation |
| `Scene5_N_General` | Smooth progression n=4→5→6→16→32 via ValueTracker |
| `Scene6_N_Infinity` | n→∞ with integral fill animation |
| `Scene7_Ratio` | Quarter-circle to bounding square ratio display |

**Critical pattern — scene boundary reconstruction**: Each scene must call `self.add()` to reconstruct the *cleaned-up* final state of the previous scene (labels/annotations added mid-scene may be omitted if they were conceptually transient). There are no shared mobjects between scene instances; the state must be rebuilt identically in position, scale, and style.

**Key shared module-level constants**: `BG_COLOR = "#16161d"`, `RADIUS = 5`, `ORIGIN_POINT = [0,0,0]`

**`create_n_rects_group(n)`**: Defined locally inside Scene5 and Scene6 (not a module-level function). Each rectangle is represented as two lines (vertical + horizontal edge), not a filled `Rectangle`. Use this pattern when adding new rect-based scenes.

**ValueTracker + `always_redraw` pattern**: Used in Scene2–Scene6 for angle-driven animation. After each phase, call `clear_updaters()` on dynamic lines before starting the next phase. Forgetting this causes lines to continue updating during unrelated animations.

**Camera position**: All scenes (Scene2–Scene7) use `self.camera.frame.move_to([4.5, 2.5, 0])` as the starting position, matching Scene1's final pan target.
