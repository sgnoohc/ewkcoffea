import json
import pandas as pd

# Load the JSON file
with open("vvh_yields_sig_bkg.json", "r") as f:
    json_data = json.load(f)

# Extract the yields
yields = json_data["yields"]

# Build a table with three columns per process: val, ±, err
rows = []
index = []

for cut, processes in yields.items():
    row = {}
    for proc, values in processes.items():
        if isinstance(values, list) and len(values) >= 2 and values[1] is not None:
            row[f"{proc}_val"] = f"{values[0]:.4f}"
            row[f"{proc}_pm"] = "±"
            row[f"{proc}_err"] = f"{values[1]:.4f}"
    rows.append(row)
    index.append(cut)

# Create DataFrame
df = pd.DataFrame(rows, index=index)

# # Get unique process names
# all_procs = {col.split('_')[0] for col in df.columns}
# # Remove 'background' and 'signal' for manual ordering
# main_procs = sorted(p for p in all_procs if p not in {"background", "signal"})
# ordered_procs = main_procs + ["background", "signal"]

ordered_procs = ["QCD", "Vjets", "VV", "VVV", "VH", "single-t", "ttbar", "ttX", "background", "signal"]

# Construct column order: val, ±, err for each process
ordered_cols = []
for proc in ordered_procs:
    ordered_cols.extend([f"{proc}_val", f"{proc}_pm", f"{proc}_err"])

# Reorder DataFrame columns
df = df.reindex(columns=ordered_cols)

# Save to CSV
df.to_csv("cutflow_yield_padded_and_ordered.csv")

