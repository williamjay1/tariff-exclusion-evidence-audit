"""Cross-tabulate unresolved evidence causes with declared policy switches.

Reads only frozen source-audit outputs. For the strict unknown conditions in
the 47 historically unknown cases it reports which units a source restoration
repairs, which a declared interpretation option can settle, and which no
declared operation changes. No administrative outcome is read, no new
annotation is made, and no rate is inferred for any larger population.
"""
from collections import Counter
import json

from build_source_audit import OUT, readl, dump
from finish_audit_report import GROUPS


def options(row):
    """Reachable states under an explicitly recorded option, plus withholding."""
    out = {'withhold_interpretation': row['strict_excerpt_state']}
    if row['reference_tier'] in ('interpretive', 'disputed'):
        for option in row['interpretation_options']:
            out[option['policy']] = option['state']
    return out


def main():
    rows = readl(OUT / 'condition_audit_long.jsonl')
    cases = readl(OUT / 'case_audit.jsonl')
    unknown_cases = [c for c in cases if c['historical_operational_case_state'] == 'unknown']
    unknown_ids = {c['case_id'] for c in unknown_cases}
    assert len(unknown_cases) == 47
    unit_rows = [r for r in rows if r['case_id'] in unknown_ids
                 and r['strict_excerpt_state'] == 'unknown']
    assert len(unit_rows) == 67

    def repairs(row):
        restored = row['strict_full_source_state'] != 'unknown'
        switched = any(s != 'unknown' for p, s in options(row).items()
                       if p != 'withhold_interpretation')
        return restored, switched

    for row in unit_rows:
        row['_restored'], row['_switched'] = repairs(row)

    unique_restored = sum(r['_restored'] for r in unit_rows)
    unique_switched = sum(r['_switched'] for r in unit_rows)
    both = sum(r['_restored'] and r['_switched'] for r in unit_rows)
    neither = sum(not (r['_restored'] or r['_switched']) for r in unit_rows)
    assert unique_restored + unique_switched - both + neither == 67
    assert unique_restored == 4, unique_restored

    groups = {}
    for name, reasons in GROUPS.items():
        members = [r for r in unit_rows if r['unknown_reason'] in reasons]
        groups[name] = {
            'cases': len({r['case_id'] for r in members}),
            'conditions': len(members),
            'restoration_repairs': sum(r['_restored'] for r in members),
            'option_repairs': sum(r['_switched'] for r in members),
            'no_declared_repair': sum(not (r['_restored'] or r['_switched']) for r in members),
        }

    sens = json.loads((OUT / 'policy_sensitivity.json').read_text(encoding='utf-8'))
    packages = {p['name']: {c['case_id']: c['state'] for c in p['cases']}
                for p in sens['explicit_policy_packages']}
    safe_unknown = [c for c in unknown_cases if c['safe_flat_conjunction']]
    assert len(safe_unknown) == 40
    movement = {}
    for name in ('declared_technical_scope_lab_peak',
                 'declared_alternative_material_use_party_nominal'):
        states = [packages[name][c['case_id']] for c in safe_unknown]
        movement[name] = dict(Counter(states))

    tiers = Counter(r['reference_tier'] for r in unit_rows)
    data = {
        'scope': 'ai-assisted source audit, frozen 23 October 2026',
        'historical_unknown_cases': 47,
        'conditions_in_those_cases': sum(len(c['condition_keys']) for c in unknown_cases),
        'strict_unknown_conditions': 67,
        'strict_unknown_by_tier': dict(tiers),
        'repaired_by_source_restoration': unique_restored,
        'settled_by_declared_interpretation_option': unique_switched,
        'both_operations_available': both,
        'no_declared_repair': neither,
        'by_cause_group': groups,
        'case_level': {
            'safe_conjunction_unknown_cases': len(safe_unknown),
            'logic_unresolved_unknown_cases': 7,
            'technical_package_states': movement['declared_technical_scope_lab_peak'],
            'alternative_package_states': movement['declared_alternative_material_use_party_nominal'],
        },
        'notes': [
            'Cause groups overlap; their condition counts sum above 67 and are not a partition.',
            'Restoration applies only to attributes that are directly described in the public ruling.',
            'An option repair needs a declared policy; the option itself is not adjudicated.',
            'No population rate, probability or legal authority is implied.',
        ],
    }
    dump(OUT / 'cross_tab_causes_policies.json', data)
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
