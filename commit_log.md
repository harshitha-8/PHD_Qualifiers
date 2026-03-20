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

