"""
CV → LLM Pipeline Architecture Diagram
NeurIPS-style figure — Tahoma font, consistent arrows, clean layout.
Excludes TACC infrastructure.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

# ─── Style setup ───────────────────────────────────────────────────────
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

# ─── Colour palette (kept as-is per user preference) ──────────────────
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
    """Create the full pipeline diagram and save it."""
    fig, ax = plt.subplots(figsize=(7.0, 8.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor(BG_COL)
    ax.set_facecolor(BG_COL)

    # ─── Helper: rounded box ──────────────────────────────────────────
    def draw_box(x, y, w, h, label, sublabel=None, color=COL_CV,
                 fontsize=8, fontweight="bold",
                 sublabel_size=6.5, linewidth=1.2, alpha=0.12,
                 highlight=False):
        fc = matplotlib.colors.to_rgba(color, alpha)
        lw = linewidth
        if highlight:
            lw = 2.0
            fc = matplotlib.colors.to_rgba(color, 0.25)
        box = FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.15",
            facecolor=fc, edgecolor=color,
            linewidth=lw, zorder=3)
        ax.add_patch(box)
        ax.text(x, y + (0.12 if sublabel else 0), label,
                ha="center", va="center", fontsize=fontsize,
                fontweight=fontweight, color="#1a1a1a", zorder=4)
        if sublabel:
            ax.text(x, y - 0.22, sublabel,
                    ha="center", va="center", fontsize=sublabel_size,
                    color=LABEL_COL, zorder=4, fontstyle="italic")

    # ─── Helper: decision diamond ─────────────────────────────────────
    def draw_diamond(x, y, size, label, color=COL_DECIDE, fontsize=6.5):
        s = size
        diamond = plt.Polygon(
            [(x, y + s), (x + s * 1.3, y), (x, y - s), (x - s * 1.3, y)],
            closed=True,
            facecolor=matplotlib.colors.to_rgba(color, 0.15),
            edgecolor=color, linewidth=1.2, zorder=3)
        ax.add_patch(diamond)
        ax.text(x, y, label, ha="center", va="center", fontsize=fontsize,
                fontweight="bold", color="#1a1a1a", zorder=4)

    # ─── Helper: arrow (consistent style throughout) ──────────────────
    def draw_arrow(x1, y1, x2, y2, label=None, color=EDGE_COL,
                   lw=1.0, ls="-", label_offset=(0, 0.12),
                   label_fontsize=6, connectionstyle="arc3,rad=0",
                   dashed=False):
        linestyle = "--" if dashed else ls
        arr = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle="-|>", color=color, linewidth=lw,
            linestyle=linestyle, connectionstyle=connectionstyle,
            mutation_scale=10, zorder=2)
        ax.add_patch(arr)
        if label:
            mx = (x1 + x2) / 2 + label_offset[0]
            my = (y1 + y2) / 2 + label_offset[1]
            ax.text(mx, my, label, ha="center", va="center",
                    fontsize=label_fontsize, color=LABEL_COL,
                    fontstyle="italic", zorder=5,
                    bbox=dict(facecolor="white", edgecolor="none",
                              pad=0.5, alpha=0.85))

    # ═══════════════════════════════════════════════════════════════════
    # TITLE
    # ═══════════════════════════════════════════════════════════════════
    ax.text(5.0, 11.65, "CV  -->  LLM Pipeline Architecture",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color="#1a1a1a")
    ax.text(5.0, 11.30,
            "From UAV Orthomosaics to On-Device Agricultural Advisory",
            ha="center", va="center", fontsize=7.5, color=LABEL_COL,
            fontstyle="italic")

    # ═══════════════════════════════════════════════════════════════════
    # (1) COMPUTER VISION PIPELINE
    # ═══════════════════════════════════════════════════════════════════
    ax.text(0.3, 10.75, "(1) Computer Vision Pipeline",
            ha="left", va="center", fontsize=8.5, fontweight="bold",
            color=COL_CV, fontstyle="italic")

    cv_y = 10.0
    # Wider spacing: positions 0.7, 2.55, 4.4, 6.25, 8.1
    cv_positions = [0.9, 2.7, 4.5, 6.3, 8.1]
    box_w = 1.45
    cv_nodes = [
        ("UAV\nOrthomosaic",
         "100 m alt, 2.5 cm GSD\n80% overlap"),
        ("RGB\nPreprocessing",
         "Resize 512x512 tiles\n64 px overlap"),
        ("HSV\nTransform",
         "H in [330-360] u [0-20]\nS>0.4, V>0.3"),
        ("DBSCAN\nClustering",
         "eps=16 px (~37.5 cm)\nMinPts=8"),
        ("Morphological\nRefinement",
         "5x5 elliptical kernel\nArea in [200-8000] px"),
    ]

    for i, (label, sub) in enumerate(cv_nodes):
        draw_box(cv_positions[i], cv_y, box_w, 0.95, label, sub,
                 color=COL_CV, fontsize=7, sublabel_size=5.5)

    # Arrows between CV nodes — with proper gap
    for i in range(len(cv_nodes) - 1):
        x1 = cv_positions[i] + box_w / 2 + 0.05
        x2 = cv_positions[i + 1] - box_w / 2 - 0.05
        draw_arrow(x1, cv_y, x2, cv_y)

    # ─── Bloom Detection ──────────────────────────────────────────────
    bloom_x, bloom_y = 5.0, 8.55
    draw_box(bloom_x, bloom_y, 1.8, 0.7, "Bloom Detection",
             "N blooms, centroids\nspatial heatmap",
             color=COL_CV, fontsize=7.5, sublabel_size=5.5)

    # Arrow from last CV node down and across to Bloom Detection
    last_cv_x = cv_positions[-1]
    draw_arrow(last_cv_x, cv_y - 0.48, last_cv_x, 9.05)
    draw_arrow(last_cv_x, 9.05, bloom_x + 0.9, bloom_y + 0.1,
               connectionstyle="arc3,rad=-0.2",
               label="structured output", label_offset=(0.6, 0.18))

    # ═══════════════════════════════════════════════════════════════════
    # (2) DECISION & PROMPT ENGINEERING
    # ═══════════════════════════════════════════════════════════════════
    ax.text(0.3, 7.95, "(2) Decision and Prompt Engineering",
            ha="left", va="center", fontsize=8.5, fontweight="bold",
            color=COL_DECIDE, fontstyle="italic")

    dec_x, dec_y = 5.0, 7.25
    draw_diamond(dec_x, dec_y, 0.45, "N >= 10-15\nblooms?",
                 color=COL_DECIDE, fontsize=6)

    draw_arrow(bloom_x, bloom_y - 0.35, dec_x, dec_y + 0.45,
               label="bloom count", label_offset=(0.7, 0.0))

    # NO branch (dashed)
    ax.text(dec_x - 1.8, dec_y, "NO  -->  Skip tile",
            ha="center", va="center", fontsize=6.5,
            color="#999999", fontstyle="italic")
    draw_arrow(dec_x - 1.3 * 0.45, dec_y, dec_x - 1.2, dec_y,
               color="#bbbbbb", dashed=True)

    # YES branch
    draw_arrow(dec_x, dec_y - 0.45, dec_x, 6.4,
               label="YES --> template", label_offset=(0.85, 0.0))

    # Structured Prompt Engineering
    prompt_x, prompt_y = 5.0, 6.05
    draw_box(prompt_x, prompt_y, 2.6, 0.65,
             "Structured Prompt Engineering",
             "bloom count, density, heatmap\ngrowth stage --> advisory request",
             color=COL_PROMPT, fontsize=7.5, sublabel_size=5.5)

    # ═══════════════════════════════════════════════════════════════════
    # (3) LLM INFERENCE
    # ═══════════════════════════════════════════════════════════════════
    ax.text(0.3, 5.30, "(3) LLM Inference (Ollama)",
            ha="left", va="center", fontsize=8.5, fontweight="bold",
            color=COL_OLLAMA, fontstyle="italic")

    ollama_x, ollama_y = 5.0, 4.65
    draw_box(ollama_x, ollama_y, 2.4, 0.65, "Ollama Server",
             "127.0.0.1:11434, local\nzero cloud, 90 s timeout, triple-retry",
             color=COL_OLLAMA, fontsize=7.5, sublabel_size=5.5)

    draw_arrow(prompt_x, prompt_y - 0.33, ollama_x, ollama_y + 0.33,
               label="structured prompt", label_offset=(1.0, 0.0))

    # Three LLM models
    model_y = 3.35
    models = [
        ("Mistral 7B",  "1,127 ms, 4.4 GB\nReal-time advisory",
         2.5, COL_MODEL, False),
        ("Gemma3",       "8,882 ms, 3.3 GB\nEdge deployment",
         5.0, COL_MODEL, False),
        ("Llama3.1 8B",  "1,294 ms, 4.9 GB\nBatch analytics",
         7.5, COL_LLAMA, True),
    ]

    for label, sub, mx, col, hl in models:
        draw_box(mx, model_y, 1.9, 0.85, label, sub, color=col,
                 fontsize=7.5, sublabel_size=5.5, highlight=hl)

    for _, _, mx, _, _ in models:
        rad = 0.0 if mx == 5.0 else (-0.15 if mx < 5 else 0.15)
        draw_arrow(
            ollama_x + (mx - ollama_x) * 0.3, ollama_y - 0.33,
            mx, model_y + 0.43,
            connectionstyle=f"arc3,rad={rad}")

    # ═══════════════════════════════════════════════════════════════════
    # (4) EVALUATION PIPELINE
    # ═══════════════════════════════════════════════════════════════════
    ax.text(0.3, 2.50, "(4) Evaluation Pipeline",
            ha="left", va="center", fontsize=8.5, fontweight="bold",
            color=COL_OUTPUT, fontstyle="italic")

    out_x, out_y = 5.0, 1.70
    draw_box(out_x, out_y, 3.6, 0.8,
             "Evaluation Output and Performance Metrics",
             "harvest timing, spray schedule, yield estimate\n"
             "7-dim metrics (latency / memory / quality / throughput)",
             color=COL_OUTPUT, fontsize=7.5, sublabel_size=5.5)

    for _, _, mx, _, _ in models:
        rad = 0.0 if mx == 5.0 else (-0.12 if mx < 5 else 0.12)
        draw_arrow(
            mx, model_y - 0.43,
            out_x + (mx - out_x) * 0.2, out_y + 0.4,
            connectionstyle=f"arc3,rad={rad}")

    # ─── Caption ──────────────────────────────────────────────────────
    ax.text(5.0, 0.60,
            "Fig. 1.  End-to-end CV to LLM pipeline: UAV orthomosaics are "
            "processed through classical computer-vision\nstages to detect "
            "cotton blooms, then structured prompts drive on-device LLM "
            "inference via Ollama\n(Mistral / Gemma3 / Llama 3.1) to produce "
            "real-time agricultural advisories.",
            ha="center", va="center", fontsize=6, color=LABEL_COL,
            fontstyle="italic", linespacing=1.4)

    # ─── Save ─────────────────────────────────────────────────────────
    fig.savefig(save_path, facecolor=BG_COL, edgecolor="none", format=fmt)
    plt.close(fig)
    print(f"Saved: {save_path}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    png_path = os.path.join(script_dir, "cv_llm_pipeline_architecture.png")
    create_diagram(png_path, fmt="png")

    pdf_path = os.path.join(script_dir, "cv_llm_pipeline_architecture.pdf")
    create_diagram(pdf_path, fmt="pdf")
