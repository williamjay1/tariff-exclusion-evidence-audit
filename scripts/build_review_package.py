"""Prepare the offline review package without changing any original source.

The default is a read-only plan. Use --build only after formal results, the
assembled manuscript, its two Word files, and all three figures are final.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import zipfile

REVISION = Path(__file__).resolve().parents[1]
PROJECT = REVISION.parent
LEGACY = PROJECT / "revision_20261009/reviewer_archive/Tariff_Exclusion_Anonymous_Review_20261009T113400_810289Z.zip"
LEGACY_SHA256 = "c484e64fd5a3d066ecc8c6488c70592bc5c5c0ab122d40e6cbd36e799c90eee6"
ALLOWED_TREE_SUFFIXES = {".md", ".json", ".jsonl", ".py", ".ps1", ".csv", ".tsv", ".txt", ".log", ".yaml", ".yml", ".toml", ".svg", ".pdf", ".png"}


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def copied_file(source, target):
    assert source.is_file(), str(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    assert not target.exists(), str(target)
    shutil.copyfile(source, target)
    assert sha(source) == sha(target), str(source)


def selected_files():
    selected = []
    # Only relevant revision payload; caches, raw copyrighted papers, weights,
    # render workspaces, and previous package builds never enter this list.
    for directory in ("manuscript", "scripts", "source_audit", "inventory_audit", "experiments", "literature", "verification", "artwork"):
        parent = REVISION / directory
        for p in sorted(parent.rglob("*")):
            if not p.is_file() or p.suffix.lower() not in ALLOWED_TREE_SUFFIXES:
                continue
            relative = p.relative_to(REVISION)
            lower = {part.lower() for part in relative.parts}
            if lower & {"__pycache__", "temp", "cache", "rendered", "extracted", "previews"}:
                continue
            if directory == "literature" and p.suffix.lower() not in {".md", ".json", ".jsonl", ".py"}:
                continue
            selected.append((p, relative))
    for p in sorted(REVISION.glob("*.md")) + sorted(REVISION.glob("*.json")):
        selected.append((p, Path(p.name)))
    for p in sorted((REVISION / "deliverables").glob("*.docx")) + sorted((REVISION / "deliverables").glob("Cover_Letter*.pdf")):
        selected.append((p, Path("deliverables") / p.name))
    # Original discovery/screening and frozen references remain distinguishable
    # from the revised AI source audit and the newly constructed diagnostics.
    for p in sorted((PROJECT / "datasets").iterdir()):
        if p.is_file() and p.suffix.lower() in {".json", ".jsonl", ".tsv"}:
            selected.append((p, Path("original_data") / p.name))
    for p in sorted((PROJECT / "revision_20261009/evidence_numeric").iterdir()):
        if p.is_file() and p.suffix.lower() in {".py", ".json", ".jsonl", ".md"}:
            selected.append((p, Path("historical_inputs/evidence_numeric") / p.name))
    assert len({str(destination) for _, destination in selected}) == len(selected)
    return selected


def readiness():
    required = ["manuscript/manuscript.md", "manuscript/supplement.md",
                "experiments/EXPERIMENT_RESULTS.md", "experiments/outputs/experiment_final_summary.json",
                "experiments/outputs/qwen14_controlled_cases_direct.jsonl",
                "experiments/outputs/qwen14_controlled_cases_checklist.jsonl",
                "experiments/outputs/qwen14_source_recovery_cases_direct.jsonl",
                "experiments/outputs/qwen14_source_recovery_cases_checklist.jsonl",
                "experiments/outputs/qwen14_controlled_cases_functional_analysis.json",
                "experiments/outputs/qwen14_controlled_cases_functional_analysis_frozen_reference.json",
                "experiments/outputs/qwen14_controlled_cases_functional_analysis_excluding_frame_species.json",
                "experiments/outputs/qwen14_source_recovery_cases_functional_analysis.json",
                "verification/final_delivery_audit.json",
                "scripts/verify_functional_results.py"]
    missing = [p for p in required if not (REVISION / p).is_file()]
    final_audit = REVISION / "verification/final_delivery_audit.json"
    if final_audit.is_file():
        audit = load(final_audit)
        if audit.get("status") != "PASS":
            missing.append("final_delivery_audit status PASS")
        for filename, expected in audit.get("files", {}).items():
            p = REVISION / "manuscript" / filename
            if not p.is_file() or sha(p) != expected:
                missing.append("final audited manuscript hash: " + filename)
    documents = [REVISION / "deliverables" / name for name in
                 ("Tariff_Evidence_Audit_20261023.docx", "Tariff_Evidence_Audit_Supplement_20261023.docx")]
    for document in documents:
        if not document.is_file():
            missing.append(str(document.relative_to(REVISION)))
    if not (REVISION / "deliverables" / "Cover_Letter_Tariff_Evidence_Audit.pdf").is_file():
        missing.append("deliverables/Cover_Letter_Tariff_Evidence_Audit.pdf")
    figure_pngs = list((REVISION / "artwork/figures").glob("*.png"))
    if len(figure_pngs) != 3:
        missing.append("exactly three artwork/figures/*.png")
    for figure in figure_pngs:
        for suffix in (".svg", ".pdf"):
            if not figure.with_suffix(suffix).is_file():
                missing.append(str(figure.with_suffix(suffix).relative_to(REVISION)))
    return missing


README = """# Tariff exclusion evidence audit: offline review package

