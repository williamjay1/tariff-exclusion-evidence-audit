"""Offline integrity and score-recount entry point for the review package.

Python >= 3.10, standard library only. No model calls, network, or original
machine paths are used. This verifies retained records, not legal validity.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path, PureWindowsPath
import struct
import sys
import zipfile


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checked_path(root, relative):
    """Reject absolute paths, traversal and symlinks outside the package."""
    relative = relative.replace("\\", "/")
    p = Path(relative)
    assert not p.is_absolute() and ":" not in relative, relative
    assert ".." not in p.parts, relative
    destination = (root / p).resolve()
    assert destination.is_relative_to(root.resolve()), relative
    return destination


def integrity(root):
    manifest = load(root / "package_manifest.json")
    declared = {}
    for item in manifest["files"]:
        relative = item["path"]
        assert relative not in declared, (relative, "duplicate manifest entry")
        p = checked_path(root, relative)
        assert p.is_file(), (relative, "missing")
        assert p.stat().st_size == item["bytes"], (relative, "size mismatch")
        assert sha(p) == item["sha256"], (relative, "SHA-256 mismatch")
        declared[relative] = item
    actual = {
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file() and p.name != "package_manifest.json"
        and "__pycache__" not in p.parts
    }
    assert set(declared) == actual, {
        "unlisted": sorted(actual - set(declared)),
        "missing": sorted(set(declared) - actual),
    }
    assert manifest["manifest_self_exclusion"] == "package_manifest.json"
    return {"files_verified": len(declared), "bytes_verified": sum(v["bytes"] for v in declared.values())}


def sources_and_conditions(root):
    audit = root / "source_audit"
    original_manifest = load(audit / "source_manifest.json")["sources"]
    packaged = load(root / "packaged_source_map.json")["sources"]
    by_ruling = {r["ruling_id"]: r for r in packaged}
    assert len(by_ruling) == len(original_manifest) == 67
    texts = {}
    for original in original_manifest:
        item = by_ruling[original["ruling_id"]]
        assert item["raw_sha256"] == original["raw_sha256"]
        assert item["text_sha256"] == original["text_sha256"]
        p = checked_path(root, item["packaged_path"])
        assert sha(p) == item["raw_sha256"], item["ruling_id"]
        text = load(p)["text"]
        assert hashlib.sha256(text.encode("utf-8")).hexdigest() == item["text_sha256"]
        texts[item["ruling_id"]] = text

    visible = {r["case_id"]: r for r in rows(root / "historical_inputs/evidence_numeric/evidence_visible_inputs.jsonl")}
    condition_rows = rows(audit / "condition_audit_long.jsonl")
    case_rows = rows(audit / "case_audit.jsonl")
    summary = load(audit / "source_audit_summary.json")
    assert len(condition_rows) == 208 and len(case_rows) == 73
    assert len({r["condition_key"] for r in condition_rows}) == 208
    span_counts = Counter()

    def locator(loc, text, key):
        assert loc, (key, "empty locator")
        if loc.get("source_text_sha256"):
            assert loc["source_text_sha256"] == hashlib.sha256(text.encode("utf-8")).hexdigest(), key
        if loc.get("raw_text_span") is not None:
            start, end = loc["raw_text_span"]
            assert 0 <= start <= end <= len(text), key
            assert text[start:end] == loc["quote"], (key, "nonmatching source span")
            span_counts["continuous"] += 1
        elif loc.get("source_spans"):
            for part in loc["source_spans"]:
                locator(part, text, key)
            span_counts["noncontinuous_entries"] += 1
        else:
            raise AssertionError((key, "locator has no exact continuous or component spans"))

    by_case = defaultdict(list)
    for row in condition_rows:
        key = row["condition_key"]
        text = texts[row["ruling_id"]]
        original = visible[row["case_id"]]
        start, end = row["rule_span"]
        assert original["rule_text"][start:end] == row["rule_quote"], key
        locator(row["rule_source_locator"], text, key + ":rule")
        for fact in row["fact_evidence"]:
            start, end = fact["frozen_span"]
            assert original["facts"][start:end] == fact["frozen_quote"], key
            locator(fact["source_locator"], text, key + ":fact")
        for recovered in row["recovered_fact_evidence"]:
            locator(recovered, text, key + ":recovered")
        assert row["expert_validated"] is False
        assert row["administrative_y_used_as_criterion"] is False
        assert row["reference_tier"] in {"direct", "interpretive", "insufficient", "disputed"}
        assert row["object"]["product_scope"] and row["object"]["quantifier"]
        assert row["attribute"] and row["logical_role"] and row["inference_basis"]
        by_case[row["case_id"]].append(row)

    def aggregate(values):
        values = [v for v in values if v != "not_applicable"]
        return "refute" if "refute" in values else "support" if values and set(values) == {"support"} else "unknown"

    for case in case_rows:
        conditions = by_case[case["case_id"]]
        assert set(case["condition_keys"]) == {r["condition_key"] for r in conditions}
        for column in ("strict_excerpt_state", "strict_full_source_state"):
            expected = aggregate([r[column] for r in conditions]) if case["safe_flat_conjunction"] else "logic_unresolved"
            assert case[column] == expected, (case["case_id"], column)
    assert summary["reference_tier_counts"] == dict(Counter(r["reference_tier"] for r in condition_rows))
    assert summary["strict_excerpt_condition_counts"] == dict(Counter(r["strict_excerpt_state"] for r in condition_rows))
    assert summary["strict_full_condition_counts"] == dict(Counter(r["strict_full_source_state"] for r in condition_rows))
    assert summary["strict_case_full_counts"] == dict(Counter(r["strict_full_source_state"] for r in case_rows))
    restored = {r["condition_key"] for r in condition_rows if r["strict_excerpt_state"] == "unknown" and r["strict_full_source_state"] == "support"}
    assert restored == {"H330938_1:c4", "H322923_1:c2", "H340899_1:c3", "H340899_1:c4"}
    assert all(r["strict_excerpt_state"] == r["strict_full_source_state"] for r in case_rows)
    assert span_counts == {"continuous": 455, "noncontinuous_entries": 2}, span_counts
    return {"official_sources": 67, "condition_units": 208, "cases": 73,
            "source_span_checks": dict(span_counts), "reference_tiers": summary["reference_tier_counts"],
            "direct_attribute_restorations": sorted(restored)}, condition_rows, case_rows


def inventory_and_policy(root, conditions, cases):
    inventory = rows(root / "inventory_audit/inventory_structural_audit.jsonl")
    readings = rows(root / "inventory_audit/reviewed_condition_groups.jsonl")
    original_rules = rows(root / "original_data/statutory_rules.jsonl")
    assert len(inventory) == len(readings) == len(original_rules) == 397
    assert {r["index"] for r in inventory} == set(range(397))
    assert {r["index"] for r in readings} == set(range(397))
    spans = 0
    for item, reading, original in zip(inventory, readings, original_rules):
        assert item["rule_id"] == reading["rule_id"] == original["rule_id"]
        assert item["scope"] == reading["scope"] == original["scope"]
        assert hashlib.sha256(item["scope"].encode("utf-8")).hexdigest() == reading["scope_sha256"]
        assert item["actual_reviewed"] and reading["complete_coarse_reading_silver"]
        assert item["coarse_required_group_count"] == reading["coarse_required_group_count"] == len(reading["groups"])
        for group in reading["groups"]:
            assert item["scope"][group["start"]:group["end"]] == group["quote"]
            spans += 1
        if item["scope_format"].startswith("code_only"):
            assert not reading["groups"]
    assert spans == 1096
    assert Counter(r["scope_format"] for r in inventory) == {"code_only_single": 41, "code_only_dated_transition": 2, "product_description": 354}
    sensitivity = load(root / "source_audit/policy_sensitivity.json")
    condition_map = {r["condition_key"]: r for r in conditions}
    safe = {r["case_id"]: r for r in cases if r["safe_flat_conjunction"]}
    assert len(safe) == 58

    def aggregate(values):
        values = [v for v in values if v != "not_applicable"]
        return "refute" if "refute" in values else "support" if values and set(values) == {"support"} else "unknown"

    possible = {}
    for key, case in safe.items():
        options = []
        for condition_key in case["condition_keys"]:
            condition = condition_map[condition_key]
            states = {condition["strict_full_source_state"]}
            if condition["reference_tier"] in {"interpretive", "disputed"}:
                states |= {r["state"] for r in condition["interpretation_options"]}
            options.append(states)
        possible[key] = {aggregate(state) for state in product(*options)}
    for row in sensitivity["cases"]:
        assert set(row["possible_states"]) == possible[row["case_id"]]
    envelopes = {state: {"necessarily_this_state": sum(v == {state} for v in possible.values()),
                         "possibly_this_state": sum(state in v for v in possible.values())}
                 for state in ("support", "refute", "unknown")}
    assert envelopes == sensitivity["marginal_count_envelopes"]
    packages = []
    for policy in sensitivity["explicit_policy_packages"]:
        predicted = {}
        for key, case in safe.items():
            states = []
            for condition_key in case["condition_keys"]:
                condition = condition_map[condition_key]
                state = condition["strict_full_source_state"]
                if condition_key in policy["overrides"]:
                    assert condition["reference_tier"] in {"interpretive", "disputed"}
                    selected = policy["overrides"][condition_key]
                    state = next(r["state"] for r in condition["interpretation_options"] if r["policy"] == selected)
                states.append(state)
            predicted[key] = aggregate(states)
        assert dict(Counter(predicted.values())) == policy["counts"]
        assert predicted == {r["case_id"]: r["state"] for r in policy["cases"]}
        packages.append({"name": policy["name"], "counts": policy["counts"]})
    return {"inventory_rows": 397, "product_descriptions": 354, "coarse_groups": spans,
            "code_only_additional_product_groups_zero": 43, "safe_conjunction_cases": len(safe),
            "declared_policy_packages": packages, "marginal_envelopes": envelopes}


def experiment_freezes(root):
    experimental = root / "experiments"
    formal = load(experimental / "controlled_freeze.json")
    assert sha(experimental / "controlled_cases.jsonl") == formal["input_sha256"]
    for relative, expected in formal["hashes"].items():
        assert sha(checked_path(experimental, relative)) == expected, relative
    for item in formal["superseded_pilot_preserved"]:
        p = checked_path(experimental, item["path"])
        assert sha(p) == item["sha256"], item["path"]
        if item["jsonl_lines"] is not None:
            assert len(rows(p)) == item["jsonl_lines"]
    qualification = load(experimental / "qualification_manifest.json")
    for filename in ("development_cases.jsonl", "qualification_cases.jsonl"):
        assert sha(experimental / filename) == qualification[filename + "_sha256"]
    recovery = load(experimental / "source_recovery_freeze.json")
    for relative, expected in recovery["hashes"].items():
        assert sha(checked_path(root, relative)) == expected, relative
    formal_rows = rows(experimental / "controlled_cases.jsonl")
    links = rows(experimental / "constructed_pairs.jsonl")
    spans = rows(experimental / "constructed_source_spans.jsonl")
    assert len(formal_rows) == 108 and len(links) == 96 and len(spans) == 12
    by_id = {r["case_id"]: r for r in formal_rows}
    assert len(by_id) == 108
    assert len({r["family"] for r in formal_rows}) == 12
    for row in formal_rows:
        assert row["constructed"] is True
        assert row["rule_text"] == "Controlled two-condition clause: " + row["conditions"][0]["requirement"] + " AND " + row["conditions"][1]["requirement"]
    for span in spans:
        for selected in span["selected_rule_quotes"]:
            start, end = selected["span"]
            assert span["full_original_rule"][start:end] == selected["quote"]
    for link in links:
        left, right = by_id[link["left"]], by_id[link["right"]]
        assert left["family"] == right["family"] == link["family"]
        assert (left["expected"]["decision"] == right["expected"]["decision"]) == (link["expected_relation"] == "same")
    return {"controlled_inputs": 108, "dependent_relations": 96, "source_families": 12,
            "source_recovery_endpoints": 8, "frozen_input_hashes": "PASS", "superseded_unpooled_pilot": 3}


def functional_recount(root):
    """Use the independent raw-JSON scorer, never the experiment evaluator."""
    path = root / "scripts/verify_functional_results.py"
    spec = importlib.util.spec_from_file_location("package_independent_functional_recount", path)
    module = importlib.util.module_from_spec(spec)
    # Avoid a pycache payload appearing after integrity verification.
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
        assert module.R.resolve() == root.resolve()
        reports = [module.check_analysis("qualification_cases"),
                   module.check_analysis("controlled_cases", erratum=True, pairs=True),
                   module.check_analysis("controlled_cases", "frozen_reference", pairs=True),
                   module.check_analysis("controlled_cases", "excluding_frame_species", erratum=True, exclude=True, pairs=True),
                   module.check_analysis("source_recovery_cases")]
    finally:
        sys.dont_write_bytecode = previous
    return {"mode": "saved_reply_recount_only", "network_or_inference": False, "reports": reports}


def final_summary_and_restoration(root):
    experimental = root / "experiments"
    output = experimental / "outputs"
    summary = load(output / "experiment_final_summary.json")
    assert summary["status"] == "complete"
    assert set(summary["datasets"]) == {"qualification_cases", "controlled_cases", "source_recovery_cases"}
    for dataset, saved in summary["datasets"].items():
        source = experimental / (dataset + ".jsonl")
        assert saved["input_sha256"] == sha(source)
        assert saved["n"] == len(rows(source))
        assert saved["analysis"] == load(output / ("qwen14_" + dataset + "_functional_analysis.json"))
        for kind, recorded in saved["arms"].items():
            p = output / ("qwen14_" + dataset + "_" + kind + ".jsonl")
            raw = rows(p)
            assert recorded["sha256"] == sha(p) and recorded["n"] == len(raw)
            assert abs(recorded["request_seconds"] - sum(r.get("seconds", 0) for r in raw)) < 1e-6
            assert recorded["invalid"] == sum(not r.get("valid") for r in raw)
            assert recorded["incomplete"] == sum(not r.get("complete_condition_ids", True) for r in raw)
            assert recorded["truncation"] == sum(bool(r.get("truncated") or r.get("stopped_limit")) for r in raw)
            assert recorded["output_tokens"] == sum(r.get("output_tokens", 0) or 0 for r in raw)
        for tag, sensitivity in saved.get("reference_sensitivity", {}).items():
            assert sensitivity == load(output / ("qwen14_" + dataset + "_functional_analysis_" + tag + ".json"))
    recovery = rows(experimental / "source_recovery_cases.jsonl")
    assert len(recovery) == 8
    assert len({r["source_condition_key"] for r in recovery}) == 4
    assert len({r["group"] for r in recovery}) == 3
    assert len({r["source_recovered_span"]["quote"] for r in recovery}) == 3
    visible = {r["case_id"]: r for r in rows(root / "historical_inputs/evidence_numeric/evidence_visible_inputs.jsonl")}
    source_map = {r["ruling_id"]: r for r in load(root / "packaged_source_map.json")["sources"]}
    for row in recovery:
        span = row["source_recovered_span"]
        text = load(checked_path(root, source_map[row["group"]]["packaged_path"]))["text"]
        start, end = span["raw_text_span"]
        assert text[start:end] == span["quote"]
        assert row["facts"][0] == {"id": "f1", "text": visible[row["source_case_id"]]["facts"]}
        if row["variant"] == "before":
            assert len(row["facts"]) == 1 and row["expected"]["decision"] == "unknown"
        else:
            assert row["variant"] == "after" and row["expected"]["decision"] == "supported"
            assert row["facts"][1] == {"id": "f2", "text": span["quote"]}
    pair_rows = rows(experimental / "source_recovery_pairs.jsonl")
    assert len(pair_rows) == 4
    references = {r["case_id"]: r["expected"]["decision"] for r in recovery}
    analysis = load(output / "qwen14_source_recovery_cases_functional_analysis.json")
    successes = {}
    for kind in ("direct", "checklist"):
        raw = rows(output / ("qwen14_source_recovery_cases_" + kind + ".jsonl"))
        actual = {r["case_id"]: r["parsed"]["decision"] if r.get("valid") and not r.get("stopped_limit") and not r.get("truncated") else None for r in raw}
        records = []
        for pair in pair_rows:
            left, right = actual[pair["left"]], actual[pair["right"]]
            correct = left == references[pair["left"]] and right == references[pair["right"]]
            relation = (left == right) if pair["expected_relation"] == "same" else (left != right)
            records.append({**pair, "both_correct": bool(correct), "expected_relation_observed": bool(relation), "success": bool(correct and relation)})
        recorded = analysis["reports"][kind]["pairs"]
        assert recorded["n"] == 4 and recorded["success"] == sum(r["success"] for r in records)
        assert recorded["records"] == records
        successes[kind] = {"n": 4, "success": recorded["success"]}
    return {"complete_final_summary_matches_analyses_and_raw_outputs": True,
            "restoration_pairs_recount": successes, "isolated_conditions": 4,
            "rulings": 3, "unique_restored_sentences": 3}


def png_metadata(path):
    width = height = None
    density = None
    with path.open("rb") as stream:
        assert stream.read(8) == b"\x89PNG\r\n\x1a\n", path.name
        while True:
            header = stream.read(8)
            if not header:
                break
            length, kind = struct.unpack(">I4s", header)
            data = stream.read(length)
            assert len(data) == length
            stream.read(4)
            if kind == b"IHDR":
                width, height = struct.unpack(">II", data[:8])
            elif kind == b"pHYs":
                x, y, unit = struct.unpack(">IIB", data)
                if unit == 1:
                    density = [round(x * 0.0254, 3), round(y * 0.0254, 3)]
            elif kind == b"IEND":
                break
    assert width and height and density and min(density) >= 1199, (path.name, density)
    return {"file": path.name, "pixels": [width, height], "dpi": density}


def deliverables(root):
    assert (root / "manuscript/manuscript.md").is_file()
    assert (root / "manuscript/supplement.md").is_file()
    documents = sorted((root / "deliverables").glob("*.docx"))
    article = [p for p in documents if p.name in {"Tariff_Evidence_Audit_20261023.docx", "Tariff_Evidence_Audit_Supplement_20261023.docx"}]
    assert len(article) == 2, "Expected the article and supplement Word files"
    assert (root / "deliverables/Cover_Letter_Tariff_Evidence_Audit.pdf").is_file()
    docx = []
    for p in article:
        with zipfile.ZipFile(p) as archive:
            assert archive.testzip() is None
            assert "word/document.xml" in archive.namelist()
            assert "[Content_Types].xml" in archive.namelist()
        docx.append(p.name)
    final_audit = load(root / "verification/final_delivery_audit.json")
    assert final_audit["status"] == "PASS" and final_audit["critique_items_closed"] == 42
    for filename, expected in final_audit["files"].items():
        assert sha(root / "manuscript" / filename) == expected
    for audited in load(root / "verification/docx_content_audit.json"):
        assert audited["paragraphs_exact"] and audited["table_cells_exact"]
        # Original Windows paths are historical metadata only, never resolved.
        filename = PureWindowsPath(audited["output"]).name
        assert sha(root / "deliverables" / filename) == audited["sha256"]
    figure_dir = root / "artwork/figures"
    figures = sorted(figure_dir.glob("*.png"))
    assert len(figures) == 3, "Expected three main figures"
    png = []
    for p in figures:
        assert p.with_suffix(".svg").is_file() and p.with_suffix(".pdf").is_file(), p.name
        assert b"<svg" in p.with_suffix(".svg").read_bytes()[:2000], p.name
        assert p.with_suffix(".pdf").read_bytes().startswith(b"%PDF-"), p.name
        png.append(png_metadata(p))
    legacy = load(root / "legacy_archive_manifest.json")
    p = checked_path(root, legacy["packaged_path"])
    assert sha(p) == legacy["sha256"]
    with zipfile.ZipFile(p) as archive:
        assert archive.testzip() is None
        count = sum(not member.is_dir() for member in archive.infolist())
        assert count == legacy["file_count"]
    return {"editable_documents": docx, "three_vector_and_1200dpi_figures": png,
            "unchanged_legacy_archive_files": count, "legacy_archive_sha256": legacy["sha256"]}


def verify(root, skip_integrity=False):
    root = root.resolve()
    report = {"status": "PASS", "verification_scope": "Offline integrity, source provenance, declared-policy arithmetic, and saved-output score recount; no fresh model inference or expert legal validation."}
    if not skip_integrity:
        report["integrity"] = integrity(root)
    report["sources"], conditions, cases = sources_and_conditions(root)
    report["inventory_and_policy"] = inventory_and_policy(root, conditions, cases)
    report["experimental_freezes"] = experiment_freezes(root)
    report["functional_results"] = functional_recount(root)
    report["final_summary_and_restoration"] = final_summary_and_restoration(root)
    report["deliverables"] = deliverables(root)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.root), indent=2, ensure_ascii=False))
    except (AssertionError, OSError, ValueError, KeyError, StopIteration) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, indent=2), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
