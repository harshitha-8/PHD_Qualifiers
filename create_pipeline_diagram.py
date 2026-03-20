"""
CV --> LLM Pipeline Architecture Diagram
NeurIPS-style, Tahoma font, pixel-perfect arrow placement.
Every arrow starts/ends exactly at box edges. Text fits inside all shapes.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

plt.rcParams.update({
    "font.family":      "sans-serif",
    "font.sans-serif":  ["Tahoma", "DejaVu Sans", "Arial"],
    "font.size":        8,
    "text.usetex":      False,
    "figure.dpi":       300,
    "savefig.dpi":      300,
    "savefig.bbox":     "tight",
    "savefig.pad_inches": 0.05,
})

# Colours
COL_CV      = "#4C72B0"
COL_DECIDE  = "#E07B39"
COL_PROMPT  = "#55A868"
COL_OLLAMA  = "#8172B2"
COL_MODEL   = "#C44E52"
COL_OUTPUT  = "#937860"
COL_LLAMA   = "#DA8BC3"
EDGE_COL    = "#444444"
BG_COL      = "#FFFFFF"
LABEL_COL   = "#666666"


def create_diagram(save_path, fmt="png"):
    fig, ax = plt.subplots(figsize=(7.0, 9.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12.5)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor(BG_COL)
    ax.set_facecolor(BG_COL)

    # ── draw_box: returns (x, y, w, h) so arrows know exact edges ─────
    def draw_box(x, y, w, h, label, sublabel=None, color=COL_CV,
                 fontsize=8, fontweight="bold", sublabel_size=6.5,
                 linewidth=1.2, alpha=0.12, highlight=False):
        fc = matplotlib.colors.to_rgba(color, alpha)
        lw = linewidth
        if highlight:
            lw = 2.0
            fc = matplotlib.colors.to_rgba(color, 0.25)
        box = FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.12",
            facecolor=fc, edgecolor=color,
            linewidth=lw, zorder=3)
        ax.add_patch(box)
        ty = y + (0.13 if sublabel else 0)
        ax.text(x, ty, label, ha="center", va="center",
                fontsize=fontsize, fontweight=fontweight,
                color="#1a1a1a", zorder=4)
        if sublabel:
            ax.text(x, y - 0.24, sublabel, ha="center", va="center",
                    fontsize=sublabel_size, color=LABEL_COL, zorder=4,
                    fontstyle="italic")
        return {"cx": x, "cy": y, "w": w, "h": h,
                "top": y + h / 2, "bot": y - h / 2,
                "left": x - w / 2, "right": x + w / 2}

    # ── draw_diamond: returns bounds ──────────────────────────────────
    def draw_diamond(x, y, sx, sy, label, color=COL_DECIDE, fontsize=6):
        diamond = plt.Polygon(
            [(x, y + sy), (x + sx, y), (x, y - sy), (x - sx, y)],
            closed=True,
            facecolor=matplotlib.colors.to_rgba(color, 0.15),
            edgecolor=color, linewidth=1.2, zorder=3)
        ax.add_patch(diamond)
        ax.text(x, y, label, ha="center", va="center",
                fontsize=fontsize, fontweight="bold",
                color="#1a1a1a", zorder=4, linespacing=1.2)
        return {"cx": x, "cy": y, "top": y + sy, "bot": y - sy,
                "left": x - sx, "right": x + sx}

    # ── draw_arrow: consistent style everywhere ───────────────────────
    def draw_arrow(x1, y1, x2, y2, label=None, color=EDGE_COL,
                   lw=1.0, dashed=False, label_offset=(0, 0),
                   label_fontsize=6.5, connectionstyle="arc3,rad=0"):
        arr = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle="-|>", color=color, linewidth=lw,
            linestyle="--" if dashed else "-",
            connectionstyle=connectionstyle,
            mutation_scale=10, zorder=2,
            shrinkA=0, shrinkB=0)
        ax.add_patch(arr)
        if label:
            mx = (x1 + x2) / 2 + label_offset[0]
            my = (y1 + y2) / 2 + label_offset[1]
            ax.text(mx, my, label, ha="center", va="center",
                    fontsize=label_fontsize, color=LABEL_COL,
                    fontstyle="italic", zorder=5,
                    bbox=dict(facecolor="white", edgecolor="none",
                              pad=1.0, alpha=0.9))

    # ==================================================================
    #  TITLE
    # ==================================================================
    ax.text(5.0, 12.2, "CV  -->  LLM Pipeline Architecture",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color="#1a1a1a")
    ax.text(5.0, 11.85,
            "From UAV Orthomosaics to On-Device Agricultural Advisory",
            ha="center", va="center", fontsize=7.5, color=LABEL_COL,
            fontstyle="italic")

    # ==================================================================
    #  (1) CV PIPELINE
    # ==================================================================
    ax.text(0.3, 11.3, "(1) Computer Vision Pipeline",
            ha="left", va="center", fontsize=8.5, fontweight="bold",
            color=COL_CV, fontstyle="italic")

    cv_y = 10.65
    # 5 boxes, evenly spaced with generous gaps for arrows
    cx_list = [1.0, 2.85, 4.7, 6.55, 8.4]
    bw = 1.50   # box width
    bh = 1.00   # box height

    cv_data = [
        ("UAV\nOrthomosaic",       "100 m alt, 2.5 cm GSD\n80% overlap"),
        ("RGB\nPreprocessing",     "Resize 512x512 tiles\n64 px overlap"),
        ("HSV\nTransform",         "H in [330-360]\nu [0-20], S>0.4, V>0.3"),
        ("DBSCAN\nClustering",    "eps=16 px (~37.5 cm)\nMinPts=8"),
        ("Morphological\nRefinement", "5x5 elliptical kernel\nArea in [200-8000] px"),
    ]

    cv_boxes = []
    for i, (lbl, sub) in enumerate(cv_data):
        b = draw_box(cx_list[i], cv_y, bw, bh, lbl, sub,
                     color=COL_CV, fontsize=7, sublabel_size=5.3)
        cv_boxes.append(b)

    # Arrows between CV boxes: right-edge of box i --> left-edge of box i+1
    for i in range(len(cv_boxes) - 1):
        draw_arrow(cv_boxes[i]["right"], cv_y,
                   cv_boxes[i + 1]["left"], cv_y)

    # ==================================================================
    #  Bloom Detection
    # ==================================================================
    bloom = draw_box(5.0, 9.1, 2.0, 0.75, "Bloom Detection",
                     "N blooms, centroids\nspatial heatmap",
                     color=COL_CV, fontsize=7.5, sublabel_size=5.3)

    # Arrow: bottom of last CV box --> down, then left to top of Bloom
    # First go straight down from Morphological Refinement
    morph = cv_boxes[-1]
    mid_y = (morph["bot"] + bloom["top"]) / 2

    # Vertical segment down from Morphological Refinement
    draw_arrow(morph["cx"], morph["bot"], morph["cx"], mid_y)
    # Horizontal + down to Bloom Detection top
    draw_arrow(morph["cx"], mid_y, bloom["right"], bloom["top"],
               connectionstyle="arc3,rad=-0.15",
               label="structured output",
               label_offset=(0.15, 0.22))

    # ==================================================================
    #  (2) DECISION & PROMPT ENGINEERING
    # ==================================================================
    ax.text(0.3, 8.35, "(2) Decision and Prompt Engineering",
            ha="left", va="center", fontsize=8.5, fontweight="bold",
            color=COL_DECIDE, fontstyle="italic")

    # Decision diamond — make it large enough for text
    dec = draw_diamond(5.0, 7.65, 0.7, 0.5,
                       "N >= 10-15\nblooms?",
                       color=COL_DECIDE, fontsize=6.5)

    # Arrow: bloom bottom --> diamond top
    draw_arrow(bloom["cx"], bloom["bot"], dec["cx"], dec["top"],
               label="bloom count", label_offset=(0.7, 0.0))

    # NO branch: diamond left edge --> text
    draw_arrow(dec["left"], dec["cy"], dec["left"] - 0.7, dec["cy"],
               color="#bbbbbb", dashed=True)
    ax.text(dec["left"] - 1.45, dec["cy"], "NO --> Skip tile",
            ha="center", va="center", fontsize=6.5,
            color="#999999", fontstyle="italic")

    # YES branch: diamond bottom --> Prompt Engineering top
    prompt = draw_box(5.0, 6.25, 2.8, 0.72,
                      "Structured Prompt Engineering",
                      "bloom count, density, heatmap\n"
                      "growth stage --> advisory request",
                      color=COL_PROMPT, fontsize=7.5, sublabel_size=5.3)

    # Enough gap between diamond bottom and prompt top for label
    draw_arrow(dec["cx"], dec["bot"], prompt["cx"], prompt["top"],
               label="YES --> template",
               label_offset=(0.85, 0.0))

    # ==================================================================
    #  (3) LLM INFERENCE
    # ==================================================================
    ax.text(0.3, 5.5, "(3) LLM Inference (Ollama)",
            ha="left", va="center", fontsize=8.5, fontweight="bold",
            color=COL_OLLAMA, fontstyle="italic")

    ollama = draw_box(5.0, 4.85, 2.6, 0.72, "Ollama Server",
                      "127.0.0.1:11434, local\n"
                      "zero cloud, 90 s timeout, triple-retry",
                      color=COL_OLLAMA, fontsize=7.5, sublabel_size=5.3)

    # Arrow: prompt bottom --> ollama top
    draw_arrow(prompt["cx"], prompt["bot"], ollama["cx"], ollama["top"],
               label="structured prompt", label_offset=(0.95, 0.0))

    # Three LLM model boxes
    model_y = 3.55
    model_data = [
        ("Mistral 7B",   "1,127 ms, 4.4 GB\nReal-time advisory",
         2.3, COL_MODEL, False),
        ("Gemma3",        "8,882 ms, 3.3 GB\nEdge deployment",
         5.0, COL_MODEL, False),
        ("Llama3.1 8B",   "1,294 ms, 4.9 GB\nBatch analytics",
         7.7, COL_LLAMA, True),
    ]

    models = []
    for lbl, sub, mx, col, hl in model_data:
        m = draw_box(mx, model_y, 2.0, 0.88, lbl, sub, color=col,
                     fontsize=7.5, sublabel_size=5.3, highlight=hl)
        models.append(m)

    # Arrows from Ollama bottom to each model top
    for m in models:
        rad = 0.0
        if m["cx"] < ollama["cx"]:
            rad = -0.2
        elif m["cx"] > ollama["cx"]:
            rad = 0.2
        draw_arrow(ollama["cx"] + (m["cx"] - ollama["cx"]) * 0.35,
                   ollama["bot"],
                   m["cx"], m["top"],
                   connectionstyle=f"arc3,rad={rad}")

    # ==================================================================
    #  (4) EVALUATION PIPELINE
    # ==================================================================
    ax.text(0.3, 2.65, "(4) Evaluation Pipeline",
            ha="left", va="center", fontsize=8.5, fontweight="bold",
            color=COL_OUTPUT, fontstyle="italic")

    out = draw_box(5.0, 1.85, 3.8, 0.85,
                   "Evaluation Output and Performance Metrics",
                   "harvest timing, spray schedule, yield estimate\n"
                   "7-dim metrics (latency / memory / quality / throughput)",
                   color=COL_OUTPUT, fontsize=7.5, sublabel_size=5.3)

    # Arrows from each model bottom to output top
    for m in models:
        rad = 0.0
        if m["cx"] < out["cx"]:
            rad = -0.15
        elif m["cx"] > out["cx"]:
            rad = 0.15
        draw_arrow(m["cx"], m["bot"],
                   out["cx"] + (m["cx"] - out["cx"]) * 0.25, out["top"],
                   connectionstyle=f"arc3,rad={rad}")

    # Caption
    ax.text(5.0, 0.75,
            "Fig. 1.  End-to-end CV to LLM pipeline: UAV orthomosaics are "
            "processed through classical\ncomputer-vision stages to detect "
            "cotton blooms, then structured prompts drive on-device\nLLM "
            "inference via Ollama (Mistral / Gemma3 / Llama 3.1) to produce "
            "real-time agricultural advisories.",
            ha="center", va="center", fontsize=6, color=LABEL_COL,
            fontstyle="italic", linespacing=1.4)

    fig.savefig(save_path, facecolor=BG_COL, edgecolor="none", format=fmt)
    plt.close(fig)
    print(f"Saved: {save_path}")


if __name__ == "__main__":
    d = os.path.dirname(os.path.abspath(__file__))
    create_diagram(os.path.join(d, "cv_llm_pipeline_architecture.png"), "png")
    create_diagram(os.path.join(d, "cv_llm_pipeline_architecture.pdf"), "pdf")
