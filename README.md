# Crash Severity Prediction for Emergency Dispatch

This repository contains the Data Stewardship 2026 Part 3 experiment setup for
predicting road collision severity from scene conditions that are likely to be
known at the time of an emergency call.

The selected use case is based on the 2023 UK Road Safety Open Data (STATS19)
published by the UK Department for Transport. The intended machine learning task
is a three-class severity prediction problem: slight, serious, or fatal. The
planned model is a Random Forest classifier trained on features such as road
type, speed limit, weather, lighting, road surface, time of day, day of week,
number of vehicles involved, and vehicle type.

## Repository structure

```text
.
|-- config/              # Configuration files for data processing and modelling
|-- data/                # Input and derived datasets
|   |-- raw/             # Original downloaded source files
|   |-- interim/         # Intermediate files created during processing
|   `-- processed/       # Final analysis-ready datasets
|-- docs/                # Assignment material, use-case notes, and project docs
|   |-- reference/       # Assignment/reference documents
|   `-- use-case/        # Selected use-case description
|-- outputs/             # Generated experiment outputs
|   |-- figures/         # Plots and visual diagnostics
|   |-- models/          # Trained model artefacts
|   `-- reports/         # Metrics, tables, and evaluation summaries
`-- src/                 # Reproducible scripts and notebooks
    |-- notebooks/       # Jupyter Notebooks
    |-- sql/             # SQL Create Scripts + Entity Relation Diagrams
    `-- dbrepo/          # Scripts to connect with DBRepo    
```

## File organisation

Use lowercase kebab-case file names with short semantic parts separated by
hyphens. Include the source, topic, year, processing stage, and version where
they help identify the file without opening it.

General pattern:

```text
<source>-<topic>-<year>-<stage>-v<major>.<extension>
```

Input datasets in `data/`:

- Raw STATS19 inputs keep their official names where possible, for example
  `dft-road-casualty-statistics-collision-2023.csv`.
- Derived datasets add a stage and version, for example
  `stats19-collision-vehicle-features-2023-processed-v1.csv`.
- Temporary or join outputs belong in `data/interim/`, for example
  `stats19-collision-vehicle-join-2023-interim-v1.csv`.

Output files in `outputs/`:

- Figures use `fig-<analysis-topic>-<year>-v<major>.png`, for example
  `fig-feature-importance-2023-v1.png`.
- Evaluation reports use `report-<metric-or-scope>-<year>-v<major>.<extension>`,
  for example `report-classification-metrics-2023-v1.csv`.
- Model artefacts use `model-<algorithm>-<target>-<year>-v<major>.pkl`, for
  example `model-random-forest-severity-2023-v1.pkl`.

Scripts and notebooks in `src/`:

- Scripts use a numeric execution prefix and action-oriented name, for example
  `01-download-stats19-data.py`, `02-prepare-features.py`, and
  `03-train-random-forest.py`.
- Notebooks follow the same prefix when they are part of the reproducible
  workflow, for example `01-explore-stats19-data.ipynb`.

Configuration files in `config/`:

- Configuration files use `config-<workflow-part>-v<major>.<extension>`, for
  example `config-random-forest-v1.yaml`.
- Local secrets or credentials must not be committed. Use environment variables
  or local files excluded by `.gitignore`.

## SQL Views

The views in `src/sql/04_views.sql` flatten the three raw tables 
(collision, vehicle, casualty) into query-ready formats for the ML pipeline.

| View | Purpose |
|------|---------|
| `v_ml_features` | Main feature table for model training – one row per casualty with all scene-condition features and the target label |
| `v_severity_distribution` | Class distribution of casualty severity with counts and percentages |
| `v_collision_summary` | One row per collision with aggregated severity and scene conditions |
| `v_feature_null_check` | Null value counts for all ML feature columns |

## Pipeline

**`01-load-merge.py`** – Loads the three raw STATS19 CSV files and merges them into one table.

**`02-explore.ipynb`** – Explores the data and saves one histogram per feature as a PNG file.

**`03-prepare-features.py`** – Cleans the data and splits it into train, validation, and test sets.

**`04-train.py`** – Trains a Random Forest Classifier and saves the model as a .pkl file.

**`05-evaluate.py`** – Runs the model on the test set and saves the confusion matrix, feature importance chart, and classification report.

## References

- Assignment: `docs/reference/2026-dast-exercise-part3-assignment.pdf`
- Selected use case: `docs/use-case/12226609-use-case-description.pdf`
