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

## References

- Assignment: `docs/reference/2026-dast-exercise-part3-assignment.pdf`
- Selected use case: `docs/use-case/12226609-use-case-description.pdf`
