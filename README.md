# Crash Severity Prediction for Emergency Dispatch

[![DOI](https://zenodo.org/badge/1228289570.svg)](https://doi.org/10.5281/zenodo.20434482)

## Abstract

This repository contains the Data Stewardship 2026 Part 3 open-science
experiment for predicting road collision casualty severity from scene conditions
that may be known during or shortly after an emergency call. The experiment uses
the 2023 UK Road Safety Open Data (STATS19) published by the UK Department for
Transport and models the target as a three-class classification problem:
`Fatal`, `Serious`, or `Slight`.

The reproducible workflow prepares linked collision, vehicle, and casualty
records; exposes query-ready DBRepo views; trains a scikit-learn Random Forest
classifier; evaluates the model on a held-out test split; and documents the
experiment with RO-Crate, CodeMeta, Croissant, FAIR4ML, and model-card metadata.
The features used by the model are road type, speed limit, weather conditions,
light conditions, road surface conditions, day of week, hour of day, number of
vehicles, and vehicle type.

## Requirements And Installation

The project is implemented in Python and SQL. A DBRepo connection is required
for the final reproducible pipeline because the training and evaluation scripts
load data from DBRepo views rather than local CSV files.

Required software:

- Python 3
- pip
- Jupyter Notebook or JupyterLab for the notebooks in `src/notebooks/`
- Access to the TU Wien DBRepo test instance used by the group

Install the Python dependencies from the repository root:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On macOS or Linux, activate the environment with:

```bash
source .venv/bin/activate
```

The pinned Python dependencies are listed in `requirements.txt`:

- `pandas==3.0.3`
- `requests==2.34.2`
- `numpy==2.4.6`
- `scikit-learn==1.8.0`
- `joblib==1.5.3`
- `matplotlib==3.10.9`
- `seaborn==0.13.2`
- `python-dotenv==1.2.2`
- `dbrepo==1.13.5`

Create a local `.env` file for DBRepo credentials. This file must not be
committed. The scripts expect these variables:

```text
DBREPO_API_BASE=<DBRepo REST API base URL>
DBREPO_DB_ID=<DBRepo database UUID>
DBREPO_USER=<DBRepo username>
DBREPO_PASSWORD=<DBRepo password>
```

## Repository Structure

```text
.
|-- data/
|   |-- raw/             # Original STATS19 input tables
|   |-- interim/         # Joined intermediate feature table
|   `-- processed/       # Train, validation, and test splits
|-- docs/
|   |-- reference/       # Assignment document
|   |-- use-case/        # Selected use-case description
|   |-- validation/      # Validation outputs
|   |-- croissant.json   # Croissant metadata for input datasets
|   |-- fair4ml-model-random-forest-severity-2023-v1.jsonld
|   `-- model-cards/     # Model Card documentation
|-- outputs/
|   |-- figures/         # Generated plots and visual diagnostics
|   |-- models/          # Trained model artefacts
|   `-- reports/         # Metrics and prediction reports
|-- src/
|   |-- notebooks/       # DBRepo, semantic, unit, and exploration notebooks
|   |-- scripts/         # Reproducible processing, training, and evaluation
|   |-- sql/             # SQL schema, views, and ER diagram
|   `-- utils/           # Shared DBRepo API helper
|-- CITATION.cff         # Citation metadata referencing the Zenodo DOI
|-- codemeta.json        # CodeMeta 2.0 software metadata
|-- requirements.txt     # Pinned Python dependencies
`-- ro-crate-metadata.json
```

## File Organisation

Files use lowercase kebab-case names with semantic parts separated by hyphens.
Where useful, file names include source, topic, year, processing stage, and
version:

```text
<source>-<topic>-<year>-<stage>-v<major>.<extension>
```

Input and derived data use stages such as `raw`, `interim`, and `processed`.
Figures use `fig-<analysis-topic>-<year>-v<major>.png`. Evaluation reports use
`report-<metric-or-scope>-<year>-v<major>.<extension>`. Model artefacts use
`model-<algorithm>-<target>-<year>-v<major>.pkl`. Scripts use a numeric prefix
that reflects the execution order.

## Inputs

The input data comes from the UK Department for Transport STATS19 2023 road
safety open dataset. The source dataset is available from:

https://www.gov.uk/government/statistical-data-sets/road-safety-open-data

Input files in this repository:

| Path | Description | Licence |
|------|-------------|---------|
| `data/raw/stats19-collision-2023-raw-v1.csv` | Collision-level STATS19 records with location, road, time, weather, lighting, and severity context. | Open Government Licence v3.0 |
| `data/raw/stats19-vehicle-2023-raw-v1.csv` | Vehicle-level STATS19 records linked to collisions. | Open Government Licence v3.0 |
| `data/raw/stats19-casualty-2023-raw-v1.csv` | Casualty-level STATS19 records containing the prediction target `casualty_severity`. | Open Government Licence v3.0 |
| `data/interim/stats19-collision-vehicle-casualty-2023-interim-v1.csv` | Intermediate joined table derived from collision, vehicle, and casualty records. | Open Government Licence v3.0 |
| `data/processed/stats19-features-train-2023-processed-v1.csv` | Training split used for fitting the Random Forest classifier. | Open Government Licence v3.0 |
| `data/processed/stats19-features-val-2023-processed-v1.csv` | Validation split used during model development. | Open Government Licence v3.0 |
| `data/processed/stats19-features-test-2023-processed-v1.csv` | Held-out test split used for final evaluation. | Open Government Licence v3.0 |

## Outputs

Generated outputs are stored under `outputs/`.

| Path | Description | Licence |
|------|-------------|---------|
| `outputs/models/model-random-forest-severity-2023-v1.pkl` | Trained Random Forest model artefact produced by `src/scripts/04-train.py`. | CC BY 4.0 |
| `outputs/reports/report-classification-metrics-2023-v1.csv` | Precision, recall, F1-score, support, accuracy, macro average, and weighted average metrics for the test split. | CC BY 4.0 |
| `outputs/reports/report-predictions-test-2023-v1.csv` | Test-set features with actual and predicted casualty severity labels. | CC BY 4.0 |
| `outputs/figures/fig-confusion-matrix-2023-v1.png` | Confusion matrix for the held-out test split. | CC BY 4.0 |
| `outputs/figures/fig-feature-importance-2023-v1.png` | Random Forest feature-importance chart. | CC BY 4.0 |
| `outputs/figures/fig-severity-distribution-2023-v1.png` | Distribution of casualty severity classes. | CC BY 4.0 |
| `outputs/figures/fig-hist-day_of_week-2023-v1.png` | Histogram for day of week. | CC BY 4.0 |
| `outputs/figures/fig-hist-light_conditions-2023-v1.png` | Histogram for light conditions. | CC BY 4.0 |
| `outputs/figures/fig-hist-number_of_vehicles-2023-v1.png` | Histogram for number of vehicles. | CC BY 4.0 |
| `outputs/figures/fig-hist-road_surface_conditions-2023-v1.png` | Histogram for road surface conditions. | CC BY 4.0 |
| `outputs/figures/fig-hist-road_type-2023-v1.png` | Histogram for road type. | CC BY 4.0 |
| `outputs/figures/fig-hist-speed_limit-2023-v1.png` | Histogram for speed limit. | CC BY 4.0 |
| `outputs/figures/fig-hist-vehicle_type-2023-v1.png` | Histogram for vehicle type. | CC BY 4.0 |
| `outputs/figures/fig-hist-weather_conditions-2023-v1.png` | Histogram for weather conditions. | CC BY 4.0 |

The current test-set metrics are:

| Metric | Value |
|--------|------:|
| Accuracy | 0.6298 |
| Weighted F1-score | 0.6407 |
| Macro F1-score | 0.3950 |
| Fatal F1-score | 0.0495 |
| Serious F1-score | 0.3884 |
| Slight F1-score | 0.7470 |

## Metadata Artefacts

The repository includes the following documentation and metadata artefacts:

| Path | Standard / Purpose |
|------|--------------------|
| `ro-crate-metadata.json` | RO-Crate metadata describing the experiment package, datasets, scripts, outputs, authors, licences, and relationships. |
| `codemeta.json` | CodeMeta 2.0 metadata for the software component, including dependencies and repository URL. |
| `docs/croissant.json` | Croissant JSON-LD metadata for the input datasets, including fields, data types, units, distribution information, and licence. |
| `docs/fair4ml-model-random-forest-severity-2023-v1.jsonld` | FAIR4ML metadata for the trained Random Forest model, including hyperparameters, datasets, evaluation metrics, intended use, and limitations. |
| `docs/model-cards/model-card-model-random-forest-severity-2023-v1.md` | Model Card for the trained model. |
| `docs/validation/RO-Crate-Validation-Report.txt` | RO-Crate validation output. |
| `CITATION.cff` | Citation metadata for the GitHub-Zenodo archived repository. |

## DBRepo Schema And Views

The relational schema is defined in:

- `src/sql/01_collision.sql`
- `src/sql/02_vehicle.sql`
- `src/sql/03_casualty.sql`

The entity-relationship diagram is stored at `src/sql/ER-Diagram.png`.

The query-ready views are defined in `src/sql/04_views.sql`, with a
MariaDB-compatible version in `src/sql/04_views_mariadb.sql`.

| View | Purpose |
|------|---------|
| `v_ml_features` | Main feature table for model training; one row per casualty with scene-condition features and the target label. |
| `v_severity_distribution` | Class distribution of casualty severity with counts and percentages. |
| `v_collision_summary` | One row per collision with aggregated severity and scene conditions. |
| `v_feature_null_check` | Null-value counts for ML feature columns. |

The scripts also expect split-specific DBRepo views for training, validation,
and testing. The accepted candidate names are:

- training: `v_features_train`, `v_ml_features_train`, `ml_features_train`, `features_train`
- validation: `v_features_val`, `v_ml_features_val`, `ml_features_val`, `features_val`
- testing: `v_features_test`, `v_ml_features_test`, `ml_features_test`, `features_test`

## Step-By-Step Reproduction

Run all commands from the repository root.

1. Install dependencies and configure DBRepo credentials as described in
   [Requirements And Installation](#requirements-and-installation).

2. Create the DBRepo database schema and load the source data using the DBRepo
   notebooks:

   ```text
   src/notebooks/dbrepo_schema.ipynb
   src/notebooks/dbrepo_load_verify.ipynb
   src/notebooks/dbrepo_create_views.ipynb
   ```

   The schema SQL files and views in `src/sql/` document the database structure
   and the query-ready subsets used by the pipeline.

3. Record semantic mappings and unit mappings:

   ```text
   src/notebooks/semantic_mapping.ipynb
   src/notebooks/unit_mapping.ipynb
   ```

4. Fetch the DBRepo feature view into the local interim file:

   ```bash
   python src/scripts/01-load-merge.py
   ```

5. Explore the interim data and regenerate exploratory figures:

   ```text
   src/notebooks/02-explore.ipynb
   ```

6. Prepare model features and create train, validation, and test splits:

   ```bash
   python src/scripts/03-prepare-features.py
   ```

7. Train the Random Forest classifier:

   ```bash
   python src/scripts/04-train.py
   ```

   This writes `outputs/models/model-random-forest-severity-2023-v1.pkl`.

8. Evaluate the trained model:

   ```bash
   python src/scripts/05-evaluate.py
   ```

   This writes the classification report, prediction report, confusion matrix,
   and feature-importance figure under `outputs/`.

9. Optionally compare DBRepo API results with the local processed splits:

   ```bash
   python src/scripts/verify_api_matches_local.py
   ```

10. Validate metadata artefacts before publication:

   - Validate `ro-crate-metadata.json` with `ro-crate-validator`.
   - Check `codemeta.json` against the CodeMeta 2.0 schema.
   - Check `docs/croissant.json` as Croissant JSON-LD.
   - Review `docs/fair4ml-model-random-forest-severity-2023-v1.jsonld`.

## Contributors

| Role | Name | ORCID |
|------|------|-------|
| A | Sebastian Schnitzer | https://orcid.org/0009-0009-5014-2131 |
| B | Maxime Philippon | https://orcid.org/0009-0003-2394-5285 |
| C | Maximillian Seiringer | https://orcid.org/0009-0008-4198-6693 |
| D | Anton Windsperger | https://orcid.org/0009-0008-9353-7427 |

## Citation

If you use or refer to this repository, cite the archived Zenodo record:

```text
Schnitzer, S., Philippon, M., Seiringer, M., & Windsperger, A. (2026).
Crash Severity Prediction for Emergency Dispatch (Version 1.0.0).
Zenodo. https://doi.org/10.5281/zenodo.20434482
```

The machine-readable citation metadata is available in `CITATION.cff`.

## Licences

This project uses different licences for the three relevant categories of
artefacts.

| Artefact category | Licence | Scope and obligations |
|-------------------|---------|-----------------------|
| Input data | Open Government Licence v3.0 (OGL-UK-3.0) | Applies to the original and derived STATS19 data. Reuse, copying, publication, distribution, and adaptation are permitted, including commercial use, provided the source is acknowledged. |
| Software / code | MIT License | Applies to Python scripts, notebooks, SQL files, and supporting software metadata in this repository. Reuse, modification, distribution, and commercial use are permitted if the copyright and licence notice are preserved. |
| Produced / output data | Creative Commons Attribution 4.0 International (CC BY 4.0) | Applies to trained model artefacts, generated datasets, figures, prediction reports, and evaluation reports. Reuse and adaptation are permitted with appropriate attribution. |

The MIT software licence was selected because it is permissive and compatible
with the OGL-UK-3.0 input data licence. CC BY 4.0 was selected for produced
research outputs because it supports broad reuse while preserving attribution.

## References

- Assignment: `docs/reference/2026-dast-exercise-part3-assignment.pdf`
- Selected use case: `docs/use-case/12226609-use-case-description.pdf`
- UK Road Safety Open Data: https://www.gov.uk/government/statistical-data-sets/road-safety-open-data
- GitHub repository: https://github.com/maxi-seiringer/dast-2026-crash-severity-prediction
- Zenodo DOI: https://doi.org/10.5281/zenodo.20434482
