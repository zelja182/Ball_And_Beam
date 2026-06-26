import random
from pathlib import Path

base = Path(__file__).resolve().parents[2] / "Data" / "Encoder_data" / "Test_2"
out_dir = Path(__file__).resolve().parent

runs = []
for amp in ("Test_30", "Test_45"):
    proc = base / amp / "Processed"
    for f in sorted(proc.glob("Test_*.csv"), key=lambda p: int(p.stem.split("_")[1])):
        rel = f"../../Data/Encoder_data/Test_2/{amp}/Processed/{f.name}"
        runs.append({"amp": amp, "test": f.stem, "rel": rel})

random.seed(42)
shuffled = runs.copy()
random.shuffle(shuffled)

n_train = round(len(runs) * 0.75)
train = shuffled[:n_train]
val = shuffled[n_train:]

for split_name, items in [("train_list", train), ("validation_list", val)]:
    lines = [
        x["rel"]
        for x in sorted(items, key=lambda x: (x["amp"], int(x["test"].split("_")[1])))
    ]
    (out_dir / f"{split_name}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

summary = [
    "# Random split seed=42, 75% train / 25% validation",
    f"# Total runs: {len(runs)}",
    f"# Training: {len(train)}, Validation: {len(val)}",
    "",
    f"TRAINING ({len(train)}):",
]
for x in sorted(train, key=lambda x: (x["amp"], int(x["test"].split("_")[1]))):
    summary.append(f"  {x['amp']}/{x['test']}")
summary.append("")
summary.append(f"VALIDATION ({len(val)}):")
for x in sorted(val, key=lambda x: (x["amp"], int(x["test"].split("_")[1]))):
    summary.append(f"  {x['amp']}/{x['test']}")

(out_dir / "data_split_summary.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
print(f"Total runs: {len(runs)}")
print(f"Training: {len(train)}, Validation: {len(val)}")
print("Files written: train_list.txt, validation_list.txt, data_split_summary.txt")
