"""
HPC Architecture Diagram for NeurIPS Publication
Includes SLURM Scheduler, HPCRoseDetector Class, H100 GPU Workers, and Output Metrics.
NeurIPS-style: Light background, Tahoma/sans-serif font, edge-to-edge arrows.

ALL arrows start at a box edge and end touching the next box edge.
NO arrow penetrates a box interior.
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

# ── Colour palette ────────────────────────────────────────────────────
COL_INPUT   = "#4C72B0"
COL_SLURM   = "#C44E52"
COL_HPC     = "#8172B2"
COL_GPU     = "#E07B39"
COL_METRICS = "#55A868"
EDGE_COL    = "#333333"
BG_COL      = "#FFFFFF"
LABEL_COL   = "#555555"


def create_diagram(save_path, fmt="png"):
    fig, ax = plt.subplots(figsize=(15, 9))
    ax.set_xlim(0, 19)
    ax.set_ylim(0, 11.5)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    fig.patch.set_facecolor(BG_COL)
    ax.set_facecolor(BG_COL)

    # ── Text helper ──────────────────────────────────────────────────
    def label(x, y, text, fs=7, color="#1a1a1a", weight="normal",
              style="normal", ha="center", va="center"):
        ax.text(x, y, text, ha=ha, va=va, fontsize=fs,
                fontweight=weight, color=color, fontstyle=style, zorder=5)

    # ── Box helper ───────────────────────────────────────────────────
    def box(x, y, w, h, title, sub1=None, sub2=None, color=COL_INPUT,
            fs=8.5, sub_fs=6.5, lw=1.4, alpha=0.12):
        fc = matplotlib.colors.to_rgba(color, alpha)
        patch = FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.08",
            facecolor=fc, edgecolor=color, linewidth=lw, zorder=3)
        ax.add_patch(patch)

        if sub1 and sub2:
            ty, s1y, s2y = y + 0.22, y - 0.08, y - 0.32
        elif sub1:
            ty, s1y = y + 0.15, y - 0.2
        else:
            ty = y

        label(x, ty, title, fs=fs, weight="bold")
        if sub1:
            label(x, s1y, sub1, fs=sub_fs, color=LABEL_COL, style="italic")
        if sub1 and sub2:
            label(x, s2y, sub2, fs=sub_fs, color=LABEL_COL, style="italic")

        return dict(cx=x, cy=y, w=w, h=h,
                    t=y + h / 2, b=y - h / 2,
                    l=x - w / 2, r=x + w / 2)

    # ── Edge accessors ───────────────────────────────────────────────
    def top(b):    return (b["cx"], b["t"])
    def bot(b):    return (b["cx"], b["b"])
    def lft(b):    return (b["l"], b["cy"])
    def rht(b):    return (b["r"], b["cy"])

    # ── Arrow: straight ──────────────────────────────────────────────
    def arr(p1, p2, lbl=None, loff=(0, 0), color=EDGE_COL, lw=1.2,
            dashed=False, headless=False, lbl_fs=6):
        style = "-" if headless else "-|>"
        a = FancyArrowPatch(
            p1, p2,
            arrowstyle=style, color=color, linewidth=lw,
            linestyle="--" if dashed else "-",
            connectionstyle="arc3,rad=0", mutation_scale=12,
            shrinkA=0, shrinkB=0, zorder=2)
        ax.add_patch(a)
        if lbl:
            mx = (p1[0] + p2[0]) / 2 + loff[0]
            my = (p1[1] + p2[1]) / 2 + loff[1]
            ax.text(mx, my, lbl, ha="center", va="center",
                    fontsize=lbl_fs, color=LABEL_COL, fontstyle="italic",
                    zorder=6,
                    bbox=dict(facecolor="white", edgecolor="none",
                              pad=0.6, alpha=0.95))

    # ── Arrow: L-shaped elbow (two segments) ─────────────────────────
    def elbow_h_then_v(p_start, p_end, lbl=None, loff=(0, 0),
                       color=EDGE_COL, lw=1.2, dashed=False):
        """Horizontal first, then vertical, with arrow at end."""
        mid = (p_end[0], p_start[1])
        arr(p_start, mid, headless=True, color=color, lw=lw, dashed=dashed)
        arr(mid, p_end, lbl=lbl, loff=loff, color=color, lw=lw, dashed=dashed)

    def elbow_v_then_h(p_start, p_end, lbl=None, loff=(0, 0),
                       color=EDGE_COL, lw=1.2, dashed=False):
        """Vertical first, then horizontal, with arrow at end."""
        mid = (p_start[0], p_end[1])
        arr(p_start, mid, headless=True, color=color, lw=lw, dashed=dashed)
        arr(mid, p_end, lbl=lbl, loff=loff, color=color, lw=lw, dashed=dashed)

    # ==================================================================
    #  COLUMN X-CENTRES & HEADINGS
    # ==================================================================
    cx1, cx2, cx3, cx4, cx5 = 1.8, 5.2, 9.0, 13.0, 16.8
    heading_y = 10.8
    for cx, txt in zip(
        [cx1, cx2, cx3, cx4, cx5],
        ["INPUT DATA", "SLURM SCHEDULER", "HPCRoseDetector CLASS",
         "H100 GPU WORKERS", "OUTPUT + METRICS"]):
        label(cx, heading_y, txt, fs=7.5, weight="bold", color="#888888")

    # ==================================================================
    #  COLUMN 1 — INPUT DATA
    # ==================================================================
    bw1, bh1 = 2.5, 0.85
    y1 = 9.5
    g1 = 1.5

    b_uav  = box(cx1, y1,        bw1, bh1, "UAV Seasonal Dataset",
                 "3,000+ orthomosaics", "300-acre nursery . 2.5cm GSD", color=COL_INPUT)
    b_sfs  = box(cx1, y1 - g1,   bw1, bh1, "Shared File System",
                 "/scratch/tacc/images/", "batch manifest file", color=COL_INPUT)
    b_venv = box(cx1, y1 - 2*g1, bw1, bh1, "Python 3.9.18 venv",
                 "CUDA-enabled env", "Dependencies pre-loaded", color=COL_INPUT)

    # UAV -> Shared File System
    arr(bot(b_uav), top(b_sfs), lbl="store", loff=(0.5, 0))
    # Shared File System -> Python venv
    arr(bot(b_sfs), top(b_venv), lbl="env", loff=(0.5, 0))

    # ==================================================================
    #  COLUMN 2 — SLURM SCHEDULER
    # ==================================================================
    bw2, bh2 = 2.8, 0.85
    y2 = 9.5
    g2 = 1.35

    b_slurm = box(cx2, y2,        bw2, bh2, "SLURM Job Script",
                  "#SBATCH --partition=gpu", "#SBATCH --nodes=1-4 --gres=gpu:h100",
                  color=COL_SLURM)
    b_queue = box(cx2, y2 - g2,   bw2, bh2, "Job Queue & Scheduling",
                  "Stampede3 H100 nodes", "Priority queue allocation", color=COL_SLURM)
    b_work  = box(cx2, y2 - 2*g2, bw2, bh2, "Worker Allocation",
                  "1 - 4 parallel workers", "Optimal: 1.75 workers", color=COL_SLURM)

    # Vertical chain in SLURM
    arr(bot(b_slurm), top(b_queue), lbl="submit", loff=(0.5, 0))
    arr(bot(b_queue), top(b_work),  lbl="dispatch", loff=(0.5, 0))

    # Python venv -> SLURM "loaded by job" (elbow right then up)
    venv_r = rht(b_venv)
    slurm_l = lft(b_slurm)
    bend_x = (venv_r[0] + slurm_l[0]) / 2
    arr(venv_r, (bend_x, venv_r[1]), headless=True)
    arr((bend_x, venv_r[1]), (bend_x, slurm_l[1]), headless=True)
    arr((bend_x, slurm_l[1]), slurm_l)
    label(bend_x, slurm_l[1] + 0.28, "loaded by job", fs=5.5,
          color=LABEL_COL, style="italic")

    # Worker Allocation "Uses Env" -> Python venv (horizontal left)
    work_l = lft(b_work)
    venv_r2 = rht(b_venv)
    # Route: left from Worker, then down to venv row, then left into venv
    uses_x = work_l[0] - 0.2
    arr(work_l, (uses_x, work_l[1]), headless=True)
    arr((uses_x, work_l[1]), (uses_x, venv_r2[1]), headless=True)
    arr((uses_x, venv_r2[1]), venv_r2)
    label(uses_x - 0.35, (work_l[1] + venv_r2[1]) / 2, "Uses Env",
          fs=5.5, color=LABEL_COL, style="italic")

    # ==================================================================
    #  COLUMN 3 — HPCRoseDetector CLASS
    # ==================================================================
    bw3, bh3 = 3.3, 0.85
    y3 = 8.6
    g3 = 1.2   # generous gap between boxes

    b_run   = box(cx3, y3,        bw3, bh3, "HPCRoseDetector.run()",
                  "Orchestrator class . Python 3.9.18",
                  "CUDA-accelerated . batch_size=16", color=COL_HPC)
    b_tile  = box(cx3, y3 - g3,   bw3, bh3, "Image Tile Generator",
                  "512x512 patches . 64px overlap",
                  "~100 tiles per orthomosaic", color=COL_HPC)
    b_cv    = box(cx3, y3 - 2*g3, bw3, bh3, "CV Detection Engine",
                  "HSV -> DBSCAN -> Morphology",
                  "Bloom count N per tile", color=COL_HPC)
    b_trig  = box(cx3, y3 - 3*g3, bw3, bh3, "LLM Trigger Logic",
                  "IF N >= 10-15: invoke Ollama",
                  "ELSE: skip tile (save compute)", color=COL_GPU, alpha=0.15)
    b_prmpt = box(cx3, y3 - 4*g3, bw3, bh3, "Prompt Builder",
                  "Bloom count . density . heatmap",
                  "-> structured advisory request", color=COL_HPC)

    # Vertical chain — arrows start at box bottom edge, end at next box top edge
    arr(bot(b_run),  top(b_tile),  lbl="tiles",  loff=(0.6, 0))
    arr(bot(b_tile), top(b_cv),    lbl="detect",  loff=(0.6, 0))
    arr(bot(b_cv),   top(b_trig),  lbl="N count", loff=(0.65, 0))
    arr(bot(b_trig), top(b_prmpt), lbl="YES branch", loff=(-0.8, 0))

    # NO branch — dashed left from LLM Trigger Logic
    no_pt = lft(b_trig)
    no_end = (no_pt[0] - 0.8, no_pt[1])
    arr(no_pt, no_end, dashed=True, headless=True)
    ax.plot([no_end[0] - 0.05, no_end[0] - 0.05],
            [no_end[1] - 0.15, no_end[1] + 0.15],
            color=EDGE_COL, linewidth=1.5, linestyle="--", zorder=2)
    label(no_end[0] - 0.5, no_end[1] - 0.3, "NO: tile discarded",
          fs=5.5, color=LABEL_COL, style="italic")

    # --- SLURM -> HPCRoseDetector connections ---

    # "orchestrate" — SLURM Job Script right edge -> HPCRoseDetector.run() left edge
    arr(rht(b_slurm), lft(b_run), lbl="orchestrate", loff=(0, 0.25))

    # "callback" — HPCRoseDetector.run() top -> up and right to H100 GPU area
    # (drawn later after column 4 boxes exist)

    # Shared File System -> Image Tile Generator
    # L-elbow: right from SFS, then down to tile row, then right into tile
    sfs_r = rht(b_sfs)
    tile_l = lft(b_tile)
    # Route through the gap between SLURM and HPC columns
    read_x = (cx2 + cx3) / 2 - 0.3
    arr(sfs_r, (read_x, sfs_r[1]), headless=True)
    arr((read_x, sfs_r[1]), (read_x, tile_l[1]), headless=True)
    arr((read_x, tile_l[1]), tile_l)
    label(read_x + 0.55, (sfs_r[1] + tile_l[1]) / 2, "read images",
          fs=5.5, color=LABEL_COL, style="italic")

    # ==================================================================
    #  COLUMN 4 — H100 GPU WORKERS
    # ==================================================================
    bw4, bh4 = 2.5, 0.85
    y4 = 9.6
    g4_top = 1.3   # GPU Node -> Ollama
    g4_mid = 1.2   # Ollama -> Mistral
    g4_llm = 1.1   # between LLMs

    b_gpu    = box(cx4, y4,                     bw4, 1.0, "H100 GPU Node",
                   "80GB HBM3 . 3.35 TB/s", "CUDA 12.x . NVLink", color=COL_SLURM)
    b_ollama = box(cx4, y4 - g4_top,            bw4, bh4, "Ollama Server",
                   "127.0.0.1:11434", "90s timeout . triple-retry", color=COL_HPC)
    b_mist   = box(cx4, y4 - g4_top - g4_mid,  bw4, bh4, "Mistral 7B",
                   "1,127ms . 4.4GB", None, color=COL_INPUT)
    b_gemma  = box(cx4, y4 - g4_top - g4_mid - g4_llm, bw4, bh4, "Gemma3",
                   "8,882ms . 3.3GB", None, color=COL_METRICS)
    b_llama  = box(cx4, y4 - g4_top - g4_mid - 2*g4_llm, bw4, bh4, "Llama3.1 8B",
                   "1,294ms . 4.9GB", None, color=COL_GPU)

    # GPU Node -> Ollama
    arr(bot(b_gpu), top(b_ollama), lbl="CUDA", loff=(0.45, 0))
    # Ollama -> Mistral (sequential dispatch label)
    arr(bot(b_ollama), top(b_mist))
    label(cx4 + 0.2, (b_ollama["b"] + b_mist["t"]) / 2, "sequential dispatch",
          fs=5.5, color=LABEL_COL, style="italic")
    # Mistral -> Gemma -> Llama (within-column)
    arr(bot(b_mist), top(b_gemma))
    arr(bot(b_gemma), top(b_llama))

    # "reserve node" — SLURM Job Script top -> right across -> H100 GPU Node top
    reserve_y = 10.4
    s_top = top(b_slurm)
    g_top = top(b_gpu)
    arr(s_top, (s_top[0], reserve_y), headless=True)
    arr((s_top[0], reserve_y), (g_top[0], reserve_y), headless=True)
    arr((g_top[0], reserve_y), g_top)
    label((s_top[0] + g_top[0]) / 2, reserve_y + 0.18, "reserve node",
          fs=5.5, color=LABEL_COL, style="italic")

    # "callback" — HPCRoseDetector.run() right -> Ollama left
    arr(rht(b_run), lft(b_ollama), lbl="callback", loff=(0, 0.25))

    # "prompt" — Prompt Builder right -> Ollama Server left (L-elbow up)
    pr_r = rht(b_prmpt)
    ol_l = lft(b_ollama)
    prompt_x = (pr_r[0] + ol_l[0]) / 2
    arr(pr_r, (prompt_x, pr_r[1]), headless=True)
    arr((prompt_x, pr_r[1]), (prompt_x, ol_l[1]), headless=True)
    arr((prompt_x, ol_l[1]), ol_l)
    label(prompt_x + 0.5, (pr_r[1] + ol_l[1]) / 2, "prompt",
          fs=5.5, color=LABEL_COL, style="italic")

    # ==================================================================
    #  COLUMN 5 — OUTPUT + METRICS
    # ==================================================================
    bw5, bh5 = 2.6, 0.85
    # Align with LLM vertical span
    out_top_y = b_mist["cy"]
    out_gap   = 1.1

    b_dirs = box(cx5, out_top_y,            bw5, bh5, "Model Output Dirs",
                 "/mistral/ /gemma3/ /llama3/", "bbox . heatmap . report", color=COL_METRICS)
    b_csv  = box(cx5, out_top_y - out_gap,  bw5, bh5, "7-Dim Metrics CSV",
                 "latency . memory . quality", "throughput . efficiency . success", color=COL_METRICS)
    b_scal = box(cx5, out_top_y - 2*out_gap, bw5, bh5, "Scaling Analysis",
                 "Strong: peak 1.75 workers", "Weak: linear throughput", color=COL_METRICS)
    b_advs = box(cx5, out_top_y - 3*out_gap, bw5, bh5, "Advisory Reports",
                 "harvest . spray . yield estimate", "per-nursery recommendations", color=COL_METRICS)

    # LLM -> Output routing (clean, non-crossing)
    # Mistral  -> top two (Output Dirs, 7-Dim CSV)
    # Gemma3   -> middle two (7-Dim CSV, Scaling)
    # Llama3.1 -> bottom two (Scaling, Advisory)
    arr(rht(b_mist),  lft(b_dirs), lw=1.0)
    arr(rht(b_mist),  lft(b_csv),  lw=1.0)

    arr(rht(b_gemma), lft(b_csv),  lw=1.0)
    arr(rht(b_gemma), lft(b_scal), lw=1.0)

    arr(rht(b_llama), lft(b_scal), lw=1.0)
    arr(rht(b_llama), lft(b_advs), lw=1.0)

    # Clarification note
    note_x = (b_llama["r"] + b_advs["l"]) / 2
    note_y = b_advs["b"] - 0.45
    ax.text(note_x, note_y, "all models -> all outputs",
            ha="center", va="center", fontsize=6.5, color="#666666",
            fontstyle="italic", fontweight="bold", zorder=6,
            bbox=dict(facecolor="#FFFFCC", edgecolor="#CCCC88",
                      boxstyle="round,pad=0.25", alpha=0.95))

    # ==================================================================
    #  FEEDBACK LOOP — scaling results inform worker allocation
    # ==================================================================
    fb_y = b_advs["b"] - 1.0
    scal_b = bot(b_scal)
    work_b = bot(b_work)
    # Down from Scaling Analysis
    arr(scal_b, (scal_b[0], fb_y), headless=True, dashed=True,
        color="#4C72B0")
    # Left across bottom
    arr((scal_b[0], fb_y), (work_b[0], fb_y), headless=True, dashed=True,
        color="#4C72B0")
    # Up into Worker Allocation
    arr((work_b[0], fb_y), work_b, dashed=True, color="#4C72B0")
    label((scal_b[0] + work_b[0]) / 2, fb_y + 0.22,
          "scaling results inform worker allocation",
          fs=5.5, color="#4C72B0", style="italic")

    # ==================================================================
    #  SAVE
    # ==================================================================
    fig.savefig(save_path, facecolor=BG_COL, edgecolor="none", format=fmt)
    plt.close(fig)
    print(f"Saved: {save_path}")


if __name__ == "__main__":
    d = os.path.dirname(os.path.abspath(__file__))
    create_diagram(os.path.join(d, "hpc_architecture_diagram.png"), "png")
    create_diagram(os.path.join(d, "hpc_architecture_diagram.pdf"), "pdf")