This package accompanies the revised article *Auditing evidence construction in
legal AI evaluation: a source to input protocol for tariff exclusion decisions*.
The main article and supplement are in `manuscript/` and their editable Word
versions in `deliverables/`. A one page cover letter in PDF form is also in
`deliverables/`.
The three main figures have editable SVG, vector PDF, and native 1200 dpi PNG
versions in `artwork/figures/`. The raster resolution is an export setting, not
an interpolation of a low-resolution image. The vectors are resolution independent.

## Check the retained results

Extract the complete ZIP into any writable local directory. Python 3.10 or newer
with its standard library is sufficient. No packages, network connection, model
weights, GPU, original drive letters, or original source repository are required:
run the following command from the extracted folder containing this README.

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
the three native 1200 dpi raster exports. `package_verification.json` is the
build-time report; the command above independently repeats these offline checks.

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
"""


def environment_manifest():
    path = REVISION / "experiments/outputs/run_sessions.jsonl"
    sessions = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    # Preserve all fixed-model session configurations, including the stopped
    # pilot, rather than claiming only the last session ever occurred.
    return {"weights_redistributed": False, "runtime_binary_redistributed": False,
            "new_inference_performed_by_package_verification": False,
            "official_model_cards": ["https://huggingface.co/Qwen/Qwen3-14B-GGUF"],
            "protocol_method_file": "experiments/METHOD_DETAILS.md",
            "recorded_sessions": sessions,
            "scope": "Retained configuration and hashes permit preparation of a fresh run; offline score recount does not execute the model."}


def make_manifest(stage):
    files = [{"path": p.relative_to(stage).as_posix(), "bytes": p.stat().st_size, "sha256": sha(p)}
             for p in sorted(stage.rglob("*")) if p.is_file() and p.name != "package_manifest.json" and "__pycache__" not in p.parts]
    dump(stage / "package_manifest.json", {"schema_version": 1, "created_utc": datetime.now(timezone.utc).isoformat(),
         "manifest_self_exclusion": "package_manifest.json", "files": files,
         "boundary": "SHA-256 checks retained byte identity; scoring and legal validity are separate questions."})


def build():
    missing = readiness()
    assert not missing, "Final package not ready: " + "; ".join(missing)
    estimate = sum(source.stat().st_size for source, _ in selected_files()) * 3 + 100 * 1024 * 1024
    assert shutil.disk_usage(REVISION).free > estimate, "Insufficient space for verified package staging and ZIP on the current work drive"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    name = "Tariff_Evidence_Audit_Review_" + timestamp
    stage = REVISION / "review_packages" / name
    assert not stage.exists()
    stage.mkdir(parents=True)
    for source, destination in selected_files():
        copied_file(source, stage / destination)
    packaged_sources = []
    for item in load(REVISION / "source_audit/source_manifest.json")["sources"]:
        source = Path(item["raw_path"])
        assert sha(source) == item["raw_sha256"], str(source)
        raw = load(source)
        assert hashlib.sha256(raw["text"].encode("utf-8")).hexdigest() == item["text_sha256"]
        relative = Path("public_sources") / (item["ruling_id"] + ".json")
        copied_file(source, stage / relative)
        packaged_sources.append({"ruling_id": item["ruling_id"], "official_url": item["official_url"],
                                 "packaged_path": relative.as_posix(), "raw_sha256": item["raw_sha256"],
                                 "text_sha256": item["text_sha256"]})
    dump(stage / "packaged_source_map.json", {"source_count": len(packaged_sources), "sources": packaged_sources,
         "scope": "Byte-identical copied snapshots of official public sources; original raw files not changed."})
    relative = Path("legacy") / LEGACY.name
    assert sha(LEGACY) == LEGACY_SHA256, "Legacy archive changed since the read-only package inspection"
    copied_file(LEGACY, stage / relative)
    with zipfile.ZipFile(LEGACY) as archive:
        assert archive.testzip() is None
        files = sum(not member.is_dir() for member in archive.infolist())
        assert files == 315
    dump(stage / "legacy_archive_manifest.json", {"packaged_path": relative.as_posix(), "bytes": LEGACY.stat().st_size,
         "sha256": sha(LEGACY), "file_count": files, "preservation": "Copied unchanged, not unpacked or rewritten."})
    dump(stage / "inference_environment_manifest.json", environment_manifest())
    (stage / "README.md").write_text(README, encoding="utf-8")
    checker = stage / "scripts/verify_package.py"
    spec = importlib.util.spec_from_file_location("build_time_package_checker", checker)
    module = importlib.util.module_from_spec(spec)
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
        report = module.verify(stage, skip_integrity=True)
        dump(stage / "package_verification.json", report)
        make_manifest(stage)
        final_report = module.verify(stage)
    finally:
        sys.dont_write_bytecode = previous
    target = REVISION / "deliverables" / (name + ".zip")
    assert not target.exists()
    with zipfile.ZipFile(target, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for p in sorted(stage.rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts:
                archive.write(p, Path(name) / p.relative_to(stage))
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
    checksum = sha(target)
    target.with_suffix(".zip.sha256").write_text(checksum + "  " + target.name + "\n", encoding="ascii")
    summary = {"status": "PASS", "zip_path": str(target), "zip_bytes": target.stat().st_size,
               "zip_sha256": checksum, "staging_path": str(stage),
               "payload_files": final_report["integrity"]["files_verified"],
               "scope": "Offline integrity/provenance and retained-response recount verified; no new inference or legal gold certification."}
    dump(REVISION / "verification/review_package_build.json", summary)
    print(json.dumps(summary, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", action="store_true", help="Construct and verify the final package; default only inspects readiness")
    args = parser.parse_args()
    if not args.build:
        selected = selected_files()
        missing = readiness()
        print(json.dumps({"mode": "READ_ONLY_PLAN", "final_package_ready": not missing,
                          "missing_prerequisites": missing, "selected_existing_files": len(selected),
                          "selected_existing_bytes": sum(p.stat().st_size for p, _ in selected),
                          "official_sources_to_copy": 67, "legacy_zip_sha256": sha(LEGACY),
                          "writes_performed": False}, indent=2))
        return
    build()


if __name__ == "__main__":
    main()
