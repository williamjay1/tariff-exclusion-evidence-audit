# Old numeric guard: refutation-loss reconstruction

{
  "reference": "Prior AI-assisted diagnostic evidence states; pending new source re-audit. No expert gold assumed.",
  "input_hashes": {
    "reference": "26c385ace3791574481ffa42f86239823aaf524adec1bd83727f8eedbd8319a0",
    "qwen4": "5488e71589b1432b262aec0af9ace8fa1feae393483e47d231141d329fc3a787",
    "numeric": "ec25de66aa220c089318629e17f0574bf7e1ef18af63cc29b342a33c972e28ad",
    "benchmark": "8e33bb2381212c5a29b63ce1c9fdbcbb1a0ae6c3d228097c748529934589a3f9"
  },
  "n_refuted": 5,
  "raw_correct": 3,
  "old_guard_correct": 1,
  "lost_raw_refutations": [
    "H318593_2",
    "N307161"
  ],
  "logic_rule": "A verified refutation of any mandatory conjunct dominates unrelated missing conditions. An unsupported model-negative may instead be referred under an explicit trust policy.",
  "proposed_diagnostic": "Measure whether independent condition evidence verifies each old lost negative; do not preserve arbitrary model negatives by definition."
}

## H336040_1
Raw 0 -> guard 0; numerical state not_parsed.
Rule: of metal and high-pressure laminated bamboo
Evidence: [{"quote": "are unfinished because they are imported without their countertops.", "span": [2800, 2867]}]
Prior rationale: The goods as imported lack countertops; the only future bamboo component is attached after importation.

## H318593_2
Raw 0 -> guard -1; numerical state unknown.
Rule: lifting capacity of not more than 550 kg
Evidence: [{"quote": "lifting capacity of 6,000 pounds", "span": [236, 268]}]
Prior rationale: 6000 international avoirdupois pounds = 2721.55422 kg; this exceeds 550 kg.

## N307161
Raw 0 -> guard -1; numerical state unknown.
Rule: measuring 148mm in length, 43 mm in width and 335 mm in height
Evidence: [{"quote": "measuring 140 mm by 150 mm by 86 mm", "span": [160, 195]}]
Prior rationale: No permutation of the three actual enclosure dimensions equals the specified dimensions.

## N311039_33
Raw 1 -> guard -1; numerical state unknown.
Rule: for a voltage exceeding 60 V but not over 250 V
Evidence: [{"quote": "coil voltage rating of 12 VAC", "span": [425, 454]}, {"quote": "contact voltage rating of 277 VAC", "span": [461, 494]}]
Prior rationale: For the first relay, both 12 V coil and 277 V contact ratings violate (60,250] V; further listed relays likewise violate both alternatives. Do not replace these discrete, per-product alternatives by a continuous hull.

## N329172
Raw -1 -> guard -1; numerical state not_parsed.
Rule: Tire carrier attachments, roof racks, fender liners, side protective attachments
Evidence: [{"quote": "components that are used to make a sound/speaker bar housing", "span": [37, 97]}]
Prior rationale: A speaker-bar housing does not have any of the listed carrier/protective functions in the described use.
Rule: the foregoing of steel
Evidence: [{"quote": "made of acrylonitrile styrene acrylate (ASA) plastic", "span": [437, 489]}]
Prior rationale: The visible facts explicitly conflict with this condition.
