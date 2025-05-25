# Thesis Repository: Sketch Maps as a Tool for Learning New Environments

This repository contains the data and Python scripts used in the Master’s thesis titled  
**"Sketch Maps as a Tool for Learning New Environments"**, submitted in partial fulfillment of the M.Sc. in Geoinformatics and Spatial Data Science at the University of Münster.

## 📁 Contents

### Data Files

- `anonymous_map_data/`  
  Anonymized participant data for each map (Map 1 and Map 2), collected during the within-subjects experiment.
  
- `Paired data.xlsx`  
  A combined dataset aggregating participant performance across both conditions (sketch map and verbal description).  
  This file was used in **JASP** for statistical analysis and generation of correlation matrices.

### Python Scripts

- `create_plots.py`  
  Generates all figures used in the thesis, including:
  - Box and strip plots for task performance
  - Task comparison visualizations across conditions and map types

- `task1.py`  
  Calculates scores for **Task 1: Sequence Ordering**, using Spearman’s rank correlation to measure recall accuracy of landmark sequences.

## 🧪 Study Overview

The thesis explored whether sketch mapping supports spatial learning better than verbal description after navigating immersive routes. A within-subjects experiment with 23 participants assessed spatial recall through:

1. **Sequence Ordering** – landmark recall in correct order  
2. **Distance Estimation** – comparison of landmark pair distances  
3. **Direction Estimation** – pointing task to estimate landmark directions

Participants completed both conditions across two different map environments.

## 🚀 Running the Scripts

Make sure the working directory includes the required data files.

To generate plots:
```bash
python create_plots.py
```

To calculate Task 1 (Sequence Ordering) scores:
```bash
python task1.py
```