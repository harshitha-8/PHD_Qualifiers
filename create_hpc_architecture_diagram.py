"""
HPC Architecture Diagram mapped EXACTLY to the user-provided reference image.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

plt.rcParams.update({
    "font.family":      "sans-serif",
    "font.sans-serif":  ["Tahoma", "Arial", "DejaVu Sans"],
    "font.size":        10,
    "text.usetex":      False,
    "figure.dpi":       300,
    "savefig.dpi":      300,
    "savefig.bbox":     "tight",
    "savefig.pad_inches": 0.05,
})

# ── Colors matched to reference image ─────────────────────────────────
C_IN  = "#D3DAED"  # Light Blue/Gray (Input Data)
C_SL  = "#E8AEAA"  # Light Red/Pink (Slurm, H100)
C_HPC = "#D5C4DB"  # Light Purple (HPC top 3)
C_TRG = "#FCE3C5"  # Light Orange (HPC bottom 2)
C_GRN = "#C5E0C2"  # Light Green (LLMs, Outputs)
EDGE_COL = "#222222"
BG_COL   = "#FFFFFF"
LABEL_COL = "#000000"


def create_diagram(save_path, fmt="png"):
    fig, ax = plt.subplots(figsize=(27.5, 11))
    ax.set_xlim(0, 32.5)
    ax.set_ylim(0, 14.5)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    fig.patch.set_facecolor(BG_COL)
    ax.set_facecolor(BG_COL)

    # ── Text helper ──────────────────────────────────────────────────
    def label(x, y, text, fs=10, color=LABEL_COL, weight="bold",
              style="normal", ha="center", va="center"):
        ax.text(x, y, text, ha=ha, va=va, fontsize=fs,
                fontweight=weight, color=color, fontstyle=style, zorder=5)

    # ── Box helper ───────────────────────────────────────────────────
    def box(cx, cy, w, h, text, fc, ec="#333333", lw=1.2):
        # Background box
        patch = FancyBboxPatch(
            (cx - w/2, cy - h/2), w, h,
            boxstyle="round,pad=0.08",
            facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3)
        ax.add_patch(patch)
        
        # Split text into lines. First line is bold (Title), rest normal.
        lines = text.split('\n')
        title = lines[0]
        
        # Position title near the top of the box
        title_y = cy + (h/2) - 0.25
        ax.text(cx, title_y, title, ha='center', va='top', 
                fontsize=11.5, fontweight='bold', zorder=5)
        
        # Position the rest of the lines with proper spacing
        if len(lines) > 1:
            sub = '\n'.join(lines[1:])
            ax.text(cx, title_y - 0.35, sub, ha='center', va='top', 
                    fontsize=9.5, fontweight='normal', zorder=5, linespacing=1.4)

        return dict(cx=cx, cy=cy, w=w, h=h,
                    t=(cx, cy + h/2 + 0.08), b=(cx, cy - h/2 - 0.08),
                    l=(cx - w/2 - 0.08, cy), r=(cx + w/2 + 0.08, cy))

    # ── Arrow: straight ──────────────────────────────────────────────
    def arr(p1, p2, lbl=None, loff=(0, 0), color=EDGE_COL, lw=1.2,
            dashed=False, headless=False, lbl_fs=10, lbl_ha="center", lbl_va="center"):
        style = "-" if headless else "-|>"
        a = FancyArrowPatch(
            p1, p2,
            arrowstyle=style, color=color, linewidth=lw,
            linestyle="--" if dashed else "-",
            connectionstyle="arc3,rad=0", mutation_scale=10,
            shrinkA=0, shrinkB=0, zorder=2)
        ax.add_patch(a)
        if lbl:
            mx = (p1[0] + p2[0]) / 2 + loff[0]
            my = (p1[1] + p2[1]) / 2 + loff[1]
            ax.text(mx, my, lbl, ha=lbl_ha, va=lbl_va,
                    fontsize=lbl_fs, color=LABEL_COL, zorder=6)

    # ==================================================================
    #  COLUMN X-CENTRES & HEADINGS
    # ==================================================================
    cx1, cx2, cx3, cx4, cx5 = 3.0, 9.0, 16.0, 22.5, 28.5
    # ==================================================================
    #  BOXES WIDTHS & HEIGHTS
    # ==================================================================
    w1, h1 = 3.8, 1.4
    w2, h2 = 3.8, 1.4
    w3, h3 = 4.6, 1.4
    w4, h4 = 3.8, 1.3
    w5, h5 = 5.0, 1.4

    heading_y = 12.0
    headings = [
        (cx1, "INPUT DATA", w1),
        (cx2, "SLURM SCHEDULER", w2),
        (cx3, "HPCRoseDetector CLASS", w3),
        (cx4, "H100 GPU WORKERS", w4),
        (cx5, "output and metrics", 6.0) # w5 will be evaluated later, hardcode for now
    ]
    
    for cx, txt, hw in headings:
        label(cx, heading_y, txt, fs=12, weight="bold")
        # Horizontal line below heading (dynamically matches box width)
        ax.plot([cx - hw/2 - 0.1, cx + hw/2 + 0.1], [heading_y - 0.3, heading_y - 0.3], 
                color=EDGE_COL, lw=1.5, zorder=2)

    # ==================================================================
    #  Y COORDINATES (Aligned perfectly with image)
    # ==================================================================
    y_r1 = 10.5  # Row 1 (top)
    y_r2 = 8.5   # Row 2
    y_r3 = 6.4   # Row 3
    y_r4 = 4.3   # Row 4
    y_r5 = 2.2   # Row 5

    # ==================================================================
    #  BOXES (Draw logic)
    # ==================================================================
    # COL 1: INPUT DATA
    b_uav = box(cx1, y_r1, w1, h1, 
                "UAV Seasonal Dataset\n3,000+ orthomosaics\n300-acre nursery, 2.5cm GSD", C_IN)
    b_sfs = box(cx1, y_r2, w1, h1, 
                "Shared File System\n/scratch/tacc/images/\nbatch_manifest_file", C_IN)
    b_venv = box(cx1, y_r3, w1, h1, 
                 "Python 3.9.18 venv\nCUDA enabled env\nDependencies pre-loaded", C_IN)

    # COL 2: SLURM
    # Job Script needs to be a bit taller for 4 lines of text
    b_slurm = box(cx2, y_r1 - 0.1, w2, 1.6, 
                  "SLURM Job Script\n#SBATCH --partition=gpu\n#SBATCH --nodes=1-4\n#SBATCH --gres=gpu:h100", C_SL)
    b_queue = box(cx2, y_r2 - 0.2, w2, h2, 
                  "Job Queue & Scheduling\nStampede5 H100 nodes\nPriority queue allocation", C_SL)
    b_work = box(cx2, y_r3 - 0.3, w2, h2, 
                 "Worker Allocation\n1 - 4 parallel workers\nOptimal: 1.75 workers", C_SL)

    # COL 3: HPC
    b_run = box(cx3, y_r1 - 0.3, w3, 1.5, 
                "HPCRoseDetector.run()\nOrchestrator class, Python 3.9.18\nCUDA-accelerated, batch_size=16", C_HPC)
    b_tile = box(cx3, y_r2 - 0.4, w3, h3, 
                 "Image Tile Generator\n512x512 patches, 64px overlap\n~100 tiles per orthomosaic", C_HPC)
    b_cv = box(cx3, y_r3 - 0.5, w3, h3, 
               "CV Detection Engine\nHSV -> DBSCAN -> Morphology\nBloom count N per tile", C_HPC)
    b_trig = box(cx3, y_r4 - 0.5, w3, h3, 
                 "LLM Trigger Logic\nIF N >= 10-15: invoke Ollama\nELSE: skip tile (save compute)", C_TRG)
    b_prmpt = box(cx3, y_r5 - 0.5, w3, h3, 
                  "Prompt Builder\nBloom count, density, heatmap\n-> structured advisory request", C_TRG)

    # COL 4: GPU
    b_node = box(cx4, y_r1, w4, h4, 
                 "H100 GPU Node\n80GB HBM3, 3.35 TB/s\nCUDA 12.x, NVLink", C_SL)
    b_ollama = box(cx4, y_r2, w4, h4, 
                   "Ollama Server\n127.0.0.1:11434\n90s timeout, triple-retry", C_GRN)
    b_mist = box(cx4, y_r3 + 0.5, w4, 1.1, 
                 "Mistral 7B\n1.15 ms, 4.46 GB", C_GRN)
    b_gemma = box(cx4, y_r4 + 0.6, w4, 1.1, 
                  "Gemma3\n8.88 ms, 3.3 GB", C_GRN)
    b_llama = box(cx4, y_r5 + 0.7, w4, 1.1, 
                  "Llama3.1 8B\n1.29 ms, 4.80 GB", C_GRN)

    # COL 5: OUTPUTS (Align exactly with LLMs)
    # They are slightly taller to fit all text
    out_w, out_h = w5, 1.3
    b_out1 = box(cx5, b_mist["cy"], out_w, out_h, 
                 "Model Output Dirs\n/mistral/, /gemma3/, /llama3/\nbbox, heatmap, report", C_GRN)
    b_out2 = box(cx5, b_gemma["cy"], out_w, out_h, 
                 "7-Dim Metrics CSV\nlatency, memory, quality\nthroughput, efficiency, success", C_GRN)
    b_out3 = box(cx5, b_llama["cy"], out_w, out_h, 
                 "Scaling Analysis\nStrong: peak 1.75 workers\nWeak: linear throughput", C_GRN)
    
    # Advisory Reports is 4 lines, needs more height
    b_out4 = box(cx5, b_llama["cy"] - 1.7, out_w, 1.6, 
                 "Advisory Reports\nbloom counts - plant density per zone\nyield estimate - spray schedule\nprecision agriculture recommendations", C_GRN)


    # ==================================================================
    #  ARROWS (Direct, elbow, etc. tracking the reference image exactly)
    # ==================================================================

    # -- Internal Column Connections --
    # COL 1
    # UAV to Shared FS is an arrow going down, no label
    arr(b_uav["b"], b_sfs["t"])
    arr(b_sfs["b"], b_venv["t"], lbl="env", loff=(0.2, 0), lbl_ha="left")

    # COL 2
    arr(b_slurm["b"], b_queue["t"], lbl="submit", loff=(0.2, 0), lbl_ha="left")
    arr(b_queue["b"], b_work["t"], lbl="dispatch", loff=(0.2, 0), lbl_ha="left")

    # COL 3
    arr(b_run["b"], b_tile["t"], lbl="tiles", loff=(0.2, 0), lbl_ha="left")
    arr(b_tile["b"], b_cv["t"], lbl="detect", loff=(0.2, 0), lbl_ha="left")
    arr(b_cv["b"], b_trig["t"], lbl="N count", loff=(0.2, 0), lbl_ha="left")
    arr(b_trig["b"], b_prmpt["t"], lbl="YES branch", loff=(0.2, 0), lbl_ha="left")

    # COL 4
    arr(b_node["b"], b_ollama["t"], lbl="CUDA", loff=(0.2, 0), lbl_ha="left")
    arr(b_ollama["b"], b_mist["t"])
    arr(b_mist["b"], b_gemma["t"])
    arr(b_gemma["b"], b_llama["t"])


    # -- Cross-Column Connections --
    
    # "loaded by job": From SLURM (left) LEFT, DOWN, LEFT to Shared FS (right)
    slurm_lt = b_slurm["l"]
    sfs_rt = b_sfs["r"]
    mid_x_1 = 6.2
    arr(slurm_lt, (mid_x_1, slurm_lt[1]), headless=True)
    arr((mid_x_1, slurm_lt[1]), (mid_x_1, sfs_rt[1]), headless=True)
    arr((mid_x_1, sfs_rt[1]), sfs_rt)
    label(5.8, sfs_rt[1] + 0.1, "loaded\nby job", ha="center", va="bottom", fs=10, weight="normal")

    # "Uses env": From Python venv (right) RIGHT, UP, RIGHT to SLURM (left)
    venv_rt = b_venv["r"]
    mid_x_2 = 5.4
    dest_y_slurm = b_slurm["cy"] - 0.4 # Enter low on the left edge
    arr(venv_rt, (mid_x_2, venv_rt[1]), headless=True)
    arr((mid_x_2, venv_rt[1]), (mid_x_2, dest_y_slurm), headless=True)
    arr((mid_x_2, dest_y_slurm), (b_slurm["l"][0], dest_y_slurm))
    label(6.6, dest_y_slurm + 0.1, "Uses\nenv", ha="center", va="bottom", fs=10, weight="normal")

    # "orchestrate": SLURM (right) to HPC Run (left)
    arr(b_slurm["r"], (b_run["l"][0], b_slurm["cy"]), lbl="orchestrate", loff=(0, 0.2), lbl_va="bottom", lbl_fs=10)

    # "reserve node": Dashed, from SLURM (top) UP, RIGHT, DOWN to H100 (top)
    sl_top = b_slurm["t"]
    hn_top = b_node["t"]
    res_y = 11.2 # Lowered below horizontal line at 11.7
    arr(sl_top, (sl_top[0], res_y), dashed=True, headless=True)
    arr((sl_top[0], res_y), (hn_top[0], res_y), dashed=True, headless=True)
    arr((hn_top[0], res_y), hn_top, dashed=True)
    label((sl_top[0] + hn_top[0]) / 2, res_y + 0.1, "reserve mode", va="bottom", weight="normal", fs=10)

    # Worker Allocation to HPC Run: RIGHT, UP, RIGHT into bottom corner of HPC Run
    wk_rt = b_work["r"]
    hpc_pt = (b_run["l"][0], b_run["cy"] - 0.4)
    arr(wk_rt, (wk_rt[0] + 0.4, wk_rt[1]), headless=True)
    arr((wk_rt[0] + 0.4, wk_rt[1]), (wk_rt[0] + 0.4, hpc_pt[1]), headless=True)
    arr((wk_rt[0] + 0.4, hpc_pt[1]), hpc_pt)

    # "read images": Job Queue (right) RIGHT, DOWN, RIGHT to Image Tile Gen (left)
    queue_rt = b_queue["r"]
    tile_lt = b_tile["l"]
    
    pass_x = (b_queue["r"][0] + b_tile["l"][0]) / 2 - 0.5
    arr(queue_rt, (pass_x, queue_rt[1]), headless=True)
    arr((pass_x, queue_rt[1]), (pass_x, tile_lt[1]), headless=True)
    arr((pass_x, tile_lt[1]), tile_lt)
    label((pass_x + tile_lt[0]) / 2, tile_lt[1] + 0.1, "read images", ha="center", va="bottom", fs=10, weight="normal")

    # NO: tile discarded: Dashed LEFT from LLM Trigger Logic
    trig_lt = b_trig["l"]
    no_end = (trig_lt[0] - 2.5, trig_lt[1]) # Stretch dashed line 2.5 units left
    arr(trig_lt, (trig_lt[0] - 0.5, trig_lt[1]), dashed=True, headless=True)
    arr((trig_lt[0] - 0.5, trig_lt[1]), (trig_lt[0] - 0.5, trig_lt[1] - 0.6), dashed=True, headless=True)
    arr((trig_lt[0] - 0.5, trig_lt[1] - 0.6), (no_end[0], trig_lt[1] - 0.6), dashed=True)
    label((trig_lt[0] - 0.5 + no_end[0]) / 2, trig_lt[1] - 0.6 + 0.1, "NO: tile discarded", ha="center", va="bottom", fs=10, weight="normal")
    
    # "prompt": Prompt Builder (right) RIGHT, UP, RIGHT to Ollama (left)
    prmpt_rt = b_prmpt["r"]
    oll_lt = b_ollama["l"]
    prompt_x = prmpt_rt[0] + 0.8
    arr(prmpt_rt, (prompt_x, prmpt_rt[1]), headless=True)
    arr((prompt_x, prmpt_rt[1]), (prompt_x, oll_lt[1]), headless=True)
    arr((prompt_x, oll_lt[1]), oll_lt)
    label((prompt_x + oll_lt[0]) / 2, oll_lt[1] + 0.1, "prompt", ha="center", va="bottom", fs=10, weight="normal")


    # -- 12 Criss-Cross Arrows --
    llms = [b_mist, b_gemma, b_llama]
    outputs = [b_out1, b_out2, b_out3, b_out4]
    
    for llm in llms:
        for out in outputs:
            arr(llm["r"], out["l"], color=EDGE_COL, lw=1.0) # Black arrows for the bundle

    # "sequential dispatch" label above the bundle
    label((b_mist["r"][0] + b_out1["l"][0]) / 2, b_mist["cy"] + 0.6, "sequential\ndispatch", fs=10, weight="normal")

    # -- Scaling Results Feedback --
    # Dashed, from Advisory Reports (bottom) DOWN, LEFT, UP to Worker Allocation (bottom)
    adv_bot = b_out4["b"]
    work_bot = b_work["b"]
    fb_y = 0.5
    arr(adv_bot, (adv_bot[0], fb_y), dashed=True, headless=True, color=EDGE_COL)
    arr((adv_bot[0], fb_y), (work_bot[0], fb_y), dashed=True, headless=True, color=EDGE_COL)
    arr((work_bot[0], fb_y), work_bot, dashed=True, color=EDGE_COL)
    label((adv_bot[0] + work_bot[0]) / 2, fb_y + 0.1, "scaling results inform worker allocation", fs=10, va="bottom", weight="normal")


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

