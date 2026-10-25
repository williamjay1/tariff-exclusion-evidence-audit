[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23641463.svg)](https://doi.org/10.5281/zenodo.23641463)

# Tariff exclusion evidence audit: source to input protocol

Reproducibility package for **Auditing evidence construction in legal AI
evaluation: a source to input protocol for tariff exclusion decisions**, by
Junjie Zhang (Shanghai International Studies University). It contains the
retained source records, the constructed diagnostic inputs, the saved model
replies, the verification scripts and the manuscript sources behind every count
reported in the article.

This is a research audit of evidence construction. It is not a customs decision
system, not a legal opinion and not a validated compliance tool. The condition
coding was produced with AI assistance and has no independent customs or trade
law expert validation; the article states that boundary explicitly.

## Licence and citation

Original software is released under the MIT licence (`LICENSE`). Author-created
condition records, inventory readings, constructed inputs, analysis outputs and
figure artwork are offered under CC BY 4.0 to the extent of the author's rights
(`DATA_LICENSE.md`). The official rulings, notices and reports are U.S.
Government works and stay in the public domain; they are included as
byte-identical snapshots so that every span can be rechecked.

Cite this package with `CITATION.cff`, or cite the Zenodo version DOI once the
archived release is deposited. The Zenodo record mirrors the tagged release of
this repository.

The main article and supplement sources are in `manuscript/`; their editable
Word versions and the cover letter are in `deliverables/`. The three figures are
in `artwork/figures/` as editable SVG, vector PDF and native 1200 dpi PNG. The
raster resolution is an export setting, not an interpolation of a low-resolution
image; the vectors are resolution independent.

## Verify the retained results

Clone or unpack the repository into any writable local directory. Python 3.10 or
newer with its standard library is sufficient. No packages, network connection,
model weights, GPU, original drive letters or original source repository are
required. Run the following command from the folder containing this README.

```text
python scripts/verify_package.py --root .
```

The verifier checks every payload file against `package_manifest.json`, copies
of all 67 official ruling snapshots against their retained raw and UTF-8 text
hashes, the exact source spans including the two noncontinuous fact entries,
208 condition records and their case aggregation, 397 inventory records and
1,096 coarse source-anchored groups, and the arithmetic of the declared
interpretation policies. It verifies the formal input freezes and re-parses
the saved model replies independently of the experiment evaluator. The recount
includes qualification, corrected constructed references, the original frozen
reference, exclusion of the entire frame-species family, and the eight real
source-restoration endpoints. It also checks the nested legacy archive and
the three native 1200 dpi raster exports. The command above repeats these checks offline
and prints its own report.

This operation **recomputes scores from retained replies**. It does **not** run
new model inference, establish legal correctness, or independently authenticate
the historical receipt of a website response. The archive makes the provenance
and calculations inspectable. AI-coded references are neither human expert gold
labels nor an independent assessment of legal truth. The source audit was
outcome-exposed and retrospective, and its uncertainty tiers remain explicit.

## What is where

* `public_sources/` contains byte-identical copies of the 67 official public CBP
  JSON snapshots. `packaged_source_map.json` maps ruling IDs to package-relative
  files. Historical original paths remain in provenance manifests, but the
  offline verifier resolves sources through this package map.
* `source_audit/` contains all 208 source-coded condition units, 73 case records,
  source manifests, recovered attributes, interpretation options and the
  explicit policy packages. Exact span checks establish traceability, not the
  truth of an AI's interpretation of the quoted words.
* `inventory_audit/` contains the 397 separate readings and their coarse groups.
  These groups are not certified atomic necessary conditions or a complexity
  scale. Code-only entries retain their identity and date gates.
* `experiments/` contains frozen inputs, supplied interpretations, all scripts,
  prompts, schemas, raw replies, logs, qualification/development runs, the
  stopped unpooled pilot, the annotation erratum, and final analyses. The new
  constructed test uses 108 unique inputs and 96 relationships sharing
  endpoints. Its twelve two-condition families are functional probes, not a
  representative independent sample of legal disputes. The source-restoration
  test has four isolated conditions, eight endpoints, three rulings and three
  distinct restored sentences.
* `historical_inputs/evidence_numeric/` preserves earlier reference versions,
  development repairs, analyses and frozen visible inputs. Older tests do not
  become held-out validation by inclusion in this package.
* `legacy/` contains the earlier 315-file reviewer ZIP unchanged. Its own guide
  and replay scripts describe the older predictions, permutations, bootstrap
  seeds, interface failures and diagnostics. The ZIP is kept nested to preserve
  its byte identity. The revised main text qualifies these historical results.
* `original_data/` preserves discovery, screening, rule, index and benchmark
  working data. The purposive sample is not a prospective importer file or an
  estimate of the universe of exclusion applications.
* `literature/` contains source metadata, verified bibliography and comparison
  notes. Downloaded full papers and extracted full-text copies are not
  redistributed. Follow their official links for the original publications.
* `verification/` and `scripts/` retain the content, provenance and numerical
  audits. Some historical or authoring scripts record original machine paths;
  `scripts/verify_package.py` is the portable offline entry point.

## Rebuilding the manuscript and figures

The Word documents are built from the Markdown sources with
`scripts/build_documents.py`; `requirements-optional.txt` lists the packages that
step needs. Figure regeneration additionally expects the author's plotting
house-style module, which is not redistributed; the three final figures are
provided in editable vector and native raster form, and `artwork/qa/` records
their export checks.

## Running new inference is a separate operation

Model weights and llama.cpp binaries are not redistributed. The exact official
publisher repository, revision, GGUF filename, byte size and SHA-256 are recorded
in `inference_environment_manifest.json` and the unmodified run-session records.
The formal model was Qwen3-14B Q4_K_M with a local llama.cpp CPU server, thinking
disabled, six threads, a 4096-token context, temperature zero and seed 20261023.
The full executable arguments and per-call token caps remain in the retained
logs and `experiments/METHOD_DETAILS.md`. To perform genuinely new inference,
obtain those official artifacts separately, verify their hashes, adapt the
runner's model/runtime paths to the new machine, use the frozen protocol and
inputs, and save outputs under a new run directory rather than overwriting the
retained responses. Numerical determinism across different runtimes or hardware
is not promised. New outputs must be scored and identified as a new run.

`package_manifest.json` hashes every other payload file, including this README,
the model/environment manifest and the build-time verification report. A manifest
cannot contain its own content hash, so its one self-exclusion is explicit.
The outer ZIP's SHA-256 is provided in the accompanying `.sha256` text file.

No data were externally published or automatically archived to another drive by
this packaging step. Original raw documents and prior artifacts were read only.
