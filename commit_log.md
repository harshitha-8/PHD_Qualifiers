# PHD Qualifiers - Development Log

This file tracks iterative development progress on the CV → LLM Pipeline Architecture diagram
and related research materials for the PhD Qualifying Examination.

---

Starting 150 commits at Fri Mar 20 17:43:00 CDT 2026

### Commit 1 / 150
- **Time:** 2026-03-20 17:43:00
- **Change:** refactor: extract CV pipeline constants into config section

### Commit 2 / 150
- **Time:** 2026-03-20 17:44:01
- **Change:** docs: add UAV orthomosaic capture parameters

### Commit 3 / 150
- **Time:** 2026-03-20 17:45:02
- **Change:** style: adjust RGB preprocessing box dimensions

### Commit 4 / 150
- **Time:** 2026-03-20 17:46:03
- **Change:** feat: add GSD resolution annotation to UAV node

### Commit 5 / 150
- **Time:** 2026-03-20 17:47:04
- **Change:** docs: document 80% overlap requirement for stitching

### Commit 6 / 150
- **Time:** 2026-03-20 17:48:05
- **Change:** refactor: parameterize tile size (512x512)

### Commit 7 / 150
- **Time:** 2026-03-20 17:49:07
- **Change:** docs: add HSV transform threshold rationale

### Commit 8 / 150
- **Time:** 2026-03-20 17:50:08
- **Change:** style: improve hue range notation readability

### Commit 9 / 150
- **Time:** 2026-03-20 17:51:09
- **Change:** feat: add DBSCAN epsilon calculation note

### Commit 10 / 150
- **Time:** 2026-03-20 17:52:10
- **Change:** docs: document MinPts=8 clustering parameter

### Commit 11 / 150
- **Time:** 2026-03-20 17:53:11
- **Change:** refactor: centralize color palette definitions

### Commit 12 / 150
- **Time:** 2026-03-20 17:54:12
- **Change:** style: adjust morphological refinement box sizing

### Commit 13 / 150
- **Time:** 2026-03-20 17:55:13
- **Change:** docs: add elliptical kernel dimension justification

### Commit 14 / 150
- **Time:** 2026-03-20 17:56:14
- **Change:** feat: annotate area filter range [200-8000] px

### Commit 15 / 150
- **Time:** 2026-03-20 17:57:15
- **Change:** docs: add bloom detection algorithm description

### Commit 16 / 150
- **Time:** 2026-03-20 17:58:16
- **Change:** refactor: extract decision threshold as constant

### Commit 17 / 150
- **Time:** 2026-03-20 17:59:18
- **Change:** docs: document N>=10-15 bloom threshold selection

### Commit 18 / 150
- **Time:** 2026-03-20 18:00:19
- **Change:** style: improve decision diamond proportions

### Commit 19 / 150
- **Time:** 2026-03-20 18:01:20
- **Change:** feat: add skip-tile logic annotation

### Commit 20 / 150
- **Time:** 2026-03-20 18:02:21
- **Change:** docs: describe structured prompt template format

### Commit 21 / 150
- **Time:** 2026-03-20 18:03:23
- **Change:** refactor: modularize prompt engineering section

### Commit 22 / 150
- **Time:** 2026-03-20 18:04:24
- **Change:** docs: add bloom count integration details

### Commit 23 / 150
- **Time:** 2026-03-20 18:05:25
- **Change:** feat: annotate density heatmap generation

### Commit 24 / 150
- **Time:** 2026-03-20 18:06:26
- **Change:** docs: document growth stage classification

### Commit 25 / 150
- **Time:** 2026-03-20 18:07:28
- **Change:** style: adjust Ollama server box layout

### Commit 26 / 150
- **Time:** 2026-03-20 18:08:29
- **Change:** docs: add 127.0.0.1:11434 endpoint documentation

### Commit 27 / 150
- **Time:** 2026-03-20 18:09:31
- **Change:** feat: document zero-cloud deployment strategy

### Commit 28 / 150
- **Time:** 2026-03-20 18:10:32
- **Change:** docs: add 90s timeout configuration rationale

### Commit 29 / 150
- **Time:** 2026-03-20 18:11:33
- **Change:** refactor: add triple-retry mechanism description

### Commit 30 / 150
- **Time:** 2026-03-20 18:12:34
- **Change:** docs: document Mistral 7B model characteristics

