#%%
import datetime
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

csv_file = Path("voluflow_log_20250722_034441_064056.csv")

timestampColumn = "Timestamp"
df = pd.read_csv(csv_file, parse_dates=[timestampColumn])

print(df.columns)

resample = 1
figsize = (16,8)
cols = ["vflow"]

df2 = df[[timestampColumn]+cols]
df2["TimeSeconds"] = (df2[timestampColumn] - df2[timestampColumn].iloc[0]).dt.total_seconds()
df2 = df2.set_index(timestampColumn).resample(f"{resample}s").mean().ffill()

plt.figure(figsize=figsize)

# Plot all variables (except timestamp)
for col in cols:
    plt.plot(df2["TimeSeconds"], df2[col], label=col)

plt.xlabel("Time (s)")
plt.ylabel("Value")
plt.title(f"{csv_file.stem}")
plt.legend()
plt.grid(True, which="both")
