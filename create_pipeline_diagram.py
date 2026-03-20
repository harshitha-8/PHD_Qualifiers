"""
CV --> LLM Pipeline Architecture Diagram
NeurIPS-style, Tahoma font, meticulous arrow and text placement.
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

# Arrow gap: how far the arrow tip stays from the box edge
GAP = 0.06


def create_diagram(save_path, fmt="png"):
    fig, ax = plt.subplots(figsize=(7.2, 9.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 13)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor(BG_COL)
    ax.set_facecolor(BG_COL)

    # ── Rounded box ───────────────────────────────────────────────────
    def box(x, y, w, h, label, sublabel=None, color=COL_CV,
            fontsize=8, sublabel_size=6.5, lw=1.2, alpha=0.12,
            highlight=False):
        fc = matplotlib.colors.to_rgba(color, alpha)
        if highlight:
            lw = 2.0
            fc = matplotlib.colors.to_rgba(color, 0.25)
        p = FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.12",
            facecolor=fc, edgecolor=color, linewidth=lw, zorder=3)
        ax.add_patch(p)
        ty = y + (0.14 if sublabel else 0)
        ax.text(x, ty, label, ha="center", va="center",
                fontsize=fontsize, fontweight="bold",
                color="#1a1a1a", zorder=4)
        if sublabel:
            ax.text(x, y - 0.25, sublabel, ha="center", va="center",
                    fontsize=sublabel_size, color=LABEL_COL, zorder=4,
                    fontstyle="italic")
        return dict(cx=x, cy=y, w=w, h=h,
                    t=y + h / 2, b=y - h / 2,
                    l=x - w / 2, r=x + w / 2)

    # ── Decision diamond ──────────────────────────────────────────────
    def diamond(x, y, sx, sy, label, color=COL_DECIDE, fontsize=6.5):
        d = plt.Polygon(
            [(x, y + sy), (x + sx, y), (x, y - sy), (x - sx, y)],
            closed=True,
            facecolor=matplotlib.colors.to_rgba(color, 0.15),
            edgecolor=color, linewidth=1.2, zorder=3)
        ax.add_patch(d)
        ax.text(x, y, label, ha="center", va="center",
                fontsize=fontsize, fontweight="bold",
                color="#1a1a1a", zorder=4, linespacing=1.15)
        return dict(cx=x, cy=y, t=y + sy, b=y - sy,
                    l=x - sx, r=x + sx)

    # ── Arrow ─────────────────────────────────────────────────────────
    def arrow(x1, y1, x2, y2, label=None, color=EDGE_COL,
              lw=1.0, dashed=False, lbl_off=(0, 0), lbl_fs=6.5,
              cs="arc3,rad=0"):
        a = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle="-|>", color=color, linewidth=lw,
            linestyle="--" if dashed else "-",
            connectionstyle=cs, mutation_scale=10,
            zorder=2, shrinkA=0, shrinkB=0)
        ax.add_patch(a)
        if label:
            mx = (x1 + x2) / 2 + lbl_off[0]
            my = (y1 + y2) / 2 + lbl_off[1]
            ax.text(mx, my, label, ha="center", va="center",
                    fontsize=lbl_fs, color=LABEL_COL,
                    fontstyle="italic", zorder=6,
                    bbox=dict(facecolor="white", edgecolor="none",
                              pad=1.2, alpha=0.95))

    # ==================================================================
    #  TITLE
    # ==================================================================
    ax.text(5.0, 12.7, "CV  -->  LLM Pipeline Architecture",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color="#1a1a1a")
    ax.text(5.0, 12.35,
            "From UAV Orthomosaics to On-Device Agricultural Advisory",
            ha="center", va="center", fontsize=7.5, color=LABEL_COL,
            fontstyle="italic")

    # ==================================================================
    #  (1) CV PIPELINE
    # ==================================================================
    ax.text(0.25, 11.75, "(1) Computer Vision Pipeline",
            ha="left", va="center", fontsize=8.5, fontweight="bold",
            color=COL_CV, fontstyle="italic")

    cv_y = 11.05
    # Positions with breathing room — 1.85 apart, box width 1.48
    positions = [1.0, 2.85, 4.70, 6.55, 8.40]
    bw, bh = 1.48, 1.02

    data = [
        ("UAV\nOrthomosaic",       "100 m alt, 2.5 cm GSD\n80% overlap"),
        ("RGB\nPreprocessing",     "Resize 512x512 tiles\n64 px overlap"),
        ("HSV\nTransform",         "H in [330-360]\nu [0-20], S>0.4, V>0.3"),
        ("DBSCAN\nClustering",     "eps=16 px (~37.5 cm)\nMinPts=8"),
        ("Morphological\nRefinement", "5x5 elliptical kernel\nArea in [200-8000] px"),
    ]

    boxes = []
    for i, (lbl, sub) in enumerate(data):
        b = box(positions[i], cv_y, bw, bh, lbl, sub,
                color=COL_CV, fontsize=7, sublabel_size=5.2)
        boxes.append(b)

    # Arrows: right edge + gap --> left edge - gap
    for i in range(4):
        arrow(boxes[i]["r"] + GAP, cv_y,
              boxes[i + 1]["l"] - GAP, cv_y)

    # ==================================================================
    #  BLOOM DETECTION
    # ==================================================================
    bl = box(5.0, 9.35, 2.1, 0.80, "Bloom Detection",
             "N blooms, centroids\nspatial heatmap",
             color=COL_CV, fontsize=7.5, sublabel_size=5.3)

    # Single clean arrow from Morphological Refinement bottom to Bloom top-right
    # Using a single curved arrow
    arrow(boxes[4]["cx"], boxes[4]["b"] - GAP,
          bl["r"] - 0.15, bl["t"] + GAP,
          cs="arc3,rad=-0.25",
          label="structured output", lbl_off=(-0.05, 0.0))

    # ==================================================================
    #  (2) DECISION & PROMPT
    # ==================================================================
    ax.text(0.25, 8.55, "(2) Decision and Prompt Engineering",
            ha="left", va="center", fontsize=8.5, fontweight="bold",
            color=COL_DECIDE, fontstyle="italic")

    dec = diamond(5.0, 7.85, 0.75, 0.55,
                  "N >= 10-15\nblooms?",
                  color=COL_DECIDE, fontsize=6.5)

    # Bloom bottom --> diamond top
    arrow(bl["cx"], bl["b"] - GAP,
          dec["cx"], dec["t"] + GAP,
          label="bloom count", lbl_off=(0.75, 0.0))

    # NO branch
    arrow(dec["l"] - GAP, dec["cy"],
          dec["l"] - 0.8, dec["cy"],
          color="#bbbbbb", dashed=True)
    ax.text(dec["l"] - 1.6, dec["cy"], "NO --> Skip tile",
            ha="center", va="center", fontsize=6.5,
            color="#999999", fontstyle="italic")

    # YES --> Structured Prompt Engineering
    pr = box(5.0, 6.30, 2.9, 0.78,
             "Structured Prompt Engineering",
             "bloom count, density, heatmap\n"
             "growth stage --> advisory request",
             color=COL_PROMPT, fontsize=7.5, sublabel_size=5.3)

    arrow(dec["cx"], dec["b"] - GAP,
          pr["cx"], pr["t"] + GAP,
          label="YES --> template", lbl_off=(0.9, 0.0))

    # ==================================================================
    #  (3) LLM INFERENCE
    # ==================================================================
    ax.text(0.25, 5.5, "(3) LLM Inference (Ollama)",
            ha="left", va="center", fontsize=8.5, fontweight="bold",
            color=COL_OLLAMA, fontstyle="italic")

    ol = box(5.0, 4.85, 2.7, 0.78, "Ollama Server",
             "127.0.0.1:11434, local\n"
             "zero cloud, 90 s timeout, triple-retry",
             color=COL_OLLAMA, fontsize=7.5, sublabel_size=5.3)

    arrow(pr["cx"], pr["b"] - GAP,
          ol["cx"], ol["t"] + GAP,
          label="structured prompt", lbl_off=(1.0, 0.0))

    # Models
    my_ = 3.45
    mdata = [
        ("Mistral 7B",  "1,127 ms, 4.4 GB\nReal-time advisory",
         2.2, COL_MODEL, False),
        ("Gemma3",       "8,882 ms, 3.3 GB\nEdge deployment",
         5.0, COL_MODEL, False),
        ("Llama3.1 8B",  "1,294 ms, 4.9 GB\nBatch analytics",
         7.8, COL_LLAMA, True),
    ]

    ml = []
    for lbl, sub, mx, col, hl in mdata:
        m = box(mx, my_, 2.05, 0.90, lbl, sub, color=col,
                fontsize=7.5, sublabel_size=5.3, highlight=hl)
        ml.append(m)

    # Ollama --> each model
    for m in ml:
        dx = m["cx"] - ol["cx"]
        rad = -0.22 if dx < -0.5 else (0.22 if dx > 0.5 else 0.0)
        start_x = ol["cx"] + dx * 0.35
        arrow(start_x, ol["b"] - GAP,
              m["cx"], m["t"] + GAP,
              cs=f"arc3,rad={rad}")

    # ==================================================================
    #  (4) EVALUATION PIPELINE
    # ==================================================================
    ax.text(0.25, 2.55, "(4) Evaluation Pipeline",
            ha="left", va="center", fontsize=8.5, fontweight="bold",
            color=COL_OUTPUT, fontstyle="italic")

    ev = box(5.0, 1.75, 3.9, 0.90,
             "Evaluation Output and Performance Metrics",
             "harvest timing, spray schedule, yield estimate\n"
             "7-dim metrics (latency / memory / quality / throughput)",
             color=COL_OUTPUT, fontsize=7.5, sublabel_size=5.3)

    for m in ml:
        dx = m["cx"] - ev["cx"]
        rad = -0.18 if dx < -0.5 else (0.18 if dx > 0.5 else 0.0)
        arrow(m["cx"], m["b"] - GAP,
              ev["cx"] + dx * 0.25, ev["t"] + GAP,
              cs=f"arc3,rad={rad}")

    # Caption
    ax.text(5.0, 0.60,
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
