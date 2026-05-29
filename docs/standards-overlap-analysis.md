# Standards Overlap Analysis

## Scope

This analysis compares the five metadata standards used in the crash severity
prediction project:

- RO-Crate: `ro-crate-metadata.json`
- CodeMeta: `codemeta.json`
- FAIR4ML: `docs/fair4ml-model-random-forest-severity-2023-v1.jsonld`
- Croissant: `docs/croissant.json`
- Model Card: `docs/model-cards/model-card-model-random-forest-severity-2023-v1.md`

The comparison focuses on overlap and complementarity between the standards.
For each pair, the table identifies fields or concepts that appear in both,
fields that are unique to each standard in this project, and conflicts or
inconsistencies that should be considered when using the metadata together.

## Pairwise Comparison

| Pair of standards | Fields or concepts appearing in both | Fields unique to the first standard | Fields unique to the second standard | Conflicts or inconsistencies |
|---|---|---|---|---|
| RO-Crate and CodeMeta | Project/software name, description, version, authors, ORCIDs, licence, GitHub repository, programming language, dependencies, Zenodo DOI. | Experiment package structure, file inventory, datasets, model artefact, figures, reports, input/output relationships, per-file licences, source dataset relationship, validation file references. | Software-specific metadata such as `applicationCategory`, `issueTracker`, and a compact dependency list as `softwareRequirements`. | RO-Crate describes the whole experiment package, while CodeMeta describes the software component. The RO-Crate root licence is MIT even though individual data and output files use OGL-UK-3.0 or CC BY 4.0, so the per-file licences are more precise than the root-level licence. |
| RO-Crate and FAIR4ML | Model artefact path, model name, licence, creators, software requirements, training/evaluation scripts, training/test datasets, evaluation outputs, repository URL, DOI-related identifiers. | Full experiment graph, all source files, all generated figures, all reports, original STATS19 source dataset, authors as reusable graph nodes, provenance links across code and data. | ML-specific metadata: model category, ML task, algorithm, hyperparameters, intended use, model risks and limitations, ethical/social/legal notes, detailed evaluation metrics. | No unresolved conflict. Both standards now reference the same TUWRD model DOI, `https://doi.org/10.70124/m2a28-1q780`. The standards differ mainly in scope: RO-Crate describes the whole research object, while FAIR4ML describes the model in detail. |
| RO-Crate and Croissant | Dataset name, description, licence, source URL, publisher/creator, data files, field names, field descriptions, data types, units, semantic mappings, temporal and spatial context. | Experiment-wide provenance, code, notebooks, trained model, model outputs, authors, generated figures, reports, software licences, Zenodo and TUWRD identifiers. | Dataset-structure metadata: `cr:distribution`, `cr:recordSet`, `cr:field`, `cr:dataType`, field-level `sameAs`, QUDT units, record-set source mappings. | The Croissant dataset name is `UK STATS19 Road Safety Data 2023`, while RO-Crate uses `STATS19 Road Accident Severity ML Experiment` for the package and separate file names for raw datasets. This is complementary rather than conflicting, but the different levels of description should be clear in the final report. |
| RO-Crate and Model Card | Model name, model artefact path, dataset source, training and evaluation pipeline, evaluation metrics, output artefacts, licences, DOI references, intended use and limitations through related metadata. | Machine-readable graph of all project entities, file-level identifiers, formal relationships between scripts, inputs, outputs, and metadata artefacts. | Human-readable narrative sections: model description, intended use, out-of-scope uses, training data, evaluation results, limitations, ethical considerations, and licence explanation. | No unresolved conflict. The Model Card now distinguishes the input features from the target label `casualty_severity`, and its model DOI is aligned with RO-Crate. |
| CodeMeta and FAIR4ML | Name/description, version, repository URL, authors/creators, ORCIDs, programming language, runtime/software requirements, licence, model/software identity. | Software package metadata: issue tracker, software-level dependency list, software licence as SPDX/MIT, compact CodeMeta 2.0 representation. | ML-model metadata: model category, task, algorithm, hyperparameters, trained/validated/tested datasets, evaluation metrics, intended use, risk/limitation notes, ethical/social/legal notes. | CodeMeta applies to the code and uses MIT, while FAIR4ML applies to the trained model artefact and uses CC BY 4.0. This is not a conflict if the scope is explicit, but it must not be read as one licence applying to every artefact. |
| CodeMeta and Croissant | Name/description at a high level, licence information, creator/author concepts, repository or source URL concepts, keywords/domain context. | Software-specific metadata: programming language, dependencies, code repository, issue tracker, software version, MIT software licence. | Dataset-specific metadata: dataset distributions, record sets, fields, data types, units, semantic mappings, publisher, temporal coverage, spatial coverage, source file URLs. | CodeMeta describes the repository software, while Croissant describes the input dataset. They therefore use different licences: MIT for code and OGL-UK-3.0 for STATS19 data. This is expected and complementary. |
| CodeMeta and Model Card | Project/model title, description, authors indirectly via project context, repository/software workflow, dependencies or implementation context, licence discussion. | Formal machine-readable software metadata such as `softwareRequirements`, `programmingLanguage`, `codeRepository`, `issueTracker`, and software licence. | Human-readable ML governance information: intended use, out-of-scope uses, training data description, evaluation table, limitations, ethical considerations, and produced-output licence discussion. | CodeMeta names the software project `Crash Severity Prediction for Emergency Dispatch`, while the Model Card names the model `STATS19 Road Accident Severity Random Forest Model 2023 V1`. These are different but compatible levels of description. |
| FAIR4ML and Croissant | Dataset references, dataset descriptions, data source, licence concepts, field/feature context, model input data, evaluation data, machine-readable JSON-LD structure, use of schema.org-style identifiers. | Model-specific metadata: algorithm, model category, hyperparameters, trained/validated/tested datasets, evaluation metrics, intended use, risks/limitations, ethical/social/legal notes, model artefact path. | Dataset-specific metadata: distributions, record sets, field-level data types, semantic mappings, QUDT units, temporal/spatial coverage, publisher and original data source URLs. | FAIR4ML refers to processed train/validation/test split files, while Croissant describes the original collision, vehicle, and casualty input datasets. This is complementary, but the final report should state that Croissant documents input data and FAIR4ML documents the trained model and its processed splits. |
| FAIR4ML and Model Card | Model name, model artefact path, algorithm, software requirements, training data, validation/test data, evaluation metrics, intended use, limitations, ethical/legal/social considerations, licence, DOI references. | Machine-readable JSON-LD fields for automated discovery and interoperability, including hyperparameters as structured `PropertyValue` entries and evaluation metrics as structured values. | Human-readable narrative and interpretation, including out-of-scope uses, explanation of class imbalance, evaluation interpretation, and licence discussion in prose. | No unresolved conflict. FAIR4ML and the Model Card now use the same model DOI. The Model Card includes richer human interpretation than FAIR4ML, so it should be treated as explanatory rather than contradictory. |
| Croissant and Model Card | Dataset name/source, publisher/source organization, licence, training data context, feature and target concepts, temporal scope, road-safety domain, input-data provenance. | Machine-readable dataset structure: file distributions, record sets, field names, field descriptions, data types, semantic mappings, units, temporal and spatial coverage. | Human-readable model documentation: model description, intended and out-of-scope uses, evaluation results, limitations, ethics, model artefact DOI, generated output DOI. | Croissant covers raw input datasets, while the Model Card discusses processed training/evaluation data. This difference is expected, but the final report should make clear that the Model Card does not replace field-level dataset metadata. |