### Commit 31 / 150
- **Time:** 2026-03-20 18:13:35
- **Change:** feat: add latency measurement (1127ms) for Mistral

### Commit 32 / 150
- **Time:** 2026-03-20 18:14:42
- **Change:** docs: document 4.4GB memory footprint for Mistral

### Commit 33 / 150
- **Time:** 2026-03-20 18:15:43
- **Change:** docs: describe real-time advisory use case

### Commit 34 / 150
- **Time:** 2026-03-20 18:16:44
- **Change:** docs: document Gemma3 model selection rationale

### Commit 35 / 150
- **Time:** 2026-03-20 18:17:45
- **Change:** feat: add Gemma3 latency benchmark (8882ms)

### Commit 36 / 150
- **Time:** 2026-03-20 18:18:46
- **Change:** docs: document 3.3GB memory profile for Gemma3

### Commit 37 / 150
- **Time:** 2026-03-20 18:19:48
- **Change:** docs: describe edge deployment scenario

### Commit 38 / 150
- **Time:** 2026-03-20 18:20:49
- **Change:** docs: document Llama3.1 8B model integration

### Commit 39 / 150
- **Time:** 2026-03-20 18:21:50
- **Change:** feat: add Llama3.1 latency measurement (1294ms)

### Commit 40 / 150
- **Time:** 2026-03-20 18:22:51
- **Change:** docs: document 4.9GB memory allocation for Llama3.1

### Commit 41 / 150
- **Time:** 2026-03-20 18:23:53
- **Change:** docs: describe batch analytics pipeline

### Commit 42 / 150
- **Time:** 2026-03-20 18:24:54
- **Change:** refactor: reorganize evaluation metrics section

### Commit 43 / 150
- **Time:** 2026-03-20 18:25:55
- **Change:** docs: add harvest timing metric description

### Commit 44 / 150
- **Time:** 2026-03-20 18:26:56
- **Change:** feat: document spray schedule output format

### Commit 45 / 150
- **Time:** 2026-03-20 18:29:41
- **Change:** docs: add yield estimate calculation method

### Commit 46 / 150
- **Time:** 2026-03-20 18:30:42
- **Change:** docs: describe 7-dim evaluation metric space

### Commit 47 / 150
- **Time:** 2026-03-20 18:31:43
- **Change:** feat: add latency metric collection details

### Commit 48 / 150
- **Time:** 2026-03-20 18:32:45
- **Change:** docs: document memory profiling methodology

### Commit 49 / 150
- **Time:** 2026-03-20 18:33:46
- **Change:** docs: add quality assessment metric definition

### Commit 50 / 150
- **Time:** 2026-03-20 18:34:47
- **Change:** docs: describe throughput measurement approach

### Commit 51 / 150
- **Time:** 2026-03-20 18:35:48
- **Change:** style: standardize font family to Tahoma

### Commit 52 / 150
- **Time:** 2026-03-20 18:36:49
- **Change:** refactor: unify arrow styling across diagram

### Commit 53 / 150
- **Time:** 2026-03-20 18:37:50
- **Change:** style: ensure consistent arrow head sizes

### Commit 54 / 150
- **Time:** 2026-03-20 18:38:51
- **Change:** refactor: remove redundant edge labels from CV row

### Commit 55 / 150
- **Time:** 2026-03-20 18:39:52
- **Change:** style: remove section divider lines for cleaner look

### Commit 56 / 150
- **Time:** 2026-03-20 18:40:53
- **Change:** refactor: increase spacing between CV pipeline boxes

### Commit 57 / 150
- **Time:** 2026-03-20 18:41:55
- **Change:** style: add proper gaps around arrow endpoints

### Commit 58 / 150
- **Time:** 2026-03-20 18:42:56
- **Change:** docs: add figure caption with pipeline summary

### Commit 59 / 150
- **Time:** 2026-03-20 18:43:57
- **Change:** feat: generate 300 DPI PNG output

### Commit 60 / 150
- **Time:** 2026-03-20 18:44:58
- **Change:** feat: add PDF vector output for LaTeX inclusion

### Commit 61 / 150
- **Time:** 2026-03-20 18:45:59
- **Change:** docs: update README with diagram description

### Commit 62 / 150
- **Time:** 2026-03-20 18:47:00
- **Change:** refactor: clean up helper function signatures

