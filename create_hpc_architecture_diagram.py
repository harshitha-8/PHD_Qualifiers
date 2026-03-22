"""
HPC Architecture Diagram for NeurIPS Publication
Includes SLURM Scheduler, HPCRoseDetector Class, H100 GPU Workers, and Output Metrics.
NeurIPS-style: Light background, Tahoma/sans-serif font, edge-to-edge arrows.
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

# Palette aligned to CV -> LLM pipeline for consistent coordination
COL_INPUT   = "#4C72B0"  # Matches COL_CV
COL_SLURM   = "#C44E52"  # Matches COL_MODEL
COL_HPC     = "#8172B2"  # Matches COL_OLLAMA
COL_GPU     = "#E07B39"  # Matches COL_DECIDE
COL_METRICS = "#55A868"  # Matches COL_PROMPT
EDGE_COL    = "#000000"
BOX_PAD     = 0.1  # Matches round box padding for edge-aligned arrows
BG_COL      = "#FFFFFF"
LABEL_COL   = "#555555"

# Arrow tuning for precise edge-to-edge
SHRINK_A = 0
SHRINK_B = 0  # For mutation_scale=12 (tips land on box edges)


def create_diagram(save_path, fmt="png"):
    fig, ax = plt.subplots(figsize=(13.5, 7.5))
    ax.set_xlim(0, 17.5)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    fig.patch.set_facecolor(BG_COL)
    ax.set_facecolor(BG_COL)

    # ── Text Helper ───────────────────────────────────────────────────
    def add_text(x, y, text, fontsize=7.5, color="#1a1a1a", weight="normal", family=None, style="normal", ha="center"):
        ax.text(x, y, text, ha=ha, va="center", fontsize=fontsize,
                fontweight=weight, color=color, fontfamily=family, fontstyle=style, zorder=5)

    # ── Box Helper ────────────────────────────────────────────────────
    def box(x, y, w, h, label, sublabel1=None, sublabel2=None, color=COL_INPUT,
            fontsize=8, sublabel_size=6, lw=1.2, alpha=0.12):
        fc = matplotlib.colors.to_rgba(color, alpha)
        p = FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="square,pad=0",  # Using square bounds, we draw a rounded rect inside
            facecolor="none", edgecolor="none") # Invisible bounding box just for math
        
        # Actual painted box
        true_box = FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.1",
            facecolor=fc, edgecolor=color, linewidth=lw, zorder=3)
        ax.add_patch(true_box)
        
        # Coordinates for text
        if sublabel1 and not sublabel2:
            ty, sy = y + 0.15, y - 0.25
        elif sublabel1 and sublabel2:
            ty, sy1, sy2 = y + 0.22, y - 0.1, y - 0.35
        else:
            ty = y

        add_text(x, ty, label, fontsize=fontsize, weight="bold")
        if sublabel1:
            if not sublabel2:
                add_text(x, sy, sublabel1, fontsize=sublabel_size, color=LABEL_COL, style="italic")
            else:
                add_text(x, sy1, sublabel1, fontsize=sublabel_size, color=LABEL_COL, style="italic")
                add_text(x, sy2, sublabel2, fontsize=sublabel_size, color=LABEL_COL, style="italic")
                
        return dict(cx=x, cy=y, w=w, h=h, t=y + h / 2, b=y - h / 2, l=x - w / 2, r=x + w / 2)

    # Edge helpers – arrows attach directly to the painted box edge
    # (no extra BOX_PAD offset; the round-pad is purely cosmetic)
    def edge_top(b):    return b["t"]
    def edge_bottom(b): return b["b"]
    def edge_left(b):   return b["l"]
    def edge_right(b):  return b["r"]

    # ── Arrow Helper ──────────────────────────────────────────────────
    def arrow(x1, y1, x2, y2, label=None, color=EDGE_COL, lw=1.2, dashed=False,
              lbl_off=(0, 0), lbl_fs=6, cs="arc3,rad=0", shrinkA=SHRINK_A, shrinkB=SHRINK_B,
              arrow_style="-|>", mutation=12, label_color="#444444", alpha=1.0):
        a = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle=arrow_style, color=color, linewidth=lw,
            linestyle="--" if dashed else "-",
            connectionstyle=cs, mutation_scale=mutation,
            zorder=2, shrinkA=shrinkA, shrinkB=shrinkB, alpha=alpha)
        ax.add_patch(a)
        if label:
            mx = (x1 + x2) / 2 + lbl_off[0]
            my = (y1 + y2) / 2 + lbl_off[1]
            ax.text(mx, my, label, ha="center", va="center",
                    fontsize=lbl_fs, color=label_color,
                    fontstyle="italic", zorder=6,
                    bbox=dict(facecolor="white", edgecolor="none",
                              pad=0.8, alpha=0.9))

    # ==================================================================
    #  COLUMNS & HEADINGS
    # ==================================================================
    cols = [1.5, 5.0, 8.5, 12.0, 15.5]
    headings = [
        "INPUT DATA",
        "SLURM SCHEDULER",
        "HPCRoseDetector CLASS",
        "H100 GPU WORKERS",
        "OUTPUT + METRICS"
    ]
    
    for x, title in zip(cols, headings):
        add_text(x, 9.6, title, fontsize=7.5, weight="bold", color="#888888")

    # ==================================================================
    #  COLUMN 1: INPUT DATA
    # ==================================================================
    bw_col1 = 2.4
    bh_col1 = 0.8
    y1_start = 8.2
    y1_gap = 1.6

    b1_1 = box(cols[0], y1_start, bw_col1, bh_col1, "UAV Seasonal Dataset",
               "3,000+ orthomosaics", "300-acre nursery · 2.5cm GSD", color=COL_INPUT)
    b1_2 = box(cols[0], y1_start - y1_gap, bw_col1, bh_col1, "Shared File System",
               "/scratch/tacc/images/", "batch manifest file", color=COL_INPUT)
    b1_3 = box(cols[0], y1_start - y1_gap*2, bw_col1, bh_col1, "Python 3.9.18 venv",
               "CUDA-enabled env", "Dependencies pre-loaded", color=COL_INPUT)

    arrow(b1_1["cx"], b1_1["b"], b1_2["cx"], b1_2["t"], label="store", lbl_off=(0.4, 0))
    arrow(b1_2["cx"], b1_2["b"], b1_3["cx"], b1_3["t"], label="env", lbl_off=(0.4, 0))


    # ==================================================================
    #  COLUMN 2: SLURM SCHEDULER
    # ==================================================================
    bw_col2 = 2.6
    bh_col2 = 0.8
    # Align SLURM Job Script with HPCRoseDetector.run()
    # Align SLURM Job Script with HPCRoseDetector.run()
    y2_start = 8.4
    y2_gap = 1.2

    b2_1 = box(cols[1], y2_start, bw_col2, bh_col2, "SLURM Job Script",
               "#SBATCH --partition=gpu", "#SBATCH --nodes=1-4 --gres=gpu:h100", color=COL_SLURM)
    b2_2 = box(cols[1], y2_start - y2_gap, bw_col2, bh_col2, "Job Queue & Scheduling",
               "Stampede3 H100 nodes", "Priority queue allocation", color=COL_SLURM)
    b2_3 = box(cols[1], y2_start - y2_gap*2, bw_col2, bh_col2, "Worker Allocation",
               "1 - 4 parallel workers", "Optimal: 1.75 workers", color=COL_SLURM)

    # Python venv is activated by the SLURM job script (clean elbow to SLURM)
    env_x = b1_3["r"] + 0.4
    arrow(b1_3["r"], b1_3["cy"], env_x, b1_3["cy"], arrow_style="-")
    arrow(env_x, b1_3["cy"], env_x, b2_1["cy"], arrow_style="-")
    arrow(env_x, b2_1["cy"], b2_1["l"], b2_1["cy"])
    ax.text((env_x + b2_1["l"]) / 2, b2_1["cy"] + 0.25, "loaded by job",
            ha="center", va="center", fontsize=6, color=LABEL_COL,
            fontstyle="italic", zorder=6,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.3, alpha=0.95))

    arrow(b2_1["cx"], b2_1["b"], b2_2["cx"], b2_2["t"], label="submit", lbl_off=(0.4, 0))
    arrow(b2_2["cx"], b2_2["b"], b2_3["cx"], b2_3["t"], label="dispatch", lbl_off=(0.4, 0))


    # ==================================================================
    #  COLUMN 3: HPCRoseDetector CLASS
    # ==================================================================
    bw_col3 = 3.2
    bh_col3 = 0.8
    # Even vertical spacing in HPCRoseDetector column
    y3_gap = 1.1
    y3_start = 7.6

    b3_1 = box(cols[2], y3_start, bw_col3, bh_col3, "HPCRoseDetector.run()",
               "Orchestrator class · Python 3.9.18", "CUDA-accelerated · batch_size=16", color=COL_HPC)
    b3_2 = box(cols[2], y3_start - y3_gap, bw_col3, bh_col3, "Image Tile Generator",
               "512x512 patches · 64px overlap", "~100 tiles per orthomosaic", color=COL_HPC)
    b3_3 = box(cols[2], y3_start - y3_gap*2, bw_col3, bh_col3, "CV Detection Engine",
               "HSV -> DBSCAN -> Morphology", "Bloom count N per tile", color=COL_HPC)

    # Shared File System -> Image Tile Generator
    # Fix 4: L-shaped elbow: go down from Shared File System's bottom,
    # then right UNDER all SLURM boxes, then up into Image Tile Generator.
    read_start_y  = b1_2["b"]                # bottom of Shared File System
    read_bottom_y = b1_3["b"] - 0.3          # well below Python venv (lowest col1 box)
    read_entry_x  = edge_left(b3_2)          # left side of Image Tile Generator
    # Down from Shared File System
    arrow(b1_2["cx"] + 0.8, b1_2["b"], b1_2["cx"] + 0.8, read_bottom_y, arrow_style="-")
    # Right under SLURM boxes to HPC column
    arrow(b1_2["cx"] + 0.8, read_bottom_y, read_entry_x, read_bottom_y, arrow_style="-")
    # Up into Image Tile Generator's left side
    arrow(read_entry_x, read_bottom_y, read_entry_x, b3_2["cy"], arrow_style="-")
    arrow(read_entry_x, b3_2["cy"], b3_2["l"], b3_2["cy"])
    # Label near the bottom horizontal segment
    ax.text((b1_2["cx"] + 0.8 + read_entry_x) / 2, read_bottom_y + 0.2, "read images",
            ha="center", va="center", fontsize=6, color=LABEL_COL,
            fontstyle="italic", zorder=6,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.4, alpha=0.95))
    
    # LLM Trigger Logic - highlighted with Orange
    b3_4 = box(cols[2], y3_start - y3_gap*3, bw_col3, bh_col3, "LLM Trigger Logic",
               "IF N >= 10-15: invoke Ollama", "ELSE: skip tile (save compute)", color=COL_GPU, alpha=0.15)
               
    b3_5 = box(cols[2], y3_start - y3_gap*4, bw_col3, bh_col3, "Prompt Builder",
               "Bloom count · density · heatmap", "-> structured advisory request", color=COL_HPC)

    # Connections from Slurm (orchestrate enters the TOP edge of HPCRoseDetector.run())
    orch_x = b2_1["r"] + 0.5
    orch_y = edge_top(b3_1) + 0.15
    arrow(b2_1["r"], b2_1["cy"], orch_x, b2_1["cy"], arrow_style="-")
    arrow(orch_x, b2_1["cy"], orch_x, orch_y, arrow_style="-")
    arrow(orch_x, orch_y, b3_1["cx"], orch_y, arrow_style="-")
    arrow(b3_1["cx"], orch_y, b3_1["cx"], edge_top(b3_1), lw=1.6)
    ax.text((orch_x + b3_1["cx"]) / 2, orch_y + 0.12, "orchestrate",
            ha="center", va="center", fontsize=6.2, color=LABEL_COL,
            fontstyle="italic", fontweight="bold", zorder=6,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.3, alpha=0.95))

    # Vertical sequence (Fix 3: arrows snap to box edges)
    arrow(b3_1["cx"], b3_1["b"], b3_2["cx"], b3_2["t"], label="tiles", lbl_off=(0.5, 0))
    arrow(b3_2["cx"], b3_2["b"], b3_3["cx"], b3_3["t"], label="detect", lbl_off=(0.5, 0))
    arrow(b3_3["cx"], b3_3["b"], b3_4["cx"], b3_4["t"], label="N count", lbl_off=(0.55, 0))
    # Fix 5: "YES branch" label placed to the LEFT of the arrow, clear of box text
    arrow(b3_4["cx"], b3_4["b"], b3_5["cx"], b3_5["t"])
    # Place label manually to the left, midway between the two boxes
    yes_mid_y = (b3_4["b"] + b3_5["t"]) / 2
    ax.text(b3_4["cx"] - 1.2, yes_mid_y, "YES branch",
            ha="center", va="center", fontsize=6.5, color="#2E7D32",
            fontstyle="italic", fontweight="bold", zorder=6,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.4, alpha=0.95))
    # NO branch from LLM Trigger Logic -> termination (tile discarded)
    no_x = b3_4["l"] - 0.35
    arrow(b3_4["l"], b3_4["cy"], no_x, b3_4["cy"], dashed=True, arrow_style="-")
    # termination bar
    ax.plot([no_x - 0.1, no_x - 0.1], [b3_4["cy"] - 0.12, b3_4["cy"] + 0.12],
            color=EDGE_COL, linewidth=1.2, linestyle="--", zorder=2)
    ax.text(no_x - 0.15, b3_4["cy"] - 0.25, "NO: tile discarded",
            ha="right", va="center", fontsize=6, color=LABEL_COL,
            fontstyle="italic", zorder=6,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.3, alpha=0.95))


    # ==================================================================
    #  COLUMN 4: H100 GPU WORKERS
    # ==================================================================
    bw_col4 = 2.4
    bh_col4 = 0.8
    y4_start = 8.3
    y4_gap = 1.1
    
    b4_1 = box(cols[3], y4_start, bw_col4, 1.0, "H100 GPU Node",
               "80GB HBM3 · 3.35 TB/s", "CUDA 12.x · NVLink", color=COL_SLURM)  # Matches reference red
               
    b4_2 = box(cols[3], y4_start - y4_gap, bw_col4, bh_col4, "Ollama Server",
               "127.0.0.1:11434", "90s timeout · triple-retry", color=COL_HPC) # Matches pipeline Ollama color
               
    b4_3 = box(cols[3], y4_start - 2*y4_gap, bw_col4, bh_col4, "Mistral 7B",
               "1,127ms · 4.4GB", None, color=COL_INPUT)
               
    b4_4 = box(cols[3], y4_start - 3*y4_gap, bw_col4, bh_col4, "Gemma3",
               "8,882ms · 3.3GB", None, color=COL_METRICS)
               
    b4_5 = box(cols[3], y4_start - 4*y4_gap, bw_col4, bh_col4, "Llama3.1 8B",
               "1,294ms · 4.9GB", None, color=COL_GPU) # Orange

    # Connections into and within Column 4
    arrow(b4_1["cx"], b4_1["b"], b4_2["cx"], b4_2["t"], label="CUDA", lbl_off=(0.3, 0))
    arrow(b4_2["cx"], b4_2["b"], b4_3["cx"], b4_3["t"])
    ax.text(b4_2["cx"] + 0.1, (b4_2["b"] + b4_3["t"]) / 2 + 0.12, "sequential dispatch",
            ha="center", va="center", fontsize=6, color=LABEL_COL,
            fontstyle="italic", zorder=6,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.3, alpha=0.95))
    # SLURM reserves hardware nodes (route above HPCRoseDetector box)
    reserve_y = 9.2
    reserve_x = b4_1["l"] - 0.25
    arrow(b2_1["r"], b2_1["cy"], b2_1["r"], reserve_y, arrow_style="-")
    arrow(b2_1["r"], reserve_y, reserve_x, reserve_y, arrow_style="-")
    arrow(reserve_x, reserve_y, reserve_x, b4_1["cy"], arrow_style="-")
    arrow(reserve_x, b4_1["cy"], b4_1["l"], b4_1["cy"])
    ax.text((b2_1["r"] + reserve_x) / 2, reserve_y + 0.12, "reserve node",
            ha="center", va="center", fontsize=6, color=LABEL_COL,
            fontstyle="italic", zorder=6,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.3, alpha=0.95))
    
    # Prompt Builder -> Ollama Server (clean orthogonal handoff)
    prompt_mid_x = (b3_5["r"] + b4_2["l"]) / 2
    arrow(edge_right(b3_5), b3_5["cy"], prompt_mid_x, b3_5["cy"], arrow_style="-")
    arrow(prompt_mid_x, b3_5["cy"], prompt_mid_x, b4_2["cy"], arrow_style="-")
    arrow(prompt_mid_x, b4_2["cy"], edge_left(b4_2), b4_2["cy"], label="prompt ->", lbl_off=(0, 0.2))
    
    # Fix 2: Worker Allocation -> HPCRoseDetector.run() (NOT Image Tile Generator)
    # L-shaped arrow: right from Worker Allocation, up to HPCRoseDetector.run() row,
    # then left into HPCRoseDetector.run() left edge.
    assign_mid_y = b3_1["cy"]           # target row
    assign_x     = b2_3["r"] + 0.25     # elbow x (tight to SLURM right edge)
    arrow(edge_right(b2_3), b2_3["cy"], assign_x, b2_3["cy"], arrow_style="-")
    arrow(assign_x, b2_3["cy"], assign_x, assign_mid_y, arrow_style="-")
    arrow(assign_x, assign_mid_y, edge_left(b3_1), assign_mid_y)
    # Label along the vertical segment
    ax.text(assign_x - 0.5, (b2_3["cy"] + assign_mid_y) / 2, "assign\nworkers",
            ha="center", va="center", fontsize=6, color=LABEL_COL,
            fontstyle="italic", zorder=6,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.3, alpha=0.95))


    # ==================================================================
    #  COLUMN 5: OUTPUT + METRICS
    # ==================================================================
    bw_col5 = 2.6
    bh_col5 = 0.8

    # Fix 1: Move output boxes up so top aligns with Mistral 7B's height,
    # and distribute evenly with generous vertical gaps.
    out_top_y = b4_3["cy"]          # align "Model Output Dirs" with Mistral 7B
    out_bot_y = b4_5["cy"] - 0.8    # extend well below Llama3.1 for breathing room
    out_gap   = (out_top_y - out_bot_y) / 3   # equal spacing between 4 boxes

    b5_1 = box(cols[4], out_top_y,             bw_col5, bh_col5, "Model Output Dirs",
               "/mistral/ /gemma3/ /llama3/", "bbox · heatmap · report", color=COL_METRICS)
               
    b5_2 = box(cols[4], out_top_y - out_gap,   bw_col5, bh_col5, "7-Dim Metrics CSV",
               "latency · memory · quality", "throughput · efficiency · success", color=COL_METRICS)
               
    b5_3 = box(cols[4], out_top_y - 2*out_gap, bw_col5, bh_col5, "Scaling Analysis",
               "Strong: peak 1.75 workers", "Weak: linear throughput", color=COL_METRICS)
               
    b5_4 = box(cols[4], out_top_y - 3*out_gap, bw_col5, bh_col5, "Advisory Reports",
               "harvest · spray · yield estimate", "per-nursery recommendations", color=COL_METRICS)

    # ------------------------------------------------------------------
    # Fix 6: Clean LLM -> output routing (avoid 12 tangled arrows)
    # Route each model to its nearest 2 outputs; add annotation.
    # Mistral  -> Model Output Dirs, 7-Dim Metrics CSV      (top two)
    # Gemma3   -> 7-Dim Metrics CSV,  Scaling Analysis       (middle two)
    # Llama3.1 -> Scaling Analysis,   Advisory Reports       (bottom two)
    # ------------------------------------------------------------------
    arrow(b4_3["r"], b4_3["cy"], b5_1["l"], b5_1["cy"], lw=1.0)
    arrow(b4_3["r"], b4_3["cy"], b5_2["l"], b5_2["cy"], lw=1.0)

    arrow(b4_4["r"], b4_4["cy"], b5_2["l"], b5_2["cy"], lw=1.0)
    arrow(b4_4["r"], b4_4["cy"], b5_3["l"], b5_3["cy"], lw=1.0)

    arrow(b4_5["r"], b4_5["cy"], b5_3["l"], b5_3["cy"], lw=1.0)
    arrow(b4_5["r"], b4_5["cy"], b5_4["l"], b5_4["cy"], lw=1.0)

    # Annotation: clarify that every model feeds every output
    note_x = (b4_3["r"] + b5_1["l"]) / 2
    note_y = b5_4["b"] - 0.4
    ax.text(note_x, note_y, "all models -> all outputs",
            ha="center", va="center", fontsize=6.5, color="#666666",
            fontstyle="italic", fontweight="bold", zorder=6,
            bbox=dict(facecolor="#FFFFCC", edgecolor="#CCCC88",
                      boxstyle="round,pad=0.3", alpha=0.95))
    
    # (Feedback loop removed to avoid dashed artifact box)


    fig.savefig(save_path, facecolor=BG_COL, edgecolor="none", format=fmt)
    plt.close(fig)
    print(f"Saved: {save_path}")

if __name__ == "__main__":
    d = os.path.dirname(os.path.abspath(__file__))
    create_diagram(os.path.join(d, "hpc_architecture_diagram.png"), "png")
    create_diagram(os.path.join(d, "hpc_architecture_diagram.pdf"), "pdf")