## Discussion

The standards are complementary because they describe different layers of the
same experiment. RO-Crate acts as the packaging and provenance layer: it links
datasets, scripts, notebooks, the trained model, generated outputs, licences,
authors, and related metadata files in one graph. CodeMeta is narrower and
focuses on the software component of the repository, especially the programming
language, repository URL, dependencies, version, and software licence.

Croissant provides the richest description of the input datasets. It documents
the STATS19 collision, vehicle, and casualty tables at field level, including
record sets, field names, data types, semantic mappings, and units. This is
information that the model-focused standards do not describe in the same level
of detail. FAIR4ML complements Croissant by documenting the trained model rather
than the raw input data. It records the model category, ML task, algorithm,
hyperparameters, processed train/validation/test datasets, evaluation metrics,
intended use, risks, limitations, and legal or ethical considerations.

The Model Card overlaps most strongly with FAIR4ML, because both describe the
trained model, its intended use, its evaluation results, and its limitations.
The difference is format and audience: FAIR4ML is structured JSON-LD intended
for machine-actionable metadata exchange, while the Model Card is a readable
governance document for humans. Together, they make the model easier to assess
both automatically and manually.

The consistency check found no remaining material conflicts between the five
standards after cleanup. The model DOI is aligned across RO-Crate, FAIR4ML, and
the Model Card. RO-Crate contains a single FAIR4ML file entity and uses
`subjectOf` to connect the model artefact to the FAIR4ML metadata. The Model
Card also now distinguishes the input features from the target label
`casualty_severity`, which avoids confusion between predictors and the class
being predicted.

Overall, the overlap is useful rather than wasteful. Repeated fields such as
title, description, authors, licences, dataset references, model path, and
evaluation outputs create cross-checks between standards. Unique fields add
coverage for different FAIR aspects: Croissant improves interoperability of the
data, CodeMeta improves software reuse, FAIR4ML improves model transparency,
the Model Card improves human assessment of risks and use limitations, and
RO-Crate ties the full research object together.