### Commit 63 / 150
- **Time:** 2026-03-20 18:51:01
- **Change:** style: fine-tune box corner radius

### Commit 64 / 150
- **Time:** 2026-03-20 18:52:06
- **Change:** docs: add color palette documentation

### Commit 65 / 150
- **Time:** 2026-03-20 18:53:07
- **Change:** refactor: extract draw_box helper for reuse

### Commit 66 / 150
- **Time:** 2026-03-20 18:54:08
- **Change:** refactor: extract draw_diamond helper for reuse

### Commit 67 / 150
- **Time:** 2026-03-20 18:55:09
- **Change:** refactor: extract draw_arrow helper for reuse

### Commit 68 / 150
- **Time:** 2026-03-20 18:56:10
- **Change:** style: adjust connection curve radii

### Commit 69 / 150
- **Time:** 2026-03-20 18:57:11
- **Change:** docs: add matplotlib backend configuration note

### Commit 70 / 150
- **Time:** 2026-03-20 18:58:12
- **Change:** refactor: parameterize figure dimensions

### Commit 71 / 150
- **Time:** 2026-03-20 18:59:13
- **Change:** style: set white background for print compatibility

### Commit 72 / 150
- **Time:** 2026-03-20 19:00:15
- **Change:** docs: add font fallback chain documentation

### Commit 73 / 150
- **Time:** 2026-03-20 19:01:16
- **Change:** refactor: clean up import statements

### Commit 74 / 150
- **Time:** 2026-03-20 19:02:18
- **Change:** docs: document save path resolution logic

### Commit 75 / 150
- **Time:** 2026-03-20 19:03:19
- **Change:** feat: add dual-format output (PNG and PDF)

### Commit 76 / 150
- **Time:** 2026-03-20 19:04:21
- **Change:** style: adjust title font size to 13pt

### Commit 77 / 150
- **Time:** 2026-03-20 19:05:22
- **Change:** docs: add subtitle with pipeline scope

### Commit 78 / 150
- **Time:** 2026-03-20 19:06:23
- **Change:** refactor: organize code into logical sections

### Commit 79 / 150
- **Time:** 2026-03-20 19:07:24
- **Change:** style: fine-tune section header positioning

### Commit 80 / 150
- **Time:** 2026-03-20 19:08:25
- **Change:** docs: add CV pipeline stage descriptions

### Commit 81 / 150
- **Time:** 2026-03-20 19:09:26
- **Change:** refactor: use consistent coordinate system

### Commit 82 / 150
- **Time:** 2026-03-20 19:10:27
- **Change:** style: adjust bloom detection box placement

### Commit 83 / 150
- **Time:** 2026-03-20 19:11:29
- **Change:** docs: add structured output annotation

### Commit 84 / 150
- **Time:** 2026-03-20 19:12:30
- **Change:** refactor: parameterize decision diamond size

### Commit 85 / 150
- **Time:** 2026-03-20 19:13:31
- **Change:** style: improve NO branch dashed arrow

### Commit 86 / 150
- **Time:** 2026-03-20 19:14:32
- **Change:** docs: add YES branch template description

### Commit 87 / 150
- **Time:** 2026-03-20 19:15:33
- **Change:** refactor: centralize arrow mutation scale

### Commit 88 / 150
- **Time:** 2026-03-20 19:16:34
- **Change:** style: adjust prompt engineering box width

### Commit 89 / 150
- **Time:** 2026-03-20 19:17:35
- **Change:** docs: add prompt content field descriptions

### Commit 90 / 150
- **Time:** 2026-03-20 19:18:39
- **Change:** refactor: organize LLM model definitions

### Commit 91 / 150
- **Time:** 2026-03-20 19:19:40
- **Change:** style: highlight Llama3.1 with distinct color

### Commit 92 / 150
- **Time:** 2026-03-20 19:20:42
- **Change:** docs: add model comparison annotations

### Commit 93 / 150
- **Time:** 2026-03-20 19:21:43
- **Change:** refactor: compute arrow trajectories dynamically

### Commit 94 / 150
- **Time:** 2026-03-20 19:22:44
- **Change:** style: adjust evaluation box dimensions

### Commit 95 / 150
- **Time:** 2026-03-20 19:23:45
- **Change:** docs: rename output section to Evaluation Pipeline

### Commit 96 / 150
- **Time:** 2026-03-20 19:24:46
- **Change:** refactor: replace plus with and in output title

